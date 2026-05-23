<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		type?: 'outer' | 'inner';
		padding?: 'none' | 'sm' | 'md' | 'lg';
		class?: string;
		children: Snippet;
	}

	let {
		type = 'inner',
		padding = 'md',
		class: className = '',
		children
	}: Props = $props();

	const paddingMap = {
		none: 'p-0',
		sm: 'p-2',
		md: 'p-4',
		lg: 'p-6'
	};
	
	const typeClasses = type === 'outer' 
		? 'brutal-border bg-surface-secondary' 
		: 'border-2 border-primary bg-surface-primary';
</script>

<div class="{typeClasses} {paddingMap[padding]} {className}">
	{@render children()}
</div>
