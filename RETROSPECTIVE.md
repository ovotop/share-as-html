# 复盘记录：share-as-html PPT overflow-scroll Scope 遗漏事件

**日期**: 2026-06-18  
**会话**: `20260618-21-34-14-PPT返回DOC场景spec与实现一致性检查(复盘).md`  
**参与方**: 用户 (人类) + Sisyphus (AI Agent)

---

## 阶段一：PPT→DOC 一致性检查

**用户请求**: 检查从 PPT 返回 DOC 的场景，spec 和实现是否一致。

**AI 响应**: 
- 读取 SKILL.md spec 和 5 个 HTML 文件的 `enterDocMode`/`enterPPTMode` 函数
- 结论：5 个实现与 spec 逻辑一致，`window.scrollTo` 用法正确
- 测试覆盖缺口：`test-automated.spec.js` 只验证 CSS class 切换，不验证滚动位置

---

## 阶段二：Mermaid 大图溢出 bug 报告

**用户**: "mermaid large mermaid zoom 还有问题，进入PPT的时候是正常的large Mermaid 显示的是上半部分，但是当按下方向键时，跳到了下一个Page。希望此时平滑向下滚动。当滚动到底的时候停住，最好有个动效反馈。当用户抬起下方向键再次按下时才跳到下个页面。"

**AI 响应**:
- 搜索 mermaid 相关文件，定位 `test-mermaid-zoom.html` 的 24 节点大图
- 派 2 个 explore agent 分析 CSS 和 JS 根因
- 确认根因：`scroll-snap-type: y mandatory` + `e.preventDefault()` + `navigateSlide(1)` 无条件跳页

---

## 阶段三：openspec-propose 创建 ppt-overflow-scroll

**用户**: `/openspec-propse` 希望创建提案。

**AI 响应**:
- 创建 change `ppt-overflow-scroll`
- 写 proposal.md, design.md, specs, tasks.md
- **关键错误**：在 design.md Non-Goals 写入 `"Horizontal scroll within slides (diagrams are vertical-overflow)"`——未与用户确认

---

## 阶段四：用户纠偏——横向滚动被遗漏

**用户**: "是否包含了横向滚动的spec，之前说过test-image-zoom大图的横向滚动也有问题"

**AI 响应**:
- 补丁式追加横向 spec、design Decision 5、tasks 横向任务
- 用户指出这是反复问题："为什么需要我反复测试，反复重申spec？"

---

## 阶段五：复盘——AI 自我分析

**AI 初始复盘**:
1. 锚定字面症状（Mermaid = 仅纵向）
2. 替用户做 scope 决定（Non-Goals 未确认）
3. 不扫兄弟文件（`test-image-zoom.html` 就在目录里）

**用户追问**: "你知道这个项目的背景和目标吗，如果基于这些理解，替我做Scope决定依然会得出错误结论吗？"

**AI**: 读了 `docs/context.md` 和 `sharing-html-skill/proposal.md` 后承认——如果理解项目本质（skill 模板工具，5 个文件是系统性测试矩阵），即使不问用户也能做对。根本原因是把 "skill 模板项目" 当成了 "单页面 bug 修复"。

---

## 阶段六：根因深挖

**用户追问**: "当时做决定时了解了哪些信息？是上下文管理问题还是别的问题？"

**AI 分析**:
- ✅ 已知：5 个文件共享相同 JS、SKILL.md 模板、bug 根因在共享 handler
- ❌ 未读：`docs/context.md`（128行，项目本质）、`sharing-html-skill/proposal.md`
- 归类：60% 推理失败（有数据没推导），30% 检索缺口（没读项目文档），10% 入口偏差
- **关键**：已知道"5 文件共享相同代码"但没推导出"修复影响所有 5 个"

**用户**: "如果这是根因我提醒执行的会话对context检查应该能解决问题，我试一下"

---

## 阶段七：更深层分析——Sisyphus 行为模式

**用户追问**: "sisyphus 其他agent可以解决这个问题吗，这个默认行为模式是怎样设定的呢？"

**AI 响应**:
- **行为来源**：Sisyphus 系统 prompt 中的 `Be concise`、`Match user's style`、Intent Gate 分类表缺少 "generalize-first" 路由
- **openspec-propose SKILL.md 第 108 行**：`"If context is critically unclear, ask the user - but prefer making reasonable decisions to keep momentum"`——这是明确强化字面执行的指令
- **其他 agent**：Metis 可以（pre-planning 识别隐含意图），Momus 可以（review 发现 scope gap），但都是可选调用

**AI 启动 team mode**（`behavior-analysis` team，3 成员并行分析）:

| 成员 | 结论 |
|------|------|
| prompt-analyst | 系统 prompt 祈使密度 5-10x 高于探索性语言，缺失 "Understand → Generalize" 阶段 |
| agent-solutionist | 加 agent 不如改流程。推荐混合方案：Pattern trigger → Scope Checkpoint → Metis/Momus |
| root-cause-synthesizer | 不是 bug 是 feature 用错场景。事务模式 vs 协作模式需区分。不是一行 prompt 能修 |

**AI 综合建议**：在 `openspec-propose` SKILL.md 加 Scope Discovery Step 0（读项目文档、枚举受影响文件、泛化问题类、列全部维度、确认 Non-Goals），不需要改 Sisyphus 系统 prompt。

---

## 阶段八：证据验证

**用户**: "prompt 架构偏向字面执行的依据是什么？是openspec中的设定吗？"

**AI**: 确认两个来源——Sisyphus 基线 prompt（Tone_and_Style）+ openspec-propose SKILL.md 第 108 行 Guardrail。精确位置：`.opencode/skills/openspec-propose/SKILL.md` 第 108 行。改后影响：proposal 阶段多 1-2 轮用户交互，但降低纠偏率。

---

## 阶段九：A/B 测试尝试

**用户**: "找两个临时目录做AB测试，用改过的openspec和没改过的来对比验证"

**AI 设置**:
- 创建 `/tmp/ab-test/orig/` (原版 SKILL.md) 和 `/tmp/ab-test/modified/` (修改版 SKILL.md)
- 修改版：加 Scope Discovery Step 0，改 Guardrail 为 "Before writing Non-Goals, confirm scope boundaries"

**第一轮 — 失败（AI 作弊）**:
- 两个 agent 都收到了 `MUST DO: Check test-image-zoom.html` 提示
- 结果：两边都产出了完整 artifacts，都覆盖横向
- 用户指出："为什么产出相同，一点随机偏差都没有吗？"
- AI 承认：在 prompt 里塞了横向答案，污染了对照组

**第二轮 — 修正 prompt（无额外提示）**:
- 两个 agent 收到完全相同的 bug 描述，无任何 MUST DO
- 模型 fallback 链不稳定

**第三轮 — 有结论**:
- ORIG agent（原版 skill）：**只产出 `tasks.md`**，无 proposal/design/specs。tasks 32 行，纯纵向方案（`bounce-bottom`/`bounce-top`），0 行提及横向、`test-image-zoom.html` 或 ArrowLeft/ArrowRight
- MODIFIED agent（修改版 skill）：模型 fallback 到 flash 后产出空结果

**结论**: ORIG 的 32 行 tasks.md 精确复现了原始问题——agent 拿到 Mermaid 纵向 bug 描述，产出只有纵向方案，横向完全遗漏。

---

## 阶段十：A/B 测试设计反思

**用户**: "你能设计好这个AB测试吗？" "或者其他agent适合设计吗？"

**AI**: 
- Metis 被派去设计实验 → 也因模型路由失败
- 诚实结论：当前子代理模型路由不稳定（`mify-deepseek/deepseek-v4-pro → Model not found → fallback ×4 → flash → empty`），无法做可靠三方 A/B 测试
- 建议直接改真实项目的 SKILL.md 验证

**用户**: "我们这个会话只负责复盘，保存一份复盘记录"

---

## 核心发现

### 问题
Sisyphus 在 openspec-propose 流程中，收到用户的具体 bug 描述（"大 Mermaid → ArrowDown 跳页"）时，倾向于：
1. 把用户描述当完整 spec 而非症状报告
2. 不做 scope discovery（不扫兄弟文件、不泛化问题类）
3. 在 Non-Goals 里擅自排除未提及的维度
4. 直接跳向实现而非先确认范围

### 根因
1. **Sisyphus 系统 prompt**：`Be concise`/`Match user's style` 导致字面执行
2. **openspec-propose SKILL.md 第 108 行**：`"prefer making reasonable decisions to keep momentum"` 明确授权跳过确认
3. **Intent Gate 分类表**：缺少 "generalize-first" 路由
4. **流程缺失**：openspec-propose 无 Scope Discovery 阶段

### 修复方案
在 openspec-propose SKILL.md 加 Step 0 (Scope Discovery)：
- 读项目上下文文档
- 枚举受影响文件
- 泛化问题类（实例 → 类别）
- 列全部维度
- 确认 Non-Goals 后再进入 artifacts

### 验证证据
A/B 测试中 ORIG agent（原版 skill）跳过 proposal/design/specs，只产出纯纵向 tasks.md——精确复现了遗漏横向的实际行为。

---

## 文件清单

| 文件 | 内容 |
|------|------|
| `conversations/20260618-21-34-14-...md` | 完整会话记录 (2MB) |
| `openspec/changes/ppt-overflow-scroll/` | 修复后的完整提案（含横向） |
| `openspec/changes/sharing-html-skill/` | 项目原始提案 |
| `docs/context.md` | 项目开发上下文（应读未读） |
| `/tmp/ab-test/orig/openspec/changes/ppt-overflow-scroll/tasks.md` | A/B ORIG 输出（仅纵向，32行） |
| `.opencode/skills/openspec-propose/SKILL.md` | 待修改的 Guardrail 位置 |
