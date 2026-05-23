<script lang="ts">
	import { untrack } from 'svelte';
	import type { Snippet } from 'svelte';

	interface Props {
		children?: Snippet;
		minSize?: number;
		maxSize?: number;
		defaultSize?: number;
		size?: number; // controlled size
		collapsible?: boolean;
		collapsedSize?: number;
		collapsed?: boolean;
		side?: 'left' | 'right' | 'top' | 'bottom';
		onResize?: (newSize: number) => void;
		onResizeEnd?: (finalSize: number) => void;
		onPathChange?: (collapsed: boolean) => void;
		class?: string;
	}

	let {
		children,
		minSize = 200,
		maxSize = 800,
		defaultSize = 300,
		size = $bindable(undefined),
		collapsible = false,
		collapsedSize = 0,
		collapsed = $bindable(false),
		side = 'right', // handle is on the right side by default
		onResize,
		onResizeEnd,
		class: className = ''
	}: Props = $props();

	// svelte-ignore state_referenced_locally
	let currentSize = $state(size ?? defaultSize);
	
	$effect(() => {
		if (size !== undefined && currentSize !== size) {
			currentSize = size;
		}
	});

	let isDragging = $state(false);
	
	// internal states for smooth transition vs active drag
	let isTransitioning = $state(false);
	let startDragPos = 0;
	let startDragSize = 0;
	
	const isHorizontal = $derived(side === 'left' || side === 'right');
	const handleSize = 6;

	function getBoundedSize(s: number) {
		if (collapsible) {
			const collapseThreshold = minSize / 2;
			if (s < collapseThreshold) {
				return collapsedSize;
			}
		}
		return Math.max(minSize, Math.min(maxSize, s));
	}

	function onPointerDown(e: PointerEvent) {
		isDragging = true;
		isTransitioning = false;
		startDragPos = isHorizontal ? e.clientX : e.clientY;
		startDragSize = currentSize;
		document.body.style.cursor = isHorizontal ? 'ew-resize' : 'ns-resize';
		document.body.style.userSelect = 'none';

		window.addEventListener('pointermove', onPointerMove);
		window.addEventListener('pointerup', onPointerUp);
	}

	function onPointerMove(e: PointerEvent) {
		if (!isDragging) return;
		
		const currentPos = isHorizontal ? e.clientX : e.clientY;
		const delta = currentPos - startDragPos;
		
		let newSize = startDragSize;
		if (side === 'right' || side === 'bottom') {
			newSize += delta;
		} else {
			newSize -= delta;
		}

		currentSize = getBoundedSize(newSize);
		if (size !== undefined) size = currentSize;

		// update collapse state
		const isNowCollapsed = collapsible && currentSize <= collapsedSize;
		if (collapsed !== isNowCollapsed) {
			collapsed = isNowCollapsed;
		}

		if (onResize) onResize(currentSize);
	}

	function onPointerUp() {
		isDragging = false;
		isTransitioning = true;
		document.body.style.cursor = '';
		document.body.style.userSelect = '';
		
		// If size shouldn't be held halfway collapsed, snap it
		currentSize = getBoundedSize(currentSize);
		if (size !== undefined) size = currentSize;

		window.removeEventListener('pointermove', onPointerMove);
		window.removeEventListener('pointerup', onPointerUp);

		if (onResizeEnd) onResizeEnd(currentSize);
	}
	
	$effect(() => {
		// handle externally toggled collapsed state
		if (collapsed && currentSize > collapsedSize) {
			isTransitioning = true;
			untrack(() => {
				currentSize = collapsedSize;
				if (size !== undefined) size = currentSize;
				if (onResizeEnd) onResizeEnd(currentSize);
			});
		} else if (!collapsed && currentSize <= collapsedSize) {
			isTransitioning = true;
			untrack(() => {
				currentSize = Math.max(minSize, defaultSize);
				if (size !== undefined) size = currentSize;
				if (onResizeEnd) onResizeEnd(currentSize);
			});
		}
	});

	// Handle positioning of the grab divider
	const dividerClass = $derived(`absolute z-50 flex items-center justify-center transition-colors group
		${isHorizontal ? 'h-full cursor-ew-resize top-0' : 'w-full cursor-ns-resize left-0'}
		${side === 'right' ? '-right-1.5 w-3' : ''}
		${side === 'left' ? '-left-1.5 w-3' : ''}
		${side === 'bottom' ? '-bottom-1.5 h-3' : ''}
		${side === 'top' ? '-top-1.5 h-3' : ''}
	`);

	const innerDividerClass = $derived(`
		bg-border-subtle group-hover:bg-brand-primary/50 transition-colors duration-200
		${isDragging ? 'bg-brand-primary' : ''}
		${isHorizontal ? 'w-0.5 h-full' : 'h-0.5 w-full'}
	`);
</script>

<svelte:window 
	onpointerup={isDragging ? onPointerUp : undefined} 
	onpointermove={isDragging ? onPointerMove : undefined} 
/>

<div 
	class="relative shrink-0 box-border border-border-base bg-surface-base flex {className}"
	class:transition-all={!isDragging && isTransitioning}
	class:duration-200={!isDragging && isTransitioning}
	style:width={isHorizontal ? `${currentSize}px` : undefined}
	style:height={!isHorizontal ? `${currentSize}px` : undefined}
	style:border-right-width={side === 'right' ? '1px' : '0'}
	style:border-left-width={side === 'left' ? '1px' : '0'}
	style:border-bottom-width={side === 'bottom' ? '1px' : '0'}
	style:border-top-width={side === 'top' ? '1px' : '0'}
>
	<div class="h-full w-full overflow-hidden">
		{@render children?.()}
	</div>

	<!-- Handle -->
	<!-- svelte-ignore a11y_no_noninteractive_tabindex -->
	<!-- svelte-ignore a11y_interactive_supports_focus -->
	<div 
		role="separator" 
		aria-orientation={isHorizontal ? 'vertical' : 'horizontal'}
		class={dividerClass} 
		onpointerdown={onPointerDown}
		tabindex="0"
	>
		<div class={innerDividerClass}></div>
	</div>
</div>