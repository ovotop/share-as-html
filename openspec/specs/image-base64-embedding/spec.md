# Image Base64 Embedding

## Purpose

Define how the Markdown-to-HTML converter embeds local `assets/` images as base64 data URIs, enabling truly self-contained single-file HTML output that can be shared without requiring external image files.

## Requirements

### Requirement: Base64 image embedding

The converter SHALL embed local images as base64 data URIs when the image file size is at or below the configured threshold (default: 1MB). Images above the threshold SHALL be kept as relative `../assets/` paths.

#### Scenario: Small image embedded

- **WHEN** a slide references `![alt](assets/qr.png)` and the file is 50KB
- **THEN** the output HTML SHALL contain `<img alt="alt" src="data:image/png;base64,..." />`

#### Scenario: Large image kept as path

- **WHEN** a slide references `![alt](assets/screenshot.png)` and the file is 2MB (above 1MB default threshold)
- **THEN** the output HTML SHALL contain `<img alt="alt" src="../assets/screenshot.png" />`

#### Scenario: Mixed sizes in one document

- **WHEN** a project has one 50KB image and one 2MB image
- **THEN** the 50KB image SHALL be embedded as base64 data URI
- **AND** the 2MB image SHALL keep its `../assets/` relative path

### Requirement: Embed mode control via CLI flags

The converter SHALL support `--no-embed` to disable embedding and `--embed-threshold` to customize the size cutoff.

#### Scenario: --no-embed flag

- **WHEN** user runs `python md2html.py project_dir --no-embed`
- **THEN** ALL images SHALL keep `../assets/` relative paths regardless of size

#### Scenario: --embed-threshold flag

- **WHEN** user runs `python md2html.py project_dir --embed-threshold 0.5`
- **THEN** images ≤ 0.5MB SHALL be embedded and images > 0.5MB SHALL use relative paths

#### Scenario: Default behavior (no flags)

- **WHEN** user runs `python md2html.py project_dir` without embed-related flags
- **THEN** embedding SHALL use the 1MB default threshold

### Requirement: Path resolution

The converter SHALL resolve image paths relative to the `project_dir/assets/` directory. The Markdown source path `assets/xxx.png` SHALL be joined with `project_dir` to locate the actual file.

#### Scenario: Image file exists

- **WHEN** `project_dir/assets/qr.png` exists and is referenced as `assets/qr.png`
- **THEN** the file SHALL be read and either embedded or path-adjusted

#### Scenario: Image file missing

- **WHEN** `project_dir/assets/missing.png` does not exist
- **THEN** the converter SHALL log a warning and keep the `../assets/missing.png` path unchanged

### Requirement: MIME type detection

The converter SHALL detect the correct MIME type for base64 data URIs. Standard image formats SHALL be recognized.

#### Scenario: PNG image

- **WHEN** embedding a `.png` file
- **THEN** the data URI SHALL use `data:image/png;base64,...`

#### Scenario: JPEG image

- **WHEN** embedding a `.jpg` file
- **THEN** the data URI SHALL use `data:image/jpeg;base64,...`

#### Scenario: Unknown extension

- **WHEN** embedding a file with an unrecognized extension
- **THEN** the converter SHALL fall back to `image/png` MIME type

### Requirement: External URLs exempt from embedding

Images with HTTP/HTTPS `src` attributes SHALL NOT be embedded. This includes the footer's ovotop icon and any user-added external images.

#### Scenario: HTTP image URL untouched

- **WHEN** the HTML contains `<img src="https://example.com/logo.png">`
- **THEN** the URL SHALL remain unchanged (not embedded, not path-adjusted)
