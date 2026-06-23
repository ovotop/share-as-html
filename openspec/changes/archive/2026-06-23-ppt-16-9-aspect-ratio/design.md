## Context

PPT mode currently fills the full viewport: `.slide` uses `min-height: 100vh`, `.content` is capped at `max-width: 1100px`. No aspect ratio constraint exists. On 4K displays (3840×2160), content occupies a narrow 1100px strip — ~29% of the viewport width. 

The user wants a 16:9 content area with 120px fixed side margins that maximizes display area on large screens. The slide-number indicator should also move to bottom-right.

The CSS lives in `md2html.py` CSS_TEMPLATE (lines 30–486) and is duplicated across 5 hand-authored test HTML files. The responsive spec (`responsive-screen-adaptation`) and pipeline spec (`md-to-html-pipeline`) encode the current 1100px constraint.

## Goals / Non-Goals

**Goals:**
- Constrain `.content` area in PPT mode to 16:9 aspect ratio
- Apply 120px fixed horizontal padding to `.slide` in PPT mode (was 80px)
- Content area fills as much space as possible within 16:9 bounds
- Reposition `.slide-number` from top-right to bottom-right
- Maintain existing PPT mode behavior: scroll-snap navigation, arrow keys, zoom

**Non-Goals:**
- Slide-level 16:9 (only content area is constrained — slide remains `min-height: 100vh`)
- Configurable aspect ratio (hardcoded 16:9, no YAML frontmatter parameter)
- Changes to DOC mode layout or responsive typography (clamp() values unchanged)
- Changes to zoom mode or focus behavior
- sharing-preview.html (has no PPT mode)

## Decisions

### D1: Apply `aspect-ratio` to `.content`, not `.slide`

**Rationale**: User explicitly chose "Content area only is 16:9." The slide container stays `min-height: 100vh` to preserve scroll-snap behavior and viewport-filling feel. The `.content` element gets `aspect-ratio: 16/9` so it's a 16:9 card centered within the slide.

**Alternative considered**: `aspect-ratio` on `.slide` itself — would letterbox the entire slide, creating visible bars above/below on non-16:9 screens. Rejected because it breaks the immersive full-viewport PPT feel.

### D2: Disable 16:9 on mobile via media query

**Rationale**: On narrow screens (≤768px), 16:9 produces an impractically short content area. Example: 375px phone with 20px padding → content width 335px → height 188px in a 768px viewport. The existing responsive breakpoint resets `aspect-ratio: auto` to restore full-width content on mobile.

```css
body.mode-ppt .slide { padding: 60px 120px; }
body.mode-ppt .slide .content { aspect-ratio: 16 / 9; width: 100%; }

@media (max-width: 768px) {
    body.mode-ppt .slide { padding: 40px 20px; }
    body.mode-ppt .slide .content { aspect-ratio: auto; }
}
```

### D3: Side margins via `.slide` padding, not margin/border

**Rationale**: `.slide` already uses `padding: 60px 80px` for internal spacing. Increasing the horizontal padding to 120px provides the fixed side margins naturally, without adding new CSS properties. The `.content` element inside the padded slide naturally respects these margins since it's a flex child.

**Alternative considered**: Adding a new wrapper `div` with `margin: 0 120px` — adds DOM complexity for no benefit.

### D4: Remove `max-width: 1100px` on `.content` in PPT mode

**Rationale**: The old 1100px cap conflicts with 16:9 — on large screens, 16:9 would compute a much wider content area. Removing `max-width` lets `aspect-ratio` + slide padding determine content width. On typical 1080p screens (1920px), content width = 1920 - 240 = 1680px, comfortable for reading.

### D5: Slide number: change `top: 24px` → `bottom: 24px`

**Rationale**: One-line CSS change. Bottom-right is more conventional for slide numbering (matches PowerPoint/Keynote convention). No DOM or JS changes needed.

## Risks / Trade-offs

**[R1] Content overflow on very tall slides** → Content with 16:9 aspect ratio is height-constrained by width. If a slide has more content than fits vertically in the 16:9 box, it will overflow. Mitigation: users should split long content across slides (already best practice for presentations). No automatic overflow handling added — relies on author discipline.

**[R2] Test file drift widens** → Test files are already missing `align-items: center` and `max-width: 1100px` that md2html.py has. Adding more divergent changes increases drift. Mitigation: apply identical CSS changes to all 5 test files in this change. Long-term: consider regenerating test files from template.

**[R3] Narrow content on 16:10 / ultrawide screens** → On 16:10 (2560×1600), content width = 2560 - 240 = 2320px, height = 1305px. Tall enough. On ultrawide (3440×1440), content = 3200px × 1800px — exceeds viewport height. The `max-height: calc(100vh - 120px)` guard prevents overflow. However, the content will be height-capped rather than width-capped — on ultrawide displays the content may not extend to full width.

## Migration Plan

1. Edit `md2html.py` CSS_TEMPLATE: update `body.mode-ppt .slide` padding, `.content` aspect-ratio, responsive breakpoint, and `.slide-number` position
2. Apply identical changes to 5 test HTML files
3. Regenerate `example-talk/output/sharing.html`
4. Run Playwright tests to verify scroll-snap, arrow navigation, and zoom still work
5. Build verification: `npx playwright test --grep "sharing-doc-test"`

No rollback complexity — CSS-only changes, revert to previous values.
