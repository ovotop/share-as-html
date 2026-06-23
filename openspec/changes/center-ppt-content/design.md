## Context

In PPT mode, the `h2` heading and body content are concatenated into a single `visual_html` string by `assemble_grid()`, which is rendered inside `<div class="content">`. The `.slide` flex container vertically centers `.content`, placing the heading in the middle of the viewport rather than at the top.

Current HTML structure:
```html
<div class="slide">
    <span class="slide-number">01</span>
    <div class="content">
        <h2>标题</h2>        <!-- heading + body together -->
        <div class="grid-2">...</div>
    </div>
</div>
```

Target HTML structure:
```html
<div class="slide">
    <span class="slide-number">01</span>
    <h2>标题</h2>             <!-- heading as direct child of .slide -->
    <div class="content">     <!-- only body content -->
        <div class="grid-2">...</div>
    </div>
</div>
```

## Goals / Non-Goals

**Goals:**
- In PPT mode, `h2` headings appear at the top of the slide (after padding), left-aligned
- Content body (`.content`) is centered both horizontally and vertically in the space below the heading
- Cover slides (`.cover`) keep their existing fully-centered layout
- Image slides (`.slide-image-fullscreen`, `.slide-image-content`) are unchanged

**Non-Goals:**
- No changes to DOC mode, PPT_ZOOM mode, or mobile breakpoints
- No changes to 16:9 aspect ratio scaling (JS-driven transform)
- No changes to YAML layout syntax

## Decisions

### Decision 1: Split heading_html from visual_html in Python

**Choice**: Add `heading_html` field to `Slide` class and stop prepending it in `assemble_grid()`.

**Rationale**: `assemble_grid()` currently returns `heading_html + grid_html` as a single string. Splitting at the data level lets the template render them in different DOM positions.

**Alternatives considered**:
- **CSS-only pseudo-element extraction**: Impossible — CSS can't move DOM elements.
- **JavaScript post-render split**: Flicker, complexity, fragile.
- **Regex split in template**: Fragile, breaks if heading contains nested HTML.

### Decision 2: Cover slides are naturally immune

Cover slides use `#` (h1), not matched by the heading extraction regex (`##\s+`). `heading_html` is already empty for covers. The template renders nothing above `.content`. `.cover` gets `justify-content: center` to stay fully centered. No special code needed.

### Decision 3: Content vertical centering via flexbox `margin: auto`

```css
body.mode-ppt .slide {
    min-height: 100vh;
    padding: 60px 120px;
    /* flex-direction: column inherited from base */
    /* naturally flex-start; no justify-content override needed */
}
body.mode-ppt .slide .content {
    align-self: center;
    margin: auto 0;
}
body.mode-ppt .slide.cover {
    justify-content: center;
}
```

With `flex-direction: column`, `margin: auto` on `.content` absorbs free space equally above and below.

### Decision 4: Slide data class extension

```python
class Slide:
    __slots__ = (
        "number", "duration", "emoji",
        "heading_html", "visual_html", "reader_html", "is_cover",
        "layout_type", "image_mode", "image_src", "image_alt",
    )
```

`assemble_grid()` returns only body content. `parse_slide()` passes `heading_html` separately.

## Risks / Trade-offs

- **[Risk] `heading_html` empty for slides without `##`**: Already existing behavior — no regression.
- **[Risk] Hand-authored test HTML untouched**: Test fixtures have their own inline CSS, not the template. Only `example-talk/output/sharing.html` is regenerated.
