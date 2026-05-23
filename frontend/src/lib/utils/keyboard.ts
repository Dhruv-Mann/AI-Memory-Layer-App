import { browser } from '$app/environment';
import { writable } from 'svelte/store';

export type Modifier = 'Ctrl' | 'Cmd' | 'Shift' | 'Alt';

export interface Shortcut {
	id: string;
	key: string;
	modifiers: Modifier[];
	description: string;
	action: (e: KeyboardEvent) => void;
	category: string;
	preventEventDefault?: boolean;
}

const STORAGE_KEY = 'ai-memory-layer:shortcuts';

const defaultShortcuts: Record<string, Shortcut> = {};

function createShortcutManager() {
	const { subscribe, set, update } = writable<Record<string, Shortcut>>(defaultShortcuts);
	
	let activeShortcuts: Record<string, Shortcut> = {};
	subscribe(v => activeShortcuts = v);

	// Convert a keyboard event into a comparable string
	const getEventKeySignature = (e: KeyboardEvent) => {
		const mods = [];
		if (e.ctrlKey) mods.push('Ctrl');
		if (e.metaKey) mods.push('Cmd');
		if (e.shiftKey) mods.push('Shift');
		if (e.altKey) mods.push('Alt');
		
		mods.sort();
		return `${mods.join('+')}+${e.key.toLowerCase()}`.replace(/^\+/, '');
	};

	// Convert a shortcut object into a comparable string
	const getShortcutSignature = (shortcut: Shortcut) => {
		const mods = [...shortcut.modifiers].sort();
		return `${mods.join('+')}+${shortcut.key.toLowerCase()}`.replace(/^\+/, '');
	};

	if (browser) {
		window.addEventListener('keydown', (e: KeyboardEvent) => {
			// Don't fire shortcuts when typing in inputs/textareas
			const target = e.target as HTMLElement;
			const isInput = target && (
				target.tagName === 'INPUT' || 
				target.tagName === 'TEXTAREA' || 
				target.isContentEditable
			);
			
			// Except when the shortcut is explicitly allowed or global
			const sig = getEventKeySignature(e);
			
			for (const shortcut of Object.values(activeShortcuts)) {
				const scSig = getShortcutSignature(shortcut);
				
				if (sig === scSig) {
					// Most shortcuts disabled in inputs
					// NOTE: This could be customized per-shortcut (e.g. `allowInInput` flag)
					if (isInput && !(scSig === 'Cmd+k' || scSig === 'Ctrl+k')) {
						// For search/palette shortcuts, we might still want to trigger them if it doesn't conflict directly with browser.
						// Or just block all if inside text. Let's block unless specified.
						// We'll trust default for now, skipping if isInput.
						if (!['Cmd+enter', 'Ctrl+enter', 'Escape'].includes(scSig)) {
							continue;
						}
					}

					if (shortcut.preventEventDefault !== false) {
						e.preventDefault();
					}
					shortcut.action(e);
					break; // Avoid triggering multiple shortcuts with exact same binding
				}
			}
		});
	}

	return {
		subscribe,
		register: (shortcut: Shortcut) => {
			update(shortcuts => {
				const sig = getShortcutSignature(shortcut);
				// Conflict detection (logging for now, but easily expandable to UI feedback)
				for (const existing of Object.values(shortcuts)) {
					if (existing.id !== shortcut.id && getShortcutSignature(existing) === sig) {
						console.warn(`Shortcut conflict: "${shortcut.id}" and "${existing.id}" both use "${sig}"`);
					}
				}
				
				return { ...shortcuts, [shortcut.id]: shortcut };
			});
		},
		unregister: (id: string) => {
			update(shortcuts => {
				const newShortcuts = { ...shortcuts };
				delete newShortcuts[id];
				return newShortcuts;
			});
		},
		getSignature: getShortcutSignature
	};
}

export const shortcutManager = createShortcutManager();

// Pre-define common global default actions that will be implemented fully later.
export function initGlobalShortcuts() {
	if (!browser) return;

	shortcutManager.register({
		id: 'global.command-palette',
		key: 'k',
		modifiers: [navigator.platform.indexOf('Mac') > -1 ? 'Cmd' : 'Ctrl'],
		description: 'Open Command Palette',
		category: 'Global',
		action: () => {
			console.log('Command palette triggered!');
			// Dispatches custom event to be picked up by CommandPalette component
			window.dispatchEvent(new CustomEvent('open-command-palette'));
		}
	});

	shortcutManager.register({
		id: 'global.search',
		key: 'f',
		modifiers: [navigator.platform.indexOf('Mac') > -1 ? 'Cmd' : 'Ctrl', 'Shift'],
		description: 'Global Search',
		category: 'Global',
		action: () => {
			window.dispatchEvent(new CustomEvent('open-search'));
		}
	});

	shortcutManager.register({
		id: 'global.new-memory',
		key: 'n',
		modifiers: [navigator.platform.indexOf('Mac') > -1 ? 'Cmd' : 'Ctrl'],
		description: 'Create New Memory',
		category: 'Global',
		action: () => {
			window.dispatchEvent(new CustomEvent('trigger-new-memory'));
		}
	});
}