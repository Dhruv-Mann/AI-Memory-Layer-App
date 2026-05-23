<!-- Button.stories.svelte -->
<script module>
    import { defineMeta } from '@storybook/addon-svelte-csf';
    import Button from '../lib/components/primitives/Button.svelte';

    const { Story } = defineMeta({
        title: 'Primitives/Button',
        component: Button,
        argTypes: {
            variant: {
                control: { type: 'select' },
                options: ['primary', 'secondary', 'ghost', 'danger', 'icon'],
            },
            size: {
                control: { type: 'select' },
                options: ['sm', 'md', 'lg'],
            },
            disabled: { control: 'boolean' },
            loading: { control: 'boolean' },
            fullWidth: { control: 'boolean' },
        },
    });
</script>

<Story name="Primary">
    <Button variant="primary">Primary Button</Button>
</Story>

<Story name="Secondary">
    <Button variant="secondary">Secondary Button</Button>
</Story>

<Story name="Danger">
    <Button variant="danger">Danger Button</Button>
</Story>

<Story name="Ghost">
    <Button variant="ghost">Ghost Button</Button>
</Story>

<Story name="Sizes">
    <div class="flex gap-4 items-center">
        <Button size="sm">Small</Button>
        <Button size="md">Medium</Button>
        <Button size="lg">Large</Button>
    </div>
</Story>

<Story name="States">
    <div class="flex flex-col gap-4 items-start">
        <Button disabled>Disabled Button</Button>
        <Button loading>Loading State</Button>
        <Button fullWidth>Full Width Button</Button>
    </div>
</Story>
