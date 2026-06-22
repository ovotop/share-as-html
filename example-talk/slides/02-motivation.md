---
slide: 2
duration: 5min
emoji: 🤔
layout:
  grid:
    - [{card: "传统痛点"}, {card: "CLI 的价值"}]
    - [{callout: "info"}]
---

## 为什么 Android 需要 CLI？

- Android Studio 启动慢、吃内存
- CI/CD 流程依赖 IDE 不现实
- AI Agent 需要轻量交互入口
- 跨平台脚本化操作困难

=== slot ===

- 单一入口，统一管理所有 Android 操作
- 可脚本化、可组合、可自动化
- 为 AI Agent 提供标准化工具接口
- 轻量、快速、无 GUI 依赖

=== slot ===

**思考**: 如果 AI Agent 想操作 Android 设备，需要怎样的接口？

<!-- reader -->
在 Android 开发生态中，命令行工具长期处于次要地位。
大多数开发者习惯通过 Android Studio 完成编译、调试、
部署的全流程。但在以下场景中，GUI IDE 不再是合适的
选择：

- **CI/CD 流水线**: Jenkins、GitHub Actions 等环境没有 GUI
- **自动化测试**: 需要脚本驱动设备操作
- **AI Agent 集成**: AI 无法打开 Android Studio

Android Studio 启动缓慢（通常 30 秒以上）、内存占用高
（超过 2GB），在无头环境中完全无法运行。而 CLI 工具
天然支持脚本化——你可以用几行 shell 完成构建、测试、
部署的全流程。

通过对比可以看到，CLI 方案在启动速度、内存占用、
脚本化能力、CI/CD 适配等每一项指标上都碾压 IDE 方案。
对于自动化场景，差异尤其明显。
<!-- /reader -->
