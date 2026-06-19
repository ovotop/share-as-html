# Android CLI 技术分享 — 上下文文档

## 目标

制作一份关于 Android CLI 的技术分享 HTML 演示文档。

## 素材来源

所有原始笔记位于：`/home/mi/Documents/box/3-项目/05-android-cli/`

### 核心素材文件

| 文件 | 内容 | 用途 |
|------|------|------|
| `android-cli-skill-summary.md` | CLI 功能总结，核心命令一览 | 全景页、命令速览 |
| `android-cmd.md` | 完整命令参考（531 行） | 所有命令细节 |
| `android-docs-kb-structure.md` | 知识库系统架构深度分析（365 行） | ⭐ 核心内容：Lucene 索引、双文件模型、搜索流程 |
| `android-docs-using.md` | docs search/fetch 使用记录 | 知识库 demo 素材 |
| `sharing-android-layout-diff.md` | Layout Diff UI 监控方案 | 实战案例：mibrowser 重构 |
| `Lucene-可扩展的信息检索引擎库.md` | Lucene 简介 | 背景知识 |
| `使用记录.md` | 安装、skills 管理实操 | 快速开始、Skills 章节 |

### 图片素材

- `Pasted image 20260525201028.png` — 项目初始化截图
- `Pasted image 20260601105756.png` — docs search 截图
- `lucene_logo_green_300.png` — Lucene logo

## 当前进展

### 已完成

- [x] 内容大纲（6 部分，20-30 分钟分享）
- [x] HTML 演示文档初版（`sharing-preview.html`，13 页幻灯片）

### 待完成

- [ ] 根据实际分享时长调整内容深度
- [ ] 插入截图素材（Pasted image 文件）
- [ ] 补充 live demo 环节脚本
- [ ] 可能需要增加"为什么用 Lucene 而不是向量检索"的对比页

## HTML 设计规范

### 技术栈

- 纯 HTML + CSS，无 JS 依赖
- 深色主题（`#0f172a` 背景）
- 系统字体栈：`-apple-system, SF Pro Display, PingFang SC, Noto Sans SC`
- 代码字体：`SF Mono, Fira Code, Cascadia Code`

### 配色方案

```css
--bg: #0f172a        /* 主背景 */
--surface: #1e293b   /* 卡片/代码块背景 */
--surface2: #334155  /* 边框、分割线 */
--accent: #38bdf8    /* 主强调色（蓝） */
--accent2: #818cf8   /* 副强调色（紫） */
--green: #4ade80     /* 成功/命令 */
--yellow: #fbbf24    /* 高亮/关键数字 */
--orange: #fb923c    /* 警告/标签 */
--text: #e2e8f0      /* 主文字 */
--text-dim: #94a3b8  /* 次要文字 */
```

### 幻灯片结构

```
<div class="slide">
    <span class="slide-number">N</span>
    <div class="content">
        <h2><span class="emoji">X</span> 标题</h2>
        内容...
    </div>
</div>
```

### 复用组件

- `.grid-2` — 两列网格布局
- `.card` — 内容卡片（带标题和描述）
- `.point` / `.point.highlight` / `.point.star` — 要点条目
- `.metric` / `.metrics-row` — 关键数字展示
- `.diagram` — ASCII 架构图
- `.tag` / `.tag-blue` 等 — 标签
- `pre > code` — 代码块（带 `.cmd` `.comment` `.string` `.keyword` 语法高亮）
- `.flow` / `.flow-item` — 编号流程列表
- `table` — 数据表格

## 分享大纲

### 一、开场（3min）
- 背景：Google 2026 IO 推出 Android CLI 三件套
- 痛点：IDE 重、AI Agent 需要轻量交互入口

### 二、Android CLI 全景（5min）
- 核心命令速览
- 完整工作流 demo
- 重点：`android layout`

### 三、知识库系统深度拆解（10min）⭐
- 双文件模型：JSON + Markdown
- Lucene 索引机制
- kb:// URI 协议
- 关键数字：4882 文档 / 65MB / 0.38% 索引比

### 四、Layout Diff UI 监控（5min）
- baseline → diff → 报告
- mibrowser 重构实战

### 五、Skills 系统（5min）
- 领域知识包
- 多 Agent 支持

### 六、收尾（2min）
- 资源汇总
- Q&A
