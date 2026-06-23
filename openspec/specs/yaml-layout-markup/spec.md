# YAML Layout Markup

## Purpose

Define the YAML-based layout description system that replaces HTML custom tags for describing slide structure.
Layout is specified in slide frontmatter as a grid of cell objects. Each cell has a type (`card`, `callout`, `steps`, `metrics`, `split`, `raw`) and an optional parameter.

## ADDED Requirements

### Requirement: YAML grid layout structure

A slide's `layout` field SHALL be a YAML mapping containing a `grid` key.
The `grid` value SHALL be a list of rows, where each row is a list of cell objects.
Each cell object SHALL be a single-key YAML mapping: `{type: param}`.

Supported cell types:
- `card`: param is the card title string. Rendered as `<div class="card"><h4>title</h4>content</div>`.
- `callout`: param is the variant string (info, warning, tip, danger). Rendered as `<div class="callout callout-{variant}">content</div>`.
- `steps`: param MUST be null. Rendered as `<div class="steps">content</div>`.
- `metrics`: param MUST be null. Rendered as `<div class="metrics-row">content</div>`.
- `split`: param MUST be null. Occupies 2 content slots. Rendered as `<div class="split-layout"><div>left</div><div>right</div></div>`.
- `raw`: param MUST be null. No container wrapper; content rendered as-is.

#### Scenario: Grid with 3 cards in one row

- **WHEN** frontmatter specifies `layout: {grid: [[{card: "A"}, {card: "B"}, {card: "C"}]]}`
- **THEN** the converter SHALL render a `<div class="grid-3">` containing three card divs in order

#### Scenario: Grid with mixed rows

- **WHEN** frontmatter specifies two rows: `[{card: "A"}, {card: "B"}]` and `[{callout: "warning"}]`
- **THEN** the converter SHALL render row 1 as `<div class="grid-2">` and row 2 as a full-width callout div

#### Scenario: Callout with unknown variant

- **WHEN** a callout cell has param "unknown"
- **THEN** the converter SHALL render `<div class="callout">` without a type-specific class

#### Scenario: Split cell occupies two slots

- **WHEN** a `{split: null}` cell appears in the grid
- **THEN** the converter SHALL consume two consecutive content slots for left and right halves

### Requirement: Layout field type detection

When `layout` is a YAML string value (e.g., `layout: grid`), the converter SHALL emit an error with a migration hint.
When `layout` is a YAML mapping with a `grid` key, the converter SHALL use the new YAML grid mode.
When `layout` is a YAML mapping with an `image` key, the converter SHALL use the image slide rendering path.
When the `layout` field is omitted, the converter SHALL fall back to an empty grid.

#### Scenario: Old string layout rejected

- **WHEN** frontmatter contains `layout: grid` (string value)
- **THEN** the converter SHALL exit with an error message indicating the new YAML syntax

#### Scenario: New mapping layout accepted

- **WHEN** frontmatter contains `layout: {grid: [[{card: "X"}]]}`
- **THEN** the converter SHALL parse it without error

#### Scenario: Image layout accepted

- **WHEN** frontmatter contains `layout: {image: {src: "assets/pic.png", alt: "A picture"}}`
- **THEN** the converter SHALL parse it without error and render an image slide

### Requirement: Image layout type detection

When `layout` is a YAML mapping with an `image` key, the converter SHALL use the image slide rendering path.
The `image` key SHALL contain a mapping with `src` (string, required), `alt` (string, required), and `mode` (string, "fullscreen" or "content", optional, default "content").
The `image` layout type SHALL be mutually exclusive with `layout.grid` — only one of `image` or `grid` SHALL appear in frontmatter.

#### Scenario: Image layout parsed correctly

- **WHEN** frontmatter contains `layout: {image: {src: "assets/hero.jpg", alt: "Hero", mode: "fullscreen"}}`
- **THEN** the converter SHALL recognize it as an image slide and render accordingly

#### Scenario: Image layout without alt rejected

- **WHEN** frontmatter contains `layout: {image: {src: "assets/pic.png"}}` without `alt`
- **THEN** the converter SHALL exit with a non-zero code and an error message

#### Scenario: Image and grid layouts mutually exclusive

- **WHEN** frontmatter contains both `image` and `grid` keys in the layout mapping
- **THEN** the converter SHALL exit with a non-zero code and an error message indicating only one layout type is allowed

### Requirement: Grid container generation

For each row in the YAML grid, the converter SHALL generate an HTML container based on the number of cells:
- 1 cell: no grid wrapper (full-width)
- 2 cells: `<div class="grid-2">`
- 3 cells: `<div class="grid-3">`
- 4 cells: `<div class="grid-4">`

Container classes SHALL include inline style attributes `--grid-cols` and `--grid-gap` derived from frontmatter fields if present.

#### Scenario: Two-column row

- **WHEN** a row has 2 cells
- **THEN** the output SHALL contain `<div class="grid-2">` wrapping those cells

#### Scenario: Single-cell row

- **WHEN** a row has 1 cell
- **THEN** the cell content SHALL NOT be wrapped in a grid container
