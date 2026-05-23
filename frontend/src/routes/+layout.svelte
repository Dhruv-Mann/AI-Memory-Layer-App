<script lang="ts">
	import '../app.css';
	import favicon from '$lib/assets/favicon.svg';
	import { page } from '$app/stores';
	import { motionFade } from '$lib/utils/animations';
	import { initWindowTracker } from '$lib/stores/windowStore';
	import { initPerformanceMonitoring } from '$lib/utils/performance';

	let { children } = $props();

	$effect(() => {
		initPerformanceMonitoring();
		const cleanup = initWindowTracker();
		return () => {
			cleanup?.();
		};
	});
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

{#key $page.url.pathname}
	<div in:motionFade={{ duration: 300 }} class="h-full w-full">
		{@render children()}
	</div>
{/key}
