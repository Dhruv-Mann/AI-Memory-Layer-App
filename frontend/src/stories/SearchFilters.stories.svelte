<!-- SearchFilters.stories.svelte -->
<script module>
    import { defineMeta } from '@storybook/addon-svelte-csf';
    import SearchFilters from '../lib/components/composite/SearchFilters.svelte';

    const { Story } = defineMeta({
        title: 'Composite/SearchFilters',
        component: SearchFilters,
        argTypes: {
            availableTags: { control: 'object' },
            availableTypes: { control: 'object' },
        },
    });
</script>

<Story name="Default">
    <div class="p-6 bg-surface-primary max-w-3xl brutal-border shadow-md">
        <SearchFilters />
    </div>
</Story>

<Story name="Customized Options">
    <div class="p-6 bg-surface-primary max-w-3xl brutal-border shadow-md">
        <SearchFilters 
            availableTags={['svelte', 'react', 'rust', 'go', 'typescript', 'd3']}
            availableTypes={['text', 'code', 'link', 'audio']}
        />
    </div>
</Story>
