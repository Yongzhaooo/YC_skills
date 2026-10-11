#!/usr/bin/env python3
"""Run one official AGY implementation assignment; delivery acceptance stays human-led."""

import argparse
import json
import math
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys


def terminal_result(path):
    results = []
    with path.open(encoding="utf-8") as stream:
        for line in stream:
            if not line.strip():
                continue
            event = json.loads(line)
            if not isinstance(event, dict):
                raise ValueError("Non-object AGY event")
            if event.get("event") == "result":
                results.append(event.get("result"))
    if len(results) != 1 or not isinstance(results[0], dict):
        raise ValueError("Expected exactly one terminal AGY result")
    result = results[0]
    if result.get("status") != "SUCCESS" or result.get("error"):
        raise ValueError(f"AGY result failed: {result.get('status')}: {result.get('error', '')}")
    if result.get("denied_actions"):
        raise ValueError("AGY denied required actions; inspect events.jsonl")
    if not isinstance(result.get("response"), str) or not result["response"].strip():
        raise ValueError("AGY returned an empty response")
    return result


def command(executable, options):
    args = [executable, "--input-format", "stream-json", "--output-format", "stream-json",
            "--mode", "accept-edits", "--disable-slash-commands", "--print-timeout", "0"]
    for name in ("model", "effort", "conversation"):
        if getattr(options, name):
            args.extend(["--" + name, getattr(options, name)])
    if options.auto_approve:
        args.append("--dangerously-skip-permissions")
    return args


def stop_process(proc):
    if proc.poll() is not None:
        return
    if os.name == "nt":
        subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10,
                       creationflags=subprocess.CREATE_NO_WINDOW)
    else:
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    if proc.poll() is None:
        proc.kill()
    proc.wait(timeout=10)


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run(options):
    cwd = options.cwd.resolve(strict=True)
    if not cwd.is_dir():
        raise ValueError("cwd must be a directory")
    prompt = options.prompt_file.read_text(encoding="utf-8-sig")
    if not prompt.strip():
        raise ValueError("Assignment is empty")
    if options.timeout is not None and (not math.isfinite(options.timeout) or options.timeout <= 0):
        raise ValueError("timeout must be finite and positive")
    executable = shutil.which("agy")
    if not executable:
        raise ValueError("Official agy CLI not found on PATH")
    args = command(executable, options)
    output = options.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=False)  # Never overwrite an earlier run's evidence.
    (output / "assignment.txt").write_text(prompt, encoding="utf-8")
    boundary = ("You implement and test this assignment as a leaf agent. Do not delegate. "
                "Preserve others' changes and the stated write/production boundaries. "
                "The primary agent independently accepts your delivery.\n\n")
    payload = json.dumps({"event": "user", "message": {"content": boundary + prompt}}, ensure_ascii=False) + "\n"
    summary = {"invocation_complete": False, "delivery_accepted": False, "exit_code": None}
    try:
        with (output / "events.jsonl").open("w", encoding="utf-8") as events, \
                (output / "stderr.log").open("w", encoding="utf-8") as errors:
            proc = subprocess.Popen(args, cwd=cwd, stdin=subprocess.PIPE, stdout=events, stderr=errors,
                                    text=True, encoding="utf-8",
                                    env={**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"},
                                    start_new_session=os.name != "nt",
                                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
            save(output / "process.json", {"pid": proc.pid, "cwd": str(cwd), "args": args})
            try:
                proc.communicate(payload, timeout=options.timeout)
            except (subprocess.TimeoutExpired, KeyboardInterrupt):
                stop_process(proc)
                raise
            finally:
                summary["exit_code"] = proc.poll()
        if proc.returncode != 0:
            raise ValueError(f"AGY exited {proc.returncode}; inspect stderr.log and events.jsonl")
        result = terminal_result(output / "events.jsonl")
        save(output / "result.json", result)
        summary["invocation_complete"] = True
        summary["conversation_id"] = result.get("conversation_id")
        return summary
    except (OSError, ValueError, subprocess.SubprocessError, KeyboardInterrupt) as exc:
        summary["error"] = str(exc) or type(exc).__name__
        raise
    finally:
        save(output / "summary.json", summary)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cwd", type=Path, required=True)
    parser.add_argument("--prompt-file", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--model")
    parser.add_argument("--effort", choices=("low", "medium", "high", "xhigh", "max"))
    parser.add_argument("--conversation", help="Exact ID; omit for a new conversation")
    parser.add_argument("--auto-approve", action="store_true", help="Requires explicit human authorization for this invocation")
    parser.add_argument("--timeout", type=float, help="Optional wall-clock limit in seconds")
    options = parser.parse_args()
    try:
        print(json.dumps(run(options), ensure_ascii=False))
        return 0
    except (OSError, ValueError, subprocess.SubprocessError, KeyboardInterrupt) as exc:
        print(json.dumps({"invocation_complete": False, "error": str(exc) or type(exc).__name__}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    raise SystemExit(main())
