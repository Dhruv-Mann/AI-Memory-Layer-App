import { writable } from 'svelte/store';
import { browser } from '$app/environment';

export interface WindowState {
	x: number;
	y: number;
	width: number;
	height: number;
	monitorIndex: number;
}

const STORAGE_KEY = 'ai-memory-layer:window-state';

export const windowStateStore = writable<WindowState | null>(null);

function detectMonitorIndex(x: number): number {
	if (!browser) return 0;
	// Heuristic: If window coordinates are negative or exceed primary monitor width,
	// it's likely placed on secondary/adjacent displays.
	const primaryWidth = window.screen.width || 1920;
	if (x < 0) return -1; // Left Monitor
	if (x >= primaryWidth) return 1; // Right Monitor
	return 0; // Primary Monitor
}

export function initWindowTracker() {
	if (!browser) return;

	const saveState = () => {
		const state: WindowState = {
			x: window.screenX,
			y: window.screenY,
			width: window.outerWidth,
			height: window.outerHeight,
			monitorIndex: detectMonitorIndex(window.screenX)
		};
		localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
		windowStateStore.set(state);
	};

	// Attempt coordinates restore from localStorage on launch
	const stored = localStorage.getItem(STORAGE_KEY);
	if (stored) {
		try {
			const parsed = JSON.parse(stored) as WindowState;
			windowStateStore.set(parsed);
			
			// Non-destructive check: only trigger resizeTo/moveTo if coordinates are finite
			if (
				typeof parsed.width === 'number' && 
				typeof parsed.height === 'number' && 
				typeof parsed.x === 'number' && 
				typeof parsed.y === 'number'
			) {
				// Secure browsers may block this, but we attempt it for compliant runtimes
				window.resizeTo?.(parsed.width, parsed.height);
				window.moveTo?.(parsed.x, parsed.y);
			}
		} catch (e) {
			console.error('Failed to restore window state:', e);
		}
	} else {
		// Initialize with current state if none stored
		saveState();
	}

	// Listeners for window move and resize events
	window.addEventListener('beforeunload', saveState);

	let resizeTimeout: number;
	const handleResize = () => {
		clearTimeout(resizeTimeout);
		resizeTimeout = window.setTimeout(saveState, 250);
	};

	window.addEventListener('resize', handleResize);
	
	// Polling fallback to capture position changes (as there is no standard window 'move' event in browsers)
	const intervalId = window.setInterval(saveState, 5000);

	return () => {
		window.removeEventListener('beforeunload', saveState);
		window.removeEventListener('resize', handleResize);
		window.clearInterval(intervalId);
	};
}
