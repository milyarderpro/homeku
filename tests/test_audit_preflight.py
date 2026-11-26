"""Preflight exercises compact working files with native video metadata."""
import copy
import json
from pathlib import Path
from unittest.mock import patch
import unittest
from . import test_prepare
from homeku.audit_session import mark_viewed
from homeku.authoring import check_camera, complete, prepare
from homeku.common import LibraryError, read_json, sha256
from homeku.preflight import camera_input, check_inputs
from homeku.video import frame_times, probe_video


def normal():
    return read_json(Path(__file__).resolve().parents[1] / "audit/examples/normal/audit.json")


class PreflightTests(test_prepare.VideoFixture, unittest.TestCase):
    def test_camera_checks_before_design_and_uses_native_bounds(self):
        source = self.video("camera-only")
        work = prepare(source, [], self.work / "audit")
        shot = normal()["shots"][0]
        shot = {key: shot[key] for key in ("shot", "start_s", "end_s", "camera")}
        info = probe_video(source)
        times = frame_times(source, info=info)
        native, = work["shots"]
        records = [item["record"] for item in work["passes"]]
        with self.assertRaisesRegex(LibraryError, "viewed coverage"):
            camera_input(shot, native, records, source, info, times)
        for row in records:
            row["viewed_frame_indices"] = row["selected_frame_indices"][:]
        self.assertEqual(camera_input(shot, native, records, source, info, times), shot["camera"])
        for edit, message in (
            (lambda s: s["camera"]["phases"][0].update(end_s=.8), "timeline incomplete"),
            (lambda s: s["camera"]["phases"][0].update(evidence=[0, 12]), "outside phase"),
            (lambda s: s["camera"]["phases"][0]["observations"].pop("translation"), "translation"),
            (lambda s: s.update(composition={"production_start": {
                "frame_index": 0, "composition_summary": "Ambang."}}), "after native Start"),
        ):
            with self.subTest(message=message), self.assertRaisesRegex(LibraryError, message):
                changed = copy.deepcopy(shot)
                edit(changed)
                camera_input(changed, native, records, source, info, times)

    def test_independent_bad_structure_precedes_probe(self):
        audit = normal()
        del audit["design"]["size"]["floor_area_m2"]
        with patch("homeku.video._probe_video_uncached") as probe:
            result = check_inputs("missing.mp4", audit, {})
        self.assertFalse(result["ok"])
        self.assertIsNone(result["context"])
        self.assertIn("/audit/design/size/floor_area_m2", {e["path"] for e in result["errors"]})
        self.assertIn("/audit-info/method", {e["path"] for e in result["errors"]})
        probe.assert_not_called()

    def test_prior_audit_format_requests_a_fresh_audit(self):
        audit = normal()
        audit["schema_version"] = "3.0"
        with patch("homeku.video._probe_video_uncached") as probe:
            result = check_inputs("missing.mp4", audit, {})
        self.assertFalse(result["ok"])
        [error] = result["errors"]
        self.assertEqual(error["path"], "/audit/schema_version")
        self.assertIn("Audit ulang MP4 dengan kit HOMEKU 3.1", error["action"])
        probe.assert_not_called()

    def test_profile_errors_precede_source_probe(self):
        audit = normal()
        design = audit["design"]
        design.update(house_type={"value": None, "state": "unknown", "evidence": []},
                      palette=[{"value": "Ivory", "role": "Dominan", "hex": "#ZZZZZZ",
                                "state": "observed", "evidence": [0]}])
        info = {"method": "Fixture", "limitations": "Synthetic fixture",
                "ai": {"provider": "fixture", "model": "fixture", "model_build": None},
                "reviewed_ranges": [{"start_s": 0, "end_s": 1, "mode": "sampling"}],
                "frame_reviews": [{"shot_id": "shot-01", "start_s": 0, "end_s": 1, "mode": "sampling",
                                   "sampling_fps": 6, "selected_frame_indices": [0],
                                   "viewed_frame_indices": [0], "reason": "Fixture"}]}
        with patch("homeku.video._probe_video_uncached") as probe:
            result = check_inputs("missing.mp4", audit, info)
            self.assertIn("/audit/design/palette/0/hex", {e["path"] for e in result["errors"]})
            design["palette"][0]["hex"] = "#F0E8DA"
            design["features"].append({"aspect": "palette", "value": "Ivory", "state": "observed",
                                       "evidence": [0]})
            result = check_inputs("missing.mp4", audit, info)
            self.assertIn("/audit/design/palette", {e["path"] for e in result["errors"]})
            probe.assert_not_called()

    def test_native_context_is_reusable_and_viewed_is_required(self):
        source = self.video("preflight")
        work = prepare(source, [], self.work / "audit")
        audit = normal()
        audit["id"] = source.stem
        Path(work["audit"]).write_text(json.dumps(audit))
        info = {"method": "Fixture inspection", "limitations": "Synthetic fixture",
                "ai": {"provider": "fixture", "model": "fixture", "model_build": None},
                "frame_reviews": [], "reviewed_ranges": []}
        Path(work["audit_info"]).write_text(json.dumps(info))
        with self.assertRaisesRegex(LibraryError, "viewed coverage"):
            check_camera(work["session"])
        mark_viewed(work["session"], all_frames=True, all_passes=True)
        check_camera(work["session"])
        complete(work["audit"], session_path=work["session"])
        authored = read_json(Path(work["audit"]))
        logs = read_json(Path(work["audit_info"]))
        with patch("homeku.video._probe_video_uncached", side_effect=AssertionError("expected session cache")):
            result = check_inputs(source, authored, logs, session_path=work["session"])
        self.assertTrue(result["ok"], result["errors"])
        self.assertEqual(result["context"]["sha256"], sha256(source))
        self.assertEqual(result["context"]["times"], frame_times(source))
        for alter in (
            lambda s: s["camera"]["phases"][0].update(notation="Dolly-In"),
            lambda s: s["camera"]["phases"][0]["observations"].update(rotation="Judgment changed."),
            lambda s: s["camera"]["phases"][0].update(end_s=1.1),
            lambda s: s["camera"]["tempo"].update(description="Tempo berubah."),
            lambda s: s["composition"].update(
                production_start={"frame_index": 4, "composition_summary": "Kamera dari dekat ambang."}),
        ):
            changed = copy.deepcopy(authored)
            alter(changed["shots"][0])
            result = check_inputs(source, changed, logs, session_path=work["session"])
            self.assertFalse(result["ok"])
            [error] = result["errors"]
            self.assertEqual(error["path"], "/session")
            self.assertRegex(error["message"], r"shot-01/(camera|production_start)")
        authored["shots"][0]["design"][0]["architecture"]["text"] = "Deskripsi desain diperbarui."
        self.assertTrue(check_inputs(source, authored, logs, session_path=work["session"])["ok"])
