<!-- MasteryEvolutionChart.stories.svelte -->
<script module>
    import { defineMeta } from '@storybook/addon-svelte-csf';
    import MasteryEvolutionChart from '../lib/components/features/MasteryEvolutionChart.svelte';

    const mockSeries = [
        {
            topicId: 't1',
            label: 'Frontend Development',
            color: 'var(--color-primary, #2563eb)',
            visible: true,
            data: Array.from({length: 10}).map((_, i) => ({
                date: new Date(Date.now() - (9 - i) * 86400000),
                value: 0.3 + i * 0.05 + Math.random() * 0.1
            }))
        },
        {
            topicId: 't2',
            label: 'Backend & Databases',
            color: 'var(--color-secondary, #7c3aed)',
            visible: true,
            data: Array.from({length: 10}).map((_, i) => ({
                date: new Date(Date.now() - (9 - i) * 86400000),
                value: Math.min(1, 0.5 + i * 0.03 + Math.random() * 0.05)
            }))
        }
    ];

    const { Story } = defineMeta({
        title: 'Features/MasteryEvolutionChart',
        component: MasteryEvolutionChart,
    });
</script>

<Story name="Default">
    <div class="p-6 max-w-2xl bg-surface-primary brutal-border shadow-md">
        <MasteryEvolutionChart series={mockSeries} />
    </div>
</Story>
