"""Audit CLI regression tests on local synthetic videos."""
import json
import shlex
import subprocess
import sys
import unittest
import zipfile
from pathlib import Path
from . import test_prepare

ROOT = Path(__file__).resolve().parents[1]
from .fixtures.factory import make_inputs, make_source


def cli(*args, root=ROOT):
    command = [sys.executable, "-B", str(root / "tools/audit.py"), *map(str, args)]
    return subprocess.run(command, cwd=root, capture_output=True, text=True, check=False, timeout=90)


class AuditCLITests(test_prepare.VideoFixture, unittest.TestCase):
    def run_json(self, *args, root=ROOT):
        result = cli(*args, root=root)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def test_authoring_phase_commands_match_the_cli(self):
        from tools.audit import parser
        path = ROOT / "audit/authoring.md"
        phases = path.read_text().split("## Fase ")[1:]
        expected_by_phase = (("inspect", "prepare"), ("sample", "mark-viewed", "check-camera"),
                             ("update-shot", "check-camera"), ("complete", "check-input", "draft", "review", "export"))
        self.assertEqual(len(phases), len(expected_by_phase))
        for phase, expected in zip(phases, expected_by_phase, strict=True):
            commands = [shlex.split(line)[2:] for line in phase.splitlines() if line.startswith("python tools/audit.py ")]
            self.assertEqual(tuple(parser().parse_args(command).command for command in commands), expected)

    def test_help_exposes_only_the_current_audit_workflow(self):
        help_text = cli("--help").stdout
        for command in ("prepare", "update-shot", "check-camera", "check-input", "draft", "review", "export", "motion-hints"):
            self.assertIn(command, help_text)
        for name in ("draft-v2", "export-v2"):
            self.assertNotIn(name, help_text)
        for name, flag in (("draft", "--include-source"), ("draft", "--renderer-version"),
                           ("prepare", "--contract-version")):
            self.assertNotIn(flag, cli(name, "--help").stdout)

    def test_normal_and_multi_use_cli_for_check_review_and_export(self):
        for name in ("normal", "multi"):
            with self.subTest(name=name):
                work = self.work / name
                source = make_source(work / f"camera-{name}.mp4")
                audit, _ = make_inputs(work / "writing", source, multi=name == "multi")
                correction = work / "patch.json"
                correction.write_text(json.dumps({"camera": {"description": "Lintasan fixture."}}))
                session = audit.with_name("session.json")
                self.assertTrue(self.run_json("update-shot", session, "--shot-id", "shot-01",
                                              "--patch", correction)["camera_recheck_required"])
                self.run_json("check-camera", session, "--shot-id", "shot-01")
                info = audit.parent / "audit-info.json"
                self.assertTrue(self.run_json("check-input", source, audit, "--audit-info", info,
                                              "--session", session)["ok"])
                draft = self.run_json("draft", source, audit, "--audit-info", info, "--session", session,
                                      "--output", work / "candidate", "--fixture")
                cards = self.run_json("review", draft["candidate"], "--output", work / "review.md")
                result = self.run_json("export", draft["candidate"], "--receipt", cards["receipt"],
                                       "--output", work / "exports")
                self.assertEqual(result["snapshot_sha256"], draft["snapshot_sha256"])
                with zipfile.ZipFile(result["package"]) as archive:
                    self.assertEqual(len(archive.namelist()), 6)
                    self.assertFalse(any(path.lower().endswith(".mp4") for path in archive.namelist()))


class KitInventoryTests(test_prepare.VideoFixture, unittest.TestCase):
    def test_portable_inventory_is_deterministic_offline_and_current(self):
        import io
        from tools import build_audit_kit as kit
        archive_bytes = kit.build_bytes()
        self.assertEqual(archive_bytes, kit.build_bytes())
        folder = self.work / "bootstrap"
        folder.mkdir()
        with zipfile.ZipFile(io.BytesIO(archive_bytes)) as archive:
            self.assertEqual(set(archive.namelist()), kit.OUTER_FILES)
            archive.extractall(folder)
        command = [sys.executable, "-B", str(folder / "homeku_runtime.py"), "--output", str(folder)]
        for _ in range(2):
            result = subprocess.run(command, cwd=folder, capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(json.loads(result.stdout)["runtime_files"], len(kit.BUNDLED))
        found = {p.relative_to(folder).as_posix() for p in folder.rglob("*") if p.is_file()}
        self.assertEqual(found, kit.OUTER_FILES.union(kit.BUNDLED))
        self.assertTrue(not any(name.startswith(("docs/", "openspec/", "audit/result/", "video/"))
                                or "media_v" in name or "reporting_v" in name for name in found))
        self.assertIn("check-camera", cli("--help", root=folder).stdout)
        self.assertTrue((folder / "audit/design-audit.md").is_file())
        self.assertEqual({name for name in kit.BUNDLED if name.startswith("tools/assets/templates/")},
                         {"tools/assets/templates/analysis.md"})
        self.assertEqual({name for name in kit.BUNDLED if name.startswith("tools/assets/layouts/")},
                         {"tools/assets/layouts/media.json"})
        self.assertEqual(json.loads((folder / "template-audit.json").read_text())["schema_version"], "3.1")
        (folder / "tools/audit.py").write_text("user-owned change")
        denied = subprocess.run(command, cwd=folder, capture_output=True, text=True, timeout=30)
        self.assertNotEqual(denied.returncode, 0)
        self.assertIn("Refusing to replace", denied.stderr)
