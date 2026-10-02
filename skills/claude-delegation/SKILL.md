---
name: claude-delegation
description: Decide whether Claude Code should keep work in the main thread or delegate a bounded subtask, then define ownership, route, context, return evidence, and acceptance. Use before delegation and when a child reaches a reserved decision.
---

# Claude Delegation

Delegate only when parallelism, independent evidence, specialized capability, or
main-context protection exceeds the handoff and integration cost. Atomic or already
in-context work stays in the main thread.

## Main-thread authority

The main thread owns scope, acceptance, architecture and public contracts, persistent
data, compatibility and security, destructive effects, conflicts with user work, and the
final response. A child returns evidence and options when one of those decisions is
needed.

## Route from live configuration

Use the single configured main/executor route in `Claude delegation routes` in the
global instructions. Do not offer a
mode menu, choose a cheaper worker, or add an automatic expert/fallback route. The main
thread keeps architecture, review and acceptance; children execute bounded assignments.
Dispatch through the built-in Agent tool as the configuration describes; its model alias
and default effort are the executor binding, so do not seek separate effort verification
or start a CLI or external process to obtain a route. If the Agent tool cannot express
the configured route, report the gap and keep dependent work in the main thread rather
than silently substituting.
A later explicit user override applies only to its stated scope, not a second default mode.

Prefer the smallest context transfer that preserves meaning. Do not use a fork or model
binding merely because it is convenient; choose it because the child needs that context
or capability.

## Child contract

Start with the objective and write ownership. Include observable completion evidence,
the initial file or behavior boundary, reserved decisions, concurrency constraints,
required validation, stop conditions, and this compact return shape:

- outcome: `pass`, `partial`, or `blocked`;
- behavior delta and changed paths, including unexpected paths;
- validation commands and observed results;
- material findings, unresolved assumptions, and recovery point.

Before dispatch, compare acceptance in the brief with the authoritative requirement or
plan section. Name that source and preserve covered cases, each/all quantifiers,
deadlines and their starting events, failure outcomes, and recovery coverage. Highlight
any proposed omission or weakening; do not silently replace the source with the parent's
summary. The child checks the named source for conflicts before dependent work and returns
the conflict to the parent rather than choosing the easier interpretation. Routine,
equivalent implementation choices remain within the assignment.

If a follow-up changes acceptance or execution conditions, identify the affected source
revision or section and update the brief and relevant checks together. Reassess affected
recovery assumptions; a workflow change does not inherit proof from its predecessor.

Parallel writers require disjoint ownership or isolation. Do not let one child revert
another's work.

## Accept and recover

Check against the original requirement as well as the assigned outcome and boundary;
the parent may have weakened the brief. Read the actual diff or evidence when validation
is missing or failed, unexpected paths changed, claims conflict, or the change reaches a public contract, persistent data,
security, irreversible behavior, or consequential acceptance criteria. For consequential
acceptance, locate the actual pass/fail rule and check a minimal case that violates the
source promise while other conditions remain healthy. Logging a condition is not enforcing
it; missing coverage is not a pass. Tests derived from the same brief and a child's pass
label cannot alone establish requirement coverage. Otherwise a bounded return may be enough.

Retry once only for transport failure or an empty response. A weak semantic answer needs
a corrected contract. Return architecture, authority, destructive, and Human decisions
to the main thread. Stop route expansion after repeated failure on the same blocker.

Report the chosen lane before visible delegation and summarize accepted evidence and
remaining decisions at integration. Do not create durable reports or receipts unless the
user or repository contract asks for them.

## Lessons

- A child faithfully implemented a weakened parent brief and its tests passed. Check
  acceptance against the source at dispatch and return, including parent-introduced drift.
- Requiring proof of executor effort, which the Agent tool cannot show, pushed dispatch
  to an unauthenticated `claude` CLI and stalled an independent trial. Use the built-in
  Agent tool route as configured.
