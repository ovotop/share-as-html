## Context

The share-as-html presentation engine renders `.slide` containers with a two-layer structure: `.slide` (flex column, centered) contains `.content` (constrained width). In DOC mode slides are `min-height: auto`; in PPT mode they become `min-height: 100vh` with `scroll-snap-align: start`. The in-progress `ppt-16-9-aspect-ratio` change adds `transform: scale()` to `.content` for fixed 1680×945 layout at all viewport sizes.

There is currently no way to dedicate an entire slide to a single image. Images are always wrapped in `.diagram-focusable` inside `.content`, participating in the keyboard focus/zoom system. The `.cover` class already exists (for text-only title slides using `.cover h1` with gradient text), but it has no image-background capabilities.

The `yaml-layout-markup` spec defines a `layout.grid` system with cell types (card, callout, steps, metrics, split, raw). Full-image slides need a different layout type — the image is the content, not a grid of cells.

## Goals / Non-Goals

**Goals:**
- Add a `layout.image` YAML frontmatter type that renders a slide with a single image as primary content
- Support two modes: `fullscreen` (image fills entire slide, `object-fit: cover`) and `content` (image constrained to `.content` area, `object-fit: contain`)
- Work correctly in both DOC and PPT modes
- Image is always centered; no keyboard focus/zoom — the image is the slide itself
- Override CSS support via project `override.css`

**Non-Goals:**
- No support for mermaid or other non-image content in image slides
- No layered content (text overlay) on top of fullscreen images — the YAML layout approaches this differently (heading is part of the slide structure, not overlaying the image)
- No slideshow/carousel — one image per slide
- No change to existing `.diagram-focusable` zoom behavior
- No change to reader-narrative layer

## Decisions

### Decision 1: YAML layout type vs CSS class

**Chosen**: New `layout.image` YAML type in slide frontmatter, with `src`, `alt`, and `mode` fields.

```yaml
layout:
  image:
    src: assets/cover.jpg
    alt: Cover illustration
    mode: fullscreen  # or "content"
```

**Rationale**: The existing `layout.grid` system already uses YAML frontmatter to declare slide structure. Adding `layout.image` as a peer of `layout.grid` is consistent with the Markdown-slide-authoring workflow. A CSS class approach (`.slide-image-fullscreen`) would require the markdown-to-HTML converter to detect image-only slides heuristically, which is fragile.

**Alternative considered**: Reusing `layout.grid` with a new cell type `{image: {src: ..., mode: fullscreen}}`. Rejected because fullscreen images span the entire slide, not a grid cell — the grid's container-generating logic (1 cell = no wrapper, 2 = grid-2, etc.) is a poor semantic match.

### Decision 2: Image placement — slide background vs `<img>` element

**Chosen**: Render as an `<img>` element that is the sole child of `.slide` (fullscreen) or inside `.content` (content mode).

- **Fullscreen**: `.slide` CSS becomes a flex container with the `<img>` filling it via `width: 100%; height: 100%; object-fit: cover`. No additional wrappers.
- **Content**: `<img>` inside `.content` with `width: 100%; height: auto; object-fit: contain`.

**Rationale**: Using `<img>` preserves accessibility (`alt` text), works with the existing `image-base64-embedding` pipeline (which operates on `src=` attributes in `<img>` tags), and avoids the complexity of CSS `background-image` with base64 data URIs. The `object-fit` property handles both cropping (cover) and fitting (contain) natively.

**Alternative considered**: CSS `background-image` on `.slide`. Rejected because: (1) requires extending the base64 embedding pipeline to handle CSS properties, (2) no native `alt` text support, (3) hard to inspect/devtools since it's a CSS property not a DOM element.

### Decision 3: Fullscreen image in DOC mode

**Chosen**: In DOC mode, the image converges to the content area width (max-width: 900px), inherits the slide padding (32px 40px), and uses `object-fit: contain` for proportional display. PPT mode retains the original full-bleed behavior (100vw × 100vh, `object-fit: cover`) via `body.mode-ppt` prefixed rules.

```css
/* DOC mode (default) — image in content flow */
.slide-image-fullscreen {
    /* inherits .slide padding and min-height: auto */
}

.slide-image-fullscreen img {
    max-width: 900px;
    width: 100%;
    height: auto;
    object-fit: contain;
}

/* PPT mode — true full-bleed */
body.mode-ppt .slide-image-fullscreen {
    min-height: 100vh;
    padding: 0;
    overflow: hidden;
    position: relative;
}

body.mode-ppt .slide-image-fullscreen img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    position: absolute;
    top: 0;
    left: 0;
    max-width: none;
}
```

**Rationale**: DOC mode is a continuous reading experience where all content shares the same 900px column width. A 100vw image between text columns breaks the reading rhythm — the eye must re-anchor from a focused reading column to full-screen and back. Converging the image to the content area preserves the document metaphor: the image is a large illustration, not a stage transition. PPT mode is a presentation mode where each slide is an independent stage — full-bleed images are expected and desired there. This change also fixes a specificity bug where `body.mode-ppt .slide` (padding: 60px 120px) was overriding `.slide-image-fullscreen` (padding: 0) due to higher specificity (0-1-2 vs 0-1-0).

**Alternative considered**: Original Decision 3 forced `min-height: 100vh` in DOC mode, arguing cover slides need visual impact. Rejected after exploring the reading experience: the visual discontinuity was jarring, and `object-fit: contain` at content width still provides a strong visual element without breaking the scroll flow.

### Decision 4: Interaction with ppt-16-9-aspect-ratio scaling

**Chosen**: Fullscreen image slides use `.slide` directly (bypassing `.content`), so the `transform: scale()` on `.content` does not apply. The image naturally fills the `.slide` bounds, which are `100vw × 100vh` in PPT mode.

Content-mode image slides keep the image inside `.content`, so the 16:9 transform scaling applies normally. The `object-fit: contain` ensures the image fits within the scaled content area.

**No CSS interaction needed** — the architecture naturally separates the two modes.

### Decision 5: Keyboard navigation behavior

**Chosen**: Image slides behave as normal slides — ArrowDown/Up advances to next/previous slide, ArrowLeft/Right does nothing (no focusable diagrams within an image slide). No Enter → zoom behavior. The image slide has no `.diagram-focusable` elements.

**Rationale**: Simpler mental model. The image *is* the slide content, not a zoomable diagram within it. Users who want zoomable images can use existing `.diagram-focusable > img` pattern.

### Decision 6: Slide number visibility

**Chosen**: Slide number (`.slide-number`) remains visible on image slides. It sits at `z-index: 1` above the image. Uses existing positioning from `ppt-16-9-aspect-ratio` (`bottom: 24px; right: 32px`).

### Decision 7: Mobile behavior

**Chosen**: On mobile (≤768px), fullscreen images use `object-fit: contain` instead of `cover` to avoid awkward cropping of narrow images. Content-mode images behave the same as desktop.

```css
@media (max-width: 768px) {
    .slide-image-fullscreen img {
        object-fit: contain;
    }
    .slide-image-fullscreen {
        min-height: 60vh;
    }
}
```

## Risks / Trade-offs

- **[Risk] Image loading latency**: Large images as fullscreen backgrounds may load slowly, showing a blank slide. → **Mitigation**: The base64 embedding pipeline (threshold ≤1MB) already mitigates this for most images. For larger images, relative paths allow progressive loading. A future enhancement could add a loading spinner.

- **[Risk] Aspect ratio mismatch on ultrawide displays**: A 16:9 image set to `object-fit: cover` on a 21:9 ultrawide display will crop top/bottom significantly. → **Mitigation**: This is inherent to `object-fit: cover` — the user chooses the image and display mode. `object-position: center` ensures the most important content is visible. Content mode with `contain` avoids this entirely.

- **[Trade-off] No text overlay on fullscreen images**: Could limit creative use cases where users want title text overlaid on a background photo. → **Mitigation**: This is a deliberate scope boundary. The `slide-number` stays visible, providing minimal context. A future change could add a dedicated overlay text layer.

## Open Questions

- None. Scope boundaries and design decisions are confirmed with user.
