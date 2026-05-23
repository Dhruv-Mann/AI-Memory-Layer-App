<!-- CommandPalette.stories.svelte -->
<script module>
    import { defineMeta } from '@storybook/addon-svelte-csf';
    import { expect, userEvent, within } from '@storybook/test';
    import CommandPalette from '../lib/components/composite/CommandPalette.svelte';

    const mockCommands = [
        {
            id: '1',
            title: 'Create Node',
            description: 'Create a new knowledge node',
            category: 'Action',
            shortcut: ['Cmd', 'N'],
            perform: () => console.log('Performed Create Node')
        },
        {
            id: '2',
            title: 'Search Library',
            description: 'Search across all memory nodes',
            category: 'Navigation',
            shortcut: ['Cmd', 'F'],
            perform: () => console.log('Performed Search Library')
        },
        {
            id: '3',
            title: 'Toggle Dark Mode',
            category: 'Preferences',
            perform: () => console.log('Performed Toggle Theme')
        }
    ];

    const { Story } = defineMeta({
        title: 'Composite/CommandPalette',
        component: CommandPalette,
        argTypes: {
            open: { control: 'boolean' }
        }
    });
</script>

<script>
    // A wrapper to control open state for manual testing
    let openState = $state(true);
</script>

<Story name="Default (Interactive)">
    <div class="h-[600px] w-full relative bg-surface-secondary flex items-center justify-center">
        <p class="text-content-tertiary">The palette is rendered in a dialog above this content.</p>
        <CommandPalette open={true} commands={mockCommands} />
    </div>
</Story>

<Story name="Functional Testing" play={async ({ canvasElement }) => {
    // Tests are run on the body because dialogs render at the root layer, outside the normal storybook canvas container
    const body = within(document.body);
    
    // 1. Initial State
    const input = await body.findByPlaceholderText('Type a command or search...');
    await expect(input).toBeVisible();

    // 2. See that all commands are initially rendered
    await expect(body.getByText('Create Node')).toBeVisible();
    await expect(body.getByText('Search Library')).toBeVisible();
    await expect(body.getByText('Toggle Dark Mode')).toBeVisible();

    // 3. Search and fuzzy match
    await userEvent.type(input, 'dark');
    
    // Toggle Dark Mode should stay, others should be hidden
    await expect(body.getByText('Toggle Dark Mode')).toBeVisible();
    await expect(body.queryByText('Create Node')).not.toBeInTheDocument();
    
    // 4. Test "No results"
    await userEvent.clear(input);
    await userEvent.type(input, 'xxxxx');
    await expect(body.getByText('No commands found for "xxxxx"')).toBeVisible();
}}>
    <div class="h-[600px] w-full relative">
        <CommandPalette open={true} commands={mockCommands} />
    </div>
</Story>