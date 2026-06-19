## Why

技术分享场景需要一种轻量、可复用的方式来创建 HTML 演示文档。现有的 `sharing-preview.html` 展示了优秀的视觉风格（深色主题、组件化卡片、代码高亮），但缺少两种关键的交互模式：自由滚动的文档模式（便于阅读）和整屏翻页的演示模式（便于演讲）。需要一个 skill 来标准化这种分享文档的创建流程，并内置双模式切换能力。

## What Changes

- 新增 `sharing-doc` skill，用于创建带 doc/ppt 双模式切换的 HTML 分享文档
- 内置键盘交互：Enter 切换模式、方向键翻页、空格键向下滚动
- 预置 sharing-preview.html 风格的深色主题 CSS 组件库
- 支持 mermaid 图表（CDN 引入）和图片的 zoom 浏览
- 产出物为自包含 HTML 文件，无外部依赖

## Capabilities

### New Capabilities

- `sharing-doc-generator`: 生成带 doc/ppt 双模式切换的 HTML 分享文档，包含深色主题 CSS 组件库、slide 结构模板、键盘交互逻辑

### Modified Capabilities

（无现有 spec 需要修改）

## Impact

- 新增 skill 文件：`~/.opencode/skills/sharing-doc/SKILL.md`
- 产出物为自包含 HTML 文件，无外部依赖
