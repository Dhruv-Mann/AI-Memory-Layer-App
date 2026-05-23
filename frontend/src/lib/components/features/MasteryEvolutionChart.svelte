<script lang="ts">
	import * as d3 from 'd3-shape';
	import * as d3Scale from 'd3-scale';
	import * as d3Array from 'd3-array';

	export interface MasterySeries {
		topicId: string;
		label: string;
		color: string;
		visible: boolean;
		data: { date: Date; value: number }[]; // value 0 to 1
	}

	interface Props {
		series: MasterySeries[];
		class?: string;
	}

	let { series = $bindable([]), class: className = '' }: Props = $props();

	let containerWidth = $state(600);
	const height = 250;
	const margin = { top: 20, right: 30, bottom: 30, left: 40 };

	let innerWidth = $derived(Math.max(0, containerWidth - margin.left - margin.right));
	let innerHeight = $derived(Math.max(0, height - margin.top - margin.bottom));

	let allDates = $derived(series.flatMap(s => s.data.map(d => d.date)));
	let allValues = $derived(series.flatMap(s => s.data.map(d => d.value)));

	let xScale = $derived(
		d3Scale.scaleTime()
			.domain(d3Array.extent(allDates) as [Date, Date] || [new Date(), new Date()])
			.range([0, innerWidth])
	);

	let yScale = $derived(
		d3Scale.scaleLinear()
			.domain([0, 1]) // 0 to 100% mastery
			.range([innerHeight, 0])
	);

	let lineGenerator = $derived(
		d3.line<{date: Date; value: number}>()
			.x((d: {date: Date; value: number}) => xScale(d.date))
			.y((d: {date: Date; value: number}) => yScale(d.value))
			.curve(d3.curveMonotoneX)
	);

	let activeSeries = $derived(series.filter(s => s.visible));

	function toggleSeries(topicId: string) {
		const s = series.find(x => x.topicId === topicId);
		if (s) s.visible = !s.visible;
		// trigger reactivity
		series = [...series];
	}
	
</script>

<div class="flex flex-col gap-4 brutal-border bg-surface-primary p-4 {className}" bind:clientWidth={containerWidth}>
	<div class="flex justify-between items-start">
		<h4 class="font-bold text-sm uppercase tracking-widest text-content-primary">Mastery Evolution</h4>
		<div class="flex flex-wrap gap-2 justify-end max-w-[50%]">
			{#each series as s}
				<button 
					class="flex items-center gap-1 text-[10px] font-bold font-mono tracking-widest uppercase transition-opacity {s.visible ? 'opacity-100' : 'opacity-40'}"
					onclick={() => toggleSeries(s.topicId)}
				>
					<div class="w-3 h-3 border border-border-base" style="background-color: {s.color};"></div>
					{s.label}
				</button>
			{/each}
		</div>
	</div>

	<div class="relative mt-2" style="height: {height}px;">
		<svg width="100%" {height}>
			<g transform={`translate(${margin.left},${margin.top})`}>
				<!-- Grid lines -->
				{#each yScale.ticks(5) as tick}
					<g transform={`translate(0,${yScale(tick)})`}>
						<line x1="0" x2={innerWidth} stroke="var(--color-border-subtle)" stroke-dasharray="4,4" />
						<text x="-10" y="3" text-anchor="end" class="text-[10px] font-mono fill-content-secondary">{Math.round(tick * 100)}%</text>
					</g>
				{/each}

				{#each xScale.ticks(5) as tick}
					<g transform={`translate(${xScale(tick)},${innerHeight})`}>
						<text y="15" text-anchor="middle" class="text-[10px] font-mono fill-content-secondary">{tick.toLocaleDateString(undefined, {month: 'short', day: 'numeric'})}</text>
					</g>
				{/each}

				<!-- Lines -->
				{#each activeSeries as s}
					<!-- svelte-ignore a11y_no_static_element_interactions -->
					<path 
						d={lineGenerator(s.data) || ''} 
						fill="none" 
						stroke={s.color} 
						stroke-width="3"
						class="transition-all duration-300"
					/>
				{/each}
			</g>
		</svg>
	</div>
</div>