import { writable } from 'svelte/store';
import { browser } from '$app/environment';

export type Theme = 'dark' | 'brutalist' | 'monochrome' | 'terminal';
export type Density = 'compact' | 'normal' | 'comfortable';

interface ThemeState {
	currentTheme: Theme;
	densityMode: Density;
}

const STORAGE_KEY = 'ai-memory-layer:theme';

const defaultState: ThemeState = {
	currentTheme: 'brutalist',
	densityMode: 'normal'
};

function createThemeStore() {
	// Initialize from local storage if available
	let initialState = defaultState;
	
	if (browser) {
		const stored = localStorage.getItem(STORAGE_KEY);
		if (stored) {
			try {
				initialState = JSON.parse(stored);
			} catch (e) {
				console.error('Failed to parse theme from localStorage', e);
			}
		}
	}

	const { subscribe, set, update } = writable<ThemeState>(initialState);

	return {
		subscribe,
		setTheme: (theme: Theme) => {
			update((state) => {
				const newState = { ...state, currentTheme: theme };
				if (browser) {
					localStorage.setItem(STORAGE_KEY, JSON.stringify(newState));
					applyThemeToDOM(newState);
				}
				return newState;
			});
		},
		setDensity: (density: Density) => {
			update((state) => {
				const newState = { ...state, densityMode: density };
				if (browser) {
					localStorage.setItem(STORAGE_KEY, JSON.stringify(newState));
					applyThemeToDOM(newState);
				}
				return newState;
			});
		}
	};
}

// Applies the current theme and density as data attributes to the document root
function applyThemeToDOM(state: ThemeState) {
	if (!browser) return;
	const root = document.documentElement;
	root.setAttribute('data-theme', state.currentTheme);
	root.setAttribute('data-density', state.densityMode);
}

export const themeStore = createThemeStore();

// Initialize the DOM payload immediately on load
if (browser) {
	const stored = localStorage.getItem(STORAGE_KEY);
	if (stored) {
		const parsed = JSON.parse(stored);
		applyThemeToDOM(parsed);
	} else {
		applyThemeToDOM(defaultState);
	}
}
