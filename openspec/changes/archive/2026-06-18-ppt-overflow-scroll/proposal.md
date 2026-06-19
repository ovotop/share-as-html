## Why

In PPT mode, slides containing oversized content (large Mermaid diagrams, tall images) overflow the 100vh viewport. Currently ArrowDown immediately jumps to the next slide via `navigateSlide(1)`, making the lower portion of the content unreadable without entering Zoom mode. This breaks the natural expectation that ArrowDown scrolls visible content before advancing.

## What Changes

- **ArrowDown in PPT_FULL mode**: When the current slide has content taller than the viewport AND the content has not been scrolled to the bottom, ArrowDown smooth-scrolls within the slide instead of advancing to the next slide
- **Bounce animation**: When scroll reaches the bottom boundary, a brief ease-out bounce signals "end of content"
- **Two-press advance**: After reaching the bottom, the next ArrowDown press (key-up then key-down) advances to the next slide
- **ArrowUp symmetry**: Same scroll-within-slide behavior for ArrowUp when content is taller than viewport
- **scroll-snap relaxation**: Switch `#scroll-container.mode-ppt` from `scroll-snap-type: y mandatory` to `y proximity` to allow partial scroll positions within a slide

## Capabilities

### New Capabilities

- `ppt-slide-internal-scroll`: Arrow keys scroll within oversized slide content before advancing to adjacent slides, with bounce feedback at boundaries

### Modified Capabilities

<!-- No existing specs to modify -->

## Impact

- **CSS**: `.mode-ppt` scroll-container snap behavior changes from `mandatory` to `proximity`; slides with overflow get `overflow-y: auto` + `max-height: 100vh`
- **JS**: PPT_FULL keyboard handler gains scroll-within-slide logic modeled on existing `scrollZoomContainer()` pattern; new `getSlideScrollBounds()` helper
- **HTML template**: SKILL.md CSS + JS templates must be updated; all existing test HTML files must be regenerated
- **No breaking changes**: Behavior change is additive — slides that fit within viewport behave identically to before
