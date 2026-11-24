"""Checks for viewed declarations and source-bound workspaces."""
import unittest
from pathlib import Path
from . import test_prepare
from homeku.audit_session import add_pass, mark_viewed, workspace
from homeku.authoring import prepare
from homeku.common import LibraryError, dumps, read_json


class AuthoringTests(test_prepare.VideoFixture, unittest.TestCase):
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
