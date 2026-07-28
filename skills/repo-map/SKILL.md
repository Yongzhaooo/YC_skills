---
name: repo-map
description: Use when locating files, exact text, symbols, callers, or project knowledge in unfamiliar, multi-file, repository-wide, or architecture-sensitive work, and an agent must identify owners, execution paths, and change boundaries before implementing.
---

# Repo Map

Build a compact repository map before implementation.

Read applicable repository instructions first. Repository-local authority, retrieval,
sensitivity, and maintenance rules override this generic policy.

Narrow root, glob, file type, and symbol context before reading broad results. **If a
route produces no new evidence, switch to a materially different route** instead of
repeating a wider version of the same search.

Treat a stale or inconsistent project index as degraded. Exact or full-text evidence may
remain usable with its warnings, but do not claim semantic retrieval is healthy.

Map:
- Entry points and user/system triggers.
- Owning files and symbols.
- Call chain or data flow through boundary layers.
- Shared abstractions that amplify blast radius.
- Existing tests and verification commands.
- Unknowns and the fastest check for each unknown.

Return:
- Primary owning path in order.
- Critical files/symbols by layer.
- Risky branch points and side effects.
- Proposed write boundary for implementation.
- Verification surface.

Stay in mapping mode unless the user has already asked for implementation.
