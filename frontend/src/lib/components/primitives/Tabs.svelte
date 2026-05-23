<script lang="ts" context="module">
	export interface TabItem {
		id: string;
		label: string;
		content: import('svelte').Snippet;
	}
</script>

<script lang="ts">
	interface Props {
		items: TabItem[];
		activeId?: string;
		orientation?: 'horizontal' | 'vertical';
		class?: string;
	}

	let {
		items,
		activeId = $bindable(items[0]?.id),
		orientation = 'horizontal',
		class: className = ''
	}: Props = $props();

	function handleKeydown(e: KeyboardEvent, index: number) {
		let newIndex = index;
		if (orientation === 'horizontal') {
			if (e.key === 'ArrowRight') newIndex = (index + 1) % items.length;
			if (e.key === 'ArrowLeft') newIndex = (index - 1 + items.length) % items.length;
		} else {
			if (e.key === 'ArrowDown') newIndex = (index + 1) % items.length;
			if (e.key === 'ArrowUp') newIndex = (index - 1 + items.length) % items.length;
		}
		if (e.key === 'Home') newIndex = 0;
		if (e.key === 'End') newIndex = items.length - 1;

		if (newIndex !== index) {
			activeId = items[newIndex].id;
			const list = e.currentTarget?.parentElement;
			if (list) {
				const btns = list.querySelectorAll('button[role="tab"]');
				(btns[newIndex] as HTMLElement)?.focus();
			}
			e.preventDefault();
		}
	}
</script>

<div class="flex brutal-border bg-surface-primary {orientation === 'vertical' ? 'flex-row' : 'flex-col'} {className}">
	<div 
		role="tablist" 
		aria-orientation={orientation}
		class="flex {orientation === 'vertical' ? 'flex-col border-r-2' : 'flex-row border-b-2'} border-primary bg-surface-secondary"
	>
		{#each items as item, index}
			<button
				role="tab"
				aria-selected={activeId === item.id}
				aria-controls="panel-{item.id}"
				id="tab-{item.id}"
				tabindex={activeId === item.id ? 0 : -1}
				onclick={() => (activeId = item.id)}
				onkeydown={(e) => handleKeydown(e, index)}
				class="px-5 py-3 font-bold tracking-tight uppercase text-sm border-2 border-transparent transition-colors focus:outline-none focus:bg-surface-tertiary
				{activeId === item.id 
					? 'bg-surface-primary text-brand-primary ' + (orientation === 'vertical' ? 'border-y-primary border-l-primary -mr-[2px]' : 'border-t-primary border-x-primary -mb-[2px] z-10') 
					: 'text-fg-secondary hover:bg-surface-tertiary hover:text-fg-primary'}"
			>
				{item.label}
			</button>
		{/each}
	</div>
	
	<div class="flex-1 p-6 relative">
		{#each items as item}
			{#if activeId === item.id}
				<div 
					role="tabpanel"
					id="panel-{item.id}"
					aria-labelledby="tab-{item.id}"
					tabindex="0"
					class="focus:outline-none w-full h-full animate-in fade-in duration-fast"
				>
					{@render item.content()}
				</div>
			{/if}
		{/each}
	</div>
</div>
