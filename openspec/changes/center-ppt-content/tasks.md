## 1. Python data model changes

- [ ] 1.1 Add `heading_html` to `Slide.__slots__`
- [ ] 1.2 Add `heading_html` parameter to `Slide.__init__()` (default `""`)
- [ ] 1.3 Include `heading_html` in `Slide.to_dict()` output

## 2. Heading extraction and assembly

- [ ] 2.1 Modify `assemble_grid()` to return only body content (remove `heading_html` prepend)
- [ ] 2.2 Pass `heading_html` separately when constructing `Slide` in `parse_slide()`

## 3. HTML template changes

- [ ] 3.1 Update Jinja2 template: render `heading_html` as direct child of `.slide`, before `.content` (non-cover slides only)
- [ ] 3.2 Ensure cover slides (`.slide.cover`) do not render `heading_html` outside `.content`

## 4. CSS changes

- [ ] 4.1 Update `body.mode-ppt .slide`: remove vertical centering, let heading flow naturally from top
- [ ] 4.2 Update `body.mode-ppt .slide .content`: add `align-self: center` and `margin: auto 0` for centering
- [ ] 4.3 Add `body.mode-ppt .slide.cover { justify-content: center }` for cover slides
- [ ] 4.4 Remove `aspect-ratio: 16/9` from `body.mode-ppt .slide .content` (heading is outside now)

## 5. Regenerate and verify

- [ ] 5.1 Re-run `python md2html.py example-talk/` to regenerate `example-talk/output/sharing.html`
- [ ] 5.2 Run `lsp_diagnostics` on `md2html.py`
- [ ] 5.3 Run `npx playwright test` to verify no regressions
- [ ] 5.4 Manual visual verification: PPT mode heading is top-left, content centered
