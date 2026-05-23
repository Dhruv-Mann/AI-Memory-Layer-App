<script lang="ts">
	import * as d3Scale from 'd3-scale';
	import * as d3Array from 'd3-array';
	import Button from '../primitives/Button.svelte';

	interface EfficiencyItem {
		name: string;
		category: string;
		timeInvestedMinutes: number;
		masteryGained: number; // percentage points gained, e.g. 0 to 100
		reviewsCount: number;
	}

	interface Props {
		items?: EfficiencyItem[];
		class?: string;
	}

	// Mock data for topics
	let mockItems: EfficiencyItem[] = [
		{ name: 'React strict mode effects', category: 'Frontend', timeInvestedMinutes: 45, masteryGained: 65, reviewsCount: 6 },
		{ name: 'Svelte 5 Runes API', category: 'Frontend', timeInvestedMinutes: 20, masteryGained: 78, reviewsCount: 4 },
		{ name: 'Tailwind CSS v4 updates', category: 'Frontend', timeInvestedMinutes: 30, masteryGained: 40, reviewsCount: 3 },
		{ name: 'Node.js event loop dynamics', category: 'Backend', timeInvestedMinutes: 80, masteryGained: 85, reviewsCount: 8 },
		{ name: 'PostgreSQL index types', category: 'Backend', timeInvestedMinutes: 90, masteryGained: 90, reviewsCount: 7 },
		{ name: 'Redis caching strategies', category: 'Backend', timeInvestedMinutes: 50, masteryGained: 45, reviewsCount: 4 },
		{ name: 'Rust memory borrow checker', category: 'Systems', timeInvestedMinutes: 110, masteryGained: 55, reviewsCount: 9 },
		{ name: 'Docker container networking', category: 'Systems', timeInvestedMinutes: 60, masteryGained: 70, reviewsCount: 4 }
	];

	let { items = mockItems, class: className = '' }: Props = $props();

	let containerWidth = $state(500);
	const height = 280;
	const margin = { top: 25, right: 30, bottom: 40, left: 50 };

	let innerWidth = $derived(Math.max(0, containerWidth - margin.left - margin.right));
	let innerHeight = $derived(Math.max(0, height - margin.top - margin.bottom));

	// Scales
	let xScale = $derived(
		d3Scale.scaleLinear()
			.domain([0, d3Array.max(items, d => d.timeInvestedMinutes) || 120])
			.nice()
			.range([0, innerWidth])
	);

	let yScale = $derived(
		d3Scale.scaleLinear()
			.domain([0, 100])
			.range([innerHeight, 0])
	);

	// Category colors
	const categoryColors: Record<string, string> = {
		'Frontend': 'var(--color-primary)',
		'Backend': 'var(--color-success-DEFAULT)',
		'Systems': 'var(--color-error-DEFAULT)'
	};

	function getCategoryColor(cat: string): string {
		return categoryColors[cat] || 'var(--color-gray-500)';
	}

	// Interactive states
	let hoveredIndex = $state<number | null>(null);
	let tooltipX = $state(0);
	let tooltipY = $state(0);

	function handleMouseMove(event: MouseEvent, index: number, item: EfficiencyItem) {
		hoveredIndex = index;
		tooltipX = xScale(item.timeInvestedMinutes) + margin.left;
		tooltipY = yScale(item.masteryGained) + margin.top - 10;
	}

	function handleMouseLeave() {
		hoveredIndex = null;
	}

	let bestItem = $derived.by(() => {
		if (items.length === 0) return null;
		return items.reduce((prev, current) => {
			const prevRatio = prev.masteryGained / prev.timeInvestedMinutes;
			const currentRatio = current.masteryGained / current.timeInvestedMinutes;
			return currentRatio > prevRatio ? current : prev;
		}, items[0]);
	});
</script>

<div 
	class="flex flex-col gap-6 brutal-border bg-surface-primary p-6 {className}"
	bind:clientWidth={containerWidth}
>
	<!-- Header -->
	<div class="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b-2 border-border-primary pb-4">
		<div>
			<h4 class="font-black text-lg uppercase tracking-tight text-fg-primary">Revision Efficiency</h4>
			<p class="text-xs text-fg-secondary font-mono mt-1">Mastery gained vs study time invested</p>
		</div>
		<div class="flex gap-4 text-xs font-mono font-bold">
			<div class="flex items-center gap-1">
				<span class="w-2.5 h-2.5 brutal-border bg-brand-primary"></span> Frontend
			</div>
			<div class="flex items-center gap-1">
				<span class="w-2.5 h-2.5 brutal-border bg-success-DEFAULT"></span> Backend
			</div>
			<div class="flex items-center gap-1">
				<span class="w-2.5 h-2.5 brutal-border bg-error-DEFAULT"></span> Systems
			</div>
		</div>
	</div>

	<!-- Scatter Plot Visual -->
	<div class="relative w-full" style="height: {height}px;">
		<svg width="100%" {height}>
			<g transform={`translate(${margin.left},${margin.top})`}>
				
				<!-- Grid lines (Y-axis: Mastery) -->
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
								{tick}%
							</text>
						</g>
					{/each}
				{/if}

				<!-- X Axis ticks (Time in minutes) -->
				{#if xScale}
					{#each xScale.ticks(5) as tick}
						<g transform={`translate(${xScale(tick)},${innerHeight})`}>
							<line 
								y1="0" 
								y2="5" 
								stroke="var(--border-primary)" 
								stroke-width="1.5" 
							/>
							<text 
								y="18" 
								text-anchor="middle" 
								class="text-[10px] font-mono fill-fg-secondary"
							>
								{tick}m
							</text>
						</g>
					{/each}
				{/if}

				<!-- Axis Labels -->
				<text
					x={innerWidth / 2}
					y={innerHeight + 34}
					text-anchor="middle"
					class="text-[10px] font-black font-mono uppercase tracking-wider fill-fg-tertiary"
				>
					Time Invested (Minutes)
				</text>

				<!-- Data Nodes (Bubbles) -->
				{#if xScale && yScale}
					{#each items as item, index}
						{@const cx = xScale(item.timeInvestedMinutes)}
						{@const cy = yScale(item.masteryGained)}
						{@const r = 8 + (item.reviewsCount * 0.8)} <!-- Radius scaled with reviews count -->
						{@const color = getCategoryColor(item.category)}

						<!-- svelte-ignore a11y_no_static_element_interactions -->
						<!-- svelte-ignore a11y_mouse_events_have_key_events -->
						<circle
							{cx}
							{cy}
							{r}
							fill={color}
							stroke="var(--border-primary)"
							stroke-width="2"
							class="transition-all duration-fast cursor-pointer hover:stroke-[3px] hover:scale-[1.1] origin-center"
							style="opacity: hoveredIndex === null || hoveredIndex === index ? 1 : 0.4;"
							onmouseover={(e) => handleMouseMove(e, index, item)}
							onmousemove={(e) => handleMouseMove(e, index, item)}
							onmouseleave={handleMouseLeave}
						/>

						<!-- Subtle inline labels for large bubbles if no hover is active -->
						{#if hoveredIndex === null && item.masteryGained > 50 && item.timeInvestedMinutes > 30}
							<text
								x={cx}
								y={cy - r - 4}
								text-anchor="middle"
								class="text-[8px] font-mono font-bold fill-fg-secondary pointer-events-none"
							>
								{item.name.split(' ')[0]}...
							</text>
						{/if}
					{/each}
				{/if}

			</g>
		</svg>

		<!-- Neo-brutalist Tooltip -->
		{#if hoveredIndex !== null && items[hoveredIndex]}
			{@const hItem = items[hoveredIndex]}
			{@const ratio = Math.round((hItem.masteryGained / hItem.timeInvestedMinutes) * 100) / 100}
			<div 
				class="absolute z-tooltip pointer-events-none -translate-x-1/2 -translate-y-full bg-surface-tertiary text-fg-primary text-xs font-mono font-bold brutal-border brutal-shadow-sm p-3 flex flex-col gap-1.5 min-w-[200px]"
				style="left: {tooltipX}px; top: {tooltipY}px;"
			>
				<div class="text-[10px] text-fg-tertiary uppercase leading-none border-b border-border-primary pb-1">{hItem.category}</div>
				<div class="font-black text-fg-primary leading-tight">{hItem.name}</div>
				<div class="grid grid-cols-2 gap-2 text-[10px] mt-1">
					<div>
						<span class="text-fg-secondary">Time:</span>
						<span>{hItem.timeInvestedMinutes}m</span>
					</div>
					<div>
						<span class="text-fg-secondary">Gained:</span>
						<span>+{hItem.masteryGained}%</span>
					</div>
					<div class="col-span-2 border-t border-border-primary pt-1 flex justify-between font-black text-fg-primary">
						<span>Efficiency Ratio:</span>
						<span class="text-brand-primary">{ratio} pts/m</span>
					</div>
				</div>
			</div>
		{/if}
	</div>

	<!-- High Efficiency Insight card -->
	{#if bestItem}
		<div class="brutal-border bg-surface-secondary p-4 flex flex-col sm:flex-row items-center justify-between gap-4 shadow-[2px_2px_0px_rgba(0,0,0,1)]">
			<div>
				<h5 class="text-xs font-black font-mono uppercase tracking-wider text-brand-primary">Max Efficiency Concept</h5>
				<p class="text-sm font-black uppercase text-fg-primary mt-1">{bestItem.name}</p>
			</div>
			<div class="text-center sm:text-right font-mono">
				<div class="text-[9px] font-bold uppercase text-fg-tertiary">Performance</div>
				<div class="text-lg font-black text-success-DEFAULT">+{bestItem.masteryGained}% <span class="text-xs font-bold text-fg-secondary">in {bestItem.timeInvestedMinutes}m</span></div>
			</div>
		</div>
	{/if}
</div>
