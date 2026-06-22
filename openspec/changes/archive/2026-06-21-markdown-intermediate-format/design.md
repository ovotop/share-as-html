## Context

当前 `share-as-html` skill 的产出物是自包含 HTML 文件，内容、CSS、JS 全部交织在一个文件中。人类修改内容需要在 HTML 源码中定位对应标签，体验极差。同时 HTML 是构建产物而非源文件——作者真正应该编辑的是内容本身。

本设计引入 Markdown 作为中间格式，将"创作内容"与"渲染 HTML"解耦。核心思路：Markdown 是源，HTML 是构建产物；脚本做转换，AI 帮忙写 Markdown。

## Goals / Non-Goals

**Goals:**
- 提供一套 Markdown 文件结构，完整描述一个技术分享的所有信息（元信息、大纲、每页内容、演讲稿）
- YAML frontmatter 控制布局参数，Markdown 正文保持纯净、可读
- Python 脚本确定性转换 Markdown → HTML，不依赖 AI
- 同一份 Markdown 源产出两种阅读体验：PPT 模式（投屏）和 DOC 模式（文章阅读）
- 人类可通过 YAML frontmatter 和 override.css 调整布局和风格
- 演讲稿独立存放，不渲染到 HTML

**Non-Goals:**
- 不提供 WYSIWYG 编辑器
- 不替换现有直接生成 HTML 的路径（两者共存）
- 不支持 Markdown 内写完整 CSS（用 YAML frontmatter + override.css 替代）
- 不做实时预览（运行脚本即可看到结果）

## Decisions

### 1. 文件结构：按页面拆分 + 独立演讲稿

```
my-talk/
├── meta.md              ← 分享元信息（title, subtitle, speaker, date, duration）
├── outline.md           ← 大纲与时长分配
├── speaker-script.md    ← 演讲稿（不渲染到 HTML）
├── slides/
│   ├── 01-cover.md
│   ├── 02-motivation.md
│   └── ...
├── override.css         ← 人类调整布局/风格（可选）
├── assets/              ← 图片等资源
└── output/
    └── sharing.html     ← 构建产物
```

**替代方案**：单文件 Markdown。

**为什么不选**：单文件难以管理——大纲、元信息、每页内容、演讲稿混在一起。多文件让每个部分职责清晰，git diff 也更有意义。

### 2. 布局控制：YAML frontmatter

每个 slide 的 `.md` 文件顶部使用 YAML frontmatter：

```yaml
---
slide: 2
duration: 5min
layout: grid           # grid | flex | stack | split | default
cols: 2                # 列数
ratio: "1/1"           # 列宽比
gap: 24                # 间距(px)
accent: blue           # 强调色
---
```

脚本读取 frontmatter 决定 HTML 结构。Markdown 正文不包含布局标签。

**替代方案**：内联 HTML 标签或自定义 directive。

**为什么不选**：HTML 标签污染 Markdown 可读性。Directive 语法（`:::grid`）虽然可读，但解析复杂度高。YAML frontmatter 是 Markdown 生态的标准做法，人类和 AI 都能轻松编辑，且与正文完全分离。

### 3. 转换引擎：Python 脚本（md2html.py）

```python
def convert(input_dir, output_path):
    meta = parse_frontmatter("meta.md")
    slides = [parse_slide(f) for f in sorted(glob("slides/*.md"))]
    html = render_template("template.html", meta=meta, slides=slides)
    write(output_path, html)
```

依赖：`markdown` (Markdown → HTML)、`PyYAML` (frontmatter 解析)、`Jinja2` (模板渲染)。

**替代方案**：Node.js + unified/remark。

**为什么不选**：Python 的 Markdown 和 Jinja2 生态更成熟，依赖更少，脚本更短。

### 4. 三层内容模型

每个 slide 文件包含两层，演讲稿单独一层：

- **Visual 层**：Markdown 正文中 `<!-- reader -->` 之前的内容。PPT 模式显示，DOC 模式也显示。
- **Reader 层**：`<!-- reader -->...<!-- /reader -->` 之间的内容。PPT 模式隐藏，DOC 模式作为文章正文展示。
- **Speaker 层**：`speaker-script.md` 独立文件，不渲染到 HTML。

Reader 层写作要求：站在读者角度，将演讲者口头表达的内容写成可阅读的散文。

**替代方案**：将所有层放在同一个 Markdown 中用分隔符区分。

**为什么不选**：演讲稿内容量大、结构不同（含舞台指示和计时提醒），独立文件更清晰。

### 5. 人类调整机制：override.css

生成的 HTML 使用稳定的语义 class 名：
- `.slide-N` — 第 N 页
- `.card-M` — 该页第 M 张卡片
- `.reader-narrative` — reader 层容器

人类编写 `override.css`，脚本生成 HTML 时在 `<head>` 中自动引入。重新生成 Markdown 后 class 名不变，CSS 规则继续生效。

**替代方案**：在 frontmatter 中提供更多布局参数覆盖所有场景。

**为什么不选**：frontmatter 无法覆盖所有视觉需求（如某个元素的阴影、动画、背景图）。CSS 是 Web 标准的表达方式，给懂 CSS 的人一个稳定的后门。

### 6. 与现有 skill 的关系

SKILL.md 新增 **Markdown 工作流**章节，AI 操作指导更新为：

1. 用户请求创建分享 → AI 生成 Markdown 文件（不直接生成 HTML）
2. AI 运行 `python md2html.py <project_dir>` 脚本
3. AI 打开生成的 HTML 供用户预览
4. 用户要求调整内容 → AI 修改 .md 文件 → 重新运行脚本

现有"直接生成 HTML"路径保留，当用户明确要求快速生成简单分享时仍可使用。

## Risks / Trade-offs

- **Markdown 表达力有限**：复杂布局可能需要 fallback 到原始 HTML。→ 脚本透传 Markdown 中的 HTML 片段；override.css 提供精准控制。
- **脚本依赖**：用户环境需要 Python + 三个 pip 包。→ 在 AGENTS.md 中记录安装命令，CI 可预装。
- **双路径维护成本**：同时维护"生成 HTML"和"生成 Markdown"两条路径。→ Markdown 路径是推荐路径，HTML 路径仅作快速原型。

## Open Questions

无。设计已在探索阶段充分讨论并达成共识。
