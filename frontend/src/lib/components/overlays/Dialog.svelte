<script lang="ts">
	import type { Snippet } from 'svelte';
	import Button from '../primitives/Button.svelte';

	interface Props {
		open?: boolean;
		title?: string;
		description?: string;
		size?: 'sm' | 'md' | 'lg' | 'xl' | 'full';
		closeOnOverlayClick?: boolean;
		closeOnEscape?: boolean;
		showCloseButton?: boolean;
		children: Snippet;
		footer?: Snippet;
		onclose?: () => void;
	}

	let {
		open = $bindable(false),
		title,
		description,
		size = 'md',
		closeOnOverlayClick = true,
		closeOnEscape = true,
		showCloseButton = true,
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

	const sizeClasses = {
		sm: 'max-w-sm',
		md: 'max-w-md',
		lg: 'max-w-lg',
		xl: 'max-w-xl',
		full: 'max-w-screen-xl h-[calc(100vh-4rem)]'
	};
</script>

<dialog
	bind:this={dialog}
	onclose={handleClose}
	onclick={handleBackdropClick}
	onkeydown={handleKeydown}
	aria-labelledby={title ? 'dialog-title' : undefined}
	aria-describedby={description ? 'dialog-description' : undefined}
	class="brutal-card p-0 m-auto {sizeClasses[size]} w-[calc(100%-2rem)] backdrop:backdrop-blur-sm backdrop:bg-black/50 open:animate-in open:fade-in open:zoom-in-95 duration-fast"
>
	{#if title || showCloseButton}
		<div class="px-6 py-4 border-b-2 border-primary flex justify-between items-center bg-surface-secondary">
			<div>
				{#if title}
					<h2 id="dialog-title" class="text-xl font-bold tracking-tight uppercase">{title}</h2>
				{/if}
				{#if description}
					<p id="dialog-description" class="text-sm mt-1 text-fg-secondary">{description}</p>
				{/if}
			</div>
			{#if showCloseButton}
				<div class="flex items-center gap-2">
					{#if closeOnEscape}
						<span class="text-xs text-content-tertiary font-mono hidden sm:inline-block">ESC</span>
					{/if}
					<Button variant="ghost" size="sm" onclick={handleClose} aria-label="Close dialog">✕</Button>
				</div>
			{/if}
		</div>
	{/if}

	<div class="p-6 overflow-y-auto">
		{@render children()}
	</div>

	{#if footer}
		<div class="px-6 py-4 border-t-2 border-primary bg-surface-tertiary flex justify-end gap-2">
			{@render footer()}
		</div>
	{/if}
</dialog>

<style>
	dialog {
		color: var(--text-primary);
		border-width: var(--border-width);
		border-style: solid;
		border-color: var(--border-primary);
	}
	/* override user agent defaults */
	dialog::backdrop {
		background: rgba(0, 0, 0, 0.5);
	}
</style>
