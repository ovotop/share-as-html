## 1. 创建 Skill 文件

- [x] 1.1 创建 `~/.opencode/skills/sharing-doc/SKILL.md` 文件，包含 skill 元数据（name, description）
- [x] 1.2 编写触发规则：何时激活此 skill（"分享"、"演示"、"slides"、"技术分享"等关键词）
- [x] 1.3 编写工作流：确定输出位置 → 生成 HTML → 写入文件 → 浏览器打开
- [x] 1.4 编写内容约束：**避免 ASCII 图**（中文对齐困难），优先用 mermaid 或图片

## 2. CSS 模板

- [x] 2.1 提取 sharing-preview.html 的 CSS 变量（`:root` 部分，深色主题配色）
- [x] 2.2 编写 `.slide` 容器样式（doc 模式：自由滚动；ppt 模式：scroll-snap 吸附）
- [x] 2.3 编写组件样式：`.slide-number`、`.card`、`.point`、`.point.highlight`、`.tag`、`.metric`、`.flow`、`pre > code`
- [x] 2.4 编写 ppt 模式专用样式：`body.mode-ppt` 下 `.slide` 的 `scroll-snap-align: start` 和 `min-height: 100vh`
- [x] 2.5 编写 mermaid 容器样式：`.mermaid` 在 ppt 模式下的布局约束
- [x] 2.6 编写图片/mermaid 焦点样式：`:focus` 或 `.focused` 状态下 `2px solid var(--accent)` 边框高亮
- [x] 2.7 编写 zoom 模式样式：`body.mode-zoom` 下图片/mermaid 全屏展示，支持内部滚动

## 3. JS 模板 — 三状态状态机

状态模型：`DOC` → `PPT_FULL` → `PPT_ZOOM`

```
DOC ──Enter──→ PPT_FULL ──Enter(diagram focused)──→ PPT_ZOOM
  ↑                ↑                                    │
  └──Esc───────────└────────────────Esc────────────────┘
```

### 3.1 模式切换

- [x] 3.1.1 Enter 键：`DOC` → `PPT_FULL`（自动吸附到最近 slide）
- [x] 3.1.2 Esc 键：`PPT_ZOOM` → `PPT_FULL`（返回完全显示），`PPT_FULL` → `DOC`
- [x] 3.1.3 状态变量管理：当前状态、当前 slide 索引、当前焦点 diagram 索引

### 3.2 DOC 模式

- [x] 3.2.1 自由滚动，方向键正常滚动页面
- [x] 3.2.2 Enter 键切换到 PPT_FULL

### 3.3 PPT_FULL 模式

- [x] 3.3.1 ArrowUp/ArrowDown/Space：上下翻页（scroll-snap 吸附）
- [x] 3.3.2 左右键行为：仅当当前 slide 有多个水平排列的可聚焦 diagram 时，才激活焦点切换；否则左右键不响应（或可选：左右键也翻页）
- [x] 3.3.3 焦点激活条件：多个 `<img>` 或 mermaid SVG 水平排列 + 均具备焦点能力
- [x] 3.3.4 Enter 键：如果有 diagram 聚焦 → 进入 PPT_ZOOM；无聚焦 → 不响应
- [x] 3.3.5 Esc 键：返回 DOC 模式

### 3.4 PPT_ZOOM 模式

- [x] 3.4.1 图片/mermaid 全屏展示，保持宽高比
- [x] 3.4.2 ArrowLeft/ArrowRight：图内横向滚动
- [x] 3.4.3 ArrowUp/ArrowDown：图内纵向滚动；滚到顶/底后，穿透到 slide 翻页
- [x] 3.4.4 Esc 键：退出 zoom，返回 PPT_FULL

### 3.5 复杂度判断

- [x] 3.5.1 运行时动态判断：渲染后比较元素尺寸 vs viewport 尺寸
- [x] 3.5.2 完全显示条件：元素宽高均 ≤ viewport 对应尺寸
- [x] 3.5.3 放大显示条件：元素宽度 > viewport 宽度 或 高度 > viewport 高度
- [x] 3.5.4 兜底策略：无法明确判断时，询问用户选择模式

### 3.6 Mermaid 支持

- [x] 3.6.1 引入 Mermaid.js CDN（`https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js`）
- [x] 3.6.2 初始化 mermaid（`startOnLoad: true, theme: 'dark'`）
- [x] 3.6.3 mermaid 渲染完成后，检查 SVG 尺寸判断是否需要 zoom
- [x] 3.6.4 zoom 模式下，SVG 容器支持滚动（`overflow: auto`）

## 4. HTML 结构模板

- [x] 4.1 编写标准 slide HTML 结构模板（`.slide` + `.slide-number` + `.content`）
- [x] 4.2 编写封面 slide 模板（`.cover` 样式）
- [x] 4.3 编写常用布局模板：两列网格（`.grid-2`）、代码块、表格
- [x] 4.4 编写图片/mermaid 容器模板（支持 `data-focusable` 属性标记可聚焦）

## 5. Skill 指引文档

- [x] 5.1 编写 skill 使用说明：如何调用、参数说明
- [x] 5.2 编写内容填充指南：每个 slide 应包含什么（标题、要点、代码示例等）
- [x] 5.3 编写 mermaid 使用指南：语法参考、dark theme 配置
- [x] 5.4 编写图片使用指南：推荐尺寸、zoom 行为说明

## 6. 验证

- [x] 6.1 使用 skill 生成一个测试 HTML 文件（含 mermaid 图和图片）
- [x] 6.2 验证 doc 模式：自由滚动正常
- [x] 6.3 验证 PPT_FULL 模式：方向键/空格翻页正常，Enter 切换正常
- [x] 6.4 验证 PPT_ZOOM 模式：图片/mermaid 放大显示，方向键滚动，Esc 返回
- [x] 6.5 验证焦点管理：多图水平排列时左右键切换焦点，边框高亮
- [x] 6.6 验证边界穿透：zoom 模式下滚到顶部再按上键 → 翻页到上一个 slide

## 7. Bugfix: 焦点切换 + no-focus 支持

- [x] 7.1 ArrowLeft/ArrowRight 添加 `e.preventDefault()` 防止浏览器默认行为
- [x] 7.2 `handleFocusSwitch` 过滤 `.no-focus` 元素，只在可聚焦元素间切换
- [x] 7.3 `updateFocus` 过滤 `.no-focus` 元素
- [x] 7.4 CSS 添加 `.no-focus` 样式（半透明 + 禁止光标）

## 8. Doc 模式滚动体验优化

- [x] 8.1 CSS: doc 模式下 `.slide` 的 `min-height: auto`、`padding: 32px 40px`、无 border
- [x] 8.2 CSS: PPT 模式下恢复 `min-height: 100vh`、`padding: 60px 80px`、有 border
- [x] 8.3 更新 SKILL.md 中的 CSS 模板

## 9. 测试 HTML 改进

- [x] 9.1 测试 slide 改为 3 图水平排列（A 可聚焦、B 不可聚焦、C 可聚焦）
- [x] 9.2 验证焦点切换跳过中间的 B 图

## 10. Bugfix: 焦点索引重置 + 方向键逻辑

- [x] 10.1 `handleFocusSwitch` 中 `clearFocus()` 重置索引为 -1 → 改为先更新索引再清除
- [x] 10.2 方向键逻辑反转 → 改用 `Math.min/max` 替代模运算
- [x] 10.3 `exitZoomMode` 不滚动回原 slide → 添加 `scrollIntoView`
- [x] 10.4 同步修复所有测试文件和 SKILL.md

## 11. 模式切换瞬时定位 + DOC/PPT 对应关系

- [x] 11.1 SKILL.md: `enterPPTMode` 选 slide 逻辑改为视口中心最近（`slideCenter - viewportCenter`），`behavior: 'instant'`
- [x] 11.2 SKILL.md: `enterDocMode` 添加垂直居中对齐（`slideCenter - viewportCenter / 2`），`behavior: 'instant'`
- [x] 11.3 SKILL.md: `navigateSlide` `behavior: 'smooth'` → `'instant'`
- [x] 11.4 更新 5 个测试 HTML 文件同步上述改动
- [x] 11.5 更新 spec.md: DOC→PPT 中心吸附 + PPT→DOC 居中 + 全部 instant
- [x] 11.6 Playwright 测试通过 30/30
