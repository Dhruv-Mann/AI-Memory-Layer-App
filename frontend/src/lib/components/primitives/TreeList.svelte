<script lang="ts" context="module">
	export interface TreeItem {
		id: string;
		label: string;
		expanded?: boolean;
		children?: TreeItem[];
	}
</script>

<script lang="ts">
	interface Props {
		items: TreeItem[];
		level?: number;
		class?: string;
	}

	let {
		items = $bindable([]),
		level = 0,
		class: className = ''
	}: Props = $props();

	function toggle(item: TreeItem) {
		if (item.children && item.children.length > 0) {
			item.expanded = !item.expanded;
		}
	}

	function handleKeydown(e: KeyboardEvent, item: TreeItem) {
		if (e.key === 'Enter' || e.key === ' ') {
			e.preventDefault();
			toggle(item);
		}
	}
</script>

<ul class="flex flex-col {level === 0 ? className : ''}" role={level === 0 ? 'tree' : 'group'}>
	{#each items as item (item.id)}
		<li class="flex flex-col" role="treeitem" aria-expanded={item.children ? !!item.expanded : undefined}>
			<div 
				class="flex items-center gap-2 py-1.5 px-2 hover:bg-surface-secondary cursor-pointer focus:outline-none focus:ring-2 focus:ring-brand-primary border-l-2 border-transparent hover:border-brand-primary transition-all select-none"
				style="padding-left: {level * 1.5 + 0.5}rem"
				tabindex="0"
				onclick={() => toggle(item)}
				onkeydown={(e) => handleKeydown(e, item)}
			>
				{#if item.children && item.children.length > 0}
					<span class="w-4 h-4 flex items-center justify-center font-mono text-xs transition-transform duration-fast {item.expanded ? 'rotate-90' : ''}">
						▶
					</span>
				{:else}
					<span class="w-4 h-4"></span>
				{/if}
				<span class="text-sm font-medium tracking-tight text-fg-primary">{item.label}</span>
			</div>
			
			{#if item.children && item.expanded}
				<svelte:self bind:items={item.children} level={level + 1} />
			{/if}
		</li>
	{/each}
</ul>
