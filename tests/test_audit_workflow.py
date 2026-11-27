"""Audit workspace and cut helpers on local synthetic sources."""
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch

from . import test_prepare
from homeku.audit_session import add_pass, mark_viewed
from homeku.audit_workflow import readiness, session_status
from homeku.authoring import prepare
from homeku.common import dumps, read_json, snapshot_hash

from .fixtures.factory import make_inputs


class ReadinessTests(test_prepare.VideoFixture, unittest.TestCase):
    def test_valid_video_and_missing_dependency(self):
        source = self.video("readiness")
        output = self.work / "working"
        self.assertTrue(readiness(source, output)["ok"])
        self.assertEqual(list(output.iterdir()), [])
        from importlib import import_module

        def missing(name):
            if name == "cv2":
                raise ImportError(name)
            return import_module(name)

        with patch("homeku.audit_workflow.import_module", side_effect=missing):
            result = readiness(source, output)
        self.assertFalse(result["ok"])
        self.assertIn("cv2", [row["check"] for row in result["checks"] if not row["ok"]])

    def test_bad_video_and_workspace_are_reported(self):
        source = self.work / "bad.mp4"
        source.write_bytes(b"invalid")
        result = readiness(source, source)
        self.assertFalse(result["ok"])
        self.assertEqual({row["check"] for row in result["checks"] if not row["ok"]}, {"workspace", "mp4"})


class SessionStatusTests(test_prepare.VideoFixture, unittest.TestCase):
    def test_partial_baseline_and_missing_review(self):
        prepared = prepare(self.video("partial"), [], self.work / "writing")
        session = self.work / "writing/session.json"
        mark_viewed(session, prepared["passes"][0]["id"], [0])
        original = session.read_bytes()
        status = session_status(session)
        self.assertEqual(status["receipt"]["missing"], ["candidate", "receipt"])
        self.assertNotIn(0, status["shots"][0]["baseline_unviewed"])
        self.assertTrue(status["shots"][0]["baseline_unviewed"])
        self.assertEqual(status["shots"][0]["camera"], "unchecked")
        self.assertEqual(session.read_bytes(), original)

    def test_status_counts_native_viewing_only_for_its_shot(self):
        prepared = prepare(self.video("native-viewed", duration=2.4), [12], self.work / "writing")
        session = prepared["session"]
        native = add_pass(session, "shot-01", native=True, reason="Periksa gerak di setiap frame.")["passes"][-1]
        self.assertEqual(native["record"]["mode"], "frame-by-frame")
        before = session_status(session)["shots"]
        self.assertTrue(before[0]["baseline_unviewed"])
        self.assertTrue(before[1]["baseline_unviewed"])
        baseline_id = before[0]["baseline_pass"]
        self.assertNotEqual(baseline_id, native["id"])

        first, second = before[0]["baseline_unviewed"][:2]
        mark_viewed(session, native["id"], [first, second])
        partial = session_status(session)["shots"]
        self.assertEqual(partial[0]["baseline_unviewed"], before[0]["baseline_unviewed"][2:])
        remaining_native = next(row for row in partial[0]["incomplete_passes"] if row["id"] == native["id"])
        self.assertEqual(remaining_native["undeclared_frame_indices"],
                         [i for i in native["record"]["selected_frame_indices"] if i not in (first, second)])
        mark_viewed(session, native["id"], all_frames=True)
        status = session_status(session)["shots"]
        self.assertEqual(status[0]["baseline_unviewed"], [])
        self.assertEqual(status[0]["baseline_pass"], baseline_id)
        remaining = {row["id"]: row["undeclared_frame_indices"] for row in status[0]["incomplete_passes"]}
        self.assertNotIn(native["id"], remaining)
        self.assertEqual(remaining[baseline_id], before[0]["baseline_unviewed"])
        for pass_id, indices in remaining.items():
            mark_viewed(session, pass_id, indices)
        status = session_status(session)["shots"]
        self.assertEqual(status[0]["incomplete_passes"], [])
        self.assertEqual(status[1], before[1])

    def test_scoped_camera_correction_and_receipt(self):
        audit, _ = make_inputs(self.work / "writing", self.video("status"))
        session = audit.with_name("session.json")
        self.assertEqual(session_status(session)["shots"][0]["camera"], "current")
        edited = read_json(audit)
        edited["shots"][0]["camera"]["description"] = "Koreksi contoh."
        audit.write_text(dumps(edited))
        candidate = self.work / "candidate"
        candidate.mkdir()
        payload = candidate / "audit.json"
        payload.write_text("{}")
        receipt = self.work / "receipt.json"
        self.assertEqual(session_status(session, candidate=candidate)["receipt"]["missing"], ["receipt"])
        receipt.write_text(dumps({"candidate": str(candidate), "snapshot_sha256": snapshot_hash(candidate)}))
        self.assertEqual(session_status(session, candidate=candidate, receipt=receipt)["receipt"]["state"], "matches")
        payload.write_text('{"edited": true}')
        status = session_status(session, candidate=candidate, receipt=receipt)
        self.assertEqual(status["shots"][0]["camera"], "stale")
        self.assertEqual(status["receipt"]["state"], "stale")


class CutPreviewTests(test_prepare.VideoFixture, unittest.TestCase):
    def test_cut_preview_preserves_native_vfr_and_leaves_cuts_to_auditor(self):
        from .test_audit import cli
        from homeku.video import frame_times
        import json

        source = self.work / "cut.mp4"
        subprocess.run([
            "ffmpeg", "-v", "error", "-f", "lavfi", "-i", "color=0x202020:size=96x160:rate=10:duration=0.6",
            "-f", "lavfi", "-i", "color=0x383838:size=96x160:rate=10:duration=0.6",
            "-filter_complex", "[0:v][1:v]concat=n=2:v=1:a=0,select=not(eq(n\\,2))",
            "-fps_mode", "vfr", "-c:v", "mpeg4", "-threads", "1", str(source),
        ], check=True, capture_output=True)
        result = cli("inspect", source, "--cut-preview", self.work / "preview")
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = json.loads(result.stdout)["cut_candidates"]
        self.assertEqual(len(rows), 1)
        after = rows[0]["after"]
        self.assertEqual(after["index"], 5)
        self.assertEqual(after["pts_s"], frame_times(source)[5])
        self.assertGreater(after["pts_s"], .5)
        self.assertEqual(rows[0]["before"]["index"], 4)
        self.assertTrue(Path(after["image"]).is_file())

        candidate = self.work / "candidate"
        media = candidate / "media"
        media.mkdir(parents=True)
        (candidate / "manifest.json").write_text("{}")
        original_snapshot = snapshot_hash(candidate)
        for output in (candidate, media / "preview"):
            with self.subTest(output=output):
                blocked = cli("inspect", source, "--cut-preview", output)
                self.assertEqual(blocked.returncode, 1, blocked.stdout)
                self.assertIn("Do not edit a rendered candidate", blocked.stderr)
                self.assertEqual(snapshot_hash(candidate), original_snapshot)

        prepared = prepare(source, [], self.work / "writing")
        self.assertEqual(len(prepared["shots"]), 1)
