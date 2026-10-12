# YC Agile Agent Skills

[English](README.en.md) | 中文

这些 skills 来自我在 Volvo 实际生产工作中积累的经验：用 Codex、Claude Code、OpenCode 等编码 Agent 做真实项目时，哪些流程有用，哪些步骤是多余的。它们帮助 Agent 在复杂任务中定位代码、澄清方案、试验、计划、委派、验证和审查；小而明确的任务仍然直接完成。

这是个人分享，不是 Volvo 官方项目，也不包含任何公司内部代码、数据或配置。

**欢迎讨论和贡献。** 对工作流或使用方式有想法，欢迎[开 issue](https://github.com/Yongzhaooo/yc-agile-agent-skills/issues) 和我讨论；发现某个 skill 有问题，欢迎直接提 [PR](https://github.com/Yongzhaooo/yc-agile-agent-skills/pulls)。

**搭配使用时，记得完整安装 Stop That Shit 和 Ponytail 两个插件。** 只安装本仓库，或只复制它们某一个 `SKILL.md`，都不等于装好了整套插件。安装命令见下文。

## 两类 skills

- **工作流 skills**：可以按阶段串起来，从理解代码、澄清方案、记录产品预期、计划、实施到验证与审查。每一步都可以单独进入，也可以跳过；前一步不自动授权下一步。
- **独立工具**：针对某个具体场景，单独调用即可，不依赖也不进入上面的流程。

“来源”一列中，**原创**指我自己编写的 skill，**改编**指借鉴并修改了上游开源 skill。详见[来源与上游](#来源与上游)。

## 工作流 skills

```text
理解 ─────> $repo-map（陌生或多文件代码库）
澄清 ─────> $grilling ──> $run-pilot（仅在可行性未证实时，停在证据）
            $proposal-review（审查一个已提出的方案）
定义 ─────> $product-spec（产品预期确定或改变）
计划 ─────> $plan-work（一次变更的实施计划与验收依据）
实施 ─────> $codex-delegation / $claude-delegation / $agy-execution（按运行时与需要）
            按需参考 $codebase-design
验证 ─────> $test-verification
审查 ─────> $code-review（指定变更） / $maintainer-review（长期设计与补丁系列）
跨会话 ───> $wayfinder（恢复长期项目） / $handoff（交接给下一位 Agent）
```

| 阶段 | Skill | 来源 | 何时使用 | 简单用法 |
| --- | --- | --- | --- | --- |
| 理解 | `repo-map` | 原创 | 陌生、多文件或架构敏感的改动，需要先找入口、调用链和测试面。 | `$repo-map 找出支付回调从 HTTP 入口到订单状态更新的路径，并给出可修改边界。` |
| 澄清 | `grilling` | 改编 | 方案、边界或取舍尚未说清，希望以成批问题发现隐含假设。 | `$grilling 我想给 CLI 加离线缓存，帮我把决策和约束问清楚。` |
| 澄清 | `run-pilot` | 改编 | 在投入完整设计前，先做一个可回滚的小试验验证关键假设。 | `$run-pilot 用冻结的样本验证新的解析器能否达到准确率目标，不改生产入口。` |
| 澄清 | `proposal-review` | 原创 | 审查 Agent 或自己提出的方案：推理是否成立、假设是否有依据、范围和下一步是否就绪。 | `$proposal-review 看看这个重试方案的推理和假设，能否进入实施。` |
| 定义 | `product-spec` | 原创 | 记录或更新产品当前应有的行为，保留未确认事项和范围边界。 | `$product-spec 根据已确认的产品行为，更新 docs/product.md。` |
| 计划 | `plan-work` | 改编 | 一次变更的需求已确定，需要具体实施计划和验收依据。 | `$plan-work 根据已确认的导入流程，拆成实施计划并列出验收检查。` |
| 实施 | `codex-delegation` | 原创 | Codex 派发、接续或验收有边界的子任务；主线程保留决策与整合。 | `$codex-delegation 划分这项迁移的并行写入边界，保留原始验收条件并定义回传证据。` |
| 实施 | `claude-delegation` | 原创 | Claude Code 使用内置 Agent 工具委派有边界的工作，按全局配置路由。 | `在 Claude Code 中使用 claude-delegation，明确子任务归属、验收证据和主线程保留的决策。` |
| 实施 | `agy-execution` | 原创 | 把实现与测试交给 Pi + Antigravity ACP 执行，由主 Agent 划定范围并独立验收交付。 | `$agy-execution 让 AGY 在这个目录实现并测试该修复，我来验收。` |
| 实施 | `codebase-design` | 改编 | 设计模块边界、公共接口和可测试的依赖关系；为设计或审查提供判断标准。 | `$codebase-design 看看这组模块是否隐藏了足够的复杂性，哪些边界值得简化。` |
| 验证 | `test-verification` | 原创 | 交付代码前，选择贴近改动的测试并说明证据与缺口。 | `$test-verification 验证这次修复，先运行最相关的检查，说明还有什么没验证。` |
| 审查 | `code-review` | 改编 | 对指定基线以来的变更，分别核对仓库规范和原始需求。 | `$code-review 审查 main 以来的变更，只报告有依据的问题，不改代码。` |
| 审查 | `maintainer-review` | 原创 | 以长期维护者视角审查设计、补丁系列或子系统：接口、状态、并发、兼容和迁移，含 Linux 内核。 | `$maintainer-review 从长期维护角度审查这组补丁的接口和生命周期设计。` |
| 跨会话 | `wayfinder` | 改编 | 报告长期项目的结果、当前焦点、里程碑与恢复入口；状态查询保持只读。 | `$wayfinder 阅读项目的 wayfinder，说明目标进展、证据日期、阻塞和下一入口。` |
| 跨会话 | `handoff` | 改编 | 把当前对话压缩成供下一位 Agent 接手的交接文档。 | `$handoff 为下一次任务生成交接文档。` |

## 独立工具

| Skill | 来源 | 何时使用 | 简单用法 |
| --- | --- | --- | --- |
| `agy-assist` | 原创 | 通过 Pi + Antigravity ACP 将有边界的阅读、润色、文本清洗或第二意见交给 Antigravity，由主 Agent 核验。 | `$agy-assist 阅读这份材料，列出有来源依据的结论和未确定事项。` |
| `improve-codebase-architecture` | 改编 | 只审查架构摩擦，返回有证据的改进候选，不直接修改代码。 | `$improve-codebase-architecture 找出订单模块最值得先处理的结构性摩擦。` |
| `bounded-filesystem-cleanup-safety` | 原创 | 清理会物理删除或破坏性移动文件、目录或不明确边界的数据。 | `$bounded-filesystem-cleanup-safety 检查这个清理范围是否可以安全执行。` |
| `github-release-recovery` | 原创 | 标签、Actions artifact 和 GitHub Release 状态不一致或发布流程失败时，分层诊断并恢复可复现发布。 | `$github-release-recovery 检查这个 tag 为什么没有生成可下载的 Release。` |
| `clean-action` | 原创 | 仅在用户明确调用时，压缩当前任务的执行路径并在完成后停止。 | `$clean-action 按最短可验证路径完成这个修复。` |

## 语言

README 提供中文和[英文](README.en.md)两个版本，内容保持一致。除 `clean-action` 正文为中文外，其余 `SKILL.md` 及参考文档均为英文；调用时可用中文或英文描述任务。

## 我的使用方式

- **让主线程保留判断。** 我目前以 Astra 作为主线程处理范围、设计、审查和整合；只有边界清楚、验收成本低的工作才考虑交给子代理。需要长期上下文和反复讨论的独立模块，再考虑单独开任务。这是个人使用中的初步适配，尚未做系统性的跨模型效果评测。
- **模型选择放在配置里。** 委派遵循全局路由和用户对当前任务的明确选择；不可用时不静默换模型。技能正文不写死模型，安装 skills 也不会自动配置或切换模型。
- **减少强制流程。** `plan-work` 按风险保留最小计划；两个委派版本按任务提供上下文、写入边界和验收证据，不要求固定角色模板、看板或成套报告。Codex 版附带可按需阅读的任务简报示例。
- **验证到足以交付。** 实现者先做最相关的检查；只有实际风险、项目规则或用户要求需要时，才另设独立验证。审查时分别看“是否符合规范”和“是否做对需求”。

这些是当前个人实践。具体可用模型、工具和权限以你的运行时为准；本仓库不包含账号配置或模型路由配置。

## 使用原则

- 小而明确的任务直接完成，不为流程而流程化。
- `grilling` 澄清决策；`run-pilot` 实现并验证一个有边界的试验，停在证据；`product-spec` 记录产品预期；`plan-work` 产出一次变更的计划。技能本身不授权下一阶段，已有明确授权按任务范围执行。
- 可行性未知时优先 `run-pilot`；方向已定时直接 `plan-work`。
- 审查按对象选择：未实施的方案用 `proposal-review`，已有 diff 用 `code-review`，长期设计或补丁系列用 `maintainer-review`。
- 并行工作前按运行时使用 `codex-delegation` 或 `claude-delegation` 划分写入边界和验收证据；验证遵循项目自身的测试约定。

## 安装本仓库的 skills

使用 [`skills`](https://github.com/vercel-labs/skills) 安装器，可以交互式选择需要的 skill 和目标 Agent：

```bash
npx skills@latest add Yongzhaooo/yc-agile-agent-skills
```

也可以安装指定 skill：

```bash
npx skills@latest add Yongzhaooo/yc-agile-agent-skills --skill repo-map
```

全局安装到 Codex：

```bash
npx skills@latest add Yongzhaooo/yc-agile-agent-skills --skill repo-map -g -a codex -y
```

安装器会记录来源；仓库发布新版本后，可更新全部或指定 skill：

```bash
npx skills update
npx skills update repo-map
```

仓库原名 `YC_skills`。GitHub 会把旧地址重定向到新地址，但建议用新名称重新安装或更新来源。

安装后可通过 `$skill-name` 显式调用，也可让支持技能路由的运行时按任务匹配。

本仓库只精选可分享的通用工作流；没有打包我的全部已安装技能、官方内置技能、账号集成或本机诊断配置。

委派技能按运行时选择：Codex 安装 `codex-delegation`，Claude Code 安装 `claude-delegation`，不要将两个版本当作同一宿主的默认规则。若以前安装了本仓库的 `delegation-policy`，请用对应版本替换旧安装，避免两套指令同时生效。安装技能不会创建模型路由；请在全局指令的 `Codex delegation routes` 或 `Claude delegation routes` 中维护自己的路由。

### AGY Assist 与 Execution：Pi 配置

两个 skill 可用于 Codex、Claude Code 和 OpenCode。主线程整理必要摘要、自动选择
可读的 Codex／Claude Skills，再传给 Pi 中的 AGY；无需把整个技能库复制到 Pi。
Assist 用于文本任务，Execution 用于实现和测试。模型从本机路由读取，也可显式指定。

```bash
npx skills@latest add Yongzhaooo/yc-agile-agent-skills --skill agy-assist --skill agy-execution
npm install -g @earendil-works/pi-coding-agent@1.1.0
pi install npm:pi-antigravity-acp-provider@0.1.14
```

安装后在 Pi 中执行 `/login antigravity-acp`，选择 Google 并完成浏览器登录；先将
`/antigravity-acp permissions default` 设好，再用 `/model` 选可用模型。首次会下载
官方 ACP 运行时。Pi 和 provider 是第三方开源组件。安装 skill 不会自动安装这些依赖
或创建账号配置。

完整配置、`agy-runner.json` 模板、上下文和 Skills 用法、权限及恢复边界见
[Pi ACP 配置文档](skills/agy-execution/references/pi-setup.md)；
[Assist 也附带独立副本](skills/agy-assist/references/pi-setup.md)，单独安装即可阅读。

Execution 会读取工程规范和已有测试／CI 定义，先在任务范围内调查与修复，遇到未决
冲突或真正阻塞再通过 `ask_primary` 主动找派发线程。主线程收到 `primary_request`
事件后回复，原会话继续执行。两个技能都可用 `inspect_context` 读取指定项目的
Wayfinder，并在配置 Bench 后查询同项目知识；没有这些入口时返回不可用。
Codex Desktop 可用 `--background` 在问题、完成或失败时自动唤醒原派发线程，主线程
不必持续等待；它复用官方 app-tools MCP 消息接口，不做定时模型轮询。需要用户授权
通知该线程，并保持 Codex 应用打开；当前不支持退出应用后的通知或开机恢复。
Claude／OpenCode 保留前台模式。已有 CI/CD 不等于获得部署授权。配置、回复命令、
超时与恢复见各技能正文及配置文档。

已在 Windows 实测 Assist 同会话问答，以及 Execution 读取 Wayfinder、运行失败
测试、询问规范冲突、按答复修复并通过测试的完整流程。后台实测中，主线程两次结束
本轮后分别被问题和完成通知唤醒，原 Pi 会话连续完成；分享版含 22 项离线回归测试。
远端 CI/CD 部署不属于这次实测范围。

启用账号池后，不同 Pi 会话可并发，包括同账号调用和等待主线程答复的场景。
每个会话使用独立 ACP 凭据及缓存目录，切号不改变其他会话；同一 Pi 会话仍只允许
一个写入者，CLI 额度查询仍串行。已实测 A 等答时 B 完成、答复后 A 继续完成。
原生会话凭据保存在用户目录，不能提交 Git；细节见配置文档。

| 组件 | 仓库／文档 |
| --- | --- |
| Pi | [earendil-works/pi](https://github.com/earendil-works/pi)、[coding-agent 文档](https://github.com/earendil-works/pi/tree/main/packages/coding-agent) |
| Antigravity ACP provider | [zacbemis/pi-antigravity-acp-provider](https://github.com/zacbemis/pi-antigravity-acp-provider) |
| Windows CLI 账号管理器 fork | [Yongzhaooo/agy-profile](https://github.com/Yongzhaooo/agy-profile)，本次核对版本 [f52cbb0](https://github.com/Yongzhaooo/agy-profile/tree/f52cbb0e65e6b1968d59c2b5686a84cb124bc346) |
| 账号管理器上游 | [haclongkim/agy-profile](https://github.com/haclongkim/agy-profile) |

切号是可选配置：先在上述管理器保存 CLI profiles，再为同一批账号分别完成 ACP
登录并运行 `pi_accounts.py enroll` 自动匹配身份，最后启用路由中的 `rotation`。
本仓库的适配器负责 ACP 快照和自动恢复；`agy-profile` 管理 CLI profiles 和额度查询。
当前适配器依赖该管理器的 PowerShell 函数及文件布局，核对过的 fork 与本次实测安装
一致；未声称上游未来版本始终兼容。ACP 快照使用 Windows DPAPI，跨平台用户先关闭
轮换使用单账号，不应把 Windows 凭据复制到其他机器。

从已安装的 skill 目录调用：

```text
python scripts/agy_assist.py --prompt-file assignment.txt --input-file source.txt --skill <SKILL.md绝对路径>
python scripts/agy_execution.py --cwd <工程目录> --prompt-file assignment.txt --output-dir <新证据目录> --skill <SKILL.md绝对路径>
```

输入使用 UTF-8；Windows 设置 `PYTHONUTF8=1` 和 `PYTHONIOENCODING=utf-8`。
Assist 的 `--schema` 由 Python `jsonschema` 校验；使用该参数或运行相关测试前安装
`python -m pip install jsonschema`。`--conversation` 接收返回的精确 Pi 会话路径。
用户明确要求 AGY 实施、修复、构建或测试，即授权范围内的必要工具调用；主线程直接
传 Execution 的 `--auto-approve`，无需再问一次。只读和资源等限制仍须遵守；仅安装
或讨论技能不构成执行授权。未传参数时，runner 仍使用 `default` 权限。

已完成多 Skills 文本调用、临时目录实现测试、真实额度耗尽切号和跨账号续接验收；
未做性能对比，也未验证 macOS／Linux 的账号轮换。离线测试不调用模型：

```text
python -m unittest discover -s tests -p "test_agy*.py"
python -m unittest discover -s tests -p "test_pi*.py"
```

### Wayfinder 阅读预算检查

`wayfinder` 的检查脚本使用 Python 标准库，默认将 `docs/wayfinder.md` 与 Git HEAD 比较，检查超预算增长和新增日志内容：

```text
python skills/wayfinder/scripts/wayfinder_check.py docs/wayfinder.md
python -m pytest tests/test_wayfinder_check.py
```

Agent hooks 需要由使用者在各自环境中配置；只安装技能不会自动启用 turn-end 检查。

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

## 来源与上游

本仓库以 MIT License 发布。MyAgents 是我的个人技能源仓库，这里是经过选择、去除部署元数据的公开分享版；更新从已审阅的源码整理，不直接镜像运行时目录。

**原创**（我自己编写）：`repo-map`、`proposal-review`、`maintainer-review`、`product-spec`、`codex-delegation`、`claude-delegation`、`agy-assist`、`agy-execution`、`test-verification`、`bounded-filesystem-cleanup-safety`、`github-release-recovery`、`clean-action`。

**改编**（借鉴并修改上游 MIT 许可内容）：

| Skill | 上游 | 主要修改 |
| --- | --- | --- |
| `grilling`、`run-pilot`、`wayfinder`、`code-review`、`codebase-design`、`improve-codebase-architecture` | [mattpocock/skills](https://github.com/mattpocock/skills) | 精简流程、去除固定工具依赖、按风险分配验证；`wayfinder` 改为本地项目地图并附带阅读预算检查。 |
| `handoff` | [mattpocock/skills](https://github.com/mattpocock/skills) | 基本保留上游正文，只调整元数据。 |
| `plan-work` | [mattpocock/skills](https://github.com/mattpocock/skills)，另参考 [obra/superpowers](https://github.com/obra/superpowers) 的 `writing-plans` | 补充具体接口、验收证据、执行依赖和人际沟通／财务操作的单独授权。 |

改编的 skills 会持续跟踪上游：每个 skill 参照的上游版本、修改说明和版权声明记录在 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。上游有值得采纳的更新时，我会审阅后合并并更新记录，而不是直接覆盖本地修改。

AGY 配套的 Pi、Antigravity ACP provider 和 `agy-profile` 是独立的第三方组件，需要另行安装，见上文。Ponytail 与 Stop That Shit 由各自上游维护，本仓库只提供完整安装指引。

## 更新记录

- 2026-10-12：新增 `proposal-review` 与 `maintainer-review`（取自 MyAgents `0d290ba`）。仓库更名为 `yc-agile-agent-skills`，增加英文 README，并标明每个 skill 是原创还是改编。同步规划工作流：新增 `product-spec`，用 `docs/product.md` 保存产品当前应有的行为；`plan-work` 负责一次变更的实施计划，`run-pilot` 停在试验证据。`wayfinder` 附带阅读预算检查脚本，安装 skill 不会自动注册 Agent hooks。
- 2026-10-11：`agy-assist` 与 `agy-execution` 已迁移到 Pi + Antigravity ACP，支持主线程传入上下文摘要、Codex／Claude Skills、精确会话续接和运行中的双向问答；可读项目 Wayfinder／Bench，Windows 可选启用额度耗尽后的自动切号。AGY 分享版取自 MyAgents `37c84eb`。
- 2026-10-03：更新 `wayfinder`，将旧 `delegation-policy` 替换为 `codex-delegation` 和 `claude-delegation`（取自 MyAgents `16def2a`）。模型路由由使用者的全局配置提供，未配置或工具无法表达时保留在主线程，不自动降级。
- 2026-09-05：初步适配 Astra，减少强制流程、保留主线程判断、按需要委派和验证。
