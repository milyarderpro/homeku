"""Image-mode data checks, not proof of live batch execution or naturalness."""
from __future__ import annotations

from copy import deepcopy
import hashlib
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from PIL import Image

from test_project_rules import VALIDATOR, WORKSPACE, approved, final_project, image_prompts, planning, write_images


class ImageModeTests(unittest.TestCase):
    def setUp(self):
        (WORKSPACE / "runs").mkdir(exist_ok=True)
        self.temp = TemporaryDirectory(dir=WORKSPACE / "runs")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_seven_individual_references_have_no_endpoint_or_collage_roles(self):
        project = final_project(self.root, kinds=("exterior", "living", "kitchen", "bedroom", "bathroom", "laundry", "wardrobe"))
        result = VALIDATOR.validate_project(project, self.root)
        self.assertTrue(result["valid"], result)
        self.assertEqual(result["image_count"], 7)
        self.assertEqual(result["available_image_count"], 7)
        self.assertEqual({asset["role"] for asset in project["assets"]}, {"reference"})

    def test_partial_generation_with_real_failure_is_valid_draft_not_final(self):
        project = image_prompts(planning())
        project.update(stage="image_draft", image_mode="generate_image")
        project["image_batch"].update(execution="unknown", note="Synthetic interrupted batch fixture.")
        write_images(project, self.root)
        missing = project["image_plan"][-1]
        project["assets"] = [asset for asset in project["assets"] if asset["asset_id"] != missing["asset_id"]]
        missing.update(asset_id=None, status="failed", error="Synthetic generation interruption.")
        result = VALIDATOR.validate_project(project, self.root)
        self.assertTrue(result["valid"], result)
        self.assertEqual(result["available_image_count"], 3)
        project["stage"] = "image_final"
        self.assertFalse(VALIDATOR.validate_project(project, self.root)["valid"])

    def test_available_images_do_not_imply_visual_review(self):
        project = final_project(self.root, prompt=False)
        project["stage"] = "image_draft"
        project["approvals"]["visual"] = None
        for image, asset in zip(project["image_plan"], project["assets"]):
            image["status"] = "available"
            asset.update(reviewed=False, review_origin=None, review_note="")
        self.assertTrue(VALIDATOR.validate_project(project, self.root)["valid"])
        project["stage"] = "image_final"
        self.assertFalse(VALIDATOR.validate_project(project, self.root)["valid"])

    def test_external_mode_records_acquisition_without_claiming_internal_batch(self):
        project = final_project(self.root, prompt=False)
        project["image_mode"] = "prompt_to_image"
        project["image_batch"].update(execution="external", note="Synthetic external-file acquisition fixture.")
        self.assertTrue(VALIDATOR.validate_project(project, self.root)["valid"])
        project["image_batch"].update(execution="not_started", note="")
        self.assertFalse(VALIDATOR.validate_project(project, self.root)["valid"])

    def test_nonportrait_png_and_actual_jpeg_are_supported_without_forced_crop(self):
        project = final_project(self.root, prompt=False)
        self.assertTrue(VALIDATOR.validate_project(project, self.root)["valid"])
        asset = project["assets"][0]
        source = self.root / asset["path"]
        target = source.with_suffix(".jpg")
        with Image.open(source) as image:
            image.save(target, format="JPEG")
        asset.update(path=str(target.relative_to(self.root)), format="JPEG",
                     sha256=hashlib.sha256(target.read_bytes()).hexdigest())
        self.assertTrue(VALIDATOR.validate_project(project, self.root)["valid"])

    def test_integrated_bathroom_laundry_can_explicitly_map_two_views_without_an_extra_shot(self):
        project = planning(("exterior", "living_to_kitchen", "bathroom_laundry"))
        shot = project["shots"][-1]
        original = project["image_plan"][-1]
        original["area_ids"] = ["bathroom"]
        additional = deepcopy(original)
        additional.update(image_id="img-laundry", primary_area="laundry", area_ids=["laundry"])
        project["image_plan"].append(additional)
        shot["reference_image_ids"].append(additional["image_id"])
        shot["reference_choice"]["count"] = 2
        result = VALIDATOR.validate_project(project, self.root)
        self.assertTrue(result["valid"], result)
        self.assertEqual(shot["duration_s"], 4)
        self.assertEqual(result["shot_count"], 3)

    def test_pure_pan_is_valid_without_inventing_a_translation(self):
        project = planning()
        camera = project["shots"][0]["camera"]
        camera["components"] = [{"kind": "pan", "description": "Test pan",
                                 "start_s": 0, "duration_s": 6, "distance_m": None, "angle_deg": 12}]
        self.assertTrue(VALIDATOR.validate_project(project, self.root)["valid"])


if __name__ == "__main__":
    unittest.main()
