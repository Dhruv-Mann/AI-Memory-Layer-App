<!-- MemoryDecayChart.stories.svelte -->
<script module>
    import { defineMeta } from '@storybook/addon-svelte-csf';
    import MemoryDecayChart from '../lib/components/features/MemoryDecayChart.svelte';

    const mockCurves = [
        {
            id: 'c1',
            label: 'First Learn',
            data: [ {day: 0, retention: 1}, {day: 1, retention: 0.8}, {day: 3, retention: 0.5} ],
            predictedForgetDay: 1
        },
        {
            id: 'c2',
            label: 'First Review',
            data: [ {day: 1, retention: 1}, {day: 3, retention: 0.8}, {day: 7, retention: 0.5} ],
            predictedForgetDay: 3
        },
        {
            id: 'c3',
            label: 'Current Status',
            data: [ {day: 3, retention: 1}, {day: 7, retention: 0.8}, {day: 14, retention: 0.6} ],
            predictedForgetDay: 7
        }
    ];

    const { Story } = defineMeta({
        title: 'Features/MemoryDecayChart',
        component: MemoryDecayChart,
        argTypes: {
            currentDay: { control: 'number' },
        },
    });
</script>

<Story name="Default">
    <div class="p-6 max-w-2xl bg-surface-primary brutal-border shadow-md">
        <MemoryDecayChart curves={mockCurves} currentDay={5} />
    </div>
</Story>
