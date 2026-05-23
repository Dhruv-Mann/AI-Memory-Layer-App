<script lang="ts">
	import Button from '../primitives/Button.svelte';

	interface Props {
		topic: {
			id: string;
			title: string;
			urgency: 'low' | 'medium' | 'high' | 'critical';
			dueDate: string | Date;
			contextPreview: string;
		};
		onReview?: (id: string) => void;
		onDismiss?: (id: string) => void;
		onViewDetails?: (id: string) => void;
		class?: string;
	}

	let {
		topic,
		onReview,
		onDismiss,
		onViewDetails,
		class: className = ''
	}: Props = $props();

	function getUrencyStyles(urgency: string) {
		switch (urgency) {
			case 'critical': return 'border-error-DEFAULT bg-error-DEFAULT/10 text-error-DEFAULT';
			case 'high': return 'border-warning-DEFAULT bg-warning-DEFAULT/10 text-warning-DEFAULT';
			case 'medium': return 'border-brand-primary bg-brand-primary/10 text-brand-primary';
			case 'low': default: return 'border-border-subtle bg-surface-secondary text-content-secondary';
		}
	}
</script>

<div class="p-4 brutal-border bg-surface-primary flex flex-col gap-3 {className}">
	<div class="flex justify-between items-start gap-4">
		<h4 class="font-bold text-content-primary line-clamp-1 flex-1">{topic.title}</h4>
		<div class="px-2 py-0.5 text-[10px] font-bold uppercase tracking-widest border border-solid shadow-[1px_1px_0px_rgba(0,0,0,1)] {getUrencyStyles(topic.urgency)}">
			{topic.urgency}
		</div>
	</div>

	<p class="text-xs text-content-secondary line-clamp-2 font-mono">
		{topic.contextPreview}
	</p>

	<div class="text-xs font-bold text-content-tertiary">
		Due: {typeof topic.dueDate === 'string' ? topic.dueDate : topic.dueDate.toLocaleDateString()}
	</div>

	<div class="flex items-center gap-2 mt-auto pt-2 border-t-2 border-border-subtle">
		<Button variant="primary" size="sm" class="flex-1 text-xs" onclick={() => onReview?.(topic.id)}>
			Review
		</Button>
		<Button variant="secondary" size="sm" class="flex-1 text-xs" onclick={() => onViewDetails?.(topic.id)}>
			Details
		</Button>
		<Button variant="ghost" size="sm" class="px-2 text-content-tertiary hover:text-error-DEFAULT" aria-label="Dismiss" onclick={() => onDismiss?.(topic.id)}>
			<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="square"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
		</Button>
	</div>
</div>