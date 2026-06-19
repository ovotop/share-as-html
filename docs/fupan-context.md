# 复盘上下文 — 下一会话继续

## 前置阅读

- `RETROSPECTIVE.md` — 完整 10 阶段复盘记录
- `openspec/changes/ppt-overflow-scroll/` — 本次创建的提案（含横向补丁）
- `docs/context.md` — 项目本质（skill 模板，5 文件是测试矩阵）

## 核心结论（已知，不需要重分析）

1. **Sisyphus 在 openspec-propose 中的 "instance-level thinking"**：用户描述 `大 Mermaid 纵向溢出`，AI 产出只有纵向方案，横向遗漏。
2. **根因**：Sisyphus 系统 prompt 的 `Be concise`/`Match user's style` + openspec-propose SKILL.md 第 108 行 `"prefer making reasonable decisions to keep momentum"` 组合导致 scope 未确认就写 Non-Goals。
3. **修复方向**：在 openspec-propose SKILL.md 加 Step 0 (Scope Discovery)。
4. **修复影响**：proposal 阶段多 1-2 轮交互，但降低 scope 纠偏率。

## A/B 测试状态

### 已完成的测试

**第三轮**（prompt 完全一致，仅 SKILL.md 不同）：

| Agent | SKILL.md | 产出 |
|-------|----------|------|
| ORIG | 原版 (`keep momentum`) | 仅 `tasks.md`，32 行，**纯纵向**，无 ArrowLeft/Right，无 test-image-zoom.html |
| MODIFIED | 修改版 (Scope Discovery) | 模型 fallback 到 flash → 空 |

- ORIG 结果验证了假设——原版 skill 让 agent 跳过 proposal/design/specs，直奔纵向实现
- MODIFIED 空结果说明基础设施不稳定（model routing fault）

### A/B 测试目录（/tmp/ab-test/）

```
/tmp/ab-test/
├── orig/
│   ├── .opencode/skills/openspec-propose/SKILL.md   ← 原版
│   ├── docs/context.md
│   ├── test-mermaid-zoom.html
│   ├── test-image-zoom.html    (1500px 宽图)
│   ├── test-focus-matrix.html
│   ├── ai-agent-tools.html
│   ├── sharing-doc-test.html
│   └── openspec/changes/ppt-overflow-scroll/tasks.md  ← ORIG 产出
│
└── modified/
    ├── .opencode/skills/openspec-propose/SKILL.md   ← 修改版（Step 0 Scope Discovery）
    ├── docs/context.md
    ├── (同上 5 个 HTML)
    └── openspec/changes/  (空)
```

### 前两轮失败教训

1. **不要作弊**：prompt 里不要写 `MUST DO: Check test-image-zoom.html`——这等于告诉 agent 答案
2. **prompt 完全一致**：两个 agent 收到的任务描述必须一字不差
3. **等结果**：model routing 不稳定，可能空产出，等超时或所有 fallback 完成

---

## 下一会话 TODO

### TODO 1: 请合适的 agent 设计 A/B 测试方案

**需求**：
- 给定当前基础设施约束（model routing 不稳定，`mify-deepseek/deepseek-v4-pro` 经常 fallback）
- 设计能产出有效对比结果的 A/B 方案
- 变量仅一个：SKILL.md（原版 vs 修改版）
- 两个 agent prompt 必须完全相同

**可以尝试的 agent**：
- **Artistry**（非传统问题）：模型路由不稳定 → 不依赖三方 agent 的方案
- **Oracle**（架构/方法论）：设计实验方法论
- **Metis**（pre-planning）：分析失败原因给方案

**不接受**：
- 需要我控制模型路由的建议
- prompt 里塞答案的实验

### TODO 2: Sisyphus 按方案调度执行

拿到方案后，由 Sisyphus 负责：
- 清理 `/tmp/ab-test/orig/openspec/changes/` 和 `/tmp/ab-test/modified/openspec/changes/`
- 按方案派 agent
- 收集结果做对比

### 度量标准

对比两个 `proposal.md`：

| 检查项 | 打分 |
|--------|------|
| 是否提及 `test-image-zoom.html` | 有/无 |
| 是否提及横向滚动（ArrowLeft/Right） | 有/无 |
| Non-Goals 是否排除了横向 | 是/否 |
| Capability 是否只覆盖纵向 | 是/否 |
| 是否枚举了全部 5 个测试文件 | 有/无 |

---

## 关键文件路径

| 作用 | 路径 |
|------|------|
| 复盘记录 | `RETROSPECTIVE.md` |
| 项目上下文 | `docs/context.md` |
| 待修改 skill | `.opencode/skills/openspec-propose/SKILL.md` |
| 已修改 skill | `/tmp/ab-test/modified/.opencode/skills/openspec-propose/SKILL.md` |
| 原版 skill | `/tmp/ab-test/orig/.opencode/skills/openspec-propose/SKILL.md` |
| ORIG 产出 | `/tmp/ab-test/orig/openspec/changes/ppt-overflow-scroll/tasks.md` |
| 本文件 | `docs/fupan-context.md` |

## openspec-propose 修改点（已知）

原版第 108 行：
```
- If context is critically unclear, ask the user - but prefer making reasonable decisions to keep momentum
```

修改版替换为：
```
- Before writing Non-Goals in design.md, confirm scope boundaries with the user. Never silently encode scope-limiting decisions.
```

并在 Step 1 之前插入 Step 0 (Scope Discovery)：读项目文档、枚举受影响文件、泛化问题类、列全部维度、确认 scope。
