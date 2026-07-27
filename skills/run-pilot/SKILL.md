---
name: run-pilot
description: Use when you want quick evidence before committing to a full design or rollout. Creates a minimal isolated experiment with clear pass/fail criteria. For single-turn checks use a conversation-only card; for cross-session work use pilot.md.
---

# Run Pilot

Turn an agreed hypothesis into the smallest isolated implementation that can produce useful evidence. Implement and verify the pilot, then stop at the evidence or authority gate.

Do not turn the pilot into a miniature specification or ticket program. Never auto-promote or auto-invoke a downstream skill.

## Decide whether the work is a pilot

Proceed when **all** of these are true:

- one main hypothesis or feasibility question is identifiable;
- inputs and observable outcomes can be frozen;
- the work can be isolated, reverted, or discarded without production migration;
- success and failure can be distinguished with a bounded test;
- the user wants evidence before committing to a durable design or rollout.

Stop and recommend a different workflow when the work requires unresolved product choices, destructive data changes, public API migration, broad cross-team coordination, production rollout, or a multi-lane dependency program.

## Choose the brief form

| When | Form |
|------|------|
| Genuinely single-turn check, no tracked writes, no cross-session recovery | **Conversation-only Pilot Card** — state the core fields inline, no file |
| Cross-session work, tracked writes, or recovery needed | **`pilot.md`** — durable resume entrypoint in the working directory |

Keep `pilot.md` concise and mutable. It is the cross-session resume index, not a second specification, task tracker, raw log, or evidence store.

## Core fields template

Recover these fields from the request, conversation, or working directory:

```text
Hypothesis:
Control / current behavior:
Treatment / candidate behavior:
Frozen inputs and leakage boundary:
Allowed writes and explicit non-goals:
Budget (time, cost, files, model calls):
PASS criteria:
FAIL criteria:
INVALID criteria (protocol / leakage / execution failure):
Hard stop condition:
Evidence preserved at:
```

If a field is already explicit, state it briefly and proceed. Ask only when a missing decision would materially change behavior, authority, cost, or interpretation.

## Implement the smallest discriminating pilot

1. Freeze input identities (paths, hashes) before observing results.
2. Bind control and treatment so only the intended variable differs.
3. Choose the smallest vertical seam that can distinguish the hypothesis from a plausible alternative.
4. Keep candidate behavior experiment-local. Avoid live-skill, production-config, public-interface, or canonical-data changes.
5. Preserve raw evidence before summarizing it.

If the first implementation cannot answer the hypothesis, classify it `INVALID` or `WEAK`. Do not expand without a new user decision.

Retry only infrastructure, transport, or schema-invalid executions. Do not rerun a structurally valid result because it is disappointing. Stop when the budget or hard-stop condition is reached.

## Classify the result

Use exactly one primary result:

- **PASS**: pre-registered evidence supports continuing to a broader validation or design step;
- **WEAK**: useful evidence but supports only one bounded revision or retest;
- **FAIL**: treatment did not justify expansion under the agreed criteria;
- **INVALID**: protocol, leakage, execution, or evidence failure prevents semantic interpretation.

## What to do after each result

| Result | Next step |
|--------|-----------|
| PASS | Recommend the smallest justified next action — a second pilot, `plan-work`, or handoff. |
| WEAK | Propose one bounded revision or retest to the user. |
| FAIL | Stop. Report findings and recommend against the approach. |
| INVALID | Report the failure mode. Propose a corrected pilot if the hypothesis is still sound. |

## Stop rules (never auto-promote)

A pilot result never automatically authorizes:

- production rollout or live workflow replacement;
- rule, skill, model, or configuration promotion;
- data or schema migration;
- additional model calls or a larger experiment;
- creation of a full spec, tickets, commit, push, or pull request;
- invocation of a downstream skill.

Stop at the evidence gate. Report the hypothesis, primary result, what was implemented and where, actual validation outcomes, budget consumed, known limitations, and exact stop point. Then yield to the user.
