<script lang="ts">
	import MemoryChunk, { type MemoryChunkData } from './MemoryChunk.svelte';
	import Button from '../primitives/Button.svelte';

	interface Props {
		query: string;
		chunks: MemoryChunkData[];
		onChunkAction?: (action: 'explain' | 'related' | 'copy', id: string) => void;
		onTopicClick?: (id: string) => void;
		class?: string;
	}

	let {
		query,
		chunks = [],
		onChunkAction,
		onTopicClick,
		class: className = ''
	}: Props = $props();

	let focusedIndex = $state(0);
	// We map string ids to expanded state booleans
	let expandedState = $state<Record<string, boolean>>({});

	function toggleExpand(id: string) {
		expandedState[id] = !expandedState[id];
	}

	function handleKeydown(e: KeyboardEvent) {
		if (chunks.length === 0) return;

		if (e.key === 'ArrowDown') {
			e.preventDefault();
			focusedIndex = Math.min(focusedIndex + 1, chunks.length - 1);
		} else if (e.key === 'ArrowUp') {
			e.preventDefault();
			focusedIndex = Math.max(focusedIndex - 1, 0);
		} else if (e.key === 'Tab') {
			// standard tab index handles button focus natively
			// but we can ensure standard focus flow is preserved
		}
	}
</script>

<!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
<div role="application" class="flex flex-col h-full bg-surface-base outline-none {className}" onkeydown={handleKeydown} tabindex="-1">
	
	<!-- Header -->
	<header class="border-b-4 border-border-base bg-surface-primary p-6 shrink-0">
		<div class="text-[10px] font-bold tracking-widest text-content-tertiary uppercase mb-2">AI Recall Query</div>
		<h2 class="text-2xl font-black tracking-tight text-content-primary">"{query}"</h2>
		
		<div class="flex gap-4 mt-4 text-xs font-mono font-bold text-content-secondary">
			<span class="flex items-center gap-1">
				<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="square"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
				{chunks.length} Contexts Extracted
			</span>
			<span class="flex items-center gap-1 text-success-DEFAULT">
				<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="square"><polyline points="20 6 9 17 4 12"></polyline></svg>
				High Confidence Synth
			</span>
		</div>
	</header>

	<!-- Document Stream -->
	<div class="flex-1 overflow-y-auto p-4 md:p-8 flex flex-col gap-6">
		{#if chunks.length === 0}
			<div class="flex-1 flex flex-col items-center justify-center text-center p-12 opacity-50">
				<div class="text-4xl mb-4">🗄️</div>
				<h3 class="font-bold text-lg mb-2">No contexts retrieved</h3>
				<p class="text-sm font-mono max-w-sm">The recall engine couldn't find memory chunks relevant to this query. Try a different terminology.</p>
			</div>
		{:else}
			{#each chunks as chunk, i (chunk.id)}
				<MemoryChunk 
					data={chunk} 
					isExpanded={!!expandedState[chunk.id]} 
					isFocused={focusedIndex === i}
					onToggleExpand={() => {
						focusedIndex = i; // Move focus to clicked
						toggleExpand(chunk.id);
					}}
					onAction={onChunkAction}
					onTopicClick={onTopicClick}
				/>
			{/each}
		{/if}
	</div>

	<!-- AI Prompt Area -->
	<div class="p-4 border-t-4 border-border-base bg-surface-primary shrink-0">
		<div class="flex gap-2">
			<input 
				type="text" 
				placeholder="Ask for clarification or deeper context..." 
				class="flex-1 h-12 px-4 brutal-border bg-surface-secondary text-content-primary font-mono text-sm focus:outline-none focus:ring-2 focus:ring-brand-primary placeholder:text-content-tertiary"
			/>
			<Button variant="primary" class="h-12 px-6">
				Probe
			</Button>
		</div>
	</div>
</div>