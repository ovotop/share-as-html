## Context

当前 share-as-html 的 CSS 模板在 `md2html.py` 的 `CSS_TEMPLATE` 常量中定义（约 470 行）。屏幕适配主要依赖一个 `@media (max-width: 768px)` 断点。问题：大屏幕内容未居中、固定字号不适应极端分辨率、小屏只缩放了部分元素。

## Goals / Non-Goals

**Goals:**
- 大屏幕（≥1200px）：内容水平居中，字号比例协调
- 中屏幕（768-1200px）：当前效果基本保持
- 小屏幕（≤768px）：所有文字等比缩小，卡片和代码块合理适配
- PPT 模式：内容可更宽（投影场景不需要留白）
- 零断点字体缩放：用 `clamp()` 替代多个 `@media` 字体覆盖

**Non-Goals:**
- 不改变现有 JS 状态机逻辑
- 不改变 HTML 结构
- 不新增 CSS 框架或依赖

## Decisions

### 1. 用 `clamp()` 实现流体字体

```css
h2  { font-size: clamp(24px, 4vw, 36px); }
h3  { font-size: clamp(17px, 2.5vw, 22px); }
p, li { font-size: clamp(14px, 1.5vw, 16px); }
.cover h1 { font-size: clamp(32px, 5vw, 48px); }
.card h4 { font-size: clamp(14px, 1.5vw, 16px); }
```

`clamp(MIN, PREFERRED, MAX)` 在三个区间工作：
- 小屏（≤ MIN/vw 对应宽度）：固定在 MIN，不继续缩小
- 中屏：随视口宽度线性缩放
- 大屏（≥ MAX/vw 对应宽度）：固定在 MAX，不继续放大

**替代方案**：多断点 `@media` 覆盖。

**为什么不选**：`clamp()` 一条规则覆盖所有尺寸，不需要为每个字号写 3+ 个断点。浏览器支持率 >97%。

### 2. `.slide` 添加 `align-items: center` 居中

```css
.slide { align-items: center; }
```

结合已有的 `max-width: 900px` on `.content`，大屏上内容自然居中。

**替代方案**：`margin: 0 auto` on `.content`。

**为什么不选**：`.slide` 已经是 `display: flex` 容器，`align-items` 更直接，不需要覆盖 `.content` 的 `width: 100%`。

### 3. PPT 模式放宽 content 宽度

```css
body.mode-ppt .slide .content { max-width: 1100px; }
```

投影场景观众距离远，内容可以更大更宽。DOC 模式保持 900px 适合阅读。

### 4. 简化 @media 断点，仅保留结构性调整

```css
@media (max-width: 768px) {
    .slide { padding: 24px 16px; }
    body.mode-ppt .slide { padding: 40px 20px; }
    /* grid collapse — keep */
    .grid-2, .grid-3, .grid-4, .split-layout { grid-template-columns: 1fr; }
    .flex-row { flex-direction: column; }
    /* 移除所有 font-size 覆盖 — clamp() 已经处理 */
}
```

### 5. 两个文件同步更新

- `md2html.py` 的 `CSS_TEMPLATE` 常量
- `skills/share-as-html/SKILL.md` 的 CSS 模板代码块
- 同步到 `.opencode/skills/share-as-html/SKILL.md`

## Risks / Trade-offs

- **`clamp()` 在极老浏览器不支持**：IE 全系不支持，但 share-as-html 目标用户使用现代浏览器。
- **PPT 模式 1100px 在 1024px 笔记本上可能溢出**：`max-width: 1100px` + `width: 100%` 保证不溢出，只是在 1024px 屏上退化为全宽。
- **vw 单位在移动端受地址栏显隐影响**：`clamp()` 的 MIN 值兜底，不会出现极端小字号。
