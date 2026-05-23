import type { Meta, StoryObj } from '@storybook/svelte';
import Toggle from '../lib/components/primitives/Toggle.svelte';

const meta = {
	title: 'Primitives/Toggle',
	component: Toggle,
	tags: ['autodocs'],
	args: {
		label: 'Enable feature'
	}
} satisfies Meta<typeof Toggle>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};

export const Checked: Story = {
	args: {
		checked: true
	}
};

export const Disabled: Story = {
	args: {
		disabled: true
	}
};

export const DisabledChecked: Story = {
	args: {
		disabled: true,
		checked: true
	}
};
