# AGENTS.md — sharing-in-html

## What this repo is

Development & testing workspace for the `sharing-in-html` OpenCode skill. This repo holds test HTML pages, Playwright tests, OpenSpec change management, shared output documents, and the canonical skill source.

## Skill deployment

The **canonical source** for the skill is `skills/sharing-in-html/SKILL.md` — this is the git-tracked version. The **deployed** skill lives at `.opencode/skills/sharing-in-html/SKILL.md` (project-level, gitignored by `.gitignore`). When iterating on the skill:

1. Edit `skills/sharing-in-html/SKILL.md` in this repo
2. Sync to `.opencode/skills/sharing-in-html/SKILL.md` for OpenCode to pick up changes
3. Commit the change to track it in git

The `.opencode/skills/` directory also contains OpenSpec project skills (`openspec-*`). The `skills/` directory at repo root is for the published sharing-in-html skill.

## File architecture

All 6 HTML files share **identical JS and CSS** (embedded inline):
- `test-focus-matrix.html` — 6 focus scenarios + debug panel
- `ai-agent-tools.html` — mermaid + 3-diagram focus test
- `sharing-doc-test.html` — full feature test
- `test-image-zoom.html` — image zoom
- `test-mermaid-zoom.html` — mermaid zoom
- `sharing-preview.html` — **output doc** (Android CLI presentation), lighter JS (no focus/zoom)

**CRITICAL**: Any JS/CSS change to one test HTML file **must be replicated across all 5 test files** (skip `sharing-preview.html` which has a slimmer feature set). When debugging, always check sibling files — the bug in one file likely exists in all.

## Three-state state machine

```
DOC ─Enter→ PPT_FULL ─Enter (focused diagram)→ PPT_ZOOM
 ↑                ↑                              │
 └Esc─────────────└──────────Esc────────────────┘
```

- **DOC**: free scroll, `min-height: auto`
- **PPT_FULL**: `scroll-snap-type: y proximity`, slides snap, Arrow keys navigate
- **PPT_ZOOM**: image/mermaid fullscreen, `overflow: auto` scrolls content

## Critical code patterns (all 5 files must match)

```js
// handleFocusSwitch: compute index FIRST, then clear old focus
function handleFocusSwitch(key) {
    let newIndex;
    if (key === 'ArrowRight') newIndex = Math.min(focusedDiagramIndex + 1, focusables.length - 1);
    else newIndex = Math.max(focusedDiagramIndex - 1, 0);
    focusedDiagramIndex = newIndex;
    document.querySelectorAll('.diagram-focusable.focused').forEach(el => el.classList.remove('focused'));
    focusables[focusedDiagramIndex].classList.add('focused');
}

// exitZoomMode: use scrollTo(instant), NOT scrollIntoView
function exitZoomMode() {
    currentState = 'PPT_FULL';
    document.body.className = 'mode-ppt';
    // ... remove zoom container ...
    const slides = document.querySelectorAll('.slide');
    if (slides[currentSlideIndex]) {
        const targetTop = slides[currentSlideIndex].offsetTop;
        window.scrollTo({ top: targetTop, behavior: 'instant' });
    }
    updateFocus(true);  // preserveIndex = true
}

// updateFocus: preserveIndex param prevents reset on exit-zoom
function updateFocus(preserveIndex = false) {
    if (!preserveIndex || focusedDiagramIndex < 0 || focusedDiagramIndex >= focusables.length) {
        focusedDiagramIndex = 0;
    }
}
```

## PPT overflow-scroll behavior (Arrow key in PPT_FULL)

ArrowDown/Up on a slide taller than viewport: scroll content first, bounce at boundary, 2nd press advances to next slide.
ArrowRight/Left on a slide wider than viewport: scroll horizontally first, bounce at boundary, 2nd press switches focus.

Uses `isAtScrollBoundary` flag, `@keyframes slide-bounce-*` animations.

## Testing

```bash
# Run all tests (5 files × 13 tests each = 65 tests)
npx playwright test test-automated.spec.js

# Run a specific file's tests
npx playwright test test-automated.spec.js -g "test-focus-matrix"

# Run a specific test
npx playwright test test-automated.spec.js -g "State Transitions"
```

Tests use Playwright (`@playwright/test` ^1.61). Spec file is at repo root. **Tests load HTML from `file:///home/mi/Documents/harness/tooling/documenting/sharing-in-html/`** — a different directory than this workspace. Before running tests, ensure the HTML files are synced to that harness directory.

Each test file name becomes a `test.describe` block, so 5 describe blocks × 13 tests each.

## OpenSpec

Schema: `spec-driven`. Two archived changes:
- `openspec/changes/archive/2026-06-18-sharing-html-skill/` — initial skill creation
- `openspec/changes/archive/2026-06-18-ppt-overflow-scroll/` — overflow scroll fix

Project-level openspec skills live at `.opencode/skills/openspec-*`. Commands at `.opencode/command/opsx-*.md`.

## Key gotcha: two repo locations

This repo is at `/home/mi/Documents/skills/sharing-in-html/`. The Playwright test harness loads files from `/home/mi/Documents/harness/tooling/documenting/sharing-in-html/`. These are **different directories**. Changes made here must be manually synced to the harness directory before running tests.

## Scope discovery rule (from RETROSPECTIVE.md)

When a bug is reported about ONE HTML file, always:
1. Read `docs/context.md` and `docs/fix-and-testing-context.md` for project overview
2. Check ALL 5 sibling test HTML files — bugs are systemic, not isolated
3. Enumerate all affected dimensions (vertical + horizontal scroll, etc.)
4. Confirm Non-Goals with user before excluding anything

The project has 5 files sharing identical code. Fixing one without checking others is a recurring failure pattern.

## Before proposing changes

Read `RETROSPECTIVE.md` — documents a multi-hour investigation into why the agent kept making scope errors by treating a system-wide template bug as a single-file issue.
