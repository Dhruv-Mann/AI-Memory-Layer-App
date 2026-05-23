<script lang="ts">
	import LineChart from '../charts/LineChart.svelte';
	import type { LineSeries, LinePoint } from '../charts/LineChart.svelte';
	import Button from '../primitives/Button.svelte';

	interface TopicStrength {
		id: string;
		name: string;
		color: string;
		halfLifeDays: number;
		totalReviews: number;
		lastReviewDate: string;
		currentStability: 'Low' | 'Medium' | 'High';
		data: LinePoint[];
	}

	interface Props {
		topics?: TopicStrength[];
		class?: string;
	}

	// Mock data for topics if not provided
	let mockTopics: TopicStrength[] = [
		{
			id: 't1',
			name: 'React strict mode effects',
			color: 'var(--color-primary)',
			halfLifeDays: 12.5,
			totalReviews: 6,
			lastReviewDate: '2 days ago',
			currentStability: 'High',
			data: [
				{ x: new Date(Date.now() - 9 * 86400000), y: 0.4 },
				{ x: new Date(Date.now() - 8 * 86400000), y: 0.35 },
				{ x: new Date(Date.now() - 7 * 86400000), y: 0.95 },
				{ x: new Date(Date.now() - 6 * 86400000), y: 0.88 },
				{ x: new Date(Date.now() - 4 * 86400000), y: 0.75 },
				{ x: new Date(Date.now() - 3 * 86400000), y: 0.98 },
				{ x: new Date(Date.now() - 2 * 86400000), y: 0.92 },
				{ x: new Date(Date.now() - 0 * 86400000), y: 0.85 }
			]
		},
		{
			id: 't2',
			name: 'Svelte 5 Runes API',
			color: 'var(--color-success-DEFAULT)',
			halfLifeDays: 8.2,
			totalReviews: 4,
			lastReviewDate: 'Yesterday',
			currentStability: 'Medium',
			data: [
				{ x: new Date(Date.now() - 8 * 86400000), y: 0.5 },
				{ x: new Date(Date.now() - 7 * 86400000), y: 0.42 },
				{ x: new Date(Date.now() - 6 * 86400000), y: 0.38 },
				{ x: new Date(Date.now() - 5 * 86400000), y: 0.98 },
				{ x: new Date(Date.now() - 3 * 86400000), y: 0.82 },
				{ x: new Date(Date.now() - 2 * 86400000), y: 0.74 },
				{ x: new Date(Date.now() - 1 * 86400000), y: 0.96 },
				{ x: new Date(Date.now() - 0 * 86400000), y: 0.91 }
			]
		},
		{
			id: 't3',
			name: 'Rust Borrow Checker',
			color: 'var(--color-error-DEFAULT)',
			halfLifeDays: 4.1,
			totalReviews: 9,
			lastReviewDate: '4 hours ago',
			currentStability: 'Low',
			data: [
				{ x: new Date(Date.now() - 9 * 86400000), y: 0.6 },
				{ x: new Date(Date.now() - 7 * 86400000), y: 0.4 },
				{ x: new Date(Date.now() - 6 * 86400000), y: 0.95 },
				{ x: new Date(Date.now() - 5 * 86400000), y: 0.75 },
				{ x: new Date(Date.now() - 3 * 86400000), y: 0.45 },
				{ x: new Date(Date.now() - 2 * 86400000), y: 0.92 },
				{ x: new Date(Date.now() - 1 * 86400000), y: 0.78 },
				{ x: new Date(Date.now() - 0 * 86400000), y: 0.58 }
			]
		}
	];

	let { topics = mockTopics, class: className = '' }: Props = $props();

	// Keep track of active/selected topic ids
	let selectedIds = $state<string[]>([]);

	$effect(() => {
		if (selectedIds.length === 0 && topics.length > 0) {
			selectedIds = [topics[0].id];
		}
	});

	// Time range selection: 7 days, 30 days
	let timeRange = $state<'7d' | '30d'>('7d');

	function toggleTopic(id: string) {
		if (selectedIds.includes(id)) {
			// Don't allow deselecting the last one
			if (selectedIds.length > 1) {
				selectedIds = selectedIds.filter(x => x !== id);
			}
		} else {
			selectedIds = [...selectedIds, id];
		}
	}

	// Filter data based on selected range
	let filteredTopics = $derived(
		topics.filter(t => selectedIds.includes(t.id))
	);

	// Convert our TopicStrength data format to the LineSeries format
	let chartSeries = $derived<LineSeries[]>(
		filteredTopics.map(t => {
			const cutDate = timeRange === '7d' 
				? new Date(Date.now() - 7 * 86400000) 
				: new Date(Date.now() - 30 * 86400000);
				
			return {
				label: t.name,
				color: t.color,
				data: t.data.filter(pt => (pt.x as Date) >= cutDate)
			};
		})
	);

	// Active single topic for showing detailed metrics panel
	let activeTopic = $derived(
		topics.find(t => t.id === selectedIds[0]) || topics[0]
	);
</script>

<div class="flex flex-col gap-6 brutal-border bg-surface-primary p-6 {className}">
	<!-- Header -->
	<div class="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b-2 border-border-primary pb-4">
		<div>
			<h4 class="font-black text-lg uppercase tracking-tight text-fg-primary">Memory Strength Analysis</h4>
			<p class="text-xs text-fg-secondary font-mono mt-1">Track stability and recall decay history</p>
		</div>
		<div class="flex gap-2">
			<Button 
				variant={timeRange === '7d' ? 'primary' : 'ghost'} 
				class="h-8 text-xs font-mono"
				onclick={() => timeRange = '7d'}
			>
				7d
			</Button>
			<Button 
				variant={timeRange === '30d' ? 'primary' : 'ghost'} 
				class="h-8 text-xs font-mono"
				onclick={() => timeRange = '30d'}
			>
				30d
			</Button>
		</div>
	</div>

	<!-- Topic Selectors -->
	<div class="flex flex-wrap gap-2">
		{#each topics as topic}
			{@const isActive = selectedIds.includes(topic.id)}
			<button
				class="flex items-center gap-2 px-3 py-1.5 brutal-border text-xs font-mono font-bold transition-all shadow-[2px_2px_0px_rgba(0,0,0,1)] hover:translate-y-[-1px] active:translate-y-[1px]"
				class:bg-surface-tertiary={isActive}
				class:bg-surface-primary={!isActive}
				onclick={() => toggleTopic(topic.id)}
			>
				<span class="w-3 h-3 brutal-border" style="background-color: {topic.color};"></span>
				{topic.name}
			</button>
		{/each}
	</div>

	<!-- Main Chart wrapper -->
	<div class="w-full">
		<LineChart 
			series={chartSeries} 
			height={220}
			xIsDate={true}
			class="shadow-[4px_4px_0px_rgba(0,0,0,1)]"
		/>
	</div>

	<!-- Detailed Metrics Cards for the current primary selected topic -->
	{#if activeTopic}
		<div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-2">
			<div class="brutal-border bg-surface-secondary p-3 shadow-[2px_2px_0px_rgba(0,0,0,1)]">
				<div class="text-[9px] font-bold font-mono tracking-wider uppercase text-fg-tertiary">Stability</div>
				<div class="text-lg font-black font-mono mt-1 text-fg-primary">{activeTopic.currentStability}</div>
			</div>
			<div class="brutal-border bg-surface-secondary p-3 shadow-[2px_2px_0px_rgba(0,0,0,1)]">
				<div class="text-[9px] font-bold font-mono tracking-wider uppercase text-fg-tertiary">Half-Life</div>
				<div class="text-lg font-black font-mono mt-1 text-fg-primary">{activeTopic.halfLifeDays} Days</div>
			</div>
			<div class="brutal-border bg-surface-secondary p-3 shadow-[2px_2px_0px_rgba(0,0,0,1)]">
				<div class="text-[9px] font-bold font-mono tracking-wider uppercase text-fg-tertiary">Total Reviews</div>
				<div class="text-lg font-black font-mono mt-1 text-fg-primary">{activeTopic.totalReviews} Times</div>
			</div>
			<div class="brutal-border bg-surface-secondary p-3 shadow-[2px_2px_0px_rgba(0,0,0,1)]">
				<div class="text-[9px] font-bold font-mono tracking-wider uppercase text-fg-tertiary">Last Review</div>
				<div class="text-sm font-black font-mono mt-2 text-fg-primary">{activeTopic.lastReviewDate}</div>
			</div>
		</div>
	{/if}
</div>
