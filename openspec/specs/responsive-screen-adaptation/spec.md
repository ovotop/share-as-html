# Responsive Screen Adaptation

## Purpose

Define the responsive design behavior of share-as-html documents across screen sizes. This spec ensures content is readable and well-presented on everything from mobile phones (375px) to 4K displays (3840px), using fluid typography, horizontal centering, and simplified breakpoints.

## Requirements

### Requirement: Content horizontal centering

All slides SHALL center their content horizontally. The `.slide` container SHALL use `align-items: center` to center the child `.content` element within the viewport.

#### Scenario: Large screen centering

- **WHEN** the page is viewed on a display wider than 900px
- **THEN** the slide content SHALL be horizontally centered within the viewport

#### Scenario: Small screen centering

- **WHEN** the page is viewed on a display narrower than 900px
- **THEN** the slide content SHALL fill the available width (via `width: 100%`)

### Requirement: Fluid typography with clamp()

All heading and body text SHALL use CSS `clamp()` for font-size to scale smoothly across screen sizes without hard breakpoints:

- `h2`: `clamp(24px, 4vw, 36px)`
- `h3`: `clamp(17px, 2.5vw, 22px)`
- `p, li`: `clamp(14px, 1.5vw, 16px)`
- `.cover h1`: `clamp(32px, 5vw, 48px)`
- `.card h4`: `clamp(14px, 1.5vw, 16px)`

#### Scenario: Phone display (375px)

- **WHEN** the page is viewed on a 375px-wide phone
- **THEN** h2 SHALL render at approximately 24px (the MIN clamp value)

#### Scenario: 4K display (3840px)

- **WHEN** the page is viewed on a 3840px-wide display
- **THEN** h2 SHALL render at 36px (the MAX clamp value, not larger)

#### Scenario: Tablet display (1024px)

- **WHEN** the page is viewed on a 1024px-wide tablet
- **THEN** h2 SHALL render at approximately 36px (4vw × 1024 ≈ 41px, capped at MAX 36px)

### Requirement: PPT mode transform scaling

In PPT mode, the `.content` element SHALL use a fixed ideal layout size of `width: 1680px` with `aspect-ratio: 16 / 9` (resulting height: 945px) and `transform-origin: center center`. JavaScript SHALL compute and apply `transform: scale()` based on available viewport dimensions, proportionally scaling content while preserving layout proportions. The slide SHALL have `padding: 60px 120px` and `overflow: hidden`.

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

### Requirement: Simplified media query

The `@media (max-width: 768px)` breakpoint SHALL only contain structural adjustments:
- Reduced slide padding
- Grid columns collapsing to single column
- Flex row collapsing to column

Font-size overrides SHALL be removed from this breakpoint, as `clamp()` handles all font scaling.

#### Scenario: No font-size in media query

- **WHEN** the CSS is inspected
- **THEN** `@media (max-width: 768px)` SHALL NOT contain `font-size` declarations for h2, h3, .cover h1, or any text element

### Requirement: mermaid diagram adaptation

Mermaid SVG diagrams SHALL continue to use `max-width: 100%; height: auto` to prevent horizontal overflow on small screens. The zoom behavior in PPT mode SHALL remain functional.

#### Scenario: Mermaid on phone

- **WHEN** a mermaid diagram is displayed on a 375px-wide phone
- **THEN** the SVG SHALL scale to fit within the viewport without horizontal scroll
