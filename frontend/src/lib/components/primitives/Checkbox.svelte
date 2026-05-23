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

<label class="inline-flex items-center gap-2 cursor-pointer {disabled ? 'opacity-50 cursor-not-allowed' : ''} {className}">
	<div class="relative flex items-center">
		<input
			type="checkbox"
			bind:checked
			{disabled}
			{onchange}
			class="peer sr-only"
		/>
		<!-- Fake Box -->
		<div class="w-5 h-5 brutal-border bg-surface-primary peer-focus-visible:ring-2 peer-focus-visible:ring-brand-primary peer-focus-visible:ring-offset-1 peer-checked:bg-brand-primary peer-checked:text-white transition-colors">
			<!-- Checkmark SVG that scales in when checked -->
			<svg 
				class="absolute top-0.5 left-0.5 w-4 h-4 pointer-events-none scale-0 peer-checked:scale-100 transition-transform brutal-ease stroke-current text-white" 
				viewBox="0 0 24 24" 
				fill="none" 
				stroke-width="4" 
				stroke-linecap="square" 
				stroke-linejoin="miter">
				<polyline points="20 6 9 17 4 12"></polyline>
			</svg>
		</div>
	</div>
	{#if label}
		<span class="text-sm font-medium tracking-tight text-fg-primary">{label}</span>
	{/if}
</label>
