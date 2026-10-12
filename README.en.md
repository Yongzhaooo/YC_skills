# YC Agile Agent Skills

English | [中文](README.md)

These skills come from what I learned in real production work at Volvo, using coding agents such as Codex, Claude Code, and OpenCode on actual projects: which steps help and which only add process. They help an agent find its way around code, clarify an approach, run experiments, plan, delegate, verify, and review in complex tasks. Small, well-defined tasks are still done directly.

This is a personal project, not an official Volvo project, and it contains no internal company code, data, or configuration.

**Discussion and contributions are welcome.** If you have thoughts on the workflows or how to use them, [open an issue](https://github.com/Yongzhaooo/yc-agile-agent-skills/issues) and let's talk. If you find a problem in a skill, please send a [pull request](https://github.com/Yongzhaooo/yc-agile-agent-skills/pulls).

**Install the full Stop That Shit and Ponytail plugins alongside these skills.** Installing only this repository, or copying a single `SKILL.md` from either plugin, does not give you the complete plugins. Installation commands are below.

## Two kinds of skills

- **Workflow skills** can be chained by stage: understand the code, clarify the approach, record product expectations, plan, implement, verify, and review. You can enter at any stage or skip stages; finishing one stage does not authorize the next.
- **Standalone tools** cover one specific situation. Call them on their own; they neither depend on nor join the workflow.

In the "Origin" column, **original** means I wrote the skill, and **adapted** means it builds on and modifies an upstream open-source skill. See [Origins and upstreams](#origins-and-upstreams).

## Workflow skills

```text
Understand ──> $repo-map (unfamiliar or multi-file codebase)
Clarify ─────> $grilling ──> $run-pilot (only when feasibility is unproven; stops at evidence)
               $proposal-review (review an approach that has been proposed)
Define ──────> $product-spec (product expectations settled or changed)
Plan ────────> $plan-work (implementation plan and acceptance evidence for one change)
Implement ───> $codex-delegation / $claude-delegation / $agy-execution (by runtime and need)
               consult $codebase-design as needed
Verify ──────> $test-verification
Review ──────> $code-review (a given change) / $maintainer-review (long-term design, patch series)
Across sessions ─> $wayfinder (resume a long-running project) / $handoff (hand over to the next agent)
```

| Stage | Skill | Origin | When to use | Example |
| --- | --- | --- | --- | --- |
| Understand | `repo-map` | Original | Unfamiliar, multi-file, or architecture-sensitive changes where you first need entry points, call paths, and test surfaces. | `$repo-map Trace the payment callback from the HTTP entry point to the order status update and give the safe change boundary.` |
| Clarify | `grilling` | Adapted | The approach, boundaries, or trade-offs are still unclear and batched questions should surface hidden assumptions. | `$grilling I want to add an offline cache to the CLI. Help me pin down the decisions and constraints.` |
| Clarify | `run-pilot` | Adapted | Run a small, reversible experiment to test a key assumption before committing to a full design. | `$run-pilot Check on a frozen sample whether the new parser reaches the accuracy target, without touching the production entry point.` |
| Clarify | `proposal-review` | Original | Review an approach proposed by an agent or by yourself: whether the reasoning holds, the assumptions are supported, and the scope and next step are ready. | `$proposal-review Check the reasoning and assumptions of this retry approach and whether it is ready to implement.` |
| Define | `product-spec` | Original | Record or update how the product is currently expected to behave, keeping open questions and scope boundaries. | `$product-spec Update docs/product.md with the confirmed product behavior.` |
| Plan | `plan-work` | Adapted | Requirements for one change are settled and it needs a concrete implementation plan and acceptance evidence. | `$plan-work Turn the confirmed import flow into an implementation plan with acceptance checks.` |
| Implement | `codex-delegation` | Original | Codex dispatches, resumes, or accepts bounded subtasks while the main thread keeps decisions and integration. | `$codex-delegation Split this migration into parallel write scopes, keep the original acceptance criteria, and define the evidence to return.` |
| Implement | `claude-delegation` | Original | Claude Code delegates bounded work through its built-in Agent tool, routed by global configuration. | `In Claude Code, use claude-delegation to define subtask ownership, acceptance evidence, and the decisions the main thread keeps.` |
| Implement | `agy-execution` | Original | Hand implementation and testing to Pi + Antigravity ACP; the main agent sets the scope and independently accepts the result. | `$agy-execution Have AGY implement and test this fix in this directory; I will review it.` |
| Implement | `codebase-design` | Adapted | Design module boundaries, public interfaces, and testable dependencies; supplies criteria for design or review. | `$codebase-design Check whether these modules hide enough complexity and which boundaries are worth simplifying.` |
| Verify | `test-verification` | Original | Before delivering code, choose the tests closest to the change and state the evidence and the gaps. | `$test-verification Verify this fix, run the most relevant checks first, and say what remains unverified.` |
| Review | `code-review` | Adapted | Check changes since a given baseline against repository standards and the original requirements, separately. | `$code-review Review the changes since main. Report only supported problems and do not edit code.` |
| Review | `maintainer-review` | Original | Review a design, patch series, or subsystem as a long-term maintainer: interfaces, state, concurrency, compatibility, and migrations, including the Linux kernel. | `$maintainer-review Review the interface and lifetime design of this patch series from a long-term maintenance view.` |
| Across sessions | `wayfinder` | Adapted | Report a long-running project's outcome, current focus, milestones, and resume points; status queries stay read-only. | `$wayfinder Read the project's wayfinder and report progress, evidence dates, blockers, and the next entry point.` |
| Across sessions | `handoff` | Adapted | Compress the current conversation into a handoff document for the next agent. | `$handoff Write a handoff document for the next task.` |

## Standalone tools

| Skill | Origin | When to use | Example |
| --- | --- | --- | --- |
| `agy-assist` | Original | Send bounded reading, polishing, text cleanup, or a second opinion to Antigravity through Pi + Antigravity ACP; the main agent checks the result. | `$agy-assist Read this material and list the sourced conclusions and the open questions.` |
| `improve-codebase-architecture` | Adapted | Review architectural friction only and return evidence-backed improvement candidates without changing code. | `$improve-codebase-architecture Find the structural friction in the order module that is most worth fixing first.` |
| `bounded-filesystem-cleanup-safety` | Original | Cleanup that will physically delete or destructively move files, directories, or data with unclear boundaries. | `$bounded-filesystem-cleanup-safety Check whether this cleanup scope is safe to run.` |
| `github-release-recovery` | Original | Tags, Actions artifacts, and GitHub Releases disagree or the release workflow fails; diagnose layer by layer and restore a reproducible release. | `$github-release-recovery Find out why this tag did not produce a downloadable release.` |
| `clean-action` | Original | Only when the user calls it explicitly: shorten the execution path of the current task and stop when done. | `$clean-action Finish this fix by the shortest verifiable path.` |

## Language

The README is available in [Chinese](README.md) and English with the same content. All `SKILL.md` bodies are in English except `clean-action`, which is in Chinese. You can describe tasks in either language.

## How I use them

- **The main thread keeps judgment.** I currently use Astra as the main thread for scope, design, review, and integration. Only work with clear boundaries and cheap acceptance goes to subagents. Independent modules that need long context and repeated discussion get their own task. This is a preliminary adaptation from personal use, not a systematic cross-model evaluation.
- **Model choice lives in configuration.** Delegation follows global routes and the user's explicit choice for the current task; when a model is unavailable, it does not silently switch. Skill bodies do not hard-code models, and installing the skills does not configure or switch models.
- **Less mandatory process.** `plan-work` keeps the smallest plan the risk allows. Both delegation skills supply context, write scopes, and acceptance evidence per task, without fixed role templates, boards, or report sets. The Codex version includes optional task-brief examples.
- **Verify enough to deliver.** The implementer runs the most relevant checks first. Independent verification is added only when real risk, project rules, or the user call for it. Reviews look separately at "does it follow the standards" and "does it do what was asked".

These reflect my current practice. Available models, tools, and permissions depend on your runtime; this repository contains no account or model-routing configuration.

## Principles

- Do small, clear tasks directly; do not add process for its own sake.
- `grilling` clarifies decisions; `run-pilot` builds and checks one bounded experiment and stops at the evidence; `product-spec` records product expectations; `plan-work` produces the plan for one change. A skill does not authorize the next stage by itself; existing explicit authorization applies within the task's scope.
- When feasibility is unknown, start with `run-pilot`; when the direction is settled, go straight to `plan-work`.
- Pick the review by its subject: `proposal-review` for an unimplemented approach, `code-review` for an existing diff, `maintainer-review` for long-term design or a patch series.
- Before parallel work, use `codex-delegation` or `claude-delegation` (by runtime) to set write scopes and acceptance evidence; verification follows the project's own test conventions.

## Installing the skills

Use the [`skills`](https://github.com/vercel-labs/skills) installer to choose skills and target agents interactively:

```bash
npx skills@latest add Yongzhaooo/yc-agile-agent-skills
```

Install a specific skill:

```bash
npx skills@latest add Yongzhaooo/yc-agile-agent-skills --skill repo-map
```

Install globally for Codex:

```bash
npx skills@latest add Yongzhaooo/yc-agile-agent-skills --skill repo-map -g -a codex -y
```

The installer records the source, so after a new release you can update all or specific skills:

```bash
npx skills update
npx skills update repo-map
```

The repository was previously named `YC_skills`. GitHub redirects the old address, but reinstalling or updating the source with the new name is recommended.

After installation, call a skill explicitly with `$skill-name`, or let a runtime with skill routing match it to the task.

This repository is a curated set of shareable, general-purpose workflows. It does not bundle all my installed skills, built-in official skills, account integrations, or local diagnostic configuration.

Choose the delegation skill by runtime: install `codex-delegation` for Codex and `claude-delegation` for Claude Code; do not treat both as default rules for the same host. If you previously installed `delegation-policy` from this repository, replace it with the matching version so that two rule sets are not active at once. Installing a skill does not create model routes; maintain your own under `Codex delegation routes` or `Claude delegation routes` in your global instructions.

### AGY Assist and Execution: Pi setup

Both skills work with Codex, Claude Code, and OpenCode. The main thread prepares the necessary summary, automatically selects readable Codex/Claude skills, and passes them to AGY in Pi; you do not need to copy your whole skill library into Pi. Assist handles text tasks; Execution handles implementation and testing. The model is read from local routes or can be specified explicitly.

```bash
npx skills@latest add Yongzhaooo/yc-agile-agent-skills --skill agy-assist --skill agy-execution
npm install -g @earendil-works/pi-coding-agent@1.1.0
pi install npm:pi-antigravity-acp-provider@0.1.14
```

After installing, run `/login antigravity-acp` in Pi, choose Google, and complete the browser login. Set `/antigravity-acp permissions default` first, then pick an available model with `/model`. The official ACP runtime is downloaded on first use. Pi and the provider are third-party open-source components. Installing the skills does not install these dependencies or create account configuration.

For the full setup, the `agy-runner.json` template, context and skill usage, permissions, and recovery boundaries, see the [Pi ACP setup guide](skills/agy-execution/references/pi-setup.md); [Assist ships its own copy](skills/agy-assist/references/pi-setup.md), so it can be read when Assist is installed alone.

Execution reads the project's engineering rules and existing test/CI definitions, investigates and fixes within the task scope, and only contacts the dispatching thread through `ask_primary` for unresolved conflicts or real blockers. The main thread answers the `primary_request` event and the original session continues. Both skills can use `inspect_context` to read a given project's Wayfinder and, when Bench is configured, query the same project's knowledge; without those entry points they report them as unavailable. In Codex Desktop, `--background` wakes the original dispatching thread on a question, completion, or failure, so the main thread does not have to keep waiting. It reuses the official app-tools MCP messaging interface and does not poll a model on a timer. It requires the user to authorize notifying that thread and the Codex app to stay open; notifications after quitting the app and resumption after reboot are not supported. Claude and OpenCode keep foreground mode. Existing CI/CD does not imply deployment authorization. For configuration, reply commands, timeouts, and recovery, see each skill body and the setup guide.

Tested on Windows: same-session Q&A with Assist, and a full Execution run that read Wayfinder, ran a failing test, asked about a rules conflict, fixed the code per the answer, and passed the tests. In background tests, the main thread ended its turn twice and was woken by a question and then a completion notice, and the original Pi session finished without interruption. The shared version includes 22 offline regression tests. Remote CI/CD deployment was not part of these tests.

With an account pool enabled, separate Pi sessions can run concurrently, including calls on the same account and sessions waiting for the main thread's answer. Each session uses its own ACP credentials and cache directory, so switching accounts does not affect other sessions. A single Pi session still allows only one writer, and CLI quota queries stay serialized. Tested: session B finished while A waited for an answer, and A finished after the answer. Native session credentials live in the user directory and must not be committed to Git; see the setup guide for details.

| Component | Repository / docs |
| --- | --- |
| Pi | [earendil-works/pi](https://github.com/earendil-works/pi), [coding-agent docs](https://github.com/earendil-works/pi/tree/main/packages/coding-agent) |
| Antigravity ACP provider | [zacbemis/pi-antigravity-acp-provider](https://github.com/zacbemis/pi-antigravity-acp-provider) |
| Windows CLI account manager fork | [Yongzhaooo/agy-profile](https://github.com/Yongzhaooo/agy-profile), checked at [f52cbb0](https://github.com/Yongzhaooo/agy-profile/tree/f52cbb0e65e6b1968d59c2b5686a84cb124bc346) |
| Account manager upstream | [haclongkim/agy-profile](https://github.com/haclongkim/agy-profile) |

Account rotation is optional: save CLI profiles in the manager above, complete ACP login for the same accounts, run `pi_accounts.py enroll` to match identities automatically, and then enable `rotation` in the route. The adapter in this repository handles ACP snapshots and automatic recovery; `agy-profile` manages CLI profiles and quota queries. The adapter currently depends on the manager's PowerShell functions and file layout. The checked fork matches the tested installation; compatibility with future upstream versions is not claimed. ACP snapshots use Windows DPAPI. On other platforms, turn rotation off and use a single account; do not copy Windows credentials to other machines.

Call from an installed skill directory:

```text
python scripts/agy_assist.py --prompt-file assignment.txt --input-file source.txt --skill <absolute path to SKILL.md>
python scripts/agy_execution.py --cwd <project directory> --prompt-file assignment.txt --output-dir <new evidence directory> --skill <absolute path to SKILL.md>
```

Inputs use UTF-8; on Windows set `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8`. Assist's `--schema` is validated by Python `jsonschema`; install it with `python -m pip install jsonschema` before using that option or running the related tests. `--conversation` takes the exact Pi session path that was returned. When the user explicitly asks AGY to implement, fix, build, or test, that authorizes the necessary tool calls within scope; the main thread passes Execution's `--auto-approve` directly without asking again. Read-only, resource, and other limits still apply; installing or discussing a skill is not execution authorization. Without the flag, the runner uses `default` permissions.

Acceptance covered multi-skill text calls, implementation tests in a temporary directory, real quota-exhaustion account switching, and cross-account session continuation. Performance comparisons were not done, and account rotation was not tested on macOS or Linux. The offline tests do not call a model:

```text
python -m unittest discover -s tests -p "test_agy*.py"
python -m unittest discover -s tests -p "test_pi*.py"
```

### Wayfinder reading-budget check

The `wayfinder` checker uses only the Python standard library. By default it compares `docs/wayfinder.md` with Git HEAD and flags over-budget growth and newly pasted logs:

```text
python skills/wayfinder/scripts/wayfinder_check.py docs/wayfinder.md
python -m pytest tests/test_wayfinder_check.py
```

Agent hooks must be configured by each user; installing the skill does not enable a turn-end check.

## Also install the full Stop That Shit and Ponytail plugins

These are separate upstream plugins and should be installed in full through a plugin installer, including their skills, commands, and hooks. Do not use `npx skills add` to extract a single skill in place of the full plugin. This repository does not install them.

In a Codex CLI terminal that supports `codex plugin`:

```bash
# Ponytail: prefer reuse, avoid over-engineering
codex plugin marketplace add DietrichGebert/ponytail
codex plugin add ponytail@ponytail

# Stop That Shit: keep task scope tight, stop unnecessary work
codex plugin marketplace add lennney/stop-that-shit --ref 0.2.0
codex plugin add stop-that-shit@stop-that-shit
```

The referenced versions are Ponytail 4.9.0 and Stop That Shit 0.2.0. The Ponytail command follows the upstream marketplace; the Stop That Shit command is pinned to the `0.2.0` tag.

After installing, restart Codex. In a new CLI session, open `/hooks`, review the plugin commands, and trust the hooks as the upstream instructions describe before starting a new task. Restart the desktop app as well if you use it. The [Ponytail installation guide](https://github.com/DietrichGebert/ponytail#codex) and the [Stop That Shit 0.2.0 installation guide](https://github.com/lennney/stop-that-shit/tree/0.2.0#codex) are authoritative.

Choose a Stop That Shit mode for the actual task, for example `$stop-that-shit review -- review this diff only, no changes` or `$stop-that-shit change -- make the changes within the confirmed scope`. The watch-only state before a mode is confirmed does not mean writes are being blocked by the Guard.

## Origins and upstreams

This repository is released under the MIT License. MyAgents is my personal skill source repository; this is a curated public version with deployment metadata removed. Updates come from reviewed source, not a mirror of runtime directories.

**Original** (written by me): `repo-map`, `proposal-review`, `maintainer-review`, `product-spec`, `codex-delegation`, `claude-delegation`, `agy-assist`, `agy-execution`, `test-verification`, `bounded-filesystem-cleanup-safety`, `github-release-recovery`, `clean-action`.

**Adapted** (based on and modifying MIT-licensed upstream content):

| Skill | Upstream | Main changes |
| --- | --- | --- |
| `grilling`, `run-pilot`, `wayfinder`, `code-review`, `codebase-design`, `improve-codebase-architecture` | [mattpocock/skills](https://github.com/mattpocock/skills) | Leaner process, no fixed tool dependencies, verification sized to risk; `wayfinder` becomes a local project map with a reading-budget checker. |
| `handoff` | [mattpocock/skills](https://github.com/mattpocock/skills) | Upstream body kept nearly as is; metadata adjusted. |
| `plan-work` | [mattpocock/skills](https://github.com/mattpocock/skills), also drawing on `writing-plans` from [obra/superpowers](https://github.com/obra/superpowers) | Adds concrete interfaces, acceptance evidence, execution dependencies, and separate authorization for communication with people and financial actions. |

Adapted skills keep tracking their upstreams. The upstream revision, change notes, and copyright notice for each are recorded in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). When an upstream update is worth adopting, I review and merge it and update the record rather than overwriting local changes.

Pi, the Antigravity ACP provider, and `agy-profile`, used with the AGY skills, are separate third-party components installed on their own (see above). Ponytail and Stop That Shit are maintained by their upstreams; this repository only provides installation guidance.

## Changelog

- 2026-10-12: Added `proposal-review` and `maintainer-review` (from MyAgents `0d290ba`). Renamed the repository to `yc-agile-agent-skills`, added the English README, and marked each skill as original or adapted. Synced the planning workflow: new `product-spec` keeps the product's expected behavior in `docs/product.md`; `plan-work` covers the implementation plan for one change, and `run-pilot` stops at experiment evidence. `wayfinder` ships a reading-budget checker; installing the skill does not register agent hooks.
- 2026-10-11: Moved `agy-assist` and `agy-execution` to Pi + Antigravity ACP, with context summaries from the main thread, Codex/Claude skills, exact session continuation, and two-way Q&A during a run; they can read a project's Wayfinder/Bench, and Windows can optionally switch accounts automatically when quota runs out. The AGY sharing version comes from MyAgents `37c84eb`.
- 2026-10-03: Updated `wayfinder` and replaced the old `delegation-policy` with `codex-delegation` and `claude-delegation` (from MyAgents `16def2a`). Model routes come from the user's global configuration; when none is configured or the tool cannot express it, work stays on the main thread without silent downgrade.
- 2026-09-05: Preliminary Astra adaptation: less mandatory process, judgment kept on the main thread, delegation and verification as needed.
