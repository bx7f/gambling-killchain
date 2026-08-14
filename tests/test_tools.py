from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "scripts/evidence.py"


def run_tool(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", str(TOOL), *arguments],
        capture_output=True,
        text=True,
    )


class EvidenceToolTests(unittest.TestCase):
    def init_case(self, temporary: str, case_id: str = "case-1") -> Path:
        root = Path(temporary) / "cases"
        result = run_tool(
            "init", "--case-id", case_id, "--root", str(root),
            "--question", "Does the observation support the claim?",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return root / case_id

    def test_init_creates_compact_case_and_resolves_templates(self):
        with tempfile.TemporaryDirectory() as temporary:
            case = self.init_case(temporary)
            state = json.loads((case / "case.json").read_text())
            self.assertEqual(state["schema_version"], "gka.case.v2")
            self.assertEqual(state["question"], "Does the observation support the claim?")
            self.assertTrue((case / "manifests/evidence.jsonl").is_file())
            self.assertTrue((case / "reports/report.md").is_file())
            self.assertNotIn("<CASE-ID>", (case / "evidence-index.md").read_text())
            if os.name == "posix":
                self.assertEqual(stat.S_IMODE(case.stat().st_mode), 0o700)
                self.assertEqual(stat.S_IMODE((case / "case.json").stat().st_mode), 0o600)

    def test_add_copies_by_hash_and_verify_succeeds(self):
        with tempfile.TemporaryDirectory() as temporary:
            case = self.init_case(temporary)
            source = Path(temporary) / "capture.json"
            source.write_text('{"status":"fixture"}\n')
            result = run_tool(
                "add", "--case-dir", str(case), "--file", str(source),
                "--test-id", "T-API-001", "--source", "captured response",
                "--notes", "Parsed JSON observation",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            record = json.loads(result.stdout)["record"]
            stored = case / record["path"]
            self.assertTrue(stored.is_file())
            self.assertEqual(record["sha256"], hashlib.sha256(source.read_bytes()).hexdigest())
            verified = run_tool("verify", "--case-dir", str(case))
            self.assertEqual(verified.returncode, 0, verified.stdout)
            output = json.loads(verified.stdout)
            self.assertTrue(output["ok"])
            self.assertEqual(output["verified_evidence"], 1)
            self.assertRegex(output["manifest_sha256"], r"^[0-9a-f]{64}$")

    def test_duplicate_content_is_idempotent(self):
        with tempfile.TemporaryDirectory() as temporary:
            case = self.init_case(temporary)
            source = Path(temporary) / "artifact.bin"
            source.write_bytes(b"same bytes")
            command = (
                "add", "--case-dir", str(case), "--file", str(source),
                "--test-id", "T-1", "--source", "fixture",
            )
            first = run_tool(*command)
            second = run_tool(*command)
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(json.loads(second.stdout)["status"], "existing")
            lines = (case / "manifests/evidence.jsonl").read_text().splitlines()
            self.assertEqual(len(lines), 1)

    def test_verify_detects_tampering(self):
        with tempfile.TemporaryDirectory() as temporary:
            case = self.init_case(temporary)
            source = Path(temporary) / "artifact.bin"
            source.write_bytes(b"original")
            added = run_tool(
                "add", "--case-dir", str(case), "--file", str(source),
                "--test-id", "T-1", "--source", "fixture",
            )
            record = json.loads(added.stdout)["record"]
            (case / record["path"]).write_bytes(b"changed")
            verified = run_tool("verify", "--case-dir", str(case))
            self.assertEqual(verified.returncode, 2)
            self.assertIn("sha256_mismatch", verified.stdout)

    def test_verify_rejects_manifest_path_escape(self):
        with tempfile.TemporaryDirectory() as temporary:
            case = self.init_case(temporary)
            outside = Path(temporary) / "outside.bin"
            outside.write_bytes(b"outside")
            digest = hashlib.sha256(outside.read_bytes()).hexdigest()
            record = {
                "schema_version": "gka.evidence.v1",
                "evidence_id": f"E-{digest[:16]}",
                "test_id": "T-1",
                "collected_at": "2026-01-01T00:00:00Z",
                "source": "fixture",
                "path": "../../outside.bin",
                "sha256": digest,
                "size": outside.stat().st_size,
                "media_type": "application/octet-stream",
                "kind": "raw",
                "notes": "",
            }
            (case / "manifests/evidence.jsonl").write_text(json.dumps(record) + "\n")
            verified = run_tool("verify", "--case-dir", str(case))
            self.assertEqual(verified.returncode, 2)
            self.assertIn("path_outside_case", verified.stdout)

    def test_add_rejects_corrupt_manifest(self):
        with tempfile.TemporaryDirectory() as temporary:
            case = self.init_case(temporary)
            (case / "manifests/evidence.jsonl").write_text("{invalid\n")
            source = Path(temporary) / "artifact.bin"
            source.write_bytes(b"artifact")
            added = run_tool(
                "add", "--case-dir", str(case), "--file", str(source),
                "--test-id", "T-1", "--source", "fixture",
            )
            self.assertNotEqual(added.returncode, 0)
            self.assertIn("invalid manifest JSON at line 1", added.stderr)

    def test_verify_reports_non_object_manifest_record(self):
        with tempfile.TemporaryDirectory() as temporary:
            case = self.init_case(temporary)
            (case / "manifests/evidence.jsonl").write_text("[]\n")
            verified = run_tool("verify", "--case-dir", str(case))
            self.assertEqual(verified.returncode, 2)
            self.assertIn("record_not_object", verified.stdout)

    def test_trigger_fixture_covers_reasoning_and_boundaries(self):
        fixture = json.loads((ROOT / "tests/trigger-cases.json").read_text())
        self.assertEqual(fixture["schema_version"], "gka.trigger-cases.v3")
        self.assertGreaterEqual(len(fixture["should_trigger"]), 8)
        self.assertGreaterEqual(len(fixture["should_not_trigger"]), 3)
        self.assertEqual(len(fixture["routing_cases"]), 7)
        for case in fixture["routing_cases"]:
            self.assertTrue((ROOT / case["reference"]).is_file(), case)

    def test_codex_and_claude_code_metadata_share_one_skill(self):
        skill_text = (ROOT / "SKILL.md").read_text()
        frontmatter = skill_text.split("---", 2)[1]
        self.assertIn("name: gambling-killchain", frontmatter)
        self.assertIn("    - codex", frontmatter)
        self.assertIn("    - claude-code", frontmatter)
        self.assertIn('    codex: "$gambling-killchain"', frontmatter)
        self.assertIn('    claude-code: "/gambling-killchain"', frontmatter)
        self.assertIn("${CLAUDE_SKILL_DIR}", skill_text)
        self.assertIn("available-Skills entry", skill_text)

        codex = (ROOT / "agents/openai.yaml").read_text()
        self.assertIn('display_name: "Gambling Platform Audit"', codex)
        self.assertIn("$gambling-killchain", codex)
        self.assertIn("allow_implicit_invocation: true", codex)

        claude = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
        self.assertEqual(claude["name"], "gambling-killchain")
        self.assertEqual(claude["displayName"], "Gambling Platform Audit")


if __name__ == "__main__":
    unittest.main(verbosity=2)
