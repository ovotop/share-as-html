## 1. Update skill source and CSS template

- [x] 1.1 Add `.doc-footer` CSS rules to SKILL.md (`.opencode/skills/sharing-in-html/SKILL.md`) — styles for footer layout, typography, and mode-specific visibility (`body.mode-ppt .doc-footer`, `body.mode-zoom .doc-footer`)
- [x] 1.2 Add footer HTML markup to the Complete HTML Skeleton section in SKILL.md — insert `<div class="doc-footer">` after last slide in `#scroll-container`

## 2. Update test HTML files

- [x] 2.1 Add footer HTML to `test-focus-matrix.html` — insert `<div class="doc-footer">` after last slide, inside `#scroll-container`
- [x] 2.2 Add footer HTML to `ai-agent-tools.html` — identical insertion
- [x] 2.3 Add footer HTML to `sharing-doc-test.html` — identical insertion
- [x] 2.4 Add footer HTML to `test-image-zoom.html` — identical insertion
- [x] 2.5 Add footer HTML to `test-mermaid-zoom.html` — identical insertion
- [x] 2.6 Add footer CSS to all 5 test HTML files — replicate the `.doc-footer` styles from SKILL.md CSS template

## 3. Update sharing-preview.html

- [x] 3.1 Add footer HTML and CSS to `sharing-preview.html` — this file has a slimmer feature set but should include the footer

## 4. Update md2html.py template

- [x] 4.1 Add `.doc-footer` CSS rules to the Jinja2 CSS template string in `md2html.py`
- [x] 4.2 Add footer HTML markup to the Jinja2 body template in `md2html.py` — render `<div class="doc-footer">` after the slide loop

## 5. Update test automation

- [x] 5.1 Add test case to `test-automated.spec.js` — verify footer is visible in DOC mode and hidden in PPT mode
- [x] 5.2 Add test case — verify footer link opens correct URL

## 6. Sync and verify

- [x] 6.1 Sync SKILL.md from `skills/share-as-html/SKILL.md` to `.opencode/skills/sharing-in-html/SKILL.md`
- [x] 6.2 Sync all test HTML files to the harness directory (`/home/mi/Documents/harness/tooling/documenting/sharing-in-html/`)
- [x] 6.3 Run `npx playwright test test-automated.spec.js` and verify all 65+ tests pass
- [x] 6.4 Run `python md2html.py` on a sample project and verify footer appears in generated output
- [x] 6.5 Commit changes to git
