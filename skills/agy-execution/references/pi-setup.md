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
selected skill body with only scoped context/question tools; supply any required reference text
explicitly. Project AGENTS.md is discovered for execution, but not text assistance.

The runner uses Pi RPC with the bundled `primary_bridge.ts` extension. Assist enables
only `ask_primary`, `inspect_context` and the provider's permission adapter. The two
bridge operations receive validated allow-once replies in default mode; arbitrary
command/edit permissions are cancelled. An explicit user request for AGY execution
authorizes necessary edits, builds and tests within that assignment: pass Execution
`--auto-approve` without a separate confirmation. Preserve stated scope and limits;
merely installing or discussing AGY does not authorize execution. Native Antigravity tools are not
a filesystem sandbox. ACP reconstruction can truncate older conversation, so verify
important continuity.
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
`quota-recovery.dpapi` blocks another query. After confirming no CLI operation
is active, restore an interrupted query with:

```text
python scripts/pi_accounts.py restore-cli
```

Only explicit exhaustion triggers automatic recovery. Unknown or zero 5h/weekly
quota is ineligible. Sort by remaining 5h, then weekly, then profile name. Never retry
an exhausted profile in the same episode. Profile names without enrolled ACP
snapshots are reported by quota discovery but cannot be selected. No implicit model
fallback or permission increase occurs. Enrollment, global account switching and
CLI quota queries share a transaction lock; active CLI work blocks quota discovery.
Preserve unrelated clients and never force past a pending recovery.

With rotation enabled, independent Pi sessions can run concurrently, even on the
same account. The runner gives each session a stable ACP home under the account
store's `sessions/<session-path-hash>/`, using `GEMINI_HOME` and
`AGY_ACP_FORCE_FILE_STORAGE=1`. These runtime settings are documented by the
[acpx Antigravity client](https://github.com/openclaw/acpx/blob/main/agents/Antigravity.md)
and verified with simultaneous calls here. No runtime binary is patched.
Account rotation changes only the requesting session's files. The session lock
prevents two writers using the same exact Pi session path; quota transactions are
serialized briefly rather than locking the entire run.

Keep the session home for resume. It contains native OAuth credential files and
runtime caches outside Git; enrollment snapshots remain DPAPI-encrypted. A legacy
session migrating from the shared ACP home rebuilds its native checkpoint from the
saved Pi transcript. Already running older runners retain their old lock behavior
until they finish. With rotation disabled, this ACP home isolation is not enabled.

The first attempt retains its files; retries use `retry-01`, etc. under that run's
evidence directory. The top-level result/summary describe the final outcome,
`initial-summary.json` preserves the original failure, `recovery.json` records
switches, and `quota.json` records remaining quota and reset times. The Pi session
path remains exact. ACP bindings are invalidated across accounts; the saved Pi
transcript reconstructs context and the continuation prohibits duplicate external
actions. Inspect old context/artifacts if reconstruction omitted important history.

## Primary dialogue, Wayfinder and Bench

Both runners emit newline-delimited JSON `primary_request` events while the process
is running. Use the exact event `run_dir` and `request_id` with `pi_dialogue.py --run
<run-dir> --request <id> --answer-file <utf8-file>`. Keep waiting on the original process
for the final envelope. Host integrations must surface intermediate stdout, not buffer
everything until exit. Foreground calls retain the host wait. The optional background
worker below uses native thread messages to wake Codex; neither mode reads host session
databases. Interruption recovery is in SKILL.md.

`inspect_context` reads `docs/wayfinder.md` under Execution's `--cwd` or Assist's
`--context-root`. For Bench, the selected root must contain `bench-project.json` with
a nonempty `project` string. Add an optional command array to machine-local routing:

```json
"bench_command": ["/absolute/path/to/python", "/absolute/path/to/bench.py"]
```

The command must implement the existing Bench CLI `--search <query> --project <name>`
JSON contract. Returned hits must have that project; mismatches fail closed. Queries
return at most eight excerpts of 5,000 characters, with source/version metadata and
truncation flags. Wayfinder reads at most 24,000 characters. For additional material,
Execution follows source paths within its authorized scope; Assist asks the primary
to supply it. No configured Bench or no Wayfinder is a supported unavailable result.
This installs neither Bench nor credentials and never broadens a search globally.

## Background wake in Codex Desktop

`--background` starts a detached local worker and returns `job_dir` immediately.
The original dispatch thread can end its turn. Question/completion/failure events
call `send_message_to_thread` through the installed official `codex-app-tools` MCP
server using standard MCP stdio. This is not a second Codex app-server instance and
does not resume a second writer onto the host's session files. It does not change
the thread model, poll an LLM, create a new task, or register a scheduled automation.

Add the verified local server entry point and Node runtime to `agy-runner.json`:

```json
"codex_app_tools_command": ["/absolute/path/to/node", "/absolute/path/to/codex-app-tools/server.mjs"]
```

Use the installed official plugin's actual path; do not copy its source into this
skill or modify its cache. The tested plugin is `codex-app-tools` 0.1.6. Its MCP
catalog and dispatch-thread identity are checked before launch. A stale path or
missing thread tools fails instead of selecting another chat. The original Codex
Desktop environment must supply `CODEX_THREAD_ID` and `CODEX_APP_TOOLS_PIPE_PATH`;
do not invent either. Other hosts keep using the foreground runner.

```text
python scripts/agy_assist.py --prompt-file task.txt --context-root <project> --background --reply-timeout 3600
python scripts/agy_execution.py --cwd <project> --prompt-file task.txt --output-dir <new-run> --background --reply-timeout 3600
python scripts/pi_background.py status <returned-job-dir>
```

Use this only with human authorization to notify the original dispatch thread.
It does not authorize automatic tool approval. Job metadata and logs stay under
`~/.pi/agent/agy-background-runs`, outside Git. `job.json` binds the original thread;
`status.json` records lifecycle and final runner result; `notifications/` records
each delivery attempt; the runner's own question/evidence files stay in its run.
Reply using `pi_dialogue.py` and the notification's exact run/request. Replies never
start a second executor; the existing Pi RPC call continues.

Keep Codex open on the dispatch machine. App shutdown/restart, machine sleep or a
lost pipe can prevent wakeup. An uncertain delivery is not retried automatically,
to avoid duplicate prompts; inspect its record and the current request status before
manual recovery. The worker is single-use and not a restart service. A question that
exceeds its reply deadline remains recoverable through the exact saved Pi session.
Only the waiting Pi session remains locked; independent managed sessions can run.
Reading `status.json` is not delivery acceptance.
