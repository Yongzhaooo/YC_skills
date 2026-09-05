---
name: codebase-design
description: Shared vocabulary and decision tests for designing deeper modules, choosing useful seams, and improving interface-level testability.
---

# Codebase Design

Prefer modules that hide meaningful behavior behind a small, stable interface. Use the
terms below when they clarify the design; repository and domain vocabulary still wins.

## Working vocabulary

- **Module** — something with an interface and an implementation, at any scale.
- **Interface** — everything callers must know: operations, inputs, invariants, failure
  modes, ordering, configuration, and relevant performance constraints.
- **Implementation** — behavior hidden behind the interface.
- **Depth** — useful behavior delivered per unit of interface a caller must understand.
- **Seam** — a place where behavior can vary without editing its consumer.
- **Adapter** — an implementation selected at a seam.
- **Leverage** — one interface serving multiple callers or use cases.
- **Locality** — related behavior, change, and verification concentrated in one place.

These words are a shared lens, not a ban on ordinary terms such as API, service,
component, or boundary when those are the repository's natural language.

## Decision tests

- **Deletion test:** if deleting a module makes its complexity reappear across callers,
  it was hiding useful behavior; if the complexity disappears, it was likely shallow.
- **Interface test:** callers and most tests should succeed through the same public
  surface. Reaching through it repeatedly suggests the seam is misplaced.
- **Variation test:** introduce an adapter seam for real variants, not a speculative
  future need. A production implementation plus a meaningful test substitute may count
  as real variation.
- **Dependency test:** accept dependencies or otherwise expose a controllable seam when
  construction would make behavior hard to test.
- **Outcome test:** prefer returning observable results over forcing callers to inspect
  internal state.

Depth is not a line-count ratio. A large implementation is useful only when it reduces
what callers must coordinate and learn.

For dependency-specific guidance, read [DEEPENING.md](DEEPENING.md) only when the chosen
candidate crosses an in-process, local-substitutable, owned-remote, or external seam.
Explore multiple interface designs when the decision is consequential; parallel agents
are optional, not the method itself.
