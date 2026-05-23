<script module lang="ts">
	export interface SearchResult {
		id: string;
		title: string;
		preview: string; // The text preview
		sourceFile: string;
		lastModified: string | Date;
		relevanceScore: number; // 0 to 1
		tags?: string[];
	}
</script>

<script lang="ts">
	import KeyboardHint from '../primitives/KeyboardHint.svelte';
	import { handleArrowNavigation, handleEnter } from '../../utils/navigation';
	import { browser } from '$app/environment';

	interface Props {
		results: SearchResult[];
		searchQuery: string;
		onSelect?: (result: SearchResult) => void;
		class?: string;
	}

	let { results, searchQuery, onSelect, class: className = '' }: Props = $props();

	let selectedIndex = $state(-1);
	let listContainer: HTMLDivElement;

	$effect(() => {
		if (results.length > 0 && selectedIndex === -1) {
			selectedIndex = 0;
		} else if (results.length === 0) {
			selectedIndex = -1;
		}
	});

	// Simple client-side text highlighter that wraps matches in a mark tag.
	function highlightText(text: string, query: string) {
		if (!query.trim()) return text;
		// Escape query for regex
		const escapedQuery = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
		const regex = new RegExp(`(${escapedQuery})`, 'gi');
		// We use an incredibly simple string split/join to inject HTML safely, 
		// but since we are returning HTML we'll just format it carefully.
		// Note: the caller uses {@html highlightText(...)} which demands sanitized text.
		// We'll trust the preview is mostly text.
		
		const parts = text.split(regex);
		return parts.map(p => 
			p.toLowerCase() === query.toLowerCase() 
				? `<mark class="bg-brand-primary/20 text-brand-primary font-bold px-0.5 rounded-sm">${escapeHtml(p)}</mark>`
				: escapeHtml(p)
		).join('');
	}

	function escapeHtml(unsafe: string) {
		return unsafe
			.replace(/&/g, "&amp;")
			.replace(/</g, "&lt;")
			.replace(/>/g, "&gt;")
			.replace(/"/g, "&quot;")
			.replace(/'/g, "&#039;");
	}

	function getScoreLabel(score: number): { label: string, colorClass: string } {
		if (score >= 0.8) return { label: 'High Match', colorClass: 'text-success-DEFAULT border-success-DEFAULT' };
		if (score >= 0.5) return { label: 'Good Match', colorClass: 'text-brand-primary border-brand-primary' };
		return { label: 'Low Match', colorClass: 'text-warning-DEFAULT border-warning-DEFAULT' };
	}

	function handleKeydown(e: KeyboardEvent) {
		if (results.length === 0) return;
		
		if (e.key === 'ArrowDown') {
			e.preventDefault();
			selectedIndex = (selectedIndex + 1) % results.length;
			scrollIntoView();
		} else if (e.key === 'ArrowUp') {
			e.preventDefault();
			selectedIndex = (selectedIndex - 1 + results.length) % results.length;
			scrollIntoView();
		} else if (e.key === 'Enter') {
			e.preventDefault();
			if (selectedIndex >= 0 && selectedIndex < results.length && onSelect) {
				onSelect(results[selectedIndex]);
			}
		}
	}

	function scrollIntoView() {
		if (!browser) return;
		setTimeout(() => {
			const selectedItems = listContainer?.querySelectorAll('[aria-selected="true"]');
			if (selectedItems && selectedItems.length > 0) {
				selectedItems[0].scrollIntoView({ block: 'nearest', behavior: 'smooth' });
			}
		}, 0);
	}
</script>

<div
	bind:this={listContainer}
	class="flex flex-col overflow-y-auto outline-none {className}"
	role="listbox"
	tabindex="0"
	onkeydown={handleKeydown}
	aria-label="Search results"
>
	{#if results.length === 0}
		<div class="flex-1 flex flex-col items-center justify-center p-12 text-center">
			<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" class="text-content-quaternary mb-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="square" stroke-linejoin="miter">
				<circle cx="11" cy="11" r="8"></circle>
				<line x1="21" y1="21" x2="16.65" y2="16.65"></line>
				<line x1="11" y1="8" x2="11" y2="14" stroke-dasharray="2 2"></line>
			</svg>
			<h3 class="text-lg font-bold text-content-primary mb-2">No results found</h3>
			<p class="text-sm text-content-secondary max-w-sm">We couldn't find any memories matching "{searchQuery}". Try using different keywords, checking for typos, or broadening your filters.</p>
		</div>
	{:else}
		<div class="divide-y-2 divide-border-subtle border-t-2 border-b-2 border-border-base bg-surface-base">
			{#each results as result, i (result.id)}
				{@const isSelected = selectedIndex === i}
				{@const scoreInfo = getScoreLabel(result.relevanceScore)}
				
				<!-- svelte-ignore a11y_click_events_have_key_events -->
				<!-- svelte-ignore a11y_interactive_supports_focus -->
				<div
					role="option"
					id="result-{result.id}"
					tabindex="-1"
					aria-selected={isSelected}
					class="p-4 cursor-pointer transition-all brutal-inner-border {isSelected ? 'bg-surface-secondary shadow-sm translate-x-1 outline-none ring-2 ring-inset ring-brand-primary' : 'hover:bg-surface-secondary/50'}"
					onclick={() => onSelect?.(result)}
					onmousemove={() => { if (selectedIndex !== i) selectedIndex = i; }}
				>
					<div class="flex justify-between items-start mb-2 gap-4">
						<h4 class="font-bold text-base text-content-primary">
							{@html highlightText(result.title, searchQuery)}
						</h4>
						
						<!-- Metadata Right Side -->
						<div class="flex items-center gap-3 shrink-0">
							<div class="px-2 py-0.5 text-[10px] font-bold tracking-widest uppercase border {scoreInfo.colorClass} bg-surface-primary">
								{Math.round(result.relevanceScore * 100)}% Match
							</div>
							{#if isSelected && onSelect}
								<KeyboardHint keys={['Enter']} />
							{/if}
						</div>
					</div>

					<p class="text-sm text-content-secondary line-clamp-2 leading-relaxed mb-3 font-mono">
						{@html highlightText(result.preview, searchQuery)}
					</p>

					<div class="flex items-center flex-wrap gap-2 text-xs font-mono text-content-tertiary">
						<span class="flex items-center gap-1">
							<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="square"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg>
							{result.sourceFile}
						</span>
						<span class="text-border-base">•</span>
						<span class="flex items-center gap-1">
							<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="square"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
							{typeof result.lastModified === 'string' ? result.lastModified : result.lastModified.toLocaleDateString()}
						</span>
						
						{#if result.tags && result.tags.length > 0}
							<span class="text-border-base">•</span>
							<div class="flex gap-1">
								{#each result.tags as tag}
									<span class="px-1.5 py-0.5 bg-surface-tertiary text-content-secondary uppercase tracking-wider text-[9px] font-bold">
										{tag}
									</span>
								{/each}
							</div>
						{/if}
					</div>
				</div>
			{/each}
		</div>
	{/if}
</div>