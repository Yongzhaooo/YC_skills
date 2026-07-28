---
name: plan-work
description: Turn settled decisions into an approved design spec and the smallest execution-ready vertical ticket set. Use after decisions are made, before implementation.
---

# Plan Work

Two halves of one job: write down what was decided (Part 1), then cut it into the
smallest set of work that can be executed safely (Part 2). Run either half alone — a
spec without slicing is fine, and an existing spec can go straight to Part 2. One
ticket is a complete plan when the work shares one state owner and one acceptance
boundary.

This is planning. It does not start implementation or create remote issues, branches,
commits, or pull requests.

## Part 1 — Write the spec

### Preconditions

A settled decision must already exist. If material behavior, scope, compatibility, or
acceptance questions are still open, either write a spec marked `Draft — open decisions`
that names them, or stop and suggest a `grilling` session. Read the relevant `AGENTS.md`,
source, existing specs, and current repository state; use verified facts and explicit
user decisions, and mark anything inferred. Never mark a spec approved just because you
wrote it.

### Classify the scope first

- **Temporary containment / quarantine.** The spec mitigates a known upstream defect or
  transient risk and will be removed when the upstream condition resolves. Write only the
  containment mechanism, its contract, contamination isolation, cleanup, and
  verification. Keep acceptance criteria to the contained state and defer the permanent
  design in one sentence. Typically 150-300 lines, 5-15 acceptance criteria. Do not put
  the containment and post-containment worlds in one document.
- **Permanent architecture.** The behavior will persist. Use the full contract below.

### Synthesis workflow

1. Identify the problem, the user-visible outcome, the affected system, and who owns it.
2. Reconcile the conversation against repository evidence and existing contracts.
3. List explicit decisions, assumptions, preserved behavior, and unresolved questions.
4. Write acceptance criteria that distinguish a root fix from a superficial patch.
5. Describe normal, failure, boundary, retry/idempotency, lifecycle, compatibility,
   security, and performance behavior where each is relevant.
6. Identify test or review seams and the evidence that will count as done.
7. Check for an existing authority covering this; extend it rather than duplicating it.
8. When the sources include an audit, postmortem, incident report, or similarly
   structured review, perform one material-finding disposition pass. Check material
   bottlenecks, limitations, observed risks, and future-default findings, not only the
   executive summary or recommendations. Map each material finding to an acceptance
   criterion, preserved invariant, open decision, evidence limitation, or a non-goal
   with its project-owned authority or follow-up. Repeated examples may share one
   disposition. If any material finding has no destination, keep the spec unapproved
   and do not hand it to Part 2.
9. Write to `docs/specs/YYYY-MM-DD-<slug>-design.md` — or the repository's own spec
   location if it has one; if neither exists, ask where specs should live before
   writing. Then report the file path and the current git commit so later work can
   tell whether the spec has moved.

### Spec contract

```markdown
# <Title>

Date: YYYY-MM-DD
Status: Draft — open decisions | Approved direction, pending implementation
Sources: <user decisions, files, commands>

## Problem and Outcome
## Goals
## Non-Goals
## Acceptance Criteria
## Decisions and Rationale
## Preserved Behavior and Invariants
## Failure and Boundary Behavior
## Verification Seams
## Migration and Compatibility
## Risks
## Open Decisions
```

Drop sections that do not apply. Prefer concrete scenarios and observable criteria over
ceremony; use user stories only when actor/need/outcome framing genuinely clarifies.

## Part 2 — Slice it into tickets

### Choose the smallest ticket set

Do not assume that multiple tickets are useful. First identify state ownership,
acceptance boundaries, and real dependency joins. Keep bounded work packages together
when they share one state owner and one acceptance boundary; checkpoints alone do not
justify extra tickets. Split only where a slice has its own observable outcome and can
be accepted independently, or where a real producer/consumer boundary requires it.

### Tracer bullets

Every work item is a **tracer bullet**: one coherent, demonstrable behavior driven
through whatever layers it needs, small enough for a single focused implementation
session, and verifiable on its own. The complete plan remains authoritative; a ticket
projection may select from it but cannot add, reinterpret, or replace missing
authority.

Each executable item carries, compactly inside the ordinary ticket:

- a stable local ID and observable outcome
- selected authority and settled facts
- allowed writes and explicit non-goals
- upstream inputs and accepted evidence
- the behavior or contract it produces
- the files or areas to inspect and change
- a failing baseline or test seam, where one applies
- implementation steps
- required validation, its evidence owner, real commands, and expected observations
- what it depends on and what it unblocks
- acceptance evidence and acceptance owner
- stop-and-return conditions
- the next recovery point
- the default review surface, targeted-expansion triggers, and full-review triggers
- a rollback or migration note, when the risk warrants one

If any required authority, seam, validation, stop condition, or recovery information is
missing, return to planning. Do not ask an executor to infer it.

### Conditional contracts

Add fields only when the behavior requires them:

- For a real cross-ticket, shared-state, persistent, or public contract, name
  `Produces`, `Consumed by`, `Exact binding`, and `Consumer proof`. Use an identifier
  already required by the business or repository contract, such as an ID, version,
  event, hash, or current tip; do not invent identity fields for isolated work.
- For fail-closed, Human-pause or required-field, stale-invalidation, exact-identity,
  archive/denylist, security, permission, or destructive gates, include a compact
  `obligation → artifact or gate → negative counterexample` mapping.
- For a structurally long delegated execution — at least three executable slices, at
  least four expected child dispatches, multiple workstreams plus verification, a real
  cross-slice/shared-state/persistent/consumer join, likely cross-session continuation,
  or an explicit Human request for long-task handling — declare that exact child
  model/effort binding is chosen at execution entry, not frozen in the plan. Do not put
  provider model identifiers in the skill or plan default.
- For that long execution, name the project-owned paths for an implementation report
  and a delegation/process audit, include both paths in `Allowed Writes`, and make both
  completed reports prerequisites for remote publication, a requested Wayfinder
  progress or Done update, or a formal report or handoff. If any path, write boundary,
  or delivery gate is missing, the plan is not execution-ready. Do not create empty
  reports during planning, and do not require them for ordinary local completion,
  pauses, compaction, or status updates.
- For a ticket that is not part of such a long execution, add report fields only when
  the Human already requested a durable report during planning. Then name its path,
  write boundary, and delivery gate; otherwise omit report fields.

An isolated single-ticket plan does not gain seam, long-execution, or report fields that
do not apply.

### Verification ownership

Assign evidence once, at the narrowest useful boundary:

- The executor owns new or modified tests and the smallest meaningful delta checks.
- A ticket verifier owns one authoritative focused or integration suite for that
  ticket's acceptance boundary.
- A join verifier owns one consumer-level or cross-slice proof at a real dependency
  join.

Do not assign the same unchanged suite to every role by default. Replay an unchanged
surface only when shared-code changes, dependency evidence, uncertainty, or another
named review trigger justifies it. Independent verification requires a verifier who did
not implement the product change; it does not require a fresh verifier after every
bounded repair. Missing or contradictory evidence expands review or blocks acceptance.

### Avoid horizontal tickets

"All types", "all backend", "all tests" are not slices — they are layers. Cut vertically
whenever a vertical behavior slice is possible. For a wide migration, use
**expand → migrate → contract** so every intermediate state is valid on its own.

### Dependencies

Keep a plain list: for each item, what it depends on and what it blocks. Draw an edge only
for a real technical, authority, or evidence dependency — not for preferred order. Then
state **what is unblocked now**: the items with no unmet dependencies. That is where work
can start, and it is recomputed after each item completes.

Before presenting the plan as execution-ready, perform one plan-wide consumer-closure
pass over actual dependency evidence: known callers, readers, writers, shared state,
persistent or public artifacts, and authority or acceptance flows. Every produced seam
names all known consumers; every consumer reciprocally names its producer and consumer
proof. Mark a genuinely isolated seam with the reason. An unknown or contradictory
material consumer blocks the affected plan. Record closure in the ordinary plan — do
not create a separate matrix, capsule, registry, or hash.

For a containment spec, do not decompose every acceptance criterion. One or two tickets —
the mechanism plus one disposable canary — is usually the whole plan. Record any deferred
permanent-architecture scope explicitly so it is not lost.

Present the slicing for approval before writing it down. Publish the plan, report the
items, dependencies, consumer closure, and what is unblocked now, and stop. Do not
dispatch an Agent or begin the first ticket.

## Lessons

- Reuse a sufficient existing authority before creating a new spec. A bounded task its
  own tracker already owns may correctly produce no new document at all.
- Feasibility uncertainty is not a spec problem. If the question is "will this even
  work", run a pilot first — a spec written over an unanswered feasibility question is
  fiction.
- A spec must distinguish the minimum required validation from conditional checks, or
  slicing inherits an unbounded verification budget.
- `run-pilot`, not this skill, owns fast bounded validation. Do not shrink the spec into
  a spike or grow a spike into a spec.
- A compact ticket is a projection of plan authority, not a replacement for it. When the
  projection and raw authority disagree, raw authority wins and review expands.
- When an audit or postmortem is source authority, approving from its headline
  recommendations can omit material limitations. Complete the disposition pass before
  approval, even when the intended skill changes already look settled.
