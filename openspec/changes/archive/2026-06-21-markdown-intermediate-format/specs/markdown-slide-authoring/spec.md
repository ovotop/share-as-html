## ADDED Requirements

### Requirement: Project directory structure

A presentation project SHALL follow this directory structure:

```
<project>/
├── meta.md              # YAML frontmatter with title, subtitle, speaker, date, theme
├── outline.md           # Markdown table with section numbers, names, durations, file paths
├── speaker-script.md    # Presenter script (not rendered to HTML)
├── slides/
│   ├── 01-cover.md
│   ├── 02-<name>.md
│   └── ...
├── override.css         # (optional) Human CSS overrides
└── assets/              # (optional) Images and other resources
```

#### Scenario: Valid project recognized by converter

- **WHEN** a directory contains `meta.md`, `outline.md`, and at least one file under `slides/`
- **THEN** the converter SHALL accept it as a valid project

#### Scenario: Missing meta.md

- **WHEN** a directory does not contain `meta.md`
- **THEN** the converter SHALL report an error indicating the missing file

### Requirement: meta.md format

`meta.md` SHALL contain YAML frontmatter with the following fields:

- `title` (required): Presentation title
- `subtitle` (optional): Subtitle
- `speaker` (optional): Speaker name
- `date` (optional): Presentation date
- `target_duration` (optional): Total target duration (e.g., "30min")
- `theme` (optional): Theme name, defaulting to "dark"

The Markdown body after the frontmatter MAY contain additional prose (e.g., abstract, description) and SHALL be ignored by the converter.

#### Scenario: Valid meta.md with all fields

- **WHEN** meta.md has YAML frontmatter with title, subtitle, speaker, date, target_duration, and theme
- **THEN** the converter SHALL extract all fields and pass them to the HTML template

#### Scenario: meta.md with only required fields

- **WHEN** meta.md has YAML frontmatter with only `title`
- **THEN** the converter SHALL use defaults for optional fields

### Requirement: outline.md format

`outline.md` SHALL contain a Markdown table with columns: section number, section name, duration, and file path. The table SHALL map each section to its corresponding slide file.

#### Scenario: Valid outline table

- **WHEN** outline.md contains a table with columns `序号 | 章节 | 时长 | 文件`
- **THEN** the converter SHALL parse the table and use it for navigation and timing display

#### Scenario: No outline.md

- **WHEN** a project does not contain `outline.md`
- **THEN** the converter SHALL infer the outline from slides/ directory ordering

### Requirement: Slide file YAML frontmatter

Each file under `slides/` SHALL have YAML frontmatter with the following fields:

- `slide` (required): Slide number
- `duration` (optional): This slide's duration
- `layout` (optional): One of `grid`, `flex`, `stack`, `split`, or `default`
  - When `layout` is `grid`, the following SHALL also be recognized: `cols` (number), `ratio` (string like "1/1" or "60/40"), `gap` (number in px)
  - When `layout` is `flex`, the following SHALL also be recognized: `dir` (row|col), `align` (center|stretch|start|end)
  - When `layout` is `split`, the following SHALL also be recognized: `ratio` (string like "60/40")
- `accent` (optional): Color name mapped to theme color (e.g., blue, green, red)
- `emoji` (optional): Emoji to display alongside the slide heading

#### Scenario: Slide with grid layout

- **WHEN** frontmatter contains `layout: grid`, `cols: 2`, `ratio: "1/1"`
- **THEN** the converter SHALL render the slide body content in a two-column CSS Grid with equal-width columns

#### Scenario: Slide with default layout

- **WHEN** frontmatter contains `layout: default` or omits the `layout` field
- **THEN** the converter SHALL infer layout from the content structure (e.g., two top-level elements → two-column)

#### Scenario: Invalid layout value

- **WHEN** frontmatter contains an unrecognized `layout` value
- **THEN** the converter SHALL fall back to `default` and emit a warning

### Requirement: Slide file Markdown body

The Markdown body of each slide file SHALL contain standard Markdown content. The following elements SHALL be supported:

- Headings (h2/h3/h4)
- Paragraphs, bold, italic, inline code
- Unordered and ordered lists
- Code blocks (fenced with ```)
- Mermaid diagrams (fenced with ```mermaid)
- Tables
- Images with alt text
- Blockquotes
- Custom tags: `<card>`, `<callout>`, `<steps>`, `<step>`

#### Scenario: Slide with cards and callout

- **WHEN** slide body contains Markdown content with `<card>` and `<callout>` tags
- **THEN** the converter SHALL render the content with corresponding CSS classes from the existing theme

#### Scenario: Slide with mermaid diagram

- **WHEN** slide body contains a fenced code block with language `mermaid`
- **THEN** the converter SHALL embed the mermaid diagram with proper container for zoom support

### Requirement: Slide content rendered as HTML

The converter SHALL render slide Markdown body to HTML using a deterministic Markdown parser (Python `markdown` library), then SHALL apply additional transformations:

1. Custom tags (`<card>`, `<callout>`, `<steps>`, `<step>`) SHALL be mapped to corresponding HTML structures with CSS classes
2. Mermaid code blocks SHALL be wrapped in `pre.mermaid` or `div.mermaid` containers
3. The final HTML SHALL use semantic class names for targeting by `override.css`

#### Scenario: Two `<card>` elements

- **WHEN** slide body has two `<card>` elements at the top level
- **THEN** they SHALL be wrapped in a `.card-group` container with `.card` class on each card

#### Scenario: Code block with syntax highlighting

- **WHEN** slide body has a fenced code block with a language tag (e.g., ```python)
- **THEN** the converter SHALL preserve the language tag and apply syntax highlighting class
