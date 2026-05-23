import { writable } from 'svelte/store';
import type { MemoryGraphState } from '../types/graph';

function createGraphStore() {
	const initialState: MemoryGraphState = {
		viewport: {
			x: 0,
			y: 0,
			zoom: 1
		},
		selection: {
			hoveredNodeId: null,
			selectedNodeIds: [],
		},
		filters: {
			masteryStates: ['not-learned', 'learning', 'mastered', 'forgotten'],
			clusters: []
		}
	};

	const { subscribe, set, update } = writable<MemoryGraphState>(initialState);

	return {
		subscribe,
		set,
		update,
		
		setViewport: (x: number, y: number, zoom: number) => {
			update(state => ({
				...state,
				viewport: { x, y, zoom }
			}));
		},
		
		setHoveredNode: (nodeId: string | null) => {
			update(state => ({
				...state,
				selection: { ...state.selection, hoveredNodeId: nodeId }
			}));
		},
		
		toggleSelectedNode: (nodeId: string, multiSelect: boolean = false) => {
			update(state => {
				const current = state.selection.selectedNodeIds;
				if (current.includes(nodeId)) {
					return {
						...state,
						selection: {
							...state.selection,
							selectedNodeIds: current.filter(id => id !== nodeId)
						}
					};
				} else {
					return {
						...state,
						selection: {
							...state.selection,
							selectedNodeIds: multiSelect ? [...current, nodeId] : [nodeId]
						}
					};
				}
			});
		},
		
		clearSelection: () => {
			update(state => ({
				...state,
				selection: { ...state.selection, selectedNodeIds: [] }
			}));
		},
		
		reset: () => set(initialState)
	};
}

export const graphStore = createGraphStore();
