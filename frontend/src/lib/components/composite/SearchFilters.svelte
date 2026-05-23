<script lang="ts">
	import { browser } from '$app/environment';
	import Button from '../primitives/Button.svelte';

	export interface FilterState {
		type: string[];
		tags: string[];
		dateRange: 'all' | 'today' | 'week' | 'month' | 'year';
	}

	interface Props {
		state?: FilterState;
		onStateChange?: (state: FilterState) => void;
		availableTags?: string[];
		availableTypes?: string[];
		class?: string;
	}

	const defaultState: FilterState = {
		type: [],
		tags: [],
		dateRange: 'all'
	};

	let {
		state = $bindable(defaultState),
		onStateChange,
		availableTags = ['concept', 'definition', 'code', 'research'],
		availableTypes = ['markdown', 'pdf', 'image', 'code'],
		class: className = ''
	}: Props = $props();

	// Session storage hydration/persistence
	$effect(() => {
		if (browser) {
			const saved = sessionStorage.getItem('ai_memory_search_filters');
			if (saved) {
				try {
					const parsed = JSON.parse(saved);
					state = { ...defaultState, ...parsed };
				} catch (e) {
					console.error("Failed to parse search filters from session storage", e);
				}
			}
		}
	});

	$effect(() => {
		if (browser) {
			sessionStorage.setItem('ai_memory_search_filters', JSON.stringify(state));
			if (onStateChange) {
				onStateChange(state);
			}
		}
	});

	function toggleTag(tag: string) {
		if (state.tags.includes(tag)) {
			state.tags = state.tags.filter(t => t !== tag);
		} else {
			state.tags = [...state.tags, tag];
		}
	}

	function toggleType(tType: string) {
		if (state.type.includes(tType)) {
			state.type = state.type.filter(t => t !== tType);
		} else {
			state.type = [...state.type, tType];
		}
	}

	function setDateRange(range: FilterState['dateRange']) {
		state.dateRange = range;
	}

	function removeFilter(category: keyof FilterState, value?: string) {
		if (category === 'dateRange') {
			state.dateRange = 'all';
		} else if (category === 'tags' && value) {
			state.tags = state.tags.filter(t => t !== value);
		} else if (category === 'type' && value) {
			state.type = state.type.filter(t => t !== value);
		}
	}

	let activeFilterCount = $derived(
		state.tags.length + state.type.length + (state.dateRange !== 'all' ? 1 : 0)
	);

</script>

<div class="flex flex-col gap-4 {className}">
	<!-- Active Filters Bar -->
	{#if activeFilterCount > 0}
		<div class="flex flex-wrap gap-2 items-center bg-surface-secondary p-2 brutal-border">
			<span class="text-xs font-bold font-mono text-content-secondary uppercase tracking-wider mr-2">Active:</span>
			
			{#if state.dateRange !== 'all'}
				<div class="flex items-center gap-1 bg-surface-primary border border-border-base px-2 py-0.5 shadow-[1px_1px_0px_rgba(0,0,0,1)]">
					<span class="text-xs font-bold">Date: {state.dateRange}</span>
					<button onclick={() => removeFilter('dateRange')} class="hover:text-error-DEFAULT transition-colors" aria-label="Remove date filter">
						<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
					</button>
				</div>
			{/if}

			{#each state.type as actType}
				<div class="flex items-center gap-1 bg-surface-primary border border-brand-primary px-2 py-0.5 text-brand-secondary shadow-[1px_1px_0px_rgba(0,0,0,1)]">
					<span class="text-xs font-bold">Type: {actType}</span>
					<button onclick={() => removeFilter('type', actType)} class="hover:text-error-DEFAULT transition-colors" aria-label="Remove type filter">
						<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
					</button>
				</div>
			{/each}

			{#each state.tags as actTag}
				<div class="flex items-center gap-1 bg-surface-primary border border-warning-DEFAULT px-2 py-0.5 text-warning-secondary shadow-[1px_1px_0px_rgba(0,0,0,1)]">
					<span class="text-xs font-bold">Tag: {actTag}</span>
					<button onclick={() => removeFilter('tags', actTag)} class="hover:text-error-DEFAULT transition-colors" aria-label="Remove tag filter">
						<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
					</button>
				</div>
			{/each}

			<div class="ml-auto">
				<Button variant="ghost" size="sm" class="h-6 text-xs py-0" onclick={() => { state.tags = []; state.type = []; state.dateRange = 'all'; }}>
					Clear All
				</Button>
			</div>
		</div>
	{/if}

	<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
		<!-- Time Range -->
		<div class="flex flex-col gap-2">
			<h4 class="text-sm font-bold uppercase tracking-widest text-content-secondary border-b-2 border-border-subtle pb-1">Modified</h4>
			<div class="flex flex-wrap gap-2 mt-2">
				{#each ['all', 'today', 'week', 'month', 'year'] as range}
					<button 
						class="px-2 py-1 text-xs font-bold capitalize transition-colors {state.dateRange === range ? 'bg-content-primary text-surface-primary' : 'bg-surface-secondary text-content-secondary hover:bg-surface-tertiary border border-border-subtle'}"
						onclick={() => setDateRange(range as FilterState['dateRange'])}
					>
						{range}
					</button>
				{/each}
			</div>
		</div>

		<!-- File Types -->
		<div class="flex flex-col gap-2">
			<h4 class="text-sm font-bold uppercase tracking-widest text-content-secondary border-b-2 border-border-subtle pb-1">Source Type</h4>
			<div class="flex flex-wrap gap-2 mt-2">
				{#each availableTypes as aType}
					<button 
						class="px-2 py-1 text-xs font-bold capitalize border-2 transition-all {state.type.includes(aType) ? 'border-brand-primary bg-brand-primary/10 text-brand-secondary' : 'border-border-subtle text-content-secondary hover:border-brand-muted hover:bg-surface-secondary'}"
						onclick={() => toggleType(aType)}
					>
						{aType}
					</button>
				{/each}
			</div>
		</div>

		<!-- Tags -->
		<div class="flex flex-col gap-2">
			<h4 class="text-sm font-bold uppercase tracking-widest text-content-secondary border-b-2 border-border-subtle pb-1">Subject Tags</h4>
			<div class="flex flex-wrap gap-2 mt-2">
				{#each availableTags as aTag}
					<button 
						class="px-2 py-1 text-xs font-bold capitalize border-2 transition-all {state.tags.includes(aTag) ? 'border-warning-DEFAULT bg-warning-DEFAULT/10 text-warning-secondary' : 'border-border-subtle text-content-secondary hover:border-warning-muted hover:bg-surface-secondary'}"
						onclick={() => toggleTag(aTag)}
					>
						#{aTag}
					</button>
				{/each}
			</div>
		</div>
	</div>
</div>