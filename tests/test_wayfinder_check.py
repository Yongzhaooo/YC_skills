from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "wayfinder" / "scripts" / "wayfinder_check.py"
spec = importlib.util.spec_from_file_location("wayfinder_check", SCRIPT)
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)

BIG = "中" * 3500
SMALL = "# map\n\n**Project outcome:** ship it.\n"
TRACE = "Traceback (most recent call last):\n"


def fence(lines: int, marker: str = "```") -> str:
    return marker + "\n" + "line\n" * lines + marker + "\n"


def test_token_estimate_weights_ascii_lower_than_cjk():
    assert check.tokens("abcd") == 1
    assert check.tokens("中文") == 2
    assert check.tokens("a b\n\tc d") == 1


def test_growth_over_budget_blocks_but_inherited_bloat_only_notices():
    assert check.evaluate(BIG, SMALL)["blocking"]
    assert check.evaluate(BIG, None)["blocking"]
    kept = check.evaluate(BIG, BIG + "中")
    assert kept["blocking"] == [] and kept["notices"]
    assert check.evaluate(SMALL, None) == {"tokens": check.tokens(SMALL), "budget": 3000, "blocking": [], "notices": []}


def test_budget_comes_from_the_baseline():
    raised = "<!-- wayfinder-budget: 5000 -->\n"
    assert check.evaluate(raised + BIG, None)["blocking"] == []
    assert check.evaluate(raised + BIG, raised)["blocking"] == []
    assert check.evaluate(raised + BIG, SMALL)["blocking"]  # cannot raise its own limit


def test_log_lines_block_only_when_they_grow():
    java = SMALL + "    at com.megacrit.cardcrawl.Foo.bar(Foo.java:12)\n"
    assert check.evaluate(SMALL + TRACE, SMALL)["blocking"]
    assert check.evaluate(java, SMALL)["blocking"]
    assert check.evaluate(SMALL + fence(11), SMALL)["blocking"]
    assert check.evaluate(SMALL + fence(11, "~~~"), SMALL)["blocking"]
    assert check.evaluate(SMALL + "```\n" + TRACE + "```\n", SMALL)["blocking"]  # trace in short block
    assert check.evaluate(SMALL + "```\n" + "line\n" * 11, SMALL)["blocking"]  # unclosed block
    assert check.evaluate(SMALL + fence(11) + fence(11), SMALL + fence(11))["blocking"]  # duplicated block
    mixed = "```text\n" + "line\n" * 6 + "~~~\n" + "line\n" * 6 + "```\n"
    assert check.evaluate(SMALL + mixed, SMALL)["blocking"]  # ~~~ does not close a ``` block
    nested = "````\n```\n" + "line\n" * 10 + "````\n"
    assert check.evaluate(SMALL + nested, SMALL)["blocking"]  # ``` does not close a ```` block
    assert check.evaluate(SMALL + fence(3), SMALL)["blocking"] == []
    assert check.evaluate(SMALL + fence(11), SMALL + fence(12))["blocking"] == []  # shrinking a block
    kept = check.evaluate(java + "- new note\n", java)
    assert kept["blocking"] == [] and kept["notices"]


def _hook(event: str, tmp: Path, payload: dict) -> dict | None:
    env = {**os.environ, "TMP": str(tmp), "TEMP": str(tmp), "TMPDIR": str(tmp)}
    out = subprocess.run([sys.executable, str(SCRIPT), "--hook", event], input=json.dumps(payload).encode("utf-8"),
                         capture_output=True, env=env, check=True).stdout.decode("utf-8").strip()
    return json.loads(out) if out else None


def _repo(tmp_path: Path, text: str | None) -> Path:
    repo = tmp_path / "repo"
    (repo / "docs").mkdir(parents=True)
    (repo / "src").mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    if text is not None:
        (repo / "docs" / "wayfinder.md").write_text(text, encoding="utf-8")
    return repo


def test_stop_blocks_only_growth_made_since_the_turn_snapshot(tmp_path: Path):
    repo = _repo(tmp_path, BIG)
    wayfinder = repo / "docs" / "wayfinder.md"
    state = tmp_path / "state"
    state.mkdir()
    agent = {"cwd": str(repo / "src"), "session_id": "s1"}

    start = _hook("session-start", state, agent)
    assert "over its 3000-token budget" in start["hookSpecificOutput"]["additionalContext"]
    assert _hook("stop", state, agent) is None  # untouched this turn

    wayfinder.write_text(BIG + "中" * 50, encoding="utf-8")
    blocked = _hook("stop", state, agent)
    assert blocked["decision"] == "block" and "+50 this change" in blocked["reason"]
    assert _hook("stop", state, agent) is None  # one reminder per outcome
    assert _hook("stop", state, {**agent, "stop_hook_active": True}) is None

    _hook("user-prompt-submit", state, agent)
    wayfinder.write_text(BIG, encoding="utf-8")
    assert _hook("stop", state, agent) is None  # shrinking is always allowed


def test_stop_without_a_snapshot_gives_no_verdict(tmp_path: Path):
    # Earlier uncommitted growth must not be blamed on a turn the hook never saw start.
    repo = _repo(tmp_path, SMALL)
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
    subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@e", "commit", "-qm", "init"], cwd=repo, check=True)
    (repo / "docs" / "wayfinder.md").write_text(BIG, encoding="utf-8")
    assert _hook("stop", tmp_path, {"cwd": str(repo), "session_id": "fresh"}) is None


def test_map_created_during_the_turn_is_judged_from_empty(tmp_path: Path):
    repo = _repo(tmp_path, None)
    agent = {"cwd": str(repo / "src"), "session_id": "s2"}
    _hook("user-prompt-submit", tmp_path, agent)
    (repo / "docs" / "wayfinder.md").write_text(BIG, encoding="utf-8")
    assert _hook("stop", tmp_path, agent)["decision"] == "block"


def test_map_lookup_stops_at_the_repository_root(tmp_path: Path):
    outer = tmp_path / "outer"
    (outer / "docs").mkdir(parents=True)
    (outer / "docs" / "wayfinder.md").write_text(SMALL, encoding="utf-8")
    inner = outer / "inner"
    inner.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=inner, check=True)
    agent = {"cwd": str(inner), "session_id": "s3"}
    _hook("user-prompt-submit", tmp_path, agent)
    (inner / "docs").mkdir()
    (inner / "docs" / "wayfinder.md").write_text(BIG, encoding="utf-8")
    assert _hook("stop", tmp_path, agent)["decision"] == "block"


def test_antigravity_hooks_cover_every_workspace(tmp_path: Path):
    repo = _repo(tmp_path, SMALL)
    other = tmp_path / "other"
    (other / "docs").mkdir(parents=True)
    (other / "docs" / "wayfinder.md").write_text(SMALL, encoding="utf-8")
    agy = {"conversationId": "c1", "workspacePaths": [str(repo), str(other)]}

    assert _hook("agy-pre-invocation", tmp_path, agy) == {"injectSteps": []}
    (other / "docs" / "wayfinder.md").write_text(SMALL + TRACE, encoding="utf-8")
    result = _hook("agy-stop", tmp_path, agy)
    assert result["decision"] == "continue" and "pasted log lines" in result["reason"]
    assert _hook("agy-stop", tmp_path, agy) == {}


def test_hooks_ignore_missing_session_or_map(tmp_path: Path):
    assert _hook("stop", tmp_path, {"cwd": str(tmp_path), "session_id": "s"}) is None
    repo = _repo(tmp_path, BIG)
    assert _hook("session-start", tmp_path, {"cwd": str(repo)}) is None
    assert _hook("agy-stop", tmp_path, {"workspacePaths": [str(repo)]}) == {}
