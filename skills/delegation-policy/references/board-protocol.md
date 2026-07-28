# Board Protocol

Documentation for the filesystem exchange seam used when a child returns substantive
results as files instead of inline text. `scripts/session_board.py` is the enforcing
authority. If this page and the script disagree, the script wins.

## Layout

`work/session-routing/<run-id>/<task-id>/` is the only substantive exchange seam.

| File | Owner | Role |
| --- | --- | --- |
| `request.md` | main Agent | immutable task, soul capsule, and capsule SHA-256 |
| `thread.json` | main Agent | run/task IDs, model, deadline |
| `result.md` | worker | the substantive answer |
| `done.json` | worker | completion marker, written last |

Repository writes outside the board require explicit, disjoint write ownership declared
in `request.md`. Board-output-only is the default.

## What the helper does

`scripts/session_board.py` prepares and validates boards. It never creates threads,
selects a route, edits a runtime store, or archives anything. It maps the selected model
to the required soul, embeds the canonical capsule plus its SHA-256 in `request.md`, and
rejects a missing, mismatched, or modified capsule.

The thread bootstrap message carries only: run ID, task ID, board path, request hash,
soul name, and an instruction to read `request.md`. The worker must not spawn agents,
create another session, or invent missing context.

## What `result.md` contains

`result.md` opens with a bounded summary: outcome (`pass`, `partial`, or `blocked`); the
behavior delta in a sentence or two; changed paths, with anything outside declared
ownership listed separately as unexpected; validation commands actually run and what
they showed; and material findings and unresolved assumptions, stating `none`
explicitly. Supporting detail — decisive diff hunks, key log excerpts — follows below
the summary; exploration narrative and raw transcripts stay out, and the board gains no
extra files.

The main Agent may accept from the summary alone only when nothing fires. An unexpected
path, failed or skipped required validation, a contradiction between the summary and its
supporting detail or the repository, or a change reaching a public contract, persistent
data, security, or anything irreversible forces reading the actual diff and evidence
before acceptance.

## Commit ordering

The worker must:

1. write and close `result.md`;
2. reread its exact on-disk bytes;
3. hash those bytes with no line-ending normalization;
4. write `done.json` last;
5. never modify `result.md` afterward.

Hashing a pre-write string instead of the final on-disk bytes is the single most common
failure and is rejected before any semantic grading.

## Validation gates

Accept only a non-empty `result.md` followed by a schema-valid `done.json` whose
run/task/model and request/result hashes match. Any of the following invalidates the
result:

- missing marker, stale hash, or empty result;
- `result.md` containing control characters outside printable ASCII (0x00-0x08,
  0x0B-0x0C, 0x0E-0x1F, 0x7F);
- marker fields added, removed, or renamed;
- malformed deadline, request/thread deadline mismatch, or a `done.json` filesystem
  completion time later than the canonical UTC deadline;
- an extra transcript/log file or a changed file outside declared ownership.

The completion-time check is an operational sanity check only. Worker-owned mtime is
mutable and not tamper-evident, so it carries no security, authorization, or promotion
authority.

## Failure handling

A worker that ignores its soul or produces invalid board output is expected behavior, not
an anomaly. Accept the failed board as evidence and proceed without it. Do not retry the
same protocol more than once per task, and never replace missing board evidence with a
final-looking model message.

Record created sessions as temporary with opaque IDs and no raw prompt or response text.
After integrating or rejecting results, hand cleanup to `session-gc`. Never purge a board
that remains unique failure evidence.
