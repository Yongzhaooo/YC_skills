---
name: delegation-policy
description: Decide whether Codex should keep work in the main thread or delegate a bounded subtask, then define its ownership, route, context, return contract, and acceptance evidence. Use before every spawn_agent call, including delegation requested by another skill, and when a child returns or needs a reserved decision.
---

# Delegation Policy

Prefer delegating clear, bounded work whose result is cheaper to verify than to reproduce.
Delegation must repay dispatch, context rebuilding, review, and likely rework through
parallelism, independent evidence, or main-context savings. Triggering this skill does
not itself require a child.

## Keep authority in the main thread

The main Agent owns task scope, acceptance criteria, architecture and public contracts,
persistent data, security and compatibility decisions, destructive or irreversible
effects, conflicts with user work, and the final response. A child may complete a bounded
assignment; when it reaches one of these decisions, it returns evidence and options.

The main Agent also executes difficult work directly when it already has the context.
Keep atomic or serially blocked work local when delegation would duplicate the immediate
next step.

Suggest a separate user-facing task when a module has its own goal and needs sustained
context and repeated user collaboration. Supply its goal, write boundary, interface
constraints, and acceptance evidence; create it only when the user explicitly asks.
Difficulty alone does not justify a new task or a stronger child.

## Select the route

Use the live `spawn_agent` schema and current routing configuration. Honor an explicit
user-selected route exactly; if unavailable, report the failure rather than substituting
silently. For implicit choices, prefer the configured lightweight route for clear,
verifiable work within its reasoning and tool capabilities; if it is unavailable, choose
the next live route allowed by the configuration that meets those needs, or work locally.
Compare total completion cost with direct work. More reasoning effort does not establish
equivalent model capability.

Prefer no-history or the smallest useful context fork. Carry recent or full history only
when the child must interpret conversation state that cannot be summarized without
changing its authority. Do not hardcode provider, model, effort, or agent identifiers in
this skill.

Before every spawn, briefly state the chosen route, ownership boundary, and expected
evidence.

Within existing task authority, dispatch an approved route without a separate user
permission round. Ask only when substantive scope, authority, destructive action, or
acceptance is missing.

## Give the child a bounded contract

Give the objective, starting files or data, write boundary, and completion evidence.
Include reserved decisions, concurrent writers, required checks, and stop conditions
when they affect the assignment. Request the compact return below.

Project an existing ticket or plan faithfully when one exists. Do not make the child
infer missing authority or inherit a planning schema merely because the task is small.

## Use only useful concurrency

Match active children to independent ready work. Parallel writers need disjoint ownership;
otherwise partition or serialize them. The platform limit is a ceiling, not a target.
Reuse an existing child for a bounded repair instead of creating a replacement merely
for a fresh context.

## Require a compact return

The child returns:

- outcome: `pass`, `partial`, or `blocked`;
- behavior delta and changed paths, including unexpected paths;
- validation actually run and observed results;
- material findings, unresolved assumptions, and the next recovery point.

Inspect the actual diff or evidence when required validation failed or is missing, the
child touched unexpected paths, its claims conflict with source evidence, or the change
reaches a public contract, persistent data, security, or irreversible behavior.

## Handle failure without loops

- Retry the same route once only for transport failure or an empty return.
- A semantically weak answer needs a corrected contract, not the same prompt repeated.
- A reproducible implementation defect returns to its implementer with the counterexample.
- A capability shortfall returns to the main Agent for decomposition or direct work.
- Environment and permission failures return to the main Agent.
- Scope, authority, architecture, or destructive decisions return to the main Agent or
  user.

After repeated failure on the same objective and blocker, stop expanding routes and ask
for the missing decision with the evidence already established.

## Verification and reporting

Use `test-verification` for code evidence and follow `plan-work` evidence ownership when
an approved plan already assigns it. Do not add a verifier, report, ledger, hash, board,
or durable receipt unless the user, repository contract, or reachable risk requires it.

At integration, report accepted evidence, rejected or blocked child work, and remaining
main-thread decisions. Child self-review is evidence, not automatic acceptance.

## Lessons

- Route availability and provider diagnosis belong in a diagnostic source, not the
  default dispatch path.
- Useful concurrency comes from independent ready work, not from filling every slot.
- Reuse the defect owner; fresh routing is for a different scope or grounding failure.
