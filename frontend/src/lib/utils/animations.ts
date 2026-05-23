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
 * Automatically respects prefers-reduced-motion.
 */
export function motionFade(node: HTMLElement, params?: FadeParams): TransitionConfig {
	if (isReducedMotion()) return { duration: 0 };
	return fade(node, {
		duration: durationNormal,
		...params
	});
}

/**
 * Motion-safe Svelte slide transition wrapper.
 * Automatically respects prefers-reduced-motion.
 */
export function motionSlide(node: HTMLElement, params?: SlideParams): TransitionConfig {
	if (isReducedMotion()) return { duration: 0 };
	return slide(node, {
		duration: durationNormal,
		...params
	});
}

/**
 * Motion-safe Svelte fly transition wrapper.
 * Automatically respects prefers-reduced-motion.
 */
export function motionFly(node: HTMLElement, params?: FlyParams): TransitionConfig {
	if (isReducedMotion()) return { duration: 0 };
	return fly(node, {
		duration: durationNormal,
		...params
	});
}
