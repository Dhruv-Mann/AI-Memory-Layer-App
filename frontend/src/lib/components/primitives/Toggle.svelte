<script lang="ts">
	interface Props {
		checked?: boolean;
		disabled?: boolean;
		label?: string;
		class?: string;
		onchange?: (event: Event) => void;
	}

	let {
		checked = $bindable(false),
		disabled = false,
		label,
		class: className = '',
		onchange
	}: Props = $props();
</script>

<label class="inline-flex items-center gap-3 cursor-pointer {disabled ? 'opacity-50 cursor-not-allowed' : ''} {className}">
	<div class="relative flex items-center">
		<input
			type="checkbox"
			role="switch"
			bind:checked
			{disabled}
			{onchange}
			aria-checked={checked}
			class="peer sr-only"
		/>
		<!-- Toggle Track (Brutalist rectangle, not rounded) -->
		<div class="w-10 h-6 brutal-border bg-surface-tertiary peer-focus-visible:ring-2 peer-focus-visible:ring-brand-primary peer-checked:bg-success-base transition-colors duration-fast"></div>
		<!-- Toggle Thumb (Square block) -->
		<div class="absolute left-1 top-1 w-4 h-4 bg-fg-primary brutal-border translate-x-0 peer-checked:translate-x-4 transition-transform duration-fast ease-brutal"></div>
	</div>
	{#if label}
		<span class="text-sm font-medium tracking-tight text-fg-primary">{label}</span>
	{/if}
</label>
