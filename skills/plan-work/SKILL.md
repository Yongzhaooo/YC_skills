---
name: plan-work
description: Turn settled requirements into execution-ready plans with concrete scope, interfaces, acceptance evidence, and explicit parallel and sequential dependencies. Use when settled work needs a durable plan or a handoff to another executor.
---

# Plan Work

Write a plan another implementer can act on without reconstructing key decisions: the
required behavior, change boundary, shared interfaces, execution dependencies, and
evidence of completion. Leave routine implementation details to the implementer.

Reuse an existing request, issue, or specification when it already carries that
information. A bounded change can be one work item with no new document. Detail follows
risk, ambiguity, coupling, and recovery needs, not task count. A plan covers one change.
The product's expected shape belongs to the project's product spec (`docs/product.md`
when present): reference it, and when this change alters that shape, make updating the
spec part of the work.

Planning alone does not authorize implementation, remote issues, or Git history changes.
Honor implementation authority already supplied by the user. Keep any step that
communicates with people or changes financial state separate from its preparation. Record
existing authorization that covers the exact action, with its limits; mark any uncovered
step **awaiting specific user authorization**, naming the approval it needs (recipient or
destination, content or commitment, and any amount and terms) as its stop condition and
release dependency. Broad execution authority and an approved plan do not cover it, and
the mark carries into every handoff, delegated task, and automation.

## Ground the plan

Read the relevant requirements and repository instructions, then inspect only enough of
the affected entry points, reusable code, known consumers, and nearby checks to settle the
boundary. Record exact paths and useful symbols, marking proposed files as new.

Resolve routine technical choices from that evidence. If a material product, public
contract, compatibility, authority, or acceptance decision remains open, name it and the
stages it blocks, and keep independent work ready. Label new design proposals separately
from decisions settled by the user or an existing contract. When feasibility is the open
question, use a bounded pilot instead of planning around an assumption.

## Record the decisions execution needs

Capture or reference the outcome, goals and non-goals, affected owners, settled decisions
and preserved behavior, acceptance and failure behavior, fixed values and constraints,
and material open decisions. Add migration, compatibility, security, performance, or
rollback detail when the change reaches those concerns. Extend the existing specification
instead of creating a competing authority, keep shared constraints in one place, and give
each requirement an owning item. A saved plan uses the repository's established location
and the user's requested format.

Preserve acceptance meaning through decomposition: covered cases, each/all quantifiers,
deadlines and their starting events, required observations, and failure and recovery
outcomes. Replacing per-event checks with an end-state check, dropping a case, or
downgrading an assertion to record-only is a contract change: state the old and proposed
guarantee, the reason, and the affected items, and settle it within existing authority. Equivalent implementation choices need
no approval. When execution conditions change (unattended runs, reboots, a different
management channel), recheck where protection starts and ends and whether recovery still
works when the component under test fails.

## Define work items

Split only when an item has its own observable outcome and independent acceptance, or a
real producer/consumer boundary needs separate ownership. Prefer vertical behavior slices;
fold setup, tests, and documentation into the result that needs them. Agent capacity is
not a reason to split.

Each item covers five fields, a sentence or two each for an ordinary item; add precision
where risk would leave the executor guessing:

1. **Outcome**: observable behavior or artifact, linked to its requirement.
2. **Scope**: known create/modify/test paths, write ownership, preserved behavior, and
   relevant non-goals.
3. **Steps**: ordered changes or bounded investigations. Name the approach where leaving
   it open would change a contract or invalidate another item.
4. **Validation**: expected behavior or assertions and the commands or observations that
   establish them; name environments or data when they affect reproducibility.
5. **Stop condition**: missing decisions, pending specific authorization, conflicting
   evidence, or scope changes that pause dependent work and return to the plan owner.
   Ordinary check failures enter authorized diagnosis and repair.

For a cross-item, public, persistent, shared-state, or security-sensitive contract, add
**Interfaces**: producer, known consumers, exact names and signatures or data shape, fixed
values, failure behavior, and the consumer-level proof for the join. Reference the
contract where it is defined instead of repeating it.

Write actual conditions and expected behavior in place of placeholders such as "handle
edge cases"; add a short input/output example when prose stays ambiguous. Write
implementation bodies only when exact content must be preserved.

## State dependencies

Every multi-item plan states which items are ready now, which can run together, and what
releases each pending item; task order alone does not express a dependency. Name what each
waits on: a decision, another item's output, or a shared environment needed only for
validation, with one owner for each combined check. A stable contract lets a consumer
proceed before its producer finishes. Parallel items need settled shared interfaces and
disjoint write ownership, including mutable state such as fixtures, databases, and
services; separate checkouts do not isolate a shared service. When nothing can run in
parallel, name what forces sequencing. A shared-contract change pauses only the items that
consume it. Use a table only for several dependencies or joins. The plan describes
feasible concurrency; execution capacity decides how much is used.

## Assign evidence

For each consequential acceptance claim, name its check and pass/fail rule, plus the
smallest violating case the rule must reject while unrelated conditions stay healthy; a
log or a test count is not this proof. For asynchronous or sampled observations, define a
valid sample and the required coverage. Missing coverage stays unverified, not passed.
For a defect, prefer a regression check that fails before the fix when practical, without
imposing test-first order or per-item commits. Distinguish planned checks from commands
actually run.

For multi-session execution, the plan records accepted results, pending joins, and the
next ready item; a project map links to the plan instead of restating it. Add other
reports or ledgers only when the user or repository asks.

## Check once, then hand off

Before presenting, check once that each source requirement has an owning item,
cross-item contracts agree, and no dependency cycle or unowned join remains; fix gaps in
place. This is a self-check, not a reviewer dispatch. The plan supplies items and
ownership boundaries; models, agent counts, and reviewers belong to the runtime's
delegation rules at execution time.

For a planning-only request, present the plan and stop. If the user already authorized
implementation and no material decision remains open, continue without another approval
round; steps awaiting specific authorization still wait.

## Lessons

- Planning depth follows decision and recovery risk, not task size alone.
- A ticket projects existing authority; it does not manufacture missing decisions.
- A plan promised per-event checks while its execution specification checked only the
  final state. Internally consistent instructions and tests can still miss the original
  goal; test a violating case.
- This skill grew by appending incident rules until planning, authorization,
  verification, and delegation shared one file. Keep cross-cutting rules with their owner;
  record an incident here as one Lesson unless the general rule changes.
