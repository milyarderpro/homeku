"""Controlled I/O failures; not a claim about ChatGPT host permissions."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
from shutil import rmtree
import sys
import subprocess
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from test_project_rules import SKILL, WORKSPACE, VALIDATOR, blank, final_project, legacy_project

SPEC = importlib.util.spec_from_file_location("home_productions_checkpoint", SKILL / "scripts/save_project.py")
SAVER = importlib.util.module_from_spec(SPEC)
with patch.object(sys, "path", [str(SKILL / "scripts"), *sys.path]):
    SPEC.loader.exec_module(SAVER)


class CheckpointTests(unittest.TestCase):
    def setUp(self):
        (WORKSPACE / "runs").mkdir(exist_ok=True)
        self.temp = TemporaryDirectory(dir=WORKSPACE / "runs")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.work = self.root / "work"
        self.work.mkdir()
        self.path = self.work / "project.json"
        self.fallback = self.root / "fallback"

    def save(self, project):
        return SAVER.save_project(project, self.path, fallback_root=self.fallback)

    def test_write_readback_and_next_checkpoint_never_overwrite_last_good(self):
        project = blank()
        first = self.save(project)
        self.assertTrue(first["saved"], first)
        original = self.path.read_bytes()
        project["brief"] = "A revised brief"
        second = self.save(project)
        self.assertTrue(second["saved"], second)
        self.assertNotEqual(second["path"], str(self.path))
        self.assertEqual(self.path.read_bytes(), original)
        restored = json.loads(Path(second["path"]).read_text())
        self.assertEqual(restored, project)
        self.assertTrue(VALIDATOR.validate_project(restored, self.work)["valid"])

    def test_permission_denied_file_uses_new_name_in_same_folder(self):
        publish = SAVER._publish
        def blocked_preferred(project, target, root):
            if target == self.path:
                raise PermissionError("simulated file permission denied")
            return publish(project, target, root)
        with patch.object(SAVER, "_publish", side_effect=blocked_preferred):
            result = self.save(blank())
        self.assertTrue(result["saved"], result)
        self.assertFalse(result["relocated"])
        self.assertNotEqual(Path(result["path"]), self.path)
        self.assertTrue(result["errors"])

    def test_readonly_directory_relocates_actual_assets_and_updates_active_path(self):
        project = final_project(self.work)
        before = deepcopy(project)
        publish = SAVER._publish
        def blocked_folder(data, target, root):
            if root == self.work:
                raise PermissionError("simulated directory permission denied")
            return publish(data, target, root)
        with patch.object(SAVER, "_publish", side_effect=blocked_folder):
            result = self.save(project)
        self.assertTrue(result["saved"], result)
        self.assertTrue(result["relocated"])
        active = Path(result["path"])
        self.assertNotEqual(active.parent, self.work)
        self.assertEqual(project, before)
        rmtree(self.work)
        restored = json.loads(active.read_text())
        self.assertTrue(VALIDATOR.validate_project(restored, active.parent)["valid"])

    def test_no_writable_location_returns_memory_handoff_without_fake_path(self):
        self.path.write_text(json.dumps(blank()))
        last_good = self.path.read_bytes()
        project = blank()
        project["brief"] = "Keep this decision in memory"
        with patch.object(SAVER, "_publish", side_effect=PermissionError("simulated all locations denied")):
            result = self.save(project)
        self.assertFalse(result["saved"])
        self.assertIsNone(result["path"])
        self.assertEqual(self.path.read_bytes(), last_good)
        self.assertEqual(project["brief"], "Keep this decision in memory")
        self.assertFalse(list(self.fallback.glob("*")))

    def test_published_readback_failure_removes_only_new_file_not_last_checkpoint(self):
        self.path.write_text(json.dumps(blank()))
        last_good = self.path.read_bytes()
        read = SAVER._read_json
        def failed_readback(path):
            if Path(path).suffix == ".json":
                raise OSError("simulated final read-back failure")
            return read(path)
        with patch.object(SAVER, "_read_json", side_effect=failed_readback):
            result = self.save(blank())
        self.assertFalse(result["saved"])
        self.assertEqual(self.path.read_bytes(), last_good)
        self.assertEqual(list(self.work.iterdir()), [self.path])

    def test_copy_corruption_never_claims_relocated_final(self):
        project = final_project(self.work)
        copy = SAVER.copyfile
        def corrupt(source, target):
            copy(source, target)
            Path(target).write_bytes(b"broken")
        publish = SAVER._publish
        def first_denied(data, target, root):
            if root == self.work:
                raise PermissionError("first folder denied")
            return publish(data, target, root)
        with patch.object(SAVER, "_publish", side_effect=first_denied), patch.object(SAVER, "copyfile", side_effect=corrupt):
            result = self.save(project)
        self.assertFalse(result["saved"])
        self.assertTrue(any("SHA-256" in message for message in result["errors"]), result)
        self.assertFalse(list(self.fallback.glob("*")))
        self.assertTrue(VALIDATOR.validate_project(project, self.work)["valid"])

    def test_missing_asset_or_invalid_data_is_not_reported_as_saved(self):
        project = final_project(self.work)
        (self.work / project["assets"][0]["path"]).unlink()
        result = self.save(project)
        self.assertFalse(result["saved"])
        self.assertTrue(any("file asli" in message for message in result["errors"]))
        result = self.save({"schema_version": "2.1"})
        self.assertFalse(result["saved"])
        self.assertIsNone(result["path"])


    def test_legacy_cli_converts_copy_without_merging_old_connector_images(self):
        original = legacy_project(final_project(self.work, living_references=2))
        self.path.write_text(json.dumps(original))
        before = self.path.read_bytes()
        target = self.root / "converted" / "project.json"
        run = subprocess.run([sys.executable, "-B", str(SKILL / "scripts/validate_project.py"),
                              str(self.path), "--migrate-to", str(target), "--fallback-root", str(self.fallback)],
                             capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr + run.stdout)
        report = json.loads(run.stdout)
        active = Path(report["path"])
        converted = json.loads(active.read_text())
        self.assertEqual(self.path.read_bytes(), before)
        self.assertNotEqual(active, self.path)
        self.assertEqual(len(converted["image_plan"]), 5)
        self.assertEqual(len(converted["shots"][1]["reference_image_ids"]), 2)
        self.assertIsNone(converted["shots"][1]["reference_choice"])
        self.assertTrue(report["needs_review"])
        self.assertTrue(VALIDATOR.validate_project(converted, active.parent)["valid"])
        rmtree(self.work)
        self.assertTrue(VALIDATOR.validate_project(converted, active.parent)["valid"])

    def test_legacy_cli_refuses_source_as_destination_and_checkpoint_cli_accepts_memory(self):
        self.path.write_text(json.dumps(legacy_project(final_project(self.work, living_references=2))))
        before = self.path.read_bytes()
        run = subprocess.run([sys.executable, "-B", str(SKILL / "scripts/validate_project.py"),
                              str(self.path), "--migrate-to", str(self.path)], capture_output=True, text=True)
        self.assertNotEqual(run.returncode, 0)
        self.assertEqual(self.path.read_bytes(), before)
        target = self.root / "memory" / "project.json"
        run = subprocess.run([sys.executable, "-B", str(SKILL / "scripts/save_project.py"), "-",
                              "--output", str(target), "--fallback-root", str(self.fallback)],
                             input=json.dumps(blank()), capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr + run.stdout)
        self.assertTrue(json.loads(run.stdout)["saved"])
        self.assertTrue(target.is_file())


if __name__ == "__main__":
    unittest.main()
