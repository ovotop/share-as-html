## 1. Arrow 键锁定 zoom（Decision 5 实现）

- [x] 1.1 `PPT_ZOOM` case: ArrowUp/Down 只调用 `scrollZoomContainer()`，去掉 `exitZoomMode()` + `navigateSlide()` 分支
- [x] 1.2 `scrollZoomContainer()`: ArrowLeft/Right 补充边界检测（当前硬编码 `return true`）
- [x] 1.3 碰边界时播放 bounce 动画（复用 `@keyframes slide-bounce-*`，target 改为 `.zoom-container`）

## 2. 动态统一 scale line（Decision 1, 3, 6 实现）

- [x] 2.1 `enterZoomMode()`: 读取 clone 内容自然尺寸 → 计算 `fillX` → 构建动态 scale line（去重）
- [x] 2.2 状态变量改为：`zoomScale`（当前 scale 值）、`scaleLine`（当前元素的动态 scale 数组）、`fillStepScale`（fill 阈值）
- [x] 2.3 `applyZoomScale()`: fill class 由 `zoomScale >= fillStepScale` 自动 derive，不再用独立 `zoomFitMode` 变量手动 toggle
- [x] 2.4 `+` / `-` handler: 沿 `scaleLine` 步进（非静态 `ZOOM_SCALE_STEPS`）

## 3. Enter 快速切换（Decision 7 实现）

- [x] 3.1 `PPT_ZOOM` case Enter: 改为 fit(1.0) ↔ fillStep 二元跳转（而非 toggle class）
- [x] 3.2 到达 fillStep 时 `.fill` class 由 `applyZoomScale()` 自动应用

## 4. 布局时序处理（fillX 计算时机）

- [x] 4.1 `enterZoomMode()`: append clone 后 `requestAnimationFrame` 等待 layout 再读 `getBoundingClientRect()`
- [x] 4.2 若 `requestAnimationFrame` 尺寸仍为 0（fallback 场景），用原始元素尺寸

## 5. CSS 变更

- [x] 5.1 `body.mode-zoom .zoom-container`: 添加 bounce keyframe 动画 class
- [x] 5.2 验证现有 `body.mode-zoom .zoom-content` / `.zoom-content.fill` 规则无需变更（design.md Decision 4 已定义）

## 6. 测试更新

- [x] 6.1 新增：ArrowUp/Down 碰边界 → 不退出 zoom（仍为 `mode-zoom`）
- [x] 6.2 新增：ArrowLeft/Right 碰边界 → 停止滚动，不退出 zoom
- [x] 6.3 新增：`+` / `-` 缩放步进（验证 scale 值变化序列）
- [x] 6.4 新增：Enter 跳 fit ↔ fillStep（验证 scale 改变 + fill class 自动应用）
- [x] 6.5 新增：多次 zoom in/out 后 `enterZoomMode()` 重置到 1.0x fit
- [x] 6.6 保留现有：「Enter zoom → Esc → 状态恢复」「Exit zoom scrolls to correct position」

## 7. 重新生成并验证

- [x] 7.1 运行 `python md2html.py example-talk/` 重新生成 fixture HTML
- [x] 7.2 同步 fixture HTML 到 test harness 目录
- [x] 7.3 全量 zoom 测试 20/20 通过，现有测试无回归
