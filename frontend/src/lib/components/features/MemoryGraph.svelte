<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import * as d3 from 'd3-force';
	import * as d3Zoom from 'd3-zoom';
	import * as d3Selection from 'd3-selection';
	import * as d3Polygon from 'd3-polygon';
	import type { MemoryNode, MemoryEdge, MemoryGraphState } from '../../types/graph';
	import { graphStore } from '../../stores/graphStore';

	interface Props {
		nodes: MemoryNode[];
		edges: MemoryEdge[];
		width?: number | string;
		height?: number | string;
		onNodeClick?: (node: MemoryNode) => void;
		onNodeDoubleClick?: (node: MemoryNode) => void;
		class?: string;
	}

	let {
		nodes = [],
		edges = [],
		width = '100%',
		height = '100%',
		onNodeClick,
		onNodeDoubleClick,
		class: className = ''
	}: Props = $props();

	let canvas: HTMLCanvasElement;
	let ctx: CanvasRenderingContext2D | null;
	let simulation: d3.Simulation<MemoryNode, MemoryEdge>;
	let animationFrameId: number;
	let zoomBehavior: d3Zoom.ZoomBehavior<HTMLCanvasElement, unknown>;
	
	// Tooltip state
	let tooltipData = $state<{node: MemoryNode, x: number, y: number} | null>(null);
	let hoverTimeoutId: ReturnType<typeof setTimeout> | undefined;
	
	// Track size internally for responsive layout updates
	let containerWidth = $state(800);
	let containerHeight = $state(600);

	let containerNode: HTMLDivElement;

	// Simple responsive resize observer
	let resizeObserver: ResizeObserver;

	$effect(() => {
		if (containerNode && typeof window !== 'undefined') {
			resizeObserver = new ResizeObserver((entries) => {
				for (let entry of entries) {
					containerWidth = entry.contentRect.width;
					containerHeight = entry.contentRect.height;
					
					if (canvas) {
						// Handle high DPI displays
						const dpr = window.devicePixelRatio || 1;
						canvas.width = containerWidth * dpr;
						canvas.height = containerHeight * dpr;
						
						if (ctx) {
							ctx.scale(dpr, dpr);
						}
						
						// Update force center
						if (simulation) {
							simulation.force('center', d3.forceCenter(containerWidth / 2, containerHeight / 2));
							simulation.alpha(0.3).restart();
						}
					}
				}
			});
			resizeObserver.observe(containerNode);
		}
		
		return () => {
			if (resizeObserver) resizeObserver.disconnect();
		};
	});

	onMount(() => {
		ctx = canvas.getContext('2d');
		
		// Setup D3 Zoom
		zoomBehavior = d3Zoom.zoom<HTMLCanvasElement, unknown>()
			.scaleExtent([0.1, 5.0])
			.on('zoom', (event) => {
				const { x, y, k } = event.transform;
				graphStore.setViewport(x, y, k);
				
				// Hide tooltip on pan/zoom
				tooltipData = null;
				if (hoverTimeoutId) clearTimeout(hoverTimeoutId);
				
				render();
			});
			
		d3Selection.select(canvas).call(zoomBehavior);

		// Interaction (Click, Hover)
		d3Selection.select(canvas)
			.on('mousemove', (event) => {
				if (!simulation) return;
				const [mx, my] = d3Selection.pointer(event, canvas);
				const state = $graphStore;
				// Transform mouse back to simulation coordinates
				const x = (mx - state.viewport.x) / state.viewport.zoom;
				const y = (my - state.viewport.y) / state.viewport.zoom;
				
				const n = simulation.find(x, y, 20 / state.viewport.zoom); // search radius
				if (n) {
					if (state.selection.hoveredNodeId !== n.id) {
						graphStore.setHoveredNode(n.id);
						
						// Setup tooltip
						if (hoverTimeoutId) clearTimeout(hoverTimeoutId);
						hoverTimeoutId = setTimeout(() => {
							tooltipData = { node: n as MemoryNode, x: mx, y: my };
						}, 300);
						render();
					}
				} else {
					if (state.selection.hoveredNodeId !== null) {
						graphStore.setHoveredNode(null);
						tooltipData = null;
						if (hoverTimeoutId) clearTimeout(hoverTimeoutId);
						render();
					}
				}
			})
			.on('click', (event) => {
				const state = $graphStore;
				if (state.selection.hoveredNodeId && simulation) {
					const node = nodes.find(n => n.id === state.selection.hoveredNodeId);
					if (node) {
						graphStore.toggleSelectedNode(node.id, event.shiftKey);
						if (onNodeClick) onNodeClick(node);
						render();
					}
				} else {
					graphStore.clearSelection();
					render();
				}
			})
			.on('dblclick', (event) => {
				const state = $graphStore;
				if (state.selection.hoveredNodeId && simulation) {
					const node = nodes.find(n => n.id === state.selection.hoveredNodeId);
					if (node && onNodeDoubleClick) {
						onNodeDoubleClick(node);
					}
				}
			});

		// Configure d3 simulation
		simulation = d3.forceSimulation<MemoryNode>(nodes)
			.force('link', d3.forceLink<MemoryNode, MemoryEdge>(edges).id((d) => d.id).distance(100))
			.force('charge', d3.forceManyBody().strength(-300))
			.force('center', d3.forceCenter(containerWidth / 2, containerHeight / 2))
			.force('collide', d3.forceCollide().radius((d: any) => d.volume + 5))
			.on('tick', () => {
				// We don't render directly in tick to allow throttling if needed
				// but since we want 60fps, we'll hook directly into rAF independent of tick,
				// or just redraw here. D3 tick usually runs via its own timer.
				// However, D3's timer is tightly coupled to requestAnimationFrame.
				render();
			});

		// Fallback manual render loop if not moving but we have viewport changes
		const loop = () => {
			if (simulation.alpha() < 0.01) {
				// Static graph, but might need redraw for pan/zoom
				render();
			}
			animationFrameId = requestAnimationFrame(loop);
		};
		animationFrameId = requestAnimationFrame(loop);

		return () => {
			simulation.stop();
			cancelAnimationFrame(animationFrameId);
		};
	});

	$effect(() => {
		// Update simulation if nodes/edges change
		if (simulation) {
			simulation.nodes(nodes);
			const linkForce = simulation.force('link') as d3.ForceLink<MemoryNode, MemoryEdge>;
			linkForce.links(edges);
			simulation.alpha(1).restart();
		}
	});

	function render() {
		if (!ctx || !canvas) return;

		// Clear canvas
		ctx.clearRect(0, 0, containerWidth, containerHeight);

		// Transform from viewport state
		ctx.save();
		const state = $graphStore;
		ctx.translate(state.viewport.x, state.viewport.y);
		ctx.scale(state.viewport.zoom, state.viewport.zoom);

		// Calculate visible viewport bounds in simulation coordinates
		const vw = containerWidth / state.viewport.zoom;
		const vh = containerHeight / state.viewport.zoom;
		const vx = -state.viewport.x / state.viewport.zoom;
		const vy = -state.viewport.y / state.viewport.zoom;

		// Group nodes by cluster to draw semantic boundaries
		const clusters = new Map<string, Array<[number, number]>>();
		for (const node of nodes) {
			if (node.clusterId && node.x !== undefined && node.y !== undefined) {
				if (!clusters.has(node.clusterId)) {
					clusters.set(node.clusterId, []);
				}
				clusters.get(node.clusterId)!.push([node.x, node.y]);
			}
		}

		// Draw cluster boundaries
		ctx.fillStyle = 'rgba(230, 230, 235, 0.3)'; // subtle background region
		ctx.strokeStyle = 'rgba(200, 200, 210, 0.5)';
		ctx.lineWidth = 1;
		for (const [clusterId, points] of Array.from(clusters.entries())) {
			// Filtering out filtered clusters
			if (state.filters.clusters.length > 0 && !state.filters.clusters.includes(clusterId)) continue;
			
			if (points.length >= 3) {
				const hull = d3Polygon.polygonHull(points);
				if (hull) {
					ctx.beginPath();
					// Make it slightly bigger by stepping out the hull or just drawing it
					ctx.moveTo(hull[0][0], hull[0][1]);
					for (let i = 1; i < hull.length; ++i) {
						ctx.lineTo(hull[i][0], hull[i][1]);
					}
					ctx.closePath();
					
					// Use a line join of round and large width for a padded look
					ctx.lineJoin = 'round';
					ctx.lineWidth = 40; 
					ctx.stroke();
					// Fill inner
					ctx.fill();

					// Add Cluster Label
					if (state.viewport.zoom > 0.5 && state.viewport.zoom < 2.0) {
						// centroid approximate
						const cx = hull.reduce((sum, p) => sum + p[0], 0) / hull.length;
						const cy = hull.reduce((sum, p) => sum + p[1], 0) / hull.length;
						ctx.fillStyle = 'rgba(0, 0, 0, 0.4)';
						ctx.font = 'bold 16px monospace';
						ctx.textAlign = 'center';
						ctx.textBaseline = 'middle';
						ctx.fillText(clusterId, cx, cy);
					}
				}
			}
		}

		// Draw edges
		ctx.strokeStyle = 'rgba(150, 150, 150, 0.4)';
		for (const edge of edges) {
			const source = edge.source as MemoryNode;
			const target = edge.target as MemoryNode;
			
			if (source.x === undefined || source.y === undefined || 
				target.x === undefined || target.y === undefined) continue;

			// Viewport culling for edges: if both nodes are out of bounds (approximate)
			const isSourceVisible = source.x >= vx && source.x <= vx + vw && source.y >= vy && source.y <= vy + vh;
			const isTargetVisible = target.x >= vx && target.x <= vx + vw && target.y >= vy && target.y <= vy + vh;
			if (!isSourceVisible && !isTargetVisible) continue;

			ctx.beginPath();
			ctx.lineWidth = edge.weight || 1;
			ctx.moveTo(source.x, source.y);
			ctx.lineTo(target.x, target.y);
			ctx.stroke();
		}

		// Draw nodes
		for (const node of nodes) {
			if (node.x === undefined || node.y === undefined) continue;

			// Viewport culling for nodes
			// Add a margin of max volume (32) to prevent popping
			if (node.x < vx - 32 || node.x > vx + vw + 32 || node.y < vy - 32 || node.y > vy + vh + 32) {
				continue;
			}

			const isHovered = state.selection.hoveredNodeId === node.id;
			const isSelected = state.selection.selectedNodeIds.includes(node.id);

			ctx.beginPath();
			ctx.arc(node.x, node.y, node.volume, 0, 2 * Math.PI);
			
			// Color by mastery
			switch (node.masteryState) {
				case 'mastered': ctx.fillStyle = '#10B981'; break; // success
				case 'learning': ctx.fillStyle = '#3B82F6'; break; // brand
				case 'forgotten': ctx.fillStyle = '#EF4444'; break; // error
				case 'not-learned': default: ctx.fillStyle = '#9CA3AF'; break; // content-tertiary
			}
			
			ctx.fill();

			// Visual feedback for selection/hover
			if (isSelected || isHovered) {
				ctx.lineWidth = isSelected ? 3 : 2;
				ctx.strokeStyle = isSelected ? '#F59E0B' : '#000000'; // warning or strong contrast
				ctx.stroke();
			}

			// Label rendering at zoom > 1.5
			if (state.viewport.zoom > 1.5) {
				ctx.fillStyle = '#111827';
				ctx.font = '10px monospace';
				ctx.textAlign = 'center';
				ctx.textBaseline = 'top';
				ctx.fillText(node.title, node.x, node.y + node.volume + 4);
			}
		}

		ctx.restore();
	}

</script>

<!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
<div 
	bind:this={containerNode}
	class="relative overflow-hidden bg-surface-primary brutal-inner-border {className}"
	style="width: {typeof width === 'number' ? width + 'px' : width}; height: {typeof height === 'number' ? height + 'px' : height};"
>
	<canvas
		bind:this={canvas}
		class="block absolute top-0 left-0 outline-none"
		style="width: 100%; height: 100%;"
	></canvas>
	
	<!-- Overlay UI (Toolbar etc) goes here -->
	<div class="absolute bottom-4 right-4 bg-surface-secondary border-2 border-border-base shadow-sm p-2 flex gap-2">
		<div class="text-xs font-mono font-bold text-content-secondary">
			Nodes: {nodes.length} | Zoom: {($graphStore.viewport.zoom).toFixed(1)}x
		</div>
	</div>

	<!-- Tooltip -->
	{#if tooltipData}
		<div 
			class="absolute pointer-events-none z-10 bg-surface-primary border-2 border-border-base shadow-sm p-3 brutal-border transition-opacity duration-100"
			style="left: {tooltipData.x + 15}px; top: {tooltipData.y + 15}px;"
		>
			<div class="font-bold text-content-primary mb-1">{tooltipData.node.title}</div>
			<div class="text-xs text-content-secondary capitalize">
				State: <span class={
					tooltipData.node.masteryState === 'mastered' ? 'text-success-DEFAULT' : 
					tooltipData.node.masteryState === 'forgotten' ? 'text-error-DEFAULT' : 
					'text-brand-primary'
				}>{tooltipData.node.masteryState}</span>
			</div>
			{#if tooltipData.node.clusterId}
				<div class="text-xs text-content-secondary font-mono mt-1 pt-1 border-t border-border-subtle">
					Cluster: {tooltipData.node.clusterId}
				</div>
			{/if}
		</div>
	{/if}
</div>