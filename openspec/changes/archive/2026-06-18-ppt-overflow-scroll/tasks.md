## 1. CSS Changes

- [x] 1.1 Change `#scroll-container.mode-ppt` scroll-snap-type from `y mandatory` to `y proximity`
- [x] 1.2 Add `@keyframes slide-bounce-down` animation (translateY: 0 → 8px → 0, 300ms ease-out)
- [x] 1.3 Add `@keyframes slide-bounce-up` animation (translateY: 0 → -8px → 0, 300ms ease-out)
- [x] 1.4 Add `@keyframes slide-bounce-left` animation (translateX: 0 → -8px → 0, 300ms ease-out)
- [x] 1.5 Add `@keyframes slide-bounce-right` animation (translateX: 0 → 8px → 0, 300ms ease-out)
- [x] 1.6 Add `.bounce-down`, `.bounce-up`, `.bounce-left`, `.bounce-right` utility classes applying keyframe animations to `#scroll-container`

## 2. JS State Machine Changes

- [x] 2.1 Add `let isAtScrollBoundary = false` variable next to `let focusedDiagramIndex = -1`
- [x] 2.2 Reset `isAtScrollBoundary` in `navigateSlide()` whenever slide index changes
- [x] 2.3 Reset `isAtScrollBoundary` in `updateFocus()` when `preserveIndex` is false
- [x] 2.4 Reset `isAtScrollBoundary` in `enterPPTMode()` on initial entry

## 3. Scroll Helper Functions

- [x] 3.1 Implement `canScrollVertically(direction)` — returns true if scroll-container can scroll further vertically within current slide
- [x] 3.2 Implement `canScrollHorizontally(direction)` — returns true if scroll-container can scroll further horizontally within focused diagram's bounds
- [x] 3.3 Implement `scrollSlideContent(direction, axis)` — smooth-scrolls `#scroll-container` by 80% of viewport dimension in `axis` ('y' or 'x'); temporarily sets `scroll-snap-type: none` before scroll, restores to `y proximity` after scroll
- [x] 3.4 Implement `triggerBounce(direction, axis)` — adds `.bounce-{direction}` class to `#scroll-container`, removes after 300ms via `setTimeout`

## 4. PPT_FULL Keyboard Handler Update

- [x] 4.1 Update ArrowDown case: if `isAtScrollBoundary` → `navigateSlide(1)` + reset flag; else if `canScrollVertically(1)` → `scrollSlideContent(1, 'y')` + check if now at boundary → set flag + `triggerBounce(1, 'y')`; else → `navigateSlide(1)`
- [x] 4.2 Update ArrowUp case: mirror of ArrowDown with `canScrollVertically(-1)`, `scrollSlideContent(-1, 'y')`, `triggerBounce(-1, 'y')`
- [x] 4.3 Update ArrowRight case: if `isAtScrollBoundary` AND multiple focusables → `handleFocusSwitch('ArrowRight')` + reset flag; else if `canScrollHorizontally(1)` → `scrollSlideContent(1, 'x')` + boundary check + bounce; else → `handleFocusSwitch('ArrowRight')` (current behavior)
- [x] 4.4 Update ArrowLeft case: mirror of ArrowRight with `canScrollHorizontally(-1)`, `scrollSlideContent(-1, 'x')`, `triggerBounce(-1, 'x')`
- [x] 4.5 When any arrow key scrolls content (not navigating/switching focus), reset `isAtScrollBoundary` to false before scrolling (moving away from boundary)
- [x] 4.6 Keep `e.preventDefault()` for all arrow keys in PPT_FULL

## 5. Template Update (SKILL.md)

- [x] 5.1 Update `#scroll-container.mode-ppt` CSS in SKILL.md template (proximity + new keyframes × 4 + bounce classes)
- [x] 5.2 Update JS state variable block in SKILL.md template (add `isAtScrollBoundary`)
- [x] 5.3 Update PPT_FULL keyboard handler section in SKILL.md template (new ArrowDown/ArrowUp + ArrowLeft/ArrowRight logic)
- [x] 5.4 Add `canScrollVertically`, `canScrollHorizontally`, `scrollSlideContent`, `triggerBounce` functions to SKILL.md template
- [x] 5.5 Update keyboard reference table in SKILL.md: ArrowDown/ArrowUp in PPT → "Scroll content / Next/Prev slide"; ArrowLeft/ArrowRight → "Scroll content / Switch focus"

## 6. HTML File Regeneration

- [x] 6.1 Regenerate `test-mermaid-zoom.html` from updated SKILL.md template
- [x] 6.2 Regenerate `test-image-zoom.html` from updated SKILL.md template
- [x] 6.3 Regenerate `test-focus-matrix.html` from updated SKILL.md template
- [x] 6.4 Regenerate `ai-agent-tools.html` from updated SKILL.md template
- [x] 6.5 Regenerate `sharing-doc-test.html` from updated SKILL.md template

## 7. Test Update

- [x] 7.1 Add test case: "PPT_FULL: ArrowDown scrolls within oversized slide before advancing" to `test-automated.spec.js`
- [x] 7.2 Add test case: "PPT_FULL: Second ArrowDown at boundary advances slide" to `test-automated.spec.js`
- [x] 7.3 Add test case: "PPT_FULL: ArrowUp scrolls back within oversized slide" to `test-automated.spec.js`
- [x] 7.4 Add test case: "PPT_FULL: Normal slide advances immediately on ArrowDown"
- [x] 7.5 Add test case: "PPT_FULL: ArrowRight scrolls horizontally within wide diagram"
- [x] 7.6 Add test case: "PPT_FULL: Second ArrowRight at horizontal boundary switches focus"
- [x] 7.7 Add test case: "PPT_FULL: ArrowLeft scrolls horizontally back"
- [x] 7.8 Add test case: "Boundary flag resets on slide change"
- [x] 7.9 Add test case: "No horizontal overflow switches focus immediately"
- [x] 7.10 Run `npx playwright test test-automated.spec.js` and verify all tests pass

## 8. Verification

- [x] 8.1 Manual test: open `test-mermaid-zoom.html`, Enter PPT mode, navigate to large mermaid slide, verify ArrowDown smooth-scrolls content
- [x] 8.2 Manual test: verify bounce animation plays when scroll hits bottom
- [x] 8.3 Manual test: verify second ArrowDown advances to next slide
- [x] 8.4 Manual test: verify normal (non-oversized) slides still advance immediately
- [x] 8.5 Manual test: verify ArrowUp symmetric behavior
