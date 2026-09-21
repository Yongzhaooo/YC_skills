# YC Skills

这里分享我日常使用 Codex 的心得，以及从实际安装、使用的 skills 中整理出的通用工作流。它们是可独立取用的工具，不是每个任务都必须经过的流水线。

**当前状态（2026-09-05）：已初步适配 Astra。** 本次对照当前安装的技能和个人维护源码更新，重点是减少强制流程、保留主线程判断、按需要委派和验证。这是个人使用中的初步适配，尚未做系统性的跨模型效果评测。

**搭配使用时，记得完整安装 Stop That Shit 和 Ponytail 两个插件。** 只安装本仓库，或只复制它们某一个 `SKILL.md`，都不等于装好了整套插件。安装命令见下文。

## 工作流

```text
陌生或多文件代码库 ──> $repo-map
                         │
方案仍有关键未知 ────────> $grilling ──> $run-pilot（仅在可行性未证实时）
                         │
恢复跨任务上下文 ─────────> $wayfinder
方向已确定且需要留计划 ───> $plan-work
实施 ──> 按需 $delegation-policy / $codebase-design ──> $test-verification
审查指定变更 ────────────> $code-review
```

## Skills

| Skill | 何时使用 | 简单用法 |
| --- | --- | --- |
| `repo-map` | 陌生、多文件或架构敏感的改动，需要先找入口、调用链和测试面。 | `$repo-map 找出支付回调从 HTTP 入口到订单状态更新的路径，并给出可修改边界。` |
| `bounded-filesystem-cleanup-safety` | 清理会物理删除或破坏性移动文件、目录或不明确边界的数据。 | `$bounded-filesystem-cleanup-safety 检查这个清理范围是否可以安全执行。` |
| `github-release-recovery` | 标签、Actions artifact 和 GitHub Release 状态不一致或发布流程失败时，分层诊断并恢复可复现发布。 | `$github-release-recovery 检查这个 tag 为什么没有生成可下载的 Release。` |
| `grilling` | 方案、边界或取舍尚未说清，希望以成批问题发现隐含假设。 | `$grilling 我想给 CLI 加离线缓存，帮我把决策和约束问清楚。` |
| `run-pilot` | 在投入完整设计前，先做一个可回滚的小试验验证关键假设。 | `$run-pilot 用冻结的样本验证新的解析器能否达到准确率目标，不改生产入口。` |
| `plan-work` | 方向已确定，需要写设计说明并拆成可验证的纵向工作项。 | `$plan-work 根据已确认的导入流程，写 spec 并拆成实施计划。` |
| `delegation-policy` | 需要派发子任务，或需要判断主线程和子代理各自应负责什么。 | `$delegation-policy 把这项迁移拆成可并行的调研、实现和验证任务，并定义回传证据。` |
| `wayfinder` | 跨 session 恢复一个长期项目，需要知道正在做什么、卡在哪里、从哪里安全继续。 | `$wayfinder 阅读项目的 wayfinder，告诉我当前主线、阻塞和最安全的下一入口。` |
| `test-verification` | 交付代码前，选择贴近改动的测试并说明证据与缺口。 | `$test-verification 验证这次修复，先运行最相关的检查，说明还有什么没验证。` |
| `code-review` | 对指定基线以来的变更，分别核对仓库规范和原始需求。 | `$code-review 审查 main 以来的变更，只报告有依据的问题，不改代码。` |
| `codebase-design` | 设计模块边界、公共接口和可测试的依赖关系。 | `$codebase-design 看看这组模块是否隐藏了足够的复杂性，哪些边界值得简化。` |
| `improve-codebase-architecture` | 只审查架构摩擦，返回有证据的改进候选，不直接修改代码。 | `$improve-codebase-architecture 找出订单模块最值得先处理的结构性摩擦。` |
| `handoff` | 把当前对话压缩成供下一位 Agent 接手的交接文档。 | `$handoff 为下一次任务生成交接文档。` |
| `clean-action` | 用户明确调用时，压缩当前任务的执行路径并在完成后停止。 | `$clean-action 按最短可验证路径完成这个修复。` |

## 这次适配与我的使用方式

- **让主线程保留判断。** 我目前以 Astra 作为主线程处理范围、设计、审查和整合；只有边界清楚、验收成本低的工作才考虑交给子代理。需要长期上下文和反复讨论的独立模块，再考虑单独开任务。
- **模型选择放在配置里。** 我目前的轻量子任务配置是 Luna + max；不可用或不适合时回到主线程。这个个人搭配不会写死在 skill 正文中，也不会因安装 skills 自动切换你的模型。
- **减少强制流程。** `plan-work` 按风险保留最小计划，普通工作项只需结果、范围、步骤、验证和停止条件；`delegation-policy` 不再要求固定角色模板、看板或成套报告。旧版委派附件已从分享包移除。
- **验证到足以交付。** 实现者先做最相关的检查；只有实际风险、项目规则或用户要求需要时，才另设独立验证。审查时分别看“是否符合规范”和“是否做对需求”。

这些是当前个人实践。具体可用模型、工具和权限以你的运行时为准；本仓库不包含账号配置或模型路由配置。

## 使用原则

- 小而明确的任务直接完成，不为流程而流程化。
- `grilling` 澄清决策；`run-pilot` 实现并验证一个有边界的试验，停在证据；`plan-work` 产出所需计划。技能本身不授权下一阶段，已有明确授权按任务范围执行。
- 可行性未知时优先 `run-pilot`；方向已定时直接 `plan-work`。
- 并行工作前先用 `delegation-policy` 划分写入边界和验收证据；验证遵循项目自身的测试约定。

## 安装本仓库的 skills

使用 [`skills`](https://github.com/vercel-labs/skills) 安装器，可以交互式选择需要的 skill 和目标 Agent：

```bash
npx skills@latest add Yongzhaooo/YC_skills
```

也可以安装指定 skill：

```bash
npx skills@latest add Yongzhaooo/YC_skills --skill repo-map
```

全局安装到 Codex：

```bash
npx skills@latest add Yongzhaooo/YC_skills --skill repo-map -g -a codex -y
```

安装器会记录来源；仓库发布新版本后，可更新全部或指定 skill：

```bash
npx skills update
npx skills update repo-map
```

安装后可通过 `$skill-name` 显式调用，也可让支持技能路由的运行时按任务匹配。

本仓库只精选可分享的通用工作流；没有打包我的全部已安装技能、官方内置技能、账号集成或本机诊断配置。

## 另外完整安装 Stop That Shit 和 Ponytail

这两个是独立的上游插件，需要通过插件安装器安装全套，包含各自的 skills、命令和 hooks。不要用 `npx skills add` 抽取某一个 skill 来代替完整插件安装。本仓库也不会自动安装它们。

在支持 `codex plugin` 的 Codex CLI 终端中执行：

```bash
# Ponytail：优先复用、减少过度设计
codex plugin marketplace add DietrichGebert/ponytail
codex plugin add ponytail@ponytail

# Stop That Shit：控制任务范围，阻止不必要的工作
codex plugin marketplace add lennney/stop-that-shit --ref 0.2.0
codex plugin add stop-that-shit@stop-that-shit
```

本次参考的安装版本为 Ponytail 4.9.0、Stop That Shit 0.2.0。上面的 Ponytail 命令跟随上游 marketplace；Stop That Shit 命令固定在 `0.2.0` tag。

安装后重启 Codex；在新的 CLI 会话中打开 `/hooks`，检查插件命令并按上游说明信任相应 hooks，再开新任务。使用桌面端时也重启应用。完整步骤以 [Ponytail 安装说明](https://github.com/DietrichGebert/ponytail#codex) 和 [Stop That Shit 0.2.0 安装说明](https://github.com/lennney/stop-that-shit/tree/0.2.0#codex) 为准。

Stop That Shit 要按实际任务选择模式，例如 `$stop-that-shit review -- 只审查这个 diff，不修改` 或 `$stop-that-shit change -- 按已确认范围完成修改`。未确认任务模式时的 watch-only 状态，不代表写入已被 Guard 阻止。

## 来源与归属

本仓库以 MIT License 发布。MyAgents 是我的个人技能源仓库，这里是经过选择、去除部署元数据的公开分享版；更新从已审阅的源码整理，不直接镜像运行时目录。

`grilling`、`run-pilot`、`plan-work`、`wayfinder`、`code-review`、`codebase-design`、`handoff` 和 `improve-codebase-architecture` 参考或改编自 [mattpocock/skills](https://github.com/mattpocock/skills) 的 MIT 许可内容，修改包括精简流程、去除固定工具依赖和按风险分配验证。来源版本与版权声明见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。其余技能为个人整理。Ponytail 与 Stop That Shit 由各自上游维护，本仓库只提供完整安装指引。
