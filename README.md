# YC Skills

这里分享我日常使用 Codex 的心得，以及从实际安装、使用的 skills 中整理出的通用工作流。它们是可独立取用的工具，不是每个任务都必须经过的流水线。

**当前状态（2026-09-05）：已初步适配 Astra。** 本次对照当前安装的技能和个人维护源码更新，重点是减少强制流程、保留主线程判断、按需要委派和验证。这是个人使用中的初步适配，尚未做系统性的跨模型效果评测。

**搭配使用时，记得完整安装 Stop That Shit 和 Ponytail 两个插件。** 只安装本仓库，或只复制它们某一个 `SKILL.md`，都不等于装好了整套插件。安装命令见下文。

2026-10-12：从 MyAgents `0d290ba` 同步规划工作流。新增 `product-spec`，用 `docs/product.md` 保存产品当前应有的行为；`plan-work` 负责一次变更的实施计划，`run-pilot` 停在试验证据，后续方向由用户或 Wayfinder 的路线复核决定。`wayfinder` 附带阅读预算检查脚本，安装 skill 不会自动注册 Agent hooks。

2026-10-11：`agy-assist` 与 `agy-execution` 已迁移到 Pi + Antigravity ACP，支持主线程传入上下文摘要、Codex／Claude Skills、精确会话续接和运行中的双向问答；可读项目 Wayfinder／Bench，Windows 可选启用额度耗尽后的自动切号。安装与上游链接见下文。

2026-10-03：从 MyAgents 已审阅源码更新 `wayfinder`，将旧 `delegation-policy` 替换为 `codex-delegation` 和 `claude-delegation`。两个委派版本分别供 Codex 和 Claude Code 使用；模型路由由使用者的全局配置提供，未配置或工具无法表达时保留在主线程，不自动降级。

## 工作流

```text
陌生或多文件代码库 ──> $repo-map
                         │
方案仍有关键未知 ────────> $grilling ──> $run-pilot（仅在可行性未证实时）
                         │
恢复跨任务上下文 ─────────> $wayfinder
产品预期已确定或改变 ─────> $product-spec
一次变更需要实施计划 ─────> $plan-work
实施 ──> 按运行时使用 $codex-delegation 或 $claude-delegation
         按需 $codebase-design ──> $test-verification
审查指定变更 ────────────> $code-review
```

## Skills

| Skill | 何时使用 | 简单用法 |
| --- | --- | --- |
| `agy-assist` | 通过 Pi + Antigravity ACP 将有边界的阅读、润色、文本清洗或第二意见交给 Antigravity，由主 Agent 核验。 | `$agy-assist 阅读这份材料，列出有来源依据的结论和未确定事项。` |
| `agy-execution` | 把实现与测试交给 Pi + Antigravity ACP 执行，由主 Agent 划定范围并独立验收交付。 | `$agy-execution 让 AGY 在这个目录实现并测试该修复，我来验收。` |
| `repo-map` | 陌生、多文件或架构敏感的改动，需要先找入口、调用链和测试面。 | `$repo-map 找出支付回调从 HTTP 入口到订单状态更新的路径，并给出可修改边界。` |
| `bounded-filesystem-cleanup-safety` | 清理会物理删除或破坏性移动文件、目录或不明确边界的数据。 | `$bounded-filesystem-cleanup-safety 检查这个清理范围是否可以安全执行。` |
| `github-release-recovery` | 标签、Actions artifact 和 GitHub Release 状态不一致或发布流程失败时，分层诊断并恢复可复现发布。 | `$github-release-recovery 检查这个 tag 为什么没有生成可下载的 Release。` |
| `grilling` | 方案、边界或取舍尚未说清，希望以成批问题发现隐含假设。 | `$grilling 我想给 CLI 加离线缓存，帮我把决策和约束问清楚。` |
| `run-pilot` | 在投入完整设计前，先做一个可回滚的小试验验证关键假设。 | `$run-pilot 用冻结的样本验证新的解析器能否达到准确率目标，不改生产入口。` |
| `product-spec` | 记录或更新产品当前应有的行为，保留未确认事项和范围边界。 | `$product-spec 根据已确认的产品行为，更新 docs/product.md。` |
| `plan-work` | 一次变更的需求已确定，需要具体实施计划和验收依据。 | `$plan-work 根据已确认的导入流程，拆成实施计划并列出验收检查。` |
| `codex-delegation` | Codex 派发、接续或验收有边界的子任务；主线程保留决策与整合。 | `$codex-delegation 划分这项迁移的并行写入边界，保留原始验收条件并定义回传证据。` |
| `claude-delegation` | Claude Code 使用内置 Agent 工具委派有边界的工作，按全局配置路由。 | `在 Claude Code 中使用 claude-delegation，明确子任务归属、验收证据和主线程保留的决策。` |
| `wayfinder` | 报告长期项目的结果、当前焦点、里程碑与恢复入口；状态查询保持只读。 | `$wayfinder 阅读项目的 wayfinder，说明目标进展、证据日期、阻塞和下一入口。` |
| `test-verification` | 交付代码前，选择贴近改动的测试并说明证据与缺口。 | `$test-verification 验证这次修复，先运行最相关的检查，说明还有什么没验证。` |
| `code-review` | 对指定基线以来的变更，分别核对仓库规范和原始需求。 | `$code-review 审查 main 以来的变更，只报告有依据的问题，不改代码。` |
| `codebase-design` | 设计模块边界、公共接口和可测试的依赖关系。 | `$codebase-design 看看这组模块是否隐藏了足够的复杂性，哪些边界值得简化。` |
| `improve-codebase-architecture` | 只审查架构摩擦，返回有证据的改进候选，不直接修改代码。 | `$improve-codebase-architecture 找出订单模块最值得先处理的结构性摩擦。` |
| `handoff` | 把当前对话压缩成供下一位 Agent 接手的交接文档。 | `$handoff 为下一次任务生成交接文档。` |
| `clean-action` | 用户明确调用时，压缩当前任务的执行路径并在完成后停止。 | `$clean-action 按最短可验证路径完成这个修复。` |

## 这次适配与我的使用方式

- **让主线程保留判断。** 我目前以 Astra 作为主线程处理范围、设计、审查和整合；只有边界清楚、验收成本低的工作才考虑交给子代理。需要长期上下文和反复讨论的独立模块，再考虑单独开任务。
- **模型选择放在配置里。** 委派遵循全局路由和用户对当前任务的明确选择；不可用时不静默换模型。技能正文不写死模型，安装 skills 也不会自动配置或切换模型。
- **减少强制流程。** `plan-work` 按风险保留最小计划；两个委派版本按任务提供上下文、写入边界和验收证据，不要求固定角色模板、看板或成套报告。Codex 版附带可按需阅读的任务简报示例。
- **验证到足以交付。** 实现者先做最相关的检查；只有实际风险、项目规则或用户要求需要时，才另设独立验证。审查时分别看“是否符合规范”和“是否做对需求”。

这些是当前个人实践。具体可用模型、工具和权限以你的运行时为准；本仓库不包含账号配置或模型路由配置。

## 使用原则

- 小而明确的任务直接完成，不为流程而流程化。
- `grilling` 澄清决策；`run-pilot` 实现并验证一个有边界的试验，停在证据；`product-spec` 记录产品预期；`plan-work` 产出一次变更的计划。技能本身不授权下一阶段，已有明确授权按任务范围执行。
- 可行性未知时优先 `run-pilot`；方向已定时直接 `plan-work`。
- 并行工作前按运行时使用 `codex-delegation` 或 `claude-delegation` 划分写入边界和验收证据；验证遵循项目自身的测试约定。

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

委派技能按运行时选择：Codex 安装 `codex-delegation`，Claude Code 安装 `claude-delegation`，不要将两个版本当作同一宿主的默认规则。若以前安装了本仓库的 `delegation-policy`，请用对应版本替换旧安装，避免两套指令同时生效。安装技能不会创建模型路由；请在全局指令的 `Codex delegation routes` 或 `Claude delegation routes` 中维护自己的路由。

这三个分享版取自 MyAgents `16def2a4caac968a02c43d121780ee80d24315ee`，保留配套参考文件、UI 元数据和来源许可，去除个人部署元数据及未随包提供的私有配置路径。`wayfinder` 新增结果判断、当前焦点和可选里程碑，并按证据重新判断下一步；不会因存在下一步就自动授权执行。

### AGY Assist 与 Execution：Pi 配置

两个 skill 可用于 Codex、Claude Code 和 OpenCode。主线程整理必要摘要、自动选择
可读的 Codex／Claude Skills，再传给 Pi 中的 AGY；无需把整个技能库复制到 Pi。
Assist 用于文本任务，Execution 用于实现和测试。模型从本机路由读取，也可显式指定。

```bash
npx skills@latest add Yongzhaooo/YC_skills --skill agy-assist --skill agy-execution
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

AGY 分享版取自 MyAgents `37c84eb`，保留 MIT 许可、
配套脚本和参考文件，去除个人部署元数据，并按本仓库目录调整离线测试。
已完成多 Skills 文本调用、临时目录实现测试、真实额度耗尽切号和跨账号续接验收；
未做性能对比，也未验证 macOS／Linux 的账号轮换。离线测试不调用模型：

```text
python -m unittest discover -s tests -p "test_agy*.py"
python -m unittest discover -s tests -p "test_pi*.py"
```

## Wayfinder 阅读预算检查

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

## 来源与归属

本仓库以 MIT License 发布。MyAgents 是我的个人技能源仓库，这里是经过选择、去除部署元数据的公开分享版；更新从已审阅的源码整理，不直接镜像运行时目录。

`grilling`、`run-pilot`、`plan-work`、`wayfinder`、`code-review`、`codebase-design`、`handoff` 和 `improve-codebase-architecture` 参考或改编自 [mattpocock/skills](https://github.com/mattpocock/skills) 的 MIT 许可内容，修改包括精简流程、去除固定工具依赖和按风险分配验证。来源版本与版权声明见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。其余技能为个人整理。Ponytail 与 Stop That Shit 由各自上游维护，本仓库只提供完整安装指引。
