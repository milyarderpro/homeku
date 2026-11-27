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
                self.run_json("complete", audit, "--session", session)
                invalid = work / "invalid.json"
                invalid.write_text("{}")
                failure = cli("check-input", source, audit, "--audit-info", invalid, "--session", session)
                self.assertEqual(failure.returncode, 1)
                self.assertFalse(json.loads(failure.stdout)["ok"])
                self.assertTrue(self.run_json("check-input", source, audit, "--audit-info", info,
                                              "--session", session)["ok"])
                draft = self.run_json("draft", source, audit, "--audit-info", info, "--session", session,
                                      "--output", work / "candidate", "--fixture")
                session_alias = session.parent / ".." / session.parent.name / session.name
                cards = self.run_json("review", draft["candidate"], "--output", work / "review.md",
                                      "--session", session_alias)
                checklist = Path(cards["checklist"]).read_text()
                self.assertIn("[ ] Periksa framing", checklist)
                self.assertIn("media/overview.jpg", checklist)
                self.assertIn("media/storyboard.jpg", checklist)
                self.assertIn("media/shot-01.jpg", checklist)
                self.assertIn(draft["snapshot_sha256"], checklist)
                missing = cli("export", draft["candidate"], "--receipt", work / "missing.json",
                              "--output", work / "exports", "--session", session)
                self.assertEqual(missing.returncode, 1)
                self.assertEqual(json.loads(missing.stderr)["status"], "failed")
                damaged_receipt = work / "damaged.json"
                damaged_receipt.write_text("{")
                damaged = cli("export", draft["candidate"], "--receipt", damaged_receipt,
                              "--output", work / "exports", "--session", session)
                self.assertEqual(damaged.returncode, 1)
                manifest = Path(draft["candidate"]) / "manifest.json"
                saved_manifest = manifest.read_bytes()
                manifest.unlink()
                incomplete = cli("export", draft["candidate"], "--receipt", cards["receipt"],
                                 "--output", work / "exports", "--session", session)
                self.assertEqual(incomplete.returncode, 1)
                manifest.write_bytes(saved_manifest)
                wrong = work / "wrong/session.json"
                args = ("export", draft["candidate"], "--receipt", cards["receipt"], "--output", work / "exports")
                self.assertEqual(cli(*args, "--session", wrong).returncode, 1)
                self.assertFalse(wrong.parent.exists())
                wrong.parent.mkdir()
                wrong.write_bytes(session.read_bytes())
                (wrong.parent / "audit.json").write_bytes(audit.read_bytes())
                for selected_session, expected in ((session, "matches"), (wrong, "stale")):
                    status = self.run_json("status", selected_session, "--candidate", draft["candidate"],
                                           "--receipt", cards["receipt"])
                    self.assertEqual(status["receipt"]["state"], expected)
                self.assertEqual(status["receipt"]["reason"], "different-session")
                denied = cli(*args, "--session", wrong)
                self.assertEqual(denied.returncode, 1)
                self.assertIn("Review receipt belongs to another session", denied.stderr)
                self.assertFalse(wrong.with_name("performance.jsonl").exists())
                source.rename(source.with_suffix(".offline"))
                result = self.run_json(*args, "--session", session)
                commands = self.run_json("performance", audit.parent)["commands"]
                self.assertEqual(commands["check-camera"]["runs"][0]["shot"], "shot-01")
                self.assertEqual(commands["complete"]["attempts"], 1)
                self.assertEqual(commands["check-input"]["attempts"], 2)
                self.assertEqual([row["state"] for row in commands["check-input"]["runs"]],
                                 ["failed", "complete"])
                self.assertEqual(commands["draft"]["attempts"], 1)
                self.assertEqual(commands["export"]["attempts"], 4)
                self.assertEqual([row["state"] for row in commands["export"]["runs"]],
                                 ["failed", "failed", "failed", "complete"])
                for command in ("draft", "review", "export"):
                    self.assertEqual(commands[command]["runs"][-1]["snapshot_sha256"], result["snapshot_sha256"])
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
        from tools.audit import parser
        visual = (folder / "audit/visual-audit.md").read_text()
        commands = [shlex.split(line)[2:] for line in visual.splitlines()
                    if line.startswith("python tools/audit.py measure-anchor ")]
        self.assertEqual(len(commands), 2)
        for args in commands:
            self.assertEqual(parser().parse_args(args).command, "measure-anchor")
        self.assertIn("--end-points", cli("measure-anchor", "--help", root=folder).stdout)
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
