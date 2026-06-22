## 1. CSS Template Update (md2html.py)

- [x] 1.1 Add `align-items: center` to `.slide` selector
- [x] 1.2 Replace `h2 { font-size: 36px; }` with `h2 { font-size: clamp(24px, 4vw, 36px); }`
- [x] 1.3 Replace `h3 { font-size: 22px; }` with `h3 { font-size: clamp(17px, 2.5vw, 22px); }`
- [x] 1.4 Replace `p { ... }` to add `font-size: clamp(14px, 1.5vw, 16px);` and same for `ul li`
- [x] 1.5 Replace `.cover h1 { font-size: 48px; }` with `font-size: clamp(32px, 5vw, 48px);`
- [x] 1.6 Replace `.card h4 { font-size: 16px; }` with `font-size: clamp(14px, 1.5vw, 16px);`
- [x] 1.7 Add `body.mode-ppt .slide .content { max-width: 1100px; }`
- [x] 1.8 Simplify `@media (max-width: 768px)`: remove font-size overrides, keep padding/grid collapse

## 2. SKILL.md Sync

- [x] 2.1 Update CSS template in `skills/share-as-html/SKILL.md` to match md2html.py changes
- [x] 2.2 Sync updated skill to `.opencode/skills/share-as-html/SKILL.md`

## 3. Verification

- [x] 3.1 Run `python md2html.py example-talk/` and confirm output contains `clamp()` and `align-items: center`
- [x] 3.2 Confirm deterministic output (run twice, byte-identical)
- [x] 3.3 Confirm PPT mode has `max-width: 1100px` in output CSS
- [x] 3.4 Confirm `@media (max-width: 768px)` has no font-size declarations
