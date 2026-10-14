---
name: route-work
description: Use only when the user explicitly invokes route-work or asks which skill or sequence of skills in this repository fits their situation. Names the next skill to call, the likely path after it, and where a human decision falls, then stops. Does not run the skills it names.
disable-model-invocation: true
---

# Route Work

Place the user's situation on a route through this repository's skills, name the next
call, and stop. The user calls it. Naming a skill grants no authority to run it or any
later stage.

This file holds routing only. Each skill's own `SKILL.md` is authoritative for what it
does; when a detail matters, read it rather than describing the skill from this map.
Route only over skills that are installed. If a named skill is missing, say so and give
the closest installed route instead of inventing one. Do not route over skills from
other repositories.

## Answer shape

1. **Where you are:** one line placing the situation on a route below.
2. **Next:** the single skill to call now, with a one-line example invocation.
3. **Then:** the likely following steps, with the condition that selects each branch.
4. **Your decisions:** the points where the user, not an agent, must choose.
5. **Session:** only if a phase boundary is near, the session advice below.

Keep the answer short. If the situation fits no route, or the task is small and clear,
say so: do it directly, no skill needed. Ask one question only when two routes differ
and the description cannot decide between them.

## Routes

**New project (0 → 1).**
`grilling` to settle goals, users, non-goals and constraints → `run-pilot` only for an
assumption whose failure would change the plan → `product-spec` to write the expected
shape → `system-blueprint` for the target architecture and milestones when the work
spans modules or stages → `wayfinder` to open the map when the work will span several
sessions → `plan-work` for the first thin end-to-end slice → implement →
`test-verification` → `code-review` → back to `wayfinder`; plan the next slice, or revise
`product-spec` or `system-blueprint` when the shape or the route changes. Add `local-ci`
once the checks are slow enough to run before every push. A short-lived tool skips
`product-spec`, `system-blueprint` and `wayfinder`.

**Change in an existing codebase.**
`repo-map` when the entry point or change boundary is unclear → `grilling` if decisions
are open → `system-blueprint` when the change crosses modules or changes an interface,
data shape or deployment shape → `plan-work` when the change needs a durable plan or
another executor →
implement → `test-verification` → `code-review`.

**Bug or failing check.**
`repo-map` if the failure site is unknown → fix → `test-verification`, which also covers
remote CI triage. A failing local CI script or pre-push hook goes to `local-ci`.
Feasibility doubts about the fix go to `run-pilot` first.

**Resume or hand over.**
Returning to long work: `wayfinder`. Leaving work for another agent or session: `handoff`.

**Codebase health.**
`improve-codebase-architecture` to find friction → `codebase-design` as the criteria for
the chosen candidate → `plan-work` if the refactor is non-trivial.

**Standalone.** `local-ci` to set up or change a local CI script and hooks;
`bounded-filesystem-cleanup-safety` before destructive cleanup;
`github-release-recovery` when a tag and its Release disagree; `agy-assist` for bounded
reading, polishing or a second opinion; `clean-action` only on explicit request.

## Close pairs

| Choosing between | Test |
| --- | --- |
| `grilling` / `run-pilot` | Is the open question a decision (grill) or a fact that needs evidence (pilot)? |
| `run-pilot` / `plan-work` | Unknown whether it can work: pilot. Direction settled: plan. |
| `product-spec` / `system-blueprint` / `plan-work` / `wayfinder` | What the product should be / how the system is built to get there / how one change gets made / where the work stands. |
| `test-verification` / `local-ci` | Which checks this change needs / the project's local CI pipeline, its hooks and its failures. |
| `proposal-review` / `code-review` / `maintainer-review` | Unimplemented approach / an existing diff / long-term design of a subsystem or patch series. |
| `codex-delegation` / `claude-delegation` / `agy-execution` | Pick by runtime: Codex subagents / Claude Code Agent tool / Pi + Antigravity. `agy-execution` needs the user to ask for AGY. |
| `agy-assist` / `agy-execution` | Text only / implementation and tests. |
| `codebase-design` / `improve-codebase-architecture` / `system-blueprint` | Criteria for one boundary / a scan for where friction is / the target structure and route for the whole change. |

## Human decisions

Mark these on every route that reaches them: what the product should be and what is out
of scope; accepting a pilot result and choosing the next route; approving a blueprint or a plan before
implementation; accepting a delivery; anything outward-facing, destructive, or financial.

## Session advice

At a phase boundary (pilot done, plan accepted, slice delivered), choose the first that fits:

1. **Continue** when the next step needs the context already loaded.
2. **Fresh session** when the next step needs little of it and the durable state lives in
   files (`docs/product.md`, `docs/architecture.md`, the plan, `docs/wayfinder.md`).
3. **`handoff`** when another agent continues or the state is not yet in files.
4. **Delegate** a bounded subtask with the runtime's delegation skill when the main
   thread should keep its context for decisions.
5. **Compact** only as the last resort; it keeps the session but loses detail unpredictably.
