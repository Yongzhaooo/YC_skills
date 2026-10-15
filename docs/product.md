# YC Agile Agent Skills product spec

Last confirmed: not yet confirmed

本仓库没有 `docs/wayfinder.md`；预期由 README.md、README.en.md 与 AGENTS.md 归纳。架构见 [architecture.md](architecture.md)。

## Purpose

向其他开发者分享一组轻量、可独立使用的 Agent 工作流 skills：帮助 Codex、Claude Code、OpenCode 等 Agent 在复杂任务中定位、澄清、试验、规划、委派、验证与审查；小而明确的任务仍直接完成。这是个人分享，不是公司官方项目。（README 已陈述）

**与 MyAgents 的关系**：本仓库是个人源码仓库 MyAgents 已审阅 skills 的精选公开副本（AGENTS.md 已陈述）。目前 22 个 skill 中约 20 个与 MyAgents 同名（`agy-assist`/`agy-execution` 在 MyAgents 中为 `pi-agy-*`，`claude-delegation` 在 MyAgents 无同名 skill），2026-10-15 对比：11 个仅差 MyAgents 私有 frontmatter，约 9 个有正文差异（详见 architecture.md）。两者内容重叠且存在漂移；MyAgents 为权威，本仓库只读消费。

## Expectations

### 安装与发现
- 用户用 `npx skills add` 安装全部或指定 skill，并可用 `$skill-name` 调用；每个 `skills/<name>/SKILL.md` 可独立安装。（README 已陈述）
- Ponytail 与 Stop That Shit 作为独立上游插件完整安装，本仓库只给指引，不以单个 skill 代替。（README 已陈述）

### 工作流
- skills 分为"工作流"与"独立工具"，每个标注来源（原创 / 改编）；任何 skill 都不自动授权下一阶段。（README / AGENTS.md 已陈述）
- skill 正文与具体模型、子代理名称、桌面端字段无关；模型选择属于使用者的全局配置。（AGENTS.md 已陈述）

### 公开安全与来源
- 不含公司内部代码、数据、系统细节、凭据、缓存、运行时导出物或个人部署元数据。（AGENTS.md 已陈述）
- 改编内容保留上游版本、修改说明与许可，记录于 `THIRD_PARTY_NOTICES.md`；中英文 README 内容保持一致。（AGENTS.md 已陈述）
- (proposed) 每次更新注明取自 MyAgents 的哪个提交（README 更新记录已有此惯例），使读者能判断新旧。

### 质量
- 带脚本的 skill（`agy-*`、`wayfinder` 检查）有离线测试，不调用模型；README 声称的测试数与实际一致。（README 已陈述，22 项）

## Non-goals

- 不打包全部个人 skills、官方内置 skill、账号集成或本机诊断配置。
- 不自动安装 Pi、ACP provider、插件或配置模型路由。
- 不从运行时目录反向导入；不另建与 MyAgents 竞争的权威源。

## Open questions

- 本仓库与 MyAgents 的同步由谁、何时、如何做（手工 / 脚本），以及如何发现漂移；blocks：判断公开版是否过期。
- 约 9 个正文差异中哪些是有意的去标识，哪些是 MyAgents 后续更新未同步；blocks：下一次发布。
- 仓库是否需要自己的 wayfinder；blocks：跨会话恢复。
- 本文整体预期待用户确认；不授权实现或发布。
