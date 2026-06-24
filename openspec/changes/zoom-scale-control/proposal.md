## Why

PPT_ZOOM mode currently displays zoomed content at its cloned natural size — small images sit centered in a sea of empty space, large ones require excessive scrolling. Users have no control over how content fills the screen. Arrow keys at scroll boundaries unexpectedly exit zoom and navigate slides, causing confusion.

## What Changes

- **Unified scale line**: fit and fill are positions on a single dimension, not orthogonal controls. `fillStep` is dynamically computed from content dimensions. Fill class is derived from scale position, not manually toggled.
- **Enter zoom default**: fit-viewport (1.0×) — see the full picture immediately.
- **`Enter` quick-toggle**: binary jump between fit anchor (1.0) and the computed fill step. No intermediate steps.
- **`+` / `-` stepped zoom**: navigate the dynamic scale line linearly. Scale ≥ fillStep automatically applies fill rendering.
- **Arrow keys locked in zoom**: scroll within content only. Never exit zoom, never navigate slides. Boundary reach plays bounce animation. Escape is the only exit.
- **ArrowLeft/Right boundary detection**: properly capped (currently hardcoded `return true`).
- Works for ALL zoomable content: images, mermaid SVGs.

## Capabilities

### New Capabilities

- `zoom-scale-control`: Unified scale line with dynamic fill-step computation. Arrow keys locked to zoom container (no exit/navigate). Enter = fit ↔ fillStep binary jump. `+`/`-` step along dynamic scale line.

### Modified Capabilities

<!-- None — zoom behavior has no existing openspec spec -->

## Impact

- **CSS**: `body.mode-zoom .zoom-container` bounce animation class; existing `.zoom-content` rules unchanged
- **JavaScript**: `enterZoomMode()` (dynamic scale line construction + layout timing), `exitZoomMode()`, `applyZoomScale()` (derive fill from position), `scrollZoomContainer()` (boundary detection), keyboard handler PPT_ZOOM case (Arrow = scroll only, Enter = binary jump)
- **Documentation**: Keyboard shortcut table in SKILL.md
- **No impact**: DOC mode, PPT_FULL focus system, state machine transitions, image slide layout
