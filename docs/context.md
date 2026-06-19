# Sharing-in-HTML Skill 开发上下文

## 项目状态

**Change**: `sharing-html-skill` (OpenSpec)
**Skill**: `sharing-in-html` @ `~/.opencode/skills/sharing-in-html/SKILL.md`
**进度**: 所有已知问题已修复，待 Playwright 自动化测试

## 核心功能

三状态状态机：
```
DOC ──Enter──→ PPT_FULL ──Enter(diagram focused)──→ PPT_ZOOM
  ↑                ↑                                    │
  └──Esc───────────└────────────────Esc────────────────┘
```

- **Doc 模式**: 自由滚动，`min-height: auto`，无分割线
- **PPT 模式**: 整屏翻页，`scroll-snap`，`min-height: 100vh`
- **Zoom 模式**: 图片/mermaid 全屏显示，容器 `overflow: auto` 支持滚动

## 所有修复的 Bug（按时间顺序）

### 第一批：交互基础问题
1. ArrowLeft/ArrowRight 缺少 `e.preventDefault()` → 已修复
2. `handleFocusSwitch` 调用 `clearFocus()` 先重置索引为 -1，再计算索引导致错误 → 改为**先算索引再清除焦点**
3. `exitZoomMode` 不滚动回原 slide → 添加 `scrollTo({top, behavior:'instant'})`
4. 方向键逻辑反了 → 改用 `Math.min/max` 替代模运算（clamp 边界）

### 第二批：zoom-content CSS + 同步问题
5. `zoom-content` 的 `max-width/max-height` 限制导致 zoom 模式下无法滚图 → **所有文件统一移除**尺寸限制
6. `updateFocus()` 硬编码 `focusedDiagramIndex = 0` → 添加 `preserveIndex` 参数，退出 zoom 时传 `true`
7. `test-focus-matrix.html` PPT_ZOOM 缺少方向键处理 → 完整添加 Arrow 四向 handler
8. `test-focus-matrix.html` 焦点边框 3px → 统一为 2px

### 第三批：handleFocusSwitch 同步
9. `test-image-zoom.html` `handleFocusSwitch` 先 call `clearFocus()` 再计算索引 → 修复
10. `test-mermaid-zoom.html` 同样问题 → 修复
11. `test-image-zoom.html` `exitZoomMode` 仍用 `scrollIntoView` → 改为 `scrollTo(instant)`
12. `test-image-zoom.html` `exitZoomMode` 调 `updateFocus()` 未传 `true` → 修复

## 关键代码模式（所有文件统一）

```javascript
// handleFocusSwitch — 正确模式
function handleFocusSwitch(key) {
    // 1. 先算新索引
    let newIndex;
    if (key === 'ArrowRight') {
        newIndex = Math.min(focusedDiagramIndex + 1, focusables.length - 1);
    } else {
        newIndex = Math.max(focusedDiagramIndex - 1, 0);
    }
    // 2. 更新全局变量
    focusedDiagramIndex = newIndex;
    // 3. 再清除旧焦点
    document.querySelectorAll('.diagram-focusable.focused').forEach(el => el.classList.remove('focused'));
    // 4. 最后应用新焦点
    focusables[focusedDiagramIndex].classList.add('focused');
}

// exitZoomMode — 正确模式
function exitZoomMode() {
    currentState = 'PPT_FULL';
    document.body.className = 'mode-ppt';
    // ... remove zoom container ...
    const slides = document.querySelectorAll('.slide');
    if (slides[currentSlideIndex]) {
        const targetTop = slides[currentSlideIndex].offsetTop;
        window.scrollTo({ top: targetTop, behavior: 'instant' });
    }
    updateFocus(true);  // preserveIndex = true
}

// updateFocus — 正确模式
function updateFocus(preserveIndex = false) {
    // ... find focusables ...
    if (!preserveIndex || focusedDiagramIndex < 0 || focusedDiagramIndex >= focusables.length) {
        focusedDiagramIndex = 0;  // 只在这三种情况下重置
    }
    // ... apply focus ...
}
```

## CSS 关键规则

```css
/* zoom-content — 无尺寸限制，让容器 overflow:auto 处理滚动 */
body.mode-zoom .zoom-content {
    /* No size restrictions — let container scroll */
}

/* 焦点状态 */
.diagram-focusable.focused { border-color: var(--accent); border-width: 2px; }

/* No-focus */
.diagram-focusable.no-focus { opacity: 0.5; cursor: default; }
```

## 测试文件

| 文件 | 用途 | 修复状态 |
|------|------|----------|
| `ai-agent-tools.html` | 主测试（mermaid + 3图焦点） | ✅ 通过 Oracle review |
| `sharing-doc-test.html` | 完整功能测试 | ✅ 通过 Oracle review |
| `test-focus-matrix.html` | 6种焦点场景 + debug面板 | ✅ 刚修复 PPT_ZOOM handler |
| `test-mermaid-zoom.html` | mermaid zoom | ✅ 刚修复 handleFocusSwitch |
| `test-image-zoom.html` | 图片 zoom | ✅ 刚修复 3 个问题 |

## 下一步：自动化测试

**问题**：Oracle review 只能检查代码逻辑，测不了运行时行为。手动测试效率低。

**计划**：用 Playwright 写自动化测试，覆盖：
1. 状态转换 (DOC→PPT→ZOOM→PPT→DOC)
2. PPT_FULL 导航（上下翻页、边界）
3. 焦点切换（多图、no-focus 过滤、单图无激活）
4. Zoom 模式（方向键滚动、边界穿透、Esc 退出）
5. 退出 zoom 后焦点保留

**方法**：加载 skill `playwright`，派 agent 写测试脚本到 `test-automated.spec.js`，运行验证。

## 文件位置

- Skill: `~/.opencode/skills/sharing-in-html/SKILL.md`
- OpenSpec: `openspec/changes/sharing-html-skill/`
- 测试: `/home/mi/Documents/harness/tooling/documenting/sharing-in-html/`
- 上下文: `docs/context.md`
