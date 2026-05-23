import type { Meta, StoryObj } from '@storybook/svelte';
import Select from '../lib/components/primitives/Select.svelte';

const meta = {
	title: 'Primitives/Select',
	component: Select,
	tags: ['autodocs'],
	args: {
		options: [
			{ label: 'Option 1', value: '1' },
			{ label: 'Option 2', value: '2' },
			{ label: 'Option 3', value: '3' }
		]
	}
} satisfies Meta<typeof Select>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};

export const WithValue: Story = {
	args: {
		value: '2'
	}
};

export const Disabled: Story = {
	args: {
		disabled: true,
		value: '1'
	}
};
