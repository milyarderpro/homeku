"""V2 data/file invariants. Synthetic review/batch metadata is not runtime proof."""
from __future__ import annotations

from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from PIL import Image

WORKSPACE = Path(__file__).resolve().parents[1]
PLUGIN = WORKSPACE / "home-productions"
SKILL = PLUGIN / "skills/produce-home-tour"
SPEC = importlib.util.spec_from_file_location("home_productions_validation", SKILL / "scripts/validate_project.py")
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)
COMMIT = "26c5e56cb0de66d5c1ab4f93a1285654180382a0"


def blank():
    return json.loads((SKILL / "assets/project-template.json").read_text())


def planning(kinds=("exterior", "living_to_kitchen", "bedroom", "bathroom")):
    project = blank()
    project.update(stage="shot_plan", brief="Synthetic planning case; not a user production.",
                   concept={"title": "Fixture", "summary": "Contract checks only."})
    project["knowledge"].update(ref="main", commit=COMMIT, route="github_connector")
    project["design"] = {key: (["Test decision"] if isinstance(value, list) else "Test decision")
                         for key, value in project["design"].items()}
    sources = {
        "exterior": ("edh022", "shot-01", "exterior_front"),
        "living_to_kitchen": ("edh022", "shot-02", "combined_living_room_and_kitchen"),
        "bedroom": ("edh022", "shot-03", "bedroom"),
        "bathroom": ("edh022", "shot-04", "bathroom"),
        "exterior_to_living": ("edh035", "shot-01", "exterior_front_to_living_room"),
        "living": ("edh058", "shot-02", "living_room"),
        "kitchen": ("edh058", "shot-03", "kitchen"),
        "laundry": ("edh030", "shot-03", "laundry_room"),
        "wardrobe": ("edh058", "shot-05", "walk_in_closet"),
        "bathroom_laundry": ("edh033", "shot-03", "combined_bathroom_and_laundry"),
    }
    image_index = {}
    for number, kind in enumerate(kinds, 1):
        shot_id, evidence_id = f"shot-{number:02d}", f"ev-{number:02d}"
        rule = VALIDATOR.RULES["shot_kinds"][kind]
        areas, seconds = list(rule["coverage_sets"][0]), rule["duration_s"]
        ref, source_shot, scene = sources[kind]
        project["knowledge"]["evidence"].append({
            "evidence_id": evidence_id, "reference_id": ref, "shot_ids": [source_shot],
            "analysis_url": f"https://github.com/milyarderpro/homeku/blob/{COMMIT}/references/{ref}/analysis.yaml",
            "field_paths": [f"/shots/{int(source_shot.split('-')[1])-1}/scene"], "excerpt": scene,
            "covered_areas": areas.copy(), "continuity": "annotated_continuous",
            "access_status": "read", "error": None,
        })
        refs = []
        for primary in rule["required_primary_areas"]:
            if primary not in image_index:
                image_id = "img-" + primary.replace("_", "-")
                item = {"image_id": image_id, "primary_area": primary, "area_ids": [primary],
                        "shot_ids": [], "revision": 1, "prompt": "Test wide area " + primary,
                        "status": "planned", "asset_id": None, "error": None}
                image_index[primary] = item
                project["image_plan"].append(item)
            image = image_index[primary]
            image["shot_ids"].append(shot_id)
            refs.append(image["image_id"])
        for extra in set(areas) - set(rule["required_primary_areas"]):
            if extra not in image_index[rule["required_primary_areas"][0]]["area_ids"]:
                image_index[rule["required_primary_areas"][0]]["area_ids"].append(extra)
        components = [{"kind": "translation", "description": "Test adaptation: move forward",
                       "start_s": 0, "duration_s": seconds, "distance_m": 0.4, "angle_deg": None}]
        combined = kind in ("living_to_kitchen", "exterior_to_living")
        if combined:
            components.append({"kind": "pan", "description": "Test adaptation: pan right",
                               "start_s": 0, "duration_s": seconds, "distance_m": None, "angle_deg": 12})
        project["shots"].append({
            "shot_id": shot_id, "kind": kind, "covered_areas": areas, "duration_s": seconds,
            "continuous": True, "evidence_ids": [evidence_id],
            "framing": {"start": "Test initial composition", "end": "Test ending composition"},
            "camera": {"description": "Synthetic motion decision, not source timing.",
                       "motion_relationship": "simultaneous" if combined else "single",
                       "components": components, "visible_motion_evidence": "Foreground grows; side becomes visible.",
                       "timing_note": "Test travel estimate fitted to the full shot duration."},
            "reference_image_ids": refs, "prompt": None,
        })
    project["total_duration_s"] = sum(shot["duration_s"] for shot in project["shots"])
    return project


def approved(project, kind):
    project["approvals"][kind] = {"revision": project["revision"], "by": "delegated",
                                 "note": "Synthetic test metadata; not a real user approval."}


def image_prompts(project):
    project["image_mode"] = "prompt_to_image"
    project["stage"] = "image_prompt_package"
    approved(project, "concept")
    approved(project, "shot_plan")
    for image in project["image_plan"]:
        image["status"] = "prompt_ready"
    return project


def write_images(project, root):
    for number, image in enumerate(project["image_plan"], 1):
        path = Path(root) / "images" / (image["image_id"] + ".png")
        path.parent.mkdir(parents=True, exist_ok=True)
        Image.new("RGB", (160, 100), (number * 20, 60, 100)).save(path)
        asset_id = "ref-" + image["primary_area"].replace("_", "-")
        image.update(asset_id=asset_id, status="reviewed")
        project["assets"].append({
            "asset_id": asset_id, "image_id": image["image_id"], "revision": project["revision"],
            "role": "reference", "path": str(path.relative_to(root)),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "width": 160, "height": 100,
            "format": "PNG", "reviewed": True, "review_origin": "user_report",
            "review_note": "Synthetic pixels only; not a house/ceiling/naturalness review.",
        })


def add_video_prompts(project):
    for shot in project["shots"]:
        sections = {name: "Test authored section: " + name for name in VALIDATOR.RULES["prompt_sections"]}
        sections["OUTPUT SPECIFICATION"] = f"Home tour, {shot['duration_s']} seconds, 9:16."
        sections["REFERENCE IMAGE ROLE"] = "; ".join(
            key + " identifies its designed area, not a mandatory endpoint."
            for key in shot["reference_image_ids"]
        )
        sections["CAMERA MOVEMENT"] = shot["camera"]["description"]
        sections["VISIBLE MOTION EVIDENCE"] = shot["camera"]["visible_motion_evidence"]
        sections["CONTINUITY AND AUDIO RULES"] = " ".join(VALIDATOR.RULES["prompt_constraints"].values())
        shot["prompt"] = {"method": "R2V", "revision": project["revision"],
                          "duration_s": shot["duration_s"],
                          "reference_image_ids": shot["reference_image_ids"].copy(), "sections": sections}
    project["stage"] = "prompt_package"
    return project


def final_project(root, prompt=True, kinds=("exterior", "living_to_kitchen", "bedroom", "bathroom")):
    project = planning(kinds)
    project.update(stage="image_final", image_mode="generate_image")
    project["image_batch"].update(execution="parallel", note="Synthetic execution metadata; no live batch was run.")
    for kind in project["approvals"]:
        approved(project, kind)
    write_images(project, root)
    return add_video_prompts(project) if prompt else project


class ProjectRulesTests(unittest.TestCase):
    def setUp(self):
        (WORKSPACE / "runs").mkdir(exist_ok=True)
        self.temp = TemporaryDirectory(dir=WORKSPACE / "runs")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def check(self, project):
        return VALIDATOR.validate_project(project, self.root)

    def invalid(self, project, fragment):
        result = self.check(project)
        self.assertFalse(result["valid"], result)
        self.assertTrue(any(fragment in message for message in result["errors"]), result)

    def test_blank_concept_and_legacy_version_are_distinct(self):
        self.assertTrue(self.check(blank())["valid"])
        project = planning()
        project.update(stage="concept", shots=[], image_plan=[], total_duration_s=0)
        project["design"] = blank()["design"]
        self.assertTrue(self.check(project)["valid"], self.check(project))
        self.invalid({"schema_version": "1.0"}, "Proyek V1")

    def test_plans_count_images_instead_of_endpoint_pairs(self):
        for kinds, count, seconds in (
            (("exterior", "living", "kitchen", "bedroom", "bathroom"), 5, 22),
            (("exterior", "living_to_kitchen", "bedroom", "bathroom"), 5, 20),
            (("exterior_to_living", "kitchen", "bedroom", "bathroom"), 5, 18),
            (("exterior", "living_to_kitchen", "bedroom", "laundry", "bathroom"), 6, 24),
            (("exterior", "living", "kitchen", "bedroom", "bathroom", "laundry", "wardrobe"), 7, 30),
        ):
            with self.subTest(kinds=kinds):
                result = self.check(planning(kinds))
                self.assertTrue(result["valid"], result)
                self.assertEqual(result["image_count"], count)
                self.assertEqual(result["total_duration_s"], seconds)

    def test_seven_image_prompts_are_valid_without_image_files(self):
        project = image_prompts(planning(("exterior", "living", "kitchen", "bedroom", "bathroom", "laundry", "wardrobe")))
        result = self.check(project)
        self.assertTrue(result["valid"], result)
        self.assertEqual(result["image_count"], 7)
        self.assertEqual(result["available_image_count"], 0)
        self.assertTrue(all(shot["prompt"] is None for shot in project["shots"]))

    def test_r2v_final_accepts_five_landscape_area_images_without_start_end(self):
        project = final_project(self.root)
        result = self.check(project)
        self.assertTrue(result["valid"], result)
        self.assertEqual(result["reviewed_image_count"], 5)
        self.assertEqual(len(project["shots"][1]["reference_image_ids"]), 2)
        self.assertFalse(any("frames" in shot for shot in project["shots"]))

    def test_both_connectors_need_their_two_distinct_areas(self):
        for kinds in (("exterior", "living_to_kitchen", "bedroom", "bathroom"),
                      ("exterior_to_living", "kitchen", "bedroom", "bathroom")):
            project = planning(kinds)
            shot = next(item for item in project["shots"] if item["kind"].endswith(("to_living", "to_kitchen")))
            shot["reference_image_ids"].pop()
            self.invalid(project, "dua referensi")

    def test_coverage_duration_and_sleeping_area_cannot_expand(self):
        self.invalid(planning(("exterior", "living_to_kitchen", "kitchen")), "Area sudah tercakup")
        self.invalid(planning(("exterior", "bedroom", "bedroom")), "Maksimal satu")
        project = planning()
        project["shots"][0]["duration_s"] = 4
        self.invalid(project, "durasi tidak sesuai")
        project = planning()
        project["shots"][2]["covered_areas"] = ["bedroom_guest"]
        self.invalid(project, "not one of")
        project = planning()
        project["total_duration_s"] = 19
        self.invalid(project, "total_duration_s")

    def test_integrated_functions_keep_four_seconds_and_one_sleeping_function(self):
        project = planning(("exterior", "living_to_kitchen", "bathroom_laundry"))
        self.assertTrue(self.check(project)["valid"], self.check(project))
        self.assertEqual(project["shots"][-1]["duration_s"], 4)
        project["shots"][1]["covered_areas"].append("sleeping_loft")
        project["knowledge"]["evidence"][1]["covered_areas"].append("sleeping_loft")
        project["image_plan"][1]["area_ids"].append("sleeping_loft")
        self.assertTrue(self.check(project)["valid"], self.check(project))
        bad = planning()
        bad["shots"][1]["covered_areas"].append("sleeping_loft")
        bad["knowledge"]["evidence"][1]["covered_areas"].append("sleeping_loft")
        bad["image_plan"][1]["area_ids"].append("sleeping_loft")
        self.invalid(bad, "Maksimal satu")

    def test_ceiling_and_connection_decisions_are_required_at_shot_plan(self):
        project = planning()
        project["design"]["ceiling"] = ""
        self.invalid(project, "design/ceiling")
        project["design"]["connections"] = []
        self.invalid(project, "design/connections")

    def test_source_failure_unknown_continuity_and_wrong_url_are_rejected(self):
        project = planning()
        project["knowledge"]["evidence"][0]["continuity"] = "unknown"
        self.invalid(project, "perlu bukti")
        project = planning()
        project["knowledge"]["evidence"][0]["analysis_url"] = "https://example.com/guessed"
        self.invalid(project, "URL anotasi")
        project = planning()
        item = project["knowledge"]["evidence"][0]
        item.update(access_status="failed", error="Test read failure", shot_ids=[], field_paths=[],
                    excerpt="", covered_areas=[], continuity="unknown")
        self.invalid(project, "belum dibaca")

    def test_camera_rotations_require_twelve_degrees_but_translation_does_not(self):
        project = planning()
        self.assertTrue(self.check(project)["valid"])
        project["shots"][1]["camera"]["components"][1]["angle_deg"] = 11.9
        self.invalid(project, "minimal 12")
        project = planning()
        project["shots"][0]["camera"]["components"][0]["distance_m"] = 0
        self.invalid(project, "jarak positif")

    def test_camera_simultaneous_and_sequential_timing_differ(self):
        project = planning()
        camera = project["shots"][1]["camera"]
        camera["motion_relationship"] = "sequential"
        camera["components"][0]["duration_s"] = 3
        camera["components"][1].update(start_s=3, duration_s=3)
        self.assertTrue(self.check(project)["valid"], self.check(project))
        camera["motion_relationship"] = "simultaneous"
        self.invalid(project, "durasi shot yang sama")
        camera["motion_relationship"] = "sequential"
        camera["components"][1]["start_s"] = 2
        self.invalid(project, "overlap")

    def test_camera_budget_and_finite_values_are_checked(self):
        project = planning()
        project["shots"][0]["camera"]["components"][0]["duration_s"] = 7
        self.invalid(project, "melampaui")
        project = planning()
        project["shots"][0]["camera"]["components"][0]["distance_m"] = float("inf")
        self.invalid(project, "finite")

    def test_final_assets_require_review_and_current_approvals(self):
        project = final_project(self.root, prompt=False)
        project["approvals"]["visual"] = None
        self.invalid(project, "approval/visual")
        project = final_project(self.root, prompt=False)
        project["assets"][0]["reviewed"] = False
        self.invalid(project, "review")
        project = final_project(self.root, prompt=False)
        project["approvals"]["concept"]["revision"] = 2
        self.invalid(project, "revisi lain")

    def test_image_mode_and_image_prompt_package_are_separate(self):
        project = image_prompts(planning())
        project["image_mode"] = "generate_image"
        self.invalid(project, "hanya untuk mode")
        project["image_mode"] = None
        self.invalid(project, "Mode gambar")

    def test_batch_claims_are_not_automatically_inferred_from_file_count(self):
        project = final_project(self.root, prompt=False)
        project["image_batch"]["execution"] = "sequential"
        self.invalid(project, "Pelaksanaan batch")
        project["image_batch"].update(request_mode="one_by_one", user_instruction="User test explicitly requests one by one.")
        self.assertTrue(self.check(project)["valid"], self.check(project))
        project["image_batch"]["user_instruction"] = None
        self.invalid(project, "instruksi eksplisit")
        project["image_batch"].update(request_mode="all_at_once", execution="unknown")
        self.invalid(project, "Pelaksanaan batch")
        project["image_batch"].update(execution="parallel", note="")
        self.invalid(project, "catatan dasar")

    def test_missing_wrong_hash_dimensions_and_format_are_rejected(self):
        project = final_project(self.root)
        asset = project["assets"][0]
        path = self.root / asset["path"]
        path.unlink()
        self.invalid(project, "file asli")
        project = final_project(self.root)
        project["assets"][0]["sha256"] = "0" * 64
        self.invalid(project, "SHA-256")
        project = final_project(self.root)
        project["assets"][0]["width"] = 99
        self.invalid(project, "dimensi aktual")
        project = final_project(self.root)
        project["assets"][0]["format"] = "JPEG"
        self.invalid(project, "format aktual")

    def test_malformed_or_animated_reference_is_not_a_valid_still(self):
        project = final_project(self.root)
        asset = project["assets"][0]
        path = self.root / asset["path"]
        path.write_bytes(b"broken image")
        asset["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
        self.invalid(project, "tidak dapat dibuka")

    def test_identical_files_and_reused_paths_cannot_fake_two_reference_images(self):
        project = final_project(self.root)
        project["assets"][1]["sha256"] = project["assets"][0]["sha256"]
        self.invalid(project, "identik")
        project = final_project(self.root)
        project["assets"][1]["path"] = project["assets"][0]["path"]
        self.invalid(project, "dua aset")

    def test_image_and_asset_versions_and_inverse_shot_map_must_match(self):
        project = final_project(self.root)
        project["image_plan"][0]["revision"] = 2
        self.invalid(project, "versi prompt/gambar")
        project = final_project(self.root)
        project["assets"][0]["revision"] = 2
        self.invalid(project, "versi aset")
        project = planning()
        project["image_plan"][0]["shot_ids"] = ["shot-99"]
        self.invalid(project, "peta shot pemakai")

    def test_path_escape_and_symlink_escape_are_rejected(self):
        project = final_project(self.root)
        project["assets"][0]["path"] = "../escape.png"
        self.invalid(project, "Path aset")
        project = final_project(self.root)
        asset = project["assets"][0]
        outside = self.root.parent / (self.root.name + "-outside.png")
        outside.write_bytes((self.root / asset["path"]).read_bytes())
        self.addCleanup(lambda: outside.unlink(missing_ok=True))
        link = self.root / "escape.png"
        link.symlink_to(outside)
        asset["path"] = "escape.png"
        self.invalid(project, "symlink aset")

    def test_r2v_prompt_has_nine_complete_sections_and_the_same_references(self):
        project = final_project(self.root)
        del project["shots"][0]["prompt"]["sections"]["VISIBLE MOTION EVIDENCE"]
        self.invalid(project, "required property")
        project = final_project(self.root)
        project["shots"][0]["prompt"]["reference_image_ids"] = project["shots"][1]["reference_image_ids"]
        self.invalid(project, "referensi berbeda")
        project = final_project(self.root)
        project["shots"][0]["prompt"]["sections"]["CAMERA MOVEMENT"] = "{{UNFILLED}}"
        self.invalid(project, "penanda template")
        project = final_project(self.root)
        project["shots"][0]["prompt"]["sections"]["REFERENCE IMAGE ROLE"] = "Unlabelled references"
        self.invalid(project, "setiap ID gambar")

    def test_prompt_versions_duration_audio_and_method_cannot_drift(self):
        project = final_project(self.root)
        project["shots"][0]["prompt"]["duration_s"] = 4
        self.invalid(project, "durasi prompt")
        project = final_project(self.root)
        project["shots"][0]["prompt"]["sections"]["CONTINUITY AND AUDIO RULES"] = "No explicit rules."
        self.invalid(project, "continuous/ambient")
        project = final_project(self.root)
        project["shots"][0]["prompt"]["method"] = "first_last"
        self.invalid(project, "expected")
        project = final_project(self.root)
        project["audio"]["music"] = True
        self.invalid(project, "audio harus")

    def test_failed_and_partial_images_stay_draft(self):
        project = image_prompts(planning())
        project["stage"] = "image_draft"
        project["image_plan"][0].update(status="failed", error="Test generator failure")
        self.assertTrue(self.check(project)["valid"], self.check(project))
        project["stage"] = "image_final"
        self.invalid(project, "gambar final")
        project["image_plan"][0]["error"] = None
        self.invalid(project, "mencatat error")

    def test_unknown_fields_and_boolean_duration_are_rejected(self):
        project = planning()
        project["shots"][0]["frames"] = {"start": None, "end": None}
        self.invalid(project, "Additional properties")
        project = planning()
        project["shots"][0]["duration_s"] = True
        self.invalid(project, "not of type")

    def test_cli_is_read_only_and_reports_invalid_json(self):
        path = self.root / "project.json"
        path.write_text(json.dumps(blank()))
        before = path.read_bytes()
        script = SKILL / "scripts/validate_project.py"
        run = subprocess.run([sys.executable, "-B", str(script), str(path)], capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(path.read_bytes(), before)
        path.write_text("{broken")
        run = subprocess.run([sys.executable, "-B", str(script), str(path)], capture_output=True, text=True)
        self.assertEqual(run.returncode, 2)


if __name__ == "__main__":
    unittest.main()
