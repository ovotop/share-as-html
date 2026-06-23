## Why

PPT_ZOOM mode currently displays zoomed content at its cloned natural size — small images sit centered in a sea of empty space, large ones require excessive scrolling. Users have no control over how content fills the screen. Adding fit/fill toggle and zoom scale control gives a natural image-viewer experience.

## What Changes

- Enter ZOOM: default to "内接" — content fits entirely within viewport (no cropping, see the full picture)
- `Enter` in ZOOM: toggle between "内接" (fit) and "填充" (fill viewport, may crop)
- `+` / `-` in ZOOM: step zoom scale through preset levels 1.0× → 1.25× → 1.5× → 2.0× → 3.0×
- Scale only goes ≥ 1.0× — never smaller than fit-to-viewport
- CSS custom property `--zoom-scale` drives sizing; `.fill` class toggles fit vs fill rendering
- Works for ALL zoomable content: images, mermaid SVGs

## Capabilities

### New Capabilities

- `zoom-scale-control`: Users can adjust the zoom level of content in PPT_ZOOM mode using the +/- keys, with 0 to reset. Scale is continuous (multiplicative), works on all zoomable content types.

### Modified Capabilities

<!-- None — zoom behavior has no existing openspec spec -->

## Impact

- **CSS**: `body.mode-zoom .zoom-content` rule in `md2html.py` CSS_TEMPLATE (currently has no style rules)
- **JavaScript**: `enterZoomMode()`, `exitZoomMode()`, and keyboard handler in PPT_ZOOM case — all in `md2html.py` JS_TEMPLATE
- **Documentation**: Keyboard shortcut table in SKILL.md
- **No impact**: DOC mode, PPT_FULL focus system, state machine transitions, image slide layout
