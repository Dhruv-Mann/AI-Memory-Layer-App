<script lang="ts">
	import { untrack } from 'svelte';
	import type { Snippet } from 'svelte';
	import Button from '../primitives/Button.svelte';

	interface Props {
		value: string;
		placeholder?: string;
		loading?: boolean;
		debounceMs?: number;
		onSearch?: (value: string) => void;
		onClear?: () => void;
		class?: string;
	}

	let {
		value = $bindable(''),
		placeholder = 'Search...',
		loading = false,
		debounceMs = 150,
		onSearch,
		onClear,
		class: className = ''
	}: Props = $props();

	let timeoutId: ReturnType<typeof setTimeout> | undefined;
	
	// Create a local variable to hold immediate changes
	let localValue = $state(value);

	$effect(() => {
		// Sync external value changes down to local if they differ
		if (value !== undefined && value !== localValue) {
			localValue = value;
		}
	});

	function handleInput(e: Event) {
		const target = e.target as HTMLInputElement;
		const newValue = target.value;
		localValue = newValue;

		if (timeoutId) clearTimeout(timeoutId);
		timeoutId = setTimeout(() => {
			value = newValue; // Update external binding
			if (onSearch) onSearch(newValue);
		}, debounceMs);
	}

	function handleClear() {
		localValue = '';
		value = '';
		if (timeoutId) clearTimeout(timeoutId);
		if (onClear) onClear();
		if (onSearch) onSearch('');
	}

</script>

<div class="relative flex items-center {className}">
	<div class="absolute left-3 text-content-tertiary">
		<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="square" stroke-linejoin="miter">
			<circle cx="11" cy="11" r="8"></circle>
			<line x1="21" y1="21" x2="16.65" y2="16.65"></line>
		</svg>
	</div>
	
	<input
		type="text"
		{placeholder}
		value={localValue}
		oninput={handleInput}
		class="w-full h-10 pl-10 pr-10 bg-surface-primary border-2 border-border-base text-content-primary placeholder:text-content-tertiary focus:outline-none focus:border-brand-primary focus:ring-1 focus:ring-brand-primary shadow-sm transition-colors brutal-border"
		role="searchbox"
		aria-label="Search items"
	/>

	{#if loading}
		<div class="absolute right-3">
			<svg class="animate-spin h-4 w-4 text-brand-primary" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
				<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
				<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
			</svg>
		</div>
	{:else if localValue.length > 0}
		<div class="absolute right-2">
			<Button variant="ghost" size="sm" class="h-6 w-6 p-0 min-w-0 flex items-center justify-center rounded-sm" onclick={handleClear} aria-label="Clear search">
				<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
					<line x1="18" y1="6" x2="6" y2="18"></line>
					<line x1="6" y1="6" x2="18" y2="18"></line>
				</svg>
			</Button>
		</div>
	{/if}
</div>