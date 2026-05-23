<script lang="ts">
	// @ts-expect-error - svelte-virtual has incomplete types for Svelte 5
	import VirtualList from 'svelte-virtual';
	import type { Snippet } from 'svelte';

	interface Props {
		items: any[];
		height?: string;
		itemHeight?: number;
		class?: string;
		children: Snippet<[any, number]>;
	}

	let {
		items,
		height = '400px',
		itemHeight,
		class: className = '',
		children
	}: Props = $props();
</script>

<div class="brutal-border bg-surface-primary overflow-hidden {className}" style="height: {height};">
	<VirtualList {items} {itemHeight} let:item let:index>
		{@render children(item, index)}
	</VirtualList>
</div>
