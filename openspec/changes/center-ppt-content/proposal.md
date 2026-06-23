## Why

In PPT mode, the title (`h2`) and content body are rendered together inside a single `<div class="content">` that inherits `justify-content: center` from the `.slide` flex container. This vertically centers the heading along with the body content, making headings appear in the middle of the slide rather than anchoring at the top. Headings should stay top-left for a consistent reading rhythm, while only the body content should be centered below.

## What Changes

- **HTML template**: `h2` heading rendered as a direct child of `.slide`, outside the `.content` wrapper
- **Python data model**: `Slide` class gains a `heading_html` field, split from `visual_html` in `assemble_grid()`
- **CSS**: PPT mode `.slide` no longer vertically centers; `.content` centered in remaining space; `.cover` slides keep centered behavior
- **Cover slides**: unaffected — covers use `#` (h1) which is not matched by the heading extraction regex (`##`), so `heading_html` is already empty
- No changes to DOC mode, mobile breakpoints, 16:9 transform scaling, or image slides

## Capabilities

### New Capabilities

- `ppt-content-centering`: In PPT mode, slide headings (`h2`) render top-left while the content body (`.content`) is centered horizontally and vertically in the space below the heading. Cover slides, which have no h2 heading, remain fully centered. This applies to all slides in PPT_FULL mode.

### Modified Capabilities

<!-- None -->

## Impact

- **Python**: `Slide` class (`__slots__`, `__init__`, `to_dict`), `assemble_grid()`, `parse_slide()` in `md2html.py`
- **HTML template**: Jinja2 slide template in `md2html.py` — heading rendered outside `.content`
- **CSS**: `body.mode-ppt .slide`, `body.mode-ppt .slide .content`, and new `body.mode-ppt .slide.cover` rules in CSS_TEMPLATE
- **Regenerated HTML**: `example-talk/output/sharing.html` must be re-rendered
- **No impact**: DOC mode, mobile breakpoints, zoom mode, JavaScript state machine, YAML layout system, image slides
