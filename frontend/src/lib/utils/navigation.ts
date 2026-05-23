export function handleEscape(action: () => void) {
	return (event: KeyboardEvent) => {
		if (event.key === 'Escape') {
			event.preventDefault();
			event.stopPropagation();
			action();
		}
	};
}

export function handleEnter(action: () => void) {
	return (event: KeyboardEvent) => {
		if (event.key === 'Enter') {
			event.preventDefault();
			action();
		}
	};
}

export function handleArrowNavigation(e: KeyboardEvent, elements: HTMLElement[], currentIdx: number, horizontal = false, wrap = true): number | null {
	let nextIdx = null;

	const backwardKey = horizontal ? 'ArrowLeft' : 'ArrowUp';
	const forwardKey = horizontal ? 'ArrowRight' : 'ArrowDown';

	if (e.key === backwardKey) {
		e.preventDefault();
		nextIdx = currentIdx - 1;
		if (nextIdx < 0) nextIdx = wrap ? elements.length - 1 : 0;
	} else if (e.key === forwardKey) {
		e.preventDefault();
		nextIdx = currentIdx + 1;
		if (nextIdx >= elements.length) nextIdx = wrap ? 0 : elements.length - 1;
	} else if (e.key === 'Home') {
		e.preventDefault();
		nextIdx = 0;
	} else if (e.key === 'End') {
		e.preventDefault();
		nextIdx = elements.length - 1;
	}

	if (nextIdx !== null && nextIdx !== currentIdx && elements[nextIdx]) {
		elements[nextIdx].focus();
		return nextIdx;
	}

	return null;
}

/**
 * Common action wrapper for keyboard-accessible Svelte components
 */
export function clickOnEnter(node: HTMLElement) {
	function handleKeyDown(e: KeyboardEvent) {
		if (e.key === 'Enter' || e.key === ' ') {
			e.preventDefault();
			node.click();
		}
	}
	
	node.addEventListener('keydown', handleKeyDown);
	
	return {
		destroy() {
			node.removeEventListener('keydown', handleKeyDown);
		}
	};
}