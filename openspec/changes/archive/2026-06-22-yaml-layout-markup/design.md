## Context

当前 md2html.py 的 slide 解析流程：
```
frontmatter 提取 → extract_mermaid → md.convert() → process_custom_tags → restore_mermaid → wrap_visual → 输出
```

`process_custom_tags` 用正则把 `<card>`、`<callout>`、`<steps>` 替换为 `<div class="card">` 等 HTML。
`wrap_visual` 根据 `layout:` 值把内容包进 grid-N / flex-row / split-layout 等容器。

两个函数运行在 markdown 转换**之后**，此时 Python-Markdown 已经把自定义标签拆散在 `<p>` 里，导致三个已验证的 bug (`<p>` 拆散 card、grid 内 markdown 不解析、`<p><div>` 嵌套)。

约束：Python-Markdown 的 `md_in_html` 扩展要求 HTML block 元素显式声明 `markdown="1"` 才解析内部 markdown；未知标签（`<card>`）被当 inline 元素强制 `<p>` 包裹。

## Goals / Non-Goals

**Goals:**
- 布局信息完全从前端 matter 的 YAML 描述，不进 body
- body 为纯 Markdown（零 HTML 标签），可读性等同于 README
- 消除问题 1/2/5 的根因：Markdown parser 不再看到任何自定义标签
- YAML 语法覆盖现有所有布局场景：card、callout、steps、metrics、split、raw
- 迁移 example-talk (4 页) 和 android-cli-docing (20 页)

**Non-Goals:**
- 不改 CSS/JS template、不改键盘导航、不改 zoom/focus 逻辑
- 不改 meta.md / outline.md / speaker-script.md / override.css 机制
- 不增加新的 Python 依赖
- 不支持运行时动态布局（所有布局在生成时确定）

## Decisions

### D1: YAML grid 语法：对象数组表示法

```yaml
layout:
  grid:
    - [{card: "卡片标题"}, {card: "卡片标题"}, {card: "卡片标题"}]
    - [{callout: "warning"}]
    - [{metrics: null}]
```

每个 cell 是单键 YAML mapping：`{type: param}`。`type` 是 cell 类型，`param` 是类型参数（card 是标题，callout 是 variant，无参数用 `null`）。

**Alias 简化**（可选，YAML anchors 支持）：
```yaml
- &C {card: "标题"}
- &W {callout: "warning"}
- &N {callout: null}
```

**为什么不用更 Flat 的语法**：`card "标题"` 不是合法 YAML；`"card 标题"` 字符串需要二次解析（空格分隔），title 含空格时需引号转义，引入不必要的歧义。

### D2: `=== slot ===` 分隔符映射 body slot

body 以 YAML frontmatter 结束后的内容开始。Heading（`## 标题`）位于 body 顶部。`=== slot ===` 分隔后续的 cell 内容。

```
---
slide: 7
layout:
  grid:
    - [{card: "Card A"}, {card: "Card B"}]
    - [{callout: "info"}]
---
## 页面标题

这是 Card A 的内容。
**markdown** 正常解析。

=== slot ===

这是 Card B 的内容。
`inline code` 也正常。

=== slot ===

这是 callout 内容。
```

Slot 分配：按 grid 行优先顺序（row-major），每个 cell 对应一个 slot。body 用 `rsplit('\n=== slot ===\n', maxsplit=N-1)` 从右往左切 N 个槽。

**为什么 `=== slot ===` 而非 `---`**：`---` 在 Markdown 中是水平线 `<hr>`，body 内可能同时需要 `<hr>` 和槽分隔——同一种字符串无法区分两种意图。`=== slot ===` 是纯标记语言指令，不可能与任何 Markdown 内容元素冲突。

### D3: 新 `parse_slide()` 流程

```
frontmatter 提取
  ↓
解析 layout.grid → 展开为 cell 列表 (type + param)
  ↓
body 按 `=== slot ===` 分 slot（rsplit，从右往左 N-1 次）
  ↓
提取 heading（body 中第一个 ## 标题）
  ↓
逐 cell 处理：
  - 取对应 slot markdown
  - md.convert(slot_md) → slot_html
  - 根据 cell type 包裹容器 HTML
  ↓
按 grid 行组合 → 换行 grid-N → 拼接 heading → 输出
```

关键变化：
- **`process_custom_tags()` 删除**：不再需要 `<card>`→`<div>` 转换，因为卡片在 YAML 中描述
- **`wrap_visual()` 简化**：不再需要 auto-card-detection、`split_top_level_blocks` 块拆分、grid 包裹逻辑——这些由 `assemble_grid()` 处理
- **每个 cell 独立 markdown 转换**：消除了问题 2（grid 内 markdown 不解析），因为每个 slot 是直接从 markdown 源转换的，不是从 HTML 字符串提取的
- **extract_mermaid / restore_mermaid 保留**：mermaid 块在每个 slot 的 markdown 转换前提取、转换后还原（逻辑不变）

### D4: Cell 类型全集

| 类型 | 语法 | 参数 | CSS class | 说明 |
|------|------|------|-----------|------|
| `card` | `{card: "标题"}` | 标题文本 | `.card` + `<h4>` | 标准卡片 |
| `callout` | `{callout: "warning"}` | variant (info/warning/tip/danger) | `.callout.callout-{variant}` | 高亮块 |
| `steps` | `{steps: null}` | — | `.steps` + `.step` | 序号步骤列表 |
| `metrics` | `{metrics: null}` | — | `.metrics-row` + `.metric` | 指标面板。body 写 `值 : 标签` 行 |
| `split` | `{split: null}` | — | `.split-layout` | 双栏对比。占用 2 个 slot |
| `raw` | `{raw: null}` | — | 无外层容器 | 裸 markdown，用于 heading 下方直接跟图片或段落 |

### D5: Grid 行 → HTML 映射

每行 cell 数决定 CSS grid class：

| 行 cell 数 | 生成容器 |
|-----------|---------|
| 1 | 无 grid 包裹（全宽） |
| 2 | `<div class="grid-2">` |
| 3 | `<div class="grid-3">` |
| 4 | `<div class="grid-4">` |
| 5+ | 超出时拆为多行或截断 |

每行独立生成 grid 容器，不同行可以有不同的列数。

### D6: heading 位置

Heading（`## 页面标题`）保持在 body 顶部，frontmatter 之后、第一个 `---` 之前。标记为纯 markdown 文本，单独经过 `md.convert()` 生成 `<h2>`。

现有的 `emoji:` frontmatter 字段保持，自动注入到 heading HTML 中（已有逻辑）。

### D7: `<!-- reader -->` 块

`<!-- reader -->...<!-- /reader -->` 标记保留在每个 slot 的 markdown 中。如果某个 slot 包含 reader 块，`split_visual_reader()` 照常拆分。reader 内容与所属 cell 一起进入 `.reader-narrative` 区域。

## Risks / Trade-offs

**[Risk] 20 页 slide 迁移工作量大**
→ Mitigation: 大部分页面结构简单（2-3 个 card + optional callout）。用脚本做第一次自动迁移，人工验证。迁移完成后旧语法直接报错（不保留兼容）。

**[Risk] 旧 frontmatter `layout: grid` 字段与新 `layout.grid` 冲突**
→ Mitigation: `layout` 从字符串变为可包含 `grid` 子键的 mapping。`parse_slide()` 中检测：如果 `layout` 是字符串 → 报错提示使用新语法；如果是 dict 且含 `grid` 键 → 新语法模式。

## Migration Plan

1. 实现 `assemble_grid()` 和新的 `parse_slide()` 流程（直接替换旧的）
2. 迁移 example-talk 4 页（手动，页数少）
3. 迁移 android-cli-docing 20 页（半自动脚本 + 人工验证）
4. 更新 `SKILL.md` 文档
5. 运行 `python md2html.py` 重新生成两份 sharing.html
6. 运行 Playwright 测试确认三态模式、键盘导航、zoom 正常
7. 对比新旧 HTML 输出的视觉一致性（通过浏览器截图对比）

## Open Questions

1. **`layout: flex` / `layout: stack` 在新语法中如何表达？** 当前生产页面未使用这两个模式（只有 grid/default）。可以暂不支持，保持 YAML grid 只画 grid。如未来需要，通过 `layout.flex` 或 `layout.stack` 键扩展。

2. **heading 是否应该也进 YAML？** 当前设计 heading 仍在 body 顶部 markdown 中。好处是不改现有习惯。坏处是 layout 信息分散在两处。倾向于保持现状——标题是"内容"而非"布局"。

## Resolved

- **槽分隔符**: 选 `=== slot ===`，零语义冲突，自解释，`rsplit` 从右往左 N-1 次取分隔点。
- **旧语法兼容**: Breaking change。直接移除，检测到旧 `layout: grid` 字符串时清晰报错。
- **`<div markdown="1">`**: 新系统不需要。每个 slot 是独立 markdown，`raw` cell 承载无容器内容。
- **B 内 `<hr>`**: 用 `***` 或 `---` 写在 slot 内容里。分隔符 `=== slot ===` 不与任何 Markdown 元素冲突。
