import type { Config } from 'tailwindcss';
import plugin from 'tailwindcss/plugin';

export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      colors: {
        gray: {
          50: 'var(--color-gray-50)',
          100: 'var(--color-gray-100)',
          200: 'var(--color-gray-200)',
          300: 'var(--color-gray-300)',
          400: 'var(--color-gray-400)',
          500: 'var(--color-gray-500)',
          600: 'var(--color-gray-600)',
          700: 'var(--color-gray-700)',
          800: 'var(--color-gray-800)',
          900: 'var(--color-gray-900)',
        },
        brand: {
          primary: 'var(--color-primary)',
          secondary: 'var(--color-secondary)',
          accent: 'var(--color-accent)',
        },
        success: {
          light: 'var(--color-success-light)',
          DEFAULT: 'var(--color-success-base)',
          dark: 'var(--color-success-dark)',
        },
        warning: {
          light: 'var(--color-warning-light)',
          DEFAULT: 'var(--color-warning-base)',
          dark: 'var(--color-warning-dark)',
        },
        error: {
          light: 'var(--color-error-light)',
          DEFAULT: 'var(--color-error-base)',
          dark: 'var(--color-error-dark)',
        },
        info: {
          light: 'var(--color-info-light)',
          DEFAULT: 'var(--color-info-base)',
          dark: 'var(--color-info-dark)',
        },
        state: {
          'not-learned': 'var(--color-state-not-learned)',
          learning: 'var(--color-state-learning)',
          mastered: 'var(--color-state-mastered)',
          forgotten: 'var(--color-state-forgotten)',
          'revision-due': 'var(--color-state-revision-due)',
        },
        urgency: {
          low: 'var(--color-urgency-low)',
          medium: 'var(--color-urgency-medium)',
          high: 'var(--color-urgency-high)',
          critical: 'var(--color-urgency-critical)',
        },
        surface: {
          primary: 'var(--bg-primary)',
          secondary: 'var(--bg-secondary)',
          tertiary: 'var(--bg-tertiary)',
          inverse: 'var(--bg-inverse)',
        },
        fg: {
          primary: 'var(--text-primary)',
          secondary: 'var(--text-secondary)',
          tertiary: 'var(--text-tertiary)',
          inverse: 'var(--text-inverse)',
        },
        brutal: {
          primary: 'var(--border-primary)',
          secondary: 'var(--border-secondary)',
        }
      },
      spacing: {
        0: 'var(--space-0)',
        1: 'var(--space-1)',
        2: 'var(--space-2)',
        3: 'var(--space-3)',
        4: 'var(--space-4)',
        6: 'var(--space-6)',
        8: 'var(--space-8)',
        12: 'var(--space-12)',
        16: 'var(--space-16)',
        24: 'var(--space-24)',
        32: 'var(--space-32)',
      },
      fontSize: {
        xs: 'var(--text-xs)',
        sm: 'var(--text-sm)',
        base: 'var(--text-base)',
        lg: 'var(--text-lg)',
        xl: 'var(--text-xl)',
        '2xl': 'var(--text-2xl)',
        '3xl': 'var(--text-3xl)',
        '4xl': 'var(--text-4xl)',
      },
      boxShadow: {
        sm: 'var(--shadow-sm)',
        md: 'var(--shadow-md)',
        lg: 'var(--shadow-lg)',
        xl: 'var(--shadow-xl)',
      },
      borderRadius: {
        none: 'var(--border-radius-none)',
        sm: 'var(--border-radius-sm)',
        md: 'var(--border-radius-md)',
        lg: 'var(--border-radius-lg)',
      },
      transitionDuration: {
        fast: 'var(--anim-duration-fast)',
        base: 'var(--anim-duration-base)',
        slow: 'var(--anim-duration-slow)',
      },
      transitionTimingFunction: {
        brutal: 'var(--anim-ease-brutal)',
      },
      zIndex: {
        base: 'var(--z-base)',
        dropdown: 'var(--z-dropdown)',
        sticky: 'var(--z-sticky)',
        panel: 'var(--z-panel)',
        modal: 'var(--z-modal)',
        tooltip: 'var(--z-tooltip)',
        'command-palette': 'var(--z-command-palette)',
        notification: 'var(--z-notification)',
      },
      borderWidth: {
        DEFAULT: 'var(--border-width)',
      }
    },
  },
  plugins: [
    plugin(function({ addUtilities }) {
      addUtilities({
        '.brutal-border': {
          border: 'var(--border-width) solid var(--border-primary)',
        },
        '.brutal-shadow-sm': {
          boxShadow: 'var(--shadow-sm)',
        },
        '.brutal-shadow-md': {
          boxShadow: 'var(--shadow-md)',
        },
        '.brutal-shadow-lg': {
          boxShadow: 'var(--shadow-lg)',
        },
        '.brutal-shadow-xl': {
          boxShadow: 'var(--shadow-xl)',
        },
        '.brutal-card': {
          backgroundColor: 'var(--card-bg)',
          border: 'var(--card-border)',
          boxShadow: 'var(--card-shadow)',
          padding: 'var(--card-pad)',
        },
      });
    })
  ],
} satisfies Config;