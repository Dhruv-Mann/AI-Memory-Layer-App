<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		open?: boolean;
		placement?: 'top' | 'bottom' | 'left' | 'right';
		offset?: number;
		arrow?: boolean;
		trigger: Snippet;
		content: Snippet;
	}

	let {
		open = $bindable(false),
		placement = 'bottom',
		offset = 8,
		arrow = true,
		trigger,
		content
	}: Props = $props();

	let triggerEl: HTMLDivElement | undefined = $state();
	let popoverEl: HTMLDivElement | undefined = $state();
    
	function toggle() {
		open = !open;
	}
	
	function close() {
		open = false;
	}

	// Click outside to close
	function handleClickOutside(event: MouseEvent) {
		if (open && popoverEl && !popoverEl.contains(event.target as Node) && triggerEl && !triggerEl.contains(event.target as Node)) {
			close();
		}
	}

	function handleKeydown(event: KeyboardEvent) {
		if (event.key === 'Escape' && open) {
			close();
		}
	}
</script>

<svelte:window onclick={handleClickOutside} onkeydown={handleKeydown} />

<div class="relative inline-block" bind:this={triggerEl}>
	<!-- svelte-ignore a11y_click_events_have_key_events -->
	<!-- svelte-ignore a11y_no_static_element_interactions -->
	<div onclick={toggle}>
		{@render trigger()}
	</div>

	{#if open}
		<div
			bind:this={popoverEl}
			class="absolute z-dropdown brutal-card p-4 min-w-[200px] animate-in fade-in zoom-in-95 duration-fast"
			class:bottom-full={placement === 'top'}
			class:mb-2={placement === 'top'}
			class:top-full={placement === 'bottom'}
			class:mt-2={placement === 'bottom'}
			class:right-full={placement === 'left'}
			class:mr-2={placement === 'left'}
			class:left-full={placement === 'right'}
			class:ml-2={placement === 'right'}
			style="
				--tw-translate-x: {placement === 'left' || placement === 'right' ? '0' : '-50%'};
				--tw-translate-y: {placement === 'top' || placement === 'bottom' ? '0' : '-50%'};
				left: {placement === 'top' || placement === 'bottom' ? '50%' : 'auto'};
				transform: translate(var(--tw-translate-x), var(--tw-translate-y));
			"
		>
			{#if arrow}
				<div
					class="absolute w-3 h-3 bg-surface-primary border-t-2 border-l-2 border-primary {placement === 'top' ? 'bottom-[-7px] left-1/2 -translate-x-1/2 rotate-[-135deg]' : ''} {placement === 'bottom' ? 'top-[-7px] left-1/2 -translate-x-1/2 rotate-[45deg]' : ''} {placement === 'left' ? 'right-[-7px] top-1/2 -translate-y-1/2 rotate-[135deg]' : ''} {placement === 'right' ? 'left-[-7px] top-1/2 -translate-y-1/2 rotate-[-45deg]' : ''}"
				></div>
			{/if}
			<div class="relative z-10">
				{@render content()}
			</div>
		</div>
	{/if}
</div>
