<script lang="ts">
	interface Props {
		targetId: string;
		label: string;
	}

	let { targetId, label }: Props = $props();
</script>

<a
	href="#{targetId}"
	class="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-notification focus:px-4 focus:py-2.5 focus:bg-brand-primary focus:text-white focus:font-black focus:font-mono focus:uppercase focus:tracking-wider focus:brutal-border focus:shadow-[4px_4px_0px_rgba(0,0,0,1)] focus:outline-none"
>
	{label}
</a>
