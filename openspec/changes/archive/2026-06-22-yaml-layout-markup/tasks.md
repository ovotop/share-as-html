## 1. Core Pipeline Implementation

- [x] 1.1 Implement `split_heading_and_slots(body, N_cells)` — split body into heading (before first `=== slot ===`) and slot list (rsplit by `=== slot ===`, maxsplit=N_cells-1, right-to-left)
- [x] 1.2 Implement `assemble_grid(grid, slots, heading_html, md_converter)` — expand YAML grid cells, convert each slot through markdown, wrap in container HTML, group by row into grid-N wrappers
- [x] 1.3 Implement cell renderers: `render_card(title, content)`, `render_callout(variant, content)`, `render_steps(content)`, `render_metrics(content)`, `render_split(left, right)`, `render_raw(content)`
- [x] 1.4 Rewrite `parse_slide()` flow: parse YAML grid → split slots → convert heading → assemble grid → split visual/reader
- [x] 1.5 Add old-layout detection: if `layout` is a string, exit with clear error message showing required YAML syntax
- [x] 1.6 Remove `process_custom_tags()` function
- [x] 1.7 Remove `wrap_visual()` old layout logic (grid auto-detection, split_top_level_blocks, card wrapping) — keep only the new assemble_grid path
- [x] 1.8 Remove unused functions: `wrap_card_group()`, `_BlockSplitter`, `split_top_level_blocks()`
- [x] 1.9 Validate pipeline: run `python md2html.py` on test fixtures, verify no Python exceptions, verify output contains expected CSS classes

## 2. Example-Talk Migration (4 slides)

- [x] 2.1 Migrate `01-cover.md`: convert to new layout syntax (cover slide has no grid, body is raw markdown)
- [x] 2.2 Migrate `02-motivation.md`: convert `<card>` tags to YAML grid with card cells
- [x] 2.3 Migrate `03-architecture.md`: convert `<card>` tags and grid layout to YAML
- [x] 2.4 Migrate `04-closing.md`: convert to new layout syntax
- [x] 2.5 Run converter on example-talk, verify output HTML visually matches previous output

## 3. Android-CLI-Docing Migration (20 slides)

- [x] 3.1 Write migration script that reads old slide files and produces YAML grid syntax
- [x] 3.2 Migrate slides 01-05 (cover, problem, overview, layout, ui-comparison)
- [x] 3.3 Migrate slides 06-10 (layout-diff, ci-efficiency, script-compare, skills-top5, skill-pipeline)
- [x] 3.4 Migrate slides 11-15 (knowledge-base, lucene-vs-rag, search-efficiency, index-design, ai-native)
- [x] 3.5 Migrate slides 16-20 (login-automation, agent-adaptive, wang-day, summary, qa)
- [x] 3.6 Run converter on android-cli-docing, verify no errors or warnings
- [x] 3.7 Open output in browser, verify all 20 slides render correctly in DOC and PPT modes

## 4. Documentation Update

- [x] 4.1 Update SKILL.md Path A — replace custom tag documentation with YAML layout syntax
- [x] 4.2 Update SKILL.md — add cell type reference table (card, callout, steps, metrics, split, raw)
- [x] 4.3 Update SKILL.md — add `---` slot delimiter documentation
- [x] 4.4 Update SKILL.md — remove all `<card>`, `<callout>`, `<steps>`, `<div class="card">` examples
- [x] 4.5 Update SKILL.md — update `<div markdown="1">` section (no longer needed, replaced by `---` slots)
- [x] 4.6 Sync deployed skill: `cp -r skills/share-as-html/* .opencode/skills/sharing-in-html/`

## 5. Testing & Verification

- [x] 5.1 Run `python md2html.py example-talk/` and confirm zero errors
- [x] 5.2 Run `python md2html.py <android-cli-docing>/sharing` and confirm zero errors
- [x] 5.3 Verify both outputs: DOC mode enter/exit, PPT mode snap scroll, keyboard navigation, zoom in/out
- [x] 5.4 Verify no `<p><div` nesting in generated HTML output (grep check)
- [x] 5.5 Verify markdown parsing inside cards: `**bold**` → `<strong>`, `` `code` `` → `<code>`
- [x] 5.6 Verify `<pre><code>` blocks stay inside card divs (not pushed out)
- [x] 5.7 Verify Playwright tests pass on regenerated harness HTML files
- [x] 5.8 Run `openspec archive yaml-layout-markup` to finalize
