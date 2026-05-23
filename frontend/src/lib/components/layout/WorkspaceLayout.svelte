<script lang="ts">
	import type { Snippet } from 'svelte';
	import { layoutStore } from '../../stores/layoutStore';
	import ResizablePanel from './ResizablePanel.svelte';
	import SkipLink from '../primitives/SkipLink.svelte';

	interface Props {
		sidebar?: Snippet;
		mainContent?: Snippet;
		auxiliaryPanel?: Snippet;
		bottomPanel?: Snippet;
		commandBar?: Snippet;
	}

	let {
		sidebar,
		mainContent,
		auxiliaryPanel,
		bottomPanel,
		commandBar
	}: Props = $props();

	import { browser } from '$app/environment';

	let storeParams = $derived($layoutStore);
	let lastWidth = browser ? window.innerWidth : 1920;

	$effect(() => {
		if (!browser) return;

		const handleResize = () => {
			const currentWidth = window.innerWidth;
			if (currentWidth < 1280 && lastWidth >= 1280) {
				if (storeParams.auxiliaryPanel.visible && !storeParams.auxiliaryPanel.collapsed) {
					layoutStore.updatePanel('auxiliaryPanel', { collapsed: true });
				}
			}
			lastWidth = currentWidth;
		};

		window.addEventListener('resize', handleResize);
		handleResize();

		return () => {
			window.removeEventListener('resize', handleResize);
		};
	});
</script>

<div class="w-full h-screen overflow-hidden flex flex-col bg-surface-base text-content-primary 3xl:max-w-[1920px] 3xl:h-[calc(100vh-4rem)] 3xl:my-8 3xl:mx-auto 3xl:brutal-border 3xl:shadow-lg">
	<!-- Accessibility Skip Links -->
	<SkipLink targetId="main-content" label="Skip to main content" />
	{#if storeParams.sidebar.visible && sidebar}
		<SkipLink targetId="sidebar-content" label="Skip to navigation" />
	{/if}
	{#if storeParams.commandBar.visible && commandBar}
		<SkipLink targetId="command-bar" label="Skip to command bar" />
	{/if}

	<!-- Command Bar Region -->
	{#if storeParams.commandBar.visible && commandBar}
		<header id="command-bar" tabindex="-1" class="shrink-0 border-b border-border-base bg-surface-base z-10 relative outline-none">
			{@render commandBar()}
		</header>
	{/if}

	<div class="flex-1 flex overflow-hidden min-h-0 relative">
		<!-- Main Sidebar -->
		{#if storeParams.sidebar.visible && sidebar}
			<ResizablePanel
				side="right"
				size={storeParams.sidebar.size}
				minSize={storeParams.sidebar.minSize}
				maxSize={storeParams.sidebar.maxSize}
				collapsible
				collapsed={storeParams.sidebar.collapsed}
				onResizeEnd={(size) => layoutStore.updatePanel('sidebar', { size })}
				class="z-10 relative"
			>
				<div id="sidebar-content" tabindex="-1" class="h-full w-full outline-none">
					{@render sidebar()}
				</div>
			</ResizablePanel>
		{/if}

		<!-- Center Area (Main + Auxiliary Left/Right + Bottom) -->
		<div class="flex-1 flex flex-col min-w-0 overflow-hidden relative">
			
			<div class="flex-1 flex overflow-hidden min-h-0 relative">
				<!-- Docked Left Auxiliary Panel -->
				{#if storeParams.auxiliaryPanel.visible && storeParams.auxiliaryPanel.dock === 'left' && auxiliaryPanel}
					<ResizablePanel
						side="right"
						size={storeParams.auxiliaryPanel.size}
						minSize={storeParams.auxiliaryPanel.minSize}
						maxSize={storeParams.auxiliaryPanel.maxSize}
						collapsible
						collapsed={storeParams.auxiliaryPanel.collapsed}
						onResizeEnd={(size) => layoutStore.updatePanel('auxiliaryPanel', { size })}
						class="z-[5] relative border-l border-border-base"
					>
						{@render auxiliaryPanel()}
					</ResizablePanel>
				{/if}

				<!-- Main Content Viewport -->
				<main id="main-content" tabindex="-1" class="flex-1 overflow-hidden bg-surface-primary min-w-0 relative outline-none">
					{#if mainContent}
						{@render mainContent()}
					{/if}

					<!-- Floating Auxiliary Panel (Overlays main content) -->
					{#if storeParams.auxiliaryPanel.visible && storeParams.auxiliaryPanel.dock === 'floating' && auxiliaryPanel}
						<div class="absolute right-4 top-4 bottom-4 shadow-xl border border-border-base rounded-md z-20 bg-surface-base"
							 style:width="{storeParams.auxiliaryPanel.size}px"
						>
							{@render auxiliaryPanel()}
						</div>
					{/if}
				</main>

				<!-- Docked Right Auxiliary Panel -->
				{#if storeParams.auxiliaryPanel.visible && storeParams.auxiliaryPanel.dock === 'right' && auxiliaryPanel}
					<ResizablePanel
						side="left"
						size={storeParams.auxiliaryPanel.size}
						minSize={storeParams.auxiliaryPanel.minSize}
						maxSize={storeParams.auxiliaryPanel.maxSize}
						collapsible
						collapsed={storeParams.auxiliaryPanel.collapsed}
						onResizeEnd={(size) => layoutStore.updatePanel('auxiliaryPanel', { size })}
						class="z-[5] relative border-l border-border-base"
					>
						{@render auxiliaryPanel()}
					</ResizablePanel>
				{/if}
			</div>

			<!-- Bottom Panel -->
			{#if storeParams.bottomPanel.visible && bottomPanel}
				<ResizablePanel
					side="top"
					size={storeParams.bottomPanel.size}
					minSize={storeParams.bottomPanel.minSize}
					maxSize={storeParams.bottomPanel.maxSize}
					collapsible
					collapsed={storeParams.bottomPanel.collapsed}
					onResizeEnd={(size) => layoutStore.updatePanel('bottomPanel', { size })}
					class="z-10 relative w-full shrink-0"
				>
					{@render bottomPanel()}
				</ResizablePanel>
			{/if}
		</div>
	</div>
</div>