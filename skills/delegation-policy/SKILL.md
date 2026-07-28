---
name: delegation-policy
description: Use before and during Codex delegation to decide ownership, bind long executions, project approved tickets into child contracts, reuse threads and validation state, and handle returns, repairs, escalation, and recovery.
---

# Delegation Policy

Run the main Agent as the orchestrator. Preserve its context for authority,
decomposition, cross-workstream integration, difficult judgment, human interaction, and
acceptance. Delegate only when parallelism, independent acceptance, specialized
capability, or material main-context protection exceeds the handoff and thread cost.
Atomic work, an already-in-context repair, or work that duplicates the immediate
blocking step may stay in the main thread.

## Keep these decisions in the main thread

The main Agent owns:

- task scope, acceptance criteria, and cross-workstream decomposition;
- architecture, public API, persistent data, compatibility, and security decisions;
- destructive or irreversible effects and conflicts with existing user work;
- durable specifications and final authoritative design synthesis;
- acceptance or rejection of child results and the final user response.

A child decides how to complete an already bounded assignment. When it discovers one of
these decisions is necessary, it returns evidence, options, risks, and proposed split
points instead of deciding for the main Agent.

The main Agent also executes directly when work requires its reserved authority, is
difficult and broad, must integrate conflicting workstreams, cannot progress through an
available child, or is too atomic to repay the handoff.

## Choose the route in priority order

Apply these priorities in order:

1. Honor an explicit user-selected Agent or model exactly. If unavailable, report the
   failure; never substitute silently.
2. Keep main-thread authority and difficult-and-broad work in the main thread.
3. Select the narrowest role contract that matches the work.
4. Select the lowest capability tier that safely meets the task: light for clear and
   repeatable work, standard for everyday implementation and reasoning, and strong for
   ambiguous, difficult, or high-value work.

| Task shape | Default contract | Capability floor or upgrade |
| --- | --- | --- |
| One specific repository fact | Scanner contract | Light; standard when synthesis is needed |
| Unfamiliar or multi-file map | `scanner` | Light; standard or strong as ambiguity rises |
| Mechanical bounded implementation | `implementer` | Light; standard for ordinary complexity |
| Clear repeatable non-code leaf | Bounded leaf contract | Light, then standard |
| Ordinary implementation or analysis | Generic workstream contract | Standard, then strong |
| Difficult and concentrated work | Generic workstream owner | Strong, then main Agent |
| Focused tests and regression evidence | `verifier` | Light; standard when diagnosis is needed |
| High-risk independent review | `reviewer` | Role route; strong when judgment is difficult |
| Difficult, broad, cross-workstream, or human-bound work | Main Agent | Human when authority is required |

Resolve concrete Agents and models from the live schema and routing configuration; do
not hardcode provider model identifiers here. When a role profile is below the required
capability floor, use a capable generic route and carry the same role contract in the
task instead of choosing between role clarity and adequate reasoning.

Before every dispatch, read the live `spawn_agent` schema and treat only its listed
model, reasoning-effort, fork, and optional role/type fields as the accepted candidate
surface. Do not assume that a field such as `agent_type` exists merely because another
runtime exposes it. A successful spawn is the availability check; a listed managed route
may still be temporarily unprovisioned. Role contracts, managed types, and model
overrides are not interchangeable. Use each through the exact field the live schema
provides, honor any fork-mode restriction on overrides, and preserve identifiers exactly.

If an implicitly selected route is unavailable, preserve the contract and move to the
next capability tier. If an explicitly selected route is unavailable, report the exact
unsupported field or platform error and wait for direction.

## Bind long executions at entry

Treat the authorized execution as long and delegated when any of these applies:

- at least three executable slices;
- at least four expected child dispatches;
- multiple child workstreams plus a ticket or join verifier;
- a cross-slice join, shared state, persistent contract, or consumer binding;
- likely continuation across a session, compaction, or handoff;
- an explicit Human request for long-task, parallel, or model-budget handling.

A single bounded ticket, main-thread-only implementation, or one implementer plus one
focused verifier without a cross-slice seam is not long merely because the diff is large
or a test is slow.

Immediately before the first child dispatch of a long execution, show the exact current
recommended role-to-model/effort binding. The Human chooses either that complete binding
or a custom exact binding. Do not freeze a planning-time recommendation, hardcode
provider model identifiers in this skill, or silently alter the main-thread model,
reasoning level, or intelligence mode.

Verify that every accepted role, model, effort, Agent type, and fork mode is representable
by the live spawn schema. If the exact binding cannot spawn, report the unsupported
surface and ask the Human; do not substitute an inherited parent, alternative model,
effort, Agent type, or fork mode. Record the accepted binding in the project-owned task
or execution record and in the first relevant dispatch contracts.

The binding is valid only for the same local date, unchanged scope, and continuous
execution. Reconfirm it after a local-date change before continuation, when no child ran
before a delayed start, or when scope materially expands. Preserve completed child
provenance when a later binding governs remaining work.

## Separate execution from acceptance proportionally

Require an independent verifier when a change affects executable behavior or tests,
crosses files or modules, touches a public interface, persistent data, security,
concurrency, or deployment, or when the executor reports uncertainty, test failure, or
environment drift. Also require one when the user asks for independent verification.

Allow executor self-checks for spelling, comments, pure documentation, and low-risk
single-file declarative configuration when a deterministic validator or exact comparison
establishes the result. Do not add a verifier merely to repeat the same evidence.

When an approved plan assigns evidence ownership, the executor runs new or modified
tests and the smallest meaningful delta checks; the ticket verifier owns the
authoritative focused or integration suite for that acceptance boundary; and a join
verifier owns the consumer-level proof at a real dependency join. Do not assign the same
unchanged suite to every role. Replay an unchanged surface only for a named trigger such
as shared-code change, dependency evidence, or material uncertainty.

Add an independent reviewer only for public API, permissions, security, migration,
concurrency, compatibility, cross-module design, a large diff that tests cannot cover,
or a concern the verifier cannot resolve. Routine implementation needs verification,
not ceremonial review.

## Bound concurrency

Keep at most three active workstreams by default. Read-only, mutually independent
investigations may temporarily exceed that limit when the parent can still track their
dependencies and return gates. Parallel writers require disjoint ownership; otherwise
partition or serialize them. Do not revert another worker.

## Escalate and fuse repeated failure

A verifier-confirmed bounded code defect returns to the original implementer and then
the original verifier. Rerun the failing regression and directly affected seam before
wider checks. Keep the same route and fuse count; an imperfect first implementation is
not by itself a reason to create fresh threads or escalate capability.

Wrong authority, wrong scope grounding, unauthorized contract changes, or repeated
inability to understand the task is a semantic route failure. For a long execution with
an accepted binding, move directly to its exact semantic-failure route once; do not walk
through intermediate effort levels. Failure of that route opens the fuse and returns to
the main thread or Human. For other implicit work, preserve the contract and move to the
next capable route under the routing priorities above.

A runner, permission, service, container, sandbox, or other environment failure returns
to the main thread for environment handling. It does not change the model route. A
transport failure may retry the same route once.

Count every attempt against the same objective and blocking condition across Agent and
model changes. Permit the initial attempt plus at most two retries. If the second retry
still fails, stop automatic work and ask the user. Reset the count only when new evidence
establishes a different root cause, the user changes scope or acceptance, or the user
chooses a new solution path; prompt changes and model changes do not reset it.

The human escalation packet contains the objective and blocker, all three routes and
results, confirmed evidence, unresolved decisions, two or three viable directions with
risks, and the exact choice required from the user. Do not keep turning the same problem
over after the fuse opens.

## Give every child a complete contract

When an approved ticket exists, project the dispatch contract from that ticket and its
accepted upstream evidence, not from chat memory. The ticket remains authoritative; the
projection cannot add or reinterpret missing authority. Do not duplicate the
`plan-work` field schema here. Confirm that the projection contains the applicable
authority, seam, validation, stop, and recovery information. If any is missing or
contradictory, return to the main thread and planning instead of asking the child to
invent it.

Before spawning, state:

1. objective and observable completion evidence;
2. initial file, module, or behavior boundary without unnecessary micromanagement;
3. decisions reserved for the main Agent;
4. write ownership and tasks that may run concurrently;
5. required validation and rollback evidence;
6. the condition that returns work to its owner;
7. the appropriate soul capsule;
8. the bounded return shape below.

Keep the message self-contained. Put the task ID, one-line objective, and write ownership
first. Do not dump a full specification or assume the child inherited the main
conversation. An empty or mismatched payload is an immediate return condition, not a
reason for the child to invent a task.

## Inject a soul

Generic strong and locked-spec children get the Janitor soul at `souls/janitor.md`;
generic leaf workers get the Mercury soul at `souls/mercury.md`. Both are standalone
files; do not inline them, and a `Soul:` label alone is not evidence of injection.
Role-oriented types already carry a role contract, so do not replace it with a soul;
add only the task-specific scope and acceptance evidence.

Janitor owns a workstream and implements directly, but is not a replacement main session
and must return difficult-and-broad work. Mercury may search, diagnose, modify, and
verify within a clear local boundary. A locked-spec implementer returns ambiguity rather
than resolving it.

## Preflight and reuse execution state

Before child-owned validation fans out in a long execution, the main thread preflights
the project-owned canonical runner once. Record its exact invocation, required
permission or approval, service or container setup, setup owner, reusable state, and
invalidation signal. This does not authorize a fallback runner or bypass project-owned
permissions, approvals, or isolation.

Reuse valid setup across executor, verifier, repair, and join work. A child does not
restart or reauthorize it without evidence that the state is unavailable or invalid.
When sandboxes cannot share setup, record that boundary, keep one setup owner per
runnable context, and minimize repeated startup. Repeat preflight only after evidence of
invalidation or material environment change.

For a long execution, keep compact task-local state in an existing project-owned task,
track, or execution record. If none exists, use a compact recovery block in the
project-approved planning or task location; do not create a universal ledger. Record
only:

- accepted model binding and validity boundary;
- ticket, role, and child-thread identities;
- active, completed, reusable, and unavailable thread state visible to the main thread;
- attempt and fuse state;
- accepted evidence pointers;
- next action and recovery point.

Update it after the first dispatch, each material return or rejection, route escalation
or fuse, and before a known compaction, handoff, or pause. Before creating another child
for the same objective, check this state and reuse the original implementer or verifier
for a bounded defect. Do not infer missing provenance, reset a fuse, or create a
replacement merely because a completed thread is inconvenient to recover. If the
original thread or exact required route is unavailable, preserve its provenance and
follow the model-binding gate or return the work to the main thread.

## Require a bounded return

A child's return — its final message inline, or `result.md` on a board — opens with a
bounded summary: outcome (`pass`, `partial`, or `blocked`); the behavior delta in a
sentence or two; changed paths, with anything outside declared ownership listed
separately as unexpected; validation commands actually run and what they showed; and
material findings and unresolved assumptions, stating `none` explicitly. Supporting
detail follows the summary; exploration narrative and raw transcripts stay out. State
this shape in the dispatch message.

Keep raw exploration, long test output, and full transcripts in child threads or
project-approved evidence locations. Bring only the bounded return and evidence needed
for the active decision into the main thread.

Accept from the summary alone only when nothing fires. An unexpected path, failed or
skipped required validation, a contradiction with the source or another worker, or a
change reaching a public contract, persistent data, security, or anything irreversible
forces reading the actual diff and evidence before acceptance. The summary is an entry
point, never the authority.

## Report the route and result

Before a visible strong route, report the lane, why it fits, its ownership boundary,
expected evidence, and return gate. Keep a leaf announcement brief.

At integration, report which layers ran, accepted evidence and actual validation,
rejected or timed-out child work, and remaining main-thread decisions plus rollback. Do
not paste child transcripts or treat a child's self-review as acceptance.

A child that ignores its soul, stalls past its wait point, or writes outside its
ownership may be interrupted. Preserve the evidence and take over rather than repeatedly
enlarging the prompt.

## Produce requested reports and close out long executions proportionally

For any ticket, an explicit Human request for a report or audit deliverable, such as an
execution report or process audit, creates that durable file automatically. This grants
narrow authority to add only that report; it does not authorize changes to the owning
plan, wayfinder, task state, or any other file. Ordinary status, progress, or result
questions remain chat-only.

A generic execution-report request produces one proportional implementation report. If
delegation occurred, include a proportional delegation/process section in that report.
Produce a separate process audit only when the Human explicitly requests a separate
audit or the long-execution contract below requires one. Trust an approved `plan-work`
artifact for its report content and acceptance contract instead of restating its full
schema here.

Use the first available report destination in this order: the Human-specified path, the
owning plan's path, a project-rule report directory, an existing repository report
directory, then a new `reports/` directory at the repository root. When reconstructing
a report or audit after the work, label the artifact as reconstructed, distinguish
reconstructed evidence from contemporaneous records, and preserve rather than erase or
normalize any process deviation that occurred.

For a long delegated execution, the main thread generates the implementation report and
delegation/process audit declared by the plan before remote publication, a requested
wayfinder update that claims progress or completion, or a formal report or handoff.
Local engineering completion, pauses, compaction, same-day continuation, and ordinary
status messages do not trigger them. A fuse or Human blocker uses the bounded escalation
packet unless one of those durable triggers also fires.

Build the reports from bounded returns, current source and diff, actual validation
evidence, and the dispatch record. The implementation report records execution status
and authority, per-slice outcomes, executor/ticket/join evidence, preserved invariants,
worktree accounting, remaining Human decisions, and recovery point. The process audit
records each dispatch role and exact binding, task, outcome, elapsed time, route and
reuse counts, concurrency, escalation classifications, repeated suites and environment
startup, root-cause attribution, necessary verifier findings, compressible steps, and
limitations.

Point to raw logs, diffs, and receipts instead of copying them. Record token, credit, or
cost values only from native receipts; otherwise write `unavailable`. Children do not
grade their own orchestration, and passing tests or strong models do not automatically
accept tickets. Engineering may be complete while the two reports — and therefore the
triggered publication or wayfinder close-out — remain pending.

## Board protocol

When a child returns results through a filesystem board rather than inline, see
`references/board-protocol.md`. `scripts/session_board.py` enforces it; the reference is
documentation, not a second implementation.

## Lessons

- A close-out obligation held only in the executing Agent's context can be bypassed by a
  later task. Long plans must authorize their report paths and expose the reports as
  completion gates, and a later progress or Done projection must consume those gates.
- Worker-controlled filesystem mtime is not tamper-evident. It may reject an ordinarily
  late completion marker, but it never supplies independent security, authorization, or
  promotion authority.
- A structurally valid return is not a correct one. Workers repeatedly produced
  well-formed output grounded in the wrong authority or scope. Grade transport validity
  and semantic grounding separately.
- Never retry a weak semantic answer. Retry only a transport failure, and only once; a
  semantically weak result is a new dispatch, not a retry.
- Reuse the original implementer and verifier for a bounded defect; fresh routing is for
  semantic grounding failure, not ordinary repair.
- Treat role/type fields as optional live-schema capabilities. A role contract belongs
  in the task even when the current spawn surface exposes only model, effort, and fork.
- When a managed Agent or profile reports unavailable, do not infer that its model is
  unavailable. Inspect the profile/provider binding and, for an implicit route, isolate
  the layers with a live-schema-supported generic type plus the same model override. A
  successful probe proves only that exact route; an explicit user-selected profile still
  requires reporting the failure and waiting for direction.
