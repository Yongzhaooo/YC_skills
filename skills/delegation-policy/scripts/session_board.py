#!/usr/bin/env python3
"""Prepare and validate isolated-session boards without touching session runtime state."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
import uuid
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


SCHEMA_VERSION = 1
CREATE_THREAD_MODELS = {
    "deepseek-v4-flash",
    "deepseek-v4-pro",
    # "glm-5.2" -- banned 2026-07-20: poor Codex adaptation; re-enable after verified compatibility
    "kimi-k2.7-code",
}
MODEL_SOULS = {
    "deepseek-v4-flash": "Mercury",
    "deepseek-v4-pro": "Janitor",
    # "glm-5.2": "Janitor",  -- banned 2026-07-20
    "kimi-k2.7-code": "Janitor",
}
SOULS_DIR = Path(__file__).resolve().parent.parent / "souls"


def _load_soul_capsule(soul: str) -> str:
    """Load a soul capsule from its standalone file."""
    soul_file = {"Janitor": "janitor.md", "Mercury": "mercury.md"}.get(soul)
    if not soul_file:
        raise BoardError(f"unknown soul: {soul}")
    path = SOULS_DIR / soul_file
    try:
        return path.read_text(encoding="utf-8").rstrip("\n")
    except (OSError, UnicodeError) as exc:
        raise BoardError(f"cannot load soul capsule for {soul}: {exc}") from exc
BOARD_FILES = {"request.md", "thread.json", "result.md", "done.json"}
COMPLETION_STATES = {"completed", "blocked", "failed"}
SAFE_ID = re.compile(r"[a-z0-9][a-z0-9._-]{0,63}")
SHA256 = re.compile(r"sha256:[0-9a-f]{64}")
UTC_DEADLINE = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,7})?Z")
REQUEST_HASH_LINE = re.compile(r"^Request SHA256: `sha256:[0-9a-f]{64}`\n", re.MULTILINE)
DISALLOWED_CONTROL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")

THREAD_FIELDS = {
    "schema_version",
    "run_id",
    "task_id",
    "model",
    "thread_id",
    "host_id",
    "temporary",
    "created_at",
    "request_sha256",
    "board_path",
    "write_ownership",
    "deadline",
}
DONE_FIELDS = {
    "schema_version",
    "run_id",
    "task_id",
    "model",
    "request_sha256",
    "result_sha256",
    "completion_state",
    "changed_files",
    "validation",
    "rollback",
    "unresolved",
}


class BoardError(ValueError):
    """A board violates the isolated-session contract."""


def _normalized_text(value: str) -> str:
    return value.replace("\r\n", "\n").replace("\r", "\n")


def _require_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise BoardError(f"{label} must be a non-empty string")
    return value.strip()


def _utc_deadline(value: Any, label: str = "deadline") -> tuple[str, dt.datetime]:
    text = _require_text(value, label)
    if not UTC_DEADLINE.fullmatch(text):
        raise BoardError(f"{label} must be an ISO-8601 UTC timestamp ending in Z")
    normalized = text[:-1]
    if "." in normalized:
        head, fraction = normalized.rsplit(".", 1)
        normalized = head + "." + fraction[:6].ljust(6, "0")
    try:
        parsed = dt.datetime.fromisoformat(normalized).replace(tzinfo=dt.timezone.utc)
    except ValueError as exc:
        raise BoardError(f"{label} must be a valid UTC timestamp") from exc
    return text, parsed


def _safe_id(value: str, label: str) -> str:
    if not isinstance(value, str) or not SAFE_ID.fullmatch(value):
        raise BoardError(f"{label} must be a safe identifier")
    return value


def _safe_repo_path(value: str, label: str) -> str:
    if not isinstance(value, str):
        raise BoardError(f"{label} must be a repository-relative path")
    normalized = value.replace("\\", "/")
    path = PurePosixPath(normalized)
    if (
        not normalized
        or path.is_absolute()
        or normalized.startswith("/")
        or re.match(r"^[A-Za-z]:", normalized)
        or any(part in {"", ".", ".."} for part in path.parts)
    ):
        raise BoardError(f"{label} must be a safe repository-relative path")
    return path.as_posix()


def _ownership(values: Iterable[str]) -> list[str]:
    if not isinstance(values, list) or any(not isinstance(item, str) for item in values):
        raise BoardError("write_ownership must be a string list")
    items = list(values)
    if not items:
        raise BoardError("write_ownership must not be empty")
    if items == ["board-only"]:
        return items
    if "board-only" in items:
        raise BoardError("board-only cannot be combined with repository write ownership")
    normalized = [_safe_repo_path(item, "write_ownership item") for item in items]
    if len(normalized) != len(set(normalized)):
        raise BoardError("write_ownership contains duplicate paths")
    return normalized


def _task_dir(board_root: Path, run_id: str, task_id: str) -> Path:
    root = Path(board_root).resolve()
    run = _safe_id(run_id, "run_id")
    task = _safe_id(task_id, "task_id")
    target = (root / run / task).resolve()
    try:
        target.relative_to(root)
    except ValueError as exc:
        raise BoardError("task directory escapes board root") from exc
    return target


def _sha256_bytes(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def file_sha256(path: Path) -> str:
    return _sha256_bytes(Path(path).read_bytes())


def request_sha256(path: Path) -> str:
    text = _normalized_text(Path(path).read_text(encoding="utf-8-sig"))
    normalized, count = REQUEST_HASH_LINE.subn("", text, count=1)
    if count != 1 or REQUEST_HASH_LINE.search(normalized):
        raise BoardError("request.md must contain exactly one Request SHA256 line")
    return _sha256_bytes(normalized.encode("utf-8"))


def _atomic_write(path: Path, content: str) -> None:
    temporary = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    try:
        temporary.write_text(content, encoding="utf-8", newline="\n")
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def prepare_board(
    *,
    board_root: Path,
    run_id: str,
    task_id: str,
    model: str,
    objective: str,
    request_body: str,
    write_ownership: Iterable[str],
    soul: str,
    validation: str,
    deadline: str,
) -> dict[str, Any]:
    """Create one immutable request.md and return its identity."""

    if model not in CREATE_THREAD_MODELS:
        raise BoardError(f"unsupported create_thread model: {model}")
    objective = _require_text(objective, "objective")
    request_body = _normalized_text(_require_text(request_body, "request_body"))
    if re.search(
        r"^(Run ID|Task ID|Model|Request SHA256|Objective|Write Ownership|Soul|Soul Capsule SHA256|Validation|Deadline):",
        request_body,
        re.MULTILINE,
    ):
        raise BoardError("request_body contains reserved request metadata")
    soul = _require_text(soul, "soul")
    expected_soul = MODEL_SOULS[model]
    if soul != expected_soul:
        raise BoardError(f"model {model} requires {expected_soul} soul")
    soul_capsule = _load_soul_capsule(soul)
    soul_capsule_sha256 = _sha256_bytes(soul_capsule.encode("utf-8"))
    validation = _require_text(validation, "validation")
    deadline, _ = _utc_deadline(deadline)
    ownership = _ownership(write_ownership)
    task_dir = _task_dir(board_root, run_id, task_id)
    if task_dir.exists() and any(task_dir.iterdir()):
        raise BoardError(f"board task already exists and is immutable: {task_dir}")
    task_dir.mkdir(parents=True, exist_ok=True)

    ownership_json = json.dumps(ownership, ensure_ascii=False, separators=(",", ":"))
    done_template = json.dumps(
        {
            "schema_version": SCHEMA_VERSION,
            "run_id": run_id,
            "task_id": task_id,
            "model": model,
            "request_sha256": "<copy Request SHA256 above>",
            "result_sha256": "sha256:<64 lowercase hex of final result.md>",
            "completion_state": "completed",
            "changed_files": [],
            "validation": "<bounded validation summary>",
            "rollback": "No repository changes; retain board until GC disposition.",
            "unresolved": [],
        },
        ensure_ascii=False,
        indent=2,
    )
    without_hash = (
        "# Isolated Session Request\n\n"
        f"Run ID: `{run_id}`\n"
        f"Task ID: `{task_id}`\n"
        f"Model: `{model}`\n"
        f"Objective: {objective}\n"
        f"Write Ownership: `{ownership_json}`\n"
        f"Soul: `{soul}`\n"
        f"Soul Capsule SHA256: `{soul_capsule_sha256}`\n"
        f"Validation: {validation}\n"
        f"Deadline: `{deadline}`\n\n"
        "## Soul Capsule\n\n"
        f"{soul_capsule}\n\n"
        "## Request\n\n"
        f"{request_body.rstrip()}\n\n"
        "## Completion Marker Contract\n\n"
        "Use this exact JSON object shape. Replace the angle-bracket placeholders and "
        "change `completion_state` to `blocked` or `failed` only when necessary. "
        "Keep the literal `sha256:` prefix and replace only its angle-bracket digest "
        "placeholder. Do not add, remove, or rename fields. After writing and closing "
        "`result.md`, reread its exact on-disk bytes and hash those bytes. Do not hash a "
        "pre-write string or normalize line endings.\n\n"
        f"```json\n{done_template}\n```\n\n"
        "Write `done.json` only after that on-disk hash is computed, then never modify "
        "`result.md`.\n"
    )
    digest = _sha256_bytes(without_hash.encode("utf-8"))
    marker = f"Model: `{model}`\n"
    content = without_hash.replace(marker, marker + f"Request SHA256: `{digest}`\n", 1)
    request_path = task_dir / "request.md"
    if request_path.exists():
        raise BoardError(f"request.md already exists and is immutable: {request_path}")
    _atomic_write(request_path, content)
    if request_sha256(request_path) != digest:
        raise BoardError("prepared request hash does not verify")
    return {
        "schema_version": SCHEMA_VERSION,
        "state": "prepared",
        "run_id": run_id,
        "task_id": task_id,
        "model": model,
        "task_dir": task_dir.as_posix(),
        "request_path": request_path.as_posix(),
        "request_sha256": digest,
        "soul": soul,
        "soul_capsule_sha256": soul_capsule_sha256,
        "write_ownership": ownership,
    }


def _load_json(path: Path, fields: set[str]) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise BoardError(f"invalid JSON in {path.name}: {exc}") from exc
    if not isinstance(value, dict):
        raise BoardError(f"{path.name} must contain a JSON object")
    unexpected = sorted(set(value) - fields)
    missing = sorted(fields - set(value))
    if unexpected or missing:
        raise BoardError(
            f"{path.name} has unexpected fields={unexpected} missing fields={missing}"
        )
    return value


def _request_metadata(path: Path) -> dict[str, Any]:
    text = _normalized_text(path.read_text(encoding="utf-8-sig"))
    patterns = {
        "run_id": r"^Run ID: `([^`]+)`$",
        "task_id": r"^Task ID: `([^`]+)`$",
        "model": r"^Model: `([^`]+)`$",
        "request_sha256": r"^Request SHA256: `(sha256:[0-9a-f]{64})`$",
        "write_ownership": r"^Write Ownership: `(.+)`$",
        "soul": r"^Soul: `([^`]+)`$",
        "soul_capsule_sha256": r"^Soul Capsule SHA256: `(sha256:[0-9a-f]{64})`$",
        "deadline": r"^Deadline: `([^`]+)`$",
    }
    metadata: dict[str, Any] = {}
    for key, pattern in patterns.items():
        matches = re.findall(pattern, text, re.MULTILINE)
        if len(matches) != 1:
            raise BoardError(f"request.md must contain exactly one {key} field")
        metadata[key] = matches[0]
    try:
        ownership = json.loads(metadata["write_ownership"])
    except json.JSONDecodeError as exc:
        raise BoardError("request.md write ownership is invalid JSON") from exc
    if not isinstance(ownership, list) or any(not isinstance(item, str) for item in ownership):
        raise BoardError("request.md write ownership must be a string list")
    metadata["write_ownership"] = _ownership(ownership)
    metadata["deadline"], metadata["deadline_utc"] = _utc_deadline(
        metadata["deadline"], "request.md deadline"
    )
    capsule_matches = re.findall(
        r"^## Soul Capsule\n\n(.*?)\n\n## Request$",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if len(capsule_matches) != 1:
        raise BoardError("request.md must contain exactly one soul capsule section")
    metadata["soul_capsule"] = capsule_matches[0]
    return metadata


def _validate_common(
    value: dict[str, Any], *, run_id: str, task_id: str, model: str, request_hash: str, label: str
) -> None:
    if value["schema_version"] != SCHEMA_VERSION:
        raise BoardError(f"{label} schema_version must be {SCHEMA_VERSION}")
    if value["run_id"] != run_id or value["task_id"] != task_id:
        raise BoardError(f"{label} run/task identity mismatch")
    if value["model"] != model:
        raise BoardError(f"{label} model mismatch")
    if value["request_sha256"] != request_hash:
        raise BoardError(f"{label} request hash mismatch")


def _changed_files_allowed(changed_files: Any, ownership: list[str]) -> list[str]:
    if not isinstance(changed_files, list) or any(not isinstance(item, str) for item in changed_files):
        raise BoardError("done.json changed_files must be a string list")
    normalized = [_safe_repo_path(item, "changed_files item") for item in changed_files]
    if ownership == ["board-only"]:
        if normalized:
            raise BoardError("board-output-only task reported repository changes")
        return normalized
    for changed in normalized:
        if not any(changed == owner or changed.startswith(owner.rstrip("/") + "/") for owner in ownership):
            raise BoardError(f"changed file is outside write ownership: {changed}")
    return normalized


def validate_board(
    *,
    board_root: Path,
    run_id: str,
    task_id: str,
    expected_model: str,
    expected_request_sha256: str,
) -> dict[str, Any]:
    """Validate a complete board without reading any runtime session content."""

    if expected_model not in CREATE_THREAD_MODELS:
        raise BoardError(f"unsupported create_thread model: {expected_model}")
    if not SHA256.fullmatch(expected_request_sha256):
        raise BoardError("expected_request_sha256 must be a lowercase SHA-256")
    task_dir = _task_dir(board_root, run_id, task_id)
    if not task_dir.is_dir():
        raise BoardError(f"missing board task directory: {task_dir}")
    entries = {path.name: path for path in task_dir.iterdir()}
    missing = sorted(BOARD_FILES - set(entries))
    unexpected = sorted(set(entries) - BOARD_FILES)
    if missing:
        raise BoardError(f"missing required board file(s): {missing}")
    if unexpected:
        label = "entries" if any(not entries[name].is_file() for name in unexpected) else "files"
        raise BoardError(f"unexpected board {label}: {unexpected}")
    for name in BOARD_FILES:
        path = task_dir / name
        if path.is_symlink() or not path.is_file():
            raise BoardError(f"board file must be a regular non-symlink file: {name}")

    request_path = task_dir / "request.md"
    request = _request_metadata(request_path)
    actual_request_hash = request_sha256(request_path)
    if request["request_sha256"] != actual_request_hash:
        raise BoardError("request.md declared request hash mismatch")
    if actual_request_hash != expected_request_sha256:
        raise BoardError("request.md request hash mismatch")
    if (
        request["run_id"] != run_id
        or request["task_id"] != task_id
        or request["model"] != expected_model
    ):
        raise BoardError("request.md identity or model mismatch")
    expected_soul = MODEL_SOULS[expected_model]
    if request["soul"] != expected_soul:
        raise BoardError("request.md soul does not match model route")
    expected_capsule = _load_soul_capsule(expected_soul)
    if request["soul_capsule"] != expected_capsule:
        raise BoardError("request.md soul capsule content mismatch")
    expected_capsule_sha256 = _sha256_bytes(expected_capsule.encode("utf-8"))
    if request["soul_capsule_sha256"] != expected_capsule_sha256:
        raise BoardError("request.md soul capsule hash mismatch")

    thread = _load_json(task_dir / "thread.json", THREAD_FIELDS)
    done = _load_json(task_dir / "done.json", DONE_FIELDS)
    _validate_common(
        thread,
        run_id=run_id,
        task_id=task_id,
        model=expected_model,
        request_hash=actual_request_hash,
        label="thread.json",
    )
    _validate_common(
        done,
        run_id=run_id,
        task_id=task_id,
        model=expected_model,
        request_hash=actual_request_hash,
        label="done.json",
    )
    if thread["temporary"] is not True:
        raise BoardError("thread.json temporary must be true")
    for key in ("thread_id", "host_id", "created_at"):
        _require_text(thread[key], f"thread.json {key}")
    thread_deadline, _ = _utc_deadline(thread["deadline"], "thread.json deadline")
    if thread_deadline != request["deadline"]:
        raise BoardError("thread.json deadline mismatch")
    board_path = _require_text(thread["board_path"], "thread.json board_path")
    if Path(board_path).resolve() != task_dir:
        raise BoardError("thread.json board_path mismatch")
    ownership = _ownership(thread["write_ownership"])
    if ownership != request["write_ownership"]:
        raise BoardError("thread.json write ownership mismatch")

    result_path = task_dir / "result.md"
    if result_path.stat().st_size == 0:
        raise BoardError("result.md must not be empty")
    try:
        result_text = result_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise BoardError(f"result.md must be valid UTF-8 text: {exc}") from exc
    if DISALLOWED_CONTROL.search(result_text):
        raise BoardError("result.md contains disallowed control characters")
    actual_result_hash = file_sha256(result_path)
    if done["result_sha256"] != actual_result_hash:
        raise BoardError("done.json result hash mismatch")
    done_path = task_dir / "done.json"
    if done_path.stat().st_mtime_ns < result_path.stat().st_mtime_ns:
        raise BoardError("done.json must be written after result.md")
    done_utc = dt.datetime.fromtimestamp(done_path.stat().st_mtime, tz=dt.timezone.utc)
    if done_utc > request["deadline_utc"]:
        raise BoardError("done.json was completed after the request deadline")
    if done["completion_state"] not in COMPLETION_STATES:
        raise BoardError("done.json completion_state is invalid")
    changed_files = _changed_files_allowed(done["changed_files"], ownership)
    _require_text(done["validation"], "done.json validation")
    _require_text(done["rollback"], "done.json rollback")
    if not isinstance(done["unresolved"], list) or any(
        not isinstance(item, str) for item in done["unresolved"]
    ):
        raise BoardError("done.json unresolved must be a string list")

    return {
        "schema_version": SCHEMA_VERSION,
        "state": "valid",
        "run_id": run_id,
        "task_id": task_id,
        "model": expected_model,
        "task_dir": task_dir.as_posix(),
        "request_sha256": actual_request_hash,
        "soul": expected_soul,
        "soul_capsule_sha256": expected_capsule_sha256,
        "deadline": request["deadline"],
        "result_sha256": actual_result_hash,
        "completion_state": done["completion_state"],
        "changed_files": changed_files,
        "validation": done["validation"],
        "rollback": done["rollback"],
        "unresolved": done["unresolved"],
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    prepare = subparsers.add_parser("prepare", help="create one immutable request.md")
    prepare.add_argument("--board-root", required=True, type=Path)
    prepare.add_argument("--run-id", required=True)
    prepare.add_argument("--task-id", required=True)
    prepare.add_argument("--model", required=True, choices=sorted(CREATE_THREAD_MODELS))
    prepare.add_argument("--objective", required=True)
    prepare.add_argument("--request-file", required=True, type=Path)
    prepare.add_argument("--write-owner", action="append", required=True)
    prepare.add_argument("--soul", required=True)
    prepare.add_argument("--validation", required=True)
    prepare.add_argument("--deadline", required=True)
    validate = subparsers.add_parser("validate", help="validate one completed board")
    validate.add_argument("--board-root", required=True, type=Path)
    validate.add_argument("--run-id", required=True)
    validate.add_argument("--task-id", required=True)
    validate.add_argument("--expected-model", required=True, choices=sorted(CREATE_THREAD_MODELS))
    validate.add_argument("--expected-request-sha256", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "prepare":
            result = prepare_board(
                board_root=args.board_root,
                run_id=args.run_id,
                task_id=args.task_id,
                model=args.model,
                objective=args.objective,
                request_body=args.request_file.read_text(encoding="utf-8"),
                write_ownership=args.write_owner,
                soul=args.soul,
                validation=args.validation,
                deadline=args.deadline,
            )
        else:
            result = validate_board(
                board_root=args.board_root,
                run_id=args.run_id,
                task_id=args.task_id,
                expected_model=args.expected_model,
                expected_request_sha256=args.expected_request_sha256,
            )
    except (BoardError, OSError, UnicodeError) as exc:
        print(
            json.dumps(
                {"schema_version": SCHEMA_VERSION, "state": "invalid", "error": str(exc)},
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            )
        )
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
