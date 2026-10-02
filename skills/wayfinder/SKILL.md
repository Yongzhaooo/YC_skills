---
name: wayfinder
description: Report project status or resume a selected task from docs/wayfinder.md, including where a long-running outcome stands and whether its route still holds. Maintain its recovery pointers when authorized work changes state. Status-only requests stay read-only; the map is not a backlog or review log.
---

# Wayfinder

Use `docs/wayfinder.md` for the project outcome, where it stands, the current focus,
recovery points, selected next work, and conditions that change what to do next.
Details belong in linked owner artifacts. Review suggestions stay there until selected
as work. A short task can be a few sentences; expand only the stage being executed.

## Orient or resume

1. Read the map; if absent, report that rather than creating one.
2. For status, report as described in Report for the reader. For a selected task, follow
   only its relevant recovery links and decisions.
3. Flag drift: duplicate entries, missing recovery evidence, a summary that conflicts
   with its owning evidence, entries that carry evidence dumps instead of state, and
   history that no longer affects recovery or selection. A map lacking the newer fields
   stays readable; missing format alone is not drift. Check current owning evidence
   before resuming or claiming completion; a draft or historical spec does not prove
   approval, execution, or deployment. Report conflicts rather than guessing.
4. If the user is choosing work, keep claimed work visible but recommend by the current
   focus and outcome; an earlier claim is not permanently the highest priority. Await
   selection. Resume an already selected, authorized task without asking them to choose
   again. A status-only request ends with the report and any proposed drift correction,
   without editing.

Entering the map, having a next step, or time passing grants no execution authority.
Return material changes to the outcome, scope, or commitments to the user.

## State contract

Preserve these headings for existing maps and Board consumers; omit empty sections.
Place the inline fields before the first `##` heading with a blank line after each;
Board reads the outcome until the first blank line or heading.

- `**Project outcome:**` — the durable result and what counts as done. For ongoing
  maintenance, state the service goal and the result this round can finish; do not
  invent an end date for the whole project.
- `**Current answer:**` — a short summary of where the outcome stands: results reached,
  key gaps, what the claim rests on, and an as-of date where timing matters. It may link
  owning evidence directly rather than only the entries below.
- `**Current focus:**` — the result this round seeks, why it was chosen, when it counts
  as done, and what change would require rethinking the route, in one paragraph.
- `## Milestones` — optional, for multi-stage work, before the task sections: results
  and gaps that still affect the current judgment. A milestone stays while it shapes the
  route, even after its tasks leave Done.
- `## In progress` — claimed unfinished work: `**name** — running|paused;
  resume: <checkable recovery point>; next: <concrete step>`. Running means executing;
  paused retains the claim across sessions.
- `## Next actions` — unclaimed near-term work selected by the user or current owning
  plan, with an outcome and entry point.
- `## Waiting` — selected work awaiting a decision, evidence, or dependency. Retain its
  recovery point and name the clearing condition and known supplier. Move the task here
  rather than duplicating its In-progress entry.
- `## Watching` — an observable condition, evidence source, and action its change would
  trigger. This does not launch a monitor or collect unprioritized debt.
- `## Done (rolling)` — verified outcomes still needed for handoff; at most three by
  default unless the project specifies another bound.

Task entries carry resumption; Current answer and Milestones carry the overall judgment.
Read legacy Destination, Live, Ready to pick up, and Blockers headings; classify affected
entries when updating them. Monitoring-only Live items need a real Watching trigger.
Record resumable work before recovery context can be lost. A pilot points to its
pilot.md, which owns its lifecycle and result. Never clear a claim merely because an
app session is absent or time has passed; use owning evidence or an explicit decision.

## Report for the reader

A status or resume report answers the user's question, not the map's layout.

1. Open with a sentence that answers the question; for general status, start from where
   the outcome stands. Then add the goal, stage, and task context the question needs.
2. Organize by the reader's questions (for example "Is the root cause known?", "Is it
   fixed upstream?"), not by map headings or chronology. Choose tables, sections, and
   term explanations by reading need, not by item count.
3. Explain each item's role toward the outcome. Call items critical-path or side work
   only when the outcome and dependency evidence support it; otherwise say it is unknown.
4. Follow only the evidence that bears on the question or selected task. Keep verified
   facts, inferences, and unknowns distinguishable. Give each state's source and date;
   reading or editing today does not refresh it, and a record read today is not live
   state. When a summary conflicts with its owning evidence, report the conflict.
5. Introduce project-specific components or identifiers by their role at first mention.
6. End with the decision or next step that is actually open. Do not restate evidence
   the owners hold or reargue settled choices.

Length follows the question; a narrow question gets a short answer.

## Reassess the route

When a task ends, a key assumption fails, an external dependency changes, or an agreed
budget runs out, judge whether the stage is complete and whether the next step still
makes sense. Judge a stage by its done condition and evidence, not by ticked tasks.
If new evidence undermines the route, propose an evidence-based change instead of
continuing the old plan mechanically.

When the current task is waiting, look for independent work that is already authorized
and can advance; keep the waiting task's recovery point. Link settled choices to the
plan or decision holding their rationale and reopen condition; no separate ADR is
required, and do not reopen them unless that condition is met. When external state is
unknown, say it needs checking: "no record of merge confirmation" does not mean "not
merged".

## Choose the next entrance

Choose only what the selected task's unresolved question needs:

- Reasoning/clarity of a proposed approach: proposal-review.
- Rigorous long-term architecture or subsystem design: maintainer-review, on design or patch.
- Feasibility evidence: run-pilot when an experiment is authorized.
- Durable planning or behavior specification of settled choices: plan-work.
- Existing patch: code-review; complexity alone: ponytail-review.
- Sufficiently clear, already-authorized work: continue directly.

These are navigation hints, not a pipeline; use available capabilities when a named
skill is absent. Use grilling only for an explicitly requested exhaustive interview.

## Maintain

During authorized work, update on changed state, recovery point, or watched condition.
Reread immediately before editing; replace or move the affected entry instead of adding
progress notes, and replace any current conclusion the change affects, checking the
related Current answer, focus, and milestones. A small change does not trigger a
project-wide reinvestigation; status queries never write.

Keep one entry per task, normally one or two lines: its role toward the outcome when
that is not obvious, present state, next action/trigger, and a link to its owner. Keep
the minimum detail that still affects recovery or selection; leave sample counts,
message or boot IDs, delivery receipts, command results, and dated history in the
owner. A still-valid recovery baseline, such as a device's restore state, may stay even
outside the standard sections. Clear blockers and claim completion only against the
owning artifact's gates and evidence.

Retain entries that enable a current recovery or selection decision. Remove superseded
pointers after checking their owners, preserving unresolved claims. Prune Done once its
evidence is retained in existing records. Do not delete source artifacts or create an
archive/ledger for each pass. Broader map cleanup is a separate requested task.
