## 1. Refactor existing path fix

- [x] 1.1 Remove `fix_image_paths()` call from `parse_slide()` — path adjustment will be handled by the embed step
- [x] 1.2 Remove `fix_image_paths()` function definition (its logic is absorbed into embed function)

## 2. Core embed implementation

- [x] 2.1 Create `embed_images(html: str, project_dir: str, threshold_bytes: int) -> str` function that finds all `<img src="assets/...">` in rendered HTML, reads files, embeds below threshold, and applies `../assets/` prefix above threshold
- [x] 2.2 Implement MIME type detection using `mimetypes.guess_type()` with `image/png` fallback
- [x] 2.3 Skip HTTP/HTTPS URLs (don't embed, don't path-adjust)
- [x] 2.4 Handle missing image files: log warning and keep `../assets/` path as fallback

## 3. CLI flags

- [x] 3.1 Add `--no-embed` flag to `argparse` (store `True`, default `False`)
- [x] 3.2 Add `--embed-threshold` flag to `argparse` (type `float`, default `1.0`, value in MB)
- [x] 3.3 Integrate flags into `main()`: skip embed when `args.no_embed`, convert threshold MB to bytes

## 4. Integration and verification

- [x] 4.1 Rebuild sharing project HTML with default embed (verify images ≤ 1MB become base64)
- [x] 4.2 Verify `--no-embed` produces only `../assets/` paths
- [x] 4.3 Verify `--embed-threshold 0.1` forces all images to relative paths (threshold tiny)
- [x] 4.4 Verify HTTP URLs remain untouched
- [x] 4.5 Sync skill to `.opencode/skills/sharing-in-html/` and android-cli-docing `.opencode/skills/share-as-html/`
