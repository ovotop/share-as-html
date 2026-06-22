## Why

The `md-to-html-pipeline` spec already requires base64 embedding for images ≤ 1MB, but `md2html.py` currently writes all images as relative paths (`../assets/xxx`). This means the output HTML cannot be shared as a single file — recipients see broken images unless they also receive the assets folder. The `import base64` statement exists in the script but is unused (Ruff F401).

## What Changes

- Implement base64 image embedding in `md2html.py` for images ≤ 1MB (configurable threshold)
- Images > 1MB keep relative path behavior with `../assets/` prefix
- Add `--no-embed` flag to opt out of embedding
- Add `--embed-threshold` flag to customize the size cutoff (default: 1MB)
- Remove unused `base64` import warning (F401) by putting it to use

## Capabilities

### New Capabilities

- `image-base64-embedding`: Convert local `assets/` images to base64 data URIs during HTML generation for images ≤ threshold, enabling truly self-contained single-file output.

### Modified Capabilities

None. The `md-to-html-pipeline` spec already defines the requirement — this change only fills an implementation gap.

## Impact

- `skills/share-as-html/scripts/md2html.py` — embed logic, new CLI flags, path resolution
- `openspec/specs/md-to-html-pipeline/spec.md` — no change needed (already spec'd)
- Output HTML files will grow by ~1.33x the size of embedded images
- Breaking: none; relative path fallback preserved for large images and `--no-embed` mode
