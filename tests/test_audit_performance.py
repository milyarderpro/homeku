"""Phase and command timing are independent, including on interrupted runs."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.homeku.audit_performance import event, mark_phase, summarize, timed
from tools.homeku.common import LibraryError


class AuditPerformanceTests(unittest.TestCase):
    def setUp(self):
        work = tempfile.TemporaryDirectory()
        self.addCleanup(work.cleanup)
        self.log = Path(work.name) / "session" / "performance.jsonl"

    def test_phase_duration_and_open_phase(self):
        times = ["2026-11-26T00:00:00+00:00", "2026-11-26T00:00:08+00:00"]
        with patch("tools.homeku.audit_performance._timestamp", side_effect=times):
            mark_phase(self.log, "shot-mapping", "start")
            with self.assertRaisesRegex(LibraryError, "already started"):
                mark_phase(self.log, "shot-mapping", "start")
            mark_phase(self.log, "shot-mapping", "finish")
        mark_phase(self.log, "camera", "start")
        phases = summarize(self.log)["phases"]
        self.assertEqual(phases["shot-mapping"][0]["seconds"], 8)
        self.assertEqual(phases["camera"][0]["state"], "incomplete")
        self.assertNotIn("seconds", phases["camera"][0])

    def test_drive_delivery_resumes_independently_of_export(self):
        mark_phase(self.log, "validation-export", "start")
        mark_phase(self.log, "validation-export", "finish")
        mark_phase(self.log, "drive-delivery", "start")
        phases = summarize(self.log)["phases"]
        self.assertEqual(phases["validation-export"][0]["state"], "complete")
        self.assertEqual(phases["drive-delivery"][0]["state"], "incomplete")
        mark_phase(self.log, "drive-delivery", "finish")
        self.assertEqual(summarize(self.log)["phases"]["drive-delivery"][0]["state"], "complete")

    def test_distinct_attempts_success_failure_and_interruption(self):
        event(self.log, "draft", state="started")
        event(self.log, "draft", state="complete", seconds=1)
        with self.assertRaisesRegex(LibraryError, "preflight"):
            with timed(self.log, "draft"):
                raise LibraryError("preflight")
        with timed(self.log, "draft") as outcome:
            outcome["snapshot_sha256"] = "a" * 64
        with self.assertRaises(KeyboardInterrupt):
            with timed(self.log, "draft"):
                raise KeyboardInterrupt
        summary = summarize(self.log)
        self.assertEqual(summary["untracked_events"], 2)
        draft = summary["commands"]["draft"]
        self.assertEqual(draft["attempts"], 3)
        failed, successful, interrupted = draft["runs"]
        self.assertEqual(failed["error"], "preflight")
        self.assertEqual(successful["snapshot_sha256"], "a" * 64)
        self.assertEqual(interrupted["state"], "incomplete")
        self.assertEqual(len({row["attempt_id"] for row in draft["runs"]}), 3)
