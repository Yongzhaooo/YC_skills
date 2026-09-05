---
name: wayfinder
description: Orient or resume a multi-session project from docs/wayfinder.md by reporting claimed work, recovery points, blockers, and unclaimed next actions without starting execution.
---

# Wayfinder

Answer "where am I on this project?" from one file: `docs/wayfinder.md`. It holds the
project outcome, claimed work and its recovery point, unclaimed next actions, waiting or
watched conditions, and recent outcomes. Detailed truth lives in the artifacts it points
at — specs, pilots, skills, and knowledge notes — not here.

## Orient

1. Read `docs/wayfinder.md`. If it does not exist, say so and offer to create it; do not
   invent one silently.
2. Report, in this order: the project outcome; every **In progress** item with its status,
   resume point, and immediate next step; **Waiting** items and their blockers; unclaimed
   **Next actions**; then watched or recently completed items only when they change the
   picture.
3. Treat an item appearing in both **In progress** and **Next actions**, or an In-progress
   item without a checkable resume point, as map drift. Say so rather than guessing.
4. Follow a reference only when the current question needs it. Do not read every linked
   artifact by default.
5. Recommend resuming claimed work before suggesting a new action. Give a one-line reason
   for each viable choice, then wait for the user to choose.

## State contract

Use these headings in new or updated maps:

- `**Project outcome:**` — the durable result the project serves.
- `## In progress` — work already claimed and not yet closed. Each line uses
  `**name** — running|paused; resume: <checkable artifact or recovery point>; next: <one
  concrete step>`. `running` means execution is underway; `paused` means the claim and
  recovery point remain valid across sessions.
- `## Next actions` — useful work that no session has claimed yet. "Next" means safe to
  start after the user chooses it; it does not mean started, approved for side effects,
  or higher priority than claimed work.
- `## Waiting` — claimed or desired work that cannot advance until the named evidence,
  decision, or dependency arrives.
- `## Watching` — a condition worth monitoring with no current execution claim.
  Also the home for low-priority, non-blocking technical debt: known issues
  recorded in a durable place (e.g. `docs/open-issues.md`) that are neither
  urgent enough for `Next actions` nor blocked enough for `Waiting`. Watch
  items are surfaced on orient, not actively pursued.
- `## Done (rolling)` — recent evidence-backed outcomes.

An empty section is valid and may be omitted. For compatibility, read `Destination`,
`Live`, `Ready to pick up`, and `Blockers`, but when editing classify each legacy entry
into the new headings. `Live` is not automatically In progress: move monitoring-only
entries to **Watching**.

When a multi-session project or resumable pilot starts, write or move its line into
**In progress** before the session can lose its recovery context. A running pilot points
to its `pilot.md`; that file owns the pilot lifecycle and result, while Wayfinder only
mirrors the current resume point. A new session must not clear or downgrade the line
because no matching app session is visible. Move it only on owning-artifact evidence or
an explicit user decision.

## Common entrances

After the report, if the user picks an action, the usual chain is: `grilling` when
decisions are still open → `plan-work` to write the spec and slice it → implement ticket
by ticket → `run-pilot` first whenever feasibility itself is the question. Suggest the
step that matches where the chosen action actually is; never start it unasked.

## Boundaries

- **Do not invent work.** "There are no unclaimed next actions" is a valid, useful answer.
- **Do not start execution.** Stop after the report. Choosing an entrance, opening a
  session, or invoking another skill is the user's next move.
- **Do not move blockers.** A blocker clears on a user decision or concrete evidence, not
  because the situation looks better.
- **Do not infer ownership from app sessions.** Session presence may corroborate a map
  line; absence never makes a durable execution claim disappear.
- Owning artifacts win conflicts. If a spec contradicts the map, the spec is right and
  the map line is stale.

## Update

Update `docs/wayfinder.md` when something concrete is learned — work was claimed, paused,
blocked, resumed, or finished; a recovery point moved; or a watched condition changed.
Reread the file immediately before editing, change only the affected lines, and keep each
entry to one or two lines. Move finished items into **Done (rolling)** with a one-line
outcome and drop the oldest entries once they stop being useful.

Before writing a progress claim or moving work into **Done (rolling)** in
`docs/wayfinder.md`, read the owning artifact's declared completion gates and require
their evidence.

Every line should point at something checkable. If you cannot name the evidence, do not
write the line.

**Drift check:** when the report and reality disagree — an In-progress item is actually
finished, a resume point moved, or a blocker no longer holds — say so explicitly and
propose the one-line correction in the same turn. A stale map that keeps being trusted is
worse than no map.

## Lessons

- Earlier versions charted the whole project and readers drowned; the value is in live
  work, blockers, and the next safe entrance, not in completeness.
- Do not build a domain router or a shard schema. The project's own artifacts already own
  their structure — this file only routes to them.
- `Live` mixed actively owned work with long-term monitoring, so a new session could not
  tell whether to resume or merely observe. Use **In progress** only for a durable claim
  with a resume point; put monitoring-only state in **Watching**.
- Low-priority tech debt is not a next action and not a blocker. Give it a
  durable home (`docs/open-issues.md`) and a `Watching` line, so it surfaces on
  orient without claiming execution or crowding the real next steps.
