<script lang="ts" context="module">
	export interface InteractiveListItem {
		id: string | number;
		label: string;
		disabled?: boolean;
	}
</script>

<script lang="ts">
	interface Props {
		items: InteractiveListItem[];
		selectedId?: string | number | null;
		class?: string;
		onselect?: (item: InteractiveListItem) => void;
	}

	let {
		items,
		selectedId = $bindable(null),
		class: className = '',
		onselect
	}: Props = $props();

	function handleKeydown(e: KeyboardEvent, index: number) {
		let newIndex = index;
		if (e.key === 'ArrowDown') newIndex = (index + 1) % items.length;
		if (e.key === 'ArrowUp') newIndex = (index - 1 + items.length) % items.length;
		if (e.key === 'Home') newIndex = 0;
		if (e.key === 'End') newIndex = items.length - 1;

		if (e.key === 'Enter' || e.key === ' ') {
			e.preventDefault();
			selectItem(items[index]);
			return;
		}

		if (newIndex !== index) {
			e.preventDefault();
			const list = e.currentTarget?.parentElement;
			if (list) {
				const itemsEl = list.querySelectorAll('li');
				(itemsEl[newIndex] as HTMLElement)?.focus();
			}
		}
	}

	function selectItem(item: InteractiveListItem) {
		if (item.disabled) return;
		selectedId = item.id;
		if (onselect) onselect(item);
	}
</script>

<ul class="brutal-border bg-surface-primary flex flex-col {className}" role="listbox">
	{#each items as item, i (item.id)}
		<!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
		<li
			role="option"
			aria-selected={selectedId === item.id}
			aria-disabled={item.disabled}
			tabindex={item.disabled ? -1 : 0}
			onclick={() => selectItem(item)}
			onkeydown={(e) => handleKeydown(e, i)}
			class="px-4 py-3 border-b-2 border-transparent last:border-b-0 focus:outline-none transition-colors 
			{item.disabled 
				? 'opacity-50 cursor-not-allowed bg-surface-tertiary' 
				: 'cursor-pointer hover:bg-surface-secondary'} 
			{selectedId === item.id 
				? 'bg-brand-primary text-white font-bold border-brand-primary' 
				: 'text-fg-primary border-primary'}"
		>
			{item.label}
		</li>
	{/each}
</ul>
