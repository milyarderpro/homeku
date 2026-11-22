"""Reader and audit 1.1 regressions; synthetic packages only, no creative benchmark."""
from __future__ import annotations

import copy
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from homeku.common import LibraryError, dumps, read_json, sha256
from homeku.engine import build, check, ingest
from homeku.exporter import assemble, frame_times, sample, selected_indices
from homeku.markdown import component, parse, review_cards
from homeku.validation import CODE_ROOT, validate_folder
from tests.fixtures.factory import copy_fixture, isolated_root, make_folder, modernize, package_folder


class ImprovementTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.shared = tempfile.TemporaryDirectory()
        cls.legacy = make_folder(Path(cls.shared.name) / "legacy", rid="prototype")

    @classmethod
    def tearDownClass(cls):
        cls.shared.cleanup()

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.work = Path(self.temporary.name)
        self.folder = modernize(copy_fixture(self.work / "fixture", "modern", self.legacy))
        self.md = self.folder / "analysis.md"
        self.manifest = read_json(self.folder / "manifest.json")
        self.root = isolated_root(self.work / "repo")

    def tearDown(self):
        self.temporary.cleanup()

    def manifest_change(self, fn):
        fn(self.manifest)
        (self.folder / "manifest.json").write_text(dumps(self.manifest))

    def ingest_fixture(self):
        package = package_folder(self.folder, self.root / "incoming/modern-r0001.zip")
        result = ingest(self.root, [package])
        self.assertEqual(result["results"][0]["status"], "imported", result)
        return read_json(self.root / "data/projections/modern.json")

    def test_folded_md_retains_dna_and_authored_narratives(self):
        _, model, _ = validate_folder(self.folder, self.root)
        self.assertEqual(len(model["profile"]), 16)
        self.assertIn("Interpretasi profil", model["profile_notes"])
        self.assertIn("pelestarian narasi", model["palette_notes"])
        self.assertIn("tanpa klaim adjacency", model["timeline_notes"])
        self.assertIn("serong", model["shots"][0]["composition_notes"])
        self.assertIn("Ritme fixture", model["shots"][0]["camera_notes"])
        self.assertNotIn("<details>", model["profile_notes"])

    def test_profile_does_not_accept_omitted_aspects_or_missing_evidence(self):
        text = self.md.read_text()
        with self.assertRaisesRegex(LibraryError, "all required aspects"):
            parse(text.replace("| dna-06 | roof | unknown | unknown | unknown | - |\n", ""))
        with self.assertRaisesRegex(LibraryError, "needs evidence"):
            parse(text.replace("| american cattage | uncertain | medium | [area](media/shot-01/area-overview.jpg) |",
                               "| american cattage | uncertain | medium | - |"))
        with self.assertRaisesRegex(LibraryError, "Unsupported"):
            parse(text.replace("| format_version | 1.1 |", "| format_version | 8.0 |"))

    def test_profile_evidence_must_link_original_registered_media(self):
        self.md.write_text(self.md.read_text().replace("[area](media/shot-01/area-overview.jpg)", "[board](media/storyboard.jpg)"))
        with self.assertRaisesRegex(LibraryError, "original shot media"):
            validate_folder(self.folder, self.root)

    def test_json_reader_has_all_source_fields_and_resolvable_provenance(self):
        reader = self.ingest_fixture()
        _, original, _ = validate_folder(self.folder, self.root)
        self.assertEqual(reader["reference"], original)
        self.assertNotIn("fingerprint", reader)
        self.assertNotIn("model_sha256", reader)
        self.assertIn("projection_sha256", read_json(self.root / "data/build.json"))
        for pointer, proof in reader["provenance"].items():
            cursor = reader
            for part in pointer.strip("/").split("/"):
                cursor = cursor[int(part)] if isinstance(cursor, list) else cursor[part]
            self.assertTrue(cursor)
            self.assertTrue((self.root / proof["md"].split("#")[0]).is_file())
            for item in proof.get("evidence", []):
                self.assertTrue((self.root / item["path"]).is_file())
                self.assertIn("timestamp_s", item)

    def test_index_normalizes_explicit_aliases_and_preserves_uncertainty(self):
        self.ingest_fixture()
        entry = read_json(self.root / "data/search-index.json")["references"][0]
        style = next(c for c in entry["profile_facets"] if c["aspect"] == "primary-style")
        self.assertEqual((style["value"], style["canonical"], style["state"]), ("american cattage", "american cottage", "uncertain"))
        mass = next(c for c in entry["profile_facets"] if c["aspect"] == "massing")
        self.assertEqual(mass["canonical"], "l-shaped")
        feature = next(c for c in entry["profile_facets"] if c["aspect"] == "distinctive-features")
        self.assertEqual(feature["canonical"], "fixture-feature-new-label")
        self.assertNotIn("design", entry["shots"][0])
        self.assertNotIn("facts", entry["shots"][0])
        self.assertTrue((self.root / entry["json"]).is_file())

    def test_legacy_data_is_not_enriched_from_prose_or_archive(self):
        old = copy_fixture(self.work / "old", "legacy", self.legacy)
        text = (old / "analysis.md").read_text().replace("Contoh sintetis", "american cottage tiny Contoh sintetis")
        (old / "analysis.md").write_text(text)
        package = package_folder(old, self.root / "incoming/legacy-r0001.zip")
        ingest(self.root, [package])
        entry = read_json(self.root / "data/search-index.json")["references"][0]
        self.assertFalse(entry["profile_available"])
        self.assertEqual(entry["profile_facets"], [])

    def test_knowledge_json_retains_nonpositive_claims_and_general_principles_are_separate(self):
        self.ingest_fixture()
        topics = read_json(self.root / "knowledge/topics/index.json")["topics"]
        states = set()
        for topic in topics:
            index = read_json(self.root / topic["json"])
            for page in index["pages"]:
                for row in read_json(self.root / page)["claims"]:
                    states.add(row["fact"]["state"])
                    self.assertTrue((self.root / row["source"].split("#")[0]).is_file())
        self.assertTrue({"observed", "not-visible", "unknown"} <= states)
        self.assertEqual(read_json(self.root / "knowledge/principles.json"), read_json(CODE_ROOT / "sources/design-principles.json"))
        self.assertEqual(build(self.root)["changed"], [])
        self.assertEqual(check(self.root)["status"], "ok")

    def test_incomplete_viewing_or_fabricated_frame_indices_are_rejected(self):
        for field, value, message in (("viewed_frame_indices", [0], "incomplete"),
                                      ("selected_frame_indices", [0, 2, 3, 4, 5], "differ from native")):
            with self.subTest(field=field):
                altered = copy.deepcopy(self.manifest)
                altered["audit"]["frame_reviews"][0][field] = value
                (self.folder / "manifest.json").write_text(dumps(altered))
                with self.assertRaisesRegex(LibraryError, message):
                    validate_folder(self.folder, self.root)

    def test_each_shot_needs_baseline_and_native_claim_must_be_backed(self):
        self.manifest_change(lambda m: m["audit"]["frame_reviews"].pop())
        with self.assertRaisesRegex(LibraryError, "Every shot"):
            validate_folder(self.folder, self.root)
        self.manifest["audit"]["frame_reviews"].append({**self.manifest["audit"]["frame_reviews"][0],
                        "shot_id": "shot-02", "start_s": .6, "end_s": 1.2,
                        "selected_frame_indices": list(range(6,12)), "viewed_frame_indices": list(range(6,12))})
        self.manifest_change(lambda m: m["audit"]["reviewed_ranges"][0].update(mode="frame-by-frame"))
        with self.assertRaisesRegex(LibraryError, "lacks native review"):
            validate_folder(self.folder, self.root)

    def test_baseline_can_be_split_into_bounded_passes_without_gaps(self):
        first = self.manifest["audit"]["frame_reviews"][0]
        self.manifest["audit"]["frame_reviews"] = [
            {**first, "end_s": .3, "selected_frame_indices": [0,1,2], "viewed_frame_indices": [0,1,2]},
            {**first, "start_s": .3, "selected_frame_indices": [3,4,5], "viewed_frame_indices": [3,4,5]},
            self.manifest["audit"]["frame_reviews"][1]]
        (self.folder / "manifest.json").write_text(dumps(self.manifest))
        validate_folder(self.folder, self.root)
        self.manifest["audit"]["frame_reviews"][1].update(start_s=.4, selected_frame_indices=[4,5], viewed_frame_indices=[4,5])
        (self.folder / "manifest.json").write_text(dumps(self.manifest))
        with self.assertRaisesRegex(LibraryError, "gap in shot-01"):
            validate_folder(self.folder, self.root)

    def test_native_deepening_can_overlap_whole_shot_sampling(self):
        record = {**self.manifest["audit"]["frame_reviews"][0], "start_s": .2, "end_s": .4,
                  "mode": "frame-by-frame", "sampling_fps": None, "selected_frame_indices": [2,3],
                  "viewed_frame_indices": [2,3], "reason": "Synthetic ambiguous direction test"}
        self.manifest_change(lambda m: m["audit"]["frame_reviews"].append(record))
        validate_folder(self.folder, self.root)

    def test_default_sampling_and_native_60fps_keep_exact_boundary_frames(self):
        source = self.work / "sixty.mp4"
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i",
                        "testsrc2=size=96x160:rate=60", "-t", "0.3", "-c:v", "mpeg4", "-an", str(source)], check=True)
        times = frame_times(source)
        cut = times[1]
        first = sample(source, self.work / "ten", start=cut, end=.3, shot_id="shot-01")
        native = sample(source, self.work / "native", start=cut, end=.3, native=True)
        indices = [r["frame_index"] for r in first["frames"]]
        self.assertEqual((indices[0], indices[-1]), (1,17))
        self.assertEqual(first["selection"]["sampling_fps"], 10)
        self.assertEqual(first["review_record_template"]["viewed_frame_indices"], [])
        self.assertEqual([r["frame_index"] for r in native["frames"]], list(range(1,18)))
        self.assertIsNone(native["selection"]["sampling_fps"])

    def test_low_fps_and_irregular_timestamps_never_interpolate_or_cross_cut(self):
        times = [0, .125, .25, .375]
        self.assertEqual(selected_indices(times, 0, .5, source_fps=8), [0,1,2,3])
        irregular = [0, .02, .13, .14, .4, .45]
        chosen = selected_indices(irregular, .13, .45, fps=10, source_fps=24)
        self.assertEqual(chosen[0], 2)
        self.assertEqual(chosen[-1], 4)
        self.assertEqual(selected_indices(irregular, .13, .45, native=True), [2,3,4])

    def test_cards_and_export_pin_the_same_md_snapshot_in_portable_kit(self):
        source = self.work / "modern.mp4"
        shutil.copyfile(self.folder / "source.mp4", source)
        info = self.manifest["audit"]
        result = assemble(source, self.md, info, self.work / "candidate", include_source=True,
                          purpose="fixture", reviewed_sha256=sha256(self.md))
        candidate = Path(result["candidate"])
        model = parse(self.md.read_text())
        cards = review_cards(model, sha256(self.md))
        self.assertIn(sha256(self.md), cards)
        for shot in model["shots"]:
            self.assertIn(shot["camera_summary"], cards)
            self.assertIn(shot["review_summary"], cards)
        with zipfile.ZipFile(result["package"]) as package:
            self.assertEqual(package.read("modern/analysis.md"), self.md.read_bytes())
            self.assertFalse(any("motion/" in p or "sampling.json" in p for p in package.namelist()))
        spec = importlib.util.spec_from_file_location("kit", CODE_ROOT / "tools/build_audit_kit.py")
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        kit = self.work / "kit.zip"; kit.write_bytes(module.build_bytes())
        portable = self.work / "chat"
        with zipfile.ZipFile(kit) as archive:
            archive.extractall(portable)
        boot=subprocess.run([sys.executable,str(portable/"homeku_runtime.py"),"--output",str(portable)],capture_output=True,text=True)
        self.assertEqual(boot.returncode,0,boot.stdout+boot.stderr)
        output = self.work / "review.md"
        command = subprocess.run([sys.executable, str(portable / "tools/audit.py"), "review", str(candidate), "--output", str(output)],
                                 cwd=portable, text=True, capture_output=True)
        self.assertEqual(command.returncode, 0, command.stdout + command.stderr)
        self.assertIn(sha256(self.md), output.read_text())

    def test_revision_replaces_dna_index_and_old_json_comparisons(self):
        self.ingest_fixture()
        current = read_json(self.root / "data/registry.json")["references"]["modern"]
        revised = copy_fixture(self.work / "revised", "modern", self.folder, revision=2,
                               supersedes={"revision": 1, "content_sha256": current["content_sha256"]},
                               source_bytes=(self.folder / "source.mp4").read_bytes(), layout="new curved arrangement")
        document = revised / "analysis.md"
        document.write_text(document.read_text().replace("fixture-feature-new-label", "replacement-feature"))
        package = package_folder(revised, self.root / "incoming/modern-r0002.zip")
        outcome = ingest(self.root, [package])
        self.assertEqual(outcome["results"][0]["status"], "imported", outcome)
        index_text = (self.root / "data/search-index.json").read_text()
        self.assertIn("replacement-feature", index_text)
        self.assertNotIn("fixture-feature-new-label", index_text)
        json_knowledge = "".join(p.read_text() for p in (self.root / "knowledge/comparisons").rglob("*.json"))
        self.assertIn("new curved arrangement", json_knowledge)
        self.assertNotIn("raised tub platform", json_knowledge)
        self.assertEqual(check(self.root)["status"], "ok")

    def test_ambiguous_style_alias_is_rejected_and_corrupt_cache_metadata_rebuilds(self):
        self.ingest_fixture()
        (self.root / "data/build.json").write_text("{broken metadata")
        self.assertTrue(build(self.root)["changed"])
        self.assertEqual(check(self.root)["status"], "ok")
        taxonomy = read_json(self.root / "data/taxonomy.json")
        taxonomy["styles"]["different-style"] = ["american cottage"]
        (self.root / "data/taxonomy.json").write_text(dumps(taxonomy))
        with self.assertRaisesRegex(LibraryError, "Ambiguous styles alias"):
            build(self.root)

    def test_camera_spelling_and_unknown_labels_preserve_literal(self):
        self.assertEqual(component("Tilt-Up (~15°)")["movement"], "Tilt Up")
        self.assertEqual(component("Tilt-Up (~15°)")["raw"], "Tilt-Up (~15°)")
        self.assertEqual(component("Crab-Diagonal custom")["movement"], "other")
        self.assertEqual(component("Crab-Diagonal custom")["raw"], "Crab-Diagonal custom")


if __name__ == "__main__":
    unittest.main()
