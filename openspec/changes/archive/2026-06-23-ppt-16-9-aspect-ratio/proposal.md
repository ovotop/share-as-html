## Why

PPT mode currently has no aspect ratio constraint — slides fill the entire viewport height and the content is capped at `max-width: 1100px`. On 4K displays (3840px wide), this wastes ~70% of the viewport, leaving a narrow content strip centered in a vast empty space. Adding a 16:9 content area constraint with fixed side margins makes presentations look polished on all screen sizes, matching mainstream presentation formats.

## What Changes

- **16:9 content area**: `.content` element in PPT mode gets `aspect-ratio: 16/9`, constrained by slide dimensions with 120px fixed side margins
- **Slide number reposition**: `.slide-number` moves from top-right to bottom-right corner (`bottom: 24px` instead of `top: 24px`)
- Spec updates to `responsive-screen-adaptation` and `md-to-html-pipeline` to reflect the new layout constraints

## Capabilities

### New Capabilities

- `ppt-16-9-aspect-ratio`: PPT mode constrains the content area to a 16:9 aspect ratio, centers it within the slide, and applies fixed 120px horizontal margins for visual framing. On wide screens (including 4K), content displays as large as possible within the 16:9 constraint while maintaining side borders.

### Modified Capabilities

- `responsive-screen-adaptation`: Update "PPT mode wider content" requirement (lines 48–60) — replace the flat `max-width: 1100px` with 16:9 aspect ratio + fixed margin constraints
- `md-to-html-pipeline`: Update CSS requirement (line 99) — replace `body.mode-ppt .slide .content { max-width: 1100px; }` with the 16:9 approach

## Impact

- **Template**: `skills/share-as-html/scripts/md2html.py` CSS_TEMPLATE — `body.mode-ppt .slide .content` rule and `.slide-number` rule
- **Test fixtures**: 5 test HTML files (test-focus-matrix.html, ai-agent-tools.html, sharing-doc-test.html, test-image-zoom.html, test-mermaid-zoom.html) — mirror the same CSS changes
- **Output docs**: example-talk/output/sharing.html — regenerated from template
- **Not affected**: sharing-preview.html (no PPT mode)
- **Tests**: Playwright tests should pass with no changes — snap navigation, arrow keys, and zoom behavior are independent of content width
