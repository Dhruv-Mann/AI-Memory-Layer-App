<script lang="ts">
	import ProgressRing from '../charts/ProgressRing.svelte';
	import Button from '../primitives/Button.svelte';

	interface Props {
		completedReviews?: number;
		totalReviewsDue?: number;
		estimatedTimeMinutes?: number;
		overloadThreshold?: number;
		class?: string;
	}

	let {
		completedReviews = 12,
		totalReviewsDue = 34,
		estimatedTimeMinutes = 25,
		overloadThreshold = 30,
		class: className = ''
	}: Props = $props();

	// Calculate load percent based on threshold
	let loadPercent = $derived(Math.round((totalReviewsDue / overloadThreshold) * 100));
	let isOverloaded = $derived(totalReviewsDue >= overloadThreshold);

	// E.g., Green for low load, Orange/Yellow for medium, Red for overload
	let loadColor = $derived.by(() => {
		if (loadPercent < 50) return 'var(--color-success-DEFAULT)';
		if (loadPercent < 100) return 'var(--color-warning-DEFAULT)';
		return 'var(--color-error-DEFAULT)';
	});

	let statusLabel = $derived.by(() => {
		if (loadPercent < 50) return 'Optimal';
		if (loadPercent < 100) return 'Moderate';
		return 'Overloaded';
	});
</script>

<div class="flex flex-col gap-6 brutal-border bg-surface-primary p-6 {className}">
	<!-- Header -->
	<div class="flex items-center justify-between border-b-2 border-border-primary pb-4">
		<div>
			<h4 class="font-black text-lg uppercase tracking-tight text-fg-primary">Cognitive Load Status</h4>
			<p class="text-xs text-fg-secondary font-mono mt-1">Daily review capacity and mental fatigue metrics</p>
		</div>
		<span 
			class="px-2 py-1 brutal-border text-xs font-mono font-bold uppercase tracking-wider shadow-[1px_1px_0px_rgba(0,0,0,1)]"
			style="background-color: {loadColor}; color: var(--bg-primary);"
		>
			{statusLabel}
		</span>
	</div>

	<!-- Core Metrics Section -->
	<div class="flex flex-col md:flex-row items-center gap-6">
		<div class="shrink-0 flex items-center justify-center brutal-border bg-surface-secondary p-4 shadow-[3px_3px_0px_rgba(0,0,0,1)]">
			<ProgressRing 
				value={loadPercent} 
				size={100} 
				strokeWidth={10} 
				color={loadColor}
				label={`${loadPercent}%`}
				subLabel="Load"
			/>
		</div>

		<div class="flex-1 grid grid-cols-1 sm:grid-cols-2 gap-4 w-full">
			<div class="brutal-border bg-surface-secondary p-3 shadow-[2px_2px_0px_rgba(0,0,0,1)]">
				<div class="text-[9px] font-bold font-mono tracking-wider uppercase text-fg-tertiary">Progress</div>
				<div class="text-xl font-black font-mono mt-1 text-fg-primary">
					{completedReviews} <span class="text-xs font-bold text-fg-secondary">/ {totalReviewsDue} Done</span>
				</div>
			</div>
			
			<div class="brutal-border bg-surface-secondary p-3 shadow-[2px_2px_0px_rgba(0,0,0,1)]">
				<div class="text-[9px] font-bold font-mono tracking-wider uppercase text-fg-tertiary">Est. Time Remaining</div>
				<div class="text-xl font-black font-mono mt-1 text-fg-primary">
					{estimatedTimeMinutes} <span class="text-xs font-bold text-fg-secondary">Minutes</span>
				</div>
			</div>
		</div>
	</div>

	<!-- Warnings and Insights -->
	{#if isOverloaded}
		<div 
			class="brutal-border p-4 bg-error-DEFAULT/10 border-error-DEFAULT shadow-[3px_3px_0px_rgba(var(--color-error-DEFAULT),1)] animate-in fade-in slide-in-from-bottom-2 duration-normal"
		>
			<div class="flex items-start gap-3">
				<div class="p-1 bg-error-DEFAULT text-surface-primary brutal-border shrink-0 mt-0.5">
					<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="square"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
				</div>
				<div>
					<h5 class="font-black text-sm uppercase tracking-tight text-error-DEFAULT">Attention: High Review Load</h5>
					<p class="text-xs font-mono font-medium text-fg-secondary mt-1 leading-relaxed">
						You have {totalReviewsDue} pending reviews, exceeding your limit of {overloadThreshold}. To prevent cognitive burnout and ensure high retention stability, we recommend pausing learning on new topics until today's reviews are cleared.
					</p>
				</div>
			</div>
		</div>
	{:else}
		<div 
			class="brutal-border p-4 bg-success-DEFAULT/10 border-success-DEFAULT shadow-[3px_3px_0px_rgba(var(--color-success-DEFAULT),1)]"
		>
			<div class="flex items-start gap-3">
				<div class="p-1 bg-success-DEFAULT text-surface-primary brutal-border shrink-0 mt-0.5">
					<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="square"><polyline points="20 6 9 17 4 12"></polyline></svg>
				</div>
				<div>
					<h5 class="font-black text-sm uppercase tracking-tight text-success-DEFAULT">Cognitive Level Stable</h5>
					<p class="text-xs font-mono font-medium text-fg-secondary mt-1 leading-relaxed">
						Your daily burden is perfectly optimized for healthy retention reinforcement. You have complete flexibility to explore new semantic areas or proceed with extra self-assessments.
					</p>
				</div>
			</div>
		</div>
	{/if}
</div>
