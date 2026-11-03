"""Self-contained validation fixtures; no GitHub writes."""
import sys
import tempfile
import unittest
from pathlib import Path

import yaml
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_analysis import InvalidPackage, validate, validate_narratives


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

    def set_regions(self, regions):
        path = self.folder / "analysis.yaml"
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        data["architecture"]["common_regions"] = regions
        path.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")
        if isinstance(regions, list) and all(isinstance(item, str) for item in regions):
            label = ", ".join(item.replace("_", " ") for item in regions) or "Tidak diketahui"
        else:
            label = "Tidak diketahui"
        md_path = self.folder / "analysis.md"
        md_path.write_text(md_path.read_text(encoding="utf-8") +
                           f"| Wilayah terkait gaya desain | {label} |\n", encoding="utf-8")

    def test_valid(self):
        # Historical schema 2.1 packages without common_regions remain valid.
        self.assertEqual(validate(self.folder)["shot_count"], 2)

    def test_multiple_common_regions(self):
        self.set_regions(["north_america", "europe"])
        self.assertEqual(validate(self.folder)["shot_count"], 2)

    def test_empty_common_regions(self):
        self.set_regions([])
        self.assertEqual(validate(self.folder)["shot_count"], 2)

    def test_invalid_region_value(self):
        self.set_regions(["antarctica"])
        with self.assertRaisesRegex(InvalidPackage, "Invalid architecture.common_regions"):
            validate(self.folder)

    def test_duplicate_regions(self):
        self.set_regions(["europe", "europe"])
        with self.assertRaisesRegex(InvalidPackage, "Duplicate architecture.common_regions"):
            validate(self.folder)

    def test_common_regions_must_be_list(self):
        self.set_regions("europe")
        with self.assertRaisesRegex(InvalidPackage, "architecture.common_regions must be a list"):
            validate(self.folder)

    def test_region_markdown_parity(self):
        self.set_regions(["europe"])
        path = self.folder / "analysis.md"
        path.write_text(path.read_text(encoding="utf-8").replace(
            "| Wilayah terkait gaya desain | europe |",
            "| Wilayah terkait gaya desain | asia |"), encoding="utf-8")
        with self.assertRaisesRegex(InvalidPackage, "differs from Markdown"):
            validate(self.folder)

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


class NarrativeValidationTests(unittest.TestCase):
    def setUp(self):
        self.data = {
            "shots": [
                {"id": "shot-01", "visible_details": {
                    "architectural": ["tall_black_framed_window", "white_shiplap_walls"],
                    "furniture_and_props": ["cream_fabric_sofa"],
                    "environment": []}},
                {"id": "shot-02", "visible_details": {
                    "architectural": [], "furniture_and_props": [],
                    "environment": ["yellow_leaf_tree_left_of_house"]}},
            ]
        }
        self.narratives = {
            "shot-01": {
                "architectural": {
                    "text": "Jendela tinggi berbingkai hitam dan dinding panel putih.",
                    "covered_indices": [0, 1]},
                "furniture_and_props": {
                    "text": "Sofa berlapis kain krem.", "covered_indices": [0]},
                "environment": {"text": None, "covered_indices": []},
            },
            "shot-02": {
                "architectural": {"text": None, "covered_indices": []},
                "furniture_and_props": {"text": None, "covered_indices": []},
                "environment": {
                    "text": "Pohon berdaun kuning terlihat di kiri rumah.",
                    "covered_indices": [0]},
            },
        }

    def test_valid_complete_coverage(self):
        self.assertIsNone(validate_narratives(self.data, self.narratives))

    def test_invalid_shot_id(self):
        self.narratives["shot-03"] = self.narratives.pop("shot-02")
        with self.assertRaisesRegex(InvalidPackage, "shot IDs"):
            validate_narratives(self.data, self.narratives)

    def test_missing_category(self):
        del self.narratives["shot-01"]["environment"]
        with self.assertRaisesRegex(InvalidPackage, "narrative categories"):
            validate_narratives(self.data, self.narratives)

    def test_extra_category(self):
        self.narratives["shot-01"]["other"] = {"text": None, "covered_indices": []}
        with self.assertRaisesRegex(InvalidPackage, "narrative categories"):
            validate_narratives(self.data, self.narratives)

    def test_missing_source_index(self):
        self.narratives["shot-01"]["architectural"]["covered_indices"] = [0]
        with self.assertRaisesRegex(InvalidPackage, "covered_indices"):
            validate_narratives(self.data, self.narratives)

    def test_duplicate_source_index(self):
        self.narratives["shot-01"]["architectural"]["covered_indices"] = [0, 0]
        with self.assertRaisesRegex(InvalidPackage, "covered_indices"):
            validate_narratives(self.data, self.narratives)

    def test_out_of_range_source_index(self):
        self.narratives["shot-01"]["architectural"]["covered_indices"] = [0, 2]
        with self.assertRaisesRegex(InvalidPackage, "covered_indices"):
            validate_narratives(self.data, self.narratives)

    def test_boolean_is_not_a_source_index(self):
        self.narratives["shot-01"]["furniture_and_props"]["covered_indices"] = [True]
        with self.assertRaisesRegex(InvalidPackage, "covered_indices"):
            validate_narratives(self.data, self.narratives)

    def test_missing_narrative_text(self):
        self.narratives["shot-01"]["architectural"]["text"] = "  "
        with self.assertRaisesRegex(InvalidPackage, "narrative text"):
            validate_narratives(self.data, self.narratives)

    def test_empty_source_must_have_null_text(self):
        self.narratives["shot-01"]["environment"]["text"] = "Pemandangan hutan."
        with self.assertRaisesRegex(InvalidPackage, "must have null text"):
            validate_narratives(self.data, self.narratives)

    def test_non_empty_source_rejects_null(self):
        self.narratives["shot-02"]["environment"]["text"] = None
        with self.assertRaisesRegex(InvalidPackage, "narrative text"):
            validate_narratives(self.data, self.narratives)

    def test_invalid_cell_keys(self):
        self.narratives["shot-01"]["environment"]["extra"] = "not allowed"
        with self.assertRaisesRegex(InvalidPackage, "cell keys"):
            validate_narratives(self.data, self.narratives)

    def test_narrative_size_and_control_character(self):
        self.narratives["shot-01"]["architectural"]["text"] = "A" * 4001
        with self.assertRaisesRegex(InvalidPackage, "narrative text"):
            validate_narratives(self.data, self.narratives)
        self.narratives["shot-01"]["architectural"]["text"] = "Rumah\x00"
        with self.assertRaisesRegex(InvalidPackage, "narrative text"):
            validate_narratives(self.data, self.narratives)


if __name__ == "__main__":
    unittest.main()
