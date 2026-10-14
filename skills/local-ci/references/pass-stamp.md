# Pass stamp and hooks

Read before writing or changing the pass stamp or the git hooks. The stamp is a git tree
id, so it identifies content, not a commit: a run on uncommitted work still matches once
exactly that content is committed.

## Tree id of the working tree

Stage everything into a temporary copy of the index and write a tree. `git add -A`
respects `.gitignore` and applies the same line-ending normalization a commit would, so
the id equals the later commit's tree. Copying the real index first keeps it fast. Keep
the temporary index under an ignored directory.

PowerShell (inside the CI script; `$logDir` is an ignored build directory):

```powershell
function Get-WorkTreeId {
    $index = Join-Path $logDir 'stamp.index'
    Copy-Item (git rev-parse --path-format=absolute --git-path index) $index -Force
    $env:GIT_INDEX_FILE = $index
    try {
        git add -A 2>$null
        git write-tree
    } finally {
        Remove-Item Env:\GIT_INDEX_FILE
        Remove-Item $index -Force -ErrorAction SilentlyContinue
    }
}
```

POSIX shell:

```sh
work_tree_id() {
    index="$LOG_DIR/stamp.index"
    cp "$(git rev-parse --path-format=absolute --git-path index)" "$index"
    GIT_INDEX_FILE="$index" git add -A 2>/dev/null
    GIT_INDEX_FILE="$index" git write-tree
    rm -f "$index"
}
```

`--git-path index` resolves correctly inside linked worktrees; don't hard-code `.git/index`.

## Writing the stamp

Take the id before the full tier starts, take it again after the last step passes, and
write the stamp only if both are equal. Write it last, after every step, including
artifact copying, has succeeded.

```powershell
if ($Full) { $treeAtStart = Get-WorkTreeId }
# ... all steps ...
if ($Full) {
    if ((Get-WorkTreeId) -eq $treeAtStart) { Set-Content -LiteralPath $passStamp -Value $treeAtStart -NoNewline }
    else { Write-Host 'files changed during the run; pass not stamped' }
}
```

Bind `Set-Content` parameters by name. With positional arguments plus `-NoNewline`, one
real run wrote a file named after the tree id that contained the stamp path.

## pre-push hook

Git passes one line per pushed ref on stdin: `<local ref> <local sha> <remote ref> <remote sha>`.
Check every pushed commit, not `HEAD`; a push may name another branch or a tag.

```sh
#!/bin/sh
# Full CI before push; skipped when every pushed commit differs from the last passing
# full run (build/ci/full-passed) only in Markdown files.
stamp=$(cat build/ci/full-passed 2>/dev/null)
reuse=$stamp
while read -r local_ref local_sha remote_ref remote_sha; do
    case "$local_sha" in *[!0]*) ;; *) continue ;; esac # branch deletion: nothing to test
    [ -n "$stamp" ] && git diff --quiet "$stamp" "$local_sha^{tree}" -- . ':(exclude)*.md' 2>/dev/null || reuse=
done
if [ -n "$reuse" ]; then
    echo "Full CI already passed for tree $stamp; skipping."
    exit 0
fi
exec pwsh -NoProfile -ExecutionPolicy Bypass -File scripts/ci.ps1 -Full
```

- Hooks run at the worktree root, so relative paths like `build/ci/full-passed` refer
  to that worktree's own stamp.
- Unreachable tree objects are eventually garbage-collected. A failing `git diff` clears
  `reuse`, so the hook falls back to a full run rather than skipping.
- Widen the exclusion only for paths that cannot affect any tier (e.g. `docs/`); never
  exclude the CI script, hooks, build files or test resources.
- Check the hook itself by feeding it a line for an already stamped commit (expect the
  skip message) and use `git diff --quiet <stamp> <commit> -- . ':(exclude)*.md'` on
  a code change (expect exit 1). Don't run a real push to test it.

## Shell pitfalls seen in practice

- Files deployed to Linux from a Windows checkout (systemd units, shell scripts, proxy
  config) need `eol=lf` in `.gitattributes`, or they arrive with CRLF.
- PowerShell treats curly quotes (`“”`, `‘’`) as string delimiters. Text arguments
  containing them can split, and the remainder silently binds to the next positional
  parameter. Validate URL-like parameters with `ValidatePattern`.
- Piping a multi-line script from PowerShell to a native command (`$script | ssh host 'sh -s'`)
  appends CR to the last line, so a final `rm -rf 'dir'` silently becomes a no-op. Pass the
  script as an argument (`ssh host $script`).
