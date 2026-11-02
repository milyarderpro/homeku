"""Self-contained validation fixtures; no GitHub writes."""
import sys
import tempfile
import unittest
from pathlib import Path

import yaml
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_analysis import InvalidPackage, validate


def make_package(root: Path, vid: str = "PENDING") -> Path:
    folder = root / vid
    folder.mkdir()
    data = {
        "schema_version": "2.1",
        "video": {"id": vid, "filename": "test.mp4", "duration_s": 6.0, "shot_count": 2},
        "architecture": {"building_scale": {"perceived_size": "small", "building_form": "rectangular", "vertical_scale": "single_story", "footprint": "compact", "estimated_floor_area_m2": {"min": 30, "max": 50}, "confidence": "low"}},
        "shots": [
            {"id": "shot-01", "start_s": 0.0, "end_s": 3.0, "keyframe": f"references/{vid}/shot-01.jpg"},
            {"id": "shot-02", "start_s": 3.0, "end_s": 6.0, "keyframe": f"references/{vid}/shot-02.jpg"},
        ],
        "analysis_quality": {"status": "draft", "human_verified": False},
    }
    (folder / "analysis.yaml").write_text(yaml.safe_dump(data), encoding="utf-8")
    (folder / "analysis.md").write_text(f"# {vid}\n![Storyboard](storyboard.jpg)\n## Shot 01\n<img src=\"shot-01.jpg\">\n## Shot 02\n<img src=\"shot-02.jpg\">\n", encoding="utf-8")
    for jpg in ("storyboard.jpg", "shot-01.jpg", "shot-02.jpg"):
        Image.new("RGB", (20, 20), (100, 130, 150)).save(folder / jpg, format="JPEG")
    return folder


class ValidateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.folder = make_package(Path(self.tmp.name))

    def tearDown(self):
        self.tmp.cleanup()

    def test_valid(self):
        self.assertEqual(validate(self.folder)["shot_count"], 2)

    def test_missing_jpeg(self):
        (self.folder / "shot-02.jpg").unlink()
        with self.assertRaises(InvalidPackage):
            validate(self.folder)

    def test_bad_count(self):
        path = self.folder / "analysis.yaml"
        y = yaml.safe_load(path.read_text())
        y["video"]["shot_count"] = 3
        path.write_text(yaml.safe_dump(y))
        with self.assertRaises(InvalidPackage):
            validate(self.folder)

    def test_inverted_area(self):
        path = self.folder / "analysis.yaml"
        y = yaml.safe_load(path.read_text())
        y["architecture"]["building_scale"]["estimated_floor_area_m2"] = {"min": 80, "max": 40}
        path.write_text(yaml.safe_dump(y))
        with self.assertRaises(InvalidPackage):
            validate(self.folder)

    def test_bad_timeline(self):
        path = self.folder / "analysis.yaml"
        y = yaml.safe_load(path.read_text())
        y["shots"][1]["start_s"] = 3.8
        path.write_text(yaml.safe_dump(y))
        with self.assertRaises(InvalidPackage):
            validate(self.folder)


if __name__ == "__main__":
    unittest.main()
