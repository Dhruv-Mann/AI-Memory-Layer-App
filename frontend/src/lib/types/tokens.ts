/**
 * Design Token Type Definitions
 * Generates literal types based on the CSS custom properties defined in the core token system.
 */

// Color System
export const GRAY_SCALE = ['50', '100', '200', '300', '400', '500', '600', '700', '800', '900'] as const;
export type GrayScale = typeof GRAY_SCALE[number];

export const BRAND_COLORS = ['primary', 'secondary', 'accent'] as const;
export type BrandColor = typeof BRAND_COLORS[number];

export const SEMANTIC_COLORS = ['success', 'warning', 'error', 'info'] as const;
export type SemanticColor = typeof SEMANTIC_COLORS[number];

export const MEMORY_STATES = ['not-learned', 'learning', 'mastered', 'forgotten', 'revision-due'] as const;
export type MemoryState = typeof MEMORY_STATES[number];

export const REVISION_URGENCY = ['low', 'medium', 'high', 'critical'] as const;
export type RevisionUrgency = typeof REVISION_URGENCY[number];

// Spacing System (Multiplier based on 4px)
export const SPACING_TOKENS = ['0', '1', '2', '3', '4', '6', '8', '12', '16', '24', '32'] as const;
export type SpacingToken = typeof SPACING_TOKENS[number];

// Typography System
export const TYPOGRAPHY_SCALES = ['xs', 'sm', 'base', 'lg', 'xl', '2xl', '3xl', '4xl'] as const;
export type TypographyScale = typeof TYPOGRAPHY_SCALES[number];

// Visual Modifiers
export const SHADOW_SIZES = ['sm', 'md', 'lg', 'xl'] as const;
export type ShadowSize = typeof SHADOW_SIZES[number];

export const BORDER_RADIUS = ['none', 'sm', 'md', 'lg'] as const;
export type BorderRadius = typeof BORDER_RADIUS[number];

export const Z_INDEX_LAYERS = ['base', 'dropdown', 'sticky', 'panel', 'modal', 'tooltip', 'command-palette', 'notification'] as const;
export type ZIndexLayer = typeof Z_INDEX_LAYERS[number];

// Component Specific
export const COMPONENT_SIZES = ['sm', 'md', 'lg'] as const;
export type ComponentSize = typeof COMPONENT_SIZES[number];

export const COMPONENT_VARIANTS = ['default', 'outline', 'ghost', 'brutal'] as const;
export type ComponentVariant = typeof COMPONENT_VARIANTS[number];

export const ComponentIntents = [...BRAND_COLORS, ...SEMANTIC_COLORS] as const;
export type ComponentIntent = typeof ComponentIntents[number];

/**
 * Convenience object exporting all design system constants
 */
export const TOKENS = {
	gray: GRAY_SCALE,
	brand: BRAND_COLORS,
	semantic: SEMANTIC_COLORS,
	states: MEMORY_STATES,
	urgency: REVISION_URGENCY,
	spacing: SPACING_TOKENS,
	typography: TYPOGRAPHY_SCALES,
	shadows: SHADOW_SIZES,
	radius: BORDER_RADIUS,
	z: Z_INDEX_LAYERS,
	sizes: COMPONENT_SIZES,
	variants: COMPONENT_VARIANTS
} as const;
