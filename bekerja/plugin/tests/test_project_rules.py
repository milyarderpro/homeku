"""Regression checks for stage-2 contracts, not a live model/video evaluation."""
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
    data = blank()
    data.update(stage="shot_plan", brief="Fixture HOMEKU, not a real production.",
                concept={"title": "Fixture", "summary": "Contract regression case."})
    data["knowledge"].update(ref="main", commit=COMMIT, route="github_connector")
    data["design"] = {key: (["entry"] if key == "anchors" else "fixture")
                      for key in data["design"]}
    sources = {
        "exterior": ("edh022", "shot-01", "exterior_front"),
        "living_to_kitchen": ("edh022", "shot-02", "combined_living_room_and_kitchen"),
        "bedroom": ("edh022", "shot-03", "bedroom"),
        "bathroom": ("edh022", "shot-04", "bathroom"),
        "exterior_to_living": ("edh016", "shot-01", "exterior_front_to_living_room"),
        "living": ("edh058", "shot-02", "living_room"),
        "kitchen": ("edh058", "shot-03", "kitchen"),
        "laundry": ("edh030", "shot-03", "laundry_room"),
        "wardrobe": ("edh058", "shot-05", "walk_in_closet"),
        "bathroom_laundry": ("edh033", "shot-03", "combined_bathroom_and_laundry"),
    }
    for number, kind in enumerate(kinds, 1):
        ident = f"shot-{number:02d}"
        spec = VALIDATOR.RULES["shot_kinds"][kind]
        areas = deepcopy(spec["coverage_sets"][0])
        ref, source_shot, scene = sources[kind]
        evidence_id = f"ev-{number}"
        data["knowledge"]["evidence"].append({
            "evidence_id": evidence_id, "reference_id": ref, "shot_ids": [source_shot],
            "analysis_url": f"https://github.com/milyarderpro/homeku/blob/{COMMIT}/references/{ref}/analysis.yaml",
            "field_paths": [f"/shots/{int(source_shot.split('-')[1])-1}/scene"],
            "excerpt": scene, "covered_areas": areas.copy(),
            "continuity": "annotated_continuous", "access_status": "read", "error": None,
        })
        data["shots"].append({
            "shot_id": ident, "kind": kind, "covered_areas": areas,
            "duration_s": spec["duration_s"], "continuous": True,
            "evidence_ids": [evidence_id],
            "framing": {"start": "Fixture start", "end": "Fixture end"},
            "camera": {"description": "Fixture continuous movement", "motion_relationship": "single"},
            "frames": {"start": None, "end": None}, "prompt": None,
        })
    data["total_duration_s"] = sum(shot["duration_s"] for shot in data["shots"])
    return data


def approved(data, kind):
    data["approvals"][kind] = {"revision": data["revision"], "by": "delegated",
                                "note": "Synthetic test metadata, not a real approval."}


class ProjectRulesTests(unittest.TestCase):
    def setUp(self):
        (WORKSPACE / "runs").mkdir(exist_ok=True)
        self.temp = TemporaryDirectory(dir=WORKSPACE / "runs")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def check(self, data):
        return VALIDATOR.validate_project(data, self.root)

    def assertInvalid(self, data, fragment):
        result = self.check(data)
        self.assertFalse(result["valid"], result)
        self.assertTrue(any(fragment in error for error in result["errors"]), result["errors"])

    def final_project(self, prompt=False):
        data = planning()
        data["stage"] = "prompt_package" if prompt else "visual_final"
        for kind in data["approvals"]:
            approved(data, kind)
        for shot in data["shots"]:
            for role, color in (("start", (120, 80, 10)), ("end", (25, 55, 85))):
                asset_id = f"{shot['shot_id']}-{role}"
                relative = f"frames/{asset_id}.png"
                path = self.root / relative
                path.parent.mkdir(exist_ok=True)
                Image.new("RGB", (9, 16), color).save(path)
                data["assets"].append({
                    "asset_id": asset_id, "shot_id": shot["shot_id"], "revision": 1,
                    "role": role, "path": relative,
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                    "width": 9, "height": 16, "reviewed": True,
                    "review_origin": "user_report",
                    "review_note": "Synthetic pixel fixture, not a visual house review.",
                })
                shot["frames"][role] = asset_id
            if prompt:
                shot["prompt"] = {
                    "revision": 1, "duration_s": shot["duration_s"],
                    "start_asset_id": shot["frames"]["start"], "end_asset_id": shot["frames"]["end"],
                    "text": "Fixture motion. " + " ".join(VALIDATOR.RULES["prompt_constraints"].values()),
                }
        return data

    def test_initial_template_and_concept_need_no_images(self):
        self.assertTrue(self.check(blank())["valid"])
        data = planning()
        data.update(stage="concept", shots=[], total_duration_s=0)
        data["design"] = blank()["design"]
        self.assertTrue(self.check(data)["valid"], self.check(data))

    def test_supported_plans_have_expected_totals(self):
        for kinds, expected in [
            (("exterior", "living", "kitchen", "bedroom", "bathroom"), 22),
            (("exterior", "living_to_kitchen", "bedroom", "bathroom"), 20),
            (("exterior_to_living", "kitchen", "bedroom", "bathroom"), 18),
            (("exterior", "living_to_kitchen", "bedroom", "laundry", "bathroom"), 24),
            (("exterior", "living_to_kitchen", "bathroom_laundry", "wardrobe"), 20),
        ]:
            with self.subTest(kinds=kinds):
                data = planning(kinds)
                result = self.check(data)
                self.assertTrue(result["valid"], result)
                self.assertEqual(result["total_duration_s"], expected)

    def test_sleeping_loft_replaces_separate_bedroom(self):
        data = planning(("exterior", "living_to_kitchen", "bathroom"))
        data["shots"][1]["covered_areas"].append("sleeping_loft")
        data["knowledge"]["evidence"][1].update(
            reference_id="edh060", shot_ids=["shot-02"],
            analysis_url=f"https://github.com/milyarderpro/homeku/blob/{COMMIT}/references/edh060/analysis.yaml",
            field_paths=["/shots/1/scene"], excerpt="living_room_kitchen_and_sleeping_loft",
            covered_areas=data["shots"][1]["covered_areas"].copy(),
        )
        self.assertTrue(self.check(data)["valid"], self.check(data))
        bad = planning()
        bad["shots"][1]["covered_areas"].append("sleeping_loft")
        bad["knowledge"]["evidence"][1]["covered_areas"].append("sleeping_loft")
        self.assertInvalid(bad, "Maksimal satu area tidur")

    def test_duration_not_uniform_and_total_must_match(self):
        data = planning()
        data["shots"][0]["duration_s"] = 4
        data["total_duration_s"] -= 2
        self.assertInvalid(data, "durasi tidak sesuai")
        data = planning()
        data["total_duration_s"] = 19
        self.assertInvalid(data, "total_duration_s")

    def test_combined_areas_cannot_repeat(self):
        for kinds in [
            ("exterior", "living_to_kitchen", "kitchen", "bedroom"),
            ("exterior_to_living", "living", "kitchen"),
            ("exterior", "bedroom", "bedroom"),
            ("exterior", "bathroom_laundry", "laundry"),
        ]:
            with self.subTest(kinds=kinds):
                self.assertInvalid(planning(kinds), "Area sudah tercakup")

    def test_renaming_bedroom_does_not_bypass_contract(self):
        data = planning()
        data["shots"][2]["covered_areas"] = ["bedroom_guest"]
        self.assertInvalid(data, "area tidak dikenal")

    def test_no_new_area_or_shot_kind(self):
        data = planning()
        data["shots"][2]["kind"] = "custom_room"
        self.assertInvalid(data, "jenis shot tidak dikenal")

    def test_every_shot_is_continuous_and_opening_is_exterior(self):
        data = planning()
        data["shots"][1]["continuous"] = False
        self.assertInvalid(data, "wajib kontinu")
        self.assertInvalid(planning(("bedroom", "bathroom")), "Shot pertama")

    def test_music_and_wrong_rules_version_rejected(self):
        data = planning()
        data["audio"]["music"] = True
        self.assertInvalid(data, "audio harus")
        data = planning()
        data["rules_version"] = "unknown"
        self.assertInvalid(data, "rules_version")

    def test_missing_or_unread_source_cannot_support_shot(self):
        data = planning()
        data["shots"][0]["evidence_ids"] = ["missing"]
        self.assertInvalid(data, "bukti sumber tidak ada")
        data = blank()
        data["knowledge"].update(ref="main", route="web", evidence=[{
            "evidence_id": "failed-read", "reference_id": "edh058", "shot_ids": [],
            "analysis_url": "https://github.com/milyarderpro/homeku/blob/main/references/edh058/analysis.yaml",
            "field_paths": [], "excerpt": "", "covered_areas": [],
            "continuity": "unknown", "access_status": "failed", "error": "Fixture unavailable.",
        }])
        self.assertTrue(self.check(data)["valid"], self.check(data))
        data.update(stage="concept", brief="Fixture", concept={"title": "Fixture", "summary": "Fixture"})
        self.assertInvalid(data, "Minimal satu bukti sumber")

    def test_source_scope_and_commit_must_match(self):
        data = planning()
        data["knowledge"]["evidence"][1]["covered_areas"] = ["living"]
        self.assertInvalid(data, "cakupan yang sama")
        data = planning()
        data["knowledge"]["evidence"][0]["analysis_url"] = "https://example.com/invented.yaml"
        self.assertInvalid(data, "URL anotasi")

    def test_visual_draft_requires_plan_approval_but_no_images(self):
        data = planning()
        data["stage"] = "visual_draft"
        self.assertInvalid(data, "approval/concept")
        approved(data, "concept")
        approved(data, "shot_plan")
        self.assertTrue(self.check(data)["valid"], self.check(data))

    def test_final_requires_two_frames_and_visual_approval(self):
        data = planning()
        data["stage"] = "visual_final"
        approved(data, "concept")
        approved(data, "shot_plan")
        self.assertInvalid(data, "frame start belum lengkap")
        self.assertInvalid(data, "approval/visual")

    def test_actual_png_pair_and_prompt_package_pass(self):
        data = self.final_project(prompt=True)
        self.assertTrue(self.check(data)["valid"], self.check(data))

    def test_final_missing_file_or_wrong_hash_rejected(self):
        data = self.final_project()
        (self.root / data["assets"][0]["path"]).unlink()
        self.assertInvalid(data, "file asli tidak tersedia")
        data["assets"].pop(0)
        self.assertInvalid(data, "pengikatan frame start")
        data = self.final_project()
        data["assets"][0]["sha256"] = "0" * 64
        self.assertInvalid(data, "SHA-256")

    def test_final_actual_dimensions_and_png_format_checked(self):
        data = self.final_project()
        path = self.root / data["assets"][0]["path"]
        Image.new("RGB", (18, 32)).save(path)
        self.assertInvalid(data, "dimensi aktual")
        path.write_bytes(b"not a png")
        data["assets"][0]["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
        self.assertInvalid(data, "gambar tidak dapat dibuka")

    def test_frame_ratio_review_and_role_binding_checked(self):
        data = self.final_project()
        data["assets"][0]["width"] = 10
        self.assertInvalid(data, "harus tepat 9:16")
        data = self.final_project()
        data["assets"][0]["reviewed"] = False
        self.assertInvalid(data, "belum diperiksa")
        data = self.final_project()
        data["shots"][0]["frames"]["start"] = data["shots"][0]["frames"]["end"]
        self.assertInvalid(data, "pengikatan frame start")

    def test_asset_prompt_and_approval_revisions_must_match(self):
        data = self.final_project(prompt=True)
        data["revision"] = 2
        self.assertInvalid(data, "versi aset")
        self.assertInvalid(data, "versi prompt")
        self.assertInvalid(data, "keputusan berasal")

    def test_prompt_uses_same_pair_duration_and_required_constraints(self):
        data = self.final_project(prompt=True)
        data["shots"][0]["prompt"]["end_asset_id"] = data["shots"][1]["frames"]["end"]
        self.assertInvalid(data, "pasangan frame")
        data["shots"][0]["prompt"]["duration_s"] = 4
        self.assertInvalid(data, "durasi prompt")
        data["shots"][0]["prompt"]["text"] = "Fixture with no explicit constraints."
        self.assertInvalid(data, "instruksi audio")
        self.assertInvalid(data, "instruksi continuous")

    def test_path_traversal_and_duplicate_asset_files_rejected(self):
        data = self.final_project()
        data["assets"][0]["path"] = "../outside.png"
        self.assertInvalid(data, "Path aset harus relatif")
        data = self.final_project()
        data["assets"][1]["path"] = data["assets"][0]["path"]
        self.assertInvalid(data, "file dipakai oleh dua")

    def test_schema_rejects_boolean_duration_and_unknown_fields(self):
        data = planning()
        data["shots"][0]["duration_s"] = True
        self.assertInvalid(data, "not of type")
        data = planning()
        data["automatic_publish"] = True
        self.assertInvalid(data, "Additional properties")

    def test_cli_is_read_only_and_rejects_bad_json(self):
        path = self.root / "project.json"
        path.write_text(json.dumps(blank()))
        before = path.read_bytes()
        run = subprocess.run([sys.executable, "-B", str(SKILL / "scripts/validate_project.py"), str(path)],
                             capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertTrue(json.loads(run.stdout)["valid"])
        self.assertEqual(path.read_bytes(), before)
        path.write_text("{broken")
        run = subprocess.run([sys.executable, "-B", str(SKILL / "scripts/validate_project.py"), str(path)],
                             capture_output=True, text=True)
        self.assertEqual(run.returncode, 2)

    def test_symlink_cannot_escape_project_directory(self):
        data = self.final_project()
        asset = data["assets"][0]
        outside = self.root.parent / (self.root.name + "-outside.png")
        outside.write_bytes((self.root / asset["path"]).read_bytes())
        self.addCleanup(lambda: outside.unlink(missing_ok=True))
        link = self.root / "escape.png"
        link.symlink_to(outside)
        asset["path"] = link.name
        self.assertInvalid(data, "symlink aset keluar")

    def test_valid_jpeg_content_is_rejected_as_png(self):
        data = self.final_project()
        asset = data["assets"][0]
        path = self.root / asset["path"]
        Image.new("RGB", (9, 16)).save(path, format="JPEG")
        asset["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
        self.assertInvalid(data, "format file harus PNG")

    def test_prompt_package_needs_prompt_and_honest_review_metadata(self):
        data = self.final_project(prompt=True)
        data["shots"][0]["prompt"] = None
        self.assertInvalid(data, "prompt final belum tersedia")
        data["assets"][0]["review_origin"] = None
        self.assertInvalid(data, "review memerlukan asal")


class ManifestFoundationTests(unittest.TestCase):
    def test_portable_identity_and_verified_publisher(self):
        manifest = json.loads((PLUGIN / "plugin.json").read_text())
        self.assertEqual(manifest["$schema"], "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json")
        self.assertEqual(manifest["name"], PLUGIN.name)
        self.assertRegex(manifest["version"], r"^(0|[1-9][0-9]*)[.](0|[1-9][0-9]*)[.](0|[1-9][0-9]*)(?:-[0-9A-Za-z.-]+)?(?:[+][0-9A-Za-z.-]+)?$")
        self.assertTrue(manifest["author"]["name"].strip())
        self.assertFalse({"skills", "apps", "mcpServers", "interface"} & manifest.keys())
        ui = manifest["extensions"]["com.openai"]["interface"]
        self.assertEqual(ui["developerName"], manifest["author"]["name"])
        self.assertLessEqual(len(ui["shortDescription"]), 30)
        self.assertEqual(ui["category"], "Creativity")
        self.assertIsInstance(ui["capabilities"], list)

    def test_no_server_or_source_archive_copied_into_package(self):
        self.assertFalse((PLUGIN / "mcp.json").exists())
        self.assertFalse((PLUGIN / ".app.json").exists())
        self.assertFalse((PLUGIN / "knowledge").exists())
        self.assertFalse((PLUGIN / "video").exists())

    def test_validator_runs_from_isolated_plugin_copy(self):
        from shutil import copytree
        (WORKSPACE / "runs").mkdir(exist_ok=True)
        with TemporaryDirectory(dir=WORKSPACE / "runs") as directory:
            isolated = Path(directory)
            copied = isolated / "home-productions"
            copytree(PLUGIN, copied)
            script = copied / "skills/produce-home-tour/scripts/validate_project.py"
            template = copied / "skills/produce-home-tour/assets/project-template.json"
            run = subprocess.run([sys.executable, "-B", str(script), str(template)],
                                 cwd=isolated, capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertTrue(json.loads(run.stdout)["valid"])


if __name__ == "__main__":
    unittest.main()
