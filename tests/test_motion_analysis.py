"""Optional 2D statistics use correct composition and explicit coverage."""
import unittest
from unittest.mock import patch
from PIL import Image
from . import test_prepare
from homeku.common import LibraryError
from homeku.motion_analysis import dependencies, interval, macro_transform, summarize, transform_metrics


class MotionMathTests(unittest.TestCase):
    def test_scale_rotation_and_translation_compose_in_temporal_order(self):
        first = {"status": "ok", "image_size": [100, 80], "matrix": [[2, 0, 10], [0, 2, 5]]}
        second = {"status": "ok", "image_size": [100, 80], "matrix": [[0, -.5, 20], [.5, 0, 3]]}
        combined = macro_transform([first, second])
        self.assertEqual(combined["matrix"], [[0, -1, 17.5], [1, 0, 8]])
        self.assertEqual(combined["scale_2d"], 1)
        self.assertEqual(combined["rotation_degrees_2d"], 90)
        self.assertAlmostEqual(combined["dx_fraction"], -.725)
        self.assertAlmostEqual(combined["dy_fraction"], .225)
        summed = sum(transform_metrics(row["matrix"], row["image_size"])["dx_fraction"]
                     for row in (first, second))
        self.assertNotAlmostEqual(summed, combined["dx_fraction"])

    def test_failed_tracking_breaks_macro_and_pts_trends_preserve_gaps(self):
        valid = {"status": "ok", "image_size": [100, 100], "matrix": [[1, 0, 5], [0, 1, 0]]}
        rows = [{**valid, "start_s": 0, "end_s": .2},
                {"status": "insufficient", "start_s": .2, "end_s": .9},
                {**valid, "start_s": .9, "end_s": 1.2}]
        result = summarize(rows, 0, 1.3)
        self.assertIsNone(result["total"])
        self.assertEqual([(r["start_s"], r["end_s"]) for r in result["ranges"]], [(0, .2), (.9, 1.2)])
        self.assertAlmostEqual(result["coverage"]["valid_duration_s"], .5)
        early, middle, late = result["trends"]
        self.assertAlmostEqual(early["covered_fraction"], .5)
        self.assertEqual(middle["covered_fraction"], 0)
        self.assertIsNone(middle["translation_fraction_per_s"])
        self.assertAlmostEqual(late["covered_fraction"], .75)
        self.assertEqual(len(result["gaps"]), 2)

    def test_zone_rates_are_weighted_by_overlap_across_unequal_intervals(self):
        valid = {"status": "ok", "image_size": [100, 100], "matrix": [[1, 0, 5], [0, 1, 0]]}
        rows = [
            {**valid, "start_s": 0, "end_s": .5, "lower_minus_upper_fraction": .1},
            {**valid, "start_s": .5, "end_s": 2.5, "lower_minus_upper_fraction": -.2},
            {**valid, "start_s": 2.5, "end_s": 3, "lower_minus_upper_fraction": None},
        ]
        early, middle, late = summarize(rows, 0, 3)["trends"]
        for segment, rate, coverage in ((early, .05, 1), (middle, -.1, 1), (late, -.1, .5)):
            with self.subTest(segment=segment["segment"]):
                self.assertAlmostEqual(segment["lower_minus_upper_fraction_per_s"], rate)
                self.assertEqual(segment["zone_coverage_fraction"], coverage)
                self.assertEqual(segment["covered_fraction"], 1)

    def test_zero_zone_difference_counts_as_measured(self):
        valid = {"status": "ok", "image_size": [100, 100], "matrix": [[1, 0, 5], [0, 1, 0]]}
        rows = [
            {**valid, "start_s": 0, "end_s": 1, "lower_minus_upper_fraction": 0},
            {**valid, "start_s": 1, "end_s": 2, "lower_minus_upper_fraction": None},
            {"status": "insufficient", "start_s": 2, "end_s": 3},
        ]
        early, middle, late = summarize(rows, 0, 3)["trends"]
        self.assertEqual(early["lower_minus_upper_fraction_per_s"], 0)
        self.assertEqual(early["zone_coverage_fraction"], 1)
        self.assertEqual(middle["covered_fraction"], 1)
        self.assertEqual(late["covered_fraction"], 0)
        for segment in (middle, late):
            self.assertIsNone(segment["lower_minus_upper_fraction_per_s"])
            self.assertEqual(segment["zone_coverage_fraction"], 0)


class MotionFallbackTests(unittest.TestCase):
    def test_missing_dependency_is_nonfatal(self):
        with Image.new("RGB", (100, 100)) as image, patch(
                "homeku.motion_analysis.dependencies", return_value=None):
            self.assertEqual(interval(image, image, .2)["status"], "unavailable")

    def test_invalid_pts_is_rejected_before_tracking(self):
        with Image.new("RGB", (100, 100)) as image:
            for delta in (0, -1, float("inf"), float("nan")):
                with self.assertRaises(LibraryError):
                    interval(image, image, delta)


class MotionCacheTests(test_prepare.VideoFixture, unittest.TestCase):

    def test_motion_cache_reuses_intervals_without_mutating_audit_or_session(self):
        from pathlib import Path
        from types import SimpleNamespace
        from homeku.authoring import prepare
        from homeku.motion_analysis import motion_hints
        result = prepare(self.video("motion"), [], self.work / "authoring")
        session, audit = Path(result["session"]), Path(result["audit"])
        original = (session.read_bytes(), audit.read_bytes())
        backend = (SimpleNamespace(__version__="test", error=RuntimeError), SimpleNamespace(__version__="test"))

        def tracked(first, second, dt, **_):
            self.assertLessEqual(first.width, 100)
            return {"status": "ok", "image_size": list(first.size), "matrix": [[1, 0, 2], [0, 1, 0]],
                    "lower_minus_upper_fraction": .03 * dt}

        with (patch("homeku.motion_analysis.dependencies", return_value=backend),
              patch("homeku.motion_analysis.interval", side_effect=tracked) as estimator):
            hints = motion_hints(session, "shot-01", max_frames=4, width=100)
            self.assertNotIn("intervals", hints)
            for segment in hints["summary"]["trends"]:
                self.assertAlmostEqual(segment["lower_minus_upper_fraction_per_s"], .03)
                self.assertEqual(segment["zone_coverage_fraction"], 1)
            self.assertFalse(hints["reused"])
            self.assertEqual(estimator.call_count, 3)
            detail = motion_hints(session, "shot-01", max_frames=4, width=100, details=True)
            self.assertTrue(detail["reused"])
            self.assertEqual(len(detail["intervals"]), 3)
            self.assertEqual(detail["summary"], hints["summary"])
            self.assertEqual(estimator.call_count, 3)
            with patch("homeku.motion_analysis.MOTION_CACHE_LIMIT", 0):
                quota = motion_hints(session, "shot-01", max_frames=5, width=100)
                self.assertIn("cache_note", quota)
                self.assertFalse(quota["reused"])
            with self.assertRaisesRegex(LibraryError, "2–64"):
                motion_hints(session, "shot-01", max_frames=1000)
        self.assertEqual((session.read_bytes(), audit.read_bytes()), original)

    def test_missing_dependencies_allow_a_prepared_session_to_continue(self):
        from homeku.authoring import prepare
        from homeku.motion_analysis import motion_hints
        result = prepare(self.video("fallback"), [], self.work / "authoring")
        with patch("homeku.motion_analysis.dependencies", return_value=None):
            hints = motion_hints(result["session"], "shot-01")
        self.assertEqual(hints["status"], "unavailable")


@unittest.skipUnless(dependencies() is not None, "Optional OpenCV/NumPy unavailable")
class RealTrackingTests(unittest.TestCase):
    def test_known_affine_transform_and_native_delta(self):
        cv, np = dependencies()
        values = np.random.default_rng(45).integers(0, 256, (240, 320), dtype=np.uint8)
        converted = cv.warpAffine(values, np.array([[1.02, 0, 4], [0, 1.02, -3]]), (320, 240))
        with Image.fromarray(values) as first, Image.fromarray(converted) as second:
            result = interval(first, second, .4, backend=(cv, np))
        self.assertEqual(result["status"], "ok")
        self.assertGreaterEqual(result["inliers"], 8)
        self.assertAlmostEqual(result["scale_2d"], 1.02, delta=.015)
        self.assertAlmostEqual(result["dx_fraction"], 7.2 / 320, delta=.008)
        self.assertAlmostEqual(result["dx_fraction_per_s"], result["dx_fraction"] / .4)

    def test_textureless_tracking_stays_insufficient(self):
        with Image.new("RGB", (160, 240), "white") as image:
            result = interval(image, image, .2)
        self.assertEqual(result["status"], "insufficient")
