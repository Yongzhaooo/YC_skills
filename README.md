# YC Skills

一套面向个人 Codex 开发的轻量工作流技能：先获得事实和决策，再以最小风险实施并用证据交付。它们是可独立取用的工具，不是每个任务都必须经过的流水线。

## 工作流

```text
陌生或多文件代码库 ──> $repo-map
                         │
方案仍有关键未知 ────────> $grilling ──> $run-pilot（仅在可行性未证实时）
                         │
恢复跨任务上下文 ─────────> $wayfinder
方向已确定 ─────────────> $plan-work ──> 实施（必要时 $delegation-policy） ──> 项目自身的测试流程
```

## Skills

| Skill | 何时使用 | 简单用法 |
| --- | --- | --- |
| `repo-map` | 陌生、多文件或架构敏感的改动，需要先找入口、调用链和测试面。 | `$repo-map 找出支付回调从 HTTP 入口到订单状态更新的路径，并给出可修改边界。` |
| `grilling` | 方案、边界或取舍尚未说清，希望以成批问题发现隐含假设。 | `$grilling 我想给 CLI 加离线缓存，帮我把决策和约束问清楚。` |
| `run-pilot` | 在投入完整设计前，先做一个可回滚的小试验验证关键假设。 | `$run-pilot 用冻结的样本验证新的解析器能否达到准确率目标，不改生产入口。` |
| `plan-work` | 方向已确定，需要写设计说明并拆成可验证的纵向工作项。 | `$plan-work 根据已确认的导入流程，写 spec 并拆成实施计划。` |
| `delegation-policy` | 需要派发子任务，或需要判断主线程和子代理各自应负责什么。 | `$delegation-policy 把这项迁移拆成可并行的调研、实现和验证任务，并定义回传证据。` |
| `wayfinder` | 跨 session 恢复一个长期项目，需要知道正在做什么、卡在哪里、从哪里安全继续。 | `$wayfinder 阅读项目的 wayfinder，告诉我当前主线、阻塞和最安全的下一入口。` |

## 使用原则

- 小而明确的任务直接完成，不为流程而流程化。
- `grilling` 只澄清决策；`run-pilot` 只给出试验证据；`plan-work` 只产出计划。阶段之间不自动推进。
- 可行性未知时优先 `run-pilot`；方向已定时直接 `plan-work`。
- 并行工作前先用 `delegation-policy` 划分写入边界和验收证据；验证遵循项目自身的测试约定。

## 安装

将需要的 skill 目录复制到 Codex 的本地 skills 目录。不同 Codex 版本的目录和安装方式可能不同，请以当前运行时的说明为准；安装后可通过 `$skill-name` 显式调用，也可让支持技能路由的运行时按任务匹配。

## 来源与归属

本仓库以 MIT License 发布。`grilling`、`run-pilot` 与 `plan-work` 源自个人工作流的持续演进，其中 `grilling` 和 `plan-work` 最初参考了 [mattpocock/skills](https://github.com/mattpocock/skills) 的 MIT 许可内容；其余技能为面向当前 Codex 工作方式的个人整理。
