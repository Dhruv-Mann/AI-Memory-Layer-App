<script lang="ts">
	import type { Snippet } from 'svelte';
	import Button from '../primitives/Button.svelte';

	interface Props {
		open?: boolean;
		position?: 'left' | 'right' | 'top' | 'bottom';
		size?: 'sm' | 'md' | 'lg' | 'full';
		closeOnOverlayClick?: boolean;
		closeOnEscape?: boolean;
		title?: string;
		children: Snippet;
		footer?: Snippet;
		onclose?: () => void;
	}

	let {
		open = $bindable(false),
		position = 'right',
		size = 'md',
		closeOnOverlayClick = true,
		closeOnEscape = true,
		title,
		children,
		footer,
		onclose
	}: Props = $props();

	let dialog: HTMLDialogElement;

	$effect(() => {
		if (dialog) {
			if (open && !dialog.open) {
				dialog.showModal();
			} else if (!open && dialog.open) {
				dialog.close();
			}
		}
	});

	function handleClose() {
		open = false;
		if (onclose) onclose();
	}

	function handleBackdropClick(e: MouseEvent) {
		if (!closeOnOverlayClick) return;
		const rect = dialog.getBoundingClientRect();
		// For dialog, clicking backdrop means clicking outside bounding client rect.
		const isInDialog =
			rect.top <= e.clientY &&
			e.clientY <= rect.top + rect.height &&
			rect.left <= e.clientX &&
			e.clientX <= rect.left + rect.width;
		
		if (!isInDialog) {
			handleClose();
		}
	}

	function handleKeydown(e: KeyboardEvent) {
		if (e.key === 'Escape' && !closeOnEscape) {
			e.preventDefault();
		}
	}

	const positionClasses = {
		left: 'left-0 h-full max-h-screen top-0 bottom-0 mr-auto border-r-2 data-[state=open]:slide-in-from-left',
		right: 'right-0 h-full max-h-screen top-0 bottom-0 ml-auto border-l-2 data-[state=open]:slide-in-from-right',
		top: 'top-0 w-full max-w-screen left-0 right-0 mb-auto border-b-2 data-[state=open]:slide-in-from-top',
		bottom: 'bottom-0 w-full max-w-screen left-0 right-0 mt-auto border-t-2 data-[state=open]:slide-in-from-bottom'
	};

	const sizeClasses = {
		horizontal: {
			sm: 'w-64',
			md: 'w-80',
			lg: 'w-96',
			full: 'w-screen'
		},
		vertical: {
			sm: 'h-48',
			md: 'h-80',
			lg: 'h-96',
			full: 'h-screen'
		}
	};

	let isHorizontal = $derived(position === 'left' || position === 'right');
	let computedWidthHeight = $derived(
		isHorizontal ? sizeClasses.horizontal[size] : sizeClasses.vertical[size]
	);

</script>

<dialog
	bind:this={dialog}
	onclose={handleClose}
	onclick={handleBackdropClick}
	onkeydown={handleKeydown}
	data-state={open ? 'open' : 'closed'}
	class="fixed m-0 p-0 bg-surface-primary text-fg-primary {positionClasses[position]} {computedWidthHeight} border-primary
	backdrop:backdrop-blur-sm backdrop:bg-black/50 transition-transform duration-fast brutal-ease z-50 flex flex-col"
>
	{#if title}
		<div class="px-6 py-4 border-b-2 border-primary flex justify-between items-center bg-surface-secondary shrink-0">
			<h2 class="text-xl font-bold tracking-tight uppercase">{title}</h2>
			<Button variant="ghost" size="sm" onclick={handleClose} aria-label="Close drawer">✕</Button>
		</div>
	{/if}

	<div class="p-6 flex-1 overflow-y-auto">
		{@render children()}
	</div>

	{#if footer}
		<div class="px-6 py-4 border-t-2 border-primary bg-surface-tertiary flex justify-end gap-2 shrink-0">
			{@render footer()}
		</div>
	{/if}
</dialog>

<style>
	dialog {
		margin: 0;
		max-width: none;
		max-height: none;
		background: var(--surface-primary);
		color: var(--text-primary);
		border-color: var(--border-primary);
	}
	/* override user agent defaults */
	dialog::backdrop {
		background: rgba(0, 0, 0, 0.5);
	}
</style>
