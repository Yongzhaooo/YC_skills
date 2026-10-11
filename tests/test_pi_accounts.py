"""ACP account selection, secure snapshots, and quota-only continuation."""
from contextlib import nullcontext
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/agy-execution/scripts"))
import pi_accounts as accounts
import pi_transport as pi


class AccountTests(unittest.TestCase):
    def test_selection_excludes_unknown_zero_exhausted_and_unenrolled(self):
        rows = [dict(profile="a", remaining_5h=90, remaining_weekly=20),
                dict(profile="b", remaining_5h=90, remaining_weekly=40),
                dict(profile="c", remaining_5h=100, remaining_weekly=100),
                dict(profile="d", remaining_5h=100, remaining_weekly=None),
                dict(profile="e", remaining_5h=100, remaining_weekly=0)]
        self.assertEqual(accounts.select_candidate(rows, ["a", "b", "d", "e"], []), "b")
        self.assertEqual(accounts.select_candidate(rows, ["a", "b"], ["b"]), "a")
        with self.assertRaises(ValueError):
            accounts.select_candidate(rows, ["d", "e"], [])
        for text in ("429 rate limit", "quota low", "RESOURCE_EXHAUSTED", "normal answer"):
            self.assertFalse(pi.quota_exhausted(text))
        self.assertTrue(pi.quota_exhausted("Usage Limit Reached\nYou have reached your current quota. Your limit will reset soon."))

    @unittest.skipUnless(os.name == "nt", "Windows DPAPI")
    def test_encrypted_snapshots_switch_readback_unknown_settings_and_lock(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            pool = accounts.AccountPool({"store": str(root/"profiles")}, auth_dir=root/"auth")
            def login(token):
                accounts.atomic_json(root/"auth/acp_token.json", {"client_id": "test", "refresh_token": token})
                accounts.atomic_json(root/"auth/settings.json", {"auth": {"type": "oauth-personal"}, "keep": "unchanged"})
            with patch.object(pool, "quiet"):
                login("fake-private-one")
                self.assertEqual(pool.save_current("one"), "one")
                self.assertNotIn(b"fake-private-one", (root/"profiles/one.dpapi").read_bytes())
                with self.assertRaises(ValueError):
                    pool.save_current("duplicate")
                login("fake-private-two")
                pool.save_current("two")
                pool.switch("one")
                self.assertEqual(pool.current(), "one")
                self.assertEqual(json.loads((root/"auth/settings.json").read_text())["keep"], "unchanged")
                self.assertEqual(pool.names(), ["one", "two"])
                with pool.locked():
                    with self.assertRaises(ValueError):
                        with pool.locked():
                            pass

    def test_skills_multiselect_references_and_delegation_rejection(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            selected = []
            for name in ["clean-text", "check-facts", "agy-execution"]:
                p = root/name/"SKILL.md"
                p.parent.mkdir()
                p.write_text(f"---\nname: {name}\n---\nInstructions for {name}", encoding="utf-8")
                selected.append(str(p))
            ref = root/"clean-text/reference.md"
            ref.write_text("Keep negations", encoding="utf-8")
            paths, text, manifest = pi.skill_bundle(selected[:2], [str(ref)])
            self.assertEqual(len(paths), 2)
            self.assertIn("Keep negations", text[-1])
            self.assertEqual(len(manifest), 3)
            with self.assertRaises(ValueError):
                pi.skill_bundle(selected)
            with self.assertRaises(ValueError):
                pi.skill_bundle(selected[:1], [selected[1]])

    def test_quota_recovery_retains_route_skills_permissions_and_session(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)/"run"
            pool = Mock()
            pool.locked.return_value = nullcontext()
            pool.current.return_value = "one"
            pool.names.return_value = ["one", "two"]
            pool.quotas.return_value = [{"profile": "two", "remaining_5h": 80, "remaining_weekly": 60}]
            pool.switch.return_value = "two"
            calls = []
            def invoke(prompt, **options):
                calls.append((prompt, options))
                output = Path(options["output"])
                output.mkdir(parents=True)
                session = root/"session.jsonl"
                session.write_text(json.dumps({"type": "session", "cwd": folder})+"\n", encoding="utf-8")
                pi.save(output/"summary.json", {"invocation_complete": len(calls)>1, "delivery_accepted": False,
                                               "exit_code": 0, "conversation_id": str(session)})
                if len(calls) == 1:
                    raise pi.QuotaExhausted("quota")
                return {"response": "finished", "conversation_id": str(session)}
            with patch.object(pi, "load_route", return_value={"rotation": {"enabled": True}}), \
                    patch.object(accounts, "AccountPool", return_value=pool), patch.object(pi, "_run_pi_once", side_effect=invoke):
                result = pi.run_pi("original", cwd=folder, output=root, model="chosen", effort="high",
                                   auto_approve=True, skills=["selected"])
            self.assertEqual(result["account_profile"], "two")
            self.assertIn("do not repeat", calls[1][0])
            self.assertEqual(calls[1][1]["conversation"], str(root/"session.jsonl"))
            for key in ["model", "effort", "auto_approve", "skills"]:
                self.assertEqual(calls[0][1][key], calls[1][1][key])
            pool.switch.assert_called_once_with("two")
            self.assertTrue(json.loads((root/"summary.json").read_text())["invocation_complete"])

    def test_enroll_matches_stable_identity_and_refuses_ambiguous_mapping(self):
        pool = accounts.AccountPool({})
        snapshot = {"token": {"refresh_token": "fake"}}
        identity = {"sub": "stable-id", "email": "daily@example.test"}
        with patch.object(pool, "quiet"), patch.object(pool, "capture", return_value=snapshot), \
                patch.object(pool, "names", return_value=[]), patch.object(pool, "current", return_value=None), \
                patch.object(pool, "write") as write, patch.object(accounts, "google_identity", return_value=identity), \
                patch.object(accounts, "cli_identities", return_value=[{"profile": "2", **identity}]) as profiles:
            self.assertEqual(pool.enroll()["profile"], "2")
            self.assertEqual(write.call_args.args[1]["identity"], identity)
            profiles.return_value = [{"profile": "1", **identity}, {"profile": "2", **identity}]
            with self.assertRaises(ValueError):
                pool.enroll()
            profiles.return_value = []
            with self.assertRaises(ValueError):
                pool.enroll()
            self.assertEqual(write.call_count, 1)

    def test_normal_failures_never_rotate(self):
        pool = Mock()
        pool.locked.return_value = nullcontext()
        pool.current.return_value = "one"
        with tempfile.TemporaryDirectory() as folder, \
                patch.object(pi, "load_route", return_value={"rotation": {"enabled": True}}), \
                patch.object(accounts, "AccountPool", return_value=pool), \
                patch.object(pi, "_run_pi_once", side_effect=ValueError("429 rate limit")):
            with self.assertRaises(ValueError):
                pi.run_pi("task", cwd=folder, output=Path(folder)/"run")
        pool.switch.assert_not_called()
        pool.quotas.assert_not_called()


if __name__ == "__main__":
    unittest.main()
