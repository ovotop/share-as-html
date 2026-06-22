## ADDED Requirements

### Requirement: Speaker script file location

The speaker script SHALL be stored in `<project>/speaker-script.md`. This file SHALL NOT be processed by the md2html.py converter and SHALL NOT appear in the output HTML.

#### Scenario: speaker-script.md present

- **WHEN** a project contains `speaker-script.md`
- **THEN** the md2html.py converter SHALL ignore it and proceed with conversion

#### Scenario: speaker-script.md absent

- **WHEN** a project does not contain `speaker-script.md`
- **THEN** the md2html.py converter SHALL proceed normally without error

### Requirement: Speaker script format

`speaker-script.md` SHALL be a free-form Markdown file. The recommended structure is:

- `# Speaker Script: <title>` as the top-level heading
- `---` (horizontal rules) to separate sections
- `## [Slide N] <slide title> {<duration>}` to mark each slide section
- Body text containing spoken words, stage directions, and timing cues
- Stage directions in parentheses, e.g., `（停顿 3 秒）`, `（点击翻页）`

#### Scenario: Well-structured speaker script

- **WHEN** speaker-script.md uses the recommended structure with slide markers
- **THEN** the presenter can navigate by slide number and follow timing cues

### Requirement: Speaker script is for presenter only

The speaker script SHALL NOT be rendered in the output HTML under any mode (PPT, DOC, or Zoom). It SHALL NOT be referenced from the HTML. It is a standalone file intended for the presenter's personal use.

#### Scenario: No accidental exposure

- **WHEN** the output HTML is opened and inspected
- **THEN** no content from speaker-script.md SHALL appear in the HTML source or rendered page

### Requirement: Slide references in speaker script

Speaker script section headings SHALL reference slides by number (`## [Slide N]`) to maintain a clear correspondence between the script and the presentation slides. This reference is for human convenience only and SHALL NOT be mechanically validated.

#### Scenario: Slide number matches file naming

- **WHEN** `speaker-script.md` has `## [Slide 2]` and `slides/02-motivation.md` is slide 2
- **THEN** the presenter can cross-reference the script with the slide file
