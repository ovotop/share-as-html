# doc-mode-footer

## Purpose

Define the attribution footer that appears at the bottom of documents in DOC (reading) mode, linking back to the ovotop/share-as-html project.

## Requirements

### Requirement: Footer presence in DOC mode

The generated HTML document SHALL contain a footer element with class `.doc-footer` placed after all slide elements. The footer SHALL be visible when the document is in DOC mode (body has no `.mode-ppt` or `.mode-zoom` class).

#### Scenario: Footer visible in DOC mode

- **WHEN** user opens the HTML document (default state is DOC mode)
- **THEN** the footer SHALL be visible at the bottom of the page after all slide content

#### Scenario: Footer visible after switching from PPT to DOC

- **WHEN** user presses Esc in PPT_FULL mode to return to DOC mode
- **THEN** the footer SHALL become visible

### Requirement: Footer hidden in presentation modes

The footer SHALL NOT be visible when the document is in PPT_FULL or PPT_ZOOM mode.

#### Scenario: Footer hidden in PPT mode

- **WHEN** user presses Enter to enter PPT_FULL mode
- **THEN** the footer SHALL be hidden (not visible or interactable)

#### Scenario: Footer hidden in zoom mode

- **WHEN** user enters PPT_ZOOM mode from PPT_FULL
- **THEN** the footer SHALL be hidden

### Requirement: Footer content

The footer SHALL display:

- An ovotop organization icon image sourced from GitHub (`https://avatars.githubusercontent.com/u/166823538?s=32`)
- The text "Powered by ovotop/share-as-html"
- The entire footer SHALL be a hyperlink to `https://github.com/ovotop/share-as-html`

The image SHALL have `alt="ovotop"` for accessibility. The link SHALL open in a new tab (`target="_blank"`) with `rel="noopener"`.

#### Scenario: Footer link opens GitHub in new tab

- **WHEN** user clicks the footer text or icon in DOC mode
- **THEN** the GitHub repository page SHALL open in a new browser tab

#### Scenario: Footer image load failure

- **WHEN** the GitHub avatar image fails to load (network error or blocked)
- **THEN** the alt text "ovotop" SHALL be displayed in place of the image, and the "Powered by" text SHALL remain visible

### Requirement: Footer styling

The footer SHALL use the following visual properties:

- Font size smaller than body text (e.g., 12px)
- Text color using the `--text-dim` CSS variable for subtle appearance
- Centered text alignment
- Vertical inline alignment of icon with text
- Padding/spacing that separates it from the last slide content
- No border or background to avoid visual separation from the DOC reading flow

#### Scenario: Footer matches dark theme

- **WHEN** the document uses the default dark theme
- **THEN** the footer text SHALL use `--text-dim` color and the footer SHALL not introduce any new colors outside the theme variables

### Requirement: Footer placement in DOM

The footer SHALL be placed inside `#scroll-container` as a sibling of `.slide` elements, after the last slide. The footer SHALL NOT be nested inside any `.slide` element.

#### Scenario: Footer after last slide

- **WHEN** the document has N slides
- **THEN** the footer SHALL appear after the Nth `.slide` element in the DOM

### Requirement: Footer does not affect navigation

The footer SHALL NOT interfere with the state machine, keyboard navigation, or scroll behavior in any mode.

#### Scenario: Arrow key navigation unaffected

- **WHEN** user navigates slides with arrow keys in PPT_FULL mode
- **THEN** slide count and navigation behavior SHALL be identical to before the footer was added (footer is hidden and does not count as a slide)

#### Scenario: Enter to PPT mode from footer area

- **WHEN** user scrolls to the bottom of DOC mode where the footer is visible and presses Enter
- **THEN** the document SHALL enter PPT_FULL mode at the nearest slide (not at the footer, which is not a slide)
