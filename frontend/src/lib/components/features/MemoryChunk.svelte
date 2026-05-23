<script lang="ts">
	import { motionSlide } from '../../utils/animations';
	import Button from '../primitives/Button.svelte';
	import KeyboardHint from '../primitives/KeyboardHint.svelte';

	export interface Citation {
		id: string;
		sourceTitle: string;
		url?: string;
	}

	export interface LinkedTopic {
		id: string;
		title: string;
	}

	export interface MemoryChunkData {
		id: string;
		summary: string;
		fullContext: string;
		confidenceScore: number; // 0 to 1
		citations: Citation[];
		linkedTopics: LinkedTopic[];
	}

	interface Props {
		data: MemoryChunkData;
		isExpanded?: boolean;
		isFocused?: boolean;
		onToggleExpand?: () => void;
		onAction?: (action: 'explain' | 'related' | 'copy', id: string) => void;
		onTopicClick?: (id: string) => void;
		class?: string;
	}

	let {
		data,
		isExpanded = false,
		isFocused = false,
		onToggleExpand,
		onAction,
		onTopicClick,
		class: className = ''
	}: Props = $props();

	// Calculate confidence color
	let confidenceColor = $derived(
		data.confidenceScore >= 0.8 ? 'text-success-DEFAULT border-success-DEFAULT bg-success-DEFAULT/10' :
		data.confidenceScore >= 0.5 ? 'text-warning-DEFAULT border-warning-DEFAULT bg-warning-DEFAULT/10' :
		'text-error-DEFAULT border-error-DEFAULT bg-error-DEFAULT/10'
	);

	function handleKeydown(e: KeyboardEvent) {
		if (!isFocused) return;
		
		if (e.key === 'Enter') {
			e.preventDefault();
			if (onToggleExpand) onToggleExpand();
		}
	}
	
	let containerRef: HTMLDivElement;
	$effect(() => {
		if (isFocused && containerRef) {
			containerRef.focus();
		}
	});

</script>

<!-- svelte-ignore a11y_no_noninteractive_tabindex -->
<!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
<div 
	bind:this={containerRef}
	class="flex flex-col brutal-border bg-surface-primary transition-all duration-200 outline-none {className} {isFocused ? 'ring-2 ring-brand-primary ring-offset-2 translate-x-1 outline-none' : ''}"
	tabindex={isFocused ? 0 : -1}
	onkeydown={handleKeydown}
	role="region"
>
	<!-- Header / Summary Section (Always visible) -->
	<!-- svelte-ignore a11y_click_events_have_key_events -->
	<div 
		role="button"
		tabindex="-1"
		class="p-4 cursor-pointer hover:bg-surface-secondary/50 transition-colors"
		onclick={() => onToggleExpand && onToggleExpand()}
	>
		<div class="flex justify-between items-start gap-4 mb-2">
			<h3 class="font-bold text-lg text-content-primary leading-tight">
				{data.summary}
			</h3>
			<div class="shrink-0 flex items-center gap-2">
				<div class="px-2 py-0.5 text-[10px] font-bold tracking-widest uppercase border brutal-border {confidenceColor}">
					{Math.round(data.confidenceScore * 100)}% Conf
				</div>
				{#if isFocused}
					<KeyboardHint keys={['Enter']} />
				{/if}
			</div>
		</div>
		
		<div class="text-xs font-mono text-content-secondary line-clamp-1">
			{#if !isExpanded}
				{data.fullContext}
			{:else}
				<span class="text-brand-primary">Viewing full context...</span>
			{/if}
		</div>
	</div>

	<!-- Expanded Content Section -->
	{#if isExpanded}
		<div 
			class="border-t-2 border-border-base bg-surface-secondary/20 block"
			transition:motionSlide={{ duration: 200 }}
		>
			<div class="p-4 font-mono text-sm text-content-primary leading-relaxed whitespace-pre-wrap">
				{data.fullContext}
			</div>

			<!-- Citations and Links -->
			<div class="p-4 border-t border-border-subtle bg-surface-tertiary/20 flex flex-col gap-3">
				{#if data.citations.length > 0}
					<div class="flex flex-col gap-1">
						<span class="text-[10px] font-bold uppercase tracking-widest text-content-tertiary">Sources</span>
						<ul class="flex flex-wrap gap-x-4 gap-y-1">
							{#each data.citations as citation, i}
								<li class="text-xs font-mono text-brand-secondary hover:text-brand-primary cursor-pointer transition-colors">
									<a href={citation.url} target="_blank" rel="noopener noreferrer">[{i + 1}] {citation.sourceTitle}</a>
								</li>
							{/each}
						</ul>
					</div>
				{/if}

				{#if data.linkedTopics.length > 0}
					<div class="flex flex-col gap-1">
						<span class="text-[10px] font-bold uppercase tracking-widest text-content-tertiary">Linked Topics</span>
						<div class="flex flex-wrap gap-2">
							{#each data.linkedTopics as topic}
								<button 
									class="px-2 py-0.5 border border-warning-DEFAULT bg-warning-DEFAULT/10 text-warning-DEFAULT text-[10px] font-bold uppercase tracking-widest hover:bg-warning-DEFAULT/20 transition-colors brutal-border"
									onclick={(e) => { e.stopPropagation(); onTopicClick?.(topic.id); }}
								>
									{topic.title}
								</button>
							{/each}
						</div>
					</div>
				{/if}
			</div>

			<!-- Actions Toolbar -->
			<div class="p-3 border-t-2 border-border-base bg-surface-primary flex flex-wrap gap-3">
				<Button variant="secondary" size="sm" class="text-xs" onclick={(e) => { e.stopPropagation(); onAction?.('explain', data.id); }}>
					Explain Differently
				</Button>
				<Button variant="secondary" size="sm" class="text-xs" onclick={(e) => { e.stopPropagation(); onAction?.('related', data.id); }}>
					Show Related
				</Button>
				<Button variant="ghost" size="sm" class="ml-auto text-xs gap-1" onclick={(e) => { e.stopPropagation(); onAction?.('copy', data.id); }}>
					<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="square"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
					Copy
				</Button>
			</div>
		</div>
	{/if}
</div>