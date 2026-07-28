---
name: run-pilot
description: Run a small, bounded, reversible experiment to get evidence before committing to a design or rollout, with a resumable pilot.md.
---

# Run Pilot

Turn an agreed hypothesis into the smallest isolated implementation that can produce
useful evidence. Implement it, verify it, then stop at the evidence. Do not let the pilot
grow into a specification or a ticket program.

## Is this a pilot?

Proceed when all of these hold: one main hypothesis or feasibility question is
identifiable; inputs and observable outcomes can be frozen; the work can be isolated,
reverted, or discarded without a production migration; success and failure can be
distinguished by a bounded test; and the user wants evidence before committing.

Stop and recommend something else when the work needs unresolved product decisions,
destructive data changes, a public API migration, or a production rollout. An existing
spec is not a reason to refuse a pilot — consume only the slice you need.

## The Pilot Brief

Before changing anything, locate an existing `pilot.md` or create one from
`assets/pilot-template.md` — under `reports/experiments/<pilot-id>/`, or whatever
convention the repository already uses. A single-turn check with no tracked writes needs
only a conversation-only Pilot Card.

`pilot.md` is the durable resume document: a new session should continue from it without
replaying finished work or rereading the conversation. Keep it concise — it is not a
second spec or an evidence store. Keep raw outputs and receipts beside it and link them.

Recover the hypothesis, control, treatment, frozen inputs, allowed writes and non-goals,
budget, PASS/WEAK/FAIL/INVALID criteria, hard stop, and resume point. If they are already
explicit, state them briefly and proceed — do not make the user reconfirm settled
decisions. Status and result are separate fields: lifecycle (`ready`, `running`,
`evaluated`, `stopped`) says where the pilot is; result (`pending`, `PASS`, `WEAK`,
`FAIL`, `INVALID`) says what it found. When a source spec exists, record its path and the
git commit and name the exact sections the pilot consumes; an approved spec does not by
itself authorize paid calls, production changes, or anything else separately gated.

## Pre-register the evidence seam

Before observing any treatment result:

1. Freeze the inputs and note their identities.
2. Bind control and treatment so only the intended variable differs.
3. Record leakage exclusions and denied inputs.
4. Define the minimum output needed to evaluate the hypothesis.
5. Define what counts as an execution-invalid run, and the retry rule for it.
6. Record the cost, call, time, or file budget.

Write this into `pilot.md` before running anything. That is the whole point: a criterion
chosen after seeing the result is not a criterion.

## Implement and run

Choose the smallest vertical seam that can distinguish the hypothesis from a plausible
alternative. Keep candidate behavior experiment-local; avoid live-skill,
production-config, or canonical-data changes, and preserve unrelated user changes in a
dirty worktree. Preserve raw evidence before summarizing it. Do not weaken tests,
hard-code the expected verdict, or use the treatment output as its own answer key.

Retry only infrastructure, transport, or schema-invalid executions, under the rule you
pre-registered.

- **Do not rerun a structurally valid result because it is disappointing.**
- **Do not tune thresholds after revealing treatment results.**

Stop when the budget or a hard-stop condition is reached. Update `pilot.md` after each
meaningful state transition and at the final handoff.

### Canary iteration rule

When a canary or disposable pilot fails on format, schema, or trivial protocol issues
(control characters, hash format, field naming, line-ending normalization), fix the
template or request in place and retry the same run. Do not create a new pilot ID or
evidence receipt for a format-only failure — start a new trial only when the hypothesis,
model, or substantive protocol changes. Keep the format failure in the pilot directory as
evidence, but do not let it multiply the iteration count: it is not a semantic result.

## Classify the result

Exactly one primary result:

- `PASS` — the pre-registered evidence supports a broader validation or design step;
- `WEAK` — useful evidence, but it supports only one bounded revision or retest;
- `FAIL` — the treatment did not justify expansion under the agreed criteria;
- `INVALID` — protocol, leakage, or execution failure prevents any semantic reading.

Separate confirmed facts from inference. Report control/treatment differences,
regressions, resource use, and what remains unverified.

## Stop instead of promoting

A pilot result never by itself authorizes rollout, promotion, migration, a larger
experiment, a spec, tickets, or a commit. Do not edit the source spec to make it agree
with the pilot — record the contradiction and propose a spec review instead.

For `PASS`, recommend the smallest justified next action. `plan-work` is right only when
durable contracts now need writing down; a second pilot is often the better next step.

The final report states: hypothesis and result, what was implemented and where, the
validation commands actually run and their outcomes, budget consumed, the exact stop
point, and known limitations.

```text
Use $run-pilot to prototype the parser behind a feature flag on frozen fixtures, run
focused tests, and do not change the production entrypoint.
```

## Lessons

- The brief must scale with recovery risk. A uniform full template for a single-turn
  check is burden without benefit; a resumable multi-session pilot needs every field.
- Format-only canary failures were being recorded as trial evidence and inflating
  iteration counts. They are not results — hence the canary iteration rule above.
