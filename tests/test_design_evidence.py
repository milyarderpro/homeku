"""Regression checks for scope, source tracing, spatial uncertainty and temporal evidence."""
import copy
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

from PIL import Image
from jsonschema import ValidationError
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import design_evidence as evidence
from knowledge_library import load_release, read_archives, resolve_pointer, validate_contract
import sample_temporal_evidence as sampler
from verify_source_integrity import sha256_file
from video_similarity import matched_frames


class EvidenceBehaviorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.release = load_release(ROOT)
        cls.sources = {s["reference_id"]: s for s in cls.release["references"]}
        cls.refs = read_archives(ROOT)
        cls.visual = evidence.load_review_notes(ROOT, "visual-notes.json", cls.sources)
        cls.temporal = evidence.load_review_notes(ROOT, "temporal-notes.json", cls.sources)
        cls.outputs, cls.coverage = evidence.build_outputs(ROOT)
        cls.packages = {ident: json.loads(cls.outputs[f"knowledge/design-evidence/{ident}.json"])
                        for ident in cls.sources}

    def test_explicit_relation_does_not_invent_world_orientation(self):
        relation = evidence.relation_from_tag("coffee_table_in_front_of_sofa")
        self.assertEqual(relation["predicate"], "in_front_of")
        self.assertEqual(relation["object_mention"], "sofa")
        self.assertEqual(relation["coordinate_system"], "camera_view_relative")
        self.assertIsNone(relation["world_orientation"])

    def test_ambiguous_or_negated_relations_are_not_positive_edges(self):
        for value in ("sofa_or_bench_facing_window", "possibly_table_beside_sofa",
                      "no_window_above_sink", "plant_not_visible_behind_curtain"):
            self.assertIsNone(evidence.relation_from_tag(value))
        relation = evidence.relation_from_tag("table_between_sofa_and_cabinet")
        self.assertEqual(relation["object_mention"], "sofa_and_cabinet")

    def test_material_facing_and_lighting_modifiers_are_not_orientation_edges(self):
        for value in ("rough_pale_stone_facing_on_main_front_facade",
                      "front_facing_gable_and_intersecting_roofs",
                      "warm_under_cabinet_backsplash_lighting",
                      "integrated_under_counter_refrigerator"):
            self.assertIsNone(evidence.relation_from_tag(value))
        relation = evidence.relation_from_tag("pale_stone_facing_beneath_lower_window_sections")
        self.assertEqual(relation["subject_mention"], "pale_stone_facing")
        self.assertEqual(relation["predicate"], "below")
        self.assertEqual(relation["object_mention"], "lower_window_sections")

    def test_scene_transition_never_becomes_shared_room(self):
        self.assertEqual(evidence.co_visible_functions({
            "scene": "exterior_to_living_kitchen",
            "visible_details": {"architectural": ["open_plan_room"]}}), [])
        self.assertEqual(evidence.co_visible_functions({
            "scene": "living_kitchen", "visible_details": {"architectural": []}}), [])
        self.assertEqual(evidence.co_visible_functions({
            "scene": "open_plan_living_kitchen_and_sleeping_loft"}), ["living", "kitchen", "sleeping_loft"])

    def test_all_records_resolve_to_their_real_saved_values(self):
        for ident, package in self.packages.items():
            doc = self.refs[ident]
            ids = []
            for row in package["observations"] + package["relations"]:
                self.assertEqual(row["source"], self.sources[ident])
                ids.append(row["id"])
                actual = resolve_pointer(doc, row["field_path"])
                if row.get("basis") in ("recorded_annotation", "recorded_annotation_literal_relation"):
                    self.assertEqual(row["raw"], actual)
            self.assertEqual(len(ids), len(set(ids)), ident)
            for shot in package["shots"]:
                for entity in shot["entities"]:
                    self.assertEqual(entity["source_mention"], resolve_pointer(doc, entity["field_path"]))

    def test_edit_sequence_and_object_identity_are_unknown(self):
        for package in self.packages.values():
            for edge in package["sequence_links"]:
                self.assertEqual(edge["physical_room_adjacency"], "unknown")
            for shot in package["shots"]:
                self.assertEqual(shot["subject_motion"]["state"], "unknown")
                for entity in shot["entities"]:
                    self.assertEqual(entity["physical_identity_across_shots"], "unknown")

    def test_saved_samples_do_not_create_a_review_event(self):
        ident = next(i for i in self.packages if i not in self.temporal["references"])
        package = self.packages[ident]
        self.assertTrue(all(s["temporal_samples"] for s in package["shots"]))
        self.assertEqual(package["review_coverage"]["temporal"], "pending")
        self.assertTrue(all(s["temporal_visual_review"]["state"] == "pending" for s in package["shots"]))
        self.assertFalse(any("temporal" in r["id"] for r in package["reviews"]))

    def test_new_reference_without_notes_remains_pending(self):
        source = copy.deepcopy(self.sources["edh060"])
        source["reference_id"] = "unreviewed"
        source["analysis_path"] = "references/unreviewed/analysis.yaml"
        source["source_path"] = "video/unreviewed.mp4"
        doc = copy.deepcopy(self.refs["edh060"])
        doc["video"].update(id="unreviewed", filename="unreviewed.mp4")
        package = evidence.build_reference(ROOT, source, doc, {"references": {}}, {"references": {}})
        self.assertEqual(package["reviews"], [])
        self.assertEqual(package["review_coverage"]["storyboard"], "pending")
        self.assertEqual(package["review_coverage"]["temporal"], "pending")
        self.assertTrue(all(s["temporal_samples"] is None for s in package["shots"]))
        rendered = evidence.render_reference(package, "fixture")
        self.assertIn("No new visual review", rendered)
        self.assertNotIn("AI reviewed selected storyboard", rendered)

    def test_stale_review_annotation_or_media_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "knowledge/reviews").mkdir(parents=True)
            source = self.sources["edh060"]
            data = {"reviewed_on": "2026-11-17", "references": {
                "edh060": {"source": {**source, "analysis_sha256": "f" * 64}, "evidence": []}}}
            path = root / "knowledge/reviews/fixture.json"
            path.write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError, "Stale AI review"):
                evidence.load_review_notes(root, "fixture.json", self.sources)
            data["references"]["edh060"]["source"] = source
            data["references"]["edh060"]["evidence"] = [{"path": "missing.jpg", "sha256": "0" * 64}]
            path.write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError, "missing evidence"):
                evidence.load_review_notes(root, "fixture.json", self.sources)

    def test_temporal_out_of_range_or_changed_asset_rejected(self):
        ident = "edh060"
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            target = root / "knowledge/temporal" / ident
            shutil.copytree(ROOT / "knowledge/temporal" / ident, target)
            path = target / "index.json"
            data = json.loads(path.read_text())
            data["shots"][0]["frames"][0]["timestamp_s"] = -1
            path.write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError, "outside shot"):
                evidence.validate_temporal(root, self.sources[ident], self.refs[ident])
            shutil.copy2(ROOT / "knowledge/temporal" / ident / "index.json", path)
            (target / "shot-01-start.jpg").write_bytes(b"corrupt")
            with self.assertRaisesRegex(ValueError, "missing evidence"):
                evidence.validate_temporal(root, self.sources[ident], self.refs[ident])

    def test_metadata_alias_difference_is_not_silently_corrected(self):
        package = self.packages["edh060"]
        expected = [(n, s["scene"]) for n, s in enumerate(self.refs["edh060"]["shots"])
                    if self.refs["edh060"]["video_structure"]["scene_sequence"][n] != s["scene"]]
        self.assertEqual(len(package["annotation_discrepancies"]), len(expected))
        self.assertEqual(self.refs["edh060"]["shots"][1]["scene"], "living_room_kitchen_and_sleeping_loft")
        self.assertTrue(all(r["status"] == "ambiguous" for r in package["annotation_discrepancies"]))

    def test_aggregate_counts_distinct_references_and_lists_exceptions(self):
        rows = evidence.aggregate_records(self.release, self.refs, self.packages)
        ids = set(self.refs)
        for row in rows:
            self.assertEqual(row["numerator"], len(set(row["reference_ids"])))
            self.assertEqual(row["denominator"], len(ids))
            self.assertEqual(set(row["reference_ids"]) | set(row["exceptions"]), ids)
            self.assertFalse(set(row["reference_ids"]) & set(row["exceptions"]))
        clone = copy.deepcopy(self.packages)
        first = next(iter(clone))
        clone[first]["shots"] *= 3
        self.assertEqual(rows, evidence.aggregate_records(self.release, self.refs, clone))

    def test_schema_rejects_asserted_world_geometry(self):
        package = copy.deepcopy(self.packages["edh060"])
        package["relations"][0]["world_orientation"] = "north"
        with self.assertRaises(ValidationError):
            validate_contract("design_evidence", package)
        package = copy.deepcopy(self.packages["edh060"])
        package["sequence_links"][0]["physical_room_adjacency"] = "adjacent"
        with self.assertRaises(ValidationError):
            validate_contract("design_evidence", package)

    def test_generated_evidence_is_reproducible_and_published_only(self):
        self.assertEqual(set(self.packages), set(self.sources))
        self.assertEqual(self.coverage["counts"]["shots"], self.release["shot_count"])
        for relative, content in self.outputs.items():
            self.assertEqual((ROOT / relative).read_text(), content, relative)

    def test_evaluation_bank_fixed_and_unscored_cases_are_honest(self):
        bank_path = ROOT / "evaluations/stage3/cases.json"
        bank = json.loads(bank_path.read_text())
        baseline = json.loads((bank_path.parent / "baseline.json").read_text())
        self.assertEqual(sha256_file(bank_path), baseline["question_bank_sha256"])
        self.assertEqual(set(x["split"] for x in bank["cases"]), {"development", "heldout"})
        self.assertTrue(set(bank["pilot_reference_ids"]) <= set(self.sources))
        self.assertIsNone(baseline["consumer_model_accuracy"])
        self.assertEqual(sum(x["passed"] is None for x in baseline["cases"]),
                         baseline["unscored_reference_answers"])


class TemporalSamplingTests(unittest.TestCase):
    def test_samples_are_clamped_inside_shorter_decoded_stream(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = {"reference_id": "fixture", "source_path": "video/fixture.mp4"}
            doc = {"shots": [{"id": "shot-01", "start_s": 0, "end_s": 2.01}]}
            def extract(video, timestamp, target):
                target.parent.mkdir(parents=True, exist_ok=True)
                Image.new("RGB", (32, 48), (round(timestamp * 50), 70, 80)).save(target)
            with patch.object(sampler, "video_duration", return_value=2), patch.object(sampler, "extract_frame", side_effect=extract):
                data = sampler.sample_reference(root, source, doc)
                shot = data["shots"][0]
                self.assertEqual(shot["annotation_end_s"], 2.01)
                self.assertEqual(shot["sample_end_limit_s"], 2)
                self.assertEqual([f["timestamp_s"] for f in shot["frames"]], [0.12, 1.0, 1.88])
                self.assertEqual(sampler.sample_reference(root, source, doc), data)
                (root / data["contact_path"]).write_bytes(b"corrupt")
                with self.assertRaisesRegex(ValueError, "changed"):
                    sampler.sample_reference(root, source, doc)

    def test_low_contrast_and_one_reused_frame_cannot_trigger_duplicate(self):
        frame = lambda path, bits="1234567890abcdef", contrast=40: {
            "path": path, "dhash": bits, "contrast": contrast}
        self.assertEqual(matched_frames([frame("a", contrast=0)], [frame("b", contrast=0)]), [])
        self.assertEqual(len(matched_frames([frame("a"), frame("b")], [frame("c")])), 1)

    def test_perceptual_matching_survives_jpeg_recompression(self):
        with tempfile.TemporaryDirectory() as folder:
            rows = []
            for n, filename in enumerate(("shot-01-start.jpg", "shot-02-start.jpg")):
                source = ROOT / "knowledge/temporal/edh060" / filename
                target = Path(folder) / filename
                with Image.open(source) as image:
                    image.save(target, quality=30)
                a, ca = sampler.dhash(source)
                b, cb = sampler.dhash(target)
                rows.append(({"path": f"original-{n}", "dhash": a, "contrast": ca},
                             {"path": f"reencoded-{n}", "dhash": b, "contrast": cb}))
            self.assertEqual(len(matched_frames([r[0] for r in rows], [r[1] for r in rows])), 2)


if __name__ == "__main__":
    unittest.main()
