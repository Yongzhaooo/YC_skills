---
name: improve-codebase-architecture
description: Inspect a codebase for concrete opportunities to deepen modules, reduce leaky interfaces, and improve testability; return prioritized candidates without changing code.
disable-model-invocation: true
---

# Improve Codebase Architecture

Find architectural friction that is active in the codebase, then propose the smallest
useful deepening opportunities. Use `codebase-design` as vocabulary, not as a compulsory
terminology filter.

## Scope

Honor a subsystem or pain point named by the user. Otherwise use recent changes,
frequently touched paths, failing tests, or repeated caller friction to choose a bounded
area. Read applicable repository guidance and relevant decisions before proposing a
change.

Inspect directly. Delegate only when an independent or parallel repository sweep has
clear value under the active delegation policy.

## Look for evidence

- callers repeating orchestration or domain rules;
- interfaces nearly as complex as their implementations;
- pass-through modules whose removal would not reveal hidden complexity;
- coupling that makes one behavior require scattered edits;
- tests forced to reach past the public interface;
- a seam justified by real variation rather than a hypothetical future adapter.

Apply the deletion test: if removing a module merely spreads its complexity among
callers, it may be earning its keep. If the complexity disappears, it is probably
shallow.

## Return candidates

For each candidate report the affected files, concrete friction, proposed interface or
ownership shift, expected locality/test benefit, risks, and confidence. Rank the
candidates and identify the best first move.

Use concise prose by default. Create diagrams, HTML, or another visual only when it
materially improves understanding or the user asks for it. Do not edit domain glossaries,
ADRs, or production code during this review. After the user selects a candidate, use the
repository's normal decision and planning workflow.
