## Why

当前 slide 的布局描述混在 Markdown body 里：卡片用 `<card>` 或 `<div class="card">`，高亮块用 `<callout>`，步骤用 `<steps>`。这些自定义 HTML 标签与 Python-Markdown 的解析器交互产生三个系统性 bug（已验证）：`<card>` 被 `<p>` 拆散、grid 内 markdown 不解析、`<p><div>` 非法嵌套。工作区被迫用 raw HTML 规避，失去了 Markdown 的可读性。解决之道不是修补 Python-Markdown 的渲染后处理，而是让布局信息**离开 body**——不进 Markdown parser 的视线。

## What Changes

- **BREAKING**: 移除 `<card>`、`<callout>`、`<steps>` 自定义标签，移除 `<div class="card">` 手写 HTML 布局写法
- **BREAKING**: frontmatter `layout:` 字段语义从简单枚举变为 YAML grid 描述
- 新增 YAML 布局语法：卡片、高亮块、步骤、指标面板、双栏对比——全部通过 frontmatter `layout.grid` 的二维数组描述
- 新增 `---` 内容分隔符：body 内各 `---` 块按行优先顺序对应 YAML grid cell，每个 cell 的内容是独立的纯 Markdown
- 迁移 example-talk 4 页 slide 和 android-cli-docing 20 页 slide 到新语法
- 更新 SKILL.md 文档、删除旧语法说明

## Capabilities

### New Capabilities

- `yaml-layout-markup`: YAML frontmatter 描述布局结构（grid 行、cell 类型、标题），替代所有 HTML 布局标签。Cell 类型包括 `card`、`callout`、`steps`、`metrics`、`split`。
- `content-slot-split`: body 用 `---` 分隔符切片，按 grid 行优先顺序对应 YAML cell。每个 slot 是独立的纯 Markdown 文本，经过完整的 markdown 转换后嵌入 HTML 容器。

### Modified Capabilities

- `markdown-slide-authoring`: 移除 `<card>`、`<callout>`、`<steps>`、`<div markdown="1">` 语法；新增 YAML layout.grid 语法和 `---` cell 分隔符。slide body 变成纯 Markdown，不含 HTML 标签。
- `md-to-html-pipeline`: 移除 `process_custom_tags()` 函数；新增 YAML grid 展开逻辑（将 grid 行/列映射为 cell HTML 容器，将对应 body slot 的 markdown 转换结果填充到容器中）。解析流程从「markdown 转换 → 后处理 tag → 后处理 grid」变为「YAML grid 展开 → 逐 cell markdown 转换 → 组装」。

## Impact

- **md2html.py**: `parse_slide()` 重构（约 50 行改动），删除 `process_custom_tags()`（约 60 行删除），`wrap_visual()` 简化（约 40 行改动）
- **SKILL.md**: 更新 Path A slide 编写章节、删除自定义标签文档、新增 YAML layout 语法
- **slides/**: example-talk 4 页 + android-cli-docing 20 页：手写 HTML 替换为纯 Markdown + YAML layout
- **test**: Playwright 测试 harness 需重新生成 HTML 输出（markdown 源文件变更导致输出 HTML 不同）
- **已生成的 sharing.html**: android-cli-docing 的输出文件需重新生成
- **不涉及**: CSS/JS template、HTML skeleton、键盘导航、zoom/focus 逻辑、override.css 机制
