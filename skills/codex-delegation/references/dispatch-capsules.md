# Dispatch capsules

Use these examples when a child cannot understand an assignment from a short brief.
The message itself is the capsule. Omit irrelevant fields; retain facts that affect
correctness, authority or acceptance. Concrete model bindings live in routing config.

## Execution or investigation

```text
Role/outcome: [implement, investigate or review] [one observable result].
Why/current state: [parent goal and why this result is needed].
Known: [verified facts and settled decisions]. Unknown: [open questions].
Inputs: [working directory; relevant instructions; source paths/sections/symbols;
necessary excerpts; accepted upstream findings; environment/check commands].
Boundary: read [scope]; write [paths or none]; preserve [behavior/contracts].
Exclude [non-goals]. Parent owns [reserved decisions]; concurrent work is [scope].
Acceptance: [observable evidence]; validate with [focused command and expectation].
Stop: return needs_context before dependent work if [missing fact or decision];
return blocked/partial with evidence if execution cannot complete. No wider search,
implementation, external effects or additional agents outside this assignment.
Return: status, result with source references, changed paths, actual checks/results,
unknowns and recovery point. Report completion or a blocker without being prompted.
Route: [model, effort, required skill; existing mode if applicable]; leaf only.
Timing: [estimated window]; [event wait/poll budget].
```

A hypothetical economical-worker brief, with actual paths filled in at dispatch:

> Investigate why the export command drops empty labels. This is evidence gathering
> for a compatibility fix; write nothing. The user requires empty strings to survive
> export, while a missing key must remain omitted. A fixture reproduces the loss; the
> suspected normalization step is a hypothesis. In the named checkout, read the export
> handler, its serializer and the specified fixture/test; run the existing focused test.
> Return the first point where the values become indistinguishable, cite the symbol and
> relevant output, and distinguish a proven cause from a suspicion. Do not change the
> schema, inspect unrelated modules or fix the issue. If the cause leaves this reading
> boundary, identify the next dependency and return needs_context. The parent owns the
> fix and compatibility decision. Include the route, leaf rule and timing line above.

For a writer, additionally state the settled behavior, allowed implementation/test paths
and expected edge cases. A read-only agent may run checks only within the assigned side
effect boundary; existing tests do not imply permission to mutate a live service.

## Expert consultation

```text
Advise read-only on this decision: [precise question]. The parent will decide and implement.
Goal/constraints: [user outcome; compatibility, data, performance or operating constraints].
Current design: [relevant components and producer/consumer relationships].
Evidence: [verified observations with paths/excerpts; prior attempts and their results].
Options considered: [alternatives and why each is plausible; open to a better option].
Unknowns: [facts not yet established; assumptions that must remain conditional].
Read scope: [sources/tools]; writes: none. Do not contact others or delegate.
Return: recommendation and rationale, strongest counterargument, evidence, uncertainty,
and the smallest discriminating check. State what would change your recommendation.
Route/timing: [explicit advisor model/effort; estimated window; waiting policy].
```

An architecture question should name a real tradeoff, such as whether a transaction
boundary belongs in the caller or storage module, and supply the current call path,
consistency requirement and failing case. "Review our architecture" gives neither an
answer boundary nor enough information to judge it.

## Follow-up and acceptance

A related follow-up can be a delta: "The serializer finding is accepted; the earlier
missing-key hypothesis is rejected by this fixture. Preserve the existing API. Implement
the stated fix only in these two files and run this regression. Other ownership and
stop conditions are unchanged." Include the new evidence; do not say only "continue".

An explicit bounded model/effort assignment needs no mode label. Do not turn the route
line in a capsule into an extra user question; unspecified orchestration uses the configured
default route. The economical long-running route requires an explicit user selection.

Accept against the source and required evidence. Begin with the compact result; inspect
the relevant diff, source section or log when needed, then widen to the full authority
for contradictions, missing evidence or consequential contracts. A confident summary
is not proof, and extra review effort is not a reason to repeat unchanged checks.

## Historical framework and external references

The local framework comes from historical MyAgents designs on ticket context capsules
and capsule-informed planning and delegation. Those designs established context compression in both directions, source recovery,
parent-owned decisions, and review that expands when evidence calls for it. Current
policy supersedes their retired model-binding gates, mandatory hashes, ledgers and
repair loops. Capsules project existing authority; they never create it.

External material consulted on 2026-09-23 (conceptual references; no code, templates,
plugins or dependencies imported):

- [Superpowers implementer prompt](https://github.com/obra/superpowers/blob/5bf4e78011075bcfc0dc295f0724994cd123ee71/skills/subagent-driven-development/implementer-prompt.md),
  revision `5bf4e78011075bcfc0dc295f0724994cd123ee71`, MIT. Useful concepts: scene-setting,
  leaf-only workers, and a distinct missing-context return. Local policy retains
  parent-owned failure recovery and proportional verification; its automatic commits,
  report files and review workflow are not adopted.
- [LangGraph Supervisor](https://github.com/langchain-ai/langgraph-supervisor-py/blob/88859b34017ac3569bbd4a3092c7e77593a0a960/README.md),
  revision `88859b34017ac3569bbd4a3092c7e77593a0a960`, MIT. Useful concepts: customize the
  handoff context and separately select the worker output entering supervisor history.
  Its README recommends direct tool-based supervision for most uses. Local policy uses
  native tools and compact evidence; full-history handoff and recursive teams are not defaults.
- [OpenAI subagent guidance](https://learn.chatgpt.com/docs/agent-configuration/subagents)
  supports scoped prompts, independent work and deliberate model/effort selection.
  Availability and fork constraints must still come from the live host schema.

These references inform locally authored guidance. The current skill and routing
configuration remain authoritative; reading the linked projects is not a dispatch step.
