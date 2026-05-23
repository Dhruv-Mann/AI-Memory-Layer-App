<script lang="ts">
	import Button from '../primitives/Button.svelte';
	import Input from '../primitives/Input.svelte';
	import SearchFilters from '../composite/SearchFilters.svelte';
	import type { FilterState } from '../composite/SearchFilters.svelte';
	
	import ForgottenTopicCard from './ForgottenTopicCard.svelte';

	// Lazy load heavy chart components
	let ActivityHeatmap = $state<any>(null);
	let MasteryEvolutionChart = $state<any>(null);
	let MemoryDecayChart = $state<any>(null);

	$effect(() => {
		import('./ActivityHeatmap.svelte').then(m => ActivityHeatmap = m.default);
		import('./MasteryEvolutionChart.svelte').then(m => MasteryEvolutionChart = m.default);
		import('./MemoryDecayChart.svelte').then(m => MemoryDecayChart = m.default);
	});

	interface Props {
		topicsDue: number;
		currentStreak: number;
		class?: string;
	}

	let {
		topicsDue = 12,
		currentStreak = 5,
		class: className = ''
	}: Props = $props();

	// Mock Filter state
	let filterState = $state<FilterState>({
		type: [],
		tags: [],
		dateRange: 'all'
	});
	let isFiltersOpen = $state(false);

	// Mock Data for Forgotten Topics
	let forgottenTopics = $state([
		{ id: '1', title: 'React strict mode effects', urgency: 'critical' as const, dueDate: 'Today', contextPreview: 'React calls setup and cleanup twice in strict mode' },
		{ id: '2', title: 'Svelte 5 Runes API', urgency: 'high' as const, dueDate: 'Tomorrow', contextPreview: '$derived, $effect, and $state core primitives' },
		{ id: '3', title: 'Neobrutalism Design', urgency: 'medium' as const, dueDate: 'In 3 days', contextPreview: 'High contrast borders, monochrome shadows, functional type' },
		{ id: '4', title: 'Rust Borrow Checker', urgency: 'low' as const, dueDate: 'Next week', contextPreview: 'Rules for memory management without garbage collection' },
	]);

	// Mock Data for Heatmap
	let heatmapData = $derived(Array.from({ length: 364 }).map((_, i) => {
		const val = Math.random();
		return {
			date: `Day ${i}`,
			count: Math.floor(val * 15),
			intensity: val < 0.8 ? 0 : val < 0.9 ? 0.4 : val < 0.95 ? 0.7 : 1
		};
	}));

	// Mock Data for Mastery Evolution
	let evolutionSeries = $state([
		{
			topicId: 't1', label: 'Frontend', color: 'var(--color-brand-primary)', visible: true,
			data: Array.from({length: 10}).map((_, i) => ({ date: new Date(Date.now() - (9 - i) * 86400000), value: 0.3 + i * 0.05 + Math.random() * 0.1 }))
		},
		{
			topicId: 't2', label: 'Backend', color: 'var(--color-success-DEFAULT)', visible: true,
			data: Array.from({length: 10}).map((_, i) => ({ date: new Date(Date.now() - (9 - i) * 86400000), value: Math.min(1, 0.6 + i * 0.02 + Math.random() * 0.05) }))
		}
	]);

	// Mock Data for Memory Decay
	let decayCurves = $state([
		{
			id: 'c1',
			label: 'First Learn',
			data: [ {day: 0, retention: 1}, {day: 1, retention: 0.8}, {day: 3, retention: 0.5} ],
			predictedForgetDay: 1
		},
		{
			id: 'c2',
			label: 'First Review',
			data: [ {day: 1, retention: 1}, {day: 3, retention: 0.8}, {day: 7, retention: 0.5} ],
			predictedForgetDay: 3
		},
		{
			id: 'c3',
			label: 'Current Status',
			data: [ {day: 3, retention: 1}, {day: 7, retention: 0.8}, {day: 14, retention: 0.6} ],
			predictedForgetDay: 7
		}
	]);

</script>

<div class="flex flex-col h-full bg-surface-base overflow-y-auto {className}">
	
	<!-- Header -->
	<header class="border-b-4 border-border-base bg-surface-primary p-6 md:px-12 flex flex-col md:flex-row md:items-end justify-between gap-6 shrink-0">
		<div>
			<h1 class="text-3xl md:text-5xl font-black tracking-tight uppercase mb-2">Recall Dashboard</h1>
			<p class="text-content-secondary font-mono font-bold max-w-xl">
				Analyze retention metrics, identify memory decay, and execute targeted review sessions.
			</p>
		</div>

		<div class="flex gap-4 items-center">
			<div class="brutal-border bg-surface-secondary px-4 py-2 text-center shadow-[2px_2px_0px_rgba(0,0,0,1)]">
				<div class="text-[10px] font-bold tracking-widest text-content-tertiary uppercase">Streak</div>
				<div class="text-2xl font-black text-brand-primary font-mono">{currentStreak} <span class="text-sm">Days</span></div>
			</div>
			<div class="brutal-border bg-error-DEFAULT/10 border-error-DEFAULT px-4 py-2 text-center shadow-[2px_2px_0px_rgba(var(--color-error-DEFAULT),1)]">
				<div class="text-[10px] font-bold tracking-widest text-error-DEFAULT opacity-80 uppercase">Due Today</div>
				<div class="text-2xl font-black text-error-DEFAULT font-mono">{topicsDue}</div>
			</div>
			
			<Button variant="primary" class="h-full px-6 flex items-center gap-2">
				<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="square"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
				Start Session
			</Button>
		</div>
	</header>

	<!-- Main Content Area -->
	<main class="flex-1 p-6 md:p-12">
		<!-- Toolbar -->
		<div class="flex flex-col gap-4 mb-8">
			<div class="flex justify-between items-center bg-surface-primary brutal-border p-2 shadow-sm">
				<div class="flex items-center gap-2">
					<Button variant="ghost" class="h-8 gap-2" onclick={() => isFiltersOpen = !isFiltersOpen}>
						<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="square"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon></svg>
						Filters
						{#if filterState.tags.length + filterState.type.length > 0}
							<span class="bg-brand-primary text-surface-primary text-[10px] px-1.5 py-0.5 ml-1">{filterState.tags.length + filterState.type.length}</span>
						{/if}
					</Button>
				</div>
				<div class="text-xs font-mono font-bold text-content-tertiary uppercase">
					System Sync: Online
				</div>
			</div>

			{#if isFiltersOpen}
				<div class="bg-surface-primary brutal-border p-4 shadow-sm animate-in fade-in slide-in-from-top-2 duration-200">
					<SearchFilters bind:state={filterState} />
				</div>
			{/if}
		</div>

		<!-- Dashboard Grid -->
		<div class="grid grid-cols-1 xl:grid-cols-12 gap-8">
			
			<!-- Left Column: Urgency list (4 cols on xl) -->
			<div class="xl:col-span-4 flex flex-col gap-4">
				<div class="flex items-center justify-between border-b-4 border-border-base pb-2">
					<h3 class="font-black text-xl uppercase tracking-tight">Forgotten Topics</h3>
					<span class="bg-error-DEFAULT text-surface-primary text-xs font-bold px-2 py-0.5 shadow-sm">{forgottenTopics.length} Needed</span>
				</div>

				<div class="flex flex-col gap-4">
					{#each forgottenTopics as topic}
						<ForgottenTopicCard {topic} />
					{/each}
				</div>
			</div>

			<!-- Right Column: Analytics (8 cols on xl) -->
			<div class="xl:col-span-8 flex flex-col gap-8">
				
				<!-- ROW 1: Heatmap -->
				<section class="bg-surface-primary brutal-border p-6 shadow-[4px_4px_0px_rgba(0,0,0,1)] min-h-[250px] flex flex-col justify-center">
					{#if ActivityHeatmap}
						<ActivityHeatmap data={heatmapData} />
					{:else}
						<div class="h-48 w-full animate-pulse bg-surface-secondary flex flex-col items-center justify-center font-mono font-bold text-xs uppercase text-content-tertiary">
							<span>Loading Activity Heatmap...</span>
						</div>
					{/if}
				</section>
				
				<!-- ROW 2: Charts Grid -->
				<div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
					<section class="shadow-[4px_4px_0px_rgba(0,0,0,1)] min-h-[280px] bg-surface-primary brutal-border p-6 flex flex-col justify-center">
						{#if MasteryEvolutionChart}
							<MasteryEvolutionChart series={evolutionSeries} />
						{:else}
							<div class="h-56 w-full animate-pulse bg-surface-secondary flex flex-col items-center justify-center font-mono font-bold text-xs uppercase text-content-tertiary">
								<span>Loading Mastery Evolution...</span>
							</div>
						{/if}
					</section>

					<section class="shadow-[4px_4px_0px_rgba(0,0,0,1)] min-h-[280px] bg-surface-primary brutal-border p-6 flex flex-col justify-center">
						{#if MemoryDecayChart}
							<MemoryDecayChart curves={decayCurves} currentDay={5} />
						{:else}
							<div class="h-56 w-full animate-pulse bg-surface-secondary flex flex-col items-center justify-center font-mono font-bold text-xs uppercase text-content-tertiary">
								<span>Loading Memory Decay...</span>
							</div>
						{/if}
					</section>
				</div>
				
			</div>
		</div>
	</main>
</div>