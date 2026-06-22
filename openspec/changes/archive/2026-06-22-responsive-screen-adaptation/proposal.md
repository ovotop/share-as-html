## Why

当前 CSS 在大屏幕上内容左对齐（未居中）、固定字号在大屏偏小；在小屏上仅 h2 和 cover h1 缩放了字号，其他元素维持桌面尺寸。需要引入流体缩放和居中布局，使一个 HTML 文件在 4K 投屏和手机阅读之间自适应。

## What Changes

- `.slide` 添加 `align-items: center`：大屏幕水平居中内容
- 用 `clamp()` 替代固定字号：h2, h3, p/li, .cover h1, .card h4 全部流体缩放
- PPT 模式下 `.content` max-width 从 900px 放宽到 1100px
- `@media (max-width: 768px)` 仅保留结构性调整（padding、grid 坍塌），移除字体覆盖
- 更新 `md2html.py` 和 `skills/share-as-html/SKILL.md` 中的 CSS 模板

## Capabilities

### Modified Capabilities

- `markdown-slide-authoring`: CSS 模板中 `.slide` 的对齐方式和字体定义变更
- `md-to-html-pipeline`: CSS_TEMPLATE 常量更新为流体缩放版本
- `dual-mode-output`: PPT 模式下 content 宽度放宽

## Impact

- `md2html.py`: 更新 CSS_TEMPLATE 常量（~30 行改动）
- `skills/share-as-html/SKILL.md`: 同步 CSS 模板
- 已有 HTML 测试文件不受影响（使用独立内联 CSS）
