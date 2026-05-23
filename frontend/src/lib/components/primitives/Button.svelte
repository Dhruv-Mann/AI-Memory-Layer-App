<script lang="ts">
	import type { Snippet } from 'svelte';
	import type { ComponentSize } from '$lib/types/tokens';
	import KeyboardHint from './KeyboardHint.svelte';

	type Variant = 'primary' | 'secondary' | 'ghost' | 'danger' | 'icon';
	type ButtonType = 'button' | 'submit' | 'reset';

	interface Props {
		children?: Snippet;
		variant?: Variant;
		size?: ComponentSize; // sm | md | lg
		disabled?: boolean;
		loading?: boolean;
		icon?: Snippet;
		iconPosition?: 'left' | 'right';
		fullWidth?: boolean;
		type?: ButtonType;
		class?: string;
		keyboardHint?: string[];
		onclick?: (event: MouseEvent) => void;
		'aria-label'?: string;
		'aria-expanded'?: boolean;
		'aria-controls'?: string;
	}

	let {
		children,
		variant = 'primary',
		size = 'md',
		disabled = false,
		loading = false,
		icon,
		iconPosition = 'left',
		fullWidth = false,
		type = 'button',
		class: className = '',
		keyboardHint,
		onclick,
		'aria-label': ariaLabel,
		'aria-expanded': ariaExpanded,
		'aria-controls': ariaControls
	}: Props = $props();

	// Neo-Brutalist base classes: bold borders, tight fonts, zero rounding on default
	const baseClasses =
		'inline-flex items-center justify-center font-bold tracking-tight uppercase transition-all duration-fast ease-brutal focus:outline-none focus:ring-2 focus:ring-brand-primary focus:ring-offset-2';

	// Sizes
	const sizeClasses = {
		sm: 'px-3 py-1.5 text-xs',
		md: 'px-4 py-2 text-sm',
		lg: 'px-6 py-3 text-base'
	};

	// Variants
	const variantClasses = {
		primary:
			'bg-brand-primary text-white brutal-border brutal-shadow-sm hover:brutal-shadow-md hover:-translate-y-0.5 active:translate-y-px active:brutal-shadow-sm',
		secondary:
			'bg-surface-secondary text-fg-primary brutal-border brutal-shadow-sm hover:brutal-shadow-md hover:-translate-y-0.5 active:translate-y-px active:brutal-shadow-sm',
		danger:
			'bg-error-DEFAULT text-white brutal-border brutal-shadow-sm hover:brutal-shadow-md hover:-translate-y-0.5 active:translate-y-px active:brutal-shadow-sm',
		ghost:
			'bg-transparent text-fg-primary border-2 border-transparent hover:bg-surface-secondary hover:border-brutal-primary',
		icon: 'p-2 bg-surface-primary text-fg-primary brutal-border brutal-shadow-sm hover:bg-surface-secondary hover:brutal-shadow-md hover:-translate-y-0.5 active:translate-y-px aspect-square'
	};

	let computedClasses = $derived(
		[
			baseClasses,
			sizeClasses[size],
			variantClasses[variant],
			size === 'sm' || variant === 'icon' ? 'touch-target-extend' : '',
			fullWidth ? 'w-full' : '',
			disabled || loading ? 'opacity-50 cursor-not-allowed pointer-events-none' : '',
			className
		]
			.filter(Boolean)
			.join(' ')
	);

	function handleKeydown(event: KeyboardEvent) {
		if (disabled || loading) return;
		// A11y: Space and Enter trigger buttons
		if (event.key === 'Enter' || event.key === ' ') {
			event.preventDefault();
			onclick?.(new MouseEvent('click'));
		}
	}
</script>

<button
	{type}
	{disabled}
	aria-disabled={disabled || loading}
	aria-busy={loading}
	aria-label={ariaLabel}
	aria-expanded={ariaExpanded}
	aria-controls={ariaControls}
	class={computedClasses}
	{onclick}
	onkeydown={handleKeydown}
>
	{#if loading}
		<span class="mr-2 animate-spin">⧗</span>
	{/if}

	{#if icon && iconPosition === 'left' && !loading}
		<span class="mr-2 flex items-center justify-center">
			{@render icon()}
		</span>
	{/if}

	{#if children && variant !== 'icon'}
		<span>{@render children()}</span>
	{/if}

	{#if icon && iconPosition === 'right' && !loading}
		<span class="ml-2 flex items-center justify-center">
			{@render icon()}
		</span>
	{/if}

    {#if variant === 'icon' && icon && !loading}
        <span class="flex items-center justify-center">
            {@render icon()}
        </span>
    {/if}

	{#if keyboardHint}
		<KeyboardHint keys={keyboardHint} class="ml-2" />
	{/if}
</button>
