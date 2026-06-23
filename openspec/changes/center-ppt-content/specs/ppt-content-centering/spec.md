# PPT Content Centering

## Purpose

Define the layout behavior for PPT mode slides: headings (`h2`) render top-left while the content body (`.content`) is centered horizontally and vertically in the space below. This replaces the previous behavior where heading and body were rendered together inside `.content` and vertically centered as a group.

## ADDED Requirements

### Requirement: Heading rendered outside content wrapper

The converter SHALL render the extracted `h2` heading as a direct child of `.slide`, not inside the `.content` wrapper. The `.content` wrapper SHALL contain only the body content (grids, cards, callouts, etc.).

#### Scenario: Normal slide with `##` heading

- **WHEN** a slide markdown file contains a `##` heading and body content
- **THEN** the generated HTML SHALL render the heading as `<h2>...</h2>` directly inside `<div class="slide">`
- **AND** the body content SHALL render inside `<div class="content">`

#### Scenario: Cover slide with `#` heading (h1)

- **WHEN** a cover slide markdown file contains an `#` heading (h1)
- **THEN** no `heading_html` SHALL be extracted (regex only matches `##`)
- **AND** the entire body including h1 SHALL render inside `<div class="content">` as before

#### Scenario: Slide without any heading

- **WHEN** a slide markdown file contains no `##` or `#` heading
- **THEN** no heading element SHALL be rendered outside `.content`
- **AND** the body content SHALL render inside `<div class="content">`

### Requirement: Heading at top in PPT mode

In PPT mode (`body.mode-ppt`), the slide heading (`h2`) SHALL appear at the top of the slide, positioned after the slide's top padding. The heading SHALL NOT be vertically centered within the viewport.

#### Scenario: Standard slide in PPT mode

- **WHEN** a slide with a heading (`h2`) and body content is displayed in PPT_FULL mode
- **THEN** the heading SHALL appear at the top of the slide area, with the 60px top padding applied
- **AND** `.content` SHALL be vertically centered in the space below the heading via `margin: auto 0`

#### Scenario: Slide without heading in PPT mode

- **WHEN** a slide without an `h2` heading is displayed in PPT_FULL mode
- **THEN** the content body SHALL be vertically centered within the slide

### Requirement: Content centered in PPT mode

In PPT mode, the `.content` element SHALL be centered both horizontally and vertically in the available space (below the heading if present, otherwise the full slide area).

#### Scenario: Content centering on wide screen

- **WHEN** a slide is displayed in PPT_FULL mode on a viewport wider than the content width
- **THEN** `.content` SHALL be horizontally centered via `align-self: center`
- **AND** `.content` SHALL be vertically centered via `margin: auto 0`

#### Scenario: Grid cards in PPT mode

- **WHEN** a slide with grid-2 or grid-3 content cards is displayed in PPT_FULL mode
- **THEN** the grid SHALL be centered within `.content`
- **AND** the heading SHALL appear above the grid at the top of the slide

### Requirement: Cover slides keep fully-centered layout

In PPT mode, cover slides (`.slide.cover`) SHALL maintain their existing fully-centered layout using `justify-content: center` on the flex container.

#### Scenario: Cover slide in PPT mode

- **WHEN** a cover slide (slide 1) is displayed in PPT_FULL mode
- **THEN** the cover content (h1, subtitle, meta) SHALL be vertically and horizontally centered in the viewport
- **AND** the cover slide SHALL NOT apply the top-anchored heading layout used for content slides

### Requirement: PPT mode padding preserved

In PPT mode, the slide SHALL retain its 60px top/bottom and 120px left/right padding.

#### Scenario: Content respects padding

- **WHEN** a slide is displayed in PPT_FULL mode
- **THEN** the heading and content body SHALL be positioned with at least 60px from the top edge of the viewport
- **AND** the content SHALL be positioned with at least 120px from the left and right edges

### Requirement: DOC mode layout visually unchanged

The structural change (heading outside `.content`) SHALL NOT cause visual regressions in DOC mode. Base `.slide` rules (`justify-content: center; align-items: center`) SHALL continue to center heading and content as a group.

#### Scenario: DOC mode centering preserved

- **WHEN** the document is in DOC mode (default state)
- **THEN** slides SHALL maintain their existing visual layout
- **AND** the heading and content SHALL appear vertically centered as a group

### Requirement: Image slides unaffected

Slides with `layout.image` SHALL NOT be affected by the heading extraction or CSS changes.

#### Scenario: Fullscreen image in PPT mode

- **WHEN** a slide with `layout: {image: {mode: fullscreen}}` is displayed in PPT_FULL mode
- **THEN** the image SHALL fill the entire slide with `object-fit: cover`
- **AND** no heading shall be rendered outside the slide's image content
