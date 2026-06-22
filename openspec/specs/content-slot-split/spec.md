# Content Slot Split

## Purpose

Define how slide body Markdown is split into content slots using `=== slot ===` delimiters, and how slots map to YAML grid cells.

## ADDED Requirements

### Requirement: Body slot splitting

After extracting YAML frontmatter, the converter SHALL split the remaining body text into heading and slots.
Heading SHALL be all content before the first `=== slot ===` line.
The converter SHALL split the body by `=== slot ===` using `rsplit('\n=== slot ===\n', maxsplit=N-1)` where N is the total number of cells in the YAML grid.
Slots are extracted right-to-left: the last `=== slot ===` closest to the end separates the last cell, working backward.

#### Scenario: Body with heading and two slots

- **WHEN** N=2 (2 cells) and body contains `## My Title\n\nSlot 1 content\n\n=== slot ===\n\nSlot 2 content`
- **THEN** the converter SHALL rsplit once: "My Title" as heading, "Slot 1 content" as slot 0, and "Slot 2 content" as slot 1

#### Scenario: Body with heading only

- **WHEN** body contains `## My Title\n\nSome paragraph text.` (no `=== slot ===`)
- **THEN** the heading SHALL be "My Title" and the remaining text SHALL be treated as a single slot

#### Scenario: `=== slot ===` lines inside slot content are preserved

- **WHEN** a slot contains the literal string `=== slot ===` embedded in its content
- **THEN** the text SHALL remain in the slot and SHALL NOT be interpreted as a slot boundary (rsplit from the right only consumes the tailmost N-1 occurrences)

### Requirement: Slot-to-cell mapping

Slots SHALL be assigned to YAML grid cells in row-major order: the first slot maps to the first cell of the first row, the second slot to the second cell, and so on.
If there are more slots than cells, excess slots SHALL be silently ignored.
If there are more cells than slots, cells without corresponding slots SHALL receive empty content.

#### Scenario: Equal slots and cells

- **WHEN** grid has 3 cells and body has 3 slots
- **THEN** each cell SHALL receive the content of its corresponding slot

#### Scenario: Fewer slots than cells

- **WHEN** grid has 3 cells but body has only 2 slots
- **THEN** the third cell SHALL render with empty content

#### Scenario: More slots than cells

- **WHEN** grid has 2 cells but body has 4 slots
- **THEN** only the first 2 slots SHALL be used; remaining slots SHALL be ignored

### Requirement: Per-slot Markdown conversion

Each slot's Markdown content SHALL be independently converted to HTML using the Python `markdown` library.
The converter SHALL apply the same extensions (`extra`, `md_in_html`, `codehilite`, `fenced_code`, `tables`) to each slot as are applied to the full body in the current pipeline.
Mermaid blocks within a slot SHALL be extracted before conversion and restored after (same as current behavior).

#### Scenario: Markdown in slot is converted

- **WHEN** a slot contains `**bold**` and `` `code` ``
- **THEN** the output HTML SHALL contain `<strong>bold</strong>` and `<code>code</code>`

#### Scenario: Mermaid in slot is preserved

- **WHEN** a slot contains a ` ```mermaid ` fenced code block
- **THEN** the output SHALL contain a `<div class="diagram-focusable">` wrapper around the mermaid div

#### Scenario: `<!-- reader -->` block in slot

- **WHEN** a slot contains `<!-- reader -->...<!-- /reader -->`
- **THEN** the converter SHALL split visual and reader layers within that slot and place them in their respective output sections
