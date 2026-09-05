---
name: test-verification
description: Use when verifying code changes before claiming completion, reviewing regression risk, assessing test coverage, triaging CI failures, or planning verification.
---

# Test Verification

Before reporting code work as complete, verify behavior with evidence.

Check:
- What files changed and what behavior boundary they affect.
- Existing tests closest to the changed behavior.
- Whether the change needs a new test or only existing coverage.
- One normal path, one failure/edge path, and one integration boundary when practical.
- Residual risk that cannot be verified locally.

Run the narrowest useful commands first. Broaden only when shared code, contracts, or build configuration changed.

Report:
- Commands run and result.
- What the commands prove.
- What remains unverified and why.
- Suggested next verification if local execution is blocked.
