## ADDED Requirements

### Requirement: 生成带三模式的 HTML 分享文档

Skill SHALL 指导 Agent 生成自包含的 HTML 文件，支持 doc、ppt-full、ppt-zoom 三种浏览模式。

#### Scenario: 生成 doc 模式默认的 HTML 文件

- **WHEN** Agent 按 skill 指引生成 HTML 分享文档
- **THEN** 产出物 SHALL 是完全自包含的 HTML 文件（所有 CSS/JS 内联，mermaid 除外走 CDN）
- **AND** 默认以 doc 模式呈现（自由滚动）
- **AND** 包含分享标题和页码指示器

### Requirement: 三状态模式切换

用户 SHALL 能够通过键盘在三种模式之间切换。

#### Scenario: Enter 键从 DOC 进入 PPT_FULL

- **WHEN** 用户在 doc 模式下按 Enter 键
- **THEN** 视图 SHALL 切换为 PPT_FULL 模式（整屏翻页）
- **AND** 当前视口 SHALL 吸附到距离**视口中心**最近的 slide（而非顶部）
- **AND** 切换 SHALL 为瞬时定位（无平滑滚动动画）

#### Scenario: Enter 键从 PPT_FULL 进入 PPT_ZOOM

- **WHEN** 用户在 PPT_FULL 模式下按 Enter 键
- **AND** 当前 slide 有聚焦的 diagram（图片或 mermaid）
- **THEN** 视图 SHALL 切换为 PPT_ZOOM 模式（图片放大显示）

#### Scenario: Esc 键从 PPT_ZOOM 返回 PPT_FULL

- **WHEN** 用户在 PPT_ZOOM 模式下按 Esc 键
- **THEN** 视图 SHALL 退出 zoom，返回 PPT_FULL 模式
- **AND** 焦点 SHALL 回到之前的 diagram
- **AND** 切换 SHALL 为瞬时定位（无平滑滚动动画）

#### Scenario: Esc 键从 PPT_FULL 返回 DOC

- **WHEN** 用户在 PPT_FULL 模式下按 Esc 键
- **THEN** 视图 SHALL 切换为 doc 模式（自由滚动）
- **AND** 当前 slide SHALL 垂直居中于视口（`slideCenter - viewportCenter` 定位）
- **AND** 切换 SHALL 为瞬时定位（无平滑滚动动画）

### Requirement: 模式切换均为瞬时定位

所有模式间的切换 SHALL 使用瞬时定位，不使用平滑滚动动画，确保切换响应即时。

#### Scenario: 所有 scrollIntoView 和 scrollTo 使用 instant

- **WHEN** 任何模式切换触发滚动定位（DOC→PPT、PPT→DOC、PPT slide 翻页、ZOOM→PPT）
- **THEN** 滚动 SHALL 使用 `behavior: 'instant'`（而非 `'smooth'`）

### Requirement: PPT_FULL 模式键盘导航

PPT_FULL 模式下，用户 SHALL 能够通过键盘翻页和切换焦点。

#### Scenario: 方向键上下翻页

- **WHEN** 用户在 PPT_FULL 模式下按 ArrowDown 或 Space 键
- **THEN** 视图 SHALL 向下滚动一个 slide 整屏
- **AND** 视图 SHALL 瞬时吸附到下一个 slide 的顶部（无平滑滚动动画）

#### Scenario: 方向键向上翻页

- **WHEN** 用户在 PPT_FULL 模式下按 ArrowUp 键
- **THEN** 视图 SHALL 向上滚动一个 slide 整屏
- **AND** 视图 SHALL 瞬时吸附到上一个 slide 的顶部（无平滑滚动动画）

#### Scenario: 首尾 slide 边界处理

- **WHEN** 用户在第一个 slide 按 ArrowUp
- **THEN** 视图 SHALL 保持在第一个 slide，不循环

- **WHEN** 用户在最后一个 slide 按 ArrowDown
- **THEN** 视图 SHALL 保持在最后一个 slide，不循环

#### Scenario: 多 diagram 焦点切换（条件激活）

- **WHEN** 当前 slide 有多个水平排列的可聚焦 diagram（`<img>` 或 mermaid SVG）
- **THEN** 左右键 SHALL 在 diagram 之间切换焦点
- **AND** 焦点 diagram SHALL 显示 `2px solid var(--accent)` 边框高亮

#### Scenario: 单 diagram 或无 diagram 时不激活焦点

- **WHEN** 当前 slide 只有一个可聚焦 diagram 或没有 diagram
- **THEN** 左右键 SHALL 不激活焦点切换

### Requirement: PPT_ZOOM 模式图片浏览

PPT_ZOOM 模式下，用户 SHALL 能够浏览放大的图片/mermaid 图。

#### Scenario: 图片全屏展示

- **WHEN** 视图进入 PPT_ZOOM 模式
- **THEN** 图片/mermaid SVG SHALL 全屏展示，保持宽高比
- **AND** 超出 viewport 的部分 SHALL 可滚动

#### Scenario: 横向滚动

- **WHEN** 用户在 PPT_ZOOM 模式下按 ArrowLeft 或 ArrowRight
- **THEN** 图片 SHALL 横向滚动

#### Scenario: 纵向滚动与边界穿透

- **WHEN** 用户在 PPT_ZOOM 模式下按 ArrowUp 或 ArrowDown
- **THEN** 图片 SHALL 纵向滚动
- **AND** 当图片滚动到顶部时按 ArrowUp → 翻页到上一个 slide
- **AND** 当图片滚动到底部时按 ArrowDown → 翻页到下一个 slide

### Requirement: 图片/Mermaid 复杂度判断

系统 SHALL 在运行时判断图片是否需要放大显示。

#### Scenario: 完全显示条件

- **WHEN** 渲染后的图片/mermaid SVG 宽高均 ≤ viewport 对应尺寸
- **THEN** 图片 SHALL 在 slide 内完全显示，无需 zoom

#### Scenario: 放大显示条件

- **WHEN** 渲染后的图片/mermaid SVG 宽度 > viewport 宽度 或 高度 > viewport 高度
- **THEN** 图片 SHALL 支持 zoom 模式（Enter 进入 PPT_ZOOM）

#### Scenario: 无法判断时询问用户

- **WHEN** 系统无法明确判断图片复杂度
- **THEN** 系统 SHALL 询问用户选择显示模式

### Requirement: Mermaid 支持

Skill SHALL 支持 mermaid 图表渲染。

#### Scenario: Mermaid CDN 引入

- **WHEN** 产出物包含 mermaid 图
- **THEN** HTML SHALL 通过 CDN 引入 mermaid.js（`https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js`）
- **AND** 初始化配置 SHALL 使用 `theme: 'dark'`

#### Scenario: Mermaid 渲染后判断 zoom

- **WHEN** mermaid 渲染完成后
- **THEN** 系统 SHALL 检查 SVG 尺寸判断是否需要 zoom
- **AND** zoom 模式下 SVG 容器 SHALL 支持滚动（`overflow: auto`）

### Requirement: 焦点管理

多个可聚焦 diagram 时，系统 SHALL 管理焦点状态。

#### Scenario: 焦点指示器

- **WHEN** diagram 获得焦点
- **THEN** SHALL 显示 `2px solid var(--accent)` 边框高亮

#### Scenario: 焦点切换

- **WHEN** 用户在 PPT_FULL 模式下按左右键（且有多个水平排列的可聚焦 diagram）
- **THEN** 焦点 SHALL 在 diagram 之间移动
- **AND** 新焦点 diagram SHALL 显示边框高亮
- **AND** ArrowLeft/ArrowRight 事件 SHALL 调用 `e.preventDefault()` 防止浏览器默认行为

#### Scenario: no-focus 过滤

- **WHEN** diagram 带有 `.no-focus` class
- **THEN** 该 diagram SHALL 不参与焦点切换
- **AND** 焦点 SHALL 跳过该 diagram，直接切换到下一个可聚焦 diagram

### Requirement: Doc 模式滚动体验

doc 模式 SHALL 提供连续文档流体验，与 PPT 模式形成明确对比。

#### Scenario: Doc 模式 slide 样式

- **WHEN** 视图处于 doc 模式（默认）
- **THEN** `.slide` 的 `min-height` SHALL 为 `auto`（内容决定高度）
- **AND** `padding` SHALL 缩小为 `32px 40px`
- **AND** `border-bottom` SHALL 移除（无分割线）

#### Scenario: PPT 模式 slide 样式

- **WHEN** 视图切换到 PPT_FULL 模式
- **THEN** `.slide` SHALL 恢复 `min-height: 100vh` 和 `padding: 60px 80px`
- **AND** `border-bottom` SHALL 恢复为 `1px solid var(--border)`

### Requirement: 内容约束

Skill SHALL 指导 Agent 避免使用 ASCII 图。

#### Scenario: 避免 ASCII 图

- **WHEN** Agent 生成分享内容
- **THEN** SHALL 优先使用 mermaid 或图片替代 ASCII 图
- **AND** SHALL 在指引中说明 ASCII 图中文对齐困难的问题

### Requirement: 深色主题 CSS 组件库

Skill SHALL 提供预置的深色主题 CSS，风格与 sharing-preview.html 一致。

#### Scenario: CSS 变量和组件可用

- **WHEN** Agent 使用 skill 生成 HTML
- **THEN** 产出物 SHALL 包含以下 CSS 组件：
  - 深色主题 CSS 变量（`--bg: #0f172a` 等）
  - `.slide` 容器样式（全屏高度、内边距、flex 布局）
  - `.slide-number` 页码指示器
  - `.card` 卡片组件
  - `.point` / `.point.highlight` 要点组件
  - `.tag` 标签组件
  - `.metric` / `.metrics-row` 关键数字组件
  - `.flow` / `.flow-item` 编号流程组件
  - `pre > code` 代码块（带 `.cmd` `.comment` `.string` `.keyword` 高亮）
  - `.mermaid` 容器样式
  - `.focused` 焦点状态样式
  - `body.mode-zoom` zoom 模式样式

### Requirement: Slide 结构模板

Skill SHALL 提供 slide 的标准 HTML 结构模板。

#### Scenario: Slide HTML 结构

- **WHEN** Agent 创建新 slide
- **THEN** SHALL 使用以下结构：
  ```html
  <div class="slide">
      <span class="slide-number">N</span>
      <div class="content">
          <h2><span class="emoji">X</span> 标题</h2>
          内容...
      </div>
  </div>
  ```
