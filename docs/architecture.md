# YC Agile Agent Skills architecture

Last confirmed: not yet confirmed
Product spec: [product.md](product.md)

## Target structure

- **`skills/<name>/`**：每个目录是一个可安装单元，入口 `SKILL.md`；可带 `scripts/`、`references/`、`agents/openai.yaml`。skill 之间只通过显式链接引用，各自可独立安装。当前 22 个。
- **`tests/`**：`agy-assist`、`agy-execution`（含 Pi 账号、后台、对话）与 `wayfinder` 检查脚本的离线测试，使用 `unittest` / `pytest`，不调用模型。
- **发布面**：`README.md`、`README.en.md`（内容一致）、`THIRD_PARTY_NOTICES.md`、`LICENSE`（MIT）。分类与来源列在 README 中维护。
- **State ownership**：skill 内容的权威在 MyAgents（源码仓库）；本仓库只拥有"选择了哪些 skill、去标识后的公开文本、README 与来源声明"。安装后的运行时副本归使用者。
- **与 MyAgents 的重叠（明确）**：`skills/` 中约 20 个 skill 与 MyAgents `skills/shared`、`skills/codex` 同名，AGY 两项对应 MyAgents 的 `pi-agy-*`。这是有意的"精选公开副本"，不是第二个源码权威；但当前没有机制检查漂移。2026-10-15 对比（忽略换行）：20 个同名 SKILL.md 中 11 个仅差 MyAgents 私有 frontmatter（`targets`/`install_mode`），约 9 个有正文差异（bounded-filesystem-cleanup-safety、local-ci、plan-work、wayfinder、maintainer-review、claude-delegation、handoff、codebase-design、codex-delegation）。
- 数据流（proposed 的形式化）：MyAgents 已审阅源码 → 人工精选与去标识 → 本仓库 → `npx skills add` → 使用者运行时。反向无自动流。

## Approach

- 已定（AGENTS.md）：精选分享版，保留来源与许可，不自动反向导入。
- 同步方式有两个可行答案：
  - A. 继续手工同步：零基建；代价是漂移不可见、版本说明靠更新记录人工维护。
  - B. 在 MyAgents 侧用 catalog 标记并导出（或在本仓库加只读比对脚本）：漂移可检出；代价是需要跨仓库工具与去标识规则的显式化。
  - (proposed) 先 A + 一次性漂移盘点，再由用户决定是否做 B。不在本仓库内复制 MyAgents 的 harness。
- 不增加 CI、打包或版本机制，直到同步方式确定。

## Route

- **M0 现状（working）**：22 个 skill、双语 README、来源声明与离线测试已就位；最近同步记录见 README 更新记录。
- **M1 漂移盘点（proposed）**：逐 skill 与 MyAgents 对比，标注"有意去标识 / 应同步 / 应回流"。验收：差异清单对应到每个字节不同的 skill；只读。
- **M2 同步规则落文（proposed）**：把去标识与同步步骤写进 AGENTS.md 或 docs，注明取自 MyAgents 的提交。验收：下一次更新可按文档重复执行。
- **M3 可选自动化（proposed，取决于决定）**：仅在选定 B 后设计。
- 不可逆点：推送到公开 GitHub 仓库并被他人安装；发布前必须检查无公司内部信息，且在用户授权下进行。
- 临时脚手架：无。

## Open decisions

- 同步方式 A / B；blocks：M3 及任何自动化。
- 是否保留 `claude-delegation` 与 `agy-*` 在公开版中的命名与 MyAgents 不一致；blocks：M1 差异清单的判定标准。
- 本仓库是否需要自己的 wayfinder；blocks：跨会话恢复与进度可见性。
- 整体目标与路线待用户确认；不授权发布。
