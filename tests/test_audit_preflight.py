"""Preflight exercises compact working files with native video metadata."""
import json
from pathlib import Path
from unittest.mock import patch
import unittest
from . import test_prepare
from homeku.audit_session import mark_viewed
from homeku.authoring import complete, prepare
from homeku.common import read_json, sha256
from homeku.preflight import check_inputs
from homeku.video import frame_times, probe_video


def normal():
    return read_json(Path(__file__).resolve().parents[1] / "audit/examples/normal/audit.json")


class PreflightTests(test_prepare.VideoFixture, unittest.TestCase):
    def test_independent_bad_structure_precedes_probe(self):
        audit = normal()
        del audit["design"]["size"]["floor_area_m2"]
        with patch("homeku.preflight.probe_video") as probe:
            result = check_inputs("missing.mp4", audit, {})
        self.assertFalse(result["ok"])
        self.assertIsNone(result["context"])
        self.assertIn("/audit/design/size/floor_area_m2", {e["path"] for e in result["errors"]})
        self.assertIn("/audit-info/method", {e["path"] for e in result["errors"]})
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
        complete(work["audit"], session_path=work["session"])
        result = check_inputs(source, audit, read_json(Path(work["audit_info"])))
        self.assertFalse(result["ok"])
        mark_viewed(work["session"], all_frames=True, all_passes=True)
        complete(work["audit"], session_path=work["session"])
        with (patch("homeku.preflight.probe_video", wraps=probe_video) as probe,
              patch("homeku.preflight.frame_times", wraps=frame_times) as pts,
              patch("homeku.preflight.sha256", wraps=sha256) as digest):
            result = check_inputs(source, read_json(Path(work["audit"])),
                                  read_json(Path(work["audit_info"])))
        self.assertTrue(result["ok"], result["errors"])
        probe.assert_called_once()
        pts.assert_called_once()
        digest.assert_called_once_with(source)
        self.assertEqual(result["context"]["sha256"], sha256(source))
        self.assertEqual(result["context"]["times"], frame_times(source))
