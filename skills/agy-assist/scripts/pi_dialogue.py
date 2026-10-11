"""Pi RPC events, scoped context reads, and durable questions to the primary agent."""
import argparse
import json
import os
from pathlib import Path
import queue
import re
import subprocess
import sys
import threading
import time


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(path)


def read_context(request, root, route):
    root = Path(root).resolve(strict=True)
    wayfinder = root / "docs/wayfinder.md"
    manifest = root / "bench-project.json"
    if manifest.is_file() and not manifest.resolve().is_relative_to(root):
        raise ValueError("Bench manifest resolves outside the selected context root")
    project = json.loads(manifest.read_text(encoding="utf-8-sig")).get("project") if manifest.is_file() else None
    command = route.get("bench_command")
    available = isinstance(command, list) and bool(command) and all(isinstance(x, str) and x for x in command)
    action = request.get("action")
    if action == "discover":
        return {"root": str(root), "wayfinder": wayfinder.is_file(), "bench": bool(available and project), "project": project}
    if action == "wayfinder":
        if not wayfinder.is_file():
            return {"available": False, "reason": "No docs/wayfinder.md in the selected context root"}
        if not wayfinder.resolve().is_relative_to(root):
            raise ValueError("Wayfinder resolves outside the selected context root")
        body = wayfinder.read_text(encoding="utf-8-sig")
        return {"path": str(wayfinder), "text": body[:24000], "truncated": len(body) > 24000}
    if action != "bench_search":
        raise ValueError("Unknown context operation")
    if not available or not isinstance(project, str) or not project.strip():
        return {"available": False, "reason": "Bench command or project manifest is not configured"}
    query = request.get("query", "")
    if not isinstance(query, str) or not query.strip() or len(query) > 1000:
        raise ValueError("Bench query must be nonempty and at most 1000 characters")
    result = subprocess.run([*command, "--search", query, "--project", project], cwd=root,
                            capture_output=True, text=True, encoding="utf-8", timeout=45,
                            env={**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"})
    if result.returncode:
        return {"available": True, "error": "Bench query failed", "exit_code": result.returncode}
    data = json.loads(result.stdout)
    hits = data.get("hits", [])
    selected = []
    for hit in hits[:8]:
        if hit.get("project") != project:
            raise ValueError("Bench returned a result outside the selected project")
        row = {k: hit.get(k) for k in ("record", "heading", "path", "project", "version", "source_version", "index_status")}
        body = hit.get("text", "")
        row.update(text=body[:5000], truncated=len(body) > 5000)
        selected.append(row)
    return {"project": project, "hits": selected, "truncated": len(hits) > 8,
            "note": "Search excerpts only. Use source paths for further authorized investigation or ask the primary agent for missing context."}


def reply(run, request_id, answer):
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,128}", request_id):
        raise ValueError("Invalid request ID")
    if not answer.strip():
        raise ValueError("An empty reply is not a decision")
    folder = Path(run).resolve() / "questions" / request_id
    record = json.loads((folder / "request.json").read_text(encoding="utf-8"))
    if record["status"] != "waiting":
        raise ValueError("Request is no longer waiting; resume the exact session before answering a new request")
    # An exclusive claim prevents two callers from overwriting each other's decision.
    (folder / "reply-claim").mkdir()
    save(folder / "answer.json", {"request_id": request_id, "answer": answer})


def bridge_permission(event):
    # Only the two read/communication tools are pre-authorized. Never approve a
    # command, file edit, or arbitrary native permission based on a display label.
    if event.get("method") != "select":
        return None
    name, _, payload = event.get("title", "").partition("\n\n")
    allowed = {"pi-bridge_pi_inspect_context": {"action", "query"},
               "pi-bridge_pi_ask_primary": {"question", "evidence", "attempted", "recommendation"}}
    if name not in allowed:
        return None
    try:
        data = json.loads(payload)
        args = data["rawInput"]["arguments"]
        if data["kind"] != "other" or not isinstance(args, dict) or not set(args) <= allowed[name]:
            return None
        if any(not isinstance(v, str) for v in args.values()):
            return None
        if name.endswith("inspect_context") and args.get("action") not in {"discover", "wayfinder", "bench_search"}:
            return None
        if name.endswith("ask_primary") and (set(args) != allowed[name] or not args["question"].strip()):
            return None
    except (KeyError, TypeError, ValueError):
        return None
    choices = [x for x in event.get("options", []) if isinstance(x, str) and x.endswith("[allow once]")]
    return choices[0] if len(choices) == 1 else None


def converse(proc, prompt, events, *, output, session, timeout, context_root, route, reply_timeout=900):
    incoming = queue.Queue()
    def reader():
        try:
            for line in proc.stdout:
                incoming.put(line)
        finally:
            incoming.put(None)
    threading.Thread(target=reader, daemon=True).start()
    def send(value):
        proc.stdin.write(json.dumps(value, ensure_ascii=False) + "\n")
        proc.stdin.flush()
    waiting = {}
    last_tick, active = time.monotonic(), 0.0
    started = False
    send({"id": "initial-state", "type": "get_state"})
    try:
        while True:
            now = time.monotonic()
            if not waiting:
                active += now - last_tick
            last_tick = now
            if timeout is not None and active > timeout:
                raise subprocess.TimeoutExpired(proc.args, timeout)
            for key, item in list(waiting.items()):
                answer_file = item["folder"] / "answer.json"
                if answer_file.exists():
                    answer = json.loads(answer_file.read_text(encoding="utf-8"))
                    if answer.get("request_id") != key or not isinstance(answer.get("answer"), str) or not answer["answer"].strip():
                        raise ValueError("Malformed primary reply")
                    send({"type": "extension_ui_response", "id": key, "value": answer["answer"]})
                    item["record"]["status"] = "answered"
                    save(item["folder"] / "request.json", item["record"])
                    del waiting[key]
                    print(json.dumps({"event": "primary_answered", "request_id": key}, ensure_ascii=False), flush=True)
                elif now - item["since"] > reply_timeout:
                    raise ValueError("Primary reply timed out; question and exact session retained")
            try:
                line = incoming.get(timeout=0.1)
            except queue.Empty:
                continue
            if line is None:
                raise ValueError("Pi RPC stream ended before completion")
            events.write(line)
            events.flush()
            event = json.loads(line)
            if event.get("type") == "response":
                if not event.get("success"):
                    raise ValueError("Pi RPC command failed: " + str(event.get("error")))
                if event.get("id") == "initial-state":
                    state = event["data"]
                    events.write(json.dumps({"type": "session", "id": state["sessionId"]}) + "\n")
                    send({"id": "assignment", "type": "prompt", "message": prompt})
                if event.get("id") == "assignment" and event.get("data", {}).get("disposition") == "handled":
                    raise ValueError("Pi handled the prompt without starting the assigned work")
            elif event.get("type") == "agent_start":
                started = True
            elif event.get("type") == "extension_ui_request":
                title, key = event.get("title", ""), event["id"]
                if title.startswith("AGY_CONTEXT_REQUEST\n"):
                    try:
                        value = read_context(json.loads(title.split("\n", 1)[1]), context_root, route)
                    except (OSError, ValueError, subprocess.SubprocessError) as exc:
                        value = {"error": str(exc)}
                    send({"type": "extension_ui_response", "id": key, "value": json.dumps(value, ensure_ascii=False)})
                elif title.startswith("AGY_PRIMARY_REQUEST\n"):
                    if not re.fullmatch(r"[A-Za-z0-9_-]{1,128}", key):
                        raise ValueError("Invalid Pi request ID")
                    question = json.loads(title.split("\n", 1)[1])
                    folder = output / "questions" / key
                    record = {"request_id": key, "status": "waiting", "session": str(session), "question": question}
                    save(folder / "request.json", record)
                    waiting[key] = {"folder": folder, "record": record, "since": time.monotonic()}
                    print(json.dumps({"event": "primary_request", "run_dir": str(output), **record}, ensure_ascii=False), flush=True)
                elif (permission := bridge_permission(event)) is not None:
                    send({"type": "extension_ui_response", "id": key, "value": permission})
                elif event.get("method") in {"select", "confirm", "input", "editor"}:
                    send({"type": "extension_ui_response", "id": key, "cancelled": True})
            elif event.get("type") == "agent_settled" and started:
                if waiting:
                    raise ValueError("Pi settled with an unanswered primary request")
                break
        proc.stdin.close()
        proc.wait(timeout=15)
    finally:
        for item in waiting.values():
            item["record"]["status"] = "interrupted"
            save(item["folder"] / "request.json", item["record"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", required=True, type=Path)
    parser.add_argument("--request", required=True)
    parser.add_argument("--answer-file", required=True, type=Path)
    args = parser.parse_args()
    try:
        reply(args.run, args.request, args.answer_file.read_text(encoding="utf-8-sig"))
        print(json.dumps({"replied": args.request}))
    except (OSError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 1
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
