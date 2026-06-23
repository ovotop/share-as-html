## Context

PPT_ZOOM mode currently clones focused content into a fixed full-viewport `.zoom-container` with flexbox centering and `overflow: auto`. The content renders at its natural size — small images are centered with wasted space, large ones require scrolling. This change adds image-viewer-style controls: fit/fill toggle and stepped zoom scale.

## Goals / Non-Goals

**Goals:**
- Enter zoom: default to fit-viewport ("内接") — see the full picture, fixed at 1.0×
- Fill mode: dynamically compute the scale needed to fill the viewport, clamped to [1.25, 3.0]
- `Enter` quick-toggles between fit (1.0×) and the fill step
- `+` / `-` step along a unified scale line that includes the fit anchor at 1.0 and the computed fill step
- Scale line auto-dedupes when fill step coincides with a preset step
- Arrow keys scroll within zoom content only — never exit zoom or navigate slides
- Works for all content types

**Non-Goals:**
- No mouse/scroll-wheel zoom
- No visual scale indicator
- No per-element scale memory
- No 0 reset key
- No scale below 1.0×

## Decisions

### Decision 1: Unified scale line — fit/fill merged into one dimension

**Choice**: Fit and fill are NOT orthogonal controls. They are positions on a single unified scale line. The user navigates the line linearly with `+`/`-`. Rendering mode (fit CSS vs fill CSS) is derived from position: at or below the fill step → fill mode; otherwise → fit mode.

```
Unified scale line (dynamic):

  fit 1.0  ─ [1.25] ─ [1.5] ─ fill@2.4 ─ [3.0]
   ↑                                      ↑
   fit mode                               fill mode
   (max-width/max-height)                 (width/height + object-fit)

The fill step is computed from content natural dimensions and inserted
into the preset sequence [1.0, 1.25, 1.5, 2.0, 3.0]. Duplicates are removed.
```

Why: Two orthogonal controls (toggle + scale) create a confusing mental model where the user must understand two independent axes. A single scale line is simpler — one dimension, linear navigation.

### Decision 2: Default to fit-viewport on entry

**Choice**: `enterZoomMode()` sets `--zoom-scale: 1.0`, content constrained to fit viewport.

### Decision 3: Dynamic scale line with fill step

**Choice**: The scale line is not a static array. It is built at `enterZoomMode()` time by computing the fill scale (`fillX`) from the content's natural dimensions and inserting it into the base sequence.

**Computation:**
```js
fillX = Math.max(viewportWidth / natWidth, viewportHeight / natHeight)
fillX = Math.max(1.25, Math.min(3.0, fillX))  // clamp [1.25, 3.0]
```

**Sequence construction:**
```js
const sorted = [...BASE, fillX].sort((a, b) => a - b);
const steps = sorted.filter((x, i, arr) =>
    i === 0 || Math.abs(x - arr[i - 1]) > 0.01
);
```

**Why clamp floor at 1.25:** If fillX < 1.25 (e.g., content almost fills viewport, fillX ≈ 1.08), the fill step is visually indistinguishable from fit 1.0. Flooring to 1.25 ensures a meaningful perceptual jump.

**Why clamp cap at 3.0:** If fillX > 3.0 (e.g., tiny image needs 9.6× to fill viewport), the content would be extremely pixelated. 3.0 is a practical maximum — content already fills most of the screen.

**Examples:**
| Content (natW × natH) | fillX (raw) | After clamp | Scale line |
|---|---|---|---|
| 1200 × 800 | 1.6 | 1.6 | [1.0, 1.25, 1.5, 1.6, 2.0, 3.0] |
| 1920 × 1080 | 1.0 | 1.25 | [1.0, 1.25, 1.5, 2.0, 3.0] (1.25 deduped) |
| 400 × 300 | 4.8 | 3.0 | [1.0, 1.25, 1.5, 2.0, 3.0] (3.0 deduped) |
| 2500 × 1500 | 0.77 | 1.25 | [1.0, 1.25, 1.5, 2.0, 3.0]

### Decision 4: CSS

```css
/* Default: fit */
body.mode-zoom .zoom-content {
    max-width: calc(var(--zoom-scale, 1) * 100vw);
    max-height: calc(var(--zoom-scale, 1) * 100vh);
}
/* Fill mode */
body.mode-zoom .zoom-content.fill {
    width: calc(var(--zoom-scale, 1) * 100vw);
    height: calc(var(--zoom-scale, 1) * 100vh);
    object-fit: cover; max-width: none; max-height: none;
}
```

### Decision 5: Keyboard

| Key | Action |
|-----|--------|
| Escape | Exit zoom |
| Enter | Quick toggle: fit (1.0) ↔ nearest fill step |
| `+` / `=` | Step to next scale in line |
| `-` | Step to previous scale in line |
| Arrow | Scroll within zoom content — never exit zoom, never navigate slides |

**Arrow keys rationale:** Allowing Arrow keys to exit zoom and navigate slides creates complex edge cases (at boundary: should it scale up? exit? switch mode?). Locking the user in zoom simplifies the mental model: zoom is a self-contained viewer — Escape to leave, +/-/Enter to adjust view. If the user wants to navigate to the next slide, they press Escape first.

### Decision 6: zoomScale tracks the current step, fill class derived from position

**Choice**: `zoomScale` stores the current step's scale value (a number from the dynamic scale line). The `.fill` class is toggled by comparing current step to the fit anchor:

```js
function applyZoomScale() {
    el.style.setProperty('--zoom-scale', zoomScale);
    el.classList.toggle('fill', zoomScale >= fillStepScale);
}
```

At scale 1.0 (fit anchor), `--zoom-scale` is 1.0 and `.fill` is absent — the fit CSS rules apply (`max-width`/`max-height` constrained). At or above the fill step, `.fill` is present — the fill CSS rules apply (`width`/`height` + `object-fit: cover`).

### Decision 7: Enter quick-toggles between fit anchor and fill step

**Choice**: Enter is NOT a full toggle through all states. It is a binary shortcut:
- If currently at fit (1.0) → jump to fill step
- If currently at any fill step → jump back to fit (1.0)

This gives the user a fast "show me the full picture" / "fill the screen" shortcut without stepping through intermediate scales.

## Risks

- **[Risk] Default fit changes existing behavior** → Mitigation: More useful default — full picture visible immediately.
- **[Risk] Fill mode crops edges** → Mitigation: Standard UX, Enter is instant toggle.
