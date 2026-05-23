<script lang="ts">
	interface Props {
		value: number; // 0 to 100
		size?: number; // width and height in px
		strokeWidth?: number;
		color?: string; // CSS color string or color name
		trackColor?: string; // CSS color string or color name
		label?: string; // Text to show in the center
		subLabel?: string; // Sub-text to show in the center
		class?: string;
	}

	let {
		value = 0,
		size = 80,
		strokeWidth = 8,
		color = 'var(--color-primary)',
		trackColor = 'var(--color-gray-200)',
		label,
		subLabel,
		class: className = ''
	}: Props = $props();

	// Ensure value stays between 0 and 100
	let normalizedValue = $derived(Math.max(0, Math.min(100, value)));
	
	let radius = $derived((size - strokeWidth) / 2);
	let circumference = $derived(2 * Math.PI * radius);
	let strokeDashoffset = $derived(circumference - (normalizedValue / 100) * circumference);
</script>

<div 
	class="relative inline-flex items-center justify-center {className}"
	style="width: {size}px; height: {size}px;"
	role="progressbar"
	aria-valuenow={normalizedValue}
	aria-valuemin="0"
	aria-valuemax="100"
>
	<svg 
		width={size} 
		height={size} 
		class="transform -rotate-90 select-none"
	>
		<!-- Track Circle -->
		<circle
			cx={size / 2}
			cy={size / 2}
			r={radius}
			fill="transparent"
			stroke={trackColor}
			stroke-width={strokeWidth}
			class="transition-all duration-fast"
		/>
		<!-- Progress Circle -->
		<circle
			cx={size / 2}
			cy={size / 2}
			r={radius}
			fill="transparent"
			stroke={color}
			stroke-width={strokeWidth}
			stroke-dasharray={circumference}
			stroke-dashoffset={strokeDashoffset}
			stroke-linecap="square"
			class="transition-all duration-base ease-brutal"
		/>
	</svg>

	<!-- Centered Labels -->
	<div class="absolute flex flex-col items-center justify-center text-center pointer-events-none px-2">
		{#if label}
			<span class="text-sm font-black font-mono leading-none text-fg-primary">{label}</span>
		{:else}
			<span class="text-sm font-black font-mono leading-none text-fg-primary">{Math.round(normalizedValue)}%</span>
		{/if}
		{#if subLabel}
			<span class="text-[9px] font-bold font-mono tracking-wider uppercase text-fg-tertiary mt-0.5 leading-none">{subLabel}</span>
		{/if}
	</div>
</div>
