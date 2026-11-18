"""Production crop checks and project integration, not house/video quality tests."""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
from shutil import copytree
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from PIL import Image

from test_project_rules import PLUGIN, SKILL, VALIDATOR, WORKSPACE, approved, planning

SPEC = importlib.util.spec_from_file_location("home_productions_split", SKILL / "scripts/split_frames.py")
SPLITTER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SPLITTER)


class SplitFramesTests(unittest.TestCase):
    def setUp(self):
        (WORKSPACE / "runs").mkdir(exist_ok=True)
        self.temp = TemporaryDirectory(dir=WORKSPACE / "runs")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "collage.png"
        self.output = self.root / "frames"

    def collage(self, size=(72, 64), mode="RGB"):
        channels = 4 if mode == "RGBA" else 3
        pixels = bytes(
            value
            for y in range(size[1])
            for x in range(size[0])
            for value in (x % 256, y % 256, 25 if x < size[0] // 2 else 225, (x + y) % 256)[:channels]
        )
        image = Image.frombytes(mode, size, pixels)
        image.save(self.source)
        return image

    def split(self, **kwargs):
        return SPLITTER.split_frames(self.source, self.output, "shot-01", **kwargs)

    def assert_no_outputs(self):
        self.assertFalse(self.output.exists() and any(self.output.iterdir()))

    def assert_crops_equal(self, image, report):
        for record in report["files"]:
            path = self.output / record["file"]
            with Image.open(path) as saved:
                saved.load()
                expected = image.crop(record["box_xyxy"])
                self.assertEqual(saved.format, "PNG")
                self.assertEqual(saved.mode, image.mode)
                self.assertEqual(saved.size, expected.size)
                self.assertEqual(saved.tobytes(), expected.tobytes())
                self.assertEqual(saved.width * 16, saved.height * 9)
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), record["sha256"])
            self.assertTrue(record["source_pixels_preserved"])

    def test_exact_split_preserves_order_pixels_source_and_report(self):
        image = self.collage()
        original = self.source.read_bytes()
        report = self.split()
        self.assertEqual([record["box_xyxy"] for record in report["files"]],
                         [[0, 0, 36, 64], [36, 0, 72, 64]])
        self.assertEqual([record["role"] for record in report["files"]], ["start", "end"])
        self.assert_crops_equal(image, report)
        self.assertEqual(self.source.read_bytes(), original)
        self.assertEqual(report["source"]["sha256"], hashlib.sha256(original).hexdigest())
        self.assertFalse(report["resized"])
        self.assertFalse(report["regenerated"])
        self.assertFalse(report["visual_review_performed"])
        self.assertIsNone(report["resolution_target_met"])
        self.assertEqual(json.loads((self.output / "shot-01-split.json").read_text()), report)

    def test_rgba_alpha_is_preserved(self):
        image = self.collage(mode="RGBA")
        self.assert_crops_equal(image, self.split())

    def test_wrong_canvas_requires_inspected_explicit_boxes(self):
        for size in ((73, 64), (74, 64)):
            with self.subTest(size=size):
                self.collage(size)
                with self.assertRaisesRegex(ValueError, "supply both crop boxes"):
                    self.split()
                self.assert_no_outputs()

    def test_explicit_pilot_inset_preserves_pixels_without_resizing(self):
        image = self.collage((1330, 1182))
        report = self.split(start_box=(4, 7, 661, 1175), end_box=(669, 7, 1326, 1175),
                            min_frame_width=720)
        self.assertTrue(report["explicit_boxes"])
        self.assertEqual([(item["width"], item["height"]) for item in report["files"]],
                         [(657, 1168), (657, 1168)])
        self.assert_crops_equal(image, report)
        self.assertFalse(report["resolution_target_met"])
        self.assertTrue(report["warnings"])

    def test_explicit_boxes_can_exclude_an_inspected_center_gutter(self):
        image = self.collage((73, 64))
        report = self.split(start_box=(0, 0, 36, 64), end_box=(37, 0, 73, 64))
        self.assert_crops_equal(image, report)

    def test_crop_validation_rejects_padding_distortion_unequal_and_mixed_panels(self):
        cases = [
            ((0, 0, 36, 64), None),
            ((-1, 0, 35, 64), (36, 0, 72, 64)),
            ((0, 0, 0, 64), (36, 0, 72, 64)),
            ((0, 0, 36, 65), (36, 0, 72, 64)),
            ((0, 0, 35, 64), (36, 0, 72, 64)),
            ((0, 0, 36, 64), (36, 0, 54, 32)),
            ((1, 0, 37, 64), (36, 0, 72, 64)),
            ((0, 0, 36, 64), (35, 0, 71, 64)),
            ((36, 0, 72, 64), (0, 0, 36, 64)),
            ((False, 0, 36, 64), (36, 0, 72, 64)),
            ((0, 0, 36.0, 64), (36, 0, 72, 64)),
        ]
        for start, end in cases:
            with self.subTest(start=start, end=end):
                with self.assertRaises(ValueError):
                    SPLITTER.panel_boxes((72, 64), start, end)

    def test_existing_results_are_not_overwritten(self):
        self.collage()
        self.output.mkdir()
        for filename in ("shot-01-start.png", "shot-01-end.png", "shot-01-split.json"):
            with self.subTest(filename=filename):
                target = self.output / filename
                target.write_bytes(b"previous-version")
                with self.assertRaises(FileExistsError):
                    self.split()
                self.assertEqual(list(self.output.iterdir()), [target])
                self.assertEqual(target.read_bytes(), b"previous-version")
                target.unlink()

    def test_broken_symlink_is_not_overwritten(self):
        self.collage()
        self.output.mkdir()
        link = self.output / "shot-01-start.png"
        link.symlink_to(self.root / "missing.png")
        with self.assertRaises(FileExistsError):
            self.split()
        self.assertTrue(link.is_symlink())
        self.assertFalse((self.root / "missing.png").exists())

    def test_write_failure_removes_only_new_partial_outputs(self):
        self.collage()
        self.output.mkdir()
        unrelated = self.output / "keep.txt"
        unrelated.write_text("keep")
        original_open = Path.open

        def fail_on_report(path, *args, **kwargs):
            if path.name == "shot-01-split.json" and args and args[0] == "xb":
                raise OSError("Test disk write failure")
            return original_open(path, *args, **kwargs)

        with patch.object(Path, "open", fail_on_report):
            with self.assertRaisesRegex(OSError, "Test disk"):
                self.split()
        self.assertEqual(list(self.output.iterdir()), [unrelated])
        self.assertEqual(unrelated.read_text(), "keep")

    def test_invalid_shot_id_and_resolution_target_do_not_write_files(self):
        self.collage()
        for shot_id in ("../shot-01", "shot-1", "kitchen"):
            with self.subTest(shot_id=shot_id):
                with self.assertRaises(ValueError):
                    SPLITTER.split_frames(self.source, self.output, shot_id)
        for minimum in (0, -1, True):
            with self.subTest(minimum=minimum):
                with self.assertRaises(ValueError):
                    self.split(min_frame_width=minimum)
        self.assert_no_outputs()

    def test_resolution_target_passes_without_upscaling(self):
        image = self.collage()
        report = self.split(min_frame_width=36)
        self.assertTrue(report["resolution_target_met"])
        self.assertEqual(report["warnings"], [])
        self.assert_crops_equal(image, report)

    def test_unreadable_multiframe_and_color_conversion_are_rejected(self):
        self.source.write_bytes(b"not an image")
        with self.assertRaises(OSError):
            self.split()
        self.assert_no_outputs()
        Image.new("L", (72, 64), 45).save(self.source)
        with self.assertRaisesRegex(ValueError, "RGB/RGBA"):
            self.split()
        self.assert_no_outputs()
        Image.new("RGB", (72, 64), "red").save(
            self.source, format="GIF", save_all=True,
            append_images=[Image.new("RGB", (72, 64), "blue")],
        )
        with self.assertRaisesRegex(ValueError, "animated or multi-frame"):
            self.split()
        self.assert_no_outputs()

    def test_exif_rotation_is_rejected_instead_of_silently_transforming_pixels(self):
        orientation = Image.Exif()
        orientation[274] = 6
        Image.new("RGB", (72, 64)).save(self.source, format="JPEG", exif=orientation)
        with self.assertRaisesRegex(ValueError, "orientation transform"):
            self.split()
        self.assert_no_outputs()

    def test_cli_works_from_isolated_package_and_invalid_crop_has_no_partial_files(self):
        self.collage()
        isolated = self.root / "installed"
        copytree(PLUGIN, isolated)
        script = isolated / "skills/produce-home-tour/scripts/split_frames.py"
        run = subprocess.run(
            [sys.executable, "-B", str(script), str(self.source),
             "--output", str(self.output), "--shot-id", "shot-01"],
            cwd=self.root, capture_output=True, text=True,
        )
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(len(json.loads(run.stdout)["files"]), 2)
        rejected_output = self.root / "invalid"
        run = subprocess.run(
            [sys.executable, "-B", str(script), str(self.source), "--output", str(rejected_output),
             "--shot-id", "shot-01", "--start-box", "0", "0", "35", "64",
             "--end-box", "36", "0", "72", "64"],
            capture_output=True, text=True,
        )
        self.assertEqual(run.returncode, 1)
        self.assertIn("9:16", run.stderr)
        self.assertFalse(rejected_output.exists())

    def test_all_shot_pairs_bind_to_project_without_auto_review_or_approval(self):
        self.collage()
        project = planning()
        project["stage"] = "visual_draft"
        for kind in ("concept", "shot_plan"):
            approved(project, kind)
        for shot in project["shots"]:
            report = SPLITTER.split_frames(self.source, self.output, shot["shot_id"])
            for record in report["files"]:
                asset_id = shot["shot_id"] + "-" + record["role"] + "-r1"
                project["assets"].append({
                    "asset_id": asset_id, "shot_id": shot["shot_id"],
                    "revision": 1, "role": record["role"],
                    "path": "frames/" + record["file"],
                    "sha256": record["sha256"], "width": record["width"], "height": record["height"],
                    "reviewed": False, "review_origin": None, "review_note": "",
                })
                shot["frames"][record["role"]] = asset_id
        self.assertTrue(VALIDATOR.validate_project(project, self.root)["valid"])
        self.assertIsNone(project["approvals"]["visual"])
        project["stage"] = "visual_final"
        self.assertFalse(VALIDATOR.validate_project(project, self.root)["valid"])
        for asset in project["assets"]:
            asset.update(reviewed=True, review_origin="user_report",
                         review_note="Synthetic pixel test metadata; not a house visual review.")
        approved(project, "visual")
        result = VALIDATOR.validate_project(project, self.root)
        self.assertTrue(result["valid"], result)
        self.assertEqual(result["total_duration_s"], 20)
        self.assertEqual(len(project["assets"]), 8)
        self.assertTrue(all(shot["prompt"] is None for shot in project["shots"]))


if __name__ == "__main__":
    unittest.main()
