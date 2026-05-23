<script lang="ts">
	interface Props {
		currentPage: number;
		totalPages: number;
		onPageChange?: (page: number) => void;
		class?: string;
	}

	let {
		currentPage = $bindable(1),
		totalPages,
		onPageChange,
		class: className = ''
	}: Props = $props();

	function goToPage(page: number) {
		if (page >= 1 && page <= totalPages) {
			currentPage = page;
			if (onPageChange) onPageChange(page);
		}
	}

	let pageNumbers = $derived.by(() => {
		const pages = [];
		if (totalPages <= 5) {
			for (let i = 1; i <= totalPages; i++) pages.push(i);
		} else {
			if (currentPage <= 3) {
				pages.push(1, 2, 3, 4, '...', totalPages);
			} else if (currentPage >= totalPages - 2) {
				pages.push(1, '...', totalPages - 3, totalPages - 2, totalPages - 1, totalPages);
			} else {
				pages.push(1, '...', currentPage - 1, currentPage, currentPage + 1, '...', totalPages);
			}
		}
		return pages;
	});
</script>

<nav aria-label="Pagination Navigation" class="flex flex-wrap items-center gap-2 {className}">
	<button
		class="w-10 h-10 flex items-center justify-center brutal-border bg-surface-primary hover:bg-surface-secondary active:translate-y-px disabled:opacity-50 disabled:cursor-not-allowed disabled:active:translate-y-0 font-bold transition-all focus:outline-none focus:ring-2 focus:ring-brand-primary"
		disabled={currentPage === 1}
		onclick={() => goToPage(currentPage - 1)}
		aria-label="Previous page"
	>
		<!-- Brutalist Left Arrow -->
		<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="square" stroke-linejoin="miter">
			<line x1="19" y1="12" x2="5" y2="12"></line>
			<polyline points="12 19 5 12 12 5"></polyline>
		</svg>
	</button>

	{#each pageNumbers as param}
		{#if param === '...'}
			<span class="w-8 h-10 flex items-center justify-center font-bold text-fg-tertiary select-none">...</span>
		{:else}
			<button
				class="w-10 h-10 flex items-center justify-center brutal-border font-bold transition-all focus:outline-none focus:ring-2 focus:ring-brand-primary 
				{currentPage === param 
					? 'bg-brand-primary text-white border-brand-primary brutal-shadow-sm translate-y-px' 
					: 'bg-surface-primary hover:bg-surface-secondary text-fg-primary active:translate-y-px'}"
				aria-current={currentPage === param ? 'page' : undefined}
				onclick={() => goToPage(param as number)}
			>
				{param}
			</button>
		{/if}
	{/each}

	<button
		class="w-10 h-10 flex items-center justify-center brutal-border bg-surface-primary hover:bg-surface-secondary active:translate-y-px disabled:opacity-50 disabled:cursor-not-allowed disabled:active:translate-y-0 font-bold transition-all focus:outline-none focus:ring-2 focus:ring-brand-primary"
		disabled={currentPage === totalPages}
		onclick={() => goToPage(currentPage + 1)}
		aria-label="Next page"
	>
		<!-- Brutalist Right Arrow -->
		<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="square" stroke-linejoin="miter">
			<line x1="5" y1="12" x2="19" y2="12"></line>
			<polyline points="12 5 19 12 12 19"></polyline>
		</svg>
	</button>
</nav>
