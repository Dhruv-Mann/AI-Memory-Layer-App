<script lang="ts">
	import WorkspaceLayout from '$lib/components/layout/WorkspaceLayout.svelte';
	import RecallDashboard from '$lib/components/features/RecallDashboard.svelte';
	import Button from '$lib/components/primitives/Button.svelte';

	// Mock Navigation State
	let activeTab = $state('dashboard');

	// Mock Command Bar Search input
	let searchVal = $state('');
</script>

<WorkspaceLayout>
	{#snippet sidebar()}
		<div class="h-full flex flex-col justify-between p-6 bg-surface-primary border-r-4 border-border-base font-mono">
			<div class="flex flex-col gap-6">
				<!-- Brand Header -->
				<div class="flex items-center gap-2 border-b-2 border-border-base pb-4">
					<div class="h-8 w-8 bg-brand-primary brutal-border flex items-center justify-center font-black text-surface-primary">
						M
					</div>
					<span class="font-black text-sm tracking-tight uppercase">Memory Layer</span>
				</div>

				<!-- Navigation Links -->
				<nav class="flex flex-col gap-2" id="sidebar-content" tabindex="-1">
					<button 
						onclick={() => activeTab = 'dashboard'}
						class="w-full text-left px-3 py-2 text-xs font-black uppercase border-2 transition-all {activeTab === 'dashboard' ? 'border-border-base bg-brand-primary text-surface-primary shadow-[2px_2px_0px_rgba(0,0,0,1)]' : 'border-transparent text-content-secondary hover:border-border-subtle hover:bg-surface-secondary'}"
					>
						📊 Recall Dashboard
					</button>
					<button 
						onclick={() => activeTab = 'review'}
						class="w-full text-left px-3 py-2 text-xs font-black uppercase border-2 transition-all {activeTab === 'review' ? 'border-border-base bg-brand-primary text-surface-primary shadow-[2px_2px_0px_rgba(0,0,0,1)]' : 'border-transparent text-content-secondary hover:border-border-subtle hover:bg-surface-secondary'}"
					>
						🧠 Review Session
					</button>
					<button 
						onclick={() => activeTab = 'memories'}
						class="w-full text-left px-3 py-2 text-xs font-black uppercase border-2 transition-all {activeTab === 'memories' ? 'border-border-base bg-brand-primary text-surface-primary shadow-[2px_2px_0px_rgba(0,0,0,1)]' : 'border-transparent text-content-secondary hover:border-border-subtle hover:bg-surface-secondary'}"
					>
						📚 Memory Chunks
					</button>
				</nav>
			</div>

			<!-- User Profile Footer -->
			<div class="border-t-2 border-border-subtle pt-4 flex items-center gap-3">
				<div class="h-8 w-8 rounded-full bg-brand-accent brutal-border text-center font-bold leading-7 text-xs text-surface-primary">
					DM
				</div>
				<div class="flex flex-col">
					<span class="text-xs font-black">Dhruv Mann</span>
					<span class="text-[10px] text-content-tertiary font-bold">Free Tier</span>
				</div>
			</div>
		</div>
	{/snippet}

	{#snippet commandBar()}
		<div class="flex items-center justify-between px-6 py-3 bg-surface-primary">
			<div class="flex items-center gap-4 w-1/2">
				<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="square"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
				<input 
					type="text" 
					placeholder="Search memory graph or commands (Ctrl + K)..." 
					bind:value={searchVal}
					class="w-full bg-transparent font-mono text-xs font-bold outline-none text-content-primary placeholder-content-tertiary"
				/>
			</div>
			<div class="flex items-center gap-2">
				<span class="font-mono text-[10px] font-black text-content-tertiary bg-surface-secondary px-2 py-0.5 brutal-border">
					Ctrl + K
				</span>
			</div>
		</div>
	{/snippet}

	{#snippet mainContent()}
		<main id="main-content" tabindex="-1" class="h-full overflow-hidden outline-none">
			{#if activeTab === 'dashboard'}
				<RecallDashboard topicsDue={12} currentStreak={5} />
			{:else if activeTab === 'review'}
				<div class="p-12 flex flex-col gap-6 font-mono">
					<h2 class="text-3xl font-black uppercase">Review Session</h2>
					<p class="text-content-secondary max-w-lg leading-relaxed">
						Start a spaced repetition memory card review. The system chooses cards based on computed exponential decay curves.
					</p>
					<Button variant="primary" class="w-fit px-6">Launch Active Review</Button>
				</div>
			{:else}
				<div class="p-12 flex flex-col gap-6 font-mono">
					<h2 class="text-3xl font-black uppercase">Memory Chunks</h2>
					<p class="text-content-secondary max-w-lg leading-relaxed">
						View and query raw text blocks, context captures, references, and semantic associations saved in your graph database.
					</p>
					<Button variant="secondary" class="w-fit px-6">Explore Knowledge Base</Button>
				</div>
			{/if}
		</main>
	{/snippet}
</WorkspaceLayout>
