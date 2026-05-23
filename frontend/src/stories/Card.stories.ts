import type { Meta, StoryObj } from '@storybook/svelte';
import Card from '../lib/components/layout/Card.svelte';
import Button from '../lib/components/primitives/Button.svelte';
import { createRawSnippet } from 'svelte';

const meta = {
	title: 'Layout/Card',
	component: Card,
	tags: ['autodocs'],
} satisfies Meta<typeof Card>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
    args: {
        children: createRawSnippet(() => ({ render: () => `<h3 class="text-xl font-bold mb-2">Card Title</h3><p>This is a brutalist card.</p>` })) as any
    }
};
