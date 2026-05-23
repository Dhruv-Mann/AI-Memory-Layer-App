<script lang="ts">
	import type { Snippet } from 'svelte';
	import type { SpacingToken } from '$lib/types/tokens';

	interface Props {
		children: Snippet;
		padding?: SpacingToken;
		hover?: boolean;
		interactive?: boolean;
		class?: string;
	}

	let {
		children,
		padding = '4',
		hover = false,
		interactive = false,
		class: className = ''
	}: Props = $props();

	let computedClasses = $derived(
		[
			'brutal-card block w-full text-left transition-all duration-fast ease-brutal',
			hover ? 'hover:brutal-shadow-xl hover:-translate-y-1' : '',
			interactive ? 'cursor-pointer active:translate-y-px active:brutal-shadow-md focus:outline-none focus:ring-2 focus:ring-brand-primary focus:ring-offset-2' : '',
			className
		].filter(Boolean).join(' ')
	);
</script>

<!-- We render as a button if it's interactive for a11y, otherwise a div -->
{#if interactive}
	<button class={computedClasses} style="--card-pad: var(--space-{padding});">
		{@render children()}
	</button>
{:else}
	<div class={computedClasses} style="--card-pad: var(--space-{padding});">
		{@render children()}
	</div>
{/if}
