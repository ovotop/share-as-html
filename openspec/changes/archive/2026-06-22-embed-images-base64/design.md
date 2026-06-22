## Context

The `md-to-html-pipeline` spec requires "Images from `assets/` SHALL be embedded as base64 data URIs (for images ≤ 1MB) or referenced by relative path." This was never implemented — `md2html.py` imports `base64` (line 12) but never uses it, and `fix_image_paths()` blindly converts all images to `../assets/` relative paths. The result is that output HTML cannot be shared as a single file.

## Goals / Non-Goals

**Goals:**
- Embed local `assets/` images ≤ 1MB as `data:image/...;base64,...` data URIs
- Keep images > 1MB as `../assets/` relative paths (with warning)
- `--no-embed` CLI flag to disable embedding entirely
- `--embed-threshold N` CLI flag to customize size cutoff (megabytes, default 1)
- Truly self-contained HTML output when all images fit the threshold

**Non-Goals:**
- Inlining mermaid CDN JavaScript (separate concern)
- Image compression or resizing
- Embedding images referenced by HTTP URLs
- Processing CSS `url()` references to local files

## Decisions

### Decision 1: Embed as post-processing step in `main()`

**Chosen**: Post-process the final rendered HTML string in `main()`, after `render_html()` and before `write`.

**Rationale**: `parse_slide()` doesn't have access to `project_dir`. Changing its signature to thread `project_dir` through would add noise for a single feature. Post-processing keeps the parsing and rendering layers focused.

**Alternative considered**: Embed inside `parse_slide()`. Rejected because it requires passing config through multiple layers for an orthogonal concern.

### Decision 2: Merge `fix_image_paths` into the embed step

**Chosen**: Remove `fix_image_paths()` from `parse_slide()`. In `main()`, the embed function handles both cases:
- Image ≤ threshold → replace with `data:image/...` (no path needed)
- Image > threshold or `--no-embed` → replace with `../assets/` relative path

**Rationale**: Currently `fix_image_paths` runs per-slide and changes `assets/` → `../assets/`. The embed step would then need to reverse-engineer this. Doing both in one pass avoids the double-transform.

### Decision 3: 1MB default threshold

**Chosen**: Default threshold of 1MB, matching the existing spec requirement.

**Rationale**: A 19-slide deck with two ~200KB images produces a ~356KB output — well under any sharing platform limits. 1MB individual image limit ensures even 10+ embedded images stay reasonable.

### Decision 4: CLI flag naming

**Chosen**: `--no-embed` (disable) and `--embed-threshold N` (MB, float).

**Rationale**: `--no-embed` follows POSIX convention for disabling features. Threshold in MB is more user-friendly than bytes.

## Risks / Trade-offs

| Risk | Mitigation |
|------|-----------|
| Large number of small images pushes total size up | Threshold is per-image; total size is user's responsibility |
| Image file not found during embedding | Log warning, keep original `assets/` path (will be fixed to `../assets/`) |
| MIME type detection for non-.png images | Use `mimetypes.guess_type()` from stdlib; fallback to `image/png` |
