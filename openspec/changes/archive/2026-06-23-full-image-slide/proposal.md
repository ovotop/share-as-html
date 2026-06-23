## Why

Currently there is no way to create a slide whose primary content is a single full-bleed image — typical for presentation covers, section dividers, photo galleries, or illustration slides. Images are always constrained within the `.content` wrapper (`max-width: 900px` in DOC, `width: 840px` + `aspect-ratio: 16/9` in PPT). Users need the ability to mark a slide as "image-first," where an `<img>` fills either the entire slide background (fullscreen cover) or the content area (centered illustration), in both DOC and PPT modes.

## What Changes

- **New YAML layout type `image`**: slide frontmatter can declare `layout: image` with `mode: fullscreen` (image fills entire slide) or `mode: content` (image fits within the 16:9 content area, centered), plus `src` and `alt` fields
- **CSS changes**: `.slide-image-fullscreen` class makes the slide a flex container that holds the image as its sole child, stretched to cover the slide bounds; `.slide-image-content` variant constrains the image to the content area
- **Image behavior**: `object-fit: cover` for fullscreen (image crops to fill), `object-fit: contain` for content area (image fits without crop). Both modes center the image
- **DOC mode**: fullscreen image slides display the image within the slide's natural height (`min-height: auto`), content-area image slides constrain to `.content` width — consistent with other slide types
- **PPT mode**: fullscreen image fills the entire 100vh snap-aligned slide; content-area image fits within the 16:9 content box — no independent zoom/focus behavior needed (the image *is* the slide)

## Capabilities

### New Capabilities

- `image-slide-layout`: A new YAML frontmatter layout (`layout: image`) that renders a slide with a single image as its primary content. Supports two display modes: `fullscreen` (image fills the entire slide, `object-fit: cover`) and `content` (image constrained to the `.content` area, `object-fit: contain`). Both DOC and PPT modes are supported. No keyboard focus/zoom — the image is the slide itself, not a focusable element within it.

### Modified Capabilities

- `yaml-layout-markup`: Add `image` cell type to the YAML layout grammar, with parameters `src`, `alt`, and `mode` (fullscreen | content)
- `md-to-html-pipeline`: Add CSS rules for `.slide-image-fullscreen` and `.slide-image-content` classes to the CSS template; update HTML structure to support image-mode slides outside the `.content` wrapper

## Impact

- **Template**: `skills/share-as-html/scripts/md2html.py` — CSS_TEMPLATE (new `.slide-image-fullscreen` and `.slide-image-content` rules), JS_TEMPLATE (no keyboard focus needed for image slides), HTML_TEMPLATE J2 template (conditional path for image slides)
- **Skill spec**: `skills/share-as-html/SKILL.md` — CSS template block, JS template block, Image Guide section, HTML skeleton example
- **Test fixtures**: 5 HTML test files — add at least one image-cover slide to `test-image-zoom.html`; ensure `test-automated.spec.js` covers new layout
- **Output docs**: `example-talk/output/sharing.html` — regenerated from template
- **Not affected**: mermaid zoom, existing diagram focus/zoom behavior, reader-narrative layer, DOC mode footer
