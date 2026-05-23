# Implementation Plan: Neo-Brutalist Design System

## Overview

This implementation plan breaks down the comprehensive neo-brutalist design system for the AI Memory Layer desktop application into discrete, manageable coding tasks. The system will be built using Tauri + SvelteKit + TailwindCSS with a focus on keyboard-first interactions, high information density, and developer-tool aesthetics.

The implementation follows a bottom-up approach: establishing design tokens and primitives first, then building composite components, and finally assembling feature-specific interfaces. Each task builds incrementally on previous work, ensuring continuous integration and validation.

## Tasks

- [x] 1. Project foundation and design token infrastructure
  - [x] 1.1 Initialize SvelteKit project with TypeScript and TailwindCSS
    - Create new SvelteKit project with TypeScript template
    - Install and configure TailwindCSS with PostCSS
    - Set up project structure: `src/lib/components/`, `src/lib/stores/`, `src/lib/styles/`, `src/lib/utils/`
    - Configure Vite for optimized chunking and build performance
    - Set up ESLint and Prettier for code quality
    - _Requirements: 15.1, 15.2, 15.3_

  - [x] 1.2 Create design token system with CSS custom properties
    - Create `src/lib/styles/tokens/core.css` with core tokens (colors, spacing, typography)
    - Create `src/lib/styles/tokens/semantic.css` with semantic tokens mapping core values to meaning
    - Create `src/lib/styles/tokens/component.css` with component-specific tokens
    - Define neutral gray palette (50-900) with 10 stops
    - Define brand colors (primary, secondary, accent) with restrained palette
    - Define semantic colors (success, warning, error, info) with light/base/dark variants
    - Define memory state colors (not-learned, learning, mastered, forgotten, revision-due)
    - Define revision urgency colors (low, medium, high, critical)
    - Define spacing scale (0-128px) based on 4px base unit
    - Define typography scale (xs-4xl) with 1.25 ratio
    - Define shadow values (sm, md, lg, xl)
    - Define border-radius values (none, sm, md, lg)
    - Define animation duration and easing values
    - Define z-index layers (base, dropdown, sticky, panel, modal, tooltip, command-palette, notification)
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.8, 2.9, 3.1, 15.1, 15.2, 15.3, 15.4, 15.5, 15.6_

  - [x] 1.3 Create TypeScript type definitions for design tokens
    - Create `src/lib/types/tokens.ts` with type definitions for all token categories
    - Define types for color tokens, spacing tokens, typography tokens
    - Define types for component variants and sizes
    - Export token constants for programmatic access
    - _Requirements: 15.7, 16.6_

  - [x] 1.4 Generate TailwindCSS configuration from design tokens
    - Create `tailwind.config.ts` extending default theme with custom tokens
    - Map CSS custom properties to Tailwind utilities
    - Configure content paths for component scanning
    - Add custom plugins for neo-brutalist utilities (hard shadows, strong borders)

  - [x]* 1.5 Set up Storybook for component documentation
    - Install and configure Storybook for SvelteKit
    - Create `.storybook/main.ts` and `.storybook/preview.ts` configuration
    - Set up Storybook addons: a11y, viewport, controls, docs
    - Create story template structure
    - _Requirements: 20.1, 20.2_

- [x] 2. Typography system implementation
  - [x] 2.1 Implement typography system with font stacks and scales
    - Create `src/lib/styles/typography.css` with font family definitions
    - Define system font stack for UI (sans-serif)
    - Define monospace font stack for code and data
    - Implement type scale classes (.text-xs through .text-4xl)
    - Implement font weight classes (.font-regular, .font-medium, .font-semibold, .font-bold)
    - Implement line-height classes (.leading-compact, .leading-normal, .leading-relaxed)
    - Implement letter-spacing adjustments for headings and labels
    - Create utility classes for editorial rhythm and vertical spacing
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8_

  - [x]* 2.2 Create typography documentation and examples
    - Create Storybook stories for typography system
    - Document font pairing guidelines
    - Document hierarchy usage patterns
    - Provide code examples for common typography patterns
    - _Requirements: 20.2, 20.3_

- [x] 3. Theme system architecture
  - [x] 3.1 Implement theme store and persistence
    - Create `src/lib/stores/themeStore.ts` with Svelte writable store
    - Implement theme state management (current theme, available themes)
    - Implement localStorage persistence with key `ai-memory-layer:theme`
    - Create theme switching function that updates CSS custom properties on `:root`
    - Implement reactive updates for theme changes
    - _Requirements: 14.1, 14.7, 14.8_

  - [x] 3.2 Create theme presets (dark, brutalist, monochrome, terminal)
    - Create `src/lib/themes/` directory with theme definition files
    - Implement dark theme with inverted color values
    - Implement brutalist theme with strong borders and hard shadows
    - Implement monochrome theme with grayscale palette
    - Implement terminal-inspired theme with retro aesthetics
    - Each theme modifies: spacing multipliers, border styles, typography mood, shadow intensity, interaction feel
    - _Requirements: 14.1, 14.2, 14.3, 14.4, 14.5, 14.6_

  - [x] 3.3 Implement density mode system
    - Add density mode support to theme store (compact, normal, comfortable)
    - Implement density multipliers (0.8x, 1.0x, 1.2x) for spacing
    - Create CSS custom property `--density-multiplier` that affects all spacing
    - Update component styles to use density-aware spacing
    - _Requirements: 3.2, 14.2_

- [x] 4. Layout primitive components
  - [x] 4.1 Create Stack layout component (vertical stacking)
    - Create `src/lib/components/layout/Stack.svelte`
    - Implement props: gap, align, justify, wrap
    - Support responsive gap values
    - Use flexbox with column direction
    - _Requirements: 16.1, 16.4_

  - [x] 4.2 Create Cluster layout component (horizontal grouping)
    - Create `src/lib/components/layout/Cluster.svelte`
    - Implement props: gap, align, justify, wrap
    - Support responsive gap values
    - Use flexbox with row direction
    - _Requirements: 16.1, 16.4_

  - [x] 4.3 Create Grid layout component
    - Create `src/lib/components/layout/Grid.svelte`
    - Implement props: columns, gap, minColumnWidth
    - Support responsive column counts
    - Use CSS Grid with auto-fit/auto-fill
    - _Requirements: 16.1, 16.4_

  - [x] 4.4 Create Sidebar layout component
    - Create `src/lib/components/layout/Sidebar.svelte`
    - Implement props: sidebarWidth, contentMinWidth, side (left/right)
    - Support responsive collapse behavior
    - _Requirements: 16.1, 16.4_

- [x] 5. Component primitives - Buttons and inputs
  - [x] 5.1 Implement Button component with variants
    - Create `src/lib/components/primitives/Button.svelte`
    - Implement TypeScript interface for ButtonProps (variant, size, disabled, loading, icon, iconPosition, fullWidth, type)
    - Implement variants: primary, secondary, ghost, danger, icon
    - Implement sizes: sm, md, lg
    - Implement interaction states: hover (translateY, shadow), focus (outline), active, disabled, loading
    - Add keyboard accessibility (Enter, Space)
    - _Requirements: 4.1, 4.7, 4.8_

  - [x]* 5.2 Create Button component tests and stories
    - Create Storybook stories for all button variants and states
    - Create unit tests for button interactions
    - Test keyboard navigation and accessibility
    - _Requirements: 20.1, 20.5_

  - [x] 5.3 Implement Input component
    - Create `src/lib/components/primitives/Input.svelte`
    - Implement TypeScript interface for InputProps (type, size, disabled, error, helperText, icon, iconPosition, placeholder, value)
    - Implement input types: text, email, password, search, url
    - Implement sizes: sm, md, lg
    - Implement states: default, hover, focus (border + shadow), error, disabled
    - Add ARIA labels and error announcements
    - _Requirements: 4.2, 4.7, 4.8, 18.1, 18.2_

  - [x] 5.4 Implement Select component
    - Create `src/lib/components/primitives/Select.svelte`
    - Implement TypeScript interface for SelectProps (options, value, placeholder, disabled, error, searchable, multiple)
    - Implement custom dropdown with keyboard navigation
    - Support searchable variant with fuzzy matching
    - Support multiple selection with chips
    - _Requirements: 4.2, 4.7, 4.8_

  - [x] 5.5 Implement Checkbox and Radio components
    - Create `src/lib/components/primitives/Checkbox.svelte`
    - Create `src/lib/components/primitives/Radio.svelte`
    - Implement TypeScript interfaces for CheckboxProps and RadioProps
    - Implement indeterminate state for Checkbox
    - Implement custom styling with neo-brutalist aesthetic
    - Add proper ARIA attributes and keyboard support
    - _Requirements: 4.2, 4.7, 4.8, 18.1_

  - [x] 5.6 Implement Toggle component
    - Create `src/lib/components/primitives/Toggle.svelte`
    - Implement TypeScript interface for ToggleProps (checked, disabled, size, label, labelPosition)
    - Implement smooth thumb animation (200ms ease-out)
    - Implement sizes: sm, md
    - Add ARIA switch role and keyboard support
    - _Requirements: 4.2, 4.7, 4.8, 18.1_

- [x] 6. Container and card components
  - [x] 6.1 Implement Card component with variants
    - Create `src/lib/components/primitives/Card.svelte`
    - Implement TypeScript interface for CardProps (variant, padding, hoverable, clickable)
    - Implement variants: flat, elevated, bordered, interactive (neo-brutalist with hard shadow)
    - Implement padding options: none, sm, md, lg
    - Implement interactive variant with transform and shadow animations
    - Support slot-based composition for header, body, footer
    - _Requirements: 4.3, 4.7, 4.8, 16.2, 16.4_

  - [x] 6.2 Create Panel and Section container components
    - Create `src/lib/components/layout/Panel.svelte`
    - Create `src/lib/components/layout/Section.svelte`
    - Implement consistent padding hierarchy (panel-outer, panel-inner)
    - Support collapsible sections with smooth animations
    - _Requirements: 3.5, 16.2, 16.4_

- [x] 7. Modal and overlay components
  - [x] 7.1 Implement Dialog component
    - Create `src/lib/components/primitives/Dialog.svelte`
    - Implement TypeScript interface for DialogProps (open, title, description, size, closeOnOverlayClick, closeOnEscape, showCloseButton)
    - Implement sizes: sm, md, lg, xl, full
    - Implement overlay with fade-in animation (200ms)
    - Implement content with slide-up animation (200ms)
    - Implement focus trapping within modal
    - Implement Escape key to close
    - Add ARIA dialog role and proper labeling
    - _Requirements: 4.5, 4.7, 4.8, 13.4, 13.7, 18.1_

  - [x] 7.2 Implement Drawer component
    - Create `src/lib/components/primitives/Drawer.svelte`
    - Implement TypeScript interface for DrawerProps (open, position, size, closeOnOverlayClick, closeOnEscape)
    - Implement positions: left, right, top, bottom
    - Implement slide-in animations based on position
    - Implement focus trapping and Escape key handling
    - _Requirements: 4.5, 4.7, 4.8, 13.4, 13.7_

  - [x] 7.3 Implement Popover component
    - Create `src/lib/components/primitives/Popover.svelte`
    - Implement TypeScript interface for PopoverProps (open, trigger, placement, offset, arrow)
    - Implement triggers: click, hover, focus
    - Implement auto-placement with collision detection
    - Implement arrow pointer with proper positioning
    - _Requirements: 4.5, 4.7, 4.8_

  - [x] 7.4 Implement Tooltip component
    - Create `src/lib/components/primitives/Tooltip.svelte`
    - Implement TypeScript interface for TooltipProps (content, placement, delay, arrow)
    - Implement placement options: top, bottom, left, right
    - Implement delay (default 300ms) before showing
    - Implement fade-in animation (100ms)
    - Add ARIA describedby for accessibility
    - _Requirements: 4.5, 4.7, 4.8, 18.1_

- [x] 8. Navigation components
  - [x] 8.1 Implement Tabs component
    - Create `src/lib/components/primitives/Tabs.svelte` (compound component)
    - Create TabsList, TabsTrigger, TabsContent sub-components
    - Implement keyboard navigation (Arrow keys, Home, End)
    - Implement ARIA tablist, tab, and tabpanel roles
    - Support horizontal and vertical orientations
    - _Requirements: 4.6, 4.7, 4.8, 13.3, 18.1_

  - [x] 8.2 Implement Breadcrumbs component
    - Create `src/lib/components/primitives/Breadcrumbs.svelte`
    - Implement separator customization
    - Implement max items with collapse behavior
    - Add ARIA navigation landmark and current page indicator
    - _Requirements: 4.6, 18.1_

  - [x] 8.3 Implement Pagination component
    - Create `src/lib/components/primitives/Pagination.svelte`
    - Implement page number buttons with ellipsis for large ranges
    - Implement previous/next navigation
    - Implement keyboard navigation (Arrow keys)
    - Add ARIA navigation role and page status announcements
    - _Requirements: 4.6, 13.3, 18.1_

- [x] 9. Data display components
  - [x] 9.1 Implement List components (simple, interactive, tree)
    - Create `src/lib/components/primitives/List.svelte`
    - Create `src/lib/components/primitives/InteractiveList.svelte` with hover and selection states
    - Create `src/lib/components/primitives/TreeList.svelte` with expand/collapse
    - Implement keyboard navigation (Arrow keys, Enter, Space)
    - Add ARIA list, listitem, and tree roles
    - _Requirements: 4.4, 4.7, 4.8, 13.3, 18.1_

  - [x] 9.2 Implement virtualized list for performance
    - Create `src/lib/components/primitives/VirtualList.svelte`
    - Integrate `svelte-virtual` library for virtualization
    - Support rendering 100+ items efficiently
    - Implement dynamic item heights
    - _Requirements: 4.4, 19.1_

  - [x] 9.3 Implement Table component with sorting and filtering
    - Create `src/lib/components/primitives/Table.svelte`
    - Implement table structure with header, body, footer slots
    - Implement sortable columns with visual indicators
    - Implement compact line-height for data density
    - Add ARIA table, row, columnheader, cell roles
    - _Requirements: 16.3, 18.1_

- [x] 10. Checkpoint - Core primitives complete
  - Ensure all tests pass, ask the user if questions arise.

- [x] 11. Workspace layout system
  - [x] 11.1 Implement layout state store
    - Create `src/lib/stores/layoutStore.ts` with Svelte writable store
    - Define WorkspaceLayout interface with sidebar, mainContent, auxiliaryPanel, bottomPanel, commandBar regions
    - Implement localStorage persistence with key `ai-memory-layer:layout`
    - Implement panel visibility, width/height, collapse states
    - Implement min/max constraints for panel sizes
    - _Requirements: 5.1, 5.2, 5.3, 5.7_

  - [x] 11.2 Create ResizablePanel component
    - Create `src/lib/components/layout/ResizablePanel.svelte`
    - Implement TypeScript interface for ResizablePanel (onResize, minSize, maxSize, defaultSize, collapsible, collapsedSize)
    - Implement mouse/touch drag handlers on panel dividers
    - Implement resize constraints and boundary checking
    - Implement smooth transitions (200ms) for collapse/expand
    - Persist sizes to layoutStore on resize end
    - Add visual feedback on hover (cursor change, divider highlight)
    - _Requirements: 5.3, 5.6_

  - [x] 11.3 Implement SplitView component
    - Create `src/lib/components/layout/SplitView.svelte`
    - Implement TypeScript interface for SplitView (orientation, ratio, minRatio, maxRatio, onRatioChange)
    - Support horizontal and vertical split orientations
    - Implement draggable divider with ratio adjustment
    - Persist split ratio to layoutStore
    - _Requirements: 5.4_

  - [x] 11.4 Create main workspace layout component
    - Create `src/lib/components/layout/WorkspaceLayout.svelte`
    - Implement sidebar region (200-400px, collapsible)
    - Implement main content area (flexible)
    - Implement auxiliary panel (300-600px, dockable: left/right/floating)
    - Implement bottom panel (200-600px, optional)
    - Implement command bar region at top
    - Wire all regions to layoutStore for state management
    - Implement panel transitions with 200ms cubic-bezier easing
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.6, 5.7, 5.8_

- [x] 12. Keyboard navigation system
  - [x] 12.1 Implement focus management store
    - Create `src/lib/stores/focusStore.ts` with Svelte writable store
    - Track current focus context (modal, panel, main content)
    - Implement focus trapping for modals and popovers
    - Implement focus restoration on modal close
    - _Requirements: 13.7_

  - [x] 12.2 Create keyboard shortcut system
    - Create `src/lib/utils/keyboard.ts` with keyboard event handling utilities
    - Implement global keyboard shortcut registration
    - Define shortcuts: Cmd/Ctrl+K (command palette), Cmd/Ctrl+F (search), Cmd/Ctrl+N (new memory)
    - Implement conflict detection for shortcut registration
    - Support customizable shortcuts with persistence
    - _Requirements: 13.1, 13.8_

  - [x] 12.3 Implement keyboard navigation utilities
    - Create `src/lib/utils/navigation.ts` with navigation helpers
    - Implement tab navigation through interactive elements
    - Implement arrow key navigation for lists, grids, trees
    - Implement Escape key handling for closing modals/popovers
    - Implement Enter key handling for confirming actions
    - _Requirements: 13.2, 13.3, 13.4, 13.5_

  - [x] 12.4 Add keyboard shortcut hints to components
    - Update Button, Dialog, and other components to display keyboard hints in tooltips
    - Create KeyboardHint component for displaying shortcuts
    - _Requirements: 13.6_

- [x] 13. Command Palette implementation
  - [x] 13.1 Create CommandPalette component
    - Create `src/lib/components/composite/CommandPalette.svelte`
    - Implement search input with instant focus
    - Implement fuzzy search with debounce (150ms)
    - Implement keyboard navigation (Arrow keys, Enter, Escape)
    - Implement result grouping by category
    - Implement result previews with metadata
    - Open with Cmd/Ctrl+K global shortcut
    - Implement z-index layering (--z-command-palette)
    - Add ARIA combobox role and live region for results
    - _Requirements: 5.5, 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.9, 13.1, 18.1, 18.2_

  - [x] 13.2 Create CommandPalette tests
    - Test search functionality and fuzzy matching
    - Test keyboard navigation
    - Test result filtering and ranking
    - _Requirements: 20.5_

- [x] 14. Semantic Search interface
  - [x] 14.1 Create SearchBar composite component
    - Create `src/lib/components/composite/SearchBar.svelte`
    - Implement search input with icon
    - Implement debounced input (150ms) to reduce computation
    - Implement clear button
    - Implement loading state indicator
    - _Requirements: 9.1, 19.3_

  - [x] 14.2 Create SearchResults component
    - Create `src/lib/components/composite/SearchResults.svelte`
    - Display results with context previews and highlighted search terms
    - Display metadata: source file, last modified date, relevance score
    - Implement keyboard navigation (Arrow keys, Enter)
    - Implement "no results" state with alternative suggestions
    - Display intelligent ranking indicators
    - _Requirements: 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.8_

  - [x] 14.3 Implement search filters
    - Create filter UI for metadata: subject, date range, file type, tags
    - Implement filter chips with remove functionality
    - Persist active filters to session storage
    - _Requirements: 9.4_

- [x] 15. Memory Graph visualization
  - [x] 15.1 Set up Canvas/WebGL rendering infrastructure
    - Create `src/lib/components/features/MemoryGraph.svelte`
    - Set up Canvas element with proper sizing and DPI handling
    - Implement WebGL context with fallback to Canvas 2D
    - Create rendering loop with requestAnimationFrame
    - _Requirements: 6.10_

  - [x] 15.2 Implement graph data structures and state
    - Create `src/lib/types/graph.ts` with MemoryNode, MemoryEdge, MemoryGraphState interfaces
    - Create `src/lib/stores/graphStore.ts` for graph state management
    - Implement viewport state (x, y, zoom)
    - Implement selection and hover state
    - Implement filter state (masteryRange, states, clusters)
    - _Requirements: 6.1, 6.2, 6.3_

  - [x] 15.3 Implement force-directed layout algorithm
    - Integrate D3-force simulation library
    - Configure link force (attraction between connected nodes)
    - Configure charge force (repulsion between all nodes)
    - Configure center force (centering)
    - Configure collision force (prevent overlap)
    - Configure cluster force (group related nodes)
    - Implement layout simulation with 60 FPS throttling
    - _Requirements: 6.8_

  - [x] 15.4 Implement node and edge rendering
    - Implement node rendering with size based on content volume (8-32px radius)
    - Implement node coloring based on mastery state (not-learned, learning, mastered, forgotten)
    - Implement edge rendering with weight-based stroke width (1-3px)
    - Implement label rendering with zoom-based visibility (show at zoom > 1.5)
    - Implement selection and hover visual feedback (stroke width, color)
    - _Requirements: 6.1, 6.2, 6.3_

  - [x] 15.5 Implement graph interactions (pan, zoom, hover, click)
    - Implement pan with mouse drag and touch drag
    - Implement zoom with mouse wheel and pinch gestures (0.1-5.0 range)
    - Implement node hover with tooltip display (300ms delay)
    - Implement node click for navigation to topic detail
    - Implement node double-click for expansion
    - Implement multi-select with Shift+Click
    - _Requirements: 6.4, 6.5, 6.6, 6.7_

  - [x] 15.6 Implement performance optimizations
    - Implement level-of-detail rendering based on zoom level
    - Implement viewport culling (only render visible nodes)
    - Implement spatial indexing (quadtree) for fast lookups
    - Implement batched rendering for nodes by state
    - Throttle hover events (100ms)
    - _Requirements: 6.10, 19.6_

  - [x] 15.7 Implement semantic cluster visualization
    - Implement cluster boundary rendering with subtle background regions
    - Implement cluster labels
    - Implement cluster-based filtering
    - _Requirements: 6.9_

- [x] 16. Checkpoint - Graph visualization complete
  - Ensure all tests pass, ask the user if questions arise.

- [x] 17. Recall Dashboard implementation
  - [x] 17.1 Create dashboard layout structure
    - Create `src/lib/components/features/RecallDashboard.svelte`
    - Implement dashboard header with streak and topics due
    - Implement grid layout for dashboard widgets
    - Implement responsive layout for different screen sizes
    - _Requirements: 7.1, 7.2_

  - [x] 17.2 Implement Forgotten Topics list
    - Create ForgottenTopicCard component
    - Display topics sorted by revision urgency
    - Implement urgency color coding (low, medium, high, critical)
    - Implement actions: review, dismiss, view details
    - _Requirements: 7.1, 7.6_

  - [x] 17.3 Implement Activity Heatmap visualization
    - Create ActivityHeatmap component
    - Display 12 months of daily review activity
    - Implement color intensity mapping (0-1 scale)
    - Implement hover tooltips with date and review count
    - Implement day/week/month navigation
    - _Requirements: 7.3_

  - [x] 17.4 Implement Mastery Evolution chart
    - Create MasteryEvolutionChart component using chart library (Chart.js or D3)
    - Display line chart showing mastery progress over time
    - Support multiple topics with color-coded lines
    - Implement interactive legend for toggling topics
    - Implement zoom and pan for time range
    - _Requirements: 7.4, 7.8_

  - [x] 17.5 Implement Memory Decay curve visualization
    - Create MemoryDecayChart component
    - Display decay curves with predicted forgetting dates
    - Implement current retention indicator
    - Implement predicted retention timeline
    - Use scientific aesthetics avoiding gamification
    - _Requirements: 7.5, 7.9_

  - [x] 17.6 Implement dashboard filtering
    - Create filter controls for subject, date range, mastery level
    - Implement filter state management
    - Update all dashboard widgets based on active filters
    - _Requirements: 7.7_

- [x] 18. AI Recall Interface implementation
  - [x] 18.1 Create AI Recall Interface layout
    - Create `src/lib/components/features/AIRecallInterface.svelte`
    - Implement document-style layout (not chat bubbles)
    - Implement memory chunk display with source attribution
    - Implement relevance score indicators
    - _Requirements: 8.1, 8.4_

  - [x] 18.2 Implement memory chunk expansion
    - Create MemoryChunk component with expandable content
    - Implement inline expansion to show full context
    - Implement smooth expand/collapse animations
    - _Requirements: 8.2_

  - [x] 18.3 Implement semantic references and citations
    - Display citations as footnotes or inline references
    - Implement linked topics that navigate to related content
    - Implement confidence scores for retrieved information
    - _Requirements: 8.3, 8.5, 8.7_

  - [x] 18.4 Implement keyboard navigation for chunks
    - Implement arrow key navigation between chunks
    - Implement Enter to expand/collapse
    - Implement Tab to navigate actions
    - _Requirements: 8.6, 13.3_

  - [x] 18.5 Implement chunk actions
    - Implement "Explain differently" action
    - Implement "Show related" action
    - Implement copy to clipboard action
    - _Requirements: 8.8_

- [x] 19. Spaced Repetition UI implementation
  - [x] 19.1 Create review card component
    - Create `src/lib/components/features/ReviewCard.svelte`
    - Display topic content with context and source attribution
    - Implement clean, scientific aesthetic (no gamification)
    - _Requirements: 10.1, 10.6_

  - [x] 19.2 Implement self-assessment actions
    - Create assessment buttons: "Forgot", "Hard", "Good", "Easy"
    - Implement keyboard shortcuts (1, 2, 3, 4)
    - Display next review date after assessment
    - _Requirements: 10.2, 10.3, 10.4_

  - [x] 19.3 Implement review session progress
    - Create progress indicator showing cards remaining
    - Display session statistics (cards reviewed, time spent)
    - Implement session completion summary
    - _Requirements: 10.5_

  - [x] 19.4 Implement weak-topic recovery suggestions
    - Detect repeated failures on same topic
    - Display recovery suggestions with related topics
    - Implement concept reinforcement mode
    - _Requirements: 10.7, 10.8_

- [x] 20. Analytics and visualization components
  - [x] 20.1 Create chart component library
    - Create `src/lib/components/charts/LineChart.svelte`
    - Create `src/lib/components/charts/BarChart.svelte`
    - Create `src/lib/components/charts/Heatmap.svelte`
    - Create `src/lib/components/charts/ProgressRing.svelte`
    - Use editorial aesthetics inspired by data journalism
    - Implement accessible color palettes for colorblind users
    - _Requirements: 7.8, 11.1, 11.2, 11.3, 11.4, 11.5, 11.6, 11.8_

  - [x] 20.2 Implement memory strength visualization
    - Create MemoryStrengthChart component
    - Display time-series data for selected topics
    - Implement interactive tooltips with detailed metrics
    - _Requirements: 11.1_

  - [x] 20.3 Implement cognitive load indicators
    - Create CognitiveLoadIndicator component
    - Display daily review burden metrics
    - Implement visual indicators for overload warnings
    - _Requirements: 11.3_

  - [x] 20.4 Implement topic retention heatmap
    - Create TopicRetentionHeatmap component
    - Display strong and weak areas across topics
    - Implement interactive filtering and drill-down
    - _Requirements: 11.4_

  - [x] 20.5 Implement revision efficiency metrics
    - Create RevisionEfficiencyChart component
    - Display time invested vs mastery gained
    - Implement comparison across topics
    - _Requirements: 11.5_

  - [x] 20.6 Add chart export functionality
    - Implement PNG export for all chart components
    - Implement SVG export for vector graphics
    - Add export button to chart toolbars
    - _Requirements: 11.7_

- [x] 21. Motion and animation system
  - [x] 21.1 Create animation utilities
    - Create `src/lib/utils/animations.ts` with animation helpers
    - Define animation duration constants (instant: 0ms, fast: 100ms, normal: 200ms, slow: 300ms)
    - Define easing function constants (ease-in, ease-out, ease-in-out)
    - Create transition utility functions
    - _Requirements: 12.1, 12.2_

  - [x] 21.2 Implement component animations
    - Apply fast (100ms) transitions to hover states
    - Apply normal (200ms) transitions to panel open/close
    - Apply slow (300ms) transitions to page navigation
    - Implement fade-in animations for viewport entries (200ms)
    - _Requirements: 12.3, 12.4, 12.5, 12.6_

  - [x] 21.3 Implement reduced-motion support
    - Detect prefers-reduced-motion media query
    - Disable non-essential animations when reduced-motion is preferred
    - Maintain essential feedback animations (focus indicators)
    - _Requirements: 12.8_

- [x] 22. Accessibility implementation
  - [x] 22.1 Add ARIA labels and roles to all components
    - Audit all components for missing ARIA attributes
    - Add aria-label, aria-labelledby, aria-describedby where needed
    - Add proper role attributes (button, dialog, navigation, etc.)
    - Add aria-live regions for dynamic content updates
    - _Requirements: 18.1, 18.2_

  - [x] 22.2 Implement skip-to-content links
    - Create skip navigation component
    - Add skip links to main content, navigation, search
    - Style skip links to be visible on focus
    - _Requirements: 18.4_

  - [x] 22.3 Implement high contrast mode support
    - Detect Windows High Contrast Mode
    - Override colors with system colors when active
    - Test all components in high contrast mode
    - _Requirements: 18.3_

  - [x] 22.4 Ensure minimum touch target sizes
    - Audit all interactive elements for size
    - Ensure minimum 44x44px touch targets
    - Add padding where needed to meet requirements
    - _Requirements: 18.5_

  - [x] 22.5 Add text alternatives for non-text content
    - Add alt text for all images
    - Add aria-label for icon-only buttons
    - Add captions for data visualizations
    - _Requirements: 18.6_

  - [x] 22.6 Test browser zoom support
    - Test all layouts at 200% zoom
    - Fix any layout breaks or content overflow
    - Ensure functionality remains intact
    - _Requirements: 18.7_

  - [x] 22.7 Run accessibility audit
    - Run automated accessibility tests with axe-core
    - Test with screen readers (NVDA, JAWS, VoiceOver)
    - Document accessibility testing results
    - _Requirements: 20.5_

- [x] 23. Responsive layout implementation
  - [x] 23.1 Implement responsive breakpoint system
    - Configure Tailwind breakpoints (sm, md, lg, xl, 2xl, 3xl)
    - Create responsive utility classes
    - Test layouts at all breakpoints
    - _Requirements: 3.7, 17.1, 17.2_

  - [x] 23.2 Implement adaptive panel behavior
    - Collapse auxiliary panels below 1280px viewport width
    - Adjust content max-width above 1920px
    - Implement responsive font sizes for high-DPI displays
    - _Requirements: 17.3, 17.4, 17.6_

  - [x] 23.3 Implement multi-monitor support
    - Persist window state (position, size) to localStorage
    - Restore window state on application launch
    - Handle window movement between monitors
    - _Requirements: 17.5_

- [ ] 24. Performance optimization
  - [ ] 24.1 Implement lazy loading for components
    - Identify heavy components for lazy loading
    - Implement dynamic imports with Svelte's lazy loading
    - Add loading states for lazy-loaded components
    - _Requirements: 19.2_

  - [ ] 24.2 Implement code splitting
    - Configure Vite for optimal code splitting
    - Split routes into separate chunks
    - Split large feature components into separate chunks
    - _Requirements: 19.5_

  - [ ] 24.3 Optimize animations for GPU acceleration
    - Use CSS transforms instead of position properties
    - Use will-change for animated elements
    - Remove will-change after animations complete
    - _Requirements: 19.4_

  - [ ] 24.4 Optimize bundle size
    - Analyze bundle with vite-bundle-visualizer
    - Remove unused dependencies
    - Tree-shake unused code
    - Minimize JavaScript bundle size
    - _Requirements: 19.5_

  - [ ] 24.5 Measure and optimize performance metrics
    - Implement performance monitoring
    - Measure First Contentful Paint (FCP)
    - Optimize to achieve FCP under 1.5 seconds
    - _Requirements: 19.7_

- [ ] 25. Documentation and Storybook completion
  - [ ] 25.1 Complete Storybook stories for all components
    - Create stories for all primitive components
    - Create stories for all composite components
    - Create stories for all feature components
    - Document all component variants and states
    - _Requirements: 20.1_

  - [ ] 25.2 Create component usage guidelines
    - Document do's and don'ts for each component
    - Provide best practices for composition
    - Document accessibility considerations
    - _Requirements: 20.2_

  - [ ] 25.3 Create design token documentation
    - Document all design tokens with visual examples
    - Create token reference guide
    - Document theme customization process
    - _Requirements: 20.6_

  - [ ] 25.4 Create code examples for common patterns
    - Document common layout patterns
    - Document form patterns
    - Document navigation patterns
    - Document data display patterns
    - Provide TypeScript examples for all patterns
    - _Requirements: 20.3, 16.7_

  - [ ]* 25.5 Set up visual regression testing
    - Configure visual regression testing with Playwright or Chromatic
    - Create baseline screenshots for all components
    - Set up CI pipeline for visual regression tests
    - _Requirements: 20.4_

- [ ] 26. Final integration and polish
  - [ ] 26.1 Create demo application
    - Build demo app showcasing all components
    - Implement example workflows (search, review, analytics)
    - Test all interactions and keyboard shortcuts
    - _Requirements: 20.1_

  - [ ] 26.2 Conduct cross-browser testing
    - Test in Chrome, Firefox, Safari, Edge
    - Fix browser-specific issues
    - Document browser compatibility
    - _Requirements: 18.7_

  - [ ] 26.3 Optimize for production build
    - Configure production build settings
    - Enable minification and compression
    - Test production build performance
    - _Requirements: 19.5, 19.7_

  - [ ] 26.4 Create migration guide
    - Document breaking changes (if any)
    - Provide migration examples
    - Document version compatibility
    - _Requirements: 20.7_

- [ ] 27. Final checkpoint - Design system complete
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation at major milestones
- The implementation follows a bottom-up approach: tokens → primitives → composites → features
- All components use TypeScript for type safety
- All components follow Svelte 5 best practices with slot-based composition
- Accessibility is built-in from the start, not added later
- Performance optimizations are applied throughout, not just at the end
- The design system is framework-agnostic at the token level, making it portable


## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "1.5"] },
    { "id": 1, "tasks": ["1.2", "1.3"] },
    { "id": 2, "tasks": ["1.4", "2.1", "3.1"] },
    { "id": 3, "tasks": ["2.2", "3.2", "3.3", "4.1", "4.2", "4.3", "4.4"] },
    { "id": 4, "tasks": ["5.1", "5.3", "5.4", "5.5", "5.6", "6.1"] },
    { "id": 5, "tasks": ["5.2", "6.2", "7.1", "7.2", "7.3", "7.4", "8.1", "8.2", "8.3"] },
    { "id": 6, "tasks": ["9.1", "9.2", "9.3"] },
    { "id": 7, "tasks": ["11.1"] },
    { "id": 8, "tasks": ["11.2", "11.3", "12.1", "12.2"] },
    { "id": 9, "tasks": ["11.4", "12.3", "12.4"] },
    { "id": 10, "tasks": ["13.1", "14.1"] },
    { "id": 11, "tasks": ["13.2", "14.2", "14.3", "15.1"] },
    { "id": 12, "tasks": ["15.2"] },
    { "id": 13, "tasks": ["15.3"] },
    { "id": 14, "tasks": ["15.4"] },
    { "id": 15, "tasks": ["15.5", "15.6", "15.7"] },
    { "id": 16, "tasks": ["17.1"] },
    { "id": 17, "tasks": ["17.2", "17.3", "17.4", "17.5", "17.6", "18.1", "19.1", "20.1"] },
    { "id": 18, "tasks": ["18.2", "18.3", "18.4", "18.5", "19.2", "19.3", "19.4", "20.2", "20.3", "20.4", "20.5"] },
    { "id": 19, "tasks": ["20.6", "21.1"] },
    { "id": 20, "tasks": ["21.2", "21.3", "22.1", "23.1"] },
    { "id": 21, "tasks": ["22.2", "22.3", "22.4", "22.5", "22.6", "22.7", "23.2", "23.3", "24.1"] },
    { "id": 22, "tasks": ["24.2", "24.3", "24.4"] },
    { "id": 23, "tasks": ["24.5", "25.1", "25.2", "25.3", "25.4", "25.5"] },
    { "id": 24, "tasks": ["26.1", "26.2"] },
    { "id": 25, "tasks": ["26.3", "26.4"] }
  ]
}
```
