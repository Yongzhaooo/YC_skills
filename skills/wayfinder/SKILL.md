---
name: wayfinder
description: Use at the start of a multi-session project or when resuming work to read docs/wayfinder.md and report the live work, blockers, and safest next entrance without starting execution.
---

# Wayfinder

`docs/wayfinder.md` 是一个长期项目的短地图，不是任务看板、变更日志或完整设计文档。它回答三件事：当前正在推进什么、卡在什么条件上、下一次从哪里安全进入。

开始时：

1. 读取 `docs/wayfinder.md`；若不存在，说明缺少恢复入口，不要凭历史对话臆造项目状态。
2. 对照当前工作区、相关文档和 git 状态，检查地图是否与现实冲突。
3. 用两到四行报告：当前主线、阻塞条件、最安全的下一入口；地图过期时指出具体条目并提出修正建议。
4. 停在定位阶段，等待用户选择要继续的方向。不要因读取地图而自动开始实现。

保持地图短小、结论优先。只有阶段、阻塞或安全入口发生实质变化时才更新；细节应链接到设计文档、计划或证据所在位置。
