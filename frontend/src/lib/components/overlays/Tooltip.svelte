<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		content: string;
		placement?: 'top' | 'bottom' | 'left' | 'right';
		delay?: number;
		arrow?: boolean;
		children: Snippet;
	}

	let {
		content,
		placement = 'top',
		delay = 300,
		arrow = true,
		children
	}: Props = $props();

	let open = $state(false);
	let timeoutId: number;

	function show() {
		clearTimeout(timeoutId);
		timeoutId = window.setTimeout(() => {
			open = true;
		}, delay);
	}

	function hide() {
		clearTimeout(timeoutId);
		open = false;
	}
</script>

<div
	class="relative inline-block"
	onmouseenter={show}
	onmouseleave={hide}
	onfocus={show}
	onblur={hide}
	role="tooltip"
>
	{@render children()}

	{#if open}
		<div
			class="absolute z-tooltip brutal-border bg-fg-primary text-surface-primary text-xs font-medium px-2 py-1 pointer-events-none animate-in fade-in duration-fast whitespace-nowrap"
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
					class="absolute w-2 h-2 bg-fg-primary"
					class:bottom-[-4px]={placement === 'top'}
					class:left-1/2={placement === 'top' || placement === 'bottom'}
					class:-translate-x-1/2={placement === 'top' || placement === 'bottom'}
					class:rotate-45={true}
					class:top-[-4px]={placement === 'bottom'}
					class:right-[-4px]={placement === 'left'}
					class:top-1/2={placement === 'left' || placement === 'right'}
					class:-translate-y-1/2={placement === 'left' || placement === 'right'}
					class:left-[-4px]={placement === 'right'}
				></div>
			{/if}
			<span class="relative z-10">{content}</span>
		</div>
	{/if}
</div>
