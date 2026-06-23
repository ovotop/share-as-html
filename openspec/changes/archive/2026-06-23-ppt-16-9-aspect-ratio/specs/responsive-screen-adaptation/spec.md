## MODIFIED Requirements

### Requirement: PPT mode wider content

In PPT mode, the `.content` element SHALL use a fixed ideal layout size of `width: 1680px` with `aspect-ratio: 16 / 9` (resulting height: 945px) and `transform-origin: center center`. JavaScript SHALL compute and apply `transform: scale()` based on available viewport dimensions, replacing the previous `max-width: 1100px` constraint. The slide SHALL have `padding: 60px 120px` and `overflow: hidden`.

#### Scenario: PPT mode on wide display

- **WHEN** the page is in PPT mode on a display wider than 768px
- **THEN** slide content SHALL be proportionally scaled to fill the available space while maintaining 16:9 layout proportions
- **AND** the slide SHALL have 120px left and right padding

#### Scenario: PPT mode on mobile display

- **WHEN** the page is in PPT mode on a display 768px or narrower
- **THEN** transform scaling SHALL be disabled
- **AND** `.content` SHALL use `width: 100%; aspect-ratio: auto; transform: none`
- **AND** slide padding SHALL be reduced to `40px 20px` with `overflow: visible`

#### Scenario: DOC mode max-width unchanged

- **WHEN** the page is in DOC mode
- **THEN** `.content` SHALL have `max-width: 900px`
