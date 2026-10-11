#!/usr/bin/env python3
"""Run one assignment through Pi + official Antigravity ACP; independently accept delivery."""

import argparse
import json
from pathlib import Path
import subprocess
import sys


from pi_transport import run_pi


def run(options):
    prompt = options.prompt_file.read_text(encoding="utf-8-sig")
    if not prompt.strip():
        raise ValueError("Assignment is empty")
    boundary = ("You implement and test this assignment as a leaf agent. Do not delegate. "
                "Preserve others' changes and the stated write/production boundaries. "
                "Read applicable repository instructions and existing test/CI definitions before choosing checks. "
                "Use the project's established validation commands, investigate failures and repair within scope. "
                "Read available Wayfinder and relevant project-scoped Bench context. "
                "Ask the primary agent only for unresolved conflicts, missing requirements or genuine blockers. "
                "Existing CI/CD does not authorize deployment, publishing or changing secrets. "
                "The primary agent independently accepts your delivery.\n\n")
    run_pi(boundary + prompt, cwd=options.cwd, output=options.output_dir,
           model=options.model, effort=options.effort, conversation=options.conversation,
           timeout=options.timeout, auto_approve=options.auto_approve,
           context_root=options.cwd, reply_timeout=options.reply_timeout,
           skills=getattr(options, "skill", []), skill_references=getattr(options, "skill_reference", []))
    return json.loads((options.output_dir / "summary.json").read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cwd", type=Path, required=True)
    parser.add_argument("--prompt-file", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--model")
    parser.add_argument("--effort", choices=("low", "medium", "high"))
    parser.add_argument("--conversation", help="Exact Pi session.jsonl path; CLI conversation IDs are not compatible")
    parser.add_argument("--skill", action="append", default=[], help="Selected installed skill name or SKILL.md path")
    parser.add_argument("--skill-reference", action="append", default=[], help="Selected UTF-8 reference inside a selected skill")
    parser.add_argument("--auto-approve", action="store_true", help="Requires explicit human authorization for this invocation")
    parser.add_argument("--background", action="store_true", help="Notify this Codex Desktop thread; requires human authorization to message it")
    parser.add_argument("--reply-timeout", type=float, default=900, help="Seconds to wait for a primary reply; separate from active timeout")
    parser.add_argument("--timeout", type=float, help="Optional active execution limit in seconds")
    options = parser.parse_args()
    try:
        if options.background:
            from pi_background import launch
            from pi_transport import load_route
            print(json.dumps(launch(__file__, sys.argv[1:], load_route()), ensure_ascii=False))
            return 0
        print(json.dumps(run(options), ensure_ascii=False))
        return 0
    except (OSError, ValueError, subprocess.SubprocessError, KeyboardInterrupt) as exc:
        print(json.dumps({"invocation_complete": False, "error": str(exc) or type(exc).__name__}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    raise SystemExit(main())
