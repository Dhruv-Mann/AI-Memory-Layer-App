<!-- MemoryChunk.stories.svelte -->
<script module>
    import { defineMeta } from '@storybook/addon-svelte-csf';
    import MemoryChunk from '../lib/components/features/MemoryChunk.svelte';

    const mockData = {
        id: 'chunk-1',
        summary: 'React StrictMode setup and cleanup execution pattern',
        fullContext: 'React calls setup and cleanup twice in strict mode. In Svelte 5, runes are evaluated and setup effects run once, but cleanups are called reactively. This prevents common state synchronization issues across mounts.',
        confidenceScore: 0.92,
        citations: [
            { id: 'cit-1', sourceTitle: 'React Docs - StrictMode', url: 'https://react.dev' },
            { id: 'cit-2', sourceTitle: 'Svelte Runes Spec', url: 'https://svelte.dev' }
        ],
        linkedTopics: [
            { id: 't-1', title: 'React Lifecycle' },
            { id: 't-2', title: 'Svelte 5 Runes' }
        ]
    };

    const { Story } = defineMeta({
        title: 'Features/MemoryChunk',
        component: MemoryChunk,
        argTypes: {
            isExpanded: { control: 'boolean' },
            isFocused: { control: 'boolean' },
        },
    });
</script>

<Story name="Default">
    <div class="p-6 max-w-xl">
        <MemoryChunk data={mockData} />
    </div>
</Story>

<Story name="Expanded">
    <div class="p-6 max-w-xl">
        <MemoryChunk data={mockData} isExpanded={true} />
    </div>
</Story>

<Story name="Focused">
    <div class="p-6 max-w-xl">
        <MemoryChunk data={mockData} isFocused={true} />
    </div>
</Story>
