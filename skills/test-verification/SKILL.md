---
name: test-verification
description: Use when verifying code changes before claiming completion, reviewing regression risk, assessing test coverage, triaging CI failures, or planning verification.
---

# Test Verification

Before reporting code work as complete, verify behavior with evidence.

Non-trivial logic needs at least one runnable check that would fail if the relevant
behavior broke. Existing tests can satisfy this requirement; it does not mean adding
a new test for every change. Reuse the repository's test framework and fixtures. If
there is no suitable coverage, add the smallest meaningful test or self-check without
introducing a new framework solely for a small change. Trivial edits do not need a new test.

Check:
- What files changed and what behavior boundary they affect.
- Existing tests closest to the changed behavior.
- Whether the change needs a new test or only existing coverage.
- The normal, failure/edge, or integration paths needed to prove the changed behavior.
- Residual risk that cannot be verified locally.

Run the narrowest useful commands first. Broaden only when shared code, contracts, or build configuration changed.

Reuse accepted verification evidence from the implementer or another agent when it still
applies to the current code and acceptance boundary. Once required checks pass, stop;
rerun or broaden only for a new change, failure, or material evidence gap. Do not add a
new test when existing coverage already proves the changed behavior.

Report:
- Commands run and result.
- What the commands prove.
- What remains unverified and why.
- Suggested next verification if local execution is blocked.

## Lessons

- For error-propagation fixes, exercise the real affected functions and their consumer
  where practical. Use an old-code or injected-fault negative control to show the check
  detects the failure; a detached model does not prove the implementation follows it.
- Keep evidence tied to the tested source and configuration. A metadata-only rewrite
  need not trigger recompilation when source equivalence is established; object builds,
  mocked tests, and hardware runs support different claims.
