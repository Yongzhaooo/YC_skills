---
name: plan-work
description: Use after a design direction is settled and before implementation to write a concise spec and slice it into small, demonstrable, verifiable vertical work items.
---

# Plan Work

这是两个可独立使用的阶段：记录已经决定的设计，再把设计拆成可执行的工作项。它不开始实现，也不创建远程 issue、分支、提交或 PR。

## Part 1 — 写设计说明

先读项目规则、相关代码、已有契约和当前状态。事实必须有证据；用户的显式决定与推断要区分。若行为、范围、兼容性或验收条件仍有关键未决项，标成开放决策或建议先使用 `grilling`。

优先扩展已有设计文档；没有约定时，将新文档写到 `docs/specs/YYYY-MM-DD-<slug>-design.md`。按需使用以下结构：

```markdown
# <标题>

Date: YYYY-MM-DD
Status: Draft | Approved direction, pending implementation

## Problem and Outcome
## Goals
## Non-Goals
## Acceptance Criteria
## Decisions and Rationale
## Preserved Behavior and Invariants
## Failure and Boundary Behavior
## Verification Seams
## Migration and Compatibility
## Risks
## Open Decisions
```

验收条件必须描述可观察的结果，覆盖正常、失败、边界、兼容和迁移情形中真正相关的部分。可行性尚未验证时，先做 `run-pilot`，不要把猜测写成设计。

## Part 2 — 拆分工作项

既有设计可直接进入本阶段。每个 work item 都是一个纵向切片：能在一个专注实施会话完成，单独可演示、可验证，并贯穿它所需的层，而不是“写完所有类型”或“补完所有测试”这样的水平层。

每项包含：

- 稳定 ID、交付的可观察结果、范围和非目标；
- 要检查或改动的区域，以及建立的行为/契约；
- 测试切口、实施和验证命令、完成证据；
- 真实依赖、它解锁的后续项，以及必要时的回滚或迁移说明。

只画技术、权限或证据上的真实依赖。明确当前已经解锁的项目。先向用户展示拆分结果，获得认可后再写入项目约定的计划目录；随后停止，不自动开始第一项。
