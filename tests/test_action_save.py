"""Tests Homeku v1.2 processing, including FFmpeg and idempotent request IDs."""
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
from save_analysis_action import process, markdown
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
