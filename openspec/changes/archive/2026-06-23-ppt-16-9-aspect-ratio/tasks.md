## 1. Template CSS changes (md2html.py)

- [x] 1.1 Update `body.mode-ppt .slide` padding from `60px 80px` to `60px 120px` in CSS_TEMPLATE
- [x] 1.2 Replace `body.mode-ppt .slide .content { max-width: 1100px; }` with `body.mode-ppt .slide .content { aspect-ratio: 16 / 9; width: 100%; }`
- [x] 1.3 Add `body.mode-ppt .slide .content { aspect-ratio: auto; }` to the `@media (max-width: 768px)` block
- [x] 1.4 Change `.slide-number` position from `top: 24px` to `bottom: 24px`

## 2. Sync test fixture HTML files

- [x] 2.1 Update test-focus-matrix.html PPT CSS (slide padding, content aspect-ratio, mobile, slide-number)
- [x] 2.2 Update ai-agent-tools.html PPT CSS (same changes)
- [x] 2.3 Update sharing-doc-test.html PPT CSS (same changes)
- [x] 2.4 Update test-image-zoom.html PPT CSS (same changes)
- [x] 2.5 Update test-mermaid-zoom.html PPT CSS (same changes)

## 3. Regenerate example output

- [x] 3.1 Run `python md2html.py example-talk/` to regenerate example-talk/output/sharing.html
- [x] 3.2 Verify generated HTML contains new CSS rules (aspect-ratio, 120px padding, bottom slide-number)

## 4. Verification

- [x] 4.1 Run `lsp_diagnostics` on md2html.py — no new errors
- [x] 4.2 Run Playwright tests: `npx playwright test test-automated.spec.js` — all 65 tests pass
- [x] 4.3 Visual spot-check: open sharing-doc-test.html in browser, press Enter for PPT mode, confirm 16:9 content area with side margins and slide number at bottom-right
