---
name: github-release-recovery
description: Diagnose and recover a GitHub release when a tag exists but the Releases page is empty, a release workflow repeatedly fails, or a workflow artifact exists without a downloadable Release.
---

# GitHub Release Recovery

Produce a reproducible GitHub Release, not merely a pushed tag or temporary workflow
artifact. Preserve unrelated repository changes and never expose credentials in logs.

## Distinguish the objects

- A Git tag names a commit; it does not create a Release by itself.
- A workflow artifact belongs to one Actions run and may expire.
- A GitHub Release is a published object associated with a tag and may expose durable
  downloadable assets.

Inspect all three before changing anything.

## Establish the failing layer

Read repository instructions and the release workflow, then inspect Git status, tags,
the target Release, recent workflow runs, and the failed job log. Confirm the workflow
trigger, tag pattern, publish condition, dependencies, permissions, package version, and
expected asset name.

Use repository-native commands and an existing authenticated GitHub CLI session. Do not
print or place token material in visible command arguments.

Fix only the first failing layer, run its smallest local check, then let the hosted runner
expose the next layer:

1. source gates under the declared runtime versions;
2. environment-sensitive tests such as local-calendar or path-containment behavior;
3. package construction and expected archive naming;
4. packaged-runtime smoke without development tools on `PATH`;
5. artifact upload and Release publication.

Hosted-runner success is authoritative for workflow compatibility. Local success remains
useful evidence but does not replace the declared CI environment.

## Protect release identity

The tag commit must contain every fix needed to reproduce the package and pass its release
gates. A green default branch after a failed tag run does not prove the tag is reproducible.

Do not move or overwrite a pushed tag without explicit user authorization. Prefer a new
patch version when a published tag is incomplete or already consumed. Keep package
version, archive name, tag, Release title, and build commit consistent.

Release publication and tag mutation are external writes. Diagnose freely; create a
Release, upload an asset, delete a Release, or change a tag only when the user requested
that action.

## Verify

- the tag resolves to the intended commit and its relevant workflow passed;
- the Release exists in the requested draft/prerelease state;
- the expected asset is downloadable and contains the promised runtime contents;
- its digest matches the locally accepted archive or trusted build artifact when identity
  comparison is required;
- source and build instructions remain available in Git;
- any acceptance that hosted CI cannot perform is stated separately.

Report the Release and asset URLs, tag and commit, workflow run, asset identity and
contents, and anything that remains unverified.

## Lessons

- A tag, workflow artifact, and Release are separate publication objects.
- Release pipelines reveal failures sequentially; a fixed early job does not prove later
  packaging or publication.
- A portable archive and a reproducible source tag are separate acceptance claims.
