## Context

The sharing-in-html PPT mode uses CSS scroll-snap (`y mandatory`) + JS keyboard interception to navigate between slides. In PPT mode, `#scroll-container` is `height: 100vh; overflow-y: scroll` with `scroll-snap-type: y mandatory`. Each `.slide` has `min-height: 100vh; scroll-snap-align: start; scroll-snap-stop: always`.

When a slide contains a large Mermaid diagram that renders taller than 100vh, the content overflows visually. However, pressing ArrowDown calls `navigateSlide(1)` unconditionally — immediately snapping to the next slide. The lower portion of the diagram becomes inaccessible without entering Zoom mode (Enter key).

The existing ZOOM mode (`PPT_ZOOM` state) already implements the pattern we need: `scrollZoomContainer(direction)` scrolls zoomed content, returns `false` at boundaries, and only then transitions slides. This design adapts that proven pattern to PPT_FULL.

## Goals / Non-Goals

**Goals:**
- ArrowDown in PPT_FULL mode scrolls within oversized slides before advancing
- ArrowLeft/ArrowRight in PPT_FULL mode scrolls horizontally within wide content before switching focus
- Smooth scroll animation (not instant jump)
- Bounce feedback when scroll reaches the slide boundary (vertical or horizontal)
- Two-press model: reaching boundary on press 1 triggers bounce; press 2 advances (vertical) or switches focus (horizontal)
- ArrowUp has symmetric scroll-within-slide behavior
- Slides that fit within viewport behave identically to current behavior

**Non-Goals:**
- Scroll within slides in DOC mode (free scroll already works)
- Auto-entering Zoom mode for oversized content (out of scope; use existing Enter key)
- Touch/swipe gesture handling (keyboard-only)

## Decisions

### Decision 1: Relax scroll-snap to `proximity` instead of `mandatory`

| Approach | Pros | Cons |
|----------|------|------|
| **`y proximity`** (chosen) | Allows partial scroll positions naturally; browser handles snap physics | Less aggressive snap at boundaries |
| `y mandatory` + JS scroll | Exact control | Browser fights JS scroll positioning |
| Inner scrollable wrapper in slides | Snap stays precise | Complex HTML changes; breaks existing slide structure |

**Rationale**: `mandatory` forces the browser to always land on a snap point — any mid-slide scrolling is immediately undone. `proximity` snaps when close to a boundary but allows intermediate positions, which is the exact UX we want.

### Decision 2: JS-driven smooth scroll, not native keyboard scroll

The current handler calls `e.preventDefault()` on all ArrowDown events in PPT_FULL. We keep this pattern and implement smooth scrolling via `container.scrollBy({ top, behavior: 'smooth' })`. This gives us:

- Consistent scroll step size (80% viewport height)
- Full control over boundary detection
- Ability to trigger bounce animation at exact boundaries
- No interference from browser's default scroll behavior

### Decision 3: `isAtScrollBoundary` flag for two-press advance

The user explicitly wants: press 1 reaches bottom → bounce → stop; press 2 → advance. A single boolean flag tracks this:

```
ArrowDown pressed:
  if isAtScrollBoundary → navigateSlide(+1), reset flag
  elif canScrollDown → smooth scroll, if now at bottom: set flag + bounce
  else (slide fits viewport, no overflow) → navigateSlide(+1)
```

The flag resets on: slide change, ArrowUp scroll (moving away from boundary).

### Decision 4: Bounce via temporary CSS animation class

Add `@keyframes slide-bounce-down` and `slide-bounce-up` animations. Apply the class to `#scroll-container` for 300ms then remove. This is non-blocking (no `setTimeout` delay on navigation) and uses GPU-accelerated `transform`.

### Decision 5: ArrowLeft/ArrowRight horizontal scroll with focus-switch priority

Currently ArrowLeft/ArrowRight in PPT_FULL calls `handleFocusSwitch()` to cycle through `diagram-focusable` elements on the current slide. When a focused diagram is wider than the viewport (e.g., 1500px placeholder image in `test-image-zoom.html`), the user has no way to horizontally scroll it.

The new behavior:

```
ArrowRight pressed:
  if focused diagram's content overflows horizontally AND not at right boundary
    → horizontal smooth scroll within scroll-container
    → if now at boundary: set flag + horizontal bounce
  elif isAtScrollBoundary AND multiple focusables exist
    → handleFocusSwitch (switch to next diagram)
  elif isAtScrollBoundary (single focusable or already cycled through all)
    → do nothing (all content viewed, all focusables cycled)
  else (no horizontal overflow)
    → handleFocusSwitch (current behavior preserved)
```

ArrowLeft is symmetric. The `isAtScrollBoundary` flag is shared between vertical and horizontal — it always resets when scroll direction changes or slide changes.

## Risks / Trade-offs

- **[Risk] `scroll-snap-type: proximity` may feel less precise at slide boundaries**  
  → Mitigation: Keep `scroll-snap-stop: always` on `.slide` to ensure single-snap behavior; proximity only relaxes the *requirement* to always snap

- **[Risk] Smooth scroll + snap may produce double-scroll**  
  → Mitigation: Disable snap temporarily during JS-driven scroll by toggling `scroll-snap-type: none` on the container, restore after scroll ends

- **[Risk] Mermaid SVG renders asynchronously — height unknown at mode entry**  
  → Mitigation: Re-check slide heights in `updateFocus()` and after Mermaid renders; use `getBoundingClientRect()` for live measurements

- **[Trade-off] Two-press model adds complexity to state machine**  
  → Acceptable: The alternative (one-press immediate advance) makes oversized content unreadable, which is the entire problem

- **[Risk] Horizontal scroll conflicts with focus-switch on ArrowLeft/ArrowRight**  
  → Mitigation: Horizontal scroll takes priority when content overflows; focus-switch only fires at boundary on second press. Single-focusable slides (most common) degrade gracefully — horizontal scroll works, boundary bounce shows, no focus-switch needed

## Open Questions

1. Should bounce animation animate the slide content or the entire scroll-container? (Recommend: scroll-container, simpler)
2. Scroll step size: 80% viewport height or content-based? (Recommend: 80% vh, consistent across slides)
3. Should we auto-detect oversized slides at PPT entry and show a visual hint (e.g., a subtle arrow indicator)? (Recommend: defer to future iteration)
