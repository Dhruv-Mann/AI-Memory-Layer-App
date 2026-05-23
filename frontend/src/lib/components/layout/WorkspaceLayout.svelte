<script lang="ts">
	import type { Snippet } from 'svelte';
	import { layoutStore } from '../../stores/layoutStore';
	import ResizablePanel from './ResizablePanel.svelte';

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

	let storeParams = $derived($layoutStore);
</script>

<div class="w-full h-screen overflow-hidden flex flex-col bg-surface-base text-content-primary">
	<!-- Command Bar Region -->
	{#if storeParams.commandBar.visible && commandBar}
		<header class="shrink-0 border-b border-border-base bg-surface-base z-10 relative">
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
				{@render sidebar()}
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
				<main class="flex-1 overflow-hidden bg-surface-primary min-w-0 relative">
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