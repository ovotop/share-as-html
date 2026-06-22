## ADDED Requirements

### Requirement: Visual layer and reader layer separation

Each slide file SHALL support two content layers:

- **Visual layer**: Content appearing before the `<!-- reader -->` marker. Displayed in both PPT mode and DOC mode.
- **Reader layer**: Content between `<!-- reader -->` and `<!-- /reader -->` markers. Hidden in PPT mode, displayed in DOC mode.

If no `<!-- reader -->` marker exists, the entire Markdown body SHALL be treated as visual layer content.

#### Scenario: Slide with both layers

- **WHEN** a slide file contains heading and cards before `<!-- reader -->`, and prose between `<!-- reader -->` and `<!-- /reader -->`
- **THEN** in PPT mode the prose SHALL be hidden; in DOC mode the prose SHALL appear as flowing paragraphs

#### Scenario: Slide without reader layer

- **WHEN** a slide file has no `<!-- reader -->` marker
- **THEN** the entire content SHALL appear in both PPT and DOC modes

### Requirement: DOC mode rendering

In DOC mode, reader layer content SHALL be interleaved with visual layer content to form a coherent article:

1. Reader prose SHALL appear as standard paragraphs before, between, or after visual blocks
2. Visual blocks (cards, diagrams, code) SHALL be embedded at the position where they appear in the Markdown
3. The resulting flow SHALL read like a self-contained document understandable without audio narration

#### Scenario: Reader layer provides context before diagram

- **WHEN** reader layer contains explanatory prose before a mermaid diagram
- **THEN** in DOC mode the prose SHALL appear before the diagram, forming a natural reading flow

#### Scenario: Reader layer summarizes after cards

- **WHEN** reader layer contains a summary paragraph after a set of cards
- **THEN** in DOC mode the summary SHALL appear after the card group

### Requirement: PPT mode rendering

In PPT mode:

- Each slide file SHALL produce one full-screen slide
- Only visual layer content SHALL be displayed
- Reader layer content (`<!-- reader -->` blocks) SHALL be completely hidden (not just transparent — not in DOM for PPT mode, or `display: none`)
- Arrow keys SHALL navigate between slides
- The existing three-state state machine (DOC → PPT_FULL → PPT_ZOOM) SHALL be preserved

#### Scenario: PPT mode hides reader prose

- **WHEN** user is in PPT mode and a slide has reader layer content
- **THEN** the reader layer content SHALL NOT be visible or interactable

#### Scenario: Enter transitions between slides

- **WHEN** user is in PPT mode and presses ArrowDown
- **THEN** the view SHALL snap to the next slide, with reader layer hidden

### Requirement: Visual block integration in both modes

Visual blocks (headings, `<card>`, `<callout>`, mermaid diagrams, code blocks, tables, images) SHALL be displayed in both PPT mode and DOC mode. Their rendering SHALL be identical in both modes, using the same CSS classes and theme.

#### Scenario: Card appearance consistent across modes

- **WHEN** a slide has a `<card>` element
- **THEN** the card SHALL have the same visual style (background, border, padding) in both DOC and PPT modes

### Requirement: Mode transition preserves slide position

When switching between DOC and PPT modes, the viewer SHALL land on the same slide they were viewing:

- DOC → PPT: The first visible slide in the viewport SHALL become the current PPT slide
- PPT → DOC: The view SHALL scroll to the same slide's position in the DOC layout

#### Scenario: Switch from DOC to PPT mid-document

- **WHEN** user scrolls to slide 3 in DOC mode and presses Enter
- **THEN** PPT mode SHALL open with slide 3 displayed
