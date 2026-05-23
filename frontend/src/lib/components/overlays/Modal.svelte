<script lang="ts">
	import type { Snippet } from 'svelte';
	import Button from '../primitives/Button.svelte';

	interface Props {
		open?: boolean;
		title?: string;
		children: Snippet;
		footer?: Snippet;
		onclose?: () => void;
	}

	let { open = $bindable(false), title, children, footer, onclose }: Props = $props();

	let dialog: HTMLDialogElement;

	// Watch the open prop to natively open/close the HTML dialog element
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

	// Because clicking the backdrop of a <dialog> registers as clicking the dialog itself,
	// we check the bounding box. If the click is outside the bounds of the dialog content, it's a backdrop click.
	function handleBackdropClick(e: MouseEvent) {
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
</script>

<!-- svelte-ignore a11y_click_events_have_key_events -->
<!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
<!-- Native dialog handles Esc key automatically -->
<dialog
	bind:this={dialog}
	onclose={handleClose}
	onclick={handleBackdropClick}
	class="brutal-card p-0 m-auto max-w-lg w-[calc(100%-2rem)] backdrop:backdrop-blur-sm backdrop:bg-black/50 open:animate-in open:fade-in open:zoom-in-95 duration-fast"
>
	<!-- Header -->
	{#if title}
		<div class="px-6 py-4 border-b-2 border-primary flex justify-between items-center bg-surface-secondary">
			<h2 class="text-xl font-bold tracking-tight uppercase">{title}</h2>
			<Button variant="ghost" size="sm" onclick={handleClose} aria-label="Close modal">✕</Button>
		</div>
	{/if}

	<!-- Body -->
	<div class="p-6">
		{@render children()}
	</div>

	<!-- Footer / Actions -->
	{#if footer}
		<div class="px-6 py-4 border-t-2 border-primary bg-surface-tertiary flex justify-end gap-2">
			{@render footer()}
		</div>
	{/if}
</dialog>

<style>
	/* Remove default dialog border styles as we use .brutal-card classes */
	dialog {
		color: var(--text-primary);
		border-width: var(--border-width);
		border-style: solid;
		border-color: var(--border-primary);
	}
</style>
