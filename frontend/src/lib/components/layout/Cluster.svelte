<script lang="ts">
	import type { Snippet } from 'svelte';
	import type { SpacingToken } from '$lib/types/tokens';

	interface Props {
		children: Snippet;
		gap?: SpacingToken;
		align?: 'start' | 'center' | 'end' | 'stretch' | 'baseline';
		justify?: 'start' | 'center' | 'end' | 'between' | 'around' | 'evenly';
		wrap?: boolean;
		class?: string;
	}

	let {
		children,
		gap = '4',
		align = 'center',
		justify = 'start',
		wrap = true,
		class: className = ''
	}: Props = $props();
</script>

<div
	class="flex flex-row {className}"
	style="
		--cluster-gap: var(--space-{gap});
		gap: var(--cluster-gap);
		align-items: {align};
		justify-content: {justify};
		flex-wrap: {wrap ? 'wrap' : 'nowrap'};
	"
>
	{@render children()}
</div>
