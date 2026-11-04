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

    def test_filename_based_video_id_valid(self):
        folder = self.folder
        target = folder.parent / "dreamsHouse003"
        folder.rename(target)
        self.folder = target
        yml = target / "analysis.yaml"
        data = yaml.safe_load(yml.read_text())
        data["video"]["id"] = "dreamsHouse003"
        data["video"]["filename"] = "dreamsHouse003.mp4"
        for i, shot in enumerate(data["shots"], 1):
            shot["keyframe"] = f"references/dreamsHouse003/shot-{i:02d}.jpg"
        yml.write_text(yaml.safe_dump(data, allow_unicode=True))
        md = target / "analysis.md"
        md.write_text(md.read_text().replace("PENDING", "dreamsHouse003"))
        self.assertEqual(validate(target)["video_id"], "dreamsHouse003")

    def test_filename_based_video_id_must_match_filename(self):
        folder = self.folder
        target = folder.parent / "edh011"
        folder.rename(target)
        self.folder = target
        yml = target / "analysis.yaml"
        data = yaml.safe_load(yml.read_text())
        data["video"]["id"] = "edh011"
        for i, shot in enumerate(data["shots"], 1):
            shot["keyframe"] = f"references/edh011/shot-{i:02d}.jpg"
        yml.write_text(yaml.safe_dump(data, allow_unicode=True))
        with self.assertRaisesRegex(InvalidPackage, "filename stem"):
            validate(target)

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

    def make_rendered_narrative_package(self):
        """Two different scenes; checks structural categories in EACH block."""
        yml = self.folder / "analysis.yaml"
        data = yaml.safe_load(yml.read_text(encoding="utf-8"))
        data["shots"][0]["visible_details"] = {
            "architectural": ["white_wood_siding", "tall_black_framed_windows"],
            "furniture_and_props": ["two_wooden_porch_chairs"],
            "environment": ["yellow_leaf_tree_left_of_house"],
        }
        data["shots"][1]["visible_details"] = {
            "architectural": ["exposed_wood_ceiling_beams"],
            "furniture_and_props": ["cream_sofa_facing_fireplace"],
            "environment": [],
        }
        yml.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")
        narratives = {
            "shot-01": {
                "architectural": {"text": "Fasad papan putih dilengkapi jendela tinggi berbingkai hitam.",
                                  "covered_indices": [0, 1]},
                "furniture_and_props": {"text": "Dua kursi kayu berada di teras.", "covered_indices": [0]},
                "environment": {"text": "Pohon berdaun kuning terlihat di kiri rumah.", "covered_indices": [0]},
            },
            "shot-02": {
                "architectural": {"text": "Balok kayu terlihat di plafon.", "covered_indices": [0]},
                "furniture_and_props": {"text": "Sofa krem menghadap perapian.", "covered_indices": [0]},
                "environment": {"text": None, "covered_indices": []},
            },
        }
        from validate_analysis import narrative_text, NARRATIVE_MARKER
        md = "# PENDING\n\n" + NARRATIVE_MARKER + "\n\n![Storyboard](storyboard.jpg)\n"
        md += "\n## 7. Analisis per Shot\n\n"
        for i, s in enumerate(data["shots"], 1):
            sid = s["id"]
            md += f"### Shot {i:02d} — contoh\n\n"
            md += f'<img src="shot-{i:02d}.jpg">\n\n'
            md += "**Detail yang terlihat**\n\n"
            for category, label in (("architectural", "Arsitektur"),
                                    ("furniture_and_props", "Furnitur dan properti"),
                                    ("environment", "Lingkungan")):
                md += f"**{label}**\n\n"
                md += narrative_text(narratives[sid][category]["text"]) + "\n\n"
            md += "**Catatan pengamatan:** Contoh.\n\n"
        md += "## 8. Kualitas dan Ketidakpastian Analisis\n"
        (self.folder / "analysis.md").write_text(md, encoding="utf-8")
        return narratives

    def test_chat_narrative_valid_per_shot(self):
        narratives = self.make_rendered_narrative_package()
        self.assertEqual(validate(self.folder)["shot_count"], 2)
        self.assertEqual(validate(self.folder, narratives=narratives)["shot_count"], 2)

    def test_missing_category_when_global_count_is_unchanged(self):
        self.make_rendered_narrative_package()
        md_path = self.folder / "analysis.md"
        md = md_path.read_text(encoding="utf-8")
        # Delete one label from the first shot, repeat it in the second:
        # total heading count is still the same, so the old validator passed.
        md = md.replace("**Lingkungan**\n\nPohon berdaun kuning terlihat di kiri rumah.\n\n",
                        "Pohon berdaun kuning terlihat di kiri rumah.\n\n", 1)
        md = md.replace("**Lingkungan**\n\nTidak ada detail yang tercatat.",
                        "**Lingkungan**\n\n**Lingkungan**\n\nTidak ada detail yang tercatat.", 1)
        md_path.write_text(md, encoding="utf-8")
        self.assertEqual(md.count("**Lingkungan**"), 2)
        with self.assertRaisesRegex(InvalidPackage, "Invalid narrative category order"):
            validate(self.folder)

    def test_category_order_in_one_shot_rejected(self):
        self.make_rendered_narrative_package()
        md_path = self.folder / "analysis.md"
        md = md_path.read_text(encoding="utf-8")
        md = md.replace("**Arsitektur**\n\nFasad papan putih",
                        "**Furnitur dan properti**\n\nFasad papan putih", 1)
        md_path.write_text(md, encoding="utf-8")
        with self.assertRaisesRegex(InvalidPackage, "Invalid narrative category order"):
            validate(self.folder)

    def test_missing_paragraph_in_one_shot_rejected(self):
        self.make_rendered_narrative_package()
        md_path = self.folder / "analysis.md"
        md = md_path.read_text(encoding="utf-8").replace(
            "**Arsitektur**\n\nFasad papan putih dilengkapi jendela tinggi berbingkai hitam.",
            "**Arsitektur**\n\n", 1)
        md_path.write_text(md, encoding="utf-8")
        with self.assertRaisesRegex(InvalidPackage, "Invalid narrative category order"):
            validate(self.folder)

    def test_empty_source_cannot_get_invented_description(self):
        self.make_rendered_narrative_package()
        md_path = self.folder / "analysis.md"
        md = md_path.read_text(encoding="utf-8").replace(
            "**Lingkungan**\n\nTidak ada detail yang tercatat.",
            "**Lingkungan**\n\nPegunungan indah terlihat melalui jendela.", 1)
        md_path.write_text(md, encoding="utf-8")
        with self.assertRaisesRegex(InvalidPackage, "Empty source narrative mismatch"):
            validate(self.folder)

    def test_wrong_shot_order_rejected(self):
        self.make_rendered_narrative_package()
        md_path = self.folder / "analysis.md"
        md = md_path.read_text(encoding="utf-8").replace(
            "### Shot 01 — contoh", "### Shot 02 — contoh", 1)
        md_path.write_text(md, encoding="utf-8")
        with self.assertRaisesRegex(InvalidPackage, "Wrong narrative report shot order"):
            validate(self.folder)

    def test_swapped_shot_paragraphs_rejected_against_request(self):
        narratives = self.make_rendered_narrative_package()
        md_path = self.folder / "analysis.md"
        md = md_path.read_text(encoding="utf-8")
        left = "Fasad papan putih dilengkapi jendela tinggi berbingkai hitam."
        right = "Balok kayu terlihat di plafon."
        md = md.replace(left, "TEMP-SWAP", 1).replace(right, left, 1).replace("TEMP-SWAP", right, 1)
        md_path.write_text(md, encoding="utf-8")
        # Shape and category count alone cannot find this; request comparison does.
        self.assertEqual(validate(self.folder)["shot_count"], 2)
        with self.assertRaisesRegex(InvalidPackage, "differs from approved request"):
            validate(self.folder, narratives=narratives)

    def test_missing_marker_for_approved_request_rejected(self):
        narratives = self.make_rendered_narrative_package()
        md_path = self.folder / "analysis.md"
        md = md_path.read_text(encoding="utf-8").replace(
            "<!-- homeku_detail_narratives: chat-reviewed -->", "", 1)
        md_path.write_text(md, encoding="utf-8")
        with self.assertRaisesRegex(InvalidPackage, "Missing approved narrative report marker"):
            validate(self.folder, narratives=narratives)

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
