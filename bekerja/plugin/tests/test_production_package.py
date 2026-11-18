"""V2 delivery and portability checks; no live image/video generation."""
from __future__ import annotations

from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import re
from shutil import copyfile, copytree, rmtree
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
from urllib.parse import unquote, urlsplit

from test_project_rules import PLUGIN, SKILL, VALIDATOR, WORKSPACE, final_project, image_prompts, planning

SPEC = importlib.util.spec_from_file_location("home_productions_delivery", SKILL / "scripts/build_production_package.py")
BUILDER = importlib.util.module_from_spec(SPEC)
with patch.object(sys, "path", [str(SKILL / "scripts"), *sys.path]):
    SPEC.loader.exec_module(BUILDER)


class ProductionPackageTests(unittest.TestCase):
    def setUp(self):
        (WORKSPACE / "runs").mkdir(exist_ok=True)
        self.temp = TemporaryDirectory(dir=WORKSPACE / "runs")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "work"
        self.source.mkdir()
        self.project_file = self.source / "project.json"
        self.output = self.root / "delivery"

    def save(self, project):
        self.project_file.write_text(json.dumps(project, ensure_ascii=False), encoding="utf-8")

    def fixture(self, **kwargs):
        project = final_project(self.source, **kwargs)
        self.save(project)
        return project

    def test_seven_prompt_package_does_not_claim_generated_or_r2v_ready_images(self):
        project = image_prompts(planning(("exterior", "living", "kitchen", "bedroom", "bathroom", "laundry", "wardrobe")))
        self.save(project)
        result = BUILDER.build_package(self.project_file, self.output)
        self.assertEqual(len(result["image_prompts"]), 7)
        self.assertEqual(result["reference_images"], [])
        self.assertEqual(result["video_prompts"], [])
        self.assertFalse((self.output / "video-prompts").exists())
        restored = json.loads((self.output / "project.json").read_text())
        self.assertEqual(restored["assets"], [])
        self.assertEqual(restored["image_batch"]["execution"], "not_started")
        for image in project["image_plan"]:
            self.assertEqual((self.output / "image-prompts" / (image["image_id"] + ".txt")).read_text(), image["prompt"])

    def test_r2v_package_keeps_five_originals_four_nine_section_prompts_and_source_independence(self):
        project = self.fixture()
        result = BUILDER.build_package(self.project_file, self.output)
        self.assertEqual((result["shot_count"], result["image_count"], result["total_duration_s"]), (4, 5, 20))
        self.assertEqual(len(result["reference_images"]), 5)
        self.assertEqual(len(result["video_prompts"]), 4)
        for shot in project["shots"]:
            content = (self.output / "video-prompts" / (shot["shot_id"] + ".txt")).read_text()
            self.assertEqual(content, BUILDER.render_video_prompt(shot["prompt"]))
            for section, body in shot["prompt"]["sections"].items():
                self.assertIn(section + "\n" + body, content)
        for asset in project["assets"]:
            self.assertEqual((self.output / asset["path"]).read_bytes(), (self.source / asset["path"]).read_bytes())
        rmtree(self.source)
        restored = json.loads((self.output / "project.json").read_text())
        self.assertEqual(restored, project)
        self.assertTrue(VALIDATOR.validate_project(restored, self.output)["valid"])
        guide = (self.output / "production-guide.md").read_text()
        for shot in project["shots"]:
            self.assertIn(shot["camera"]["visible_motion_evidence"], guide)
        self.assertIn(project["knowledge"]["commit"], guide)

    def test_other_durations_and_reference_counts_are_preserved(self):
        for kinds, count, seconds in (
            (("exterior_to_living", "kitchen", "bedroom", "bathroom"), 5, 18),
            (("exterior", "living", "kitchen", "bedroom", "bathroom"), 5, 22),
            (("exterior", "living_to_kitchen", "bedroom", "laundry", "bathroom"), 6, 24),
        ):
            with self.subTest(kinds=kinds):
                project = self.fixture(kinds=kinds)
                output = self.root / str(seconds)
                result = BUILDER.build_package(self.project_file, output)
                self.assertEqual((result["image_count"], result["total_duration_s"]), (count, seconds))
                restored = json.loads((output / "project.json").read_text())
                self.assertEqual(restored["shots"], project["shots"])

    def test_sources_are_unchanged_and_unlisted_attempts_are_not_copied(self):
        project = self.fixture()
        extra = self.source / "old-attempt.txt"
        extra.write_text("unlisted")
        original = self.project_file.read_bytes()
        BUILDER.build_package(self.project_file, self.output)
        self.assertEqual(self.project_file.read_bytes(), original)
        self.assertFalse((self.output / extra.name).exists())
        expected = {"project.json", "production-guide.md"}
        expected.update(asset["path"] for asset in project["assets"])
        expected.update("image-prompts/" + image["image_id"] + ".txt" for image in project["image_plan"])
        expected.update("video-prompts/" + shot["shot_id"] + ".txt" for shot in project["shots"])
        self.assertEqual({str(path.relative_to(self.output)) for path in self.output.rglob("*") if path.is_file()}, expected)

    def test_existing_delivery_is_not_overwritten(self):
        self.fixture()
        self.output.mkdir()
        marker = self.output / "keep.txt"
        marker.write_text("old release")
        with self.assertRaises(FileExistsError):
            BUILDER.build_package(self.project_file, self.output)
        self.assertEqual(list(self.output.iterdir()), [marker])

    def test_invalid_stale_and_incomplete_packages_never_export(self):
        base = self.fixture()
        variants = []
        for stage in ("shot_plan", "image_final"):
            project = deepcopy(base)
            project["stage"] = stage
            variants.append(project)
        project = deepcopy(base)
        project["shots"][0]["prompt"]["reference_image_ids"] = base["shots"][1]["reference_image_ids"]
        variants.append(project)
        project = deepcopy(base)
        project["assets"][0]["revision"] = 2
        variants.append(project)
        project = deepcopy(base)
        project["approvals"]["visual"] = None
        variants.append(project)
        for project in variants:
            self.save(project)
            with self.assertRaises(ValueError):
                BUILDER.build_package(self.project_file, self.output)
            self.assertFalse(self.output.exists())

    def test_missing_reference_prevents_export(self):
        project = self.fixture()
        (self.source / project["assets"][0]["path"]).unlink()
        with self.assertRaises(ValueError):
            BUILDER.build_package(self.project_file, self.output)
        self.assertFalse(self.output.exists())

    def test_reserved_asset_paths_do_not_overwrite_exported_prompts(self):
        project = self.fixture()
        asset = project["assets"][0]
        original = self.source / asset["path"]
        asset["path"] = "video-prompts/area.png"
        target = self.source / asset["path"]
        target.parent.mkdir()
        copyfile(original, target)
        self.save(project)
        self.assertTrue(VALIDATOR.validate_project(project, self.source)["valid"])
        with self.assertRaisesRegex(ValueError, "reserved"):
            BUILDER.build_package(self.project_file, self.output)
        self.assertFalse(self.output.exists())

    def test_copy_failure_and_corruption_roll_back_only_new_delivery(self):
        self.fixture()
        with patch.object(BUILDER, "copyfile", side_effect=OSError("test failure")):
            with self.assertRaises(OSError):
                BUILDER.build_package(self.project_file, self.output)
        self.assertFalse(self.output.exists())
        original_copy = BUILDER.copyfile
        def corrupt(source, target):
            original_copy(source, target)
            Path(target).write_bytes(b"broken copy")
        with patch.object(BUILDER, "copyfile", side_effect=corrupt):
            with self.assertRaisesRegex(ValueError, "Copied package"):
                BUILDER.build_package(self.project_file, self.output)
        self.assertFalse(self.output.exists())
        self.assertTrue(self.project_file.is_file())

    def test_guide_links_with_spaces_resolve(self):
        project = self.fixture()
        asset = project["assets"][0]
        original = self.source / asset["path"]
        asset["path"] = "images/area exterior.png"
        copyfile(original, self.source / asset["path"])
        self.save(project)
        BUILDER.build_package(self.project_file, self.output)
        guide = (self.output / "production-guide.md").read_text()
        self.assertIn("area%20exterior.png", guide)
        for href in re.findall(r"\[[^\]]*\]\(([^)]+)\)", guide):
            uri = urlsplit(href)
            if not uri.scheme:
                self.assertTrue((self.output / unquote(uri.path)).is_file(), href)

    def test_export_cli_works_from_isolated_plugin_copy(self):
        self.fixture()
        copied = self.root / "plugin-copy"
        copytree(PLUGIN, copied)
        run = subprocess.run([sys.executable, "-B", str(copied / "skills/produce-home-tour/scripts/build_production_package.py"),
                              str(self.project_file), "--output", str(self.output)],
                             cwd=self.root, capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(json.loads(run.stdout)["image_count"], 5)


if __name__ == "__main__":
    unittest.main()
