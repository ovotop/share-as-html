# PPT Overflow Scroll — 修复与测试上下文

## 概述

**Change**: `openspec/changes/ppt-overflow-scroll/` (spec-driven, all artifacts complete)

**问题**: PPT 模式下，大 Mermaid 图 / 宽图片超出视口时，ArrowDown/ArrowRight 直接跳到下一页/切焦点，无法滚动查看内容。

**方案**: 三管齐下：
- CSS: `scroll-snap-type: y mandatory` → `y proximity` + `overflow-x: auto`
- JS: ArrowDown/Up 优先纵向滚动内容，到底后 bounce 反馈，二次按下才翻页
- JS: ArrowLeft/Right 优先横向滚动内容，到底后 bounce 反馈，二次按下才切焦点

## 已完成

### SKILL.md 模板 (`~/.opencode/skills/sharing-in-html/SKILL.md`)
- `scroll-snap-type: y mandatory` → `y proximity`
- 新增 `overflow-x: auto`（允许横向滚动）
- 新增 4 个 `@keyframes` (slide-bounce-down/up/left/right) + 4 个 bounce 类
- 新增 `let isAtScrollBoundary = false` 状态变量
- 重写 PPT_FULL 键盘处理器：ArrowDown/Up/Left/Right 全部支持 scroll-then-advance 逻辑
- 新增 4 个辅助函数：`canScrollVertically`, `canScrollHorizontally`, `scrollSlideContent`, `triggerBounce`
- `exitZoomMode` 改为 `window.scrollTo({ top: targetTop })` 替代 `scrollIntoView`

### 5 个 HTML 文件全部更新
- `test-mermaid-zoom.html` ✅
- `test-image-zoom.html` ✅
- `test-focus-matrix.html` ✅
- `ai-agent-tools.html` ✅
- `sharing-doc-test.html` ✅

### 测试 (test-automated.spec.js)
- 新增 9 个测试用例（ArrowDown 滚动、bounce+二次翻页、ArrowRight 横向滚动、focus 切换、flag 重置等）
- **最后已知结果: 62/65 通过，3 失败**（详见下方）

## 待修复：3 个测试失败

### 1. test-image-zoom.html: ArrowRight horizontal scroll (test line ~412)
```
Error: goToSlide or undefined reference
```
可能原因：test-image-zoom.html 的 JS 仍然有残留语法错误。需检查 `<script>` 块中 exitZoomMode 附近。

### 2. test-image-zoom.html: ArrowLeft horizontal scroll (test line ~553)
同上。

### 3. test-mermaid-zoom.html: PPT_FULL Navigation Last Index (test line ~93)
已修复测试逻辑（adapt for new scroll-before-advance behavior），但上次运行被用户 aborted，需重新跑验证。

### 待手动验证 (tasks 8.1-8.5)
- [ ] 打开 `test-mermaid-zoom.html` → Enter PPT → 大 mermaid slide → ArrowDown 平滑滚动
- [ ] Bounce 动画在滚动到底部时触发
- [ ] 第二次 ArrowDown 翻到下一页
- [ ] 普通 slide 直接翻页（行为不变）
- [ ] ArrowUp 对称行为

## 已知问题与设计决策

### 1. exitZoomMode 已修复
- **旧**: `slides[currentSlideIndex].scrollIntoView({ behavior: 'instant' })`
- **新**: `window.scrollTo({ top: targetTop, behavior: 'instant' })`
- **原因**: context.md Bug #11/#12 要求 scrollTo 替代 scrollIntoView

### 2. overflow-x: auto（非 hidden）
- 初版错误使用了 `overflow-x: hidden`，会阻止横向滚动功能
- 已修复为 `overflow-x: auto`

### 3. 80% viewport 滚动步长
- `scrollSlideContent` 每次滚动 80% 视口尺寸
- 临时设置 `scroll-snap-type: none`，500ms 后恢复 `y proximity`

### 4. isAtScrollBoundary flag
- ArrowDown 到达底部 → set flag + bounce → 不下翻
- 再次 ArrowDown → 翻页 + reset flag
- ArrowUp 滚动时先 reset flag（离开边界）

### 5. 测试中 window.isAtScrollBoundary 暴露问题
- `ai-agent-tools.html` 有 `Object.defineProperty` getter 暴露，但无 setter
- 其他 4 个文件未暴露
- 重写了 Boundary flag 测试改用 scroll + code-path 方式触发，避免依赖 window 属性

## 关键文件位置

| 文件 | 路径 |
|------|------|
| Skill 模板 | `~/.opencode/skills/sharing-in-html/SKILL.md` |
| OpenSpec change | `openspec/changes/ppt-overflow-scroll/` |
| 测试文件 | `test-automated.spec.js` |
| 上下文文档 | `docs/context.md` (原始) |
| 本次上下文 | `docs/fix-and-testing-context.md` (本文件) |

## 下一步操作

1. `npx playwright test test-automated.spec.js --reporter=line` 运行测试
2. 修复 3 个失败的测试
3. 手动验证 tasks 8.1-8.5
4. 完成后运行 `/opsx-archive` 归档 change
