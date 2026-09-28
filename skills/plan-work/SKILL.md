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
risk, ambiguity, coupling, and recovery needs, not task count.

Planning alone does not authorize implementation, remote issues, or Git history changes.
Honor implementation authority already supplied by the user, subject to the separate
communication and financial authorization below.

## Separate execution from communication and financial authority

Flag any work involving email, communication with people, or money. General execution
authority — including "fully authorized", "do everything", or "全部授权" — does not
authorize communication or financial actions. Do not turn these steps into ready-to-run
work merely because the surrounding implementation is authorized.

Within the authorized scope, finish research, analysis, drafts, calculations, and other
reversible preparation so the user can review a concrete result. Before sending or
replying to email, messaging people, posting comments, submitting a form to a person or
organization, making commitments on the user's behalf, or changing financial state,
require explicit user authorization for that specific action. Financial actions include
purchases, payments, transfers, refunds, subscriptions, trades, and accepting prices or
financial obligations, even through an automated service with no human recipient.

The reviewable action must identify the recipient or destination, final content or
commitment, and, where relevant, amount, currency, account, and terms. Record existing
specific authorization and its limits; do not ask again when it already covers the exact
action. Broad task approval, an approved plan, silence, and elapsed time are not substitutes.
Material changes to the recipient, content, amount, or terms require renewed authorization.

Put preparation and the external action in separate plan steps. Mark the latter as
**awaiting specific user authorization**, with the concrete approval needed as its stop
condition and release dependency. Keep independent authorized work moving. Preserve this
boundary in every handoff, delegated task, scheduled job, and automation; another executor
or tool does not acquire authority the plan owner lacks.

## Ground the plan

Read the relevant requirements and repository instructions, then inspect only enough of
the affected entry points, reusable code, known consumers, and nearby checks to settle the
boundary. Record exact paths and useful symbols, marking proposed files as new.

Resolve routine technical choices from that evidence. If a material product, public
contract, compatibility, authority, or acceptance decision remains open, name it and the
stages it blocks, and keep independent work ready; do not make an executor infer it. Label
new design proposals separately from decisions settled by the user or an existing contract.
When feasibility is the open question, use a bounded pilot instead of planning around an
assumption.

## Record the decisions execution needs

Extend the existing specification instead of creating a competing authority. Capture or
reference the outcome, goals and non-goals, affected owners, settled decisions and preserved
behavior, acceptance and failure behavior, fixed values and constraints, and material open
decisions. Add migration, compatibility, security, performance, or rollback detail when the
change reaches those concerns. Keep shared constraints in one place and give each
requirement an owning item.

When a saved plan is needed, use the repository's established location and the user's
requested format; do not impose a separate specification or a length target.

## Define work items

Split only when an item has its own observable outcome and independent acceptance, or a
real producer/consumer boundary needs separate ownership. Prefer vertical behavior slices;
fold setup, tests, and documentation into the result that needs them. Do not split work to
fill agent slots.

Each item covers five fields. A sentence or two per field is enough for an ordinary item.
Add precision where risk or ambiguity would otherwise leave the executor guessing, such as
exact inputs, failure behavior, or recovery checks for a data migration or security setting.

1. **Outcome** — observable behavior or artifact, linked to its requirement.
2. **Scope** — known create/modify/test paths, write ownership, preserved behavior, and
   relevant non-goals.
3. **Steps** — ordered changes or bounded investigations. Name the approach where leaving
   it open would change a contract or invalidate another item.
4. **Validation** — expected behavior or assertions, established by commands or
   observations; name environments or data when they affect reproducibility.
5. **Stop condition** — missing decisions, specific communication or financial
   authorization, conflicting evidence, or scope changes that
   pause dependent work and return to the plan owner. Ordinary check failures enter
   authorized diagnosis and repair; they do not automatically require user approval.

For a cross-item, public, persistent, shared-state, or security-sensitive contract, add
**Interfaces**: producer, known consumers, exact names and signatures or data shape, fixed
values, failure behavior, and the consumer-level proof for the join. Reference the contract
where it is defined instead of repeating it.

Replace placeholders such as "handle edge cases" or "add appropriate tests" with actual
conditions and expected behavior; add a short input/output example when prose stays
ambiguous. Write implementation bodies only when exact content must be preserved.

## State parallel and sequential relationships

Every multi-item plan states which items are ready now, which can run together, and what
releases each pending item. Task order alone does not express a dependency. A simple
relationship takes one sentence, for example: "A can start; B's implementation waits for
A's output X; they cannot run in parallel." Use a table or graph when there are several
dependencies or join points. When nothing can run in parallel, name the shared decision,
output, or mutable state that forces sequencing.

Label each dependency by the stage it blocks:

- **Implementation** — needs an unresolved decision or upstream result. A stable contract
  can let a consumer proceed before the producer finishes; name the contract and any test
  double built on it.
- **Validation** — work and local checks can proceed, but acceptance needs another item's
  result or a shared environment. Name the combined check and its single owner.
- **Submission or merge** — only publication or integration order; include it only when
  that stage belongs to the authorized workflow.

Parallel items need settled shared interfaces, including binding names, and disjoint write
ownership across files and mutable state such as fixtures, databases, and services.
Separate checkouts do not isolate a shared service. Partition or sequence overlaps, name who
settles a pending contract, and show serialized checks even when implementation runs in
parallel. A change to a shared contract pauses only the affected items until their
interfaces and dependencies are updated.

The plan describes feasible concurrency; execution capacity decides how much is used.

## Assign evidence once

Distinguish planned checks from commands actually run and results observed. For a defect,
prefer a regression check that fails before the fix when practical; do not force test-first
sequencing or per-item commits on every change.

The implementer owns changed tests and narrow checks. Use an independent verifier when risk,
the plan, or the user requires it, with the smallest authoritative suite for the acceptance
boundary; do not assign the same unchanged suite to every role. Reuse sufficient evidence,
rerun affected checks after changes, and widen only when shared behavior or the acceptance contract
requires it.

When cross-session recovery would otherwise be lost, record accepted results, pending joins,
and the next ready item in the plan or project record. Add other reports or process
evidence only when the user or repository contract asks, naming paths and owners; do not
create universal ledgers, capsules, hashes, or report gates.

## Check once, then hand off

Before presenting, check requirement coverage, cross-item contract consistency, dependency
cycles, and unowned joins, and fix gaps in place. This is one self-check, not a reviewer
dispatch or an iterative gate.

When clean-action is explicitly active, use it to consolidate the execution path after
coverage and interfaces are settled. Delegation routes, handoff, and acceptance belong to
the applicable delegation-policy at execution time; the plan supplies items and ownership
boundaries, not models, agent counts, or per-item reviewers.

For a planning-only request, present the plan and stop. If the user already authorized
implementation and no material decision remains open, continue the authorized work without
another approval round. Communication and financial actions still require the specific
authorization defined above.

## Lessons

- Planning depth should follow decision and recovery risk, not task size alone.
- A ticket projects existing authority; it does not manufacture missing decisions.
- Feasibility evidence belongs in a pilot, not a speculative specification.
- An implementation request remains authorized when planning is a necessary intermediate step.
- Planning detail is sufficient when the executor can implement without inventing key
  requirements or shared contracts; brevity alone does not establish readiness.
