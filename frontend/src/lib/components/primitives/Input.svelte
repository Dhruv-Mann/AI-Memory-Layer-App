<script lang="ts">
	import type { Snippet } from 'svelte';
	import type { ComponentSize } from '$lib/types/tokens';

	interface Props {
		type?: 'text' | 'email' | 'password' | 'search' | 'url';
		size?: ComponentSize; // sm | md | lg
		disabled?: boolean;
		error?: boolean;
		helperText?: string;
		icon?: Snippet;
		iconPosition?: 'left' | 'right';
		placeholder?: string;
		value?: string;
		class?: string;
		oninput?: (event: Event) => void;
	}

	let {
		type = 'text',
		size = 'md',
		disabled = false,
		error = false,
		helperText = '',
		icon,
		iconPosition = 'left',
		placeholder = '',
		value = $bindable(''),
		class: className = '',
		oninput
	}: Props = $props();

	// Input specific Neo-brutalist styles: deep inset shadows, sharp borders.
	const baseInputClasses =
		'block w-full brutal-border bg-surface-primary text-fg-primary focus:outline-none focus:ring-2 transition-all duration-fast placeholder:text-gray-400';

	const sizeClasses = {
		sm: 'px-2 py-1 text-sm',
		md: 'px-3 py-2 text-base',
		lg: 'px-4 py-3 text-lg'
	};

	let computedInputClasses = $derived(
		[
			baseInputClasses,
			sizeClasses[size],
			error
				? 'border-error-DEFAULT ring-error-light focus:ring-error-DEFAULT'
				: 'focus:ring-brand-primary',
			disabled ? 'opacity-50 cursor-not-allowed bg-surface-tertiary' : 'shadow-inner',
			icon && iconPosition === 'left' ? (size === 'sm' ? 'pl-8' : size === 'lg' ? 'pl-12' : 'pl-10') : '',
			icon && iconPosition === 'right' ? (size === 'sm' ? 'pr-8' : size === 'lg' ? 'pr-12' : 'pr-10') : '',
			className
		]
			.filter(Boolean)
			.join(' ')
	);
</script>

<div class="relative w-full flex flex-col gap-1 {className}">
	<div class="relative w-full">
		{#if icon && iconPosition === 'left'}
			<div class="absolute left-3 top-1/2 -translate-y-1/2 flex items-center justify-center text-fg-secondary pointer-events-none">
				{@render icon()}
			</div>
		{/if}

		<input
			{type}
			{disabled}
			{placeholder}
			bind:value
			{oninput}
			aria-invalid={error}
			aria-describedby={helperText ? "helper-text" : undefined}
			class={computedInputClasses}
		/>

		{#if icon && iconPosition === 'right'}
			<div class="absolute right-3 top-1/2 -translate-y-1/2 flex items-center justify-center text-fg-secondary pointer-events-none">
				{@render icon()}
			</div>
		{/if}
	</div>

	{#if helperText}
		<span id="helper-text" class="text-xs font-medium {error ? 'text-error-DEFAULT' : 'text-fg-secondary'}">
			{helperText}
		</span>
	{/if}
</div>
