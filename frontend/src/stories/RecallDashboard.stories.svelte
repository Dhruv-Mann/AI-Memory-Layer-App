<!-- RecallDashboard.stories.svelte -->
<script module>
    import { defineMeta } from '@storybook/addon-svelte-csf';
    import RecallDashboard from '../lib/components/features/RecallDashboard.svelte';

    const { Story } = defineMeta({
        title: 'Features/RecallDashboard',
        component: RecallDashboard,
        argTypes: {
            topicsDue: { control: 'number' },
            currentStreak: { control: 'number' },
        },
    });
</script>

<Story name="Default">
    <div class="h-screen w-full brutal-border overflow-hidden">
        <RecallDashboard topicsDue={12} currentStreak={5} />
    </div>
</Story>
