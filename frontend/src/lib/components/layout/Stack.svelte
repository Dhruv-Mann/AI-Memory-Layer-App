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
		align = 'stretch',
		justify = 'start',
		wrap = false,
		class: className = ''
	}: Props = $props();

	// Map gap tokens to tailwind classes assuming gap-{spacing} matches tailwind default setup (0, 1, 2, 3, 4, 6, 8, 12, 16, 24, 32)
	// We use an inline style mapped to our custom property just to be perfectly generic and support custom variables in dynamic density.
</script>

<div
	class="flex flex-col {className}"
	style="
		--stack-gap: var(--space-{gap});
		gap: var(--stack-gap);
		align-items: {align};
		justify-content: {justify};
		flex-wrap: {wrap ? 'wrap' : 'nowrap'};
	"
>
	{@render children()}
</div>
