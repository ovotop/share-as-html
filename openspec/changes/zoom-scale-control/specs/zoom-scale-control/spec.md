# Zoom Scale Control

## Purpose

Define keyboard controls for PPT_ZOOM mode: unified dynamic scale line, fit/fill rendering derived from scale position, Enter = fit ↔ fillStep binary jump, Arrow keys locked within zoom container.

## ADDED Requirements

### Requirement: Default fit-viewport on zoom entry

When entering PPT_ZOOM mode, content SHALL default to fit-viewport ("内接") at 1.0× scale. Content SHALL be constrained to fit entirely within the viewport without cropping.

#### Scenario: Enter zoom from focused diagram

- **WHEN** a user presses Enter on a focused element in PPT_FULL mode
- **THEN** content SHALL display at fit-viewport with 1.0× scale
- **AND** `.zoom-content` SHALL NOT have `.fill` class

### Requirement: Dynamic scale line construction

On zoom entry, a unified scale line SHALL be built by computing `fillX = max(vw/natW, vh/natH)`, clamping to [1.25, 3.0], and inserting into the base sequence [1.0, 1.25, 1.5, 2.0, 3.0] with deduplication (diff < 0.01). The resulting array SHALL be sorted ascending and used for all +/- navigation.

#### Scenario: Content smaller than viewport

- **WHEN** content natural size is 1200×800 and viewport is 1920×1080
- **THEN** `fillX` SHALL be computed as `max(1920/1200, 1080/800)` = 1.6
- **AND** scale line SHALL be `[1.0, 1.25, 1.5, 1.6, 2.0, 3.0]`

#### Scenario: Content near viewport size

- **WHEN** `fillX` computes to 1.08 (less than 1.25 clamp floor)
- **THEN** `fillStepScale` SHALL be 1.25
- **AND** scale line SHALL be `[1.0, 1.25, 1.5, 2.0, 3.0]` (no duplicate)

### Requirement: Fill rendering derived from scale position

The `.fill` class SHALL be automatically applied to `.zoom-content` when `zoomScale >= fillStepScale`. It SHALL NOT be controlled by an independent toggle variable. At scales below `fillStepScale`, `.fill` SHALL be absent and fit CSS rules apply.

#### Scenario: Scale at fill threshold

- **WHEN** user steps to `fillStepScale` (e.g., 2.4×)
- **THEN** `.zoom-content` SHALL gain `.fill` class
- **AND** `width`/`height` + `object-fit: cover` SHALL be used

#### Scenario: Scale below fill threshold

- **WHEN** scale is 1.5× and `fillStepScale` is 2.4
- **THEN** `.zoom-content` SHALL NOT have `.fill` class
- **AND** `max-width`/`max-height` constraints SHALL be used

### Requirement: Enter quick-toggles fit and fill step

In PPT_ZOOM mode, Enter SHALL perform a binary jump:
- If currently at scale 1.0 (fit anchor) → jump to `fillStepScale`
- If currently at any other scale (including fill step) → jump back to 1.0

#### Scenario: Enter from fit anchor

- **WHEN** scale is 1.0× and user presses Enter
- **THEN** scale SHALL become `fillStepScale` (e.g., 2.4×)
- **AND** `.zoom-content` SHALL gain `.fill` class (derived from scale position)

#### Scenario: Enter from fill step

- **WHEN** scale is `fillStepScale` (2.4×) and user presses Enter
- **THEN** scale SHALL become 1.0×
- **AND** `.zoom-content` SHALL lose `.fill` class

### Requirement: + steps up dynamic scale line

`+` SHALL advance one position in the element's dynamic scale line. At the maximum position, further presses have no effect.

#### Scenario: Step through dynamic line

- **WHEN** scale line is `[1.0, 1.25, 1.5, 1.6, 2.0, 3.0]` and current scale is 1.25
- **AND** user presses `+`
- **THEN** scale SHALL become 1.5

#### Scenario: Cap at max

- **WHEN** current scale is the maximum in the scale line and user presses `+`
- **THEN** scale SHALL remain unchanged

### Requirement: - steps down dynamic scale line

`-` SHALL retreat one position in the element's dynamic scale line. At 1.0, further presses have no effect.

#### Scenario: Floor at 1.0

- **WHEN** scale is 1.0× and user presses `-`
- **THEN** scale SHALL remain 1.0×

### Requirement: Arrow keys locked in zoom

In PPT_ZOOM mode, Arrow keys SHALL scroll the `.zoom-container` only. Arrow keys SHALL NOT exit zoom mode and SHALL NOT navigate slides. Escape is the only way to exit zoom.

#### Scenario: ArrowDown at scroll boundary

- **WHEN** `.zoom-container` is at vertical scroll bottom and user presses ArrowDown
- **THEN** container SHALL NOT scroll further
- **AND** zoom mode SHALL persist (currentState remains PPT_ZOOM)
- **AND** slide index SHALL NOT change

#### Scenario: ArrowUp at scroll top boundary

- **WHEN** `.zoom-container` is at scroll top and user presses ArrowUp
- **THEN** container SHALL NOT scroll further
- **AND** zoom mode SHALL persist

#### Scenario: ArrowRight at horizontal boundary

- **WHEN** `.zoom-container` is at horizontal scroll end and user presses ArrowRight
- **THEN** container SHALL NOT scroll further
- **AND** zoom mode SHALL persist

#### Scenario: ArrowLeft at horizontal boundary

- **WHEN** `.zoom-container` is at horizontal scroll start and user presses ArrowLeft
- **THEN** container SHALL NOT scroll further
- **AND** zoom mode SHALL persist

### Requirement: Bounce animation at zoom scroll boundary

When Arrow key reaches a scroll boundary in `.zoom-container`, a brief bounce animation SHALL play on `.zoom-container` to provide tactile feedback that the boundary was reached.

#### Scenario: Bounce at bottom boundary

- **WHEN** ArrowDown is pressed at vertical scroll bottom
- **THEN** `.zoom-container` SHALL show a brief downward bounce animation

### Requirement: State resets on zoom exit

Re-entering zoom SHALL reconstruct the scale line from the new element and reset to defaults: 1.0×, fit rendering.

#### Scenario: Re-enter after adjusting

- **WHEN** user exits at 2.0× fill mode on element A, then enters zoom on element B
- **THEN** element B's scale line SHALL be computed from B's dimensions
- **AND** zoom SHALL start in fit at 1.0×

### Requirement: Scale line recomputed per element

Scale line SHALL be recomputed each time `enterZoomMode()` is called, using the focused element's natural dimensions. Different elements SHALL have different scale lines.

#### Scenario: Two elements with different sizes

- **WHEN** element A is 1200×800 and element B is 400×300
- **THEN** entering zoom on A produces fillStep ≈ 1.6
- **AND** entering zoom on B produces fillStep ≈ 3.0 (clamped from larger raw value)
