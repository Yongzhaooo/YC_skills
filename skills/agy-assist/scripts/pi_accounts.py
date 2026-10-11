"""Local ACP login snapshots; reuse named CLI profiles only for quota discovery."""
import argparse
import base64
import urllib.request
import urllib.parse
from contextlib import contextmanager
import ctypes
import json
import os
from pathlib import Path
import re
import subprocess
import sys


def atomic_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def dpapi(data, *, decrypt=False):
    if os.name != "nt":
        raise ValueError("ACP account snapshots currently require Windows DPAPI")
    class Blob(ctypes.Structure):
        _fields_ = [("size", ctypes.c_ulong), ("data", ctypes.POINTER(ctypes.c_char))]
    buffer = ctypes.create_string_buffer(data)
    source = Blob(len(data), ctypes.cast(buffer, ctypes.POINTER(ctypes.c_char)))
    target = Blob()
    api = ctypes.windll.crypt32.CryptUnprotectData if decrypt else ctypes.windll.crypt32.CryptProtectData
    if not api(ctypes.byref(source), None, None, None, None, 1, ctypes.byref(target)):
        raise ValueError("Windows DPAPI could not protect/unprotect the ACP snapshot")
    try:
        return ctypes.string_at(target.data, target.size)
    finally:
        ctypes.windll.kernel32.LocalFree(ctypes.cast(target.data, ctypes.c_void_p))


def google_identity(token):
    """Resolve the current login at Google; never log request bodies or tokens."""
    try:
        data = urllib.parse.urlencode({k: token[k] for k in
            ("client_id", "client_secret", "refresh_token")} | {"grant_type": "refresh_token"}).encode()
        request = urllib.request.Request("https://oauth2.googleapis.com/token", data=data)
        with urllib.request.urlopen(request, timeout=30) as response:
            access = json.load(response)["access_token"]
        request = urllib.request.Request("https://openidconnect.googleapis.com/v1/userinfo",
                                         headers={"Authorization": "Bearer " + access})
        with urllib.request.urlopen(request, timeout=30) as response:
            identity = json.load(response)
    except Exception as exc:
        raise ValueError("Google account identity lookup failed; no account was enrolled") from None
    if not identity.get("sub") or not identity.get("email") or identity.get("email_verified") is not True:
        raise ValueError("Google did not return a verified email and account ID")
    return {k: identity[k] for k in ("sub", "email")}


def cli_identities(root=None):
    """Read identity labels from local CLI snapshots, not credentials for ACP use.

    Cached ID-token claims are historical profile metadata, not fresh authentication.
    Enrollment compares their stable subject with the live Google userinfo response.
    """
    rows = []
    for path in (Path(root) if root else Path.home() / ".gemini/agy-profiles").glob("*/credential.dpapi"):
        if path.parent.name.startswith("_"):
            continue
        try:
            saved = json.loads(dpapi(path.read_bytes(), decrypt=True))
            credential = json.loads(base64.b64decode(saved["blobB64"]))
            claims = json.loads(base64.urlsafe_b64decode(credential["id_token"].split(".")[1] + "==="))
            if claims.get("sub") and claims.get("email"):
                rows.append({"profile": path.parent.name, "sub": claims["sub"], "email": claims["email"]})
        except (ValueError, KeyError, IndexError, TypeError):
            raise ValueError(f"Cannot read cached CLI identity for {path.parent.name}") from None
    return rows


def validate_name(name):
    if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9_-]+", name):
        raise ValueError("Profile name must contain only letters, digits, _ or -")
    return name


def select_candidate(rows, enrolled, tried):
    candidates = []
    for row in rows:
        name = row.get("profile")
        a, b = row.get("remaining_5h"), row.get("remaining_weekly")
        if (name in enrolled and name not in tried and type(a) in (int, float)
                and type(b) in (int, float) and 0 < a <= 100 and 0 < b <= 100):
            candidates.append((name, a, b))
    if not candidates:
        raise ValueError("No enrolled ACP profile has verified positive 5h and weekly quota")
    return sorted(candidates, key=lambda item: (-item[1], -item[2], item[0]))[0][0]


class AccountPool:
    def __init__(self, config, *, auth_dir=None):
        self.config = config
        self.root = Path(config.get("store", Path.home() / ".pi/agent/acp-profiles"))
        self.auth_dir = Path(auth_dir or Path.home() / ".gemini/antigravity-acp")

    @contextmanager
    def locked(self):
        # ponytail: shared Google auth files require one managed run at a time;
        # replace this lock only when the official runtime supports isolated auth roots.
        import msvcrt
        self.root.mkdir(parents=True, exist_ok=True)
        with (self.root / "pool.lock").open("a+b") as handle:
            handle.seek(0)
            if os.fstat(handle.fileno()).st_size == 0:
                handle.write(b"0")
                handle.flush()
            handle.seek(0)
            try:
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            except OSError as exc:
                raise ValueError("Another managed ACP run/account operation is active; retry after it finishes") from exc
            try:
                yield self
            finally:
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)

    def quiet(self, *, include_cli=False):
        names = "'agy_acp_server','localharness_external'" + (",'agy'" if include_cli else "")
        script = f"@(Get-Process -Name {names} -ErrorAction SilentlyContinue).Count"
        result = subprocess.run([self.config.get("powershell", "pwsh"), "-NoProfile", "-Command", script],
                                capture_output=True, text=True, encoding="utf-8", check=True)
        if result.stdout.strip() != "0":
            raise ValueError("ACP/AGY processes are active; preserve their work and close them before account switching/quota discovery")

    def capture(self):
        auth_record = json.loads((self.auth_dir / "acp_token.json").read_text(encoding="utf-8-sig"))
        settings = json.loads((self.auth_dir / "settings.json").read_text(encoding="utf-8-sig"))
        if not auth_record.get("refresh_token") or settings.get("auth", {}).get("type") != "oauth-personal":
            raise ValueError("An official ACP Google personal login is required before saving a profile")
        return {"token": auth_record, "auth": settings["auth"]}

    def read(self, name):
        name = validate_name(name)
        return json.loads(dpapi((self.root / f"{name}.dpapi").read_bytes(), decrypt=True))

    def write(self, name, snapshot):
        name = validate_name(name)
        self.root.mkdir(parents=True, exist_ok=True)
        path = self.root / f"{name}.dpapi"
        temporary = path.with_suffix(".tmp")
        temporary.write_bytes(dpapi(json.dumps(snapshot).encode("utf-8")))
        temporary.replace(path)

    def names(self):
        return sorted(p.stem for p in self.root.glob("*.dpapi") if p.stem not in {"_recovery", "quota-recovery"})

    def current(self):
        auth_record = self.capture()["token"]
        matches = []
        for name in self.names():
            saved = self.read(name)["token"]
            if (saved.get("refresh_token"), saved.get("client_id")) == (auth_record.get("refresh_token"), auth_record.get("client_id")):
                matches.append(name)
        if len(matches) > 1:
            raise ValueError("The same ACP login was enrolled under multiple names; resolve the duplicate")
        return matches[0] if matches else None

    def save_current(self, name):
        self.quiet()
        validate_name(name)
        if name.startswith("_") or name == "quota-recovery":
            raise ValueError("That profile name is reserved for recovery")
        current = self.current()
        if current and current != name:
            raise ValueError(f"This login is already enrolled as {current}")
        self.write(name, self.capture())
        return name

    def enroll(self):
        self.quiet()
        snapshot = self.capture()
        identity = google_identity(snapshot["token"])
        matches = [row for row in cli_identities() if row["sub"] == identity["sub"]]
        if len(matches) != 1:
            raise ValueError("Current Google account must match exactly one saved CLI profile")
        name = matches[0]["profile"]
        if name in self.names():
            previous = self.read(name).get("identity")
            if previous and previous["sub"] != identity["sub"]:
                raise ValueError("Saved ACP identity differs from CLI profile; preserve both and resolve explicitly")
        snapshot["identity"] = identity
        current = self.current()
        if current and current != name:
            raise ValueError("Current login already has a different profile binding")
        self.write(name, snapshot)
        return {"profile": name, **identity}

    def apply(self, snapshot):
        settings_file = self.auth_dir / "settings.json"
        settings = json.loads(settings_file.read_text(encoding="utf-8-sig")) if settings_file.exists() else {}
        settings["auth"] = snapshot["auth"]
        atomic_json(self.auth_dir / "acp_token.json", snapshot["token"])
        atomic_json(settings_file, settings)

    def switch(self, name):
        self.quiet()
        target = self.read(name)
        original = self.capture()
        self.write("_recovery", original)
        try:
            self.apply(target)
            if self.current() != name:
                raise ValueError("ACP profile readback did not match the selected profile")
        except Exception:
            self.apply(original)
            raise
        return name

    def quota_command(self):
        manager = Path(self.config["cli_manager"])
        if not manager.is_file():
            raise ValueError("Configured agy-profile manager is missing")
        return [self.config.get("powershell", "pwsh"), "-NoProfile", "-File",
                str(Path(__file__).with_name("pi_cli_quota.ps1")), "-Manager", str(manager),
                "-Recovery", str(self.root / "quota-recovery.dpapi")]

    def restore_cli(self):
        self.quiet(include_cli=True)
        restored = subprocess.run([*self.quota_command(), "-RestoreOnly"], capture_output=True)
        if restored.returncode:
            raise ValueError("Encrypted CLI quota recovery snapshot could not be restored")

    def quotas(self):
        self.quiet(include_cli=True)
        args = self.quota_command()
        proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True, encoding="utf-8", creationflags=subprocess.CREATE_NO_WINDOW)
        try:
            stdout, _ = proc.communicate()
        except KeyboardInterrupt:
            from pi_transport import stop_process
            stop_process(proc)
            if (self.root / "quota-recovery.dpapi").exists():
                self.restore_cli()
            raise
        if proc.returncode != 0:
            raise ValueError("CLI quota query/restoration failed; ACP was not switched")
        rows = json.loads(stdout)
        if not isinstance(rows, list):
            raise ValueError("CLI quota response was not a profile list")
        return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("save", "list", "current", "switch", "quota", "restore-cli", "enroll", "identity"))
    parser.add_argument("name", nargs="?")
    args = parser.parse_args()
    from pi_transport import load_route
    try:
        pool = AccountPool(load_route().get("rotation", {}))
        with pool.locked():
            if args.action == "enroll":
                output = {"enrolled": pool.enroll()}
            elif args.action == "identity":
                output = {"current": google_identity(pool.capture()["token"]), "cli_profiles": cli_identities()}
            elif args.action == "save":
                output = {"saved": pool.save_current(args.name)}
            elif args.action == "switch":
                output = {"current": pool.switch(args.name)}
            elif args.action == "quota":
                output = {"profiles": pool.quotas()}
            elif args.action == "restore-cli":
                pool.restore_cli()
                output = {"restored": True}
            else:
                output = {"current": pool.current(), "enrolled": pool.names(),
                          "identities": {name: pool.read(name).get("identity") for name in pool.names()}}
        print(json.dumps(output, ensure_ascii=False))
        return 0
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    raise SystemExit(main())
