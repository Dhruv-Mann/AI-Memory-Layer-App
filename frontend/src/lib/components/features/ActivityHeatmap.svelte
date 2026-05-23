<script lang="ts">
	interface HeatmapData {
		date: string; // YYYY-MM-DD
		count: number;
		intensity: number; // 0 to 1
	}

	interface Props {
		data: HeatmapData[];
		year?: number;
		class?: string;
	}

	let {
		data = [],
		year = new Date().getFullYear(),
		class: className = ''
	}: Props = $props();

	// Generate 52 weeks x 7 days grid
	let weeks = $derived.by(() => {
		const result = [];
		// Simplified layout: we just map data onto a 7-row grid (columns are weeks).
		// In a real app we'd map exact dates, here we just show the structure based on data array length.
		// For demo we just populate a 364 items array (52 cols x 7 rows)
		for (let c = 0; c < 52; c++) {
			const col = [];
			for (let r = 0; r < 7; r++) {
				const i = c * 7 + r;
				col.push(data[i] || { date: `Day ${i}`, count: 0, intensity: 0 });
			}
			result.push(col);
		}
		return result;
	});

	let hoveredData = $state<HeatmapData | null>(null);

	function getIntensityColor(intensity: number) {
		if (intensity === 0) return 'bg-surface-tertiary';
		if (intensity < 0.25) return 'bg-brand-primary/30';
		if (intensity < 0.5) return 'bg-brand-primary/60';
		if (intensity < 0.75) return 'bg-brand-primary text-brand-secondary';
		return 'bg-brand-primary text-brand-secondary shadow-[0_0_8px_rgba(var(--color-brand-primary),0.8)]'; // Strongest glow
	}
</script>

<div class="flex flex-col gap-2 {className}">
	<div class="flex justify-between items-center mb-2">
		<h4 class="font-bold text-sm uppercase tracking-widest text-content-primary">Activity Heatmap {year}</h4>
		<div class="flex gap-1 text-xs text-content-secondary font-mono">
			<button class="hover:text-brand-primary">Day</button> | 
			<button class="hover:text-brand-primary">Week</button> | 
			<button class="text-content-primary font-bold">Month</button>
		</div>
	</div>

	<div class="relative overflow-x-auto pb-4">
		<div class="flex gap-1 min-w-max">
			{#each weeks as week}
				<div class="flex flex-col gap-1">
					{#each week as day}
						<!-- svelte-ignore a11y_no_static_element_interactions -->
						<!-- svelte-ignore a11y_click_events_have_key_events -->
						<div 
							class="w-3 h-3 brutal-border transition-all cursor-pointer {getIntensityColor(day.intensity)}"
							onmouseenter={() => hoveredData = day}
							onmouseleave={() => hoveredData = null}
						></div>
					{/each}
				</div>
			{/each}
		</div>
	</div>

	<div class="flex justify-between items-center text-xs font-mono text-content-tertiary mt-1">
		<div class="flex items-center gap-2">
			<span>Less</span>
			<div class="flex gap-1">
				<div class="w-3 h-3 bg-surface-tertiary brutal-border"></div>
				<div class="w-3 h-3 bg-brand-primary/30 brutal-border"></div>
				<div class="w-3 h-3 bg-brand-primary/60 brutal-border"></div>
				<div class="w-3 h-3 bg-brand-primary brutal-border"></div>
			</div>
			<span>More</span>
		</div>
		
		<div class="h-4">
			{#if hoveredData && hoveredData.intensity > 0}
				<span class="font-bold text-content-primary">{hoveredData.count} reviews</span> on {hoveredData.date}
			{/if}
		</div>
	</div>
</div>