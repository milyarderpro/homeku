"""Checks for viewed declarations and source-bound workspaces."""
import copy
import unittest
from pathlib import Path
from . import test_prepare
from homeku.audit_session import add_pass, mark_viewed, workspace
from homeku.authoring import check_camera, complete, prepare, update_shot
from homeku.common import LibraryError, dumps, read_json


class AuthoringTests(test_prepare.VideoFixture, unittest.TestCase):
    def test_camera_checkpoint_is_source_bound_and_idempotent(self):
        source = self.video("camera-checkpoint")
        prepared = prepare(source, [], self.work / "audit")
        session, audit = map(Path, (prepared["session"], prepared["audit"]))
        example = Path(__file__).resolve().parents[1] / "audit/examples/normal/audit.json"
        draft = read_json(audit)
        draft["shots"][0]["camera"] = read_json(example)["shots"][0]["camera"]
        draft["shots"][0]["camera"]["phases"][0]["notation"] = "Dolly-In (~1,3x) + gentle Pan Right (~15°)"
        audit.write_text(dumps(draft))
        mark_viewed(session, all_frames=True, all_passes=True)
        report = check_camera(session)
        self.assertIn("Dolly-In (~1.3×)", report["checked"][0]["camera_movement"])
        saved = session.read_bytes()
        self.assertEqual(check_camera(session), report)
        self.assertEqual(session.read_bytes(), saved)
        draft = read_json(audit)
        draft["shots"][0]["end_s"] = 1.1
        audit.write_text(dumps(draft))
        with self.assertRaisesRegex(LibraryError, "boundaries"):
            check_camera(session)
        state = read_json(session)
        state["format_version"] = "3.0"
        session.write_text(dumps(state))
        with self.assertRaisesRegex(LibraryError, "audit the MP4.*kit 3.1"):
            check_camera(session)
        session.write_bytes(saved)
        self.video(source.stem, rate=5)
        with self.assertRaisesRegex(LibraryError, "Source changed"):
            check_camera(session)

    def test_scoped_camera_recheck_keeps_other_shot_proofs(self):
        source = self.video("camera-correction")
        prepared = prepare(source, [6], self.work / "audit")
        session, audit = map(Path, (prepared["session"], prepared["audit"]))
        example = Path(__file__).resolve().parents[1] / "audit/examples/normal/audit.json"
        working = read_json(audit)
        camera = read_json(example)["shots"][0]["camera"]
        for shot, native in zip(working["shots"], prepared["shots"], strict=True):
            shot["camera"] = copy.deepcopy(camera)
            shot["camera"]["phases"][0].update(start_s=native["start_s"], end_s=native["end_s"],
                                               evidence=[native["first"], native["last"]])
            shot["camera"]["tempo"] = {"label": "moderate", "description": "Tempo sedang."}
        audit.write_text(dumps(working))
        mark_viewed(session, all_frames=True, all_passes=True)
        with self.assertRaisesRegex(LibraryError, "Run check-camera"):
            check_camera(session, shot_id="shot-01")
        check_camera(session)
        old = read_json(session)["camera_check"]["shots"]
        changed = read_json(audit)
        changed["shots"][1]["camera"]["description"] = "Kamera pada shot kedua telah diedit."
        audit.write_text(dumps(changed))
        patch = self.work / "correction.json"
        patch.write_text(dumps({"composition": {"production_start": {
            "frame_index": 1, "composition_summary": "Sudut awal lebih dekat."}}}))
        self.assertTrue(update_shot(session, "shot-01", patch)["camera_recheck_required"])
        with self.assertRaisesRegex(LibraryError, "shot-01/production_start.*shot-02/camera"):
            check_camera(session)
        result = check_camera(session, shot_id="shot-01")
        self.assertEqual([row["shot"] for row in result["checked"]], ["shot-01"])
        revised = read_json(session)["camera_check"]["shots"]
        self.assertNotEqual(revised["shot-01"]["production_start"], old["shot-01"]["production_start"])
        self.assertEqual(revised["shot-01"]["camera"], old["shot-01"]["camera"])
        self.assertEqual(revised["shot-02"], old["shot-02"])
        with self.assertRaisesRegex(LibraryError, "shot-02/camera"):
            complete(audit, session_path=session)
        changed = read_json(audit)
        changed["shots"][0]["end_s"] = .5
        audit.write_text(dumps(changed))
        with self.assertRaisesRegex(LibraryError, "boundaries"):
            check_camera(session, shot_id="shot-01")

    def test_selective_viewing_and_deepening(self):
        source = self.video("declared")
        result = prepare(source, [], self.work / "audit")
        session = Path(result["session"])
        pid = result["passes"][0]["id"]
        with self.assertRaises(LibraryError):
            mark_viewed(session, pid, [999])
        self.assertFalse(mark_viewed(session, pid, [0])["complete"])
        with self.assertRaises(LibraryError):
            add_pass(session, "shot-01", reason=" ")
        additions = add_pass(session, "shot-01", start=.2, end=.5, native=True,
                             reason="Pertanyaan oklusi sintetis.")
        self.assertEqual(additions["passes"][-1]["record"]["viewed_frame_indices"], [])

    def test_resume_recovers_missing_pass_records(self):
        source = self.video("interrupted")
        result = prepare(source, [], self.work / "audit")
        session, audit = map(Path, (result["session"], result["audit"]))
        stored = read_json(session)
        stored["passes"] = []
        session.write_text(dumps(stored))
        before = audit.read_bytes()
        resumed = prepare(source, [], session.parent, resume=True)
        self.assertTrue(resumed["passes"])
        self.assertEqual(resumed["cache"]["canonical_decodes"], 0)
        self.assertEqual(audit.read_bytes(), before)

    def test_invalid_cuts_and_managed_reference_paths_fail(self):
        source = self.video("cuts")
        for cuts in ([True], [0], [12], [5, 4], [4, 4]):
            with self.subTest(cuts=cuts), self.assertRaisesRegex(LibraryError, "Cuts must"):
                prepare(source, cuts, self.work / str(cuts))
        with self.assertRaisesRegex(LibraryError, "separate audit workspace"):
            workspace(Path(__file__).resolve().parents[1] / "references/fixture/audit.json")
