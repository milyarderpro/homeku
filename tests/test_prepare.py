"""Prepare/session regression tests on synthetic videos; never real audit claims."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from homeku.authoring import check_camera, complete, prepare, update_shot
from homeku.video import frame_times, selected_indices, probe_video
from homeku.common import LibraryError, read_json
from homeku.audit_session import load_session, mark_viewed


class VideoFixture:
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.work = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def video(self, name, *, rate=10, duration=1.2, filters=None, audio=False):
        path = self.work / (name + ".mp4")
        command = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]
        if audio:
            command += ["-f", "lavfi", "-i", "sine=frequency=1000:sample_rate=8000"]
        command += ["-f", "lavfi", "-i", f"testsrc2=size=96x160:rate={rate}"]
        if audio:
            command += ["-map", "0:a", "-map", "1:v", "-c:a", "aac"]
        else:
            command += ["-an"]
        if filters:
            command += ["-vf", filters, "-vsync", "vfr"]
        command += ["-t", str(duration), "-c:v", "mpeg4", "-q:v", "5", "-threads", "1", str(path)]
        subprocess.run(command, check=True, capture_output=True, timeout=30)
        return path


class PrepareTests(VideoFixture, unittest.TestCase):
    def test_prepare_has_compact_source_native_midpoint_and_no_viewed(self):
        source = self.video("basic")
        result = prepare(source, [], self.work / "audit")
        value = read_json(Path(result["audit"]))
        self.assertEqual(value["schema_version"], "3.1")
        self.assertNotIn("profile", value)
        self.assertEqual(value["design"]["house_type"]["value"], "{{HOUSE_TYPE}}")
        self.assertEqual(value["design"]["palette"], [])
        self.assertEqual(value["areas"], [])
        self.assertEqual([p["frame_index"] for p in value["shots"][0]["panels"]], [0, 6, 11])
        row = result["shots"][0]
        self.assertEqual((row["first"], row["middle"], row["last"]), (0, 6, 11))
        times = frame_times(source)
        baseline = next(p["record"] for p in result["passes"] if p["record"]["mode"] == "sampling")
        self.assertEqual(baseline["sampling_fps"], 6)
        self.assertEqual(baseline["selected_frame_indices"],
                         selected_indices(times, 0, 1.2, 6, source_fps=10))
        self.assertTrue(any(p["record"]["selected_frame_indices"] == [6]
                            for p in result["passes"]))
        self.assertTrue(all(p["record"]["viewed_frame_indices"] == [] for p in result["passes"]))
        session = read_json(Path(result["session"]))
        self.assertEqual(session["format_version"], "3.1")
        self.assertNotIn("contract_version", session)
        load_session(Path(result["session"]))

    def test_low_fps_source_uses_all_native_frames(self):
        source = self.video("five", rate=5)
        result = prepare(source, [], self.work / "audit")
        baseline = result["passes"][0]["record"]
        self.assertEqual(baseline["mode"], "frame-by-frame")
        self.assertIsNone(baseline["sampling_fps"])
        self.assertEqual(baseline["selected_frame_indices"], list(range(6)))
        self.assertEqual(baseline["viewed_frame_indices"], [])

    def test_short_shots_use_native_frames_without_crossing_cut(self):
        source = self.video("short", rate=30, duration=0.4)
        times = frame_times(source)
        result = prepare(source, [6], self.work / "audit")
        self.assertEqual(len(result["shots"]), 2)
        self.assertEqual(result["shots"][0]["end_s"], times[6])
        self.assertEqual(result["shots"][1]["start_s"], times[6])
        for item, expected in zip(result["passes"], (list(range(6)), list(range(6, 12)))):
            record = item["record"]
            self.assertEqual(record["mode"], "frame-by-frame")
            self.assertEqual(record["selected_frame_indices"], expected)
            self.assertFalse(record["viewed_frame_indices"])

    def test_vfr_pts_drive_sampling_and_cut_boundaries(self):
        source = self.video("irregular", rate=30, duration=2.4,
                            filters=r"select=not(mod(n\,3))+eq(n\,1)")
        times = frame_times(source)
        gaps = {round(b - a, 6) for a, b in zip(times, times[1:])}
        self.assertGreater(len(gaps), 1)
        result = prepare(source, [8], self.work / "audit")
        self.assertEqual(result["shots"][0]["end_s"], times[8])
        by_shot = {s["shot"]: s for s in result["shots"]}
        info = probe_video(source)
        fps = info["fps"]["numerator"] / info["fps"]["denominator"]
        for item in result["passes"]:
            record = item["record"]
            row = by_shot[record["shot_id"]]
            self.assertTrue(all(row["first"] <= i <= row["last"]
                                for i in record["selected_frame_indices"]))
            self.assertEqual(record["selected_frame_indices"], selected_indices(
                times, record["start_s"], record["end_s"], record["sampling_fps"] or 6,
                native=record["mode"] == "frame-by-frame", source_fps=fps))

    def test_audio_first_input_uses_actual_video_stream(self):
        source = self.video("audio-first", audio=True)
        self.assertEqual(probe_video(source)["video_stream_index"], 1)
        result = prepare(source, [], self.work / "audit")
        self.assertEqual(result["shots"][0]["last"], 11)
        self.assertTrue(all(p["record"]["viewed_frame_indices"] == [] for p in result["passes"]))

    def test_update_shot_preserves_other_observations_and_rejects_invalid_patch(self):
        result = prepare(self.video("patch"), [6], self.work / "audit")
        audit_path = Path(result["audit"])
        original = read_json(audit_path)
        patch = self.work / "patch.json"
        patch.write_text(json.dumps({"camera": {"description": "Kamera mundur."}}))
        update_shot(result["session"], "shot-02", patch)
        updated = read_json(audit_path)
        self.assertEqual(updated["shots"][0], original["shots"][0])
        self.assertEqual(updated["shots"][1]["camera"]["phases"],
                         original["shots"][1]["camera"]["phases"])
        self.assertEqual(updated["shots"][1]["camera"]["description"], "Kamera mundur.")
        saved = audit_path.read_bytes()
        for changes in ({"start_s": 0}, {"camera": {"camera_summary": "Dolly-Out"}},
                        {"panels": [{"frame_index": 6, "timestamp_s": 0.6}]}):
            with self.subTest(changes=changes):
                patch.write_text(json.dumps(changes))
                with self.assertRaises(LibraryError):
                    update_shot(result["session"], "shot-02", patch)
                self.assertEqual(audit_path.read_bytes(), saved)

    def test_complete_preserves_observations_and_only_copies_explicit_viewed(self):
        source = self.video("completion")
        result = prepare(source, [], self.work / "audit")
        audit_path = Path(result["audit"])
        template = Path(__file__).resolve().parents[1] / "audit/examples/normal/audit.json"
        audit = read_json(template)
        audit["id"] = source.stem
        phase = audit["shots"][0]["camera"]["phases"][0]
        phase.update(notation="Dolly-Out (~1,6x) + Orbit Left", depth_direction="OUT")
        audit_path.write_text(json.dumps(audit))
        info_path = Path(result["audit_info"])
        info = read_json(info_path)
        info["method"] = "Pemeriksaan fixture"
        info_path.write_text(json.dumps(info))
        resumed = prepare(source, [], self.work / "audit", resume=True)
        self.assertTrue(resumed["resumed"])
        self.assertEqual(read_json(audit_path), audit)
        with self.assertRaisesRegex(LibraryError, "Run check-camera"):
            complete(audit_path, session_path=result["session"])
        self.assertEqual(read_json(audit_path), audit)
        self.assertEqual(read_json(info_path), info)
        mark_viewed(result["session"], all_frames=True, all_passes=True)
        check_camera(result["session"])
        complete(audit_path, session_path=result["session"])
        phase["notation"] = "Dolly-Out (~1.6×) + Orbit Left"
        self.assertEqual(read_json(audit_path), audit)
        logs = read_json(info_path)
        self.assertEqual(logs["method"], info["method"])
        self.assertTrue(logs["reviewed_ranges"])
        self.assertTrue(all(row["viewed_frame_indices"] == row["selected_frame_indices"]
                            for row in logs["frame_reviews"]))
        with self.assertRaisesRegex(LibraryError, "Source/cuts differ"):
            prepare(source, [6], self.work / "audit", resume=True)

    def test_complete_rejects_changed_source_and_old_session(self):
        source = self.video("bound")
        result = prepare(source, [], self.work / "audit")
        session_path = Path(result["session"])
        original = session_path.read_bytes()
        session = read_json(session_path)
        for version in ("2.5", "9.0"):
            session["format_version"] = version
            session_path.write_text(json.dumps(session))
            with self.subTest(version=version), self.assertRaisesRegex(LibraryError, "Unsupported audit session"):
                complete(result["audit"], session_path=session_path)
        session_path.write_bytes(original)
        self.video("bound", rate=5)
        with self.assertRaisesRegex(LibraryError, "Source changed"):
            complete(result["audit"], session_path=session_path)
