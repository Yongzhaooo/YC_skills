"""Focused CLI boundary checks; no paid AGY call and no product modifications."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "skills/agy-execution/scripts/agy_execution.py"
SPEC = importlib.util.spec_from_file_location("agy_execution", SCRIPT)
agy = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(agy)


class ExecutionTests(unittest.TestCase):
    def test_terminal_failures_and_delivery_boundary(self):
        good = {"status": "SUCCESS", "response": "Implemented; tests passed", "conversation_id": "example-id"}
        with tempfile.TemporaryDirectory() as temp:
            log = Path(temp) / "events.jsonl"
            for result in (dict(good, response=""), dict(good, denied_actions=[{"action": "command"}]),
                           dict(good, status="ERROR"), dict(good, error="failed"), None):
                log.write_text(json.dumps({"event": "result", "result": result}), encoding="utf-8")
                with self.assertRaises(ValueError):
                    agy.terminal_result(log)
            log.write_text(json.dumps({"event": "result", "result": good}), encoding="utf-8")
            self.assertEqual(agy.terminal_result(log), good)
            log.write_text(log.read_text(encoding="utf-8") + "\n" + log.read_text(encoding="utf-8"), encoding="utf-8")
            with self.assertRaises(ValueError):
                agy.terminal_result(log)

    def test_utf8_process_evidence_and_explicit_approval(self):
        real_popen = subprocess.Popen
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            prompt = root / "任务.txt"
            prompt.write_text("实现并测试中文任务；只写临时目录", encoding="utf-8")
            options = SimpleNamespace(cwd=root, prompt_file=prompt, output_dir=root / "run",
                                      model=None, effort=None, conversation=None, auto_approve=False, timeout=10)
            self.assertNotIn("--dangerously-skip-permissions", agy.command("agy", options))
            options.auto_approve = True
            options.conversation = "selected-id"
            self.assertIn("--dangerously-skip-permissions", agy.command("agy", options))
            self.assertIn("selected-id", agy.command("agy", options))
            fake = ('import json,sys; p=json.loads(sys.stdin.readline()); '
                    'assert "中文任务" in p["message"]["content"]; '
                    'print(json.dumps({"event":"result","result":{"status":"SUCCESS",'
                    '"response":"已实现","conversation_id":"selected-id"}},ensure_ascii=False))')
            def launch(args, **kwargs):
                return real_popen([sys.executable, "-c", fake], **kwargs)
            with patch.object(agy.shutil, "which", return_value="agy"), patch.object(agy.subprocess, "Popen", side_effect=launch):
                summary = agy.run(options)
                self.assertTrue(summary["invocation_complete"])
                self.assertFalse(summary["delivery_accepted"])
                self.assertEqual(summary["exit_code"], 0)
                self.assertEqual(json.loads((options.output_dir / "result.json").read_text(encoding="utf-8"))["response"], "已实现")
                with self.assertRaises(FileExistsError):
                    agy.run(options)

    def test_nonzero_exit_and_timeout_preserve_failure_evidence(self):
        real_popen = subprocess.Popen
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            prompt = root / "task.txt"
            prompt.write_text("Only a local test", encoding="utf-8")
            for name, source, expected, timeout in [
                ("nonzero", "import sys; sys.stdin.read(); sys.exit(7)", ValueError, 10),
                ("timeout", "import time; time.sleep(30)", subprocess.TimeoutExpired, 0.1),
            ]:
                options = SimpleNamespace(cwd=root, prompt_file=prompt, output_dir=root / name,
                                          model=None, effort=None, conversation=None, auto_approve=False, timeout=timeout)
                def launch(args, **kwargs):
                    # Let stop_process use the real native taskkill when testing timeout.
                    if args[0] == "taskkill":
                        return real_popen(args, **kwargs)
                    return real_popen([sys.executable, "-c", source], **kwargs)
                with patch.object(agy.shutil, "which", return_value="agy"), patch.object(agy.subprocess, "Popen", side_effect=launch):
                    with self.assertRaises(expected):
                        agy.run(options)
                summary = json.loads((options.output_dir / "summary.json").read_text(encoding="utf-8"))
                self.assertFalse(summary["invocation_complete"])
                self.assertFalse(summary["delivery_accepted"])
                self.assertIsNotNone(summary["exit_code"])
                self.assertIn("error", summary)
                if name == "nonzero":
                    self.assertEqual(summary["exit_code"], 7)


if __name__ == "__main__":
    unittest.main()
