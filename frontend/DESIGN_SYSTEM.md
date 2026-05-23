# AI Memory Layer - Design System Documentation

Welcome to the design system blueprint for the **AI Memory Layer App**. This system relies on a high-contrast, robust **Neo-Brutalist** visual aesthetic combined with modern, motion-safe interactions.

---

## 1. Design Tokens Reference

Our core design tokens are defined in `core.css` and mapped to Tailwind configuration tokens.

### Color System
* **Monochrome Palette**: Custom stark neutrals representing flat layouts.
  * `--color-gray-50`: `#fafafa` (surface highlighting)
  * `--color-gray-100`: `#f4f4f5` (main cards/panels background)
  * `--color-gray-200`: `#e4e4e7` (borders and subtler separators)
  * `--color-gray-800`: `#27272a` (stark borders)
  * `--color-gray-900`: `#18181b` (monochrome shadows and text)
* **Brutalist Brand Accent System**: High contrast, fully saturated values.
  * `--color-primary`: `#2563eb` (Royal Blue)
  * `--color-secondary`: `#7c3aed` (Electric Purple)
  * `--color-accent`: `#db2777` (Deep Pink)

### Spacing & Grid Scale
All spacing scales are based on a 4px grid system:
* `xs`: `0.25rem` (4px)
* `sm`: `0.5rem` (8px)
* `md`: `1rem` (16px)
* `lg`: `1.5rem` (24px)
* `xl`: `2rem` (32px)
* `2xl`: `3rem` (48px)

### Borders & Shadows
* **Brutalist Border**: `.brutal-border`
  * `border: 4px solid var(--color-gray-900);`
* **Brutalist Shadow**:
  * Small: `2px 2px 0px rgba(0,0,0,1)`
  * Medium: `4px 4px 0px rgba(0,0,0,1)`
  * Large: `8px 8px 0px rgba(0,0,0,1)`

---

## 2. Component Usage Guidelines

### Button (`Button.svelte`)
* **Do's**: Use for triggers and active page events. Ensure size fits context (use `sm` for mini headers, `md` default, `lg` for hero calls).
* **Don'ts**: Do not overload forms with multiple contrasting "Primary" variants.
* **Accessibility**: Handles touch targets automatically via the `.touch-target-extend` utility, ensuring minimum dimensions of 44x44px.

### Card (`Card.svelte`)
* **Do's**: Package clean contextual sections. Keep shadow sizes aligned to component weight (smaller cards get `2px` shadow, larger blocks get `4px` or `8px`).
* **Accessibility**: Use appropriate headings within the card layout to maintain correct document outlines.

### SearchFilters (`SearchFilters.svelte`)
* **Do's**: Leverage to filter query listings dynamically.
* **Composition**: Always bind state using Svelte 5 `$bindable` bindings to maintain reactive form inputs.

---

## 3. Common Code Patterns

### Grid Layout Layouts
Below is the standard, responsive Neo-Brutalist grid wrapper pattern for dashboard pages:

```svelte
<div class="grid grid-cols-1 xl:grid-cols-12 gap-8">
    <!-- Secondary/Side Column (4 cols) -->
    <div class="xl:col-span-4 flex flex-col gap-4">
        <h3 class="font-black text-xl uppercase">Secondary Controls</h3>
        <div class="brutal-border bg-surface-primary p-4">
            <!-- Sidebar content -->
        </div>
    </div>

    <!-- Main Content Column (8 cols) -->
    <div class="xl:col-span-8 flex flex-col gap-8">
        <section class="bg-surface-primary brutal-border p-6 shadow-md">
            <!-- Central Chart/D3 Graph -->
        </section>
    </div>
</div>
```

### Dynamic Lazy Loading Components
To avoid initial page render blocks on heavy components (like graphs or map visualizers):

```svelte
<script lang="ts">
    let LazyComponent = $state<any>(null);

    $effect(() => {
        import('./HeavyComponent.svelte').then(m => LazyComponent = m.default);
    });
</script>

{#if LazyComponent}
    <LazyComponent />
{:else}
    <div class="animate-pulse bg-surface-secondary h-48 w-full flex items-center justify-center">
        <span>Loading...</span>
    </div>
{/if}
```

### GPU-Accelerated Animations
Always use the `gpuAccelerated` action on container components undergoing transitions:

```svelte
<script lang="ts">
    import { motionSlide, gpuAccelerated } from '$lib/utils/animations';
    let visible = $state(true);
</script>

{#if visible}
    <div transition:motionSlide use:gpuAccelerated class="p-4 brutal-border">
        Accelerated animation block.
    </div>
{/if}
```
