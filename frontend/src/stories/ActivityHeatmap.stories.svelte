<!-- ActivityHeatmap.stories.svelte -->
<script module>
    import { defineMeta } from '@storybook/addon-svelte-csf';
    import ActivityHeatmap from '../lib/components/features/ActivityHeatmap.svelte';

    const mockData = Array.from({ length: 364 }).map((_, i) => {
        const val = Math.random();
        return {
            date: `Day ${i}`,
            count: Math.floor(val * 15),
            intensity: val < 0.8 ? 0 : val < 0.9 ? 0.4 : val < 0.95 ? 0.7 : 1
        };
    });

    const { Story } = defineMeta({
        title: 'Features/ActivityHeatmap',
        component: ActivityHeatmap,
        argTypes: {
            year: { control: 'number' },
        },
    });
</script>

<Story name="Default">
    <div class="p-6 max-w-4xl bg-surface-primary brutal-border shadow-md">
        <ActivityHeatmap data={mockData} />
    </div>
</Story>
