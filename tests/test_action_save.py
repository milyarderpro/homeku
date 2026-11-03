"""Tests Homeku v1.3 processing, including FFmpeg, narratives and legacy replay."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from save_analysis_action import process, markdown, narrative_text
from test_validation import make_package


class ActionSaveTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "requests").mkdir()
        (self.root / "references").mkdir()
        (self.root / "video").mkdir()
        self.origin_cwd = Path.cwd()
        package = make_package(self.root)
        data = yaml.safe_load((package / "analysis.yaml").read_text())
        data["architecture"]["primary_style"] = "country_cottage"
        data["architecture"]["common_regions"] = ["north_america", "europe"]
        data["architecture"]["secondary_influences"] = []
        data["architecture"]["exterior_features"] = []
        data["architecture"]["interior_style"] = []
        data["architecture"]["style_confidence"] = "low"
        data["visual_style"] = {
            "dominant_colors": [{"name": "sage_green", "hex_approx": "#AABBCC"}],
            "lighting": ["daylight"], "setting": [], "season_appearance": None, "mood": ["calm"]
        }
        data["video_structure"] = {"type": "home_tour", "overall_pace": "slow", "transition_pattern": "hard_cut"}
        for s in data["shots"]:
            s.update({
                "scene": "living_room",
                "framing": {"start": "wide", "end": "medium", "view_angle": "eye_level"},
                "camera": {"movements": ["dolly_in"], "speed": "slow"},
                "focal_subject": "window",
                "visible_details": {"architectural": ["window"], "furniture_and_props": [], "environment": []},
                "lighting": "daylight", "transition_out": "cut",
                "confidence": {"camera": "medium", "visual_details": "high"},
                "observation_note": "test fixture",
            })
        self.data = data
        shutil.rmtree(package)
        self.source = self.root / "video/test.mp4"
        subprocess.run([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-nostdin", "-y",
            "-f", "lavfi", "-i", "testsrc2=size=320x240:rate=2:duration=6",
            "-c:v", "mpeg4", "-q:v", "4", str(self.source)
        ], check=True)
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.name", "Unit Test"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=self.root, check=True)
        subprocess.run(["git", "add", "video/test.mp4"], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", "initial video"], cwd=self.root, check=True)
        sha = subprocess.check_output(["git", "rev-parse", "HEAD:video/test.mp4"], cwd=self.root, text=True).strip()
        self.req = {
            "schema_version": "1.0", "status": "approved",
            "request_id": "test-video-00001",
            "video": {"path": "video/test.mp4", "blob_sha": sha},
            "analysis_yaml": yaml.safe_dump(data, allow_unicode=True),
            "keyframe_times_s": [1.0, 4.0],
        }
        (self.root / "requests/save.json").write_text(json.dumps(self.req), encoding="utf-8")
        os.chdir(self.root)

    def tearDown(self):
        os.chdir(self.origin_cwd)
        self.tmp.cleanup()

    def test_complete_package_and_replay(self):
        out = process(self.root, "actions-jpg-test")
        self.assertEqual(out["status"], "saved")
        self.assertEqual(out["video_id"], "VID-001")
        self.assertEqual(out["file_count"], 5)
        package = self.root / "references" / out["video_id"]
        stored = yaml.safe_load((package / "analysis.yaml").read_text(encoding="utf-8"))
        self.assertEqual(stored["architecture"]["common_regions"], ["north_america", "europe"])
        self.assertIn("| Wilayah terkait gaya desain | north america, europe |",
                      (package / "analysis.md").read_text(encoding="utf-8"))
        self.assertEqual(json.loads((self.root/"requests/result.json").read_text())["request_id"],self.req["request_id"])
        repeat = process(self.root, "actions-jpg-test")
        self.assertEqual(repeat["status"], "already_saved")
        self.assertEqual(len(list((self.root/"references").glob("VID-*"))), 1)

    def test_reject_sha_mismatch_without_folder(self):
        self.req["video"]["blob_sha"] = "0"*40
        (self.root / "requests/save.json").write_text(json.dumps(self.req))
        with self.assertRaisesRegex(ValueError, "SHA mismatch"):
            process(self.root, "actions-jpg-test")
        self.assertFalse(any((self.root/"references").iterdir()))

    def test_legacy_request_without_regions(self):
        self.data["architecture"].pop("common_regions", None)
        self.req["analysis_yaml"] = yaml.safe_dump(self.data, allow_unicode=True)
        (self.root / "requests/save.json").write_text(json.dumps(self.req), encoding="utf-8")
        out = process(self.root, "actions-jpg-test")
        self.assertEqual(out["status"], "saved")
        md = (self.root / "references" / out["video_id"] / "analysis.md").read_text(encoding="utf-8")
        self.assertIn("| Wilayah terkait gaya desain | Tidak diketahui |", md)


    def add_narratives(self):
        self.req["shot_narratives"] = {
            s["id"]: {
                "architectural": {
                    "text": "Sebuah jendela terlihat di ruangan.",
                    "covered_indices": [0],
                },
                "furniture_and_props": {"text": None, "covered_indices": []},
                "environment": {"text": None, "covered_indices": []},
            }
            for s in self.data["shots"]
        }
        (self.root / "requests/save.json").write_text(
            json.dumps(self.req, ensure_ascii=False), encoding="utf-8")

    def add_detailed_scenes(self):
        """Hypothetical exterior + interior fixture; checks YAML/narrative parity."""
        exterior, interior = self.data["shots"]
        exterior["scene"] = "exterior_front"
        exterior["focal_subject"] = "house_facade"
        exterior["visible_details"] = {
            "architectural": [
                "steep_gabled_roof",
                "white_horizontal_wood_siding",
                "tall_black_framed_windows",
            ],
            "furniture_and_props": [
                "two_wooden_chairs_on_front_porch",
                "small_round_table_between_chairs",
            ],
            "environment": [
                "large_tree_with_yellow_leaves_left_of_house",
                "green_rice_field_beside_house",
                "distant_mountain_range_behind_roofline",
                "clear_blue_sky",
            ],
        }
        interior["scene"] = "living_room"
        interior["focal_subject"] = "seating_area"
        interior["visible_details"] = {
            "architectural": [
                "exposed_wood_ceiling_beams",
                "tall_black_framed_windows",
                "light_wood_appearance_flooring",
            ],
            "furniture_and_props": [
                "cream_fabric_sofa_facing_stone_fireplace",
                "natural_wood_coffee_table_in_front_of_sofa",
                "beige_area_rug_under_coffee_table",
                "potted_green_plant_beside_window",
            ],
            "environment": ["green_leafy_trees_visible_through_windows"],
        }
        texts = {
            "shot-01": {
                "architectural": (
                    "Atap rumah berbentuk pelana dengan kemiringan curam. "
                    "Fasad memakai panel kayu horizontal berwarna putih, "
                    "serta jendela-jendela tinggi dengan bingkai hitam."),
                "furniture_and_props": (
                    "Di teras depan terlihat dua kursi kayu. "
                    "Sebuah meja bundar kecil berada di antara kedua kursi."),
                "environment": (
                    "Di sebelah kiri rumah terdapat pohon besar dengan dedaunan kuning. "
                    "Hamparan sawah hijau berada di samping rumah, "
                    "sementara pegunungan terlihat di kejauhan di balik garis atap. "
                    "Langit tampak biru cerah."),
            },
            "shot-02": {
                "architectural": (
                    "Ruang tamu memiliki balok kayu terekspos pada plafon, "
                    "jendela-jendela tinggi dengan bingkai hitam, "
                    "dan lantai berpenampilan kayu berwarna terang."),
                "furniture_and_props": (
                    "Sofa berlapis kain krem menghadap perapian batu. "
                    "Di depan sofa terdapat meja kopi kayu alami dengan "
                    "karpet berwarna beige di bawahnya. "
                    "Tanaman hijau dalam pot ditempatkan di samping jendela."),
                "environment": (
                    "Pepohonan berdaun hijau terlihat melalui jendela ruang tamu."),
            },
        }
        self.req["analysis_yaml"] = yaml.safe_dump(self.data, allow_unicode=True)
        self.req["shot_narratives"] = {
            s["id"]: {
                category: {
                    "text": texts[s["id"]][category],
                    "covered_indices": list(range(len(source))),
                }
                for category, source in s["visible_details"].items()
            }
            for s in self.data["shots"]
        }
        (self.root / "requests/save.json").write_text(
            json.dumps(self.req, ensure_ascii=False), encoding="utf-8")
        return texts

    def test_rich_exterior_interior_end_to_end_and_semantic_spot_check(self):
        """Test pipeline parity with visually plausible, explicitly fictional observations."""
        texts = self.add_detailed_scenes()
        out = process(self.root, "actions-jpg-test")
        self.assertEqual(out["status"], "saved")
        self.assertEqual(out["shot_count"], 2)
        self.assertEqual(out["file_count"], 5)
        folder = self.root / "references" / out["video_id"]
        self.assertTrue((folder / "storyboard.jpg").is_file())
        self.assertTrue((folder / "shot-01.jpg").is_file())
        self.assertTrue((folder / "shot-02.jpg").is_file())
        stored = yaml.safe_load((folder / "analysis.yaml").read_text(encoding="utf-8"))
        self.assertNotIn("shot_narratives", stored)
        for before, after in zip(self.data["shots"], stored["shots"]):
            self.assertEqual(after["visible_details"], before["visible_details"])
            self.assertEqual(after["scene"], before["scene"])
        self.assertEqual([s["scene"] for s in stored["shots"]],
                         ["exterior_front", "living_room"])
        self.assertEqual([s["keyframe"] for s in stored["shots"]],
                         ["references/VID-001/shot-01.jpg",
                          "references/VID-001/shot-02.jpg"])
        md = (folder / "analysis.md").read_text(encoding="utf-8")
        exterior = md.split("### Shot 01 —", 1)[1].split("### Shot 02 —", 1)[0]
        interior = md.split("### Shot 02 —", 1)[1].split(
            "## 8. Kualitas dan Ketidakpastian Analisis", 1)[0]
        for index, section in enumerate((exterior, interior), 1):
            sid = f"shot-{index:02d}"
            self.assertEqual(section.count("**Detail yang terlihat**"), 1)
            for category, label in (("architectural", "Arsitektur"),
                                    ("furniture_and_props", "Furnitur dan properti"),
                                    ("environment", "Lingkungan")):
                self.assertEqual(section.count("**" + label + "**"), 1)
                self.assertIn(narrative_text(texts[sid][category]), section)
            self.assertNotIn("Tidak ada detail yang tercatat.", section)
        # Manual source/target spot-check assertions: relative position, color,
        # object count and material remain present in the correct shot.
        for term in ("atap rumah", "panel kayu horizontal berwarna putih",
                     "dua kursi kayu", "pohon besar dengan dedaunan kuning",
                     "sawah hijau", "pegunungan", "langit tampak biru cerah"):
            self.assertIn(term.lower(), exterior.lower())
            self.assertNotIn(term.lower(), interior.lower())
        for term in ("balok kayu", "lantai berpenampilan kayu",
                     "sofa berlapis kain krem menghadap perapian batu",
                     "karpet berwarna beige", "di samping jendela",
                     "Pepohonan berdaun hijau"):
            self.assertIn(term.lower(), interior.lower())
        self.assertEqual(
            json.loads((self.root / "requests/result.json").read_text())["request_id"],
            self.req["request_id"])
        self.assertEqual(process(self.root, "actions-jpg-test")["status"], "already_saved")

    def test_natural_narrative_save_without_changing_yaml_facts(self):
        self.add_narratives()
        out = process(self.root, "actions-jpg-test")
        self.assertEqual(out["status"], "saved")
        package = self.root / "references" / out["video_id"]
        final_yaml = yaml.safe_load((package / "analysis.yaml").read_text(encoding="utf-8"))
        self.assertEqual(
            [s["visible_details"] for s in final_yaml["shots"]],
            [s["visible_details"] for s in self.data["shots"]])
        self.assertNotIn("shot_narratives", final_yaml)
        md = (package / "analysis.md").read_text(encoding="utf-8")
        self.assertEqual(md.count("Sebuah jendela terlihat di ruangan."), 2)
        self.assertEqual(md.count("Tidak ada detail yang tercatat."), 4)
        self.assertEqual(md.count("**Arsitektur**"), 2)
        self.assertIn("<img src=\"shot-02.jpg\"", md)
        self.assertNotIn("- **Arsitektur:** window", md)
        self.assertEqual(len(list(package.glob("*.jpg"))), 3)

    def test_invalid_present_narratives_fail_before_any_files(self):
        self.add_narratives()
        self.req["shot_narratives"]["shot-02"]["architectural"]["covered_indices"] = []
        (self.root / "requests/save.json").write_text(json.dumps(self.req), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "covered_indices"):
            process(self.root, "actions-jpg-test")
        self.assertFalse(any((self.root / "references").iterdir()))
        self.assertFalse((self.root / "requests/result.json").exists())

    def test_null_narratives_do_not_fallback(self):
        self.req["shot_narratives"] = None
        (self.root / "requests/save.json").write_text(json.dumps(self.req))
        with self.assertRaisesRegex(ValueError, "shot_narratives must be an object"):
            process(self.root, "actions-jpg-test")

    def test_html_and_markdown_are_escaped_as_literal_prose(self):
        self.add_narratives()
        self.req["shot_narratives"]["shot-01"]["architectural"]["text"] = (
            "Jendela <script>alert(1)</script> dan **bingkai** [klik](https://example.com).")
        (self.root / "requests/save.json").write_text(json.dumps(self.req), encoding="utf-8")
        out = process(self.root, "actions-jpg-test")
        md = (self.root / "references" / out["video_id"] / "analysis.md").read_text(encoding="utf-8")
        self.assertNotIn("<script>", md)
        self.assertIn("&lt;script&gt;", md)
        self.assertIn(r"\*\*bingkai\*\*", md)
        self.assertIn(r"\[klik\]\(https://example.com\)", md)

    def test_idle_request_does_nothing(self):
        (self.root / "requests/save.json").write_text('{"schema_version":"1.0","status":"idle"}')
        self.assertEqual(process(self.root, "main"), {"status": "idle"})

if __name__=="__main__":
    unittest.main()
