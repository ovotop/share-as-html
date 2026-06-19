## ADDED Requirements

### Requirement: ArrowDown scrolls within oversized slide before advancing

In PPT_FULL mode, when the current slide's content exceeds the viewport height, pressing ArrowDown SHALL smooth-scroll the content vertically within the scroll-container instead of advancing to the next slide.

#### Scenario: Large Mermaid diagram partial scroll
- **WHEN** the current slide contains a Mermaid diagram taller than the viewport AND the slide is not scrolled to its bottom
- **THEN** pressing ArrowDown SHALL scroll the scroll-container down by 80% of the viewport height with smooth behavior
- **AND** the slide index SHALL NOT change

#### Scenario: Scroll reaches slide bottom on first press
- **WHEN** pressing ArrowDown causes the scroll position to reach or exceed the current slide's bottom boundary
- **THEN** the scroll-container SHALL stop at the slide bottom
- **AND** a bounce animation SHALL play on the scroll-container for 300ms
- **AND** the `isAtScrollBoundary` flag SHALL be set to `true`
- **AND** the slide index SHALL NOT change

#### Scenario: Second ArrowDown at bottom boundary advances slide
- **WHEN** the `isAtScrollBoundary` flag is `true` AND the user presses ArrowDown
- **THEN** the system SHALL advance to the next slide via `navigateSlide(1)`
- **AND** the `isAtScrollBoundary` flag SHALL be reset to `false`

#### Scenario: Normal slide advances immediately
- **WHEN** the current slide content fits entirely within the viewport (no vertical overflow)
- **THEN** pressing ArrowDown SHALL immediately advance to the next slide via `navigateSlide(1)`

### Requirement: ArrowUp scrolls within oversized slide before retreating

In PPT_FULL mode, when the current slide's content exceeds the viewport height, pressing ArrowUp SHALL smooth-scroll the content upward before retreating to the previous slide.

#### Scenario: Large Mermaid diagram scroll up
- **WHEN** the current slide contains content taller than the viewport AND the slide is scrolled away from its top
- **THEN** pressing ArrowUp SHALL scroll the scroll-container up by 80% of the viewport height with smooth behavior

#### Scenario: Scroll reaches slide top on first press
- **WHEN** pressing ArrowUp causes the scroll position to reach or pass the current slide's top boundary
- **THEN** the scroll-container SHALL stop at the slide top
- **AND** a bounce animation SHALL play
- **AND** the `isAtScrollBoundary` flag SHALL be set to `true`

#### Scenario: Second ArrowUp at top boundary retreats slide
- **WHEN** the `isAtScrollBoundary` flag is `true` AND the user presses ArrowUp
- **THEN** the system SHALL retreat to the previous slide via `navigateSlide(-1)`
- **AND** the `isAtScrollBoundary` flag SHALL be reset to `false`

### Requirement: ArrowLeft/ArrowRight scroll horizontally within wide focused diagram

In PPT_FULL mode, when the currently focused `diagram-focusable` element's content exceeds the viewport width, pressing ArrowLeft or ArrowRight SHALL smooth-scroll the scroll-container horizontally instead of switching focus.

#### Scenario: Large image horizontal scroll right
- **WHEN** the focused diagram has content wider than the viewport AND the container is not scrolled to the right boundary
- **THEN** pressing ArrowRight SHALL scroll the scroll-container right by 80% of the viewport width with smooth behavior
- **AND** the focused diagram index SHALL NOT change

#### Scenario: Horizontal scroll reaches right boundary on first press
- **WHEN** pressing ArrowRight causes the horizontal scroll position to reach the focused diagram's right boundary
- **THEN** the scroll-container SHALL stop at the right boundary
- **AND** a horizontal bounce animation SHALL play
- **AND** the `isAtScrollBoundary` flag SHALL be set to `true`

#### Scenario: Second ArrowRight at right boundary switches focus
- **WHEN** the `isAtScrollBoundary` flag is `true` AND the user presses ArrowRight AND multiple focusable diagrams exist on the slide
- **THEN** the system SHALL switch focus to the next diagram via `handleFocusSwitch('ArrowRight')`
- **AND** the `isAtScrollBoundary` flag SHALL be reset to `false`

#### Scenario: Single focusable diagram at boundary does nothing
- **WHEN** the `isAtScrollBoundary` flag is `true` AND there is only one focusable diagram on the slide
- **THEN** pressing ArrowRight SHALL have no effect (all content viewed, no further focusables)

#### Scenario: No horizontal overflow switches focus immediately
- **WHEN** the focused diagram fits entirely within the viewport width
- **THEN** pressing ArrowRight or ArrowLeft SHALL immediately switch focus via `handleFocusSwitch` (existing behavior preserved)

### Requirement: Boundary flag resets on scroll direction change or slide change

The `isAtScrollBoundary` flag SHALL be reset to `false` whenever:
- The slide index changes (via any navigation method)
- `updateFocus()` is called during a slide transition
- The user scrolls in the opposite direction (moving away from boundary)
- The user scrolls in a perpendicular direction (switching from vertical to horizontal or vice versa)

#### Scenario: ArrowDown after changing slides via keyboard
- **WHEN** the user navigates to a new slide (via ArrowDown advance or ArrowUp retreat)
- **THEN** `isAtScrollBoundary` SHALL be `false` regardless of the new slide's scroll position

### Requirement: Scroll-snap relaxation in PPT mode

The `#scroll-container.mode-ppt` CSS SHALL use `scroll-snap-type: y proximity` instead of `y mandatory` to allow intermediate scroll positions within oversized slides.

#### Scenario: Partial scroll position preserved
- **WHEN** the user scrolls to a mid-slide position within an oversized slide
- **THEN** the browser SHALL NOT force-snap to the slide boundary
- **AND** the position SHALL persist until the user scrolls again or changes slides

### Requirement: SKILL.md template SHALL include new CSS and JS

The SKILL.md template (`/home/mi/.opencode/skills/sharing-in-html/SKILL.md`) SHALL be updated to include:
- Updated `#scroll-container.mode-ppt` CSS with `scroll-snap-type: y proximity`
- New `@keyframes slide-bounce-down` and `slide-bounce-up` CSS animations
- New `@keyframes slide-bounce-left` and `slide-bounce-right` CSS animations for horizontal bounce
- New `isAtScrollBoundary` variable in the JS state machine
- Updated PPT_FULL ArrowDown/ArrowUp handler with vertical scroll-within-slide logic
- Updated PPT_FULL ArrowLeft/ArrowRight handler with horizontal scroll + focus-switch logic
- New `canScrollVertically(direction)` helper function
- New `canScrollHorizontally(direction)` helper function
- New `scrollSlideContent(direction, axis)` helper function (supports 'y' and 'x' axes)
- New `triggerBounce(direction, axis)` helper function
- Updated keyboard reference table

#### Scenario: Template generates functional HTML
- **WHEN** an HTML file is generated using the updated SKILL.md template
- **THEN** the file SHALL support ArrowDown/ArrowUp scroll-within-slide behavior for oversized slides in PPT mode
- **AND** the file SHALL support bounce feedback at scroll boundaries
