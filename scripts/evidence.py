#!/usr/bin/env python3
"""Initialize a case, register material artifacts, and verify evidence hashes."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import mimetypes
import os
from pathlib import Path
import re
import shutil
import sys

CASE_SCHEMA = "gka.case.v2"
EVIDENCE_SCHEMA = "gka.evidence.v1"
CASE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
MODES = ("offline", "passive", "active-readonly")


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.chmod(temporary, 0o600)
    os.replace(temporary, path)


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"[ERROR] invalid JSON {path}: {exc}") from exc


def ensure_case(case_dir: Path) -> dict:
    state_path = case_dir / "case.json"
    if not state_path.is_file():
        raise SystemExit(f"[ERROR] case.json missing: {state_path}")
    state = load_json(state_path)
    if not isinstance(state, dict):
        raise SystemExit(f"[ERROR] case.json must contain a JSON object: {state_path}")
    if state.get("schema_version") != CASE_SCHEMA:
        raise SystemExit(f"[ERROR] unsupported case schema: {state.get('schema_version')!r}")
    return state


def load_manifest_for_update(manifest: Path) -> list[dict]:
    """Read a manifest before mutation, failing closed on malformed records."""
    if not manifest.is_file():
        raise SystemExit(f"[ERROR] evidence manifest missing: {manifest}")
    records = []
    for line_number, line in enumerate(manifest.read_text(encoding="utf-8").splitlines(), 1):
        if not line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise SystemExit(
                f"[ERROR] invalid manifest JSON at line {line_number}: {exc}"
            ) from exc
        if not isinstance(record, dict):
            raise SystemExit(f"[ERROR] manifest line {line_number} must contain a JSON object")
        records.append(record)
    return records


def safe_case_path(case_dir: Path, recorded: str) -> Path | None:
    relative = Path(recorded)
    if relative.is_absolute():
        return None
    resolved = (case_dir / relative).resolve()
    try:
        resolved.relative_to(case_dir.resolve())
    except ValueError:
        return None
    return resolved


def init_case(args) -> int:
    if not CASE_ID_RE.fullmatch(args.case_id):
        raise SystemExit("[ERROR] invalid case-id")
    root = Path(args.root).expanduser().resolve()
    case_dir = root / args.case_id
    if case_dir.exists():
        raise SystemExit(f"[ERROR] case already exists: {case_dir}")

    for relative in ("evidence/objects", "notes", "reports", "manifests"):
        (case_dir / relative).mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(case_dir, 0o700)

    created = utc_now()
    state = {
        "schema_version": CASE_SCHEMA,
        "case_id": args.case_id,
        "question": args.question,
        "mode": args.mode,
        "created_at": created,
        "updated_at": created,
        "scope": [],
    }
    write_json(case_dir / "case.json", state)
    manifest = case_dir / "manifests/evidence.jsonl"
    manifest.touch(mode=0o600)
    os.chmod(manifest, 0o600)

    skill_dir = Path(__file__).resolve().parent.parent
    replacements = {"<CASE-ID>": args.case_id, "<QUESTION>": args.question}
    for source_name, destination in (
        ("evidence-index.md", case_dir / "evidence-index.md"),
        ("report.md", case_dir / "reports/report.md"),
    ):
        source = skill_dir / "assets/templates" / source_name
        text = source.read_text(encoding="utf-8")
        for old, new in replacements.items():
            text = text.replace(old, new)
        destination.write_text(text, encoding="utf-8")
        os.chmod(destination, 0o600)

    print(json.dumps({"case_dir": str(case_dir), "case": state}, ensure_ascii=False, indent=2))
    return 0


def add_evidence(args) -> int:
    case_dir = Path(args.case_dir).expanduser().resolve()
    state = ensure_case(case_dir)
    source_file = Path(args.file).expanduser().resolve()
    if not source_file.is_file():
        raise SystemExit(f"[ERROR] evidence file missing: {source_file}")

    digest = sha256_file(source_file)
    evidence_id = f"E-{digest[:16]}"
    manifest = case_dir / "manifests/evidence.jsonl"
    for existing in load_manifest_for_update(manifest):
        if existing.get("evidence_id") == evidence_id:
            if existing.get("sha256") != digest:
                raise SystemExit(f"[ERROR] evidence ID collision: {evidence_id}")
            print(json.dumps({"status": "existing", "record": existing}, ensure_ascii=False, indent=2))
            return 0

    suffix = re.sub(r"[^A-Za-z0-9._-]", "_", "".join(source_file.suffixes))[-24:]
    object_dir = case_dir / "evidence/objects"
    object_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    stored = object_dir / f"{digest}{suffix}"
    if stored.exists():
        if sha256_file(stored) != digest:
            raise SystemExit(f"[ERROR] stored object hash mismatch: {stored}")
    else:
        shutil.copyfile(source_file, stored)
        os.chmod(stored, 0o600)
        if sha256_file(stored) != digest:
            raise SystemExit(f"[ERROR] copied object hash mismatch: {stored}")

    record = {
        "schema_version": EVIDENCE_SCHEMA,
        "evidence_id": evidence_id,
        "test_id": args.test_id,
        "collected_at": utc_now(),
        "source": args.source,
        "path": stored.relative_to(case_dir).as_posix(),
        "sha256": digest,
        "size": stored.stat().st_size,
        "media_type": mimetypes.guess_type(stored.name)[0] or "application/octet-stream",
        "kind": args.kind,
        "notes": args.notes or "",
    }

    with manifest.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")
    os.chmod(manifest, 0o600)
    state["updated_at"] = utc_now()
    write_json(case_dir / "case.json", state)
    print(json.dumps({"status": "added", "record": record}, ensure_ascii=False, indent=2))
    return 0


def verify_case(args) -> int:
    case_dir = Path(args.case_dir).expanduser().resolve()
    ensure_case(case_dir)
    manifest = case_dir / "manifests/evidence.jsonl"
    errors = []
    seen = set()
    verified = 0

    for line_number, line in enumerate(manifest.read_text(encoding="utf-8").splitlines(), 1):
        if not line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append({"line": line_number, "error": f"invalid_json:{exc}"})
            continue
        if not isinstance(record, dict):
            errors.append({"line": line_number, "error": "record_not_object"})
            continue
        evidence_id = record.get("evidence_id")
        if record.get("schema_version") != EVIDENCE_SCHEMA:
            errors.append({"line": line_number, "evidence_id": evidence_id, "error": "unsupported_schema"})
        for field in ("evidence_id", "test_id", "source", "path", "sha256", "size"):
            if record.get(field) in (None, ""):
                errors.append({"line": line_number, "evidence_id": evidence_id,
                               "error": "missing_field", "field": field})
        if evidence_id in seen:
            errors.append({"line": line_number, "evidence_id": evidence_id, "error": "duplicate_id"})
        seen.add(evidence_id)
        path = safe_case_path(case_dir, str(record.get("path", "")))
        if path is None:
            errors.append({"line": line_number, "evidence_id": evidence_id, "error": "path_outside_case"})
            continue
        if not path.is_file():
            errors.append({"line": line_number, "evidence_id": evidence_id, "error": "missing_file"})
            continue
        actual_hash = sha256_file(path)
        actual_size = path.stat().st_size
        if actual_hash != record.get("sha256"):
            errors.append({"line": line_number, "evidence_id": evidence_id, "error": "sha256_mismatch"})
        if actual_size != record.get("size"):
            errors.append({"line": line_number, "evidence_id": evidence_id, "error": "size_mismatch"})
        if evidence_id != f"E-{actual_hash[:16]}":
            errors.append({"line": line_number, "evidence_id": evidence_id, "error": "id_hash_mismatch"})
        if actual_hash == record.get("sha256") and actual_size == record.get("size"):
            verified += 1

    result = {
        "case_dir": str(case_dir),
        "verified_evidence": verified,
        "manifest_sha256": sha256_file(manifest),
        "errors": errors,
        "ok": not errors,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    command = commands.add_parser("init", help="initialize a compact case directory")
    command.add_argument("--case-id", required=True)
    command.add_argument("--root", default="evidence")
    command.add_argument("--question", required=True)
    command.add_argument("--mode", choices=MODES, default="offline")
    command.set_defaults(func=init_case)

    command = commands.add_parser("add", help="copy and register a material artifact")
    command.add_argument("--case-dir", required=True)
    command.add_argument("--file", required=True)
    command.add_argument("--test-id", required=True)
    command.add_argument("--source", required=True)
    command.add_argument("--kind", choices=("raw", "derived", "report"), default="raw")
    command.add_argument("--notes")
    command.set_defaults(func=add_evidence)

    command = commands.add_parser("verify", help="verify registered evidence hashes and sizes")
    command.add_argument("--case-dir", required=True)
    command.set_defaults(func=verify_case)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
