# Markdown Slide Authoring (Delta)

## MODIFIED Requirements

### Requirement: Slide file YAML frontmatter

Each file under `slides/` SHALL have YAML frontmatter with the following fields:

- `slide` (required): Slide number
- `duration` (optional): This slide's duration
- `layout` (required): A YAML mapping with a `grid` key, where `grid` is a list of rows. Each row is a list of cell objects in the format `{type: param}`.
  - Cell types: `card` (param = title string), `callout` (param = variant), `steps` (param = null), `metrics` (param = null), `split` (param = null), `raw` (param = null)
  - When `layout` is omitted, the slide SHALL render with an empty grid and `raw` cells for all content slots.
- `accent` (optional): Color name mapped to theme color
- `emoji` (optional): Emoji to display alongside the slide heading

The previous string-valued `layout` field (`grid`, `flex`, `stack`, `split`, `default`) and associated fields (`cols`, `ratio`, `gap`, `dir`, `align`) are no longer supported.

#### Scenario: Slide with YAML grid layout

- **WHEN** frontmatter contains `layout: {grid: [[{card: "A"}, {card: "B"}]]}`
- **THEN** the converter SHALL render a grid-2 with two cards

#### Scenario: Old string layout rejected

- **WHEN** frontmatter contains `layout: grid` (string value)
- **THEN** the converter SHALL exit with an error message directing the user to the new YAML syntax

#### Scenario: Layout omitted

- **WHEN** frontmatter omits the `layout` field
- **THEN** the converter SHALL treat all content slots as `raw` cells in a single-row grid

### Requirement: Slide file Markdown body

The Markdown body of each slide file SHALL contain standard Markdown content with NO HTML custom tags.
Content SHALL be divided into slots using `=== slot ===` delimiters.
The heading (first `##` title) SHALL appear before the first `=== slot ===`.
Each slot SHALL map to a cell in the YAML layout grid in row-major order.

The following elements SHALL be supported:
- Headings (h2/h3/h4)
- Paragraphs, bold, italic, inline code
- Unordered and ordered lists
- Code blocks (fenced with ```)
- Mermaid diagrams (fenced with ```mermaid)
- Tables
- Images with alt text
- Blockquotes
- The `<!-- reader -->...<!-- /reader -->` marker for reader layer content
- Standard HTML `<hr>` for horizontal rules
- Standard HTML `<br>` for line breaks

The following previously supported elements are REMOVED:
- `<card>` custom tags
- `<callout>` custom tags
- `<steps>` and `<step>` custom tags
- `<div class="card">`, `<div class="callout">`, `<div class="metrics-row">` and similar HTML layout divs
- `<div markdown="1">` wrapper blocks

#### Scenario: Slide with YAML-described cards

- **WHEN** slide body contains markdown content separated by `=== slot ===`, and frontmatter has `layout.grid` with `{card: ...}` cells
- **THEN** each card SHALL render the corresponding slot's markdown content properly parsed

#### Scenario: Slide with mermaid diagram

- **WHEN** any content slot contains a fenced code block with language `mermaid`
- **THEN** the converter SHALL embed the mermaid diagram with proper container for zoom support

### Requirement: Slide content rendered as HTML

The converter SHALL render slide Markdown body to HTML using the following pipeline:

1. Extract YAML frontmatter and layout grid
2. Split body into heading and content slots (by `=== slot ===`, rsplit from right)
3. Convert heading and each slot independently through Python `markdown` library
4. Wrap each slot's HTML in the container corresponding to its YAML cell type
5. Assemble rows into CSS grid containers based on cell count per row

The following previously supported transformations are REMOVED:
- Custom tag processing (`<card>`, `<callout>`, `<steps>`, `<step>`)
- Auto-card-detection and re-wrapping
- `split_top_level_blocks` block splitting

#### Scenario: Two card cells

- **WHEN** grid has two `{card: ...}` cells and body has two corresponding slots
- **THEN** the output SHALL contain two `<div class="card">` elements inside a `<div class="grid-2">`

#### Scenario: Code block in card slot

- **WHEN** a card cell's content slot contains a fenced code block
- **THEN** the code block SHALL be rendered inside the card div with syntax highlighting applied
