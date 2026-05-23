<script lang="ts">
	interface BreadcrumbItem {
		label: string;
		href?: string;
	}

	interface Props {
		items: BreadcrumbItem[];
		separator?: string;
		class?: string;
	}

	let {
		items,
		separator = '/',
		class: className = ''
	}: Props = $props();

	let shownItems = $derived(
		items.length > 5 
			? [items[0], { label: '...' }, ...items.slice(-3)]
			: items
	);
</script>

<nav aria-label="Breadcrumb" class={className}>
	<ol class="flex flex-wrap items-center gap-2 text-sm font-bold tracking-tight">
		{#each shownItems as item, index}
			<li class="flex items-center">
				{#if item.label === '...'}
					<span class="px-2 py-0.5 bg-surface-tertiary brutal-border flex items-center justify-center">...</span>
				{:else if item.href && index !== shownItems.length - 1}
					<a 
						href={item.href} 
						class="text-fg-secondary hover:text-brand-primary hover:underline underline-offset-4 decoration-2 decoration-brand-primary transition-colors focus:outline-none focus:ring-2 focus:ring-brand-primary px-1"
					>
						{item.label}
					</a>
				{:else}
					<span class="text-fg-primary px-1 border-b-2 border-brand-primary" aria-current="page">
						{item.label}
					</span>
				{/if}

				{#if index < shownItems.length - 1}
					<span class="ml-2 text-fg-tertiary select-none flex items-center h-full" aria-hidden="true">{separator}</span>
				{/if}
			</li>
		{/each}
	</ol>
</nav>
