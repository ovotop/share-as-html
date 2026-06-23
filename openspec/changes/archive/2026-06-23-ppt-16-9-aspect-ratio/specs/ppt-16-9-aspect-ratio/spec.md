## ADDED Requirements

### Requirement: Fixed-layout content with proportional transform scaling

In PPT mode, the `.content` element SHALL use a fixed ideal layout size of 1680px × 945px (16:9 ratio derived from a 1920×1080 reference viewport with 120px side margins). At runtime, JavaScript SHALL compute a `scale` factor based on the available viewport dimensions and apply `transform: scale()` to proportionally scale the content up or down while preserving layout proportions.

#### Scenario: Content scales to fill available space

- **WHEN** the document is in PPT mode on a display where `container.clientWidth - 240` differs from the ideal 1680px
- **THEN** the content SHALL be proportionally scaled via `transform: scale()` so it fills as much of the slide as possible without distortion
- **AND** the computed scale SHALL be `min((container.clientWidth - 240) / 1680, (container.clientHeight - 120) / 945)`

#### Scenario: Content layout preserved at all scales

- **WHEN** content is scaled up or down via transform
- **THEN** text line lengths, grid columns, and element spacing SHALL remain identical to the ideal 1680×945 layout
- **AND** fonts SHALL scale proportionally with the content

#### Scenario: Content vertically centered in slide

- **WHEN** the scaled content area is shorter than the slide height
- **THEN** the content SHALL be vertically centered within the slide via flexbox `justify-content: center`

### Requirement: 120px fixed side margins in PPT mode

In PPT mode, the `.slide` element SHALL have `padding: 60px 120px` (60px vertical, 120px horizontal) to provide fixed side margins that frame the content area.

#### Scenario: Side margins on desktop

- **WHEN** the document is in PPT mode on a display wider than 768px
- **THEN** the slide SHALL have 120px left and right padding

### Requirement: Overflow clipping on slides in PPT mode

In PPT mode, the `.slide` element SHALL use `overflow: hidden` to clip any visual overflow from scaled content extending beyond the slide bounds.

#### Scenario: Scaled content clipped at slide boundary

- **WHEN** transform scaling causes content to visually extend beyond the slide's border box
- **THEN** the overflowing visual content SHALL be clipped at the slide boundary

### Requirement: Transform scaling disabled on mobile

On narrow viewports (≤768px), transform scaling SHALL be disabled and the content SHALL use full-width layout.

#### Scenario: Mobile resets to full-width

- **WHEN** the viewport width is 768px or less
- **THEN** `.content` SHALL have `width: 100%; aspect-ratio: auto; transform: none`
- **AND** `.slide` SHALL have `padding: 40px 20px; overflow: visible`

### Requirement: Transform scaling only in PPT mode

The `updateContentScale()` function SHALL only apply transform scaling when `currentState === 'PPT_FULL'`. Transforms SHALL be cleared when exiting PPT mode.

#### Scenario: DOC mode unaffected by transform

- **WHEN** the document is in DOC mode
- **THEN** no `transform: scale()` SHALL be applied to any `.content` element

#### Scenario: Transforms cleared on exit

- **WHEN** user exits PPT mode to DOC mode
- **THEN** all inline `transform` styles on `.slide .content` elements SHALL be reset to `''`

### Requirement: Slide number at bottom-right

The `.slide-number` element SHALL be positioned at the bottom-right corner of the slide using `bottom: 24px; right: 32px`.

#### Scenario: Slide number visible at bottom-right

- **WHEN** a slide contains a `.slide-number` element
- **THEN** the number SHALL appear at the bottom-right corner of the slide

### Requirement: Slide number z-index above content

The `.slide-number` element SHALL have `z-index: 1` to render above `.content` elements that may create stacking contexts via CSS `transform`.

#### Scenario: Number visible above scaled content

- **WHEN** `.content` has `transform: scale()` creating a stacking context
- **THEN** `.slide-number` SHALL render above the content and remain visible
