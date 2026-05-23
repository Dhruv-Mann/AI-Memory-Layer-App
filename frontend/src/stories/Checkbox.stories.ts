import type { Meta, StoryObj } from '@storybook/svelte';
import Checkbox from '../lib/components/primitives/Checkbox.svelte';

const meta = {
	title: 'Primitives/Checkbox',
	component: Checkbox,
	tags: ['autodocs'],
	args: {
		label: 'Accept Terms and Conditions'
	}
} satisfies Meta<typeof Checkbox>;

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
