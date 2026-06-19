## Context

现有的 `sharing-preview.html` 展示了一套成熟的技术分享 HTML 风格：深色主题（`#0f172a`）、组件化卡片、代码高亮、slide 结构。但它是一个静态文档，缺少交互能力。

用户需要一个 skill 来标准化这种分享文档的创建，并增加双模式切换：
- **Doc 模式**：自由滚动，便于阅读和分享链接
- **PPT 模式**：整屏翻页，便于演讲演示

## Goals / Non-Goals

**Goals:**
- 创建 `sharing-doc` skill，指导 Agent 生成带双模式的 HTML 分享文档
- 内置键盘交互：Enter 切换模式、方向键翻页、空格键向下
- 预置 sharing-preview.html 风格的深色主题 CSS 组件库
- 产出物为完全自包含的 HTML 文件，无外部依赖

**Non-Goals:**
- 不支持主题切换（仅深色主题）
- 不支持动画过渡效果（保持简洁）
- 不支持导出 PDF（浏览器原生打印即可）

## Decisions

### D1: 三状态状态机 — DOC / PPT_FULL / PPT_ZOOM

**选择**：三个状态通过 CSS class（`mode-doc` / `mode-ppt` / `mode-zoom`）+ JS 状态变量管理。

```
DOC ──Enter──→ PPT_FULL ──Enter(diagram focused)──→ PPT_ZOOM
  ↑                ↑                                    │
  └──Esc───────────└────────────────Esc────────────────┘
```

**备选方案**：
- 两个独立 HTML 文件 → 维护成本高，内容重复
- iframe 嵌套 → 性能差，通信复杂
- 纯两状态（DOC/PPT）→ 无法处理图片放大浏览

**理由**：三状态模型清晰覆盖所有交互场景，class 切换实现简单。

### D2: PPT 模式翻页机制 — scroll-snap + JS 键盘

**选择**：CSS `scroll-snap-type: y mandatory` + JS 监听键盘事件控制 `scrollTo`。

**理由**：scroll-snap 提供原生整屏吸附，JS 键盘监听提供精确控制，两者结合最佳。

### D3: 图片/Mermaid Zoom — 运行时动态判断

**选择**：渲染后比较元素尺寸 vs viewport 尺寸，决定完全显示还是放大显示。

**判断逻辑**：
- 元素宽高均 ≤ viewport → 完全显示（`PPT_FULL`）
- 宽度 > viewport 或 高度 > viewport → 放大显示（`PPT_ZOOM`）
- 无法明确判断时 → 询问用户

**备选方案**：
- 生成时静态判断（`data-zoom`）→ 需要手动标注，增加内容创作者负担
- 固定策略（全部放大/全部完全显示）→ 不够灵活

**理由**：运行时判断零负担，且能根据实际渲染结果自适应。

### D4: 焦点管理 — 条件激活 + no-focus 过滤

**选择**：
- 仅当当前 slide 有多个水平排列的可聚焦 diagram 时，才激活焦点切换
- 焦点指示器用 `2px solid var(--accent)` 边框高亮
- 支持 `.no-focus` class 排除特定 diagram（如装饰性图片）
- `handleFocusSwitch` 过滤 `.no-focus` 元素，只在可聚焦元素间切换
- ArrowLeft/ArrowRight 必须调用 `e.preventDefault()` 防止浏览器默认行为干扰

**理由**：条件激活避免不必要的交互复杂度，no-focus 支持混合布局场景。

### D5: Mermaid 支持 — CDN 引入

**选择**：通过 CDN 引入 mermaid.js，`theme: 'dark'` 配合深色主题。

**理由**：CDN 方案文件小，mermaid ~1MB 不内联，保持 HTML 轻量。

### D6: Skill 结构 — 单文件 SKILL.md + 代码模板

**选择**：一个 SKILL.md 文件，包含触发规则、工作流、CSS 模板、JS 模板。

**理由**：skill 文件自包含，Agent 加载后即可直接使用，无需额外文件。

### D7: CSS 组件库来源 — 提取 sharing-preview.html 的样式

**选择**：从 sharing-preview.html 提取 CSS 变量和组件样式，作为 skill 的内置模板。

**理由**：复用已验证的视觉风格，保持一致性。

### D8: Doc 模式滚动体验 — 连续文档流

**选择**：doc 模式下调整 slide 样式为连续文档流：
- `min-height` 从 `100vh` 降为 `auto`（内容决定高度）
- `padding` 从 `60px 80px` 缩小为 `32px 40px`
- `border-bottom` 去掉（无分割线）
- PPT 模式保持原有全屏吸附样式不变

**实现方式**：通过 `body.mode-ppt` 的 CSS 覆盖，doc 模式为默认样式。

**备选方案**：
- 保留 border 但淡化（`rgba(边框, 0.2)`）→ 仍有视觉断层
- 完全连续流 + section 标记 → 过度设计

**理由**：doc 模式强调阅读流畅性，PPT 模式强调整屏展示，两种模式的视觉差异本身就是功能区分。

## Risks / Trade-offs

- **[Risk] scroll-snap 在某些浏览器兼容性问题** → Mitigation: 使用 `scroll-snap-type: y proximity` 作为 fallback
- **[Risk] 键盘事件可能与浏览器快捷键冲突** → Mitigation: 仅监听特定键（Enter/Arrow/Space），不阻止其他按键
- **[Trade-off] 单文件 vs 多文件** → 选择单文件，牺牲模块化换取易用性
- **[Risk] ArrowLeft/ArrowRight 未 preventDefault 导致焦点切换失效** → Mitigation: 所有方向键必须调用 preventDefault
