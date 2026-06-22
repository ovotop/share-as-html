## Why

当前 `share-as-html` skill 要求 AI 直接生成 HTML——内容、CSS、JS 全部交织在一个文件中。这导致两个根本问题：(1) 人类无法轻松编辑产出物（改一个标题需要在 HTML 源码中定位对应标签），(2) AI 不可用时完全无法维护或产出。需要引入 Markdown 作为中间格式，将"创作内容"和"渲染 HTML"解耦。

## What Changes

- 新增 `markdown-slide-authoring` 能力：用 Markdown 文件组织分享内容，每页 PPT 一个 `.md` 文件，通过 `meta.md` 管理元信息，`outline.md` 管理大纲和时长分配
- 新增 `md-to-html-pipeline` 能力：用确定性 Python 脚本将 Markdown 转换为此 skill 已有的三模式（DOC/PPT/Zoom）自包含 HTML
- 新增 `dual-mode-output` 能力：同一份 Markdown 产出两种阅读体验——PPT 模式仅显示视觉层（投屏给观众），DOC 模式将视觉层嵌入读者叙述层形成完整文章（供无语音环境下的读者理解）
- 新增 `speaker-script` 能力：单独的 `speaker-script.md` 文件记录演讲者的串词和舞台指示，不渲染到 HTML 中
- 演进 `share-as-html` skill：SKILL.md 新增 Markdown 工作流指导，AI 的职责从"直接生成 HTML"变为"帮助创作 Markdown + 运行脚本转换"
- 引入 `override.css` 机制：生成的 HTML 使用稳定的 class 名，人类可通过 CSS 文件精准调整布局和风格，脚本重新生成时 class 名不变

## Capabilities

### New Capabilities

- `markdown-slide-authoring`: 用 Markdown + YAML frontmatter 描述分享内容，包括元信息（meta.md）、大纲与时长（outline.md）、每页 PPT 内容（slides/*.md）。YAML frontmatter 控制布局参数（layout、cols、ratio、gap、accent），Markdown 正文保持纯净。
- `md-to-html-pipeline`: 确定性 Python 脚本将上述 Markdown 文件转换为 share-as-html 格式的自包含 HTML。支持自定义 HTML 标签（`<grid>`、`<card>`、`<callout>` 等）和标准 Markdown 语法。脚本完全确定、无 AI 依赖。
- `dual-mode-output`: 同一 Markdown 源文件渲染为 PPT 模式和 DOC 模式。PPT 模式仅显示视觉层（投屏、逐页切换），DOC 模式将 `<!-- reader -->...<!-- /reader -->` 区域的读者叙述与视觉层结合，呈现为可阅读的文章。
- `speaker-script`: 独立的演讲稿文件（`speaker-script.md`），包含演讲者串词、舞台指示、计时提醒。此文件不参与 HTML 渲染，仅演讲者自己使用。

## Impact

- `skills/share-as-html/SKILL.md`：新增 Markdown 工作流章节，更新 AI 操作指导
- 新增 `md2html.py`：核心转换脚本（Python，依赖 markdown、Jinja2、PyYAML）
- 新增 `template.html`：Jinja2 模板，包含现有 CSS + JS
- 新增示例项目目录：`example-talk/`（含 meta.md、outline.md、slides/*.md、speaker-script.md）
- 现有 HTML 测试文件不直接受影响（仍使用直接 HTML 路径）
