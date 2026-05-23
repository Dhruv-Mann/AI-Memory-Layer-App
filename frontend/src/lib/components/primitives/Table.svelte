<script module lang="ts">
	export interface TableColumn {
		key: string;
		label: string;
		sortable?: boolean;
		align?: 'left' | 'center' | 'right';
	}
</script>

<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		columns: TableColumn[];
		data: any[];
		sortKey?: string | null;
		sortDirection?: 'asc' | 'desc';
		class?: string;
		onsort?: (key: string, direction: 'asc' | 'desc') => void;
		
		// Snippets
		header?: Snippet<[TableColumn]>;
		body?: Snippet<[any, TableColumn]>;
		footer?: Snippet;
	}

	let {
		columns,
		data,
		sortKey = $bindable(null),
		sortDirection = $bindable('asc'),
		class: className = '',
		onsort,
		header,
		body,
		footer
	}: Props = $props();

	function handleSort(col: TableColumn) {
		if (!col.sortable) return;
		
		if (sortKey === col.key) {
			sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
		} else {
			sortKey = col.key;
			sortDirection = 'asc';
		}

		if (onsort) onsort(col.key, sortDirection);
	}
</script>

<div class="w-full overflow-x-auto brutal-border bg-surface-primary {className}">
	<table class="w-full text-sm tracking-tight text-left border-collapse">
		<thead class="bg-surface-secondary border-b-2 border-primary">
			<tr>
				{#each columns as col}
					<th 
						aria-sort={sortKey === col.key ? (sortDirection === 'asc' ? 'ascending' : 'descending') : undefined}
						class="px-4 py-2 font-bold uppercase text-fg-primary leading-compact select-none"
						class:cursor-pointer={col.sortable}
						class:text-center={col.align === 'center'}
						class:text-right={col.align === 'right'}
						onclick={() => handleSort(col)}
					>
						<div class="flex items-center gap-2 {col.align === 'right' ? 'justify-end' : col.align === 'center' ? 'justify-center' : 'justify-start'}">
							{#if header}
								{@render header(col)}
							{:else}
								{col.label}
							{/if}
							
							{#if col.sortable}
								<span class="w-3 h-3 flex items-center justify-center">
									{#if sortKey === col.key}
										{sortDirection === 'asc' ? '▲' : '▼'}
									{:else}
										<span class="text-surface-tertiary">↕</span>
									{/if}
								</span>
							{/if}
						</div>
					</th>
				{/each}
			</tr>
		</thead>
		<tbody class="divide-y-2 divide-surface-tertiary">
			{#each data as row}
				<tr class="hover:bg-surface-secondary transition-colors duration-fast">
					{#each columns as col}
						<td 
							class="px-4 py-1.5 leading-compact text-fg-primary whitespace-nowrap"
							class:text-center={col.align === 'center'}
							class:text-right={col.align === 'right'}
						>
							{#if body}
								{@render body(row, col)}
							{:else}
								{row[col.key]}
							{/if}
						</td>
					{/each}
				</tr>
			{/each}
		</tbody>
		{#if footer}
			<tfoot class="bg-surface-tertiary border-t-2 border-primary font-bold text-fg-primary px-4 py-2">
				<tr>
					<td colspan={columns.length} class="px-4 py-2">
						{@render footer()}
					</td>
				</tr>
			</tfoot>
		{/if}
	</table>
</div>
