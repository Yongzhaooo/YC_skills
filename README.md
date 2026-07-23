# YC Skills — 个人 Codex 工作流

为 **Codex + GPT 5.6 sol subagent 模式** 调优的个人 skills。

## 适用场景

你有一个编程任务，不确定怎么做，或者做一半发现方向可能不对。这套工具帮你 **先想清楚，再动手**。

## 工作流

```
$grilling     →  明确边界 & 约束（高智能 agent；新项目建议先跟网页版 GPT 聊清楚）
    ↓
$run-pilot    →  快速验证一个概念是否可行（最小实现 + 证据）
    ↓
$to-spec      →  把已验证的方向固化为 spec 文档
    ↓
$to-tickets   →  把 spec 拆成可执行的 tracer-bullet tickets
    ↓
开 Thread 执行 →  主 agent（推荐 GPT 5.6 sol HIGH）指挥 sol MEDIUM 子代理逐个执行
```

## 安装

把这些 skill 文件夹复制到 Codex 的 skills 目录：

```powershell
# 从 YC_skills 仓库复制到 Codex runtime
Copy-Item -Recurse "C:\workarea\YC_skills\skills\*" "$env:USERPROFILE\.codex\skills\"
```

装完后在 Codex 里输入 `/grilling`、`/run-pilot`、`/to-spec`、`/to-tickets` 即可调用。

## 执行 Thread 的 Main Agent Prompt

当你完成 to-tickets 后，开一个新 Thread，选 **GPT 5.6 sol HIGH**，粘贴这个 prompt：

```
你是主 agent，负责指挥 subagent 执行以下 tickets。

规则：
1. 按照依赖顺序，选择 blocking edges 已完成的 ticket
2. 每个 ticket 派给一个 subagent（建议选 sol MEDIUM），给清楚 objective + completion evidence
3. 一个 ticket 完成后，验证结果，再派下一个
4. 不要自己实现——你是指挥官，不是执行者
5. 如果 ticket 的结果改变了后面的设计，暂停并报告

当前 tickets：[粘贴 to-tickets 输出]
```

## 重要提示

- **不要给 GPT 5.6 装太多 skills**。这些四个就够了。Superpowers 等重型 skill 套件会让 agent 注意力分散。
- **grilling 建议用高智能模型**。如果 Codex 当前模型不够聪明，把问题描述粘贴到网页版 GPT 聊完，拿着结论回来。
- **run-pilot 是可选步骤**。如果你对方向已经很有信心，可以跳过直接 to-spec。
- **这套工具是流程框架，不是代码生成器**。它们帮你做决策和规划，实际代码你自己写（或让 subagent 写）。

## 四个 Skill 简介

| Skill | 触发 | 做什么 |
|-------|------|--------|
| `/grilling` | `/grilling` | 用设计树方式反复追问你，直到边界清晰 |
| `/run-pilot` | `/run-pilot` | 最小实现验证一个假设，产出 PASS/WEAK/FAIL 证据 |
| `/to-spec` | `/to-spec` | 把讨论结果合成为结构化 spec 文档 |
| `/to-tickets` | `/to-tickets` | 把 spec 拆成依赖有序的 tracer-bullet tickets |

## 来源与归属

这四个 skill 是个人 fork，基于以下上游开源项目修改而来：

| Skill | 上游来源 | License | 修改内容 |
|-------|----------|---------|----------|
| grilling | [superpowers](https://github.com/obra/superpowers) | MIT | 去掉了 handoff envelope、self-feedback 等系统基础设施，保留设计树核心 |
| to-spec | [mattpocock/skills](https://github.com/mattpocock/skills) | MIT | 去掉了 issue tracker 发布、跨仓库路由、Content Hash。简化为纯合成+本地文件 |
| to-tickets | [mattpocock/skills](https://github.com/mattpocock/skills) | MIT | 去掉了 Goal 控制器、parallel matrix、多仓库路由。保留 tracer-bullet 核心 |
| run-pilot | 原创 | — | 基于个人在 MyAgents 仓库的 skill 演进实践，不属于上游 |

本仓库同样以 MIT License 发布。修改的核心方向：去掉通用软件工程的复杂度（issue tracker、多仓库、CI 绑定），聚焦于 **单人 + Codex subagent** 的使用场景。

**如果你打算基于这套 skill 做更多修改，建议你自己 fork 一份，README 里标注清楚上游来源和你的修改内容即可。开源协议的核心要求是保留原始 License 声明，不要求你把修改回传。**
