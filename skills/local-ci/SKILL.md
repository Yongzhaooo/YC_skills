---
name: local-ci
description: Set up, run and maintain a repository's local CI - one entry script with fast and full tiers, git hooks, reuse of a passing full run, and the split with remote CI - and triage its failures as real, flaky or environmental. Use when adding or changing a project's local CI script or hooks, running full local CI before a push or release, a local CI or pre-push run fails, or deciding what remote CI should repeat. Not for choosing which tests a change needs (test-verification), debugging a build tool itself or triaging external CI systems.
---

# Local CI

Local CI runs the project's slow, device- or environment-bound checks on the
maintainer's machine, once per content change, and leaves remote CI only what a clean
environment adds. Read the repository's existing script, hooks, remote workflow and build
docs first; extend them rather than adding a parallel pipeline.

## Shape of the pipeline

- **One entry script** (for example `scripts/ci.ps1` or `scripts/ci.sh`) that people and
  hooks both call. Tiers are flags, not separate scripts: a fast tier (build + unit tests,
  minutes) and a full tier (adds integration, device or UI tests). It finds the
  toolchain itself, fails with a fix-it message when something is missing, and writes logs,
  screenshots and artifacts under an ignored build directory.
- **Explicit test target.** Device or service tests run only against a named, isolated
  target (a dedicated emulator, container or test database) with isolated app data. The
  script refuses anything else; never point it at a personal device or production data.
- **Judge by the runner's verdict.** Some runners exit 0 on failures (for example
  `am instrument`); parse their summary line (`OK (N tests)` / `FAILURES!!!`) and fail the
  step yourself. Report test counts, not just "passed".
- **Hooks are optional and repo-owned** (`.githooks/` + `git config core.hooksPath`):
  pre-commit runs the fast tier, pre-push runs the full tier.

## Run once per content: the pass stamp

Running the full tier by hand and then again in pre-push is the main waste. Avoid it:

1. When the full tier passes, record the git tree of the exact content it tested,
   including uncommitted and untracked files, but only if that tree did not change
   during the run.
2. pre-push compares each pushed commit's tree with the stamp and skips the full tier
   when the only differences are in files that cannot affect it (by default `*.md`; drop
   that default if the build packages Markdown, e.g. as app assets, templates or test
   fixtures). Deleted refs push nothing; a missing or unreadable stamp means run.
3. Any other change, including to the CI script itself, runs the full tier again. Only a
   complete full-tier pass writes the stamp; rerunning a single test never does.

Fragile details (temporary index, hook parsing of stdin, shell pitfalls) and tested
snippets are in [references/pass-stamp.md](references/pass-stamp.md); read it before
writing or changing the stamp or hooks.

## Split with remote CI

Remote CI repeats only what local CI cannot prove: a build from a clean checkout. For the
maintainer's pushes to the main branch that already passed local full CI, a compile check
is enough. Pull requests from contributors and release tags still run unit tests, because
contributors' local hooks are not guaranteed and release artifacts must be built and signed
remotely. Remote CI cannot see the local stamp, so this split assumes the people pushing
to main run the hooks and do not bypass them; for a team without that guarantee, keep
unit tests on main pushes too. Keep documentation-only commits on the repository's
existing skip convention (such as `[skip ci]`). After a green remote run, do not add more
local runs for the same content.

On a private Forgejo (or similar self-hosted) server, keep execution off the code host:
the server stores Git and artifacts, and a dedicated compute machine runs the runner under
a project label. Leave queueing, cancellation, timeouts and result storage to Forgejo's
native `concurrency`, `timeout-minutes` and artifact upload; do not add hand-built
queues, lock files or result-publishing pushes. The workflow only checks out, calls the
same entry script, and uploads its output. Read
[references/forgejo-actions.md](references/forgejo-actions.md) before setting up or
changing such a runner or workflow.

## Running it

- Start one full run and let it finish. Wait on the process; don't poll it with new runs.
- **Do not edit the working tree while a run is going.** Edits mix into what is being
  tested and invalidate the stamp. Edit outside the tree (other repositories, scratch
  space) or wait. If edits were needed, rerun the full tier on the final content.
- The test target is shared. Before starting, check for another CI or test-runner process
  using it, including from other worktrees or sessions; wait for it rather than killing it.
  Separate worktrees build separately but still share the device.
- For a release: full pass on the release content, then merge and tag. Pushes whose
  content matches the stamp skip the full run. Afterwards check the actual artifacts
  (signature, version, contents), not just the workflow's green status.

## When a run fails

Read the failing test names and stack lines from the runner log. Rule out the environment
first, then run each failed test alone on the same target, then classify:

| Class | Evidence | Action |
|---|---|---|
| Environment | Device offline or unresponsive, missing SDK, port in use, setup errors before any assertion | Fix or restart the environment, then rerun. It is not a test result. |
| Real | Fails again when run alone, or covers code the change touched | Fix the code or the test, then run the full tier again. |
| Flaky | Passes when run alone, cannot be affected by the change, and fails with a timing or framework-internal symptom (e.g. a layout/measure-pass exception) rather than an assertion about behavior | Record it with the evidence where the repository keeps verification records (plan, wayfinder or an issue) and rerun the full tier. Fix it when it repeats or when a new test is the flaky one. |

One alone-pass of an old test that the change cannot reach is enough for a rerun; it is not
enough to dismiss a failure in a test you just wrote. Never bypass hooks (`--no-verify`)
to get past a failure unless the user explicitly asks.

Common UI-test timing causes and fixes (deterministic in practice, so fix rather than
retry):

- An action whose effect is asynchronous (an intent sent after a disk write, a dialog
  opened from a coroutine): wait for its visible result before asserting.
- The soft keyboard is still opening and moves the layout: hide it and wait before clicking.
- The target is out of view inside a scrolling dialog or list: scroll to it first, or move
  primary actions above long content.
- System BACK reaches a closing dialog window instead of the screen: use the screen's own
  back control.

When the cause isn't visible, temporarily log the UI tree or the relevant state at the
failure point, run that test alone, then remove the debug code before committing.

## Report

State the tier and the result with counts, which runs were skipped by the stamp and why,
flakes seen (test, symptom, alone-run result), and anything not run (device-only steps,
manual checks).
