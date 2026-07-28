---
name: wayfinder
description: Orient a multi-session project by reading docs/wayfinder.md and reporting live work, blockers, and safe next entrances without starting execution.
---

# Wayfinder

Answer "where am I on this project?" from one file: `docs/wayfinder.md`. It holds the
Destination, what is live, what is ready to pick up, and what is done. Detailed truth
lives in the artifacts it points at — specs, skills, knowledge notes — not here.

## Orient

1. Read `docs/wayfinder.md`. If it does not exist, say so and offer to create it; do not
   invent one silently.
2. Report, in this order: the Destination, live work and what each is blocked on, the
   entrances that are ready to pick up, and anything recently done that changes the
   picture.
3. Follow a reference only when the current question needs it. Do not read every linked
   spec by default.
4. Recommend entrances with a one-line reason each, then wait for the user to choose.

## Common entrances

After the report, if the user picks an entrance, the usual chain is: `grilling` when
decisions are still open → `plan-work` to write the spec and slice it → implement ticket
by ticket → `run-pilot` first whenever feasibility itself is the question. Suggest the
step that matches where the chosen entrance actually is; never start it unasked.

## Boundaries

- **Do not invent work.** "Nothing is ready to pick up" is a valid, useful answer.
- **Do not start execution.** Stop after the report. Choosing an entrance, opening a
  session, or invoking another skill is the user's next move.
- **Do not move blockers.** A blocker clears on a user decision or concrete evidence, not
  because the situation looks better.
- Owning artifacts win conflicts. If a spec contradicts the map, the spec is right and
  the map line is stale.

## Update

Update `docs/wayfinder.md` when something concrete is learned — a track became blocked or
unblocked, a recovery point moved, work finished, a new track started. Reread the file
immediately before editing, change only the affected lines, and keep each entry to one or
two lines. Move finished items into **Done (rolling)** with a one-line outcome and drop
the oldest entries once they stop being useful.

Before writing a progress claim or moving work into **Done (rolling)** in
`docs/wayfinder.md`, read the owning artifact's declared completion gates and require
their evidence.

Every line should point at something checkable. If you cannot name the evidence, do not
write the line.

**Drift check:** when the report and reality disagree — a Live item that is actually
finished, a blocker that no longer holds — say so explicitly and propose the one-line
correction in the same turn. A stale map that keeps being trusted is worse than no map.

## Lessons

- Earlier versions charted the whole project and readers drowned; the value is in live
  work, blockers, and the next safe entrance, not in completeness.
- Do not build a domain router or a shard schema. The project's own artifacts already own
  their structure — this file only routes to them.
