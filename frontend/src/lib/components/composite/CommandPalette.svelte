<script module lang="ts">
	export interface CommandAction {
		id: string;
		title: string;
		category: string;
		description?: string;
		shortcut?: string[];
		perform: () => void;
	}
</script>

<script lang="ts">
	import { browser } from '$app/environment';
	import { untrack } from 'svelte';
	import { trapFocus } from '../../stores/focusStore';
	import KeyboardHint from '../primitives/KeyboardHint.svelte';

	interface Props {
		open?: boolean;
		commands?: CommandAction[];
	}

	let { open = $bindable(false), commands = [] }: Props = $props();

	let search = $state('');
	let selectedIndex = $state(0);
	
	let inputElement: HTMLInputElement;
	let containerElement: HTMLElement;
	let dialogElement: HTMLDialogElement;

	// Fake fuzzy match for demo
	let filteredCommands = $derived.by(() => {
		if (!search) return commands;
		const query = search.toLowerCase();
		return commands.filter(
			c => c.title.toLowerCase().includes(query) || 
			(c.description && c.description.toLowerCase().includes(query)) ||
			c.category.toLowerCase().includes(query)
		);
	});

	let groupedCommands = $derived.by(() => {
		const groups: Record<string, CommandAction[]> = {};
		for (const cmd of filteredCommands) {
			if (!groups[cmd.category]) groups[cmd.category] = [];
			groups[cmd.category].push(cmd);
		}
		return groups;
	});

	let flatFilteredList = $derived(filteredCommands);

	$effect(() => {
		if (search !== undefined) {
			untrack(() => {
				selectedIndex = 0;
			});
		}
	});

	$effect(() => {
		if (browser) {
			const handleOpen = () => (open = true);
			window.addEventListener('open-command-palette', handleOpen);
			return () => window.removeEventListener('open-command-palette', handleOpen);
		}
	});

	$effect(() => {
		if (dialogElement) {
			if (open && !dialogElement.open) {
				dialogElement.showModal();
				// Use timeout to ensure it renders before focusing
				setTimeout(() => {
					if (inputElement) inputElement.focus();
				}, 10);
			} else if (!open && dialogElement.open) {
				dialogElement.close();
				search = '';
			}
		}
	});

	function close() {
		open = false;
	}

	function executeCommand(cmd: CommandAction) {
		close();
		cmd.perform();
	}

	function handleKeydown(e: KeyboardEvent) {
		if (e.key === 'Escape') {
			e.preventDefault();
			close();
			return;
		}

		if (flatFilteredList.length === 0) return;

		if (e.key === 'ArrowDown') {
			e.preventDefault();
			selectedIndex = (selectedIndex + 1) % flatFilteredList.length;
			scrollSelectedIntoView();
		} else if (e.key === 'ArrowUp') {
			e.preventDefault();
			selectedIndex = (selectedIndex - 1 + flatFilteredList.length) % flatFilteredList.length;
			scrollSelectedIntoView();
		} else if (e.key === 'Enter') {
			e.preventDefault();
			const cmd = flatFilteredList[selectedIndex];
			if (cmd) executeCommand(cmd);
		}
	}

	function scrollSelectedIntoView() {
		if (!browser) return;
		setTimeout(() => {
			const selected = containerElement?.querySelector('[aria-selected="true"]');
			if (selected) {
				selected.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
			}
		}, 0);
	}
</script>

<!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
<dialog
	bind:this={dialogElement}
	onclose={close}
	onclick={(e) => {
		if (e.target === dialogElement) close();
	}}
	onkeydown={handleKeydown}
	class="bg-transparent p-0 m-auto max-w-2xl w-[90vw] top-1/4 absolute z-[100] backdrop:bg-black/60 backdrop:backdrop-blur-sm open:animate-in open:fade-in duration-100"
>
	<div 
		use:trapFocus={open}
		class="brutal-card flex flex-col overflow-hidden shadow-2xl bg-surface-base w-full max-h-[60vh] border-2 border-brand-primary"
		role="combobox"
		aria-expanded={open}
		aria-haspopup="listbox"
		aria-controls="command-palette-results"
	>
		<!-- Search Header -->
		<div class="flex items-center px-4 py-3 border-b-2 border-border-base gap-3">
			<span class="text-brand-primary">➜</span>
			<input 
				bind:this={inputElement}
				bind:value={search}
				type="text"
				placeholder="Type a command or search..."
				class="flex-1 bg-transparent border-none outline-none text-lg font-mono placeholder:text-content-tertiary text-content-primary"
				aria-autocomplete="list"
			/>
			<KeyboardHint keys={['Esc']} />
		</div>

		<!-- Results -->
		<div 
			bind:this={containerElement}
			id="command-palette-results"
			class="flex-1 overflow-y-auto outline-none"
			role="listbox"
		>
			{#if flatFilteredList.length === 0}
				<div class="px-6 py-12 text-center text-content-tertiary">
					<p class="font-mono text-sm">No commands found for "{search}"</p>
				</div>
			{:else}
				<div class="p-2 space-y-4">
					{#each Object.entries(groupedCommands) as [category, items]}
						<div class="space-y-1">
							<div class="px-3 text-xs font-bold uppercase tracking-wider text-brand-primary mb-2 mt-2">
								{category}
							</div>
							{#each items as item}
								{@const globalIndex = flatFilteredList.indexOf(item)}
								{@const isSelected = globalIndex === selectedIndex}
								<!-- svelte-ignore a11y_interactive_supports_focus -->
								<!-- svelte-ignore a11y_click_events_have_key_events -->
								<div
									role="option"
									aria-selected={isSelected}
									class="flex items-center justify-between px-3 py-2.5 cursor-pointer brutal-border transition-all {isSelected ? 'bg-surface-secondary border-brand-primary brutal-shadow-sm translate-x-1' : 'border-transparent hover:bg-surface-secondary/50'}"
									onclick={() => executeCommand(item)}
									onmousemove={() => { if (selectedIndex !== globalIndex) selectedIndex = globalIndex }}
								>
									<div class="flex flex-col gap-0.5 min-w-0">
										<span class="font-medium text-sm text-content-primary truncate">{item.title}</span>
										{#if item.description}
											<span class="text-xs text-content-tertiary truncate">{item.description}</span>
										{/if}
									</div>
									{#if item.shortcut}
										<div class="shrink-0 ml-4">
											<KeyboardHint keys={item.shortcut} />
										</div>
									{/if}
								</div>
							{/each}
						</div>
					{/each}
				</div>
			{/if}
		</div>

		<div aria-live="polite" class="sr-only">
			{flatFilteredList.length} results available.
		</div>

		<!-- Footer -->
		<div class="px-4 py-2 border-t border-border-base bg-surface-tertiary flex items-center gap-4 text-xs text-content-tertiary font-mono">
			<span class="flex items-center gap-1"><KeyboardHint keys={['↑', '↓']} /> to navigate</span>
			<span class="flex items-center gap-1"><KeyboardHint keys={['Enter']} /> to select</span>
		</div>
	</div>
</dialog>