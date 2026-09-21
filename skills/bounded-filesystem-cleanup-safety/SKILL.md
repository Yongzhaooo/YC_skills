---
name: bounded-filesystem-cleanup-safety
description: Use when cleanup will physically delete or destructively move directories, broad file sets, tracked or unique data, or targets with unclear ownership or boundaries. Keep exact disposable-file cleanup lightweight and ask once only for materially risky scope.
---

# Bounded Filesystem Cleanup Safety

Use proportionate safeguards for physical deletion and destructive moves. This skill is
not a general gate for worktree curation, staging, commits, formatting cleanup, or
read-only inventory. If no destructive filesystem mutation is needed, stop using it.

Project rules, user scope, and higher safety instructions still win. Preserve unrelated
dirty work. Never reset, stash, take ownership, broaden ACLs, or treat Git history as
disposable filesystem content.

## Exact, disposable targets

Proceed without new confirmation when the target is an exact path or short explicit
allowlist inside the requested scope, is disposable or recoverable, and has no tracked,
unique, active-owner, symlink, mount, privilege, or boundary ambiguity.

Use the cheapest check that could reveal a mistake, perform the exact operation, and
verify the actual post-state and nearby boundary. Exact paths, basic metadata, ownership,
and post-state are normally enough.

Do not calculate content hashes by default. Use a hash only when an owning tool or
protocol already requires one, or when content identity genuinely cannot be established
more cheaply. Do not create manifests, capsules, or quarantine flows for routine cleanup.

## Materially risky scope

Ask once before mutation when the operation is recursive or broad, the target includes
tracked, unique, user-authored, synchronized, or expensive-to-recreate data, ownership or
enumeration is unclear, a producer may still be active, a link or repository boundary is
involved, or recovery would be materially difficult.

Keep the request compact: state the target boundary, intended operation, why it is risky,
and the recovery boundary. Include counts or size only when they are cheap and useful;
do not build an exhaustive inventory just to request permission.

Confirmation authorizes the semantic operation within that boundary, not one command
spelling or one snapshot. Recheck the boundary before acting. Repair commands and retry
recoverable failures within the same scope without asking again. Ask again only if the
target expands, ownership changes materially, another owner must be overridden, or
recovery becomes worse.

## During and after cleanup

- Prefer trash, an exact move, or quarantine only when it materially improves recovery.
- Never widen the target to finish a cleanup.
- Stop on unexpected paths, ownership, permissions, links, or cross-boundary effects.
- Verify the real post-state; an exit code alone is not evidence.
- A safe bounded partial cleanup is acceptable. Isolated, reproducible residue may also
  be left in place instead of creating more cleanup machinery.

Report the exact target, action, post-state, and recovery option. If no safe mutation is
possible, report the missing authority or evidence and state `mutation: none`.

## Lessons

- Hashes are exceptional identity tools, not default cleanup evidence or authorization.
- User friction is a safety failure when ceremony is applied to exact, disposable targets.
- One confirmation covers the stated risk boundary; command repairs do not consume it.
- Large dirty diffs require curation and preservation, not automatic physical deletion.
