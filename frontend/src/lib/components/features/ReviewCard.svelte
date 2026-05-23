<script lang="ts">
	import Button from '../primitives/Button.svelte';

	interface ReviewCardProps {
		topic: string;
		content: string;
		source?: string;
		context?: string[];
		onAssess: (rating: 'forgot' | 'hard' | 'good' | 'easy') => void;
	}

	let { 
		topic, 
		content, 
		source, 
		context = [], 
		onAssess
	}: ReviewCardProps = $props();

	let showAnswer = $state(false);

	function handleKeydown(e: KeyboardEvent) {
		// Prevent default actions for standard space/enter when acting as a global shortcut
		// Note: ensure we only intercept when not typing in an input
		const target = e.target as HTMLElement;
		if (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA') return;

		if (!showAnswer && (e.key === 'Enter' || e.key === ' ')) {
			e.preventDefault();
			showAnswer = true;
			return;
		}

		if (showAnswer) {
			switch (e.key) {
				case '1': onAssess('forgot'); break;
				case '2': onAssess('hard'); break;
				case '3': onAssess('good'); break;
				case '4': onAssess('easy'); break;
			}
		}
	}
</script>

<svelte:window onkeydown={handleKeydown} />

<div class="flex flex-col brutal-border bg-surface-primary max-w-2xl mx-auto w-full h-full md:min-h-[500px]">
	<!-- Header -->
	<header class="p-6 border-b-4 border-border-base flex flex-col gap-2 shrink-0 bg-surface-secondary">
		<span class="text-[10px] font-mono font-bold text-content-tertiary uppercase tracking-widest">Concept Recall</span>
		<h2 class="text-2xl md:text-3xl font-black text-content-primary tracking-tight leading-tight">{topic}</h2>
		
		{#if source}
			<div class="inline-flex self-start px-2 py-1 mt-2 text-xs font-mono font-bold bg-surface-base brutal-border">
				Source: {source}
			</div>
		{/if}
	</header>
	
	<!-- Context / Answer Area -->
	<div class="p-6 md:p-8 flex-1 flex flex-col {showAnswer ? 'justify-start' : 'justify-center'} overflow-y-auto">
		{#if !showAnswer}
			<div class="flex flex-col items-center justify-center text-center gap-6 opacity-80 h-full">
				<div class="text-4xl">🤔</div>
				<p class="font-mono text-sm text-content-secondary max-w-sm">Think deeply about the concept.</p>
				<Button variant="primary" size="lg" onclick={() => showAnswer = true} class="mt-4 px-8">
					Reveal Answer (Space)
				</Button>
			</div>
		{:else}
			<div class="flex flex-col gap-6 animate-fade-in">
				<div class="text-lg md:text-xl font-medium text-content-primary leading-relaxed font-sans">
					{content}
				</div>
				
				{#if context.length > 0}
					<div class="mt-4 border-l-4 border-brand-primary pl-5 py-2 bg-brand-primary/5">
						<h4 class="text-xs font-bold font-mono uppercase tracking-wider mb-3 text-content-secondary">Referenced Contexts</h4>
						<ul class="text-sm text-content-primary space-y-4">
							{#each context as ctx}
								<li class="leading-relaxed relative before:content-['-'] before:absolute before:-left-4 before:text-brand-primary">{ctx}</li>
							{/each}
						</ul>
					</div>
				{/if}
			</div>
		{/if}
	</div>

	<!-- Assessment Actions -->
	{#if showAnswer}
		<div class="p-4 border-t-4 border-border-base bg-surface-secondary shrink-0 animate-slide-up">
			<div class="text-center mb-3">
				<span class="text-[10px] font-bold font-mono tracking-widest uppercase text-content-tertiary">Assess Retention</span>
			</div>
			<div class="grid grid-cols-2 md:grid-cols-4 gap-3 md:gap-4">
				<Button variant="danger" onclick={() => onAssess('forgot')} class="w-full py-4 relative group overflow-hidden">
					<div class="flex flex-col items-center gap-1 z-10 relative">
						<span class="font-black tracking-wide">Forgot</span>
						<span class="text-[10px] font-mono opacity-80 border border-current px-2 py-0.5 rounded-sm">Press 1</span>
					</div>
					<div class="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform"></div>
				</Button>
				
				<Button variant="secondary" onclick={() => onAssess('hard')} class="w-full py-4 relative group overflow-hidden">
					<div class="flex flex-col items-center gap-1 z-10 relative">
						<span class="font-black tracking-wide">Hard</span>
						<span class="text-[10px] font-mono opacity-80 border border-current px-2 py-0.5 rounded-sm">Press 2</span>
					</div>
					<div class="absolute inset-0 bg-black/5 translate-y-full group-hover:translate-y-0 transition-transform"></div>
				</Button>
				
				<Button variant="primary" onclick={() => onAssess('good')} class="w-full py-4 relative group overflow-hidden">
					<div class="flex flex-col items-center gap-1 z-10 relative">
						<span class="font-black tracking-wide">Good</span>
						<span class="text-[10px] font-mono opacity-80 border border-current px-2 py-0.5 rounded-sm">Press 3</span>
					</div>
					<div class="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform"></div>
				</Button>

				<!-- Note: Passing custom style directly because it matches the neo-brutalist aesthetic with custom green -->
				<Button variant="primary" onclick={() => onAssess('easy')} class="w-full py-4 relative group overflow-hidden !bg-success-DEFAULT !text-white !border-current hover:!-translate-y-1">
					<div class="flex flex-col items-center gap-1 z-10 relative">
						<span class="font-black tracking-wide">Easy</span>
						<span class="text-[10px] font-mono opacity-80 border border-current px-2 py-0.5 rounded-sm">Press 4</span>
					</div>
					<div class="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform"></div>
				</Button>
			</div>
		</div>
	{/if}
</div>

<style>
	@keyframes fadeIn {
		from { opacity: 0; }
		to { opacity: 1; }
	}
	@keyframes slideUp {
		from { opacity: 0; transform: translateY(10px); }
		to { opacity: 1; transform: translateY(0); }
	}
	.animate-fade-in {
		animation: fadeIn 0.3s ease-out forwards;
	}
	.animate-slide-up {
		animation: slideUp 0.3s ease-out forwards;
	}
</style>