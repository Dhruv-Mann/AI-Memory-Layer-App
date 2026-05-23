import { writable } from 'svelte/store';
import { browser } from '$app/environment';

export type FocusContext = 'main' | 'panel' | 'modal' | 'toast';

interface FocusState {
	currentContext: FocusContext;
	history: HTMLElement[];
	trappedElements: HTMLElement[];
}

const initialState: FocusState = {
	currentContext: 'main',
	history: [],
	trappedElements: []
};

// Simple writable store for global focus tracking
const focusStoreWritable = writable<FocusState>(initialState);

export const focusStore = {
	subscribe: focusStoreWritable.subscribe,

	setContext(context: FocusContext) {
		focusStoreWritable.update(state => ({ ...state, currentContext: context }));
	},

	// Save current focus before opening a modal/popover
	saveFocus() {
		if (!browser) return;
		const activeElement = document.activeElement as HTMLElement;
		if (activeElement) {
			focusStoreWritable.update(state => {
				const history = [...state.history, activeElement];
				return { ...state, history };
			});
		}
	},

	// Restore previous focus after closing a modal/popover
	restoreFocus() {
		if (!browser) return;
		focusStoreWritable.update(state => {
			const history = [...state.history];
			const lastElement = history.pop();
			if (lastElement && document.body.contains(lastElement)) {
				// use a slight timeout to ensure element is visible before focusing
				setTimeout(() => lastElement.focus(), 0);
			}
			return { ...state, history };
		});
	},

	// Add an element to be focus trapped
	addTrappedElement(el: HTMLElement) {
		focusStoreWritable.update(state => {
			return { ...state, trappedElements: [...state.trappedElements, el] };
		});
	},

	// Remove an element from focus trapping
	removeTrappedElement(el: HTMLElement) {
		focusStoreWritable.update(state => {
			return { 
				...state, 
				trappedElements: state.trappedElements.filter(e => e !== el) 
			};
		});
	}
};

/**
 * Action to trap focus within an element.
 */
export function trapFocus(node: HTMLElement, active: boolean = true) {
	if (!active) return {};

	const focusableElementsSelector = 
		'a[href], area[href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), button:not([disabled]), iframe, object, embed, [tabindex="0"], [contenteditable]';

	function handleKeyDown(event: KeyboardEvent) {
		if (event.key !== 'Tab') return;

		const focusableElements = Array.from(node.querySelectorAll<HTMLElement>(focusableElementsSelector))
			.filter(el => !el.hasAttribute('disabled') && !el.getAttribute('aria-hidden'));
		
		if (focusableElements.length === 0) {
			event.preventDefault();
			return;
		}

		const firstElement = focusableElements[0];
		const lastElement = focusableElements[focusableElements.length - 1];

		if (event.shiftKey) {
			if (document.activeElement === firstElement || document.activeElement === node) {
				event.preventDefault();
				lastElement.focus();
			}
		} else {
			if (document.activeElement === lastElement) {
				event.preventDefault();
				firstElement.focus();
			}
		}
	}

	node.addEventListener('keydown', handleKeyDown);
	focusStore.addTrappedElement(node);

	return {
		update(newActive: boolean) {
			active = newActive;
			if (!active) {
				node.removeEventListener('keydown', handleKeyDown);
			} else {
				node.addEventListener('keydown', handleKeyDown);
			}
		},
		destroy() {
			node.removeEventListener('keydown', handleKeyDown);
			focusStore.removeTrappedElement(node);
		}
	};
}