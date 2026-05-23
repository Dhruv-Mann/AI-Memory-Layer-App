<script lang="ts">
	interface Props {
		keys: string[];
		class?: string;
	}

	let { keys, class: className = '' }: Props = $props();

	// Format Mac specific symbols if needed
	const formatKey = (key: string) => {
		const isMac = typeof navigator !== 'undefined' && navigator.platform.indexOf('Mac') > -1;
		
		switch (key.toLowerCase()) {
			case 'cmd': return isMac ? '⌘' : 'Ctrl';
			case 'ctrl': return isMac ? '⌃' : 'Ctrl';
			case 'alt': return isMac ? '⌥' : 'Alt';
			case 'shift': return isMac ? '⇧' : 'Shift';
			case 'enter': return '↵';
			case 'escape': return 'ESC';
			default: return key.toUpperCase();
		}
	};
</script>

<span class="inline-flex items-center gap-1 {className}">
	{#each keys as key}
		<kbd class="min-w-[1.25rem] h-5 inline-flex items-center justify-center px-1 rounded bg-surface-secondary text-content-secondary border border-border-base border-b-2 font-mono text-[10px] font-semibold leading-none select-none shadow-sm shadow-black/5">
			{formatKey(key)}
		</kbd>
	{/each}
</span>