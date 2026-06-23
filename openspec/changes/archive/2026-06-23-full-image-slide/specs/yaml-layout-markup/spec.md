# YAML Layout Markup (Delta)

## ADDED Requirements

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

## MODIFIED Requirements

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
