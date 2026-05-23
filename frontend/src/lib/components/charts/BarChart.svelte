<script lang="ts">
	import * as d3Scale from 'd3-scale';
	import * as d3Array from 'd3-array';
	import { exportChart } from '../../utils/chartExport';

	export interface BarDataItem {
		label: string;
		value: number;
		color?: string;
	}

	interface Props {
		data: BarDataItem[];
		height?: number;
		margin?: { top: number; right: number; bottom: number; left: number };
		color?: string; // fallback color for bars
		interactive?: boolean;
		class?: string;
	}

	let {
		data = [],
		height = 250,
		margin = { top: 20, right: 20, bottom: 40, left: 50 },
		color = 'var(--color-primary)',
		interactive = true,
		class: className = ''
	}: Props = $props();

	let containerWidth = $state(400);
	let containerRef = $state<HTMLElement | null>(null);

	let innerWidth = $derived(Math.max(0, containerWidth - margin.left - margin.right));
	let innerHeight = $derived(Math.max(0, height - margin.top - margin.bottom));

	// Scales
	let xScale = $derived(
		d3Scale.scaleBand()
			.domain(data.map(d => d.label))
			.range([0, innerWidth])
			.padding(0.2)
	);

	let yScale = $derived(
		d3Scale.scaleLinear()
			.domain([0, d3Array.max(data, d => d.value) || 10])
			.nice()
			.range([innerHeight, 0])
	);

	// Interactive states
	let hoveredIndex = $state<number | null>(null);
	let tooltipX = $state(0);
	let tooltipY = $state(0);

	function handleMouseMove(event: MouseEvent, index: number, item: BarDataItem) {
		if (!interactive) return;
		hoveredIndex = index;
		
		// Find target bar's center point relative to the container
		const x = xScale(item.label) || 0;
		const bandwidth = xScale.bandwidth();
		const y = yScale(item.value);
		
		tooltipX = x + margin.left + bandwidth / 2;
		tooltipY = y + margin.top - 8;
	}

	function handleMouseLeave() {
		hoveredIndex = null;
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
			onclick={() => containerRef && exportChart(containerRef, 'bar-chart', 'svg')} 
			title="Export as SVG"
			class="px-1.5 py-0.5 brutal-border bg-surface-secondary text-[8px] font-mono font-bold uppercase shadow-[1px_1px_0px_rgba(0,0,0,1)] hover:bg-surface-tertiary hover:translate-y-[-0.5px] active:translate-y-[0.5px] transition-all"
		>
			SVG
		</button>
		<button 
			onclick={() => containerRef && exportChart(containerRef, 'bar-chart', 'png')} 
			title="Export as PNG"
			class="px-1.5 py-0.5 brutal-border bg-surface-secondary text-[8px] font-mono font-bold uppercase shadow-[1px_1px_0px_rgba(0,0,0,1)] hover:bg-surface-tertiary hover:translate-y-[-0.5px] active:translate-y-[0.5px] transition-all"
		>
			PNG
		</button>
	</div>
	<div class="relative" style="height: {height}px;">
		<svg 
			width="100%" 
			{height}
			role="img"
			aria-label="Bar chart showing topic performance"
		>
			<title>Bar Chart</title>
			<desc>A bar chart visualizing topic performance metrics with hover states.</desc>
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

				<!-- X Axis labels -->
				{#if xScale}
					{#each data as item}
						<g transform={`translate(${xScale(item.label) || 0 + xScale.bandwidth() / 2},${innerHeight})`}>
							<text 
								y="18" 
								text-anchor="middle" 
								class="text-[10px] font-mono fill-fg-secondary truncate max-w-[50px]"
							>
								{item.label}
							</text>
						</g>
					{/each}
				{/if}

				<!-- Bars -->
				{#if xScale && yScale}
					{#each data as item, index}
						{@const barWidth = xScale.bandwidth()}
						{@const barHeight = innerHeight - yScale(item.value)}
						{@const x = xScale(item.label) || 0}
						{@const y = yScale(item.value)}
						{@const barColor = item.color || color}

						<!-- svelte-ignore a11y_no_static_element_interactions -->
						<!-- svelte-ignore a11y_mouse_events_have_key_events -->
						<rect
							{x}
							{y}
							width={barWidth}
							height={Math.max(0, barHeight)}
							fill={barColor}
							stroke="var(--border-primary)"
							stroke-width="2"
							class="transition-all duration-fast cursor-pointer"
							style="opacity: hoveredIndex === null || hoveredIndex === index ? 1 : 0.6;"
							onmouseover={(e) => handleMouseMove(e, index, item)}
							onmousemove={(e) => handleMouseMove(e, index, item)}
							onmouseleave={handleMouseLeave}
						/>
					{/each}
				{/if}
			</g>
		</svg>

		<!-- Neo-brutalist Tooltip -->
		{#if hoveredIndex !== null && data[hoveredIndex]}
			<div 
				class="absolute z-tooltip pointer-events-none -translate-x-1/2 -translate-y-full bg-surface-tertiary text-fg-primary text-xs font-mono font-bold brutal-border brutal-shadow-sm px-2 py-1 leading-none"
				style="left: {tooltipX}px; top: {tooltipY}px;"
			>
				<span class="text-fg-secondary">{data[hoveredIndex].label}:</span> {data[hoveredIndex].value}
			</div>
		{/if}
	</div>
</div>
