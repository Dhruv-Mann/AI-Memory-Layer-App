import { readable } from 'svelte/store';
import { browser } from '$app/environment';
import { fade, slide, fly } from 'svelte/transition';
import type { FadeParams, SlideParams, FlyParams, TransitionConfig } from 'svelte/transition';

// Task 21.1 Duration Constants
export const durationInstant = 0;
export const durationFast = 100;
export const durationNormal = 200;
export const durationSlow = 300;

// Task 21.1 Easing Constants
export const easeIn = 'cubic-bezier(0.4, 0, 1, 1)';
export const easeOut = 'cubic-bezier(0, 0, 0.2, 1)';
export const easeInOut = 'cubic-bezier(0.4, 0, 0.2, 1)';
export const easeBrutal = 'cubic-bezier(0.2, 1, 0.2, 1)';

/**
 * Readable store detecting user's OS preference for reduced motion.
 */
export const prefersReducedMotion = readable(false, (set) => {
	if (!browser) return;
	const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
	set(mediaQuery.matches);

	const listener = (event: MediaQueryListEvent) => {
		set(event.matches);
	};

	mediaQuery.addEventListener('change', listener);
	return () => {
		mediaQuery.removeEventListener('change', listener);
	};
});

// Helper to check current state synchronously
function isReducedMotion(): boolean {
	if (!browser) return false;
	return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

/**
 * Motion-safe Svelte fade transition wrapper.
 * Automatically respects prefers-reduced-motion and applies GPU will-change styles.
 */
export function motionFade(node: HTMLElement, params?: FadeParams): TransitionConfig {
	if (isReducedMotion()) return { duration: 0 };
	const config = fade(node, {
		duration: durationNormal,
		...params
	});
	return {
		...config,
		css: (t, u) => {
			const originalCss = config.css ? config.css(t, u) : '';
			return `${originalCss} will-change: opacity;`;
		}
	};
}

/**
 * Motion-safe Svelte slide transition wrapper.
 * Automatically respects prefers-reduced-motion and applies GPU will-change styles.
 */
export function motionSlide(node: HTMLElement, params?: SlideParams): TransitionConfig {
	if (isReducedMotion()) return { duration: 0 };
	const config = slide(node, {
		duration: durationNormal,
		...params
	});
	return {
		...config,
		css: (t, u) => {
			const originalCss = config.css ? config.css(t, u) : '';
			return `${originalCss} will-change: transform, opacity;`;
		}
	};
}

/**
 * Motion-safe Svelte fly transition wrapper.
 * Automatically respects prefers-reduced-motion and applies GPU will-change styles.
 */
export function motionFly(node: HTMLElement, params?: FlyParams): TransitionConfig {
	if (isReducedMotion()) return { duration: 0 };
	const config = fly(node, {
		duration: durationNormal,
		...params
	});
	return {
		...config,
		css: (t, u) => {
			const originalCss = config.css ? config.css(t, u) : '';
			return `${originalCss} will-change: transform, opacity;`;
		}
	};
}

/**
 * Reusable Svelte Action that temporarily applies will-change styling during
 * active animation or transition cycles and cleans it up once completed.
 */
export function gpuAccelerated(node: HTMLElement) {
	const handleStart = () => {
		node.style.willChange = 'transform, opacity';
	};
	const handleEnd = () => {
		node.style.willChange = '';
	};

	node.addEventListener('animationstart', handleStart);
	node.addEventListener('animationend', handleEnd);
	node.addEventListener('transitionstart', handleStart);
	node.addEventListener('transitionend', handleEnd);

	return {
		destroy() {
			node.removeEventListener('animationstart', handleStart);
			node.removeEventListener('animationend', handleEnd);
			node.removeEventListener('transitionstart', handleStart);
			node.removeEventListener('transitionend', handleEnd);
		}
	};
}
