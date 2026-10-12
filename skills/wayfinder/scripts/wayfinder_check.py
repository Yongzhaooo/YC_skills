#!/usr/bin/env python3
"""Keep docs/wayfinder.md within its reading budget and free of pasted logs.

A map may stay over budget; a change may not make an over-budget map larger
or add log-shaped content. Standard library only.

  wayfinder_check.py [PATH]          check PATH (default docs/wayfinder.md) against git HEAD
  wayfinder_check.py --hook EVENT    Claude/Codex hook: session-start | user-prompt-submit | stop
  wayfinder_check.py --hook agy-pre-invocation | agy-stop    Antigravity hooks.json

Agent hooks judge only a change made since their own snapshot of the map; without a
snapshot they give no verdict. Git HEAD is the baseline only for this CLI and doctor.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

MAP = Path("docs") / "wayfinder.md"
DEFAULT_BUDGET = 3000
MAX_FENCE_LINES = 10
BUDGET_RE = re.compile(r"<!--\s*wayfinder-budget:\s*(\d+)\s*-->")
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
LOG_LINE_RES = (
    re.compile(r"Traceback \(most recent call last\)"),
    re.compile(r"^\s*at [\w$.<>]+\([^)]*\)\s*$"),  # JVM stack frame
    re.compile(r"panicked at "),
)
FIX_HINT = (
    "Replace instead of appending: move finished items to docs/wayfinder-done.md or their owner, "
    "keep receipts, IDs, counts and logs in the owning record, and rewrite stale Current answer text."
)
NOT_MINE = "If this turn did not edit the map (another session did), say so and stop; this reminder fires once."


def tokens(text: str) -> int:
    """Approximate reading cost: an ASCII character ~1/4 token, any other character ~1."""
    return round(sum(1 if ord(c) > 127 else 0.25 for c in text if not c.isspace()))


def budget(text: str) -> int:
    match = BUDGET_RE.search(text)
    return int(match.group(1)) if match else DEFAULT_BUDGET


def log_lines(text: str) -> int:
    """Lines that look pasted from a console: stack-trace lines anywhere, plus every line
    of a code block (closed or not) longer than MAX_FENCE_LINES."""
    count, fence = 0, None

    def close(block: list[bool]) -> int:
        return len(block) if len(block) > MAX_FENCE_LINES else sum(block)

    opener = ""
    for line in text.splitlines():
        is_log = any(rx.search(line) for rx in LOG_LINE_RES)
        match = FENCE_RE.match(line)
        if fence is None and match:
            fence, opener = [], match.group(1)
        elif (fence is not None and match and not match.group(2).strip()
              and match.group(1)[0] == opener[0] and len(match.group(1)) >= len(opener)):
            count += close(fence)  # a closing fence matches the opener's character and length
            fence = None
        elif fence is not None:
            fence.append(is_log)
        else:
            count += is_log
    return count + (close(fence) if fence is not None else 0)


def evaluate(text: str, baseline: str | None) -> dict:
    """Blocking problems are those this change introduced; notices describe inherited state.
    The budget comes from the baseline, so a change cannot raise its own limit."""
    text = text.replace("\r\n", "\n")
    size = tokens(text)
    limit = budget(baseline if baseline is not None else text)
    base_size = tokens(baseline) if baseline is not None else None
    logs = log_lines(text)
    base_logs = log_lines(baseline) if baseline is not None else 0
    blocking, notices = [], []
    if size > limit:
        if base_size is None or size > base_size:
            grew = f" (+{size - base_size} this change)" if base_size is not None else ""
            blocking.append(f"map is ~{size} tokens, over its {limit}-token budget{grew}")
        else:
            notices.append(f"map is ~{size} tokens, over its {limit}-token budget")
    if logs > base_logs:
        blocking.append(f"added {logs - base_logs} pasted log lines "
                        f"(stack traces or code blocks over {MAX_FENCE_LINES} lines)")
    elif logs:
        notices.append(f"map holds {logs} pasted log lines")
    return {"tokens": size, "budget": limit, "blocking": blocking, "notices": notices}


def git_toplevel(folder: Path) -> Path | None:
    try:
        out = subprocess.run(["git", "-C", str(folder), "rev-parse", "--show-toplevel"],
                             capture_output=True, check=True).stdout.decode("utf-8").strip()
    except (OSError, subprocess.CalledProcessError, UnicodeDecodeError):
        return None
    return Path(out) if out else None


def git_head(path: Path) -> str | None:
    top = git_toplevel(path.parent)
    if top is None:
        return None
    try:
        rel = path.resolve().relative_to(top.resolve()).as_posix()
        blob = subprocess.run(["git", "-C", str(top), "show", f"HEAD:{rel}"], capture_output=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError, ValueError):
        return None
    return blob.decode("utf-8", "replace")


def read(path: Path) -> str:
    return path.read_bytes().decode("utf-8", "replace")


def map_path(start: str) -> Path | None:
    """The project's map: an existing docs/wayfinder.md at or above start, else where it
    would go at the git root, so a map created during the turn has an empty baseline."""
    if not start:
        return None
    here = Path(start).resolve()
    top = git_toplevel(here)
    folders = [here, *here.parents]
    if top is not None and top.resolve() in folders:
        folders = folders[: folders.index(top.resolve()) + 1]  # never climb out of this repository
    for folder in folders:
        if (folder / MAP).is_file():
            return folder / MAP
    return top / MAP if top else None


def state_file(session: str) -> Path:
    name = hashlib.sha256(session.encode("utf-8")).hexdigest()[:16]
    return Path(tempfile.gettempdir()) / "wayfinder-check" / f"{name}.json"


def load_state(session: str) -> dict:
    try:
        data = json.loads(state_file(session).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        data = {}
    return {"maps": data.get("maps", {}), "blocked": data.get("blocked", [])}


def save_state(session: str, state: dict) -> None:
    target = state_file(session)
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=target.parent, suffix=".tmp")
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(state, handle)
        os.replace(tmp, target)
    except OSError:
        pass  # without a snapshot, Stop gives no verdict


def message(path: Path, items: list[str]) -> str:
    return f"wayfinder check ({path}): " + "; ".join(items) + ". " + FIX_HINT


def snapshot(state: dict, paths: list[Path], reset: bool) -> list[str]:
    """Record each map's current content as its baseline; return notices for inherited problems."""
    if reset:
        state["maps"], state["blocked"] = {}, []
    notes = []
    for path in paths:
        if str(path) in state["maps"]:
            continue
        text = read(path) if path.is_file() else ""
        state["maps"][str(path)] = text
        result = evaluate(text, text)
        if result["notices"]:
            notes.append(message(path, result["notices"]) + " Compact it when this task touches the map; never grow it.")
    return notes


def stop_reason(state: dict) -> str | None:
    """Judge only maps that changed since their snapshot; report each distinct outcome once."""
    problems = []
    for key, baseline in state["maps"].items():
        path = Path(key)
        if not path.is_file():
            continue
        text = read(path)
        if text.replace("\r\n", "\n") == baseline.replace("\r\n", "\n"):
            continue
        result = evaluate(text, baseline)
        if result["blocking"]:
            problems.append(message(path, result["blocking"]))
    if not problems:
        return None
    reason = " ".join(problems) + " " + NOT_MINE
    digest = hashlib.sha256(reason.encode("utf-8")).hexdigest()
    if digest in state["blocked"]:
        return None
    state["blocked"].append(digest)
    return reason


def run_hook(event: str) -> int:
    try:
        payload = json.loads(sys.stdin.buffer.read().decode("utf-8") or "{}")
    except (ValueError, UnicodeDecodeError):
        payload = {}
    agy = event.startswith("agy-")
    session = str(payload.get("conversationId" if agy else "session_id") or "")
    starts = (payload.get("workspacePaths") or []) if agy else [payload.get("cwd", "")]
    paths = sorted({p for p in map(map_path, starts) if p})
    if not session or not paths:
        print("{}" if agy else "", end="")
        return 0
    session = ("agy:" if agy else "agent:") + session
    state = load_state(session)
    if event in ("session-start", "user-prompt-submit", "agy-pre-invocation"):
        # Antigravity has no prompt event: its baseline is the map as the conversation first saw it.
        notes = snapshot(state, paths, reset=event == "user-prompt-submit")
        save_state(session, state)
        if agy:
            print(json.dumps({"injectSteps": [{"ephemeralMessage": n} for n in notes]}))
        elif event == "session-start" and notes:
            print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart",
                                                     "additionalContext": " ".join(notes)}}))
        return 0
    if event in ("stop", "agy-stop"):
        reason = None if payload.get("stop_hook_active") else stop_reason(state)
        save_state(session, state)
        if agy:
            print(json.dumps({"decision": "continue", "reason": reason} if reason else {}))
        elif reason:
            print(json.dumps({"decision": "block", "reason": reason}))
        return 0
    print(f"unknown hook event: {event}", file=sys.stderr)
    return 2


def main(argv: list[str] | None = None) -> int:
    sys.stdout.reconfigure(errors="replace")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("path", nargs="?", default=str(MAP))
    parser.add_argument("--hook", choices=("session-start", "user-prompt-submit", "stop",
                                           "agy-pre-invocation", "agy-stop"))
    args = parser.parse_args(argv)
    if args.hook:
        return run_hook(args.hook)
    path = Path(args.path)
    try:
        text = read(path)
    except OSError as exc:
        print(f"{path}: {exc}", file=sys.stderr)
        return 2
    result = evaluate(text, git_head(path))
    print(f"{path}: ~{result['tokens']}/{result['budget']} tokens")
    for item in result["blocking"]:
        print(f"  BLOCK  {item}")
    for item in result["notices"]:
        print(f"  NOTICE {item}")
    return 1 if result["blocking"] else 0


if __name__ == "__main__":
    sys.exit(main())
