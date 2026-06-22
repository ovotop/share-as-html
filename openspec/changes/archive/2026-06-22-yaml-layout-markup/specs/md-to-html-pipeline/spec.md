# Markdown-to-HTML Pipeline (Delta)

## MODIFIED Requirements

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

### Requirement: Deterministic output

Given the same input Markdown files, the script SHALL produce identical HTML output on every run. The output SHALL NOT depend on AI, random values, timestamps, or external network resources.

#### Scenario: Identical outputs on repeated runs

- **WHEN** the script is run twice on the same project directory without changes
- **THEN** the two output HTML files SHALL be byte-identical

## REMOVED Requirements

### Requirement: Semantic class naming

**Reason**: With YAML grid-based layout, stable `.slide-N` and `.card-M` class names are no longer generated. Layout is controlled by frontmatter YAML rather than position-based auto-class generation.

**Migration**: Users targeting elements with `.card-M` in `override.css` should use generic selectors (`.card:nth-child(N)`) or add custom classes via raw HTML in content slots if precise targeting is needed.
