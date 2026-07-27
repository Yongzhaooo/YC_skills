---
name: repo-map
description: Use when locating files, symbols, callers, tests, or change boundaries in an unfamiliar, multi-file, repository-wide, or architecture-sensitive task before implementing.
---

# Repo Map

在实施前建立一份紧凑的代码库地图。先读适用的 `AGENTS.md` 或项目规则；项目本地的权限、检索和维护规则优先。

缩小根目录、文件类型、符号和关键字范围后再搜索。某条检索路径没有带来新证据时，换一种实质不同的路径，不要机械扩大搜索结果。

确认并报告：

- 入口点、用户或系统触发点；
- 按层列出的主文件、符号与调用/数据流；
- 放大风险的共享抽象、副作用与分支点；
- 已有测试和最小验证命令；
- 未知项、最快的确认方法，以及建议的改动边界。

除非用户已要求实施，否则停留在定位模式。
