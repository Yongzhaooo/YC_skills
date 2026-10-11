"""Read-only context boundaries and real pipe question/reply lifecycle."""
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/agy-execution/scripts"))
import pi_dialogue as dialogue


class DialogueTests(unittest.TestCase):
    def test_permission_only_known_bridge_calls_once(self):
        event = {"method": "select", "title": "pi-bridge_pi_inspect_context\n\n" + json.dumps(
            {"kind": "other", "rawInput": {"arguments": {"action": "discover"}}}),
            "options": ["1. Allow Always [allow always]", "2. Allow [allow once]", "3. Deny [reject once]"]}
        self.assertEqual(dialogue.bridge_permission(event), "2. Allow [allow once]")
        for title in ["run_command\n\n{}", "pi-bridge_pi_inspect_context\n\ninvalid",
                      "pi-bridge_pi_inspect_context\n\n" + json.dumps(
                          {"kind": "execute", "rawInput": {"arguments": {"action": "discover"}}}),
                      "pi-bridge_pi_inspect_context\n\n" + json.dumps(
                          {"kind": "other", "rawInput": {"arguments": {"action": "delete"}}})]:
            self.assertIsNone(dialogue.bridge_permission({**event, "title": title}))

    def test_context_absent_scoped_and_cross_project_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertFalse(dialogue.read_context({"action": "discover"}, root, {})["bench"])
            self.assertFalse(dialogue.read_context({"action": "wayfinder"}, root, {})["available"])
            (root / "docs").mkdir()
            (root / "docs/wayfinder.md").write_text("当前任务", encoding="utf-8")
            (root / "bench-project.json").write_text('{"project":"selected"}', encoding="utf-8")
            self.assertEqual(dialogue.read_context({"action": "wayfinder"}, root, {})["text"], "当前任务")
            route = {"bench_command": ["python", "bench.py"]}
            with patch.object(dialogue.subprocess, "run") as run:
                run.return_value = subprocess.CompletedProcess([], 0, json.dumps({"hits": [
                    {"project": "selected", "text": "evidence"}]}))
                result = dialogue.read_context({"action": "bench_search", "query": "conflict"}, root, route)
                self.assertEqual(result["hits"][0]["text"], "evidence")
                self.assertEqual(run.call_args.args[0][-4:], ["--search", "conflict", "--project", "selected"])
                run.return_value.stdout = '{"hits":[{"project":"another","text":"private"}]}'
                with self.assertRaises(ValueError):
                    dialogue.read_context({"action": "bench_search", "query": "conflict"}, root, route)

    def exercise_rpc(self, answer):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            child = '''import json,sys
def send(value): print(json.dumps(value),flush=True)
assert json.loads(sys.stdin.readline())["type"] == "get_state"
send({"type":"response","id":"initial-state","success":True,"data":{"sessionId":"exact"}})
assert json.loads(sys.stdin.readline())["message"] == "中文"
send({"type":"agent_start"})
send({"type":"extension_ui_request","id":"request-1","method":"input","title":"AGY_PRIMARY_REQUEST\\n"+json.dumps({"question":"7 or 8?"})})
response=json.loads(sys.stdin.readline())
assert response["id"] == "request-1" and response["value"] == "7"
send({"type":"agent_settled"})
'''
            proc = subprocess.Popen([sys.executable, "-u", "-c", child], stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
            errors = []
            def respond():
                try:
                    record = root / "questions/request-1/request.json"
                    deadline = time.monotonic() + 5
                    while not record.exists() and time.monotonic() < deadline:
                        time.sleep(.01)
                    time.sleep(.3)  # Waiting for the primary must not spend the active timeout.
                    dialogue.reply(root, "request-1", "7")
                    try:
                        dialogue.reply(root, "request-1", "8")
                        errors.append("duplicate reply accepted")
                    except (ValueError, FileExistsError):
                        pass
                except Exception as exc:
                    errors.append(str(exc))
            worker = threading.Thread(target=respond) if answer else None
            if worker:
                worker.start()
            try:
                with patch("sys.stdout", new=io.StringIO()):
                    if answer:
                        dialogue.converse(proc, "中文", io.StringIO(), output=root, session=root/"session.jsonl",
                                          timeout=.25, context_root=root, route={}, reply_timeout=3)
                    else:
                        with self.assertRaisesRegex(ValueError, "reply timed out"):
                            dialogue.converse(proc, "中文", io.StringIO(), output=root, session=root/"session.jsonl",
                                              timeout=3, context_root=root, route={}, reply_timeout=.05)
                record = json.loads((root / "questions/request-1/request.json").read_text())
                self.assertEqual(record["status"], "answered" if answer else "interrupted")
                if not answer:
                    with self.assertRaises(ValueError):
                        dialogue.reply(root, "request-1", "7")
            finally:
                if worker:
                    worker.join(5)
                if proc.poll() is None:
                    proc.kill()
                proc.wait()
                proc.stdin.close()
                proc.stdout.close()
                proc.stderr.close()
            self.assertFalse(errors, errors)

    def test_same_session_question_answer_and_duplicate_rejection(self):
        self.exercise_rpc(True)

    def test_unanswered_question_retains_interrupted_record(self):
        self.exercise_rpc(False)


if __name__ == "__main__":
    unittest.main()
