## Context

The sharing-in-html skill generates self-contained HTML documents with a three-state mode system (DOC → PPT_FULL → PPT_ZOOM). Currently there is no attribution or branding in any mode. The proposed footer adds subtle project attribution visible only in DOC (reading) mode.

The existing HTML structure uses `<div id="scroll-container">` wrapping `<div class="slide">` elements. Mode is tracked via `body` CSS classes (`mode-ppt`, `mode-zoom`). In DOC mode, the body has no special class.

## Goals / Non-Goals

**Goals:**
- Display a subtle "Powered by" footer at the bottom of DOC mode pages
- Include the ovotop organization icon and a link to the GitHub repository
- Footer must be hidden in PPT_FULL and PPT_ZOOM modes
- Style must match the existing dark theme (subtle colors, small text)
- Footer must be positioned after all slide content, not overlapping any content
- Link must be functional (clickable, opens in new tab)
- Must be replicated across all test HTML files (AGENTS.md requirement: all 5 files share identical JS and CSS)

**Non-Goals:**
- No attribution in PPT or ZOOM presentation modes
- No configuration option to disable the footer (always present)
- No hover animations or interactive effects beyond the link
- No modification to the scroll/snap behavior

## Decisions

**Decision 1: Use a dedicated `.doc-footer` div placed outside slides but inside `#scroll-container`**

The footer is placed as a sibling of slides inside the scroll container. This ensures it participates in normal document flow while being hidden via CSS in PPT/zoom modes.

*Alternatives considered:*
- Fixed position footer: Would overlap content in DOC mode and require extra bottom padding, breaking existing layout
- Inside last slide: Would require per-slide logic and break if the last slide's content is tall
- Outside `#scroll-container`: Would need separate mode-switching logic for visibility

**Decision 2: Use CSS class selectors for visibility**

Footer visibility is controlled purely via CSS:
```css
.doc-footer { /* visible by default (DOC mode) */ }
body.mode-ppt .doc-footer { display: none; }
body.mode-zoom .doc-footer { display: none; }
```

No JavaScript changes needed — the existing `document.body.className` manipulation in mode-switch functions already handles this. In DOC mode, body has no special class, so `.doc-footer` is visible. In PPT/zoom, the body class hides it.

*Alternatives considered:*
- JavaScript toggle: Adds complexity and state to track. CSS-only is simpler and already works with the existing pattern used by `.slide` elements in zoom mode.
- `display: none` on footer vs mode-specific: Using `display: none` on the body mode class is the cleanest approach matching existing patterns (`.slide` is hidden in zoom mode the same way).

**Decision 3: Image from GitHub org avatar**

The ovotop icon uses `https://avatars.githubusercontent.com/u/166823538?s=32` (GitHub organization avatar with fixed size). Fixed width/height (16px or 18px) ensures layout stability regardless of image load timing.

*Alternatives considered:*
- Base64 inline: Would bloat HTML for all generated documents
- Local asset: Would break self-contained requirement
- SVG inline: Clean but adds markup complexity

**Decision 4: Footer structure**

```html
<div class="doc-footer">
  <a href="https://github.com/ovotop/share-as-html" target="_blank" rel="noopener">
    <img src="https://avatars.githubusercontent.com/u/166823538?s=32" alt="ovotop" width="16" height="16">
    Powered by ovotop/share-as-html
  </a>
</div>
```

The entire footer is a single `<a>` tag for simplicity. The link opens in a new tab with `rel="noopener"` for security.

## Risks / Trade-offs

- **Image loading failure**: If the GitHub avatar URL is unreachable, a broken image icon with `alt="ovotop"` text appears. → Mitigation: The text "Powered by" is always visible regardless of image load. The image is small and non-critical.
- **Visual inconsistency across themes**: If the dark theme CSS variables change, the footer might lose contrast. → Mitigation: Footer uses the same `--text-dim` color variable as other secondary text elements, so it adapts automatically.
- **Extra DOM element in all modes**: The footer element exists in DOM even when hidden. → Mitigation: A single `<div>` has negligible performance impact. This matches the existing pattern where zoom containers are added/removed dynamically.
