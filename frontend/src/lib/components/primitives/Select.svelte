<script lang="ts">
	interface Option {
		label: string;
		value: string | number;
	}

	interface Props {
		options: Option[];
		value?: string | number;
		placeholder?: string;
		disabled?: boolean;
		class?: string;
		onchange?: (event: Event) => void;
	}

	let {
		options,
		value = $bindable(''),
		placeholder = 'Select an option...',
		disabled = false,
		class: className = '',
		onchange
	}: Props = $props();

	// Neo-brutalist select: hard borders, custom chevron
	const baseClasses =
		'block w-full brutal-border bg-surface-primary text-fg-primary focus:outline-none focus:ring-2 focus:ring-brand-primary transition-all duration-fast appearance-none px-3 py-2 cursor-pointer shadow-inner';
	
	let computedClasses = $derived(
		[
			baseClasses,
			disabled ? 'opacity-50 cursor-not-allowed bg-surface-tertiary' : 'hover:bg-surface-secondary',
			className
		].filter(Boolean).join(' ')
	);
</script>

<div class="relative w-full">
	<select
		{disabled}
		bind:value
		{onchange}
		class={computedClasses}
	>
		{#if placeholder}
			<option value="" disabled selected hidden>{placeholder}</option>
		{/if}
		{#each options as option}
			<option value={option.value}>{option.label}</option>
		{/each}
	</select>

	<!-- Custom Chevron for Brutalist look -->
	<div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-3 text-fg-primary">
		<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="square" stroke-linejoin="miter">
			<polyline points="6 9 12 15 18 9"></polyline>
		</svg>
	</div>
</div>
