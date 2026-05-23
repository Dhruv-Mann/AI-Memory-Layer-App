export interface MemoryNode {
	id: string;
	title: string;
	volume: number; // For size (8-32px radius)
	masteryState: 'not-learned' | 'learning' | 'mastered' | 'forgotten';
	clusterId?: string;
	
	// D3-force optional positional data that D3 manages mutably
	x?: number;
	y?: number;
	fx?: number | null;
	fy?: number | null;
	vx?: number;
	vy?: number;
}

export interface MemoryEdge {
	source: string | MemoryNode;
	target: string | MemoryNode;
	weight: number; // Stroke width
}

export interface MemoryGraphState {
	viewport: {
		x: number;
		y: number;
		zoom: number; // 0.1-5.0
	};
	selection: {
		hoveredNodeId: string | null;
		selectedNodeIds: string[];
	};
	filters: {
		masteryStates: Array<'not-learned' | 'learning' | 'mastered' | 'forgotten'>;
		clusters: string[];
	};
}
