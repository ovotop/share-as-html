## 1. CSS changes

- [ ] 1.1 Add `.zoom-content` default rule: `max-width`/`max-height` via `--zoom-scale` for fit mode
- [ ] 1.2 Add `.zoom-content.fill` rule: `width`/`height` + `object-fit: cover` for fill mode

## 2. JavaScript changes

- [ ] 2.1 Add `zoomScale` (float) and `zoomFitMode` ('fit' | 'fill') state variables
- [ ] 2.2 Define `SCALE_STEPS = [1.0, 1.25, 1.5, 2.0, 3.0]`
- [ ] 2.3 Initialize to fit mode, 1.0× in `enterZoomMode()`
- [ ] 2.4 `Enter` handler: toggle `.fill` class on `.zoom-content`
- [ ] 2.5 `+` handler: step to next higher scale in SCALE_STEPS, update `--zoom-scale`
- [ ] 2.6 `-` handler: step to next lower scale in SCALE_STEPS, update `--zoom-scale`
- [ ] 2.7 `applyZoomScale()` helper: set `--zoom-scale` on `.zoom-content`

## 3. Regenerate and verify

- [ ] 3.1 Re-run `python md2html.py example-talk/` to regenerate output
- [ ] 3.2 Run `lsp_diagnostics` on `md2html.py`
