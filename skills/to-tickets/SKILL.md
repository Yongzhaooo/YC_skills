---
name: to-tickets
description: >-
  Use when you have an approved spec and need to decompose it into executable
  tracer-bullet tickets. Each ticket is a narrow vertical slice with clear
  blocking edges, sized for one subagent session.
---

# To Tickets

Turn an approved specification into small, end-to-end, verifiable work slices.
Each slice is a ticket — a single subagent-sized task that demonstrates real
behavior through the full stack.

Tickets are not GitHub issues. They are lightweight planning nodes in a
repository-local plan file. Each one is narrow enough for one MEDIUM subagent
session (~30 min), wide enough to show working behavior.

This skill is invoked with the `/to-tickets` command. It publishes a plan only.
It never starts implementation.

## Read the spec

Read the approved spec end to end. Also read:

- `AGENTS.md` for repository conventions
- Current task state and task tracking files
- Relevant existing code, tests, and schemas

If the spec has open decisions that block decomposition, stop and flag them
to the user. Don't guess.

## Draft vertical slices

Decompose into **tracer-bullet tickets**. Each ticket must be:

- **A vertical slice** — cuts through all layers (schema, logic, UI, test) to
  demonstrate one complete behavior. No "all types" or "all backend" layers.
- **Demoable on its own** — produces something you can show, run, or verify
  without finishing other tickets.
- **Subagent-sized** — fits in one MEDIUM subagent session (~30 min). The
  orchestrating agent (HIGH) manages sequence and context handoff, not
  implementation.

Design blocking edges carefully. Prefer genuine technical dependencies over
sequencing convenience. If two tickets could reasonably be done in either
order, make them parallel.

### What not to ticket

- **Horizontal layers** ("Implement all API types", "Write all tests") — these
  hide dependencies and force big-bang integration. Split into vertical slices.
- **Refactoring without behavior change** — fold it into the ticket that needs
  the new structure.
- **Research or exploration** — do that before the spec is approved, or make
  it an explicit spike ticket with a timebox.
- **Setup, config, tooling** — fold into the first ticket that needs it, or
  make it a single discovery ticket at the front.

### Each ticket contains:

```
## T1: <verb phrase — e.g., "Display empty state when no items exist">

**Blocked by:** <ticket IDs or "none">
**What it delivers:** <one-sentence outcome>
**Acceptance criteria:**
- <concrete, testable condition>
- <concrete, testable condition>
```

- **T1, T2, T3** — stable IDs scoped to this plan
- **Blocked by** — only real technical or authority dependencies. Leave blank
  ("none") for tickets that can start immediately.
- **What it delivers** — the observable outcome, not the implementation steps.
  One sentence. If it needs paragraphs, the ticket is probably too big.
- **Acceptance criteria** — 2-4 verifiable conditions. Each one must be
  testable by a subagent or the orchestrator without subjective judgment.
  No "works correctly" or "is robust" — those are not tests.

## Review with the user

Present the full ticket set to the user. Ask about:

- **Granularity** — are any tickets too big (split) or too small (merge)?
- **Blocking edges** — are the dependencies correct?
- **Order** — should any tickets move between parallel and serial?

Iterate until the user approves the structure.

## Publish

Write the approved plan to `plans/<YYYY-MM-DD>-<slug>.md`. Include:

- Spec path and title
- Full ticket list with IDs, blocked-by edges, deliverables, and acceptance
  criteria
- A short dependency diagram in plain text, e.g.:

  ```
  T1 (none) ──> T2 ──> T4
             └─> T3 ──> T5
  ```

Report the plan path and ticket count to the user. Stop — no implementation.
