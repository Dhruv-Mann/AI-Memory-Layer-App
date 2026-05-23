<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		primary?: Snippet;
		secondary?: Snippet;
		orientation?: 'horizontal' | 'vertical';
		ratio?: number; // 0 to 1
		minRatio?: number;
		maxRatio?: number;
		onRatioChange?: (newRatio: number) => void;
		onResizeEnd?: (finalRatio: number) => void;
		class?: string;
	}

	let {
		primary,
		secondary,
		orientation = 'horizontal',
		ratio = $bindable(0.5),
		minRatio = 0.1,
		maxRatio = 0.9,
		onRatioChange,
		onResizeEnd,
		class: className = ''
	}: Props = $props();

	let container: HTMLElement | undefined;
	let isDragging = $state(false);

	function getBoundedRatio(r: number) {
		return Math.max(minRatio, Math.min(maxRatio, r));
	}

	function onPointerDown(e: PointerEvent) {
		isDragging = true;
		document.body.style.cursor = orientation === 'horizontal' ? 'ew-resize' : 'ns-resize';
		document.body.style.userSelect = 'none';

		window.addEventListener('pointermove', onPointerMove);
		window.addEventListener('pointerup', onPointerUp);
	}

	function onPointerMove(e: PointerEvent) {
		if (!isDragging || !container) return;

		const rect = container.getBoundingClientRect();
		// Compute the ratio directly based on container bounds
		let newRatio = ratio;

		if (orientation === 'horizontal') {
			const deltaX = e.clientX - rect.left;
			newRatio = getBoundedRatio(deltaX / rect.width);
		} else {
			const deltaY = e.clientY - rect.top;
			newRatio = getBoundedRatio(deltaY / rect.height);
		}

		ratio = newRatio;
		if (onRatioChange) onRatioChange(ratio);
	}

	function onPointerUp() {
		isDragging = false;
		document.body.style.cursor = '';
		document.body.style.userSelect = '';

		window.removeEventListener('pointermove', onPointerMove);
		window.removeEventListener('pointerup', onPointerUp);

		if (onResizeEnd) onResizeEnd(ratio);
	}

	const dividerOuterClass = $derived(`
		flex items-center justify-center transition-colors group z-10 
		${orientation === 'horizontal' ? 'w-3 h-full -mx-1.5 cursor-ew-resize' : 'h-3 w-full -my-1.5 cursor-ns-resize'}
	`);

	const dividerInnerClass = $derived(`
		bg-border-subtle group-hover:bg-brand-primary/50 transition-colors duration-200
		${isDragging ? 'bg-brand-primary' : ''}
		${orientation === 'horizontal' ? 'w-0.5 h-full' : 'h-0.5 w-full'}
	`);
</script>

<svelte:window 
	onpointerup={isDragging ? onPointerUp : undefined} 
	onpointermove={isDragging ? onPointerMove : undefined} 
/>

<div
	bind:this={container}
	class="flex w-full h-full overflow-hidden {orientation === 'horizontal' ? 'flex-row' : 'flex-col'} {className}"
>
	<!-- Primary Area -->
	<div 
		class="overflow-hidden shrink-0 flex items-stretch border-border-base bg-surface-base box-border"
		style:flex-basis="{ratio * 100}%"
		style:border-right-width={orientation === 'horizontal' ? '1px' : '0'}
		style:border-bottom-width={orientation === 'vertical' ? '1px' : '0'}
	>
		{@render primary?.()}
	</div>

	<!-- Handle -->
	<!-- svelte-ignore a11y_no_noninteractive_tabindex -->
	<!-- svelte-ignore a11y_interactive_supports_focus -->
	<div
		role="separator"
		aria-orientation={orientation}
		class={dividerOuterClass}
		onpointerdown={onPointerDown}
		tabindex="0"
	>
		<div class={dividerInnerClass}></div>
	</div>

	<!-- Secondary Area -->
	<div 
		class="flex-1 overflow-hidden flex items-stretch bg-surface-base"
	>
		{@render secondary?.()}
	</div>
</div>