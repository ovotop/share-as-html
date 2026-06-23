# Markdown-to-HTML Pipeline (Delta)

## MODIFIED Requirements

### Requirement: Existing CSS and JS reuse

The script SHALL use the existing CSS and JS from the `share-as-html` skill as-is. The CSS template (deep theme, card styles, callout styles, grid layouts) and JS template (three-state state machine, keyboard navigation, zoom mode) SHALL be embedded in the Jinja2 template without modification. The footer CSS styles (`.doc-footer` and mode-specific hiding rules) SHALL also be included in the CSS template.

**Addition**: The CSS template SHALL include rules for `.slide-image-fullscreen` and `.slide-image-content` classes to support the `layout.image` YAML type. The JS template requires no modification — image slides behave as normal slides within the existing state machine (no focus, no zoom).

#### Scenario: PPT mode works

- **WHEN** user opens the output HTML and presses Enter
- **THEN** the page SHALL switch to PPT mode with snap-to-slide behavior

#### Scenario: DOC mode works

- **WHEN** user is in PPT mode and presses Esc
- **THEN** the page SHALL return to DOC mode with free scrolling

#### Scenario: Fluid typography in generated HTML

- **WHEN** md2html.py generates output HTML
- **THEN** the CSS SHALL contain `clamp()` font-size values and `.slide { align-items: center; }`

#### Scenario: PPT mode transform scaling in generated HTML

- **WHEN** md2html.py generates output HTML
- **THEN** the CSS SHALL contain `body.mode-ppt .slide .content { width: 1680px; aspect-ratio: 16 / 9; max-width: none; transform-origin: center center; }`
- **AND** the CSS SHALL contain `body.mode-ppt .slide { padding: 60px 120px; overflow: hidden; }`
- **AND** the CSS SHALL contain a responsive override: `@media (max-width: 768px) { body.mode-ppt .slide .content { width: 100%; aspect-ratio: auto; transform: none; } }`
- **AND** the JavaScript SHALL contain an `updateContentScale()` function that applies `transform: scale()` to `.slide .content` elements
- **AND** the JavaScript SHALL call `updateContentScale()` on entering PPT mode, navigating slides, and window resize
- **AND** the CSS SHALL NOT contain `body.mode-ppt .slide .content { max-width: 1100px; }`

#### Scenario: Footer hidden in PPT mode in generated HTML

- **WHEN** md2html.py generates output HTML
- **THEN** the CSS SHALL contain `body.mode-ppt .doc-footer { display: none; }` and `body.mode-zoom .doc-footer { display: none; }`

#### Scenario: Image slide CSS in generated HTML

- **WHEN** md2html.py generates output HTML
- **THEN** the CSS SHALL contain DOC-mode rules for `.slide-image-fullscreen img { max-width: 900px; width: 100%; height: auto; object-fit: contain; }`
- **AND** the CSS SHALL contain PPT-mode rules for `body.mode-ppt .slide-image-fullscreen { min-height: 100vh; padding: 0; overflow: hidden; position: relative; }`
- **AND** the CSS SHALL contain PPT-mode rules for `body.mode-ppt .slide-image-fullscreen img { width: 100%; height: 100%; object-fit: contain; position: absolute; top: 0; left: 0; max-width: none; }`
- **AND** the CSS SHALL contain `.slide-image-content img { width: 100%; height: auto; object-fit: contain; }`
- **AND** the CSS SHALL contain a mobile override: `@media (max-width: 768px) { body.mode-ppt .slide-image-fullscreen { min-height: 60vh; } body.mode-ppt .slide-image-fullscreen img { object-fit: contain; } }`

## ADDED Requirements

### Requirement: Image slide HTML structure

When a slide uses `layout.image`, the script SHALL generate HTML that differs from standard slides:

- **fullscreen mode**: `<div class="slide slide-image-fullscreen"><span class="slide-number">...</span><img src="..." alt="..."></div>` — no `.content` wrapper
- **content mode**: `<div class="slide slide-image-content"><span class="slide-number">...</span><div class="content"><img src="..." alt="..."></div></div>` — image inside `.content`

#### Scenario: Fullscreen image slide HTML structure

- **WHEN** the script processes a slide with `layout: {image: {src: "assets/hero.png", alt: "Hero", mode: "fullscreen"}}`
- **THEN** the output SHALL contain `<div class="slide slide-image-fullscreen" data-slide="N"><span class="slide-number">NN</span><img src="..." alt="Hero"></div>`

#### Scenario: Content image slide HTML structure

- **WHEN** the script processes a slide with `layout: {image: {src: "assets/diagram.png", alt: "Diagram", mode: "content"}}`
- **THEN** the output SHALL contain `<div class="slide slide-image-content" data-slide="N"><span class="slide-number">NN</span><div class="content"><img src="..." alt="Diagram"></div></div>`
