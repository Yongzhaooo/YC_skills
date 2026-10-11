"""Pi transport boundaries with a real local child process and no model calls."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills/agy-execution/scripts"
sys.path.insert(0, str(SCRIPTS))
import pi_transport as pi


def events(response="中文完成", **changes):
    message = {"role": "assistant", "content": [{"type": "text", "text": response}],
               "stopReason": "stop", "provider": "antigravity-acp", "model": "test-model"}
    message.update(changes)
    return [{"type": "session", "id": "exact-id"},
            {"type": "message_end", "message": message},
            {"type": "agent_settled", "aborted": False}]


class ExecutionTests(unittest.TestCase):
    def test_settled_final_result_and_false_success(self):
        with tempfile.TemporaryDirectory() as folder:
            log = Path(folder) / "events.jsonl"
            cases = [events(""), events(stopReason="error"), events()[:-1],
                     events("Usage Limit Reached\nYou have reached your current quota for this period. Your limit will reset in 2 hours."),
                     events() + [{"type": "agent_settled", "aborted": True}],
                     events() + [{"type": "extension_error", "error": "broken"}],
                     events() + [{"type": "tool_execution_end", "result": {"details": {
                         "kind": "pi-antigravity-acp-permission-v1", "cancelled": True}}}]]
            for case in cases:
                log.write_text("\n".join(json.dumps(e) for e in case), encoding="utf-8")
                with self.subTest(case=case), self.assertRaises(ValueError):
                    pi.parse_events(log)
            good = events("合法\u2028中文")
            log.write_text("\n".join(json.dumps(e, ensure_ascii=False) for e in good), encoding="utf-8")
            self.assertEqual(pi.parse_events(log)["response"], "合法\u2028中文")
            good.insert(1, {"type": "tool_execution_start", "toolName": "read"})
            log.write_text("\n".join(json.dumps(e) for e in good), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Text-only"):
                pi.parse_events(log, text_only=True)

    def test_utf8_stdin_scoped_permissions_and_exact_resume(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            extension = root / "extension.ts"
            extension.write_text("", encoding="utf-8")
            fake = root / "fake.py"
            fake.write_text("import json,sys\nfrom pathlib import Path\n"
                "prompt=sys.stdin.read(); assert '中文' in prompt\n"
                "p=Path(sys.argv[sys.argv.index('--session')+1])\n"
                "p.write_text(json.dumps({'type':'session','cwd':str(Path.cwd())})+'\\n',encoding='utf-8')\n"
                "for e in " + repr(events()) + ": print(json.dumps(e,ensure_ascii=False))\n", encoding="utf-8")
            route = {"command": [sys.executable, str(fake)], "extension": str(extension),
                     "model": "test-model", "effort": "medium"}
            with patch.object(pi, "load_route", return_value=route):
                result = pi.run_pi("中文\n$() harmless", cwd=root, output=root/"run", timeout=10)
                session = result["conversation_id"]
                self.assertEqual(result["response"], "中文完成")
                config = root/"run/session.agent/antigravity-acp-provider/config.json"
                self.assertEqual(json.loads(config.read_text())["permissions"], "default")
                pi.run_pi("中文继续", cwd=root, output=root/"resume", conversation=session,
                          auto_approve=True, timeout=10)
                self.assertEqual(json.loads(config.read_text())["permissions"], "yolo")
                process = json.loads((root/"resume/process.json").read_text())
                self.assertEqual(process["args"][process["args"].index("--session")+1], session)
                summary = json.loads((root/"resume/summary.json").read_text())
                self.assertTrue(summary["invocation_complete"])
                self.assertFalse(summary["delivery_accepted"])
                with self.assertRaises(FileExistsError):
                    pi.run_pi("中文", cwd=root, output=root/"run")
                with self.assertRaises(ValueError):
                    pi.run_pi("中文", cwd=root/"run", output=root/"bad", conversation=session)

    def test_nonzero_timeout_and_route_mismatch(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            extension = root/"extension.ts"
            extension.touch()
            for name, source, timeout, error in [
                ("exit", "import sys; sys.stdin.read(); sys.exit(7)", 10, ValueError),
                ("timeout", "import time; time.sleep(30)", 0.1, subprocess.TimeoutExpired),
                ("wrong-model", "import json; [print(json.dumps(e)) for e in " + repr(events(model="wrong")) + "]", 10, ValueError)]:
                route = {"command": [sys.executable, "-c", source], "extension": str(extension), "model": "test-model"}
                with patch.object(pi, "load_route", return_value=route), self.assertRaises(error):
                    pi.run_pi("task", cwd=root, output=root/name, timeout=timeout)
                summary = json.loads((root/name/"summary.json").read_text())
                self.assertFalse(summary["invocation_complete"])
                self.assertIsNotNone(summary["exit_code"])
            for timeout in (0, -1, float("nan")):
                with self.assertRaises(ValueError):
                    pi.run_pi("task", cwd=root, output=root/"invalid", timeout=timeout)
            with self.assertRaises(ValueError):
                pi.run_pi("task", cwd=root, output=root/"invalid", text_only=True, auto_approve=True)

    def test_transport_copies_match_and_selected_skill(self):
        for helper in ("pi_transport.py", "pi_accounts.py", "pi_cli_quota.ps1"):
            source = (SCRIPTS/helper).read_bytes()
            self.assertEqual(source, (ROOT/"skills/agy-assist/scripts"/helper).read_bytes())
        with tempfile.TemporaryDirectory() as folder:
            skill = Path(folder)/"SKILL.md"
            skill.write_text("text only", encoding="utf-8")
            self.assertEqual(pi.resolve_skill(str(skill.parent)), skill)
            with self.assertRaises(ValueError):
                pi.resolve_skill("missing-uninstalled-skill")


if __name__ == "__main__":
    unittest.main()
