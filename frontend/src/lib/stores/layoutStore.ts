import { writable } from 'svelte/store';
import { browser } from '$app/environment';

export interface PanelState {
	visible: boolean;
	size: number;
	collapsed: boolean;
	minSize: number;
	maxSize: number;
}

export interface WorkspaceLayout {
	sidebar: PanelState;
	mainContent: PanelState; // mainContent might not have a fixed size, it takes remaining space, but keeping it for consistency if needed
	auxiliaryPanel: PanelState & { dock: 'left' | 'right' | 'floating' };
	bottomPanel: PanelState;
	commandBar: { visible: boolean };
}

const STORAGE_KEY = 'ai-memory-layer:layout';

const defaultLayout: WorkspaceLayout = {
	sidebar: {
		visible: true,
		size: 250,
		collapsed: false,
		minSize: 200,
		maxSize: 400
	},
	mainContent: {
		visible: true,
		size: 0, // Flexibly takes the remaining space
		collapsed: false,
		minSize: 300,
		maxSize: Infinity
	},
	auxiliaryPanel: {
		visible: false,
		size: 300,
		collapsed: false,
		minSize: 300,
		maxSize: 600,
		dock: 'right'
	},
	bottomPanel: {
		visible: false,
		size: 200,
		collapsed: false,
		minSize: 200,
		maxSize: 600
	},
	commandBar: {
		visible: false
	}
};

function createLayoutStore() {
	let initialLayout = defaultLayout;

	if (browser) {
		const stored = localStorage.getItem(STORAGE_KEY);
		if (stored) {
			try {
				const parsed = JSON.parse(stored);
				// Shallow merge with defaults to avoid missing properties if updates happen
				initialLayout = {
					...defaultLayout,
					...parsed,
					sidebar: { ...defaultLayout.sidebar, ...(parsed.sidebar || {}) },
					auxiliaryPanel: { ...defaultLayout.auxiliaryPanel, ...(parsed.auxiliaryPanel || {}) },
					bottomPanel: { ...defaultLayout.bottomPanel, ...(parsed.bottomPanel || {}) }
				};
			} catch (e) {
				console.error('Failed to parse layout from localStorage', e);
			}
		}
	}

	const { subscribe, set, update } = writable<WorkspaceLayout>(initialLayout);

	const persist = (state: WorkspaceLayout) => {
		if (browser) {
			localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
		}
		return state;
	};

	return {
		subscribe,
		set,
		updatePanel: (panel: keyof Omit<WorkspaceLayout, 'commandBar'>, updates: Partial<PanelState>) => {
			update(state => {
				const newState = {
					...state,
					[panel]: {
						...state[panel],
						...updates
					}
				};
				return persist(newState);
			});
		},
		togglePanel: (panel: keyof WorkspaceLayout) => {
			update(state => {
				const panelState = state[panel];
				const newState = {
					...state,
					[panel]: {
						...panelState,
						visible: !panelState.visible
					}
				};
				return persist(newState);
			});
		},
		toggleCollapse: (panel: keyof Omit<WorkspaceLayout, 'commandBar'>) => {
			update(state => {
				const newState = {
					...state,
					[panel]: {
						...state[panel],
						collapsed: !state[panel].collapsed
					}
				};
				return persist(newState);
			});
		},
		setDock: (dock: 'left' | 'right' | 'floating') => {
			update(state => {
				const newState = {
					...state,
					auxiliaryPanel: {
						...state.auxiliaryPanel,
						dock
					}
				};
				return persist(newState);
			});
		},
		reset: () => {
			set(defaultLayout);
			persist(defaultLayout);
		}
	};
}

export const layoutStore = createLayoutStore();