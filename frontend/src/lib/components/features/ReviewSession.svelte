<script lang="ts">
	import ReviewCard from './ReviewCard.svelte';
	import Button from '../primitives/Button.svelte';

	interface ReviewItem {
		id: string;
		topic: string;
		content: string;
		source?: string;
		context?: string[];
	}

	interface SpacedRepetitionSessionProps {
		items: ReviewItem[];
		onComplete: (results: Record<string, string>) => void;
	}

	let { items = [], onComplete }: SpacedRepetitionSessionProps = $props();

	let currentIndex = $state(0);
	let sessionActive = $state(true);
	let startTime = $state(Date.now());
	let timeSpent = $state(0); // in minutes
	
	let results = $state<Record<string, 'forgot' | 'hard' | 'good' | 'easy'>>({});
	
	let currentItem = $derived(items[currentIndex]);
	let progressPercent = $derived(items.length > 0 ? (currentIndex / items.length) * 100 : 0);
	let weakTopics = $derived(
		items.filter(item => results[item.id] === 'forgot' || results[item.id] === 'hard')
	);

	function handleAssess(rating: 'forgot' | 'hard' | 'good' | 'easy') {
		if (!currentItem) return;
		
		results[currentItem.id] = rating;

		if (currentIndex < items.length - 1) {
			// Advance to next card
			currentIndex++;
		} else {
			// Finish session
			timeSpent = Math.max(1, Math.round((Date.now() - startTime) / 60000));
			sessionActive = false;
		}
	}

	function finish() {
		onComplete(results);
	}
</script>

<div class="flex flex-col h-full w-full max-w-4xl mx-auto p-4 md:p-8">
	{#if items.length === 0}
		<div class="flex-1 flex flex-col items-center justify-center text-center p-12 bg-surface-primary brutal-border">
			<div class="text-4xl mb-4">📭</div>
			<h3 class="text-xl font-black mb-2">No reviews scheduled</h3>
			<p class="text-sm font-mono text-content-secondary max-w-sm mb-6">Your memory queues are fully cleared for today. Take a break or explore new concepts.</p>
			<Button variant="primary" onclick={() => onComplete({})}>Return to Dashboard</Button>
		</div>
	{:else if sessionActive}
		<!-- Session Header / Progress -->
		<div class="mb-6 md:mb-10">
			<div class="flex justify-between items-center text-xs font-mono font-bold mb-3 uppercase tracking-wider text-content-secondary">
				<span>Active Review Session</span>
				<span>{currentIndex + 1} / {items.length} Remaining</span>
			</div>
			<!-- Progress Bar -->
			<div class="h-4 w-full bg-surface-secondary brutal-border overflow-hidden">
				<div 
					class="h-full bg-brand-primary transition-all duration-300 ease-out border-r-4 border-black" 
					style="width: {progressPercent}%"
				></div>
			</div>
		</div>

		<!-- Review Card Area -->
		<div class="flex-1 overflow-hidden pb-4">
			{#key currentItem.id}
				<ReviewCard 
					topic={currentItem.topic}
					content={currentItem.content}
					source={currentItem.source}
					context={currentItem.context}
					onAssess={handleAssess}
				/>
			{/key}
		</div>
		
	{:else}
		<!-- Post-Session Analytics & Recovery Suggestions -->
		<div class="brutal-border bg-surface-primary w-full animate-slide-up flex flex-col overflow-hidden text-center md:text-left">
			<div class="p-8 md:p-12 text-center border-b-4 border-border-base bg-[#ffe1e8]">
				<div class="text-6xl mb-4">🧠</div>
				<h2 class="text-3xl md:text-4xl font-black tracking-tight mb-2 uppercase">Session Cleared</h2>
				<p class="font-mono text-sm font-bold opacity-75">Synaptic weights updated securely.</p>
			</div>
			
			<div class="grid grid-cols-1 md:grid-cols-3 gap-0 border-b-4 border-border-base">
				<!-- Session Stats -->
				<div class="p-6 md:border-r-4 border-border-base flex flex-col items-center justify-center bg-surface-secondary">
					<span class="text-[10px] font-bold font-mono tracking-widest uppercase text-content-tertiary mb-1">Items Processed</span>
					<span class="text-3xl font-black">{items.length}</span>
				</div>
				<div class="p-6 md:border-r-4 border-b-4 md:border-b-0 border-border-base flex flex-col items-center justify-center bg-surface-secondary">
					<span class="text-[10px] font-bold font-mono tracking-widest uppercase text-content-tertiary mb-1">Time Elapsed</span>
					<span class="text-3xl font-black">{timeSpent}m</span>
				</div>
				<div class="p-6 flex flex-col items-center justify-center bg-surface-secondary">
					<span class="text-[10px] font-bold font-mono tracking-widest uppercase text-content-tertiary mb-1">Retention Rate</span>
					<span class="text-3xl font-black text-success-DEFAULT">
						{Math.round(((items.length - weakTopics.length) / Math.max(1, items.length)) * 100)}%
					</span>
				</div>
			</div>

			<!-- Weak Topic Recovery (Concept Reinforcement Mode) -->
			{#if weakTopics.length > 0}
				<div class="w-full bg-surface-primary p-6 md:p-8">
					<h3 class="font-black text-xl mb-4 flex items-center justify-center md:justify-start gap-2 text-warning-DEFAULT">
						<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" class="stroke-current" stroke-width="3" stroke-linecap="square"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
						Degradation Detected
					</h3>
					<p class="text-sm font-mono text-content-secondary mb-6 md:max-w-xl text-left mx-auto md:mx-0">
						The AI has flagged repeated failures on these semantic nodes. Consider running a reinforcement mode session to rebuild the structural understanding before standard recall scheduling applies.
					</p>
					
					<div class="flex flex-col gap-3 mb-8">
						{#each weakTopics as wt}
							<div class="flex items-center gap-4 p-4 brutal-border bg-surface-base">
								<div class="w-2 h-2 rounded-full bg-warning-DEFAULT shrink-0"></div>
								<div class="flex-1 font-mono font-bold text-sm text-left">{wt.topic}</div>
								<span class="text-xs font-bold text-content-tertiary uppercase tracking-widest">{results[wt.id]}</span>
							</div>
						{/each}
					</div>

					<div class="flex flex-col md:flex-row justify-between items-center gap-4 pt-4 border-t-4 border-border-base">
						<Button variant="secondary" onclick={finish} class="w-full md:w-auto order-2 md:order-1">Disengage</Button>
						<Button variant="primary" class="w-full md:w-auto order-1 md:order-2 bg-brand-secondary text-white">Start Reinforcement Mode</Button>
					</div>
				</div>
			{:else}
				<!-- Pure Success state -->
				<div class="p-8 pb-12 flex justify-center">
					<Button variant="primary" size="lg" onclick={finish} class="px-12 w-full md:w-auto">Return to Main View</Button>
				</div>
			{/if}
		</div>
	{/if}
</div>

<style>
	@keyframes slideUp {
		from { opacity: 0; transform: translateY(20px); }
		to { opacity: 1; transform: translateY(0); }
	}
	.animate-slide-up {
		animation: slideUp 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
	}
</style>