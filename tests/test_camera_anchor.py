"""Anchor measurement fixtures are synthetic and remain outside the audit."""
import subprocess
import unittest
from pathlib import Path

from . import test_prepare
from homeku.authoring import prepare
from homeku.camera_anchor import measure_anchor
from homeku.common import LibraryError
from homeku.motion_analysis import require_backend


class CameraAnchorTests(test_prepare.VideoFixture, unittest.TestCase):
    def test_native_manual_enlarging_and_shrinking(self):
        prepared = prepare(self.video("anchor"), [], self.work / "writing")
        session = Path(prepared["session"])
        original = session.read_bytes()
        small, large = (5, 5, 25, 5), (5, 5, 55, 5)
        enlarged = measure_anchor(session, "shot-01", (0, 10), small, large, self.work / "measurements")
        self.assertEqual(enlarged["direction"], "enlarging")
        self.assertEqual(enlarged["estimate"], "~2.5×")
        self.assertEqual([row["pts_s"] for row in enlarged["frames"]], [0, 1])
        self.assertEqual([row["length_px"] for row in enlarged["frames"]], [20, 50])
        paths = [enlarged["measurement"], *(row["preview"] for row in enlarged["frames"])]
        saved = {Path(path): Path(path).read_bytes() for path in paths}
        shrunk = measure_anchor(session, "shot-01", (0, 10), large, small, self.work / "measurements")
        self.assertEqual(shrunk["direction"], "shrinking")
        self.assertEqual(shrunk["ratio"], 2.5)
        self.assertTrue(Path(shrunk["measurement"]).is_file())
        other_paths = [shrunk["measurement"], *(row["preview"] for row in shrunk["frames"])]
        self.assertTrue(set(paths).isdisjoint(other_paths))
        for path, content in saved.items():
            self.assertEqual(path.read_bytes(), content)
        self.assertEqual(session.read_bytes(), original)

    def test_invalid_points_and_cross_shot(self):
        prepared = prepare(self.video("split"), [6], self.work / "writing")
        session = Path(prepared["session"])
        valid = (5, 5, 25, 5)
        for frames, points, message in (
            ((0, 6), valid, "same shot"),
            ((2, 1), valid, "chronological"),
            ((0, 5), (5, 5, 5, 5), "positive length"),
            ((0, 5), (-1, 5, 25, 5), "outside native frame"),
        ):
            with self.subTest(frames=frames, points=points), self.assertRaisesRegex(LibraryError, message):
                measure_anchor(session, "shot-01", frames, points, valid, self.work / "measurements")

    def test_opencv_proposes_shift_and_leaves_viewed_unchanged(self):
        cv, np = require_backend()
        source = self.work / "tracking.mp4"
        pattern = np.random.default_rng(17).integers(0, 256, (160, 96), dtype=np.uint8)
        pattern = cv.GaussianBlur(pattern, (5, 5), 1)
        for i in range(8):
            transform = np.array([[1, 0, 2 * i], [0, 1, i]], dtype=np.float32)
            cv.imwrite(str(self.work / f"frame-{i:02d}.png"), cv.warpAffine(pattern, transform, (96, 160)))
        subprocess.run(["ffmpeg", "-v", "error", "-framerate", "10", "-i", str(self.work / "frame-%02d.png"),
                        "-c:v", "mpeg4", "-q:v", "2", "-threads", "1", str(source)], check=True)
        prepared = prepare(source, [], self.work / "writing")
        session = Path(prepared["session"])
        original = session.read_bytes()
        result = measure_anchor(session, "shot-01", (0, 4), (30, 55, 55, 80), None, self.work / "measures")
        self.assertEqual(result["status"], "proposed", result.get("reason"))
        self.assertNotIn("estimate", result)
        for observed, expected in zip(result["frames"][-1]["points_px"], ((38, 59), (63, 84)), strict=True):
            for coordinate, reference in zip(observed, expected, strict=True):
                self.assertAlmostEqual(coordinate, reference, delta=.6)
        self.assertTrue(Path(result["frames"][-1]["preview"]).is_file())
        proposal = Path(result["measurement"])
        original_proposal = proposal.read_bytes()
        end_points = [coordinate for point in result["frames"][-1]["points_px"] for coordinate in point]
        confirmed = measure_anchor(session, "shot-01", (0, 4), (30, 55, 55, 80), end_points, self.work / "measures")
        self.assertEqual(confirmed["status"], "measured")
        self.assertNotEqual(confirmed["measurement"], str(proposal))
        self.assertEqual(proposal.read_bytes(), original_proposal)
        self.assertEqual(session.read_bytes(), original)

    def test_textureless_tracking_accepts_manual_correction(self):
        source = self.work / "textureless.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "color=white:size=96x160:rate=10",
                        "-t", "0.6", "-c:v", "mpeg4", "-threads", "1", str(source)], check=True)
        prepared = prepare(source, [], self.work / "writing")
        session = Path(prepared["session"])
        original = session.read_bytes()
        points = (25, 30, 55, 60)
        proposed = measure_anchor(session, "shot-01", (0, 4), points, None, self.work / "measures")
        self.assertEqual(proposed["status"], "insufficient")
        self.assertIsNone(proposed["frames"][-1]["points_px"])
        manual = measure_anchor(session, "shot-01", (0, 4), points, points, self.work / "measures")
        self.assertEqual(manual["status"], "measured")
        self.assertEqual(session.read_bytes(), original)
