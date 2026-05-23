<!-- Input.stories.svelte -->
<script module>
    import { defineMeta } from '@storybook/addon-svelte-csf';
    import Input from '../lib/components/primitives/Input.svelte';

    const { Story } = defineMeta({
        title: 'Primitives/Input',
        component: Input,
        argTypes: {
            type: {
                control: { type: 'select' },
                options: ['text', 'email', 'password', 'search', 'url'],
            },
            size: {
                control: { type: 'select' },
                options: ['sm', 'md', 'lg'],
            },
            disabled: { control: 'boolean' },
            error: { control: 'boolean' },
        },
    });
</script>

<Story name="Default">
    <div class="w-72">
        <Input placeholder="Type something..." />
    </div>
</Story>

<Story name="Sizes">
    <div class="flex flex-col gap-4 w-72">
        <Input size="sm" placeholder="Small input" />
        <Input size="md" placeholder="Medium input" />
        <Input size="lg" placeholder="Large input" />
    </div>
</Story>

<Story name="States">
    <div class="flex flex-col gap-4 w-72">
        <Input placeholder="Normal input..." helperText="This is some helper text." />
        <Input disabled placeholder="I am disabled..." value="Disabled Value" />
        <Input error placeholder="Error state..." helperText="This field is required!" />
    </div>
</Story>

<Story name="Types">
    <div class="flex flex-col gap-4 w-72">
        <Input type="email" placeholder="Email map@memory.local" />
        <Input type="password" placeholder="Password" value="hunter2" />
        <Input type="search" placeholder="Search memories..." />
    </div>
</Story>
