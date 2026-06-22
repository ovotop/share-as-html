## Why

Users generating HTML documents with the sharing-in-html skill need a way to attribute the tooling that powers the document. Adding a subtle "Powered by" footer in DOC mode gives visibility to the ovotop/share-as-html project while being unobtrusive — it only appears in reading mode, not during PPT presentations.

## What Changes

- Add a footer element at the bottom of DOC mode pages showing: "Powered by" + ovotop icon + link to `https://github.com/ovotop/share-as-html`
- Footer is hidden in PPT_FULL and PPT_ZOOM modes, visible only in DOC mode
- Footer styles are self-contained (small text, centered, subtle colors matching the dark theme)
- The footer is added to the HTML skeleton template in SKILL.md and replicated across all test HTML files

## Capabilities

### New Capabilities

- `doc-mode-footer`: A footer element that displays attribution text ("Powered by") with an icon and hyperlink to the ovotop/share-as-html GitHub repository. Visible only in DOC mode; hidden in PPT_FULL and PPT_ZOOM modes.

### Modified Capabilities

- `md-to-html-pipeline`: The HTML skeleton template in SKILL.md must include the footer HTML markup and CSS. The `md2html.py` Jinja2 template must render the footer in generated output.

## Impact

- **SKILL.md** (`.opencode/skills/sharing-in-html/SKILL.md`): Add footer CSS and HTML to the template sections
- **All 5 test HTML files**: Add identical footer markup — `test-focus-matrix.html`, `ai-agent-tools.html`, `sharing-doc-test.html`, `test-image-zoom.html`, `test-mermaid-zoom.html`
- **sharing-preview.html**: Add footer (this file has a slimmer feature set but can include the footer)
- **md2html.py**: Update the Jinja2 template to render the footer in generated output
- **test-automated.spec.js**: Optionally add a test verifying the footer is present in DOC mode and hidden in PPT mode
