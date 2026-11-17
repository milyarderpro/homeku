"""Growth, provenance and bilingual vocabulary behavior for stage 1/2."""
import copy
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

import yaml
from jsonschema import ValidationError

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from knowledge_library import (
    Taxonomy, check_library, load_release, normalize_reference, publish_release,
    published_references, read_archives, resolve_pointer, search_examples,
    source_binding, source_terms, validate_contract, write_outputs,
)
from verify_source_integrity import (
    SourceIntegrityError, sha256_file, sync_archive_manifest, verify_sources, write_manifest,
)


class KnowledgeGrowthTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "video").mkdir()
        (self.root / "references").mkdir()
        (self.root / "knowledge/taxonomy").mkdir(parents=True)
        shutil.copy2(ROOT / "knowledge/taxonomy/v1.0.1.json",
                     self.root / "knowledge/taxonomy/v1.0.1.json")
        self.template = yaml.safe_load((ROOT / "references/edh060/analysis.yaml").read_text())
        self.add_reference("sample1")
        write_manifest(self.root)
        publish_release(self.root, "fixture-1", "2026-11-17")

    def add_reference(self, ident):
        doc = copy.deepcopy(self.template)
        doc["video"].update(id=ident, filename=ident + ".mp4")
        folder = self.root / "references" / ident
        folder.mkdir()
        (folder / "analysis.yaml").write_text(yaml.safe_dump(doc, sort_keys=False))
        (self.root / "video" / (ident + ".mp4")).write_bytes(
            ("synthetic source fixture " + ident).encode())
        return folder / "analysis.yaml"

    def test_archive_growth_does_not_publish_or_break_current_knowledge(self):
        frozen = (self.root / "knowledge/release.json").read_bytes()
        self.add_reference("sample2")
        self.add_reference("sample3")
        self.assertEqual(verify_sources(self.root, allow_additions=True)["reference_count"], 3)
        sync_archive_manifest(self.root)
        self.assertEqual(len(read_archives(self.root)), 3)
        self.assertEqual(set(published_references(self.root)), {"sample1"})
        self.assertEqual(check_library(self.root)["reference_count"], 1)
        self.assertEqual((self.root / "knowledge/release.json").read_bytes(), frozen)
        publish_release(self.root, "fixture-2", "2026-11-17")
        self.assertEqual(check_library(self.root)["reference_count"], 3)
        self.assertEqual(json.loads((self.root / "knowledge/releases/fixture-1.json").read_text())["reference_count"], 1)

    def test_annotation_correction_requires_explicit_release(self):
        path = self.root / "references/sample1/analysis.yaml"
        doc = yaml.safe_load(path.read_text())
        doc["architecture"]["primary_style"] = "tropical_bungalow"
        path.write_text(yaml.safe_dump(doc))
        with self.assertRaisesRegex(SourceIntegrityError, "Pinned archive changed"):
            sync_archive_manifest(self.root)
        write_manifest(self.root)  # Explicitly reviewed correction.
        with self.assertRaisesRegex(ValueError, "annotation changed"):
            load_release(self.root)
        publish_release(self.root, "fixture-corrected", "2026-11-17")
        self.assertIn("tropical_bungalow",
                      (self.root / "knowledge/reference-profiles/sample1.md").read_text())

    def test_missing_published_source_is_not_silently_dropped(self):
        (self.root / "video/sample1.mp4").unlink()
        with self.assertRaises((FileNotFoundError, ValueError)):
            check_library(self.root)
        with self.assertRaisesRegex(SourceIntegrityError, "Missing source|No source"):
            sync_archive_manifest(self.root)

    def test_release_id_and_taxonomy_are_immutable(self):
        self.add_reference("sample2")
        sync_archive_manifest(self.root)
        with self.assertRaisesRegex(ValueError, "immutable"):
            publish_release(self.root, "fixture-1", "2026-11-17")
        path = self.root / "knowledge/taxonomy/v1.0.1.json"
        value = json.loads(path.read_text())
        value["notes"].append("edited without version bump")
        path.write_text(json.dumps(value))
        with self.assertRaisesRegex(ValueError, "taxonomy changed"):
            load_release(self.root)
        with self.assertRaisesRegex(ValueError, "taxonomy is immutable"):
            publish_release(self.root, "fixture-3", "2026-11-17")

    def test_rebuild_preserves_unmanaged_notes(self):
        note = self.root / "knowledge/reference-profiles/editorial-notes.md"
        note.write_text("User notes outside the generated source profiles.")
        extra = self.root / "knowledge/enrichment/notes.json"
        extra.write_text('{"note": "unmanaged"}')
        write_outputs(self.root, load_release(self.root))
        self.assertTrue(note.is_file())
        self.assertEqual(extra.read_text(), '{"note": "unmanaged"}')
        check_library(self.root)

    def test_mapping_tampering_is_detected(self):
        path = self.root / "knowledge/enrichment/sample1.json"
        value = json.loads(path.read_text())
        value["mappings"][0]["raw"] = "invented source description"
        path.write_text(json.dumps(value))
        with self.assertRaisesRegex(ValueError, "Stale generated"):
            check_library(self.root)

    def test_snapshot_source_identifiers_are_validated(self):
        source = copy.deepcopy(load_release(self.root)["references"][0])
        source["analysis_sha256"] = "invalid"
        with self.assertRaises(ValidationError):
            validate_contract("source", source)

    def test_bilingual_query_returns_same_examples(self):
        self.assertEqual(search_examples("small farmhouse", self.root),
                         search_examples("kecil rumah farmhouse", self.root))
        self.assertEqual(search_examples("small farmhouse", self.root), ["sample1"])
        self.assertEqual(search_examples("invented unmatched style", self.root), [])


class VocabularyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tax = Taxonomy(ROOT / "knowledge/taxonomy/v1.0.1.json")

    def test_open_plan_room_types_and_loft_are_separate(self):
        one = self.tax.map("open_plan_living_room_kitchen", {"room_type", "configuration"})
        two = self.tax.map("open_plan_living_kitchen", {"room_type", "configuration"})
        self.assertEqual(one["matches"], two["matches"])
        ids = {r["concept_id"] for r in one["matches"]}
        self.assertEqual(ids, {"room_type.living_room", "room_type.kitchen", "configuration.open_plan"})
        combined = self.tax.map("living_room_kitchen_and_sleeping_loft", {"room_type", "configuration"})
        self.assertIn("configuration.loft", {r["concept_id"] for r in combined["matches"]})
        self.assertNotIn("configuration.open_plan", {r["concept_id"] for r in combined["matches"]})

    def test_scene_transition_is_not_open_plan(self):
        record = self.tax.map("exterior_front_to_living_room", {"room_type", "configuration"})
        ids = {r["concept_id"] for r in record["matches"]}
        self.assertIn("configuration.transition_between_spaces", ids)
        self.assertNotIn("configuration.open_plan", ids)

    def test_camera_modifier_is_preserved_without_turning_pan_into_tracking(self):
        record = self.tax.map("subtle_pan_right", {"camera"})
        self.assertEqual(record["raw"], "subtle_pan_right")
        self.assertEqual(record["matches"], [{"concept_id": "camera.pan_right", "dimension": "camera"}])
        self.assertEqual(record["qualifiers"], ["subtle"])

    def test_unknown_missing_empty_and_explicit_states_are_distinct(self):
        self.assertEqual(self.tax.map(None, {"opening"})["state"], "unknown")
        self.assertEqual(self.tax.map(None, {"opening"}, presence=False)["state"], "missing")
        self.assertEqual(self.tax.map([], {"opening"})["state"], "empty")
        self.assertEqual(self.tax.map("not_visible", {"opening"})["state"], "not_visible")
        self.assertEqual(self.tax.map("not_applicable", {"opening"})["state"], "not_applicable")

    def test_alternatives_and_negation_do_not_assert_positive_facts(self):
        for value in ("stone_or_tile_appearance", "no_window", "possible_loft"):
            mapped = self.tax.map(value, {"material_appearance", "opening", "configuration"})
            self.assertEqual(mapped["state"], "ambiguous")
            self.assertEqual(mapped["matches"], [])
        self.assertEqual(self.tax.map("unfamiliar_new_label", {"opening"})["state"], "unmapped")

    def test_warm_daylight_is_not_mislabeled_as_a_practical_lamp(self):
        record = self.tax.map("clear_warm_daylight", {"lighting"})
        ids = {m["concept_id"] for m in record["matches"]}
        self.assertIn("lighting.daylight", ids)
        self.assertIn("lighting.warm_tone", ids)
        self.assertNotIn("lighting.warm_practical", ids)

    def test_sleeping_loft_is_not_a_separate_bedroom(self):
        record = self.tax.map("living_room_kitchen_and_sleeping_loft", {"room_type", "configuration"})
        ids = {m["concept_id"] for m in record["matches"]}
        self.assertIn("room_type.sleeping_area", ids)
        self.assertIn("configuration.loft", ids)
        self.assertNotIn("room_type.bedroom", ids)

    def test_field_scope_prevents_style_and_geography_invention(self):
        mapped = self.tax.map("tropical_wooden_window", {"material_appearance", "opening"})
        self.assertNotIn("style_family.tropical", {m["concept_id"] for m in mapped["matches"]})
        self.assertIn("material_appearance.wood", {m["concept_id"] for m in mapped["matches"]})

    def test_every_published_source_value_is_preserved_and_traceable(self):
        release = load_release(ROOT)
        refs = read_archives(ROOT)
        for source in release["references"]:
            stored = json.loads((ROOT / f"knowledge/enrichment/{source['reference_id']}.json").read_text())
            self.assertEqual(stored["source"], source)
            self.assertEqual(len(stored["mappings"]), len(list(source_terms(refs[source["reference_id"]]))))
            for record in stored["mappings"]:
                if record["presence"]:
                    self.assertEqual(resolve_pointer(refs[source["reference_id"]], record["field_path"]), record["raw"])
                for match in record["matches"] + record["candidates"]:
                    self.assertIn(match["concept_id"], self.tax.concepts)

    def test_current_release_build_is_reproducible(self):
        release = check_library(ROOT)
        self.assertEqual(release["reference_count"], len(release["references"]))

    def test_review_contract_does_not_invent_a_review_event(self):
        with self.assertRaises(ValidationError):
            validate_contract("review", {"schema_version": "1.0"})
