"""Project-delivery checks; fixtures do not certify creative or generator quality."""
from __future__ import annotations

from copy import deepcopy
import hashlib
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

from PIL import Image

from test_project_rules import PLUGIN, SKILL, VALIDATOR, WORKSPACE, approved, planning

SPEC = importlib.util.spec_from_file_location(
    "home_productions_delivery", SKILL / "scripts/build_production_package.py",
)
BUILDER = importlib.util.module_from_spec(SPEC)
with patch.object(sys, "path", [str(SKILL / "scripts"), *sys.path]):
    SPEC.loader.exec_module(BUILDER)


def final_fixture(root, kinds=("exterior", "living_to_kitchen", "bedroom", "bathroom")):
    """Synthetic decisions, images and review metadata for file/contract checks."""
    project = planning(kinds)
    project["stage"] = "prompt_package"
    project["revision_notes"] = ["Synthetic package test; not user approval or house-quality evidence."]
    for kind in project["approvals"]:
        approved(project, kind)
    for number, shot in enumerate(project["shots"], 1):
        for role, offset in (("start", 20), ("end", 100)):
            asset_id = shot["shot_id"] + "-" + role
            relative = "frames/" + asset_id + ".png"
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            Image.new("RGB", (18, 32), (number * 20, offset, 40)).save(path)
            project["assets"].append({
                "asset_id": asset_id, "shot_id": shot["shot_id"], "revision": 1,
                "role": role, "path": relative,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "width": 18, "height": 32, "reviewed": True,
                "review_origin": "user_report",
                "review_note": "Synthetic pixels and review metadata; not an actual house review.",
            })
            shot["frames"][role] = asset_id
        # Deliberately different authored timing; the exporter must not rewrite it.
        motion = ("Move forward while panning right throughout the movement." if number % 2
                  else "First move forward, then pan right after reaching the planned turning point.")
        shot["camera"] = {
            "description": "Test adaptation: " + motion,
            "motion_relationship": "simultaneous" if number % 2 else "sequential",
        }
        shot["prompt"] = {
            "revision": 1, "duration_s": shot["duration_s"],
            "start_asset_id": shot["frames"]["start"], "end_asset_id": shot["frames"]["end"],
            "text": f"Synthetic test {shot['shot_id']}. Duration: {shot['duration_s']} seconds. "
                    + motion + " " + " ".join(VALIDATOR.RULES["prompt_constraints"].values()),
        }
    return project


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

    def fixture(self, kinds=("exterior", "living_to_kitchen", "bedroom", "bathroom")):
        project = final_fixture(self.source, kinds)
        self.save(project)
        return project

    def test_twenty_second_package_survives_loss_of_original_working_directory(self):
        project = self.fixture()
        result = BUILDER.build_package(self.project_file, self.output)
        self.assertEqual(result["total_duration_s"], 20)
        self.assertEqual(len(result["frames"]), 8)
        self.assertEqual(len(result["prompts"]), 4)
        for shot in project["shots"]:
            self.assertEqual(
                (self.output / "prompts" / (shot["shot_id"] + ".txt")).read_text(),
                shot["prompt"]["text"],
            )
        for asset in project["assets"]:
            copied = self.output / asset["path"]
            self.assertEqual(copied.read_bytes(), (self.source / asset["path"]).read_bytes())
        rmtree(self.source)
        restored = json.loads((self.output / "project.json").read_text())
        self.assertEqual(restored, project)
        self.assertTrue(VALIDATOR.validate_project(restored, self.output)["valid"])
        guide = (self.output / "production-guide.md").read_text()
        self.assertIn(project["knowledge"]["commit"], guide)
        self.assertIn(project["revision_notes"][0], guide)
        for shot in project["shots"]:
            self.assertIn(shot["camera"]["description"], guide)
            for role in ("start", "end"):
                self.assertIn(shot["frames"][role] + ".png", guide)

    def test_other_shot_counts_keep_exact_durations_pairs_and_prompt_text(self):
        for kinds, expected in (
            (("exterior_to_living", "kitchen", "bedroom", "bathroom"), 18),
            (("exterior", "living", "kitchen", "bedroom", "bathroom"), 22),
            (("exterior", "living_to_kitchen", "bedroom", "laundry", "bathroom"), 24),
        ):
            with self.subTest(kinds=kinds):
                project = self.fixture(kinds)
                output = self.root / ("delivery-" + str(expected))
                result = BUILDER.build_package(self.project_file, output)
                self.assertEqual(result["total_duration_s"], expected)
                self.assertEqual(len(result["frames"]), 2 * len(kinds))
                self.assertEqual(len(result["prompts"]), len(kinds))
                restored = json.loads((output / "project.json").read_text())
                self.assertEqual(restored["shots"], project["shots"])

    def test_input_and_unlisted_files_are_not_changed_or_copied(self):
        project = self.fixture()
        unrelated = self.source / "old-attempt.txt"
        unrelated.write_text("unlisted fixture")
        original = self.project_file.read_bytes()
        BUILDER.build_package(self.project_file, self.output)
        self.assertEqual(self.project_file.read_bytes(), original)
        self.assertEqual(unrelated.read_text(), "unlisted fixture")
        expected = {"project.json", "production-guide.md"}
        expected.update(asset["path"] for asset in project["assets"])
        expected.update("prompts/" + shot["shot_id"] + ".txt" for shot in project["shots"])
        actual = {str(path.relative_to(self.output)) for path in self.output.rglob("*") if path.is_file()}
        self.assertEqual(actual, expected)

    def test_existing_delivery_is_not_overwritten(self):
        self.fixture()
        self.output.mkdir()
        marker = self.output / "keep.txt"
        marker.write_text("old delivery")
        with self.assertRaises(FileExistsError):
            BUILDER.build_package(self.project_file, self.output)
        self.assertEqual(list(self.output.iterdir()), [marker])
        self.assertEqual(marker.read_text(), "old delivery")

    def test_incomplete_stale_or_mismatched_projects_never_create_a_delivery(self):
        base = self.fixture()
        variants = []
        changed = deepcopy(base)
        changed["stage"] = "visual_final"
        variants.append(changed)
        changed = deepcopy(base)
        changed["shots"][0]["prompt"]["end_asset_id"] = base["shots"][1]["frames"]["end"]
        variants.append(changed)
        changed = deepcopy(base)
        changed["shots"][0]["prompt"]["revision"] = 2
        variants.append(changed)
        changed = deepcopy(base)
        changed["shots"][0]["prompt"]["text"] = "No explicit continuous or ambient instructions."
        variants.append(changed)
        changed = deepcopy(base)
        changed["approvals"]["visual"] = None
        variants.append(changed)
        for index, project in enumerate(variants):
            with self.subTest(index=index):
                self.save(project)
                with self.assertRaises(ValueError):
                    BUILDER.build_package(self.project_file, self.output)
                self.assertFalse(self.output.exists())

    def test_unresolved_prompt_template_markers_are_rejected(self):
        project = self.fixture()
        project["shots"][0]["prompt"]["text"] += " {{CAMERA_PATH_SPEED_AND_REVEAL}}"
        self.save(project)
        result = VALIDATOR.validate_project(project, self.source)
        self.assertFalse(result["valid"])
        self.assertTrue(any("penanda template" in message for message in result["errors"]))
        with self.assertRaises(ValueError):
            BUILDER.build_package(self.project_file, self.output)
        self.assertFalse(self.output.exists())

    def test_missing_frame_prevents_export(self):
        project = self.fixture()
        (self.source / project["assets"][0]["path"]).unlink()
        with self.assertRaises(ValueError):
            BUILDER.build_package(self.project_file, self.output)
        self.assertFalse(self.output.exists())

    def test_assets_cannot_collide_with_generated_guide_or_prompt_files(self):
        for reserved in ("project.json", "production-guide.md", "prompts"):
            with self.subTest(reserved=reserved):
                project = self.fixture()
                asset = project["assets"][0]
                original = self.source / asset["path"]
                asset["path"] = reserved + "/image.png"
                target = self.source / asset["path"]
                # project.json is already a file at the source; use another input filename.
                if reserved == "project.json":
                    self.project_file.rename(self.source / "active.json")
                    self.project_file = self.source / "active.json"
                target.parent.mkdir(exist_ok=True)
                copyfile(original, target)
                self.save(project)
                self.assertTrue(VALIDATOR.validate_project(project, self.source)["valid"])
                with self.assertRaisesRegex(ValueError, "reserved delivery path"):
                    BUILDER.build_package(self.project_file, self.output)
                self.assertFalse(self.output.exists())
                # Reset this test's workspace for the next reserved path.
                rmtree(self.source)
                self.source.mkdir()
                self.project_file = self.source / "project.json"

    def test_copy_corruption_rolls_back_new_delivery(self):
        project = self.fixture()
        original_copy = BUILDER.copyfile
        before = (self.source / project["assets"][0]["path"]).read_bytes()

        def corrupt(source, target):
            original_copy(source, target)
            Path(target).write_bytes(b"corrupted copy")

        with patch.object(BUILDER, "copyfile", side_effect=corrupt):
            with self.assertRaisesRegex(ValueError, "Copied package failed"):
                BUILDER.build_package(self.project_file, self.output)
        self.assertFalse(self.output.exists())
        self.assertEqual((self.source / project["assets"][0]["path"]).read_bytes(), before)

    def test_copy_failure_rolls_back_new_delivery(self):
        self.fixture()
        with patch.object(BUILDER, "copyfile", side_effect=OSError("Test write failure")):
            with self.assertRaises(OSError):
                BUILDER.build_package(self.project_file, self.output)
        self.assertFalse(self.output.exists())
        self.assertTrue(self.project_file.is_file())

    def test_guide_links_resolve_with_spaces_in_asset_paths(self):
        project = self.fixture()
        asset = project["assets"][0]
        original = self.source / asset["path"]
        asset["path"] = "frames/frame awal.png"
        copyfile(original, self.source / asset["path"])
        self.save(project)
        BUILDER.build_package(self.project_file, self.output)
        guide = (self.output / "production-guide.md").read_text()
        self.assertIn("frames/frame%20awal.png", guide)
        for href in re.findall(r"\[[^\]]*\]\(([^)]+)\)", guide):
            url = urlsplit(href)
            if not url.scheme:
                self.assertTrue((self.output / unquote(url.path)).is_file(), href)

    def test_cli_runs_from_isolated_plugin_copy(self):
        self.fixture()
        installed = self.root / "installed-plugin"
        copytree(PLUGIN, installed)
        script = installed / "skills/produce-home-tour/scripts/build_production_package.py"
        run = subprocess.run(
            [sys.executable, "-B", str(script), str(self.project_file), "--output", str(self.output)],
            cwd=self.root, capture_output=True, text=True,
        )
        self.assertEqual(run.returncode, 0, run.stderr)
        result = json.loads(run.stdout)
        self.assertEqual(result["shot_count"], 4)
        self.assertTrue(Path(result["guide"]).is_file())


if __name__ == "__main__":
    unittest.main()
