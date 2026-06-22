# md-to-html-pipeline Delta Spec

## MODIFIED Requirements

### Requirement: Template architecture

The script SHALL use a Jinja2 template with the following structure:

- Fixed `<style>` block (CSS copied from current SKILL.md)
- Fixed `<script>` block (JS copied from current test HTML files)
- Dynamic `<body>` block rendered from parsed Markdown slides
- The body block SHALL include a `.doc-footer` element after the last slide, containing the attribution link to the ovotop/share-as-html GitHub repository

The template SHALL be embedded in the script as a string constant, not loaded from an external file.

#### Scenario: Template renders all slides

- **WHEN** the script processes a project with 5 slides
- **THEN** the output HTML SHALL contain 5 `<div class="slide">` elements in order

#### Scenario: Template renders footer after slides

- **WHEN** the script processes a project with any number of slides
- **THEN** the output HTML SHALL contain a `<div class="doc-footer">` element after the last slide, inside `#scroll-container`

### Requirement: Self-contained HTML output

The output HTML file SHALL be self-contained:
- All CSS SHALL be embedded in a `<style>` tag (no external stylesheets)
- All JavaScript SHALL be embedded in a `<script>` tag
- Mermaid SHALL be loaded from CDN (`https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js`)
- Images from `assets/` SHALL be embedded as base64 data URIs (for images ≤ 1MB) or referenced by relative path
- The footer's ovotop icon SHALL be loaded from external URL (`https://avatars.githubusercontent.com/u/166823538?s=32`) and is exempt from the base64 embedding rule

#### Scenario: Single file sharing

- **WHEN** user opens the output HTML file by double-clicking
- **THEN** it SHALL render correctly without a web server or additional files

### Requirement: Existing CSS and JS reuse

The script SHALL use the existing CSS and JS from the `share-as-html` skill as-is. The CSS template (deep theme, card styles, callout styles, grid layouts) and JS template (three-state state machine, keyboard navigation, zoom mode) SHALL be embedded in the Jinja2 template without modification. The footer CSS styles (`.doc-footer` and mode-specific hiding rules) SHALL also be included in the CSS template.

#### Scenario: PPT mode works

- **WHEN** user opens the output HTML and presses Enter
- **THEN** the page SHALL switch to PPT mode with snap-to-slide behavior

#### Scenario: DOC mode works

- **WHEN** user is in PPT mode and presses Esc
- **THEN** the page SHALL return to DOC mode with free scrolling

#### Scenario: Fluid typography in generated HTML

- **WHEN** md2html.py generates output HTML
- **THEN** the CSS SHALL contain `clamp()` font-size values and `.slide { align-items: center; }`

#### Scenario: PPT mode wider content in generated HTML

- **WHEN** md2html.py generates output HTML
- **THEN** the CSS SHALL contain `body.mode-ppt .slide .content { max-width: 1100px; }`

#### Scenario: Footer hidden in PPT mode in generated HTML

- **WHEN** md2html.py generates output HTML
- **THEN** the CSS SHALL contain `body.mode-ppt .doc-footer { display: none; }` and `body.mode-zoom .doc-footer { display: none; }`
