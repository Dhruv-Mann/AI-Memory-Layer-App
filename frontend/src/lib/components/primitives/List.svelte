<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		ordered?: boolean;
		class?: string;
		children: Snippet;
	}

	let {
		ordered = false,
		class: className = '',
		children
	}: Props = $props();
</script>

{#if ordered}
	<ol class="list-decimal list-inside space-y-2 text-fg-primary tracking-tight {className}" role="list">
		{@render children()}
	</ol>
{:else}
	<ul class="space-y-2 text-fg-primary tracking-tight {className}" role="list">
		{@render children()}
	</ul>
{/if}
