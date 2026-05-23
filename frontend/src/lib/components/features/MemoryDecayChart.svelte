<script lang="ts">
	import * as d3 from 'd3-shape';
	import * as d3Scale from 'd3-scale';

	export interface DecayPoint {
		day: number; // days since learning
		retention: number; // 0 to 1
	}

	interface Props {
		curves: {
			id: string;
			label: string;
			data: DecayPoint[];
			predictedForgetDay: number;
		}[];
		currentDay: number; // To show current retention line
		class?: string;
	}

	let { curves = [], currentDay = 0, class: className = '' }: Props = $props();

	let containerWidth = $state(600);
	const height = 200;
	const margin = { top: 10, right: 20, bottom: 20, left: 40 };

	let innerWidth = $derived(Math.max(0, containerWidth - margin.left - margin.right));
	let innerHeight = $derived(Math.max(0, height - margin.top - margin.bottom));

	let maxDays = $derived(Math.max(...curves.map(c => c.data[c.data.length - 1]?.day || 0), currentDay + 5));

	let xScale = $derived(
		d3Scale.scaleLinear()
			.domain([0, maxDays])
			.range([0, innerWidth])
	);

	let yScale = $derived(
		d3Scale.scaleLinear()
			.domain([0, 1])
			.range([innerHeight, 0])
	);

	let lineGenerator = $derived(
		d3.line<DecayPoint>()
			.x((d: DecayPoint) => xScale(d.day))
			.y((d: DecayPoint) => yScale(d.retention))
			.curve(d3.curveMonotoneX) // Ebbinghaus forgetting curve
	);

</script>

<div class="flex flex-col brutal-border bg-surface-primary p-4 {className}" bind:clientWidth={containerWidth}>
	<div class="flex justify-between items-start mb-4">
		<h4 class="font-bold text-sm uppercase tracking-widest text-content-primary">Memory Decay Prediction</h4>
	</div>

	<div class="relative" style="height: {height}px;">
		<svg width="100%" {height}>
			<g transform={`translate(${margin.left},${margin.top})`}>
				
				<!-- Retention threshold line usually at 0.8 -->
				<line 
					x1="0" x2={innerWidth} 
					y1={yScale(0.8)} y2={yScale(0.8)} 
					stroke="var(--color-error-DEFAULT)" 
					stroke-opacity="0.5"
					stroke-dasharray="2,2" 
				/>
				<text x={innerWidth - 5} y={yScale(0.8) - 5} text-anchor="end" class="text-[9px] font-mono fill-error-DEFAULT opacity-80 uppercase">Review Threshold</text>

				<!-- Y Axis -->
				{#each [0, 0.5, 0.8, 1] as tick}
					<text x="-10" y={yScale(tick) + 3} text-anchor="end" class="text-[10px] font-mono fill-content-secondary">{tick * 100}%</text>
				{/each}

				<!-- X Axis (Days) -->
				<line x1="0" x2={innerWidth} y1={innerHeight} y2={innerHeight} stroke="var(--color-border-base)" />
				{#each xScale.ticks(5) as tick}
					<text x={xScale(tick)} y={innerHeight + 15} text-anchor="middle" class="text-[10px] font-mono fill-content-secondary">{tick}d</text>
				{/each}

				<!-- Current Day Indicator -->
				<line 
					x1={xScale(currentDay)} x2={xScale(currentDay)} 
					y1="0" y2={innerHeight} 
					stroke="var(--color-brand-primary)" 
					stroke-width="2"
				/>
				<text x={xScale(currentDay)} y="-2" text-anchor="middle" class="text-[9px] font-mono font-bold fill-brand-primary uppercase">Today</text>

				<!-- Curves -->
				{#each curves as curve, i}
					<path 
						d={lineGenerator(curve.data) || ''} 
						fill="none" 
						stroke={i === curves.length - 1 ? "var(--color-content-primary)" : "var(--color-content-tertiary)"}
						stroke-width={i === curves.length - 1 ? 3 : 1.5}
						stroke-dasharray={i === curves.length - 1 ? "0" : "4,4"}
					/>
					
					<!-- Predict Dot -->
					{#if curve.predictedForgetDay > 0}
						<circle 
							cx={xScale(curve.predictedForgetDay)} 
							cy={yScale(0.8)} 
							r="4" 
							fill="var(--color-surface-primary)"
							stroke={i === curves.length - 1 ? "var(--color-content-primary)" : "var(--color-content-tertiary)"}
							stroke-width="2"
						/>
					{/if}
				{/each}
			</g>
		</svg>
	</div>
</div>