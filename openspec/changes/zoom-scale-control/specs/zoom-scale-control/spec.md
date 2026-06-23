# Zoom Scale Control

## Purpose

Define keyboard controls for PPT_ZOOM mode: fit/fill toggle via Enter, and stepped zoom scale adjustment via +/- keys. Content defaults to fit-viewport on entry.

## ADDED Requirements

### Requirement: Default fit-viewport on zoom entry

When entering PPT_ZOOM mode, content SHALL default to fit-viewport ("内接") at 1.0× scale. Content SHALL be constrained to fit entirely within the viewport without cropping.

#### Scenario: Enter zoom from focused diagram

- **WHEN** a user presses Enter on a focused element in PPT_FULL mode
- **THEN** content SHALL display at fit-viewport with 1.0× scale
- **AND** `.zoom-content` SHALL NOT have `.fill` class

### Requirement: Enter toggles fit and fill mode

In PPT_ZOOM mode, Enter SHALL toggle between fit and fill. Toggle SHALL preserve the current scale level.

#### Scenario: Toggle from fit to fill

- **WHEN** a user in PPT_ZOOM fit mode presses Enter
- **THEN** `.zoom-content` SHALL gain `.fill` class and render via `object-fit: cover`

#### Scenario: Toggle preserves scale

- **WHEN** scale is 2.0× and user toggles fit → fill → fit
- **THEN** scale SHALL remain 2.0× throughout

### Requirement: + steps up preset scale levels

`+` SHALL step: 1.0 → 1.25 → 1.5 → 2.0 → 3.0. At 3.0, further presses have no effect.

#### Scenario: Step from 1.0 to 1.25

- **WHEN** scale is 1.0× and user presses `+`
- **THEN** scale SHALL become 1.25×

#### Scenario: Cap at 3.0

- **WHEN** scale is 3.0× and user presses `+`
- **THEN** scale SHALL remain 3.0×

### Requirement: - steps down preset scale levels

`-` SHALL step: 3.0 → 2.0 → 1.5 → 1.25 → 1.0. At 1.0, further presses have no effect.

#### Scenario: Floor at 1.0

- **WHEN** scale is 1.0× and user presses `-`
- **THEN** scale SHALL remain 1.0×

### Requirement: State resets on zoom exit

Re-entering zoom SHALL reset to defaults: fit mode, 1.0× scale.

#### Scenario: Re-enter after adjusting

- **WHEN** user exits at 2.0× fill mode, then re-enters zoom
- **THEN** zoom SHALL start in fit mode at 1.0×

### Requirement: Arrow scrolling works at all scales

Arrow keys SHALL scroll the container at any scale in either mode.

#### Scenario: Scroll at 2.0× fill

- **WHEN** user is at 2.0× fill mode and presses ArrowDown
- **THEN** container SHALL scroll by 100px
