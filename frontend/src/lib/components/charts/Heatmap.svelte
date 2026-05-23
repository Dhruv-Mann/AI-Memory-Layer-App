<script lang="ts">
	import * as d3Scale from 'd3-scale';
	import * as d3Array from 'd3-array';

	export interface HeatmapCell {
		x: string | number; // column index or label
		y: string | number; // row index or label
		value: number;      // intensity value (e.g. 0 to 100)
		label?: string;     // custom description for tooltips
	}

	interface Props {
		data: HeatmapCell[];
		xLabels?: (string | number)[]; // optional custom order/labels for X axis
		yLabels?: (string | number)[]; // optional custom order/labels for Y axis
		colors?: string[]; // array of colors representing levels from lowest to highest
		height?: number;
		margin?: { top: number; right: number; bottom: number; left: number };
		interactive?: boolean;
		tooltipFormatter?: (cell: HeatmapCell) => string;
		class?: string;
	}

	let {
		data = [],
		xLabels,
		yLabels,
		colors = [
			'var(--color-gray-100)',
			'rgba(var(--color-primary-rgb, 139, 92, 246), 0.2)',
			'rgba(var(--color-primary-rgb, 139, 92, 246), 0.5)',
			'rgba(var(--color-primary-rgb, 139, 92, 246), 0.8)',
			'var(--color-primary)'
		],
		height = 200,
		margin = { top: 20, right: 20, bottom: 30, left: 40 },
		interactive = true,
		tooltipFormatter,
		class: className = ''
	}: Props = $props();

	let containerWidth = $state(400);

	let innerWidth = $derived(Math.max(0, containerWidth - margin.left - margin.right));
	let innerHeight = $derived(Math.max(0, height - margin.top - margin.bottom));

	// Derive X and Y labels if not provided
	let derivedXLabels = $derived.by(() => {
		if (xLabels && xLabels.length > 0) return xLabels;
		return Array.from(new Set(data.map(d => d.x))).sort((a, b) => String(a).localeCompare(String(b)));
	});

	let derivedYLabels = $derived.by(() => {
		if (yLabels && yLabels.length > 0) return yLabels;
		return Array.from(new Set(data.map(d => d.y))).sort((a, b) => String(a).localeCompare(String(b)));
	});

	// Scales
	let xScale = $derived(
		d3Scale.scaleBand()
			.domain(derivedXLabels.map(String))
			.range([0, innerWidth])
			.padding(0.08)
	);

	let yScale = $derived(
		d3Scale.scaleBand()
			.domain(derivedYLabels.map(String))
			.range([0, innerHeight])
			.padding(0.08)
	);

	let maxValue = $derived(d3Array.max(data, d => d.value) || 1);

	// Color interpolator
	let colorScale = $derived(
		d3Scale.scaleLinear<string>()
			.domain(d3Array.range(0, maxValue + 0.1, maxValue / (colors.length - 1)))
			.range(colors)
			.clamp(true)
	);

	// Interactive states
	let hoveredCell = $state<HeatmapCell | null>(null);
	let tooltipX = $state(0);
	let tooltipY = $state(0);

	function handleMouseMove(event: MouseEvent, cell: HeatmapCell) {
		if (!interactive) return;
		hoveredCell = cell;

		const x = xScale(String(cell.x)) || 0;
		const y = yScale(String(cell.y)) || 0;
		const cellWidth = xScale.bandwidth();

		tooltipX = x + margin.left + cellWidth / 2;
		tooltipY = y + margin.top - 8;
	}

	function handleMouseLeave() {
		hoveredCell = null;
	}

	function defaultFormatter(cell: HeatmapCell): string {
		if (cell.label) return cell.label;
		return `[${cell.x}, ${cell.y}]: ${cell.value}`;
	}
</script>

<div 
	class="relative w-full brutal-border bg-surface-primary p-4 {className}" 
	bind:clientWidth={containerWidth}
>
	<div class="relative animate-in fade-in duration-normal" style="height: {height}px;">
		<svg width="100%" {height}>
			<g transform={`translate(${margin.left},${margin.top})`}>
				<!-- Y Axis labels -->
				{#if yScale}
					{#each derivedYLabels as yLabel}
						<text
							x="-10"
							y={(yScale(String(yLabel)) || 0) + yScale.bandwidth() / 2 + 3}
							text-anchor="end"
							class="text-[9px] font-mono fill-fg-secondary font-bold"
						>
							{yLabel}
						</text>
					{/each}
				{/if}

				<!-- X Axis labels (Only show some if there are too many) -->
				{#if xScale}
					{#each derivedXLabels as xLabel, idx}
						{#if derivedXLabels.length < 15 || idx % Math.ceil(derivedXLabels.length / 10) === 0}
							<text
								x={(xScale(String(xLabel)) || 0) + xScale.bandwidth() / 2}
								y={innerHeight + 15}
								text-anchor="middle"
								class="text-[9px] font-mono fill-fg-secondary font-bold"
							>
								{xLabel}
							</text>
						{/if}
					{/each}
				{/if}

				<!-- Heatmap Cells -->
				{#if xScale && yScale && colorScale}
					{#each data as cell}
						{@const x = xScale(String(cell.x))}
						{@const y = yScale(String(cell.y))}
						{@const cellWidth = xScale.bandwidth()}
						{@const cellHeight = yScale.bandwidth()}

						{#if x !== undefined && y !== undefined}
							<!-- svelte-ignore a11y_no_static_element_interactions -->
							<!-- svelte-ignore a11y_mouse_events_have_key_events -->
							<rect
								{x}
								{y}
								width={cellWidth}
								height={cellHeight}
								fill={colorScale(cell.value)}
								stroke="var(--border-primary)"
								stroke-width="1"
								class="transition-all duration-fast cursor-pointer hover:stroke-2 hover:scale-[1.05] origin-center"
								onmouseover={(e) => handleMouseMove(e, cell)}
								onmousemove={(e) => handleMouseMove(e, cell)}
								onmouseleave={handleMouseLeave}
							/>
						{/if}
					{/each}
				{/if}
			</g>
		</svg>

		<!-- Neo-brutalist Tooltip -->
		{#if hoveredCell}
			<div 
				class="absolute z-tooltip pointer-events-none -translate-x-1/2 -translate-y-full bg-surface-tertiary text-fg-primary text-xs font-mono font-bold brutal-border brutal-shadow-sm px-2 py-1 leading-none whitespace-nowrap"
				style="left: {tooltipX}px; top: {tooltipY}px;"
			>
				{tooltipFormatter ? tooltipFormatter(hoveredCell) : defaultFormatter(hoveredCell)}
			</div>
		{/if}
	</div>
</div>
