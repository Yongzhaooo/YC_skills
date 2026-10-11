# Pi ACP setup and routing

Install a supported Node runtime, Pi, and `pi-antigravity-acp-provider` through
npm/Pi's package installer. Current verified package versions are Pi 1.1.0 and
provider 0.1.14; Node must satisfy Pi's engine requirement (at least 22.19).
Upstream: https://github.com/zacbemis/pi-antigravity-acp-provider (MIT).
The official ACP runtime is managed by that plugin; do not patch its binaries.

## Install Pi and the provider

- Pi: [earendil-works/pi](https://github.com/earendil-works/pi),
  [coding-agent documentation](https://github.com/earendil-works/pi/tree/main/packages/coding-agent).
- Provider: [zacbemis/pi-antigravity-acp-provider](https://github.com/zacbemis/pi-antigravity-acp-provider).
- Pi and the provider are third-party components; the Google ACP runtime is official.

```text
npm install -g @earendil-works/pi-coding-agent@1.1.0
pi install npm:pi-antigravity-acp-provider@0.1.14
pi
```

These versions were tested together on Windows on 2026-10-11. The first Google
login downloads the official runtime. Skills installation alone does not install
Node, Pi, the provider or any account credentials. Verify the actual installed
Node, Pi entry point and provider extension paths before filling the route below;
`npm root -g` locates globally installed packages, while Pi-installed packages may
live in its own agent directory. Use the paths from your installation, not another
user's machine. Check the provider README before upgrading this combination.


In interactive Pi, use `/login antigravity-acp` and choose Google sign-in. This
avoids an accidentally filtered provider picker. Run `/antigravity-acp permissions
default`; then choose a model with `/model`. Browser login is user-operated.
Existing CLI credentials do not authenticate ACP automatically.

The Python runners read `~/.pi/agent/agy-runner.json`, or the file explicitly selected
by `PI_AGY_CONFIG`. This is machine-local, non-secret configuration:

```json
{
  "command": ["/absolute/path/to/node", "/absolute/path/to/pi/dist/cli.js"],
  "node": "/absolute/path/to/node",
  "extension": "/absolute/path/to/pi-antigravity-acp-provider/extensions/index.ts",
  "model": "gemini-3.8-flash",
  "effort": "medium"
}
```

Use absolute paths verified on the current host. On Windows invoke Node and the
CLI JS directly, rather than passing prompts through a `.cmd` shell. On other hosts
`command` may name the native `pi` executable. `node` is optional when PATH already
resolves a compatible Node. Python uses standard library transport; schema requests
add the installed `jsonschema` library. Do not copy authentication files into MyAgents.

The CLI model slug `gemini-3.8-flash-medium` becomes Pi model `gemini-3.8-flash` plus
`--effort medium`. Verify model availability; do not fuzzy-substitute an unavailable
selection. The runner always selects the `antigravity-acp` provider.

Each Pi session has a sibling `.agent` directory containing only its runner settings,
non-secret authentication marker, and ACP checkpoint mapping. Google owns the actual
credentials under `~/.gemini/antigravity-acp`. Preserve both session and profile for
continuation. Never run two writers against one session. Interactive defaults are
not changed by per-run permission settings.

For executor skills pass selected already-installed paths with `--skill`; Pi accepts
standard SKILL.md resources. Do not install AGY delegation skills inside this leaf
executor, or mirror the whole Codex/Claude plugin cache. Text assistance embeds the
selected skill body without enabling Pi tools; supply any required reference text
explicitly. Project AGENTS.md is discovered for execution, but not text assistance.

Known limits: JSON mode cannot ask a human for ACP approval; prompting permissions
are denied. `--auto-approve` is available only for an explicitly authorized execution
run. Native Antigravity tools are not controlled by Pi's `--no-tools`. ACP history
reconstruction can truncate older conversation, so verify important continuity.
The original CLI quota/selection policy is reused by the ACP account adapter below;
its credentials remain separate.


## Automatic account recovery

The primary model selects task skills automatically and passes repeated `--skill`
arguments to either runner. Assist also accepts `--skill-reference` for selected
UTF-8 support files. No separate Pi-wide skill installation is necessary.

The current Windows adapter reuses `agy-profile` helper functions for CLI quota
discovery. This is an optional dependency, not bundled or installed by the skills:

- Tested fork: [Yongzhaooo/agy-profile](https://github.com/Yongzhaooo/agy-profile).
- Verified revision: [f52cbb0e65e6b1968d59c2b5686a84cb124bc346](https://github.com/Yongzhaooo/agy-profile/tree/f52cbb0e65e6b1968d59c2b5686a84cb124bc346).
  Its PowerShell script matched the tested installed copy after newline normalization.
- Upstream: [haclongkim/agy-profile](https://github.com/haclongkim/agy-profile).

Follow the fork README to install the CLI profile manager and save each Google
login as a named CLI profile. Its installer is `install.cmd`; the default installed
script is under `%LOCALAPPDATA%/agy-profile/agy-profile.ps1`. The ACP adapter depends
on helper functions including `Get-SavedProfiles`, `Apply-ProfileFilesAndCred`,
`Protect-JsonToFile`, and `Unprotect-FromFile`, plus the manager's credential and file
layout. Recheck these before using a different revision; the links are not a claim
that every upstream release is compatible. CLI profile snapshots stay separate
from the official ACP logins enrolled below.

Leave rotation omitted or disabled for a single account or non-Windows machine.
After installing the compatible manager and enrolling the desired ACP accounts,
add this non-secret block to the machine's `agy-runner.json`:

```json
"rotation": {
  "enabled": true,
  "cli_manager": "absolute/path/to/agy-profile.ps1",
  "powershell": "absolute/path/to/pwsh.exe"
}
```

Check the configured manager and its saved profile names first. For each account,
use official Pi `/login antigravity-acp`, then automatically identify and enroll its independent ACP login:

```text
python scripts/pi_accounts.py identity
python scripts/pi_accounts.py enroll
python scripts/pi_accounts.py list
python scripts/pi_accounts.py quota
python scripts/pi_accounts.py switch <enrolled-profile-name>
```

Enrollment reads the current verified email and stable account ID from Google's
official userinfo endpoint, then matches that ID against the saved CLI ID-token
claims (historical local metadata, not fresh authentication). Exactly one match is
required. Preserve CLI IDs for compatibility; store the email as the display identity
in the encrypted ACP snapshot. Do not guess mappings or ask users to remember numeric
profile names. `identity` shows the mapping and `list` shows enrolled emails.
For another login use Pi's account/logout flow, sign in through Google, and enroll once. After enrollment, automatic recovery
needs no browser login. Snapshots live under `~/.pi/agent/acp-profiles` and are
protected by Windows DPAPI for this user/machine. They are not portable exports.
The adapter preserves other ACP settings and does not change interactive permissions.

The manager queries official CLI `/usage`, then verifies restoration of the original
CLI credential, active marker and account-bound files. A pending encrypted
`quota-recovery.dpapi` blocks another query. After confirming no ACP/CLI operation
is active, restore an interrupted query with:

```text
python scripts/pi_accounts.py restore-cli
```

Only explicit exhaustion triggers automatic recovery. Unknown or zero 5h/weekly
quota is ineligible. Sort by remaining 5h, then weekly, then profile name. Never retry
an exhausted profile in the same episode. Profile names without enrolled ACP
snapshots are reported by quota discovery but cannot be selected. No implicit model
fallback or permission increase occurs. A managed-run lock prevents overlapping
account changes; it does not control unrelated clients. Close/preserve those clients
before switching; the adapter refuses an unsafe switch.

The first attempt retains its files; retries use `retry-01`, etc. under that run's
evidence directory. The top-level result/summary describe the final outcome,
`initial-summary.json` preserves the original failure, `recovery.json` records
switches, and `quota.json` records remaining quota and reset times. The Pi session
path remains exact. ACP bindings are invalidated across accounts; the saved Pi
transcript reconstructs context and the continuation prohibits duplicate external
actions. Inspect old context/artifacts if reconstruction omitted important history.
