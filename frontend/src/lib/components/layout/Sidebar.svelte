<script lang="ts">
	import type { Snippet } from 'svelte';
	import type { SpacingToken } from '$lib/types/tokens';

	interface Props {
		sidebar: Snippet;
		content: Snippet;
		sidebarWidth?: string;
		contentMinWidth?: string;
		side?: 'left' | 'right';
		gap?: SpacingToken;
		class?: string;
	}

	let {
		sidebar,
		content,
		sidebarWidth = '300px',
		contentMinWidth = '50%',
		side = 'left',
		gap = '0',
		class: className = ''
	}: Props = $props();
</script>

<div class="sidebar-layout {className}" style="--sidebar-gap: var(--space-{gap}); gap: var(--sidebar-gap);">
	{#if side === 'left'}
		<aside class="sidebar-slot" style="flex-basis: {sidebarWidth};">
			{@render sidebar()}
		</aside>
		<main class="content-slot" style="min-width: {contentMinWidth};">
			{@render content()}
		</main>
	{:else}
		<main class="content-slot" style="min-width: {contentMinWidth};">
			{@render content()}
		</main>
		<aside class="sidebar-slot" style="flex-basis: {sidebarWidth};">
			{@render sidebar()}
		</aside>
	{/if}
</div>

<style>
	.sidebar-layout {
		display: flex;
		flex-wrap: wrap;
	}

	.sidebar-slot {
		flex-grow: 1;
	}

	.content-slot {
		flex-basis: 0;
		flex-grow: 999;
	}
</style>
