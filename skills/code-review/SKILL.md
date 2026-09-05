---
name: code-review
description: Review changes since a commit, branch, tag, or merge-base against repository standards and the originating specification, and report actionable findings without editing the code.
---

# Code Review

Review a fixed diff along two independent axes:

- **Standards** — documented repository rules and clear maintainability defects.
- **Spec** — missing, incorrect, or unrequested behavior relative to the owning issue,
  design, or user request.

The axes are separate perspectives, not a requirement to spawn separate agents.
Use an independent reviewer only when the user asks or the risk justifies it.

## Establish the review boundary

1. Resolve the fixed point supplied by the user. If none is given, use the repository's
   documented review base; ask only when no safe base can be inferred.
2. Inspect `git diff <base>...HEAD` and `git log <base>..HEAD --oneline`. Stop if the ref
   is invalid or the diff is empty.
3. Read applicable repository instructions and coding standards.
4. Find the owning spec or issue from the user's path, commit references, or nearby
   repository documentation. If none exists, review the Standards axis and state that
   Spec coverage was unavailable.

Do not require a particular issue tracker, setup command, or repository layout.

## Review

Report only defects introduced or exposed by the diff that have a concrete effect.
For each finding include severity, file and line, evidence, impact, and the smallest
credible correction. Distinguish documented-rule violations from judgment calls.

Useful maintainability signals include duplicated logic, speculative abstraction,
misleading names, pass-through wrappers, scattered changes for one behavior, and
interfaces that leak implementation details. Do not turn this list into a mandatory
smell checklist or report issues already enforced by tooling.

On the Spec axis check:

- requested behavior that is missing or partial;
- behavior added without authority;
- implementation that appears to satisfy the text but violates its observable intent.

## Return

Present findings by severity, retaining a `Standards` or `Spec` label on each. If there
are no actionable findings, say so and name any material evidence gap. Do not pad the
result with compliments, restate the diff, or create a report file unless requested.
