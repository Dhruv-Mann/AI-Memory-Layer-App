<script lang="ts">
	import * as d3 from 'd3-shape';
	import * as d3Scale from 'd3-scale';
	import * as d3Array from 'd3-array';
	import { exportChart } from '../../utils/chartExport';

	export interface LinePoint {
		x: Date | number;
		y: number;
	}

	export interface LineSeries {
		label: string;
		color?: string;
		data: LinePoint[];
	}

	interface Props {
		series?: LineSeries[]; // Multi-series support
		data?: LinePoint[]; // Single series fallback
		color?: string; // Default line color
		height?: number;
		margin?: { top: number; right: number; bottom: number; left: number };
		interactive?: boolean;
		xIsDate?: boolean; // Formats X ticks as dates if true
		class?: string;
	}

	let {
		series,
		data,
		color = 'var(--color-primary)',
		height = 250,
		margin = { top: 20, right: 30, bottom: 40, left: 50 },
		interactive = true,
		xIsDate = true,
		class: className = ''
	}: Props = $props();

	let containerWidth = $state(400);
	let containerRef = $state<HTMLElement | null>(null);

	let innerWidth = $derived(Math.max(0, containerWidth - margin.left - margin.right));
	let innerHeight = $derived(Math.max(0, height - margin.top - margin.bottom));

	// Normalize data to always work with series array
	let normalizedSeries = $derived.by<LineSeries[]>(() => {
		if (series && series.length > 0) {
			return series;
		}
		if (data && data.length > 0) {
			return [{ label: 'Data', color, data }];
		}
		return [];
	});

	// Get all flat points to compute domains
	let allPoints = $derived(normalizedSeries.flatMap(s => s.data));
	let allXValues = $derived(allPoints.map(p => p.x));
	let allYValues = $derived(allPoints.map(p => p.y));

	// Scales
	let xScale = $derived.by(() => {
		if (allXValues.length === 0) {
			return xIsDate 
				? d3Scale.scaleTime().domain([new Date(), new Date()]).range([0, innerWidth])
				: d3Scale.scaleLinear().domain([0, 10]).range([0, innerWidth]);
		}

		if (xIsDate) {
			const dates = allXValues as Date[];
			return d3Scale.scaleTime()
				.domain(d3Array.extent(dates) as [Date, Date])
				.range([0, innerWidth]);
		} else {
			const nums = allXValues as number[];
			return d3Scale.scaleLinear()
				.domain(d3Array.extent(nums) as [number, number])
				.range([0, innerWidth]);
		}
	});

	let yScale = $derived(
		d3Scale.scaleLinear()
			.domain([0, d3Array.max(allYValues) || 10])
			.nice()
			.range([innerHeight, 0])
	);

	// D3 Line Generator
	let lineGenerator = $derived(
		d3.line<LinePoint>()
			.x(d => xScale(d.x as any))
			.y(d => yScale(d.y))
			.curve(d3.curveMonotoneX)
	);

	// Interactive Hover State
	let hoveredX = $state<number | null>(null);
	let hoveredPoints = $derived.by(() => {
		if (hoveredX === null || normalizedSeries.length === 0 || !xScale) return null;

		// Convert pixel X coordinate back to domain X value
		const domainXValue = xScale.invert(hoveredX - margin.left);

		return normalizedSeries.map(s => {
			if (s.data.length === 0) return null;

			// Find point closest to domainXValue
			let closestPoint = s.data[0];
			let minDiff = Infinity;

			for (const p of s.data) {
				const diff = xIsDate
					? Math.abs((p.x as Date).getTime() - (domainXValue as Date).getTime())
					: Math.abs((p.x as number) - (domainXValue as number));
				
				if (diff < minDiff) {
					minDiff = diff;
					closestPoint = p;
				}
			}

			return {
				seriesLabel: s.label,
				color: s.color || color,
				point: closestPoint,
				pxX: xScale(closestPoint.x as any) + margin.left,
				pxY: yScale(closestPoint.y) + margin.top
			};
		}).filter(p => p !== null) as {
			seriesLabel: string;
			color: string;
			point: LinePoint;
			pxX: number;
			pxY: number;
		}[];
	});

	function handleMouseMove(event: MouseEvent) {
		if (!interactive) return;
		const rect = event.currentTarget as SVGElement;
		const svgRect = rect.getBoundingClientRect();
		const mouseX = event.clientX - svgRect.left;
		
		// Ensure mouse is within data area margins
		if (mouseX >= margin.left && mouseX <= margin.left + innerWidth) {
			hoveredX = mouseX;
		} else {
			hoveredX = null;
		}
	}

	function handleMouseLeave() {
		hoveredX = null;
	}

	function formatXLabel(val: Date | number): string {
		if (val instanceof Date) {
			return val.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
		}
		return val.toString();
	}
</script>

<div 
	class="relative w-full brutal-border bg-surface-primary p-4 group/chart {className}" 
	bind:clientWidth={containerWidth}
	bind:this={containerRef}
>
	<!-- Export Options -->
	<div class="absolute top-2 right-2 flex gap-1 z-dropdown opacity-0 group-hover/chart:opacity-100 focus-within:opacity-100 transition-opacity duration-fast">
		<button 
			onclick={() => containerRef && exportChart(containerRef, 'line-chart', 'svg')} 
			title="Export as SVG"
			class="px-1.5 py-0.5 brutal-border bg-surface-secondary text-[8px] font-mono font-bold uppercase shadow-[1px_1px_0px_rgba(0,0,0,1)] hover:bg-surface-tertiary hover:translate-y-[-0.5px] active:translate-y-[0.5px] transition-all"
		>
			SVG
		</button>
		<button 
			onclick={() => containerRef && exportChart(containerRef, 'line-chart', 'png')} 
			title="Export as PNG"
			class="px-1.5 py-0.5 brutal-border bg-surface-secondary text-[8px] font-mono font-bold uppercase shadow-[1px_1px_0px_rgba(0,0,0,1)] hover:bg-surface-tertiary hover:translate-y-[-0.5px] active:translate-y-[0.5px] transition-all"
		>
			PNG
		</button>
	</div>
	<div class="relative" style="height: {height}px;">
		<!-- svelte-ignore a11y_no_static_element_interactions -->
		<svg 
			width="100%" 
			{height}
			onmousemove={handleMouseMove}
			onmouseleave={handleMouseLeave}
			class="cursor-crosshair"
			role="img"
			aria-label="Line chart showing performance metrics over time"
		>
			<title>Line Chart</title>
			<desc>A line chart visualizing metrics over time with interactive details.</desc>
			<g transform={`translate(${margin.left},${margin.top})`}>
				<!-- Grid lines -->
				{#if yScale}
					{#each yScale.ticks(5) as tick}
						<g transform={`translate(0,${yScale(tick)})`}>
							<line 
								x1="0" 
								x2={innerWidth} 
								stroke="var(--color-gray-300)" 
								stroke-dasharray="4,4" 
							/>
							<text 
								x="-10" 
								y="3" 
								text-anchor="end" 
								class="text-[10px] font-mono fill-fg-secondary"
							>
								{tick}
							</text>
						</g>
					{/each}
				{/if}

				<!-- X Axis ticks -->
				{#if xScale}
					{#each xScale.ticks(5) as tick}
						<g transform={`translate(${xScale(tick)},${innerHeight})`}>
							<text 
								y="18" 
								text-anchor="middle" 
								class="text-[10px] font-mono fill-fg-secondary"
							>
								{formatXLabel(tick)}
							</text>
						</g>
					{/each}
				{/if}

				<!-- Lines -->
				{#if lineGenerator}
					{#each normalizedSeries as s}
						<path 
							d={lineGenerator(s.data) || ''} 
							fill="none" 
							stroke={s.color || color} 
							stroke-width="3"
							class="transition-all duration-300"
						/>
					{/each}
				{/if}

				<!-- Interactive Hover line and markers -->
				{#if hoveredPoints && hoveredPoints.length > 0}
					<!-- Vertical hover guide line -->
					<line
						x1={hoveredPoints[0].pxX - margin.left}
						y1="0"
						x2={hoveredPoints[0].pxX - margin.left}
						y2={innerHeight}
						stroke="var(--border-primary)"
						stroke-width="1.5"
						stroke-dasharray="2,2"
					/>

					<!-- Interactive point markers -->
					{#each hoveredPoints as hp}
						<circle
							cx={hp.pxX - margin.left}
							cy={hp.pxY - margin.top}
							r="5"
							fill={hp.color}
							stroke="var(--border-primary)"
							stroke-width="2.5"
						/>
					{/each}
				{/if}
			</g>
		</svg>

		<!-- Neo-brutalist Tooltip -->
		{#if hoveredPoints && hoveredPoints.length > 0}
			{@const firstHp = hoveredPoints[0]}
			<div 
				class="absolute z-tooltip pointer-events-none -translate-x-1/2 -translate-y-full bg-surface-tertiary text-fg-primary text-xs font-mono font-bold brutal-border brutal-shadow-sm p-2 flex flex-col gap-1"
				style="left: {firstHp.pxX}px; top: {Math.min(...hoveredPoints.map(h => h.pxY)) - 10}px;"
			>
				<div class="text-[10px] text-fg-tertiary leading-none">{formatXLabel(firstHp.point.x)}</div>
				{#each hoveredPoints as hp}
					<div class="flex items-center gap-2 leading-tight">
						<span class="w-2.5 h-2.5 brutal-border" style="background-color: {hp.color};"></span>
						<span class="text-fg-secondary">{hp.seriesLabel}:</span>
						<span>{hp.point.y}</span>
					</div>
				{/each}
			</div>
		{/if}
	</div>
</div>
