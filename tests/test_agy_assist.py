"""Offline regressions for the headless adapter; no model calls or extra dependencies."""

import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import Mock, patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/agy-assist/scripts/agy_assist.py"
spec = importlib.util.spec_from_file_location("agy_assist", SCRIPT)
agy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(agy)


def stream(result, *prefix):
    return "\n".join(json.dumps(event, ensure_ascii=False) for event in
                     [*prefix, {"event": "result", "result": result}])


class AgyAssistTests(unittest.TestCase):
    def test_cli_requires_and_forwards_selected_model(self):
        with patch("sys.stderr"), self.assertRaises(SystemExit) as missing:
            agy.main(["--prompt-file", "unused.txt"])
        self.assertEqual(missing.exception.code, 2)
        with patch.object(agy, "make_prompt", return_value="task"), patch.object(agy, "run_agy", return_value={"ok": True}) as run, patch("builtins.print"):
            self.assertEqual(agy.main(["--prompt-file", "unused.txt", "--model", "user-selected-model", "--effort", "high"]), 0)
            self.assertEqual(run.call_args.args[1], "user-selected-model")
            self.assertEqual(run.call_args.kwargs["effort"], "high")

    def test_accepts_chinese_and_prefers_separate_structured_output(self):
        result = {"status": "SUCCESS", "response": "```json\n杂项\n```",
                  "structured_output": {"正文": "保留歧义"}}
        self.assertEqual(agy.parse_result(stream(result), True)["structured_output"], {"正文": "保留歧义"})
        self.assertEqual(agy.parse_result(stream({"status": "SUCCESS", "response": "中文"}))["response"], "中文")
        for scalar in (False, 0, None):
            self.assertIs(agy.parse_result(stream({"status": "SUCCESS", "structured_output": scalar}), True)["structured_output"], scalar)

    def test_rejects_false_success_and_protocol_failures(self):
        bad_results = [
            {"status": "SUCCESS", "response": "  "},
            {"status": "SUCCESS", "response": "partial", "denied_actions": [{"action": "command"}]},
            {"status": "ERROR", "response": "partial", "error": "failed"},
            {"status": "WAITING", "response": "partial"},
            {"status": "SUCCESS", "response": "partial", "error": "failed"},
        ]
        for result in bad_results:
            with self.subTest(result=result), self.assertRaises(ValueError):
                agy.parse_result(stream(result))
        for raw in ("", "not json", "[]", '{"event":"init"}',
                    stream({"status": "SUCCESS", "response": "ok"}) + "\n" + stream({"status": "SUCCESS", "response": "ok"})):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                agy.parse_result(raw)
        with self.assertRaisesRegex(ValueError, "structured_output"):
            agy.parse_result(stream({"status": "SUCCESS", "response": "{}"}), True)
        with self.assertRaisesRegex(ValueError, "step failed"):
            agy.parse_result(stream({"status": "SUCCESS", "response": "partial"},
                                    {"event": "step_update", "step_update": {"state": "ERROR", "tool_name": "run_command"}}))

    def test_long_unicode_input_uses_stdin_and_preserves_exact_session(self):
        prompt = '中文、引号"、美元$、换行\n' * 6000
        proc = Mock(returncode=0)
        proc.communicate.return_value = (stream({"status": "SUCCESS", "response": "完成"}), "")
        with patch.object(agy.shutil, "which", return_value="agy.exe"), patch.object(agy.subprocess, "Popen", return_value=proc) as launch:
            output = agy.run_agy(prompt, "test-model", conversation="exact-id")
        args = launch.call_args.args[0]
        self.assertNotIn(prompt, args)
        self.assertNotIn("--dangerously-skip-permissions", args)
        self.assertNotIn("--continue", args)
        self.assertEqual(args[args.index("--conversation") + 1], "exact-id")
        self.assertEqual(json.loads(proc.communicate.call_args.args[0])["message"]["content"], prompt)
        self.assertEqual(launch.call_args.kwargs["encoding"], "utf-8")
        self.assertTrue(output["ok"])

    def test_schema_goes_to_file_and_cli_errors_fail(self):
        proc = Mock(returncode=0)
        def communicate(payload, timeout):
            args = launch.call_args.args[0]
            schema_file = Path(args[args.index("--json-schema") + 1])
            self.assertEqual(json.loads(schema_file.read_text(encoding="utf-8")), {"type": "object"})
            self.assertIn('"type": "object"', json.loads(payload)["message"]["content"])
            return stream({"status": "SUCCESS", "structured_output": {}, "response": "duplicate draft"}), ""
        proc.communicate.side_effect = communicate
        with patch.object(agy.shutil, "which", return_value="agy.exe"), patch.object(agy.subprocess, "Popen", return_value=proc) as launch:
            output = agy.run_agy("task", "test-model", schema={"type": "object"})
            self.assertTrue(output["ok"])
            self.assertNotIn("response", output["result"])
        proc.returncode = 1
        proc.communicate.side_effect = None
        proc.communicate.return_value = ("", "authentication required")
        with patch.object(agy.shutil, "which", return_value="agy.exe"), patch.object(agy.subprocess, "Popen", return_value=proc):
            with self.assertRaisesRegex(RuntimeError, "authentication required"):
                agy.run_agy("task", "test-model")

    def test_timeout_stops_owned_process_without_retry(self):
        proc = Mock()
        proc.communicate.side_effect = subprocess.TimeoutExpired("agy", 1)
        with patch.object(agy.shutil, "which", return_value="agy.exe"), patch.object(agy.subprocess, "Popen", return_value=proc) as launch, patch.object(agy, "stop_process") as stop:
            with self.assertRaisesRegex(RuntimeError, "timed out"):
                agy.run_agy("task", "test-model", timeout=1)
            stop.assert_called_once_with(proc)
            self.assertEqual(launch.call_count, 1)
        for timeout in (0, -1, float("nan"), float("inf")):
            with self.subTest(timeout=timeout), self.assertRaises(ValueError):
                agy.run_agy("task", "test-model", timeout=timeout)

    def test_source_labels_line_numbers_bom_and_empty_input(self):
        with tempfile.TemporaryDirectory() as folder:
            prompt = Path(folder) / "prompt.txt"
            source = Path(folder) / "source.txt"
            prompt.write_text("润色", encoding="utf-8-sig")
            source.write_text("2026-09-16\n上限1500欧元，未支出。", encoding="utf-8")
            material = agy.make_prompt(prompt, [source])
            self.assertIn("source-1: source.txt", material)
            self.assertIn("1: 2026-09-16\n2: 上限1500欧元，未支出。", material)
            self.assertNotIn("\ufeff", material)
            prompt.write_text(" ", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "empty"):
                agy.make_prompt(prompt, [source])


if __name__ == "__main__":
    unittest.main()
