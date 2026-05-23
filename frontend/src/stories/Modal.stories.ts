import type { Meta, StoryObj } from '@storybook/svelte';
import Modal from '../lib/components/overlays/Modal.svelte';

const meta = {
	title: 'Overlays/Modal',
	component: Modal,
	tags: ['autodocs'],
} satisfies Meta<typeof Modal>;

export default meta;
type Story = StoryObj<typeof meta>;

// Storybook handling for standard Modals can be tricky due to native HTML <dialog>.
// For now, these provide basic structure
export const Default: Story = {
    args: {
        open: true,
        title: 'Confirmation'
    }
};
