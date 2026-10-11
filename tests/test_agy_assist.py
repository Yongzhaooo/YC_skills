"""Text fidelity, explicit skills and local schema validation for the Pi route."""
import importlib.util
import json
from pathlib import Path
import tempfile
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT/"skills/agy-assist/scripts/agy_assist.py"
sys.path.insert(0, str(SCRIPT.parent))
spec = importlib.util.spec_from_file_location("agy_assist", SCRIPT)
agy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(agy)


class AgyAssistTests(unittest.TestCase):
    def test_source_fidelity_and_empty_input(self):
        with tempfile.TemporaryDirectory() as folder:
            prompt, source = Path(folder)/"prompt.txt", Path(folder)/"source.txt"
            prompt.write_text("润色", encoding="utf-8-sig")
            source.write_text("2026-09-16\n上限1500欧元，未支出。", encoding="utf-8")
            material = agy.make_prompt(prompt, [source])
            self.assertIn("1: 2026-09-16\n2: 上限1500欧元，未支出。", material)
            self.assertIn("source-1: source.txt", material)
            self.assertNotIn("\ufeff", material)
            prompt.write_text(" ", encoding="utf-8")
            with self.assertRaises(ValueError):
                agy.make_prompt(prompt, [source])

    def test_schema_validates_actual_value_and_skill_stays_text_only(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(agy.Path, "home", return_value=Path(folder)):
            for response, valid in [(' {"正文":"保留歧义"}', True), ('{"正文":3}', False), ('```json {} ```', False)]:
                with patch.object(agy, "run_pi", return_value={"response": response}) as run:
                    if valid:
                        out = agy.run_agy("task", None, schema={"type":"object", "properties":{"正文":{"type":"string"}}, "required":["正文"]}, skill="humanizer")
                        self.assertEqual(out["result"]["structured_output"], {"正文":"保留歧义"})
                        self.assertNotIn("response", out["result"])
                        self.assertTrue(run.call_args.kwargs["text_only"])
                        self.assertEqual(run.call_args.kwargs["skills"], ["humanizer"])
                    else:
                        with self.assertRaises(ValueError):
                            agy.run_agy("task", None, schema={"type":"object", "properties":{"正文":{"type":"string"}}})
            with self.assertRaises(ValueError):
                agy.run_agy("task", None, schema={"type":"not-a-json-type"})

    def test_cli_medium_and_explicit_model(self):
        with patch.object(agy, "make_prompt", return_value="task"), patch.object(agy, "run_agy", return_value={"ok":True}) as run, patch("builtins.print"):
            self.assertEqual(agy.main(["--prompt-file", "unused"]), 0)
            self.assertIsNone(run.call_args.args[1])
            self.assertEqual(run.call_args.kwargs["effort"], "medium")
            agy.main(["--prompt-file", "unused", "--model", "chosen", "--skill", "selected"])
            self.assertEqual(run.call_args.args[1], "chosen")
            self.assertEqual(run.call_args.kwargs["skill"], ["selected"])


if __name__ == "__main__":
    unittest.main()
