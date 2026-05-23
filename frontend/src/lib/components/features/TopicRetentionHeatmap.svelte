<script lang="ts">
	import Heatmap from '../charts/Heatmap.svelte';
	import type { HeatmapCell } from '../charts/Heatmap.svelte';
	import Button from '../primitives/Button.svelte';
	import Input from '../primitives/Input.svelte';

	interface TopicItem {
		name: string;
		category: string;
		retention: number; // 0 to 100
		lastReviewed: string;
		halfLifeDays: number;
		reviewsCount: number;
	}

	interface Props {
		topics?: TopicItem[];
		class?: string;
	}

	// Mock data for topics across subjects
	let mockTopics: TopicItem[] = [
		// Frontend
		{ name: 'React strict mode effects', category: 'Frontend', retention: 85, lastReviewed: '2 days ago', halfLifeDays: 12.5, reviewsCount: 6 },
		{ name: 'Svelte 5 Runes API', category: 'Frontend', retention: 92, lastReviewed: 'Yesterday', halfLifeDays: 8.2, reviewsCount: 4 },
		{ name: 'Tailwind CSS v4 updates', category: 'Frontend', retention: 68, lastReviewed: '1 week ago', halfLifeDays: 14.1, reviewsCount: 3 },
		{ name: 'CSS container queries', category: 'Frontend', retention: 45, lastReviewed: '2 weeks ago', halfLifeDays: 5.4, reviewsCount: 2 },
		{ name: 'Web accessibility standards', category: 'Frontend', retention: 74, lastReviewed: '3 days ago', halfLifeDays: 9.8, reviewsCount: 5 },

		// Backend
		{ name: 'Node.js event loop dynamics', category: 'Backend', retention: 88, lastReviewed: '3 days ago', halfLifeDays: 15.2, reviewsCount: 8 },
		{ name: 'PostgreSQL index types', category: 'Backend', retention: 91, lastReviewed: '2 days ago', halfLifeDays: 18.4, reviewsCount: 7 },
		{ name: 'Redis caching strategies', category: 'Backend', retention: 55, lastReviewed: '5 days ago', halfLifeDays: 6.8, reviewsCount: 4 },
		{ name: 'GraphQL schema federation', category: 'Backend', retention: 38, lastReviewed: '3 weeks ago', halfLifeDays: 3.2, reviewsCount: 1 },
		{ name: 'JWT security guidelines', category: 'Backend', retention: 78, lastReviewed: 'Yesterday', halfLifeDays: 11.0, reviewsCount: 5 },

		// Systems
		{ name: 'Rust memory borrow checker', category: 'Systems', retention: 58, lastReviewed: '4 hours ago', halfLifeDays: 4.1, reviewsCount: 9 },
		{ name: 'Docker container networking', category: 'Systems', retention: 70, lastReviewed: '4 days ago', halfLifeDays: 10.5, reviewsCount: 4 },
		{ name: 'Kubernetes ingress controller', category: 'Systems', retention: 42, lastReviewed: '1 week ago', halfLifeDays: 5.1, reviewsCount: 2 },
		{ name: 'Linux process signals', category: 'Systems', retention: 82, lastReviewed: 'Yesterday', halfLifeDays: 20.0, reviewsCount: 10 },
		{ name: 'WebAssembly runtime engine', category: 'Systems', retention: 31, lastReviewed: '1 month ago', halfLifeDays: 2.4, reviewsCount: 1 }
	];

	let { topics = mockTopics, class: className = '' }: Props = $props();

	// Search & filtering state
	let searchFilter = $state('');
	let categoryFilter = $state('All');

	// Selected cell for drill-down view
	let selectedTopicName = $state<string | null>(null);

	// Get unique categories for filtering dropdown
	let categories = $derived(['All', ...Array.from(new Set(topics.map(t => t.category)))]);

	// Filter topics according to search & category filters
	let filteredTopics = $derived(
		topics.filter(t => {
			const matchesSearch = t.name.toLowerCase().includes(searchFilter.toLowerCase());
			const matchesCategory = categoryFilter === 'All' || t.category === categoryFilter;
			return matchesSearch && matchesCategory;
		})
	);

	// Map filtered topics to matrix coordinates for the Heatmap component
	// We want columns to represent topic index within their category, rows as Category names.
	let heatmapCells = $derived.by<HeatmapCell[]>(() => {
		const categoryCounts: Record<string, number> = {};
		
		return filteredTopics.map(t => {
			if (!categoryCounts[t.category]) {
				categoryCounts[t.category] = 0;
			}
			categoryCounts[t.category]++;
			const index = categoryCounts[t.category];

			return {
				x: `Topic ${index}`,
				y: t.category,
				value: t.retention,
				label: t.name // Store full name in label
			};
		});
	});

	// Find the full details of the currently selected/drilled topic
	let selectedTopicDetails = $derived(
		topics.find(t => t.name === selectedTopicName) || null
	);

	function handleCellSelect(cell: HeatmapCell) {
		selectedTopicName = cell.label || null;
	}

	function clearSelection() {
		selectedTopicName = null;
	}

	// Custom color scale matching retention health (Red for decay, Green for mastered)
	let colors = [
		'var(--color-error-light)', // decayed/forgotten
		'var(--color-warning-light)', // low retention
		'rgba(var(--color-primary-rgb, 139, 92, 246), 0.4)', // learning/medium
		'rgba(var(--color-primary-rgb, 139, 92, 246), 0.8)', // high retention
		'var(--color-success-DEFAULT)' // mastered
	];

	function tooltipFormatter(cell: HeatmapCell): string {
		return `${cell.label}: ${cell.value}% Retention`;
	}
</script>

<div class="flex flex-col gap-6 brutal-border bg-surface-primary p-6 {className}">
	<!-- Header -->
	<div class="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b-2 border-border-primary pb-4">
		<div>
			<h4 class="font-black text-lg uppercase tracking-tight text-fg-primary">Topic Retention Heatmap</h4>
			<p class="text-xs text-fg-secondary font-mono mt-1">Matrix of conceptual mastery stability across subjects</p>
		</div>
	</div>

	<!-- Controls Toolbar -->
	<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
		<div class="md:col-span-2">
			<Input 
				placeholder="Search topic name..." 
				bind:value={searchFilter}
				class="w-full font-mono text-xs"
			/>
		</div>
		<div>
			<select
				bind:value={categoryFilter}
				class="w-full h-10 brutal-border bg-surface-primary text-xs font-mono font-bold px-3 shadow-[2px_2px_0px_rgba(0,0,0,1)] outline-none"
			>
				{#each categories as cat}
					<option value={cat}>{cat}</option>
				{/each}
			</select>
		</div>
	</div>

	<!-- Interactive Heatmap Area -->
	<div class="relative w-full">
		{#if heatmapCells.length === 0}
			<div class="flex items-center justify-center brutal-border bg-surface-secondary py-12 text-center text-xs font-mono font-bold text-fg-tertiary">
				No topics matched your search parameters.
			</div>
		{:else}
			<!-- svelte-ignore a11y_click_events_have_key_events -->
			<!-- svelte-ignore a11y_no_static_element_interactions -->
			<div onclick={(e) => {
				// We can intercept click coordinates inside Heatmap or check selection
				// Since Heatmap contains hover states, we can handle it directly or let user click cell.
			}}>
				<Heatmap 
					data={heatmapCells} 
					{colors}
					height={180}
					{tooltipFormatter}
					class="shadow-[4px_4px_0px_rgba(0,0,0,1)]"
					margin={{ top: 20, right: 20, bottom: 30, left: 65 }}
				/>
			</div>
			
			<p class="text-[10px] text-fg-tertiary font-mono italic mt-2">
				* Click cells below to drill down into specific topic metrics.
			</p>

			<!-- Quick Grid helper to select topic directly by list in dashboard drill-down -->
			<div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2 mt-4 max-h-32 overflow-y-auto brutal-border p-2 bg-surface-secondary">
				{#each filteredTopics as t}
					<button
						class="text-[10px] font-mono font-bold truncate p-1.5 brutal-border text-left shadow-[1px_1px_0px_rgba(0,0,0,1)] hover:bg-surface-tertiary transition-all"
						class:bg-surface-tertiary={selectedTopicName === t.name}
						class:bg-surface-primary={selectedTopicName !== t.name}
						onclick={() => selectedTopicName = t.name}
					>
						{t.name}
					</button>
				{/each}
			</div>
		{/if}
	</div>

	<!-- Drill Down Side/Bottom Panel -->
	{#if selectedTopicDetails}
		<div 
			class="brutal-border p-5 bg-surface-secondary shadow-[3px_3px_0px_rgba(0,0,0,1)] flex flex-col md:flex-row justify-between items-start md:items-center gap-6 animate-in fade-in slide-in-from-top-2 duration-normal"
		>
			<div class="flex-1 flex flex-col gap-2">
				<div class="flex items-center gap-2">
					<span class="text-[9px] font-mono font-bold uppercase tracking-wider bg-fg-primary text-surface-primary px-1.5 py-0.5 brutal-border">
						{selectedTopicDetails.category}
					</span>
					<span class="text-[10px] font-mono font-bold text-fg-tertiary">
						Last reviewed {selectedTopicDetails.lastReviewed}
					</span>
				</div>
				<h5 class="font-black text-base uppercase tracking-tight text-fg-primary">{selectedTopicDetails.name}</h5>
				
				<div class="flex items-center gap-6 mt-1 text-xs font-mono font-bold">
					<div>
						<span class="text-fg-secondary">Half-Life:</span>
						<span class="text-fg-primary">{selectedTopicDetails.halfLifeDays} Days</span>
					</div>
					<div>
						<span class="text-fg-secondary">Total Reviews:</span>
						<span class="text-fg-primary">{selectedTopicDetails.reviewsCount} Times</span>
					</div>
				</div>
			</div>

			<!-- Retention Score progress & actions -->
			<div class="shrink-0 w-full md:w-auto flex flex-col sm:flex-row items-center gap-4">
				<div class="flex flex-col items-center gap-1 min-w-[80px]">
					<div class="text-[9px] font-bold font-mono uppercase text-fg-tertiary">Retention</div>
					<div 
						class="text-2xl font-black font-mono leading-none"
						style="color: {selectedTopicDetails.retention >= 80 ? 'var(--color-success-DEFAULT)' : selectedTopicDetails.retention >= 50 ? 'var(--color-warning-DEFAULT)' : 'var(--color-error-DEFAULT)'}"
					>
						{selectedTopicDetails.retention}%
					</div>
				</div>
				<div class="flex gap-2 w-full sm:w-auto">
					<Button variant="primary" class="h-10 px-4 text-xs">
						Review Now
					</Button>
					<Button variant="ghost" class="h-10 px-3 text-xs" onclick={clearSelection}>
						Dismiss
					</Button>
				</div>
			</div>
		</div>
	{/if}
</div>
