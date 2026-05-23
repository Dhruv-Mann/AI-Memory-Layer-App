<script lang="ts">
	import type { Snippet } from 'svelte';
	import { slide } from 'svelte/transition';

	interface Props {
		title: string;
		collapsible?: boolean;
		collapsed?: boolean;
		class?: string;
		children: Snippet;
	}

	let {
		title,
		collapsible = false,
		collapsed = $bindable(false),
		class: className = '',
		children
	}: Props = $props();

	function toggle() {
		if (collapsible) {
			collapsed = !collapsed;
		}
	}
</script>

<section class="flex flex-col border-2 border-primary bg-surface-primary {className}">
	<!-- svelte-ignore a11y_click_events_have_key_events -->
	<!-- svelte-ignore a11y_no_static_element_interactions -->
	<div 
		class="px-4 py-3 flex justify-between items-center bg-surface-tertiary select-none border-b-2 border-transparent transition-colors"
		class:border-primary={!collapsed}
		class:cursor-pointer={collapsible}
		onclick={toggle}
	>
		<h3 class="text-lg font-bold tracking-tight text-fg-primary uppercase">{title}</h3>
		{#if collapsible}
			<button 
				class="w-6 h-6 flex items-center justify-center brutal-border hover:bg-surface-secondary transition-colors"
				aria-expanded={!collapsed}
				aria-label="Toggle section"
			>
				<span class="transform transition-transform delay-75 {collapsed ? 'rotate-0' : 'rotate-180'}">
					▼
				</span>
			</button>
		{/if}
	</div>
	
	{#if !collapsed}
		<div transition:slide={{ duration: 200 }} class="p-4 bg-surface-primary overflow-hidden">
			{@render children()}
		</div>
	{/if}
</section>
