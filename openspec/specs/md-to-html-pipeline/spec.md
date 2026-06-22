# Markdown-to-HTML Pipeline

## Purpose

Define a deterministic Python script (`md2html.py`) that converts Markdown presentation projects into self-contained HTML files. The script operates without AI, producing identical output given identical input. It reuses the existing share-as-html CSS theme and JavaScript state machine.

## Requirements

### Requirement: Script entry point

The converter SHALL be a single Python script `md2html.py` that accepts a project directory path and an optional output path.

```bash
python md2html.py <project_dir> [-o <output.html>]
```

If `-o` is not specified, the script SHALL output to `<project_dir>/output/sharing.html`.

#### Scenario: Basic conversion

- **WHEN** user runs `python md2html.py my-talk/`
- **THEN** the script SHALL create `my-talk/output/sharing.html` and exit with code 0

#### Scenario: Custom output path

- **WHEN** user runs `python md2html.py my-talk/ -o /tmp/demo.html`
- **THEN** the script SHALL create `/tmp/demo.html` and exit with code 0

#### Scenario: Invalid project directory

- **WHEN** user runs `python md2html.py /nonexistent/`
- **THEN** the script SHALL exit with a non-zero code and print an error message

#### Scenario: Old layout syntax rejected

- **WHEN** a slide's frontmatter contains `layout: grid` (string value)
- **THEN** the script SHALL exit with a non-zero code and print an error indicating the required YAML syntax

### Requirement: Dependency specification

The script SHALL declare dependencies in a `requirements.txt` file:

- `markdown` — Markdown to HTML conversion
- `PyYAML` — YAML frontmatter parsing
- `Jinja2` — HTML template rendering

No other pip dependencies SHALL be required.

#### Scenario: Install dependencies

- **WHEN** user runs `pip install -r requirements.txt`
- **THEN** all three packages SHALL be installed and the script SHALL run without import errors

### Requirement: Deterministic output

Given the same input Markdown files, the script SHALL produce identical HTML output on every run. The output SHALL NOT depend on AI, random values, timestamps, or external network resources.

#### Scenario: Identical outputs on repeated runs

- **WHEN** the script is run twice on the same project directory without changes
- **THEN** the two output HTML files SHALL be byte-identical

### Requirement: Self-contained HTML output

The output HTML file SHALL be self-contained:
- All CSS SHALL be embedded in a `<style>` tag (no external stylesheets)
- All JavaScript SHALL be embedded in a `<script>` tag
- Mermaid SHALL be loaded from CDN (`https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js`)
- Images from `assets/` SHALL be embedded as base64 data URIs (for images ≤ 1MB) or referenced by relative path
- The footer's ovotop icon SHALL be loaded from external URL (`https://avatars.githubusercontent.com/u/61374409?s=96&v=4`) and is exempt from the base64 embedding rule

#### Scenario: Single file sharing

- **WHEN** user opens the output HTML file by double-clicking
- **THEN** it SHALL render correctly without a web server or additional files

### Requirement: Existing CSS and JS reuse

The script SHALL use the existing CSS and JS from the `share-as-html` skill as-is. The CSS template (deep theme, card styles, callout styles, grid layouts) and JS template (three-state state machine, keyboard navigation, zoom mode) SHALL be embedded in the Jinja2 template without modification. The footer CSS styles (`.doc-footer` and mode-specific hiding rules) SHALL also be included in the CSS template.

#### Scenario: PPT mode works

- **WHEN** user opens the output HTML and presses Enter
- **THEN** the page SHALL switch to PPT mode with snap-to-slide behavior

#### Scenario: DOC mode works

- **WHEN** user is in PPT mode and presses Esc
- **THEN** the page SHALL return to DOC mode with free scrolling

#### Scenario: Fluid typography in generated HTML

- **WHEN** md2html.py generates output HTML
- **THEN** the CSS SHALL contain `clamp()` font-size values and `.slide { align-items: center; }`

#### Scenario: PPT mode wider content in generated HTML

- **WHEN** md2html.py generates output HTML
- **THEN** the CSS SHALL contain `body.mode-ppt .slide .content { max-width: 1100px; }`

#### Scenario: Footer hidden in PPT mode in generated HTML

- **WHEN** md2html.py generates output HTML
- **THEN** the CSS SHALL contain `body.mode-ppt .doc-footer { display: none; }` and `body.mode-zoom .doc-footer { display: none; }`

### Requirement: Template architecture

The script SHALL use a Jinja2 template with the following structure:

- Fixed `<style>` block (CSS copied from current SKILL.md)
- Fixed `<script>` block (JS copied from current test HTML files)
- Dynamic `<body>` block rendered from parsed Markdown slides
- The body block SHALL include a `.doc-footer` element after the last slide, containing the attribution link to the ovotop/share-as-html GitHub repository

The template SHALL be embedded in the script as a string constant, not loaded from an external file.

#### Scenario: Template renders all slides

- **WHEN** the script processes a project with 5 slides
- **THEN** the output HTML SHALL contain 5 `<div class="slide">` elements in order

#### Scenario: Template renders footer after slides

- **WHEN** the script processes a project with any number of slides
- **THEN** the output HTML SHALL contain a `<div class="doc-footer">` element after the last slide, inside `#scroll-container`

### Requirement: override.css support

If `<project_dir>/override.css` exists, the script SHALL embed its content in a second `<style>` tag placed after the main theme CSS, so that override rules take precedence.

#### Scenario: override.css present

- **WHEN** the project directory contains `override.css`
- **THEN** its content SHALL appear after the theme CSS in the output HTML

#### Scenario: override.css absent

- **WHEN** the project directory does not contain `override.css`
- **THEN** the script SHALL proceed normally without error


