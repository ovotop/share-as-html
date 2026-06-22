## 1. Setup

- [x] 1.1 Create `md2html.py` script file with dependency imports
- [x] 1.2 Create `requirements.txt` with `markdown`, `PyYAML`, `Jinja2`
- [x] 1.3 Embed existing CSS template (from `skills/share-as-html/SKILL.md`) as Jinja2 CSS block
- [x] 1.4 Embed existing JS template (from test HTML files) as Jinja2 JS block

## 2. Markdown Parsing

- [x] 2.1 Implement `extract_frontmatter()` to extract YAML frontmatter from Markdown files
- [x] 2.2 Implement `parse_meta()` to read and validate `meta.md`
- [x] 2.3 Implement `parse_outline()` to read `outline.md` table and infer outline if missing
- [x] 2.4 Implement `parse_slide()` to parse individual slide file: frontmatter + Markdown body
- [x] 2.5 Implement custom tag processor: `<card>`, `<callout>`, `<steps>`, `<step>` → HTML with CSS classes
- [x] 2.6 Implement `split_visual_reader()` to separate visual layer from `<!-- reader -->` blocks

## 3. HTML Generation

- [x] 3.1 Implement Jinja2 template rendering with meta, slides, CSS, JS blocks
- [x] 3.2 Implement layout wrapper mapping: `grid` (CSS Grid), `flex` (Flexbox), `stack` (vertical), `split` (two-panel)
- [x] 3.3 Implement `override.css` injection when file exists
- [x] 3.4 Implement image embedding from `assets/` (base64 for ≤1MB, path reference otherwise)
- [x] 3.5 Implement semantic class naming: `.slide-N`, `.card-M`, `.reader-narrative`
- [x] 3.6 Implement output directory creation and file writing

## 4. Dual-Mode Rendering

- [x] 4.1 Implement DOC mode: reader prose interleaved with visual blocks
- [x] 4.2 Implement PPT mode: visual blocks only, reader layer hidden via class
- [x] 4.3 Verify three-state state machine (DOC → PPT_FULL → PPT_ZOOM) works in generated HTML
- [x] 4.4 Verify mode transition preserves slide position

## 5. CLI Interface

- [x] 5.1 Implement command-line argument parsing (`project_dir`, optional `-o output`)
- [x] 5.2 Implement error handling for missing files, invalid frontmatter, empty slides
- [x] 5.3 Implement warnings for unrecognized layout values (fall back to default)

## 6. Example Project

- [x] 6.1 Create `example-talk/` directory with `meta.md`, `outline.md`, `speaker-script.md`
- [x] 6.2 Create example slides: `01-cover.md`, `02-motivation.md` (with dual grids + reader layer), `03-architecture.md` (with mermaid), `04-closing.md`
- [x] 6.3 Create `override.css` example with commented demo overrides
- [x] 6.4 Verify `python md2html.py example-talk/` produces valid `output/sharing.html`

## 7. Skill Update

- [x] 7.1 Update `skills/share-as-html/SKILL.md`: add Markdown workflow section
- [x] 7.2 Update AI instructions: when to generate Markdown vs direct HTML
- [x] 7.3 Document tag vocabulary and frontmatter schema in SKILL.md
- [x] 7.4 Sync updated skill to `.opencode/skills/share-as-html/SKILL.md`

## 8. Verification

- [x] 8.1 Verify deterministic output: run script twice, confirm byte-identical results
- [x] 8.2 Verify PPT mode: Enter to activate, arrow keys navigate, reader layer hidden
- [x] 8.3 Verify DOC mode: Esc to return, reader prose visible, free scroll works
- [x] 8.4 Verify ZOOM mode: mermaid diagrams and images zoomable in PPT mode
- [x] 8.5 Verify override.css: rules applied after theme CSS, take precedence
- [x] 8.6 Verify no content from speaker-script.md leaks into HTML
