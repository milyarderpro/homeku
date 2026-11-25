"""Selective reads and search over isolated fixture projections."""
import shutil
import unittest
from pathlib import Path
from unittest.mock import patch
from . import test_generation, test_prepare
from homeku.common import LibraryError, dumps, read_json, sha256
from homeku.derivations import frame_map, resolve
from homeku.generation import render
from homeku.reader import read_reference, search

ROOT = Path(__file__).resolve().parents[1]


class ReaderTests(test_prepare.VideoFixture, unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.root = self.work / "repo"
        (self.root / "data").mkdir(parents=True)
        shutil.copyfile(ROOT / "data/taxonomy.json", self.root / "data/taxonomy.json")
        self.models = [test_generation.model(name) for name in ("normal", "multi")]
        self.models[1]["audit"]["design"]["house_type"]["value"] = "Villa"
        self.models[1]["audit"]["design"]["styles"]["influences"] = [
            {"value": "Modern Farmhouse", "state": "observed", "evidence": [0]}]
        self.models[1]["audit"]["shots"][0]["design"][0]["architecture"]["facts"][0]["value"] = "living-only layout"
        alternate = self.models[1]
        alternate["audit"]["shots"][0]["composition"]["production_start"] = {
            "frame_index": 5, "composition_summary": "Kamera serong dari ambang."}
        alternate["manifest"]["frames"] = frame_map(alternate["audit"], test_generation.TIMES)
        registry = {}
        for item in self.models:
            rid = item["id"]
            folder = self.root / "references" / rid
            folder.mkdir(parents=True)
            for filename, key in (("audit.json", "audit"), ("manifest.json", "manifest")):
                (folder / filename).write_text(dumps(item[key]))
            registry[rid] = {"content_sha256": item["content_sha256"], "contract_version": "3.0", "revision": 1,
                             "source_sha256": item["manifest"]["source"]["sha256"],
                             "audit_sha256": sha256(folder / "audit.json"),
                             "manifest_sha256": sha256(folder / "manifest.json"),
                             "analysis_sha256": "0" * 64, "package_sha256": "0" * 64}
        (self.root / "data/registry.json").write_text(dumps({"version": 1, "references": registry}))
        for name, value in render(self.root, {item["id"]: item for item in self.models}).items():
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(value)

    def test_explicit_filters_match_one_continuous_take(self):
        filters = {"style": "farmhouse modern", "style_role": "style-influence", "scale": "kecil",
                   "area": ["dapur"], "configuration": "curved island", "tempo": "fast",
                   "movement": "dolly in", "camera_qualifier": "gentle", "route": ["living room", "dapur"]}
        result = search(self.root, **filters)
        self.assertEqual([row["id"] for row in result["results"]], ["camera-multi"])
        self.assertEqual(search(self.root, configuration="living-only layout", area=["dapur"])["total"], 0)
        self.assertEqual(search(self.root, **{**filters, "route": ["dapur", "living"]})["total"], 0)
        self.assertEqual(search(self.root, **{**filters, "camera_qualifier": "Strong"})["total"], 0)
        self.assertEqual(search(self.root, style="cottage", style_relation="family")["total"], 2)
        self.assertEqual(search(self.root, style="cozy minimalist", style_role="interior-style")["total"], 2)
        self.assertEqual(search(self.root, style="Modern Cottage", include_uncertain=False)["total"], 0)
        self.assertEqual(search(self.root, limit=1)["next_offset"], 1)

    def test_search_house_type_alias_combines_with_other_filters(self):
        filters = {"house_type": "vila", "style": "farmhouse modern", "style_role": "style-influence",
                   "scale": "kecil", "area": ["dapur"]}
        result = search(self.root, **filters)
        self.assertEqual([r["id"] for r in result["results"]], ["camera-multi"])
        self.assertEqual(search(self.root, **filters, include_uncertain=False)["total"], 0)
        self.assertEqual(search(self.root, **{**filters, "house_type": "Tower House"})["total"], 0)
        self.assertEqual(search(self.root, **{**filters, "area": ["bathroom"]})["total"], 0)

    def test_identity_exposes_palette_and_evidence_without_indexing_colors(self):
        rid = "camera-multi"
        identity = read_reference(self.root, rid, part="identity")
        design = identity["design"]
        self.assertEqual(design["house_type"]["value"], "Villa")
        self.assertTrue({"spatial-configuration", "lighting", "atmosphere"} <=
                        {row["aspect"] for row in design["features"]})
        self.assertEqual(design["palette"][0]["hex"], "#F0E8DA")
        for color in design["palette"]:
            self.assertTrue({str(index) for index in color["evidence"]} <= identity["evidence"]["frames"].keys())
        pointer = identity["provenance"]["/reference/design/palette/0"]
        self.assertEqual(pointer, {"document": "audit", "source_pointer": "/design/palette/0"})
        index = read_json(self.root / "data/search-index.json")
        self.assertNotIn("#F0E8DA", dumps(index))

    def test_read_does_not_need_md_media_or_mp4(self):
        rid = "camera-multi"
        result = read_reference(self.root, rid, part="shot", shot="shot-01")
        shot = result["shot"]
        self.assertEqual(len(shot["design"]), 2)
        self.assertEqual(result["evidence"]["frames"]["5"], .5)
        self.assertNotIn(5, {p["frame_index"] for p in result["evidence"]["selections"]})
        path = "/shots/0/composition/production_start"
        for key in ("frame_index", "composition_summary"):
            pointer = result["provenance"]["/reference" + path + "/" + key]
            self.assertEqual(pointer["document"], "audit")
            self.assertEqual(resolve(self.models[1]["audit"], pointer["source_pointer"]),
                             shot["composition"]["production_start"][key])
        self.assertIn("segments", shot["camera"]["tempo"])
        self.assertNotIn("frame_reviews", dumps(result))
        self.assertNotIn("reference", result)
        area = read_reference(self.root, rid, part="area", shot="shot-01", area=shot["area_ids"][-1])
        self.assertEqual(len(area["shot"]["design"]), 1)
        self.assertEqual(area["shot"]["route"], shot["route"])
        self.assertEqual(area["shot"]["camera"], shot["camera"])
        self.assertEqual(read_reference(self.root, rid)["design"]["styles"]["primary"]["value"], "Modern Cottage")
        self.assertEqual(read_reference(self.root, rid, part="full")["reference"]["id"], rid)

    def test_registered_source_json_tampering_is_rejected(self):
        rid = "camera-multi"
        folder = self.root / "references" / rid
        (folder / "audit.json").write_text("{}")
        with self.assertRaisesRegex(LibraryError, "audit.json changed"):
            read_reference(self.root, rid)

    def test_stored_reads_work_without_source_and_check_only_selected_media(self):
        import json
        from homeku.media import build_media
        from homeku.reader import extract_panel, extract_shot_image
        from homeku.render_assets import render_config
        rid = "camera-multi"
        model = self.models[1]
        source = self.video(rid)
        folder = self.root / "references" / rid
        info = model["manifest"]["source"]
        info["sha256"] = sha256(source)
        model["manifest"]["media"] = build_media(folder, model["audit"], source, info,
                                                   render_config(), test_generation.TIMES)
        manifest = folder / "manifest.json"
        manifest.write_text(dumps(model["manifest"]))
        path = self.root / "data/registry.json"
        registry = json.loads(path.read_text())
        registry["references"][rid].update(manifest_sha256=sha256(manifest), source_sha256=info["sha256"])
        path.write_text(dumps(registry))
        for name, value in render(self.root, {m["id"]: m for m in self.models}).items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(value)
        with patch("homeku.video.extract_frame", side_effect=AssertionError("stored reads cannot decode")):
            result = extract_panel(self.root, rid, "s01-panel-01", self.work / "panel.png")
            self.assertEqual(result["source_panel"], "s01-panel-01")
            shot = extract_shot_image(self.root, rid, "shot-01", self.work / "shot.jpg")
            self.assertEqual(shot["source"], "media/shot-01.jpg")
            self.assertEqual((self.work / "shot.jpg").read_bytes(), (folder / shot["source"]).read_bytes())
            board = extract_shot_image(self.root, rid, "shot-01", self.work / "block.png", from_storyboard=True)
            self.assertEqual(board["location"]["path"], "media/storyboard.jpg")
        with self.assertRaisesRegex(LibraryError, "requires canonical MP4"):
            extract_panel(self.root, rid, "F5", self.work / "native.jpg", native=True)
        canonical = self.root / info["path"]
        canonical.parent.mkdir()
        shutil.copyfile(source, canonical)
        from homeku.video import extract_frame
        result = extract_panel(self.root, rid, "F5", self.work / "native.jpg", native=True)
        self.assertEqual((result["frame_index"], result["timestamp_s"]), (5, .5))
        self.assertEqual((self.work / "native.jpg").read_bytes(), extract_frame(canonical, 5))
        (folder / "media/shot-01.jpg").write_bytes(b"changed")
        with self.assertRaisesRegex(LibraryError, "Stored media unavailable or changed"):
            extract_shot_image(self.root, rid, "shot-01", self.work / "invalid.jpg")
        self.assertEqual(read_reference(self.root, rid)["id"], rid)
