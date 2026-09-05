---
name: plan-work
description: Turn settled decisions into the smallest useful design record and execution-ready work items. Use after material choices are made and before implementation when the work needs durable planning.
---

# Plan Work

Write only the planning artifact the work needs. A bounded task already owned by a clear
request, issue, or specification may need no new document. One work item is a complete
plan when it has one outcome and acceptance boundary.

This skill does not start implementation, create remote issues, or change Git history.

## Confirm planning is ready

Use verified repository facts and explicit user decisions. If a material product,
compatibility, authority, or acceptance decision remains open, record it as open or
return to the user; do not make an executor infer it.

When feasibility is the unresolved question, use a bounded pilot instead of writing a
spec around an assumption.

## Write the smallest design record

Capture:

- the problem and observable outcome;
- goals, non-goals, and affected owners;
- settled decisions and preserved behavior;
- acceptance criteria and failure behavior;
- validation evidence and material open decisions.

Add migration, compatibility, security, performance, or rollback detail only when the
change reaches those concerns. Extend an existing authority instead of duplicating it.

Use the repository's specification location. A practical default is:

```markdown
# <Title>

Status: Draft | Approved direction
Sources: <decisions and repository evidence>

## Outcome and Scope
## Decisions
## Acceptance
## Validation
## Open Decisions
```

Drop sections that do not help execution or acceptance. Do not prescribe document length
or a minimum number of acceptance criteria.

## Create the smallest work-item set

Split only when an item has its own observable outcome and can be accepted independently,
or when a real producer/consumer dependency requires sequencing. Prefer vertical behavior
slices over separate type, backend, frontend, and test layers.

Every ordinary work item needs five fields:

1. **Outcome** — observable behavior or artifact.
2. **Scope** — allowed changes and explicit non-goals.
3. **Steps** — the smallest credible implementation path.
4. **Validation** — commands or observations that establish acceptance.
5. **Stop condition** — what returns the task for a decision or blocks acceptance.

For multiple items, add dependencies and a recovery point. State which items are
unblocked now. For a public, persistent, shared-state, or security-sensitive contract,
also name the producer, known consumers, exact binding, and consumer-level proof.

## Assign evidence once

The implementer owns changed tests and narrow checks. Use an independent verifier when
the risk, plan, or user requires it, and give that verifier the smallest authoritative
suite for the acceptance boundary. A real cross-item join may have one consumer-level
proof. Do not assign the same unchanged suite to every role.

Long execution may need durable recovery state, reports, or process evidence. Add those
only when the user or repository contract requests them, or when cross-session recovery
would otherwise be lost. Name their paths and owners explicitly; do not create universal
ledgers, capsules, hashes, or report gates.

Present the proposed design or slicing for approval and stop. Implementation begins only
when the user has authorized it.

## Lessons

- Planning depth should follow decision and recovery risk, not task size alone.
- A ticket projects existing authority; it does not manufacture missing decisions.
- Feasibility evidence belongs in a pilot, not a speculative specification.
