# Image Slide Layout

## Purpose

Define the `layout.image` YAML frontmatter type that renders a slide with a single image as its primary content. Supports two display modes: `fullscreen` (image fills the entire slide) and `content` (image constrained to the 16:9 content area). Works in both DOC and PPT viewing modes.

## ADDED Requirements

### Requirement: Image layout type declaration

A slide MAY declare `layout.image` in frontmatter instead of `layout.grid`.
The `image` value SHALL be a YAML mapping with keys `src` (required), `alt` (required), and `mode` (optional, default `content`).

```yaml
layout:
  image:
    src: assets/hero.jpg
    alt: Hero illustration
    mode: fullscreen
```

#### Scenario: Fullscreen image layout declared

- **WHEN** frontmatter specifies `layout: {image: {src: "assets/cover.png", alt: "Cover", mode: "fullscreen"}}`
- **THEN** the converter SHALL generate a slide with class `slide-image-fullscreen` containing an `<img>` element with `src`, `alt`, `object-fit: cover`, and dimensions filling the slide

#### Scenario: Content image layout declared

- **WHEN** frontmatter specifies `layout: {image: {src: "assets/diagram.png", alt: "Diagram", mode: "content"}}`
- **THEN** the converter SHALL generate a slide with class `slide-image-content` containing an `<img>` element inside `.content` with `object-fit: contain`

#### Scenario: Mode defaults to content

- **WHEN** frontmatter specifies `layout: {image: {src: "assets/pic.png", alt: "Picture"}}` without a `mode` field
- **THEN** the converter SHALL treat it as `mode: content`

#### Scenario: Missing alt text

- **WHEN** frontmatter specifies `layout: {image: {src: "assets/pic.png"}}` without alt
- **THEN** the converter SHALL exit with a non-zero code and an error message indicating alt is required

### Requirement: Fullscreen image slide rendering

A slide with `mode: fullscreen` SHALL render the image as the sole visual element filling the entire `.slide` container.
The slide SHALL have class `slide-image-fullscreen`.

#### Scenario: Fullscreen image structure

- **WHEN** a fullscreen image slide is rendered
- **THEN** the output SHALL contain `<div class="slide slide-image-fullscreen"><img src="..." alt="..." style="max-width:900px;width:100%;height:auto;object-fit:contain;"></div>`
- **AND** the slide SHALL NOT contain a `.content` wrapper
- **AND** the image SHALL be constrained to 900px max-width and displayed proportionally (object-fit: contain)

#### Scenario: Fullscreen image in PPT mode

- **WHEN** the viewer is in PPT mode on a fullscreen image slide
- **THEN** the image SHALL fill the entire viewport (100vw × 100vh) via `body.mode-ppt .slide-image-fullscreen img` rules with `position: absolute; object-fit: contain`
- **AND** scroll-snap SHALL be active

#### Scenario: Fullscreen image in DOC mode

- **WHEN** the viewer is in DOC mode on a fullscreen image slide
- **THEN** the slide SHALL have `min-height: auto` so it flows naturally in the scroll
- **AND** the image SHALL be constrained to content area width (max-width: 900px) with `object-fit: contain`
- **AND** the slide SHALL inherit standard slide padding (32px 40px)

### Requirement: Content-mode image slide rendering

A slide with `mode: content` SHALL render the image inside the `.content` wrapper, constrained by the standard content area dimensions.
The slide SHALL have class `slide-image-content`.

#### Scenario: Content image structure

- **WHEN** a content image slide is rendered
- **THEN** the output SHALL contain `<div class="slide slide-image-content"><div class="content"><img src="..." alt="..." style="width:100%;height:auto;object-fit:contain;"></div></div>`

#### Scenario: Content image in PPT mode

- **WHEN** the viewer is in PPT mode on a content image slide
- **THEN** the image SHALL be constrained within the 16:9 `.content` area using `width: 100%; height: auto; object-fit: contain`
- **AND** the `transform: scale()` from updateContentScale() SHALL apply to the `.content` wrapper

#### Scenario: Content image in DOC mode

- **WHEN** the viewer is in DOC mode on a content image slide
- **THEN** the slide SHALL have `min-height: auto` (standard DOC behavior)
- **AND** the image SHALL be constrained to `.content` max-width (900px)

### Requirement: Image slide keyboard behavior

Image slides SHALL NOT participate in the diagram focus system.
No `.diagram-focusable` elements SHALL be generated for image slides.

#### Scenario: Arrow keys on image slide

- **WHEN** the viewer is in PPT mode on an image slide
- **THEN** ArrowDown SHALL navigate to the next slide
- **AND** ArrowUp SHALL navigate to the previous slide
- **AND** ArrowLeft/Right SHALL NOT trigger focus switching (no focusable diagrams)
- **AND** Enter SHALL NOT trigger zoom mode

#### Scenario: Image slide has no zoom

- **WHEN** `updateFocus()` runs on the current slide
- **AND** the slide is an image slide (no `.diagram-focusable` children)
- **THEN** `focusedDiagramIndex` SHALL remain `-1` and no border SHALL be applied

### Requirement: Slide number on image slides

The `.slide-number` element SHALL remain visible on image slides.
It SHALL render above the image using `z-index: 1`.

#### Scenario: Slide number on fullscreen image

- **WHEN** a fullscreen image slide is rendered
- **THEN** the `.slide-number` SHALL be present with `z-index: 1`
- **AND** its position SHALL be `bottom: 24px; right: 32px`

### Requirement: Mobile adaptation for image slides

On screens ≤768px wide, fullscreen image slides SHALL adjust for narrower viewports.

#### Scenario: Mobile fullscreen image

- **WHEN** viewport width is ≤768px
- **AND** the slide is a fullscreen image slide
- **THEN** the image SHALL use `object-fit: contain` instead of `cover`
- **AND** the slide SHALL use `min-height: 60vh` instead of `100vh`
