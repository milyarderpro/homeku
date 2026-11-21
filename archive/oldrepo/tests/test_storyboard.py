"""Regression tests for reference-style storyboard and column breakpoints."""
from pathlib import Path
import math
import sys
import tempfile
import unittest

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from storyboard import generate_storyboard, MARGIN_X, CARD_W, CARD_H, GAP_X, GAP_Y, HEADER_H, FOOTER


class StoryboardLayoutTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.frames = []
        for i in range(9):
            path = self.root / f"shot-{i+1:02d}.jpg"
            Image.new("RGB", (450, 800), (80 + i * 9, 110, 130)).save(path, format="JPEG")
            self.frames.append(path)
        self.video = {"filename": "dreamsHouse002.mp4", "duration_s": 20.9}
        self.architecture = {"primary_style": "modern_rustic_cottage"}

    def tearDown(self):
        self.tmp.cleanup()

    def render(self, count):
        dest = self.root / f"board-{count}.jpg"
        shots = [{
            "start_s": i * 2,
            "end_s": i * 2 + 2,
            "scene": "very_long_but_still_readable_example_interior_scene_name",
            "camera": {"movements": ["slow_dolly_in", "tracking_to_the_right"]}
        } for i in range(count)]
        generate_storyboard(self.frames[:count], dest, video=self.video,
                            architecture=self.architecture, shots=shots)
        with Image.open(dest) as img:
            self.assertEqual(img.format, "JPEG")
            img.verify()
        with Image.open(dest) as img:
            return img.size

    def test_one_row_for_one_through_five_shots(self):
        for count in range(1, 6):
            with self.subTest(count=count):
                width, height = self.render(count)
                self.assertEqual(width, MARGIN_X * 2 + CARD_W * count + GAP_X * (count - 1))
                self.assertEqual(height, HEADER_H + CARD_H + 88 + FOOTER)

    def test_three_columns_for_six_or_more_shots(self):
        for count in (6, 7, 8, 9):
            with self.subTest(count=count):
                width, height = self.render(count)
                rows = math.ceil(count / 3)
                self.assertEqual(width, MARGIN_X * 2 + CARD_W * 3 + GAP_X * 2)
                self.assertEqual(height, HEADER_H + (rows - 1) * (CARD_H + GAP_Y) + CARD_H + 88 + FOOTER)

    def test_requires_matching_frames_and_shots(self):
        with self.assertRaises(ValueError):
            generate_storyboard([self.frames[0]], self.root / "mismatch.jpg",
                                video=self.video, architecture=self.architecture, shots=[])


if __name__ == "__main__":
    unittest.main()
