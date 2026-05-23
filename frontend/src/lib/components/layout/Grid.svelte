<script lang="ts">
	import type { Snippet } from 'svelte';
	import type { SpacingToken } from '$lib/types/tokens';

	interface Props {
		children: Snippet;
		columns?: number;
		gap?: SpacingToken;
		minColumnWidth?: string;
		class?: string;
	}

	let {
		children,
		columns,
		gap = '4',
		minColumnWidth = '250px',
		class: className = ''
	}: Props = $props();

	// If columns is explicitly provided, we use a fixed grid.
	// Otherwise, we use auto-fit with the minColumnWidth for responsive masonry.
	let gridTemplateColumns = $derived(
		columns ? `repeat(${columns}, 1fr)` : `repeat(auto-fit, minmax(${minColumnWidth}, 1fr))`
	);
</script>

<div
	class="grid {className}"
	style="
		--grid-gap: var(--space-{gap});
		gap: var(--grid-gap);
		grid-template-columns: {gridTemplateColumns};
	"
>
	{@render children()}
</div>
