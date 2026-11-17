"""Reader navigation, changed-source impact and honest remote-evaluation regressions."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from knowledge_access import (audit, dependency_impact, input_fingerprint, local_links,
                              remote_summary, validate_remote_run, visible_reading)


def fixture():
    bank = {"cases": [
        {"id": "Q1", "kind": "source_value", "split": "heldout",
         "reference_id": "fixture", "field_path": "/video/shot_count", "expected": 2},
        {"id": "Q2", "kind": "retrieval", "split": "development", "expected_reference_ids": ["fixture"]},
        {"id": "Q3", "kind": "unknown_source_fact", "split": "heldout"},
        {"id": "Q4", "kind": "creative_boundary", "split": "development"},
    ]}
    commit = "a" * 40
    def event(ident, path, content):
        return {"id": ident, "route": "github_connector", "commit": commit,
                "path": path, "status": "read", "content": content,
                "content_sha256": hashlib.sha256(content.encode()).hexdigest(),
                "characters": len(content)}
    source = event("source", "references/fixture/analysis.yaml", "video:\n  id: fixture\n  shot_count: 2\n")
    source.update(annotation_text=source["content"], content_format="raw_utf8")
    core = event("core", "knowledge/ai-knowledge.md", "Measured plan unknown. A new house may choose natural stone.")
    cite = lambda ident, text: [{"event_id": ident, "excerpt": text}]
    run = {"route": "github_connector", "commit": commit, "release_id": "fixture",
           "independent_model_evaluation": False, "consumer_model_accuracy": None,
           "context_isolation": False, "limitations": ["Prior context; not a blind benchmark."],
           "visual_access": {"status": "unsupported"}, "search_access": {"status": "not_tested"},
           "access_events": [source, core], "responses": [
               {"case_id": "Q1", "status": "answered", "answer": "2 recorded shots.",
                "answer_value": 2, "citations": cite("source", "shot_count: 2")},
               {"case_id": "Q2", "status": "answered", "answer": "fixture", "reference_ids": ["fixture"],
                "citations": cite("source", "id: fixture")},
               {"case_id": "Q3", "status": "answered", "answer": "No measured plan available.",
                "citations": cite("core", "Measured plan unknown.")},
               {"case_id": "Q4", "status": "answered", "answer": "Natural stone may be a new design choice.",
                "citations": cite("core", "A new house may choose natural stone.")},
           ]}
    return bank, run


class ReaderAccessTests(unittest.TestCase):
    def test_current_library_has_one_short_entry_and_all_profiles(self):
        data = audit(ROOT)
        self.assertEqual(data["primary_entry_count"], 1)
        self.assertEqual(data["required_image_fetches_for_core_reading"], 0)
        self.assertEqual(data["published_reference_count"],
                         json.loads((ROOT / "knowledge/release.json").read_text())["reference_count"])
        self.assertLessEqual(data["profile_word_max"], 1200)
        stored = json.loads((ROOT / "evaluations/stage7/local-report.json").read_text())
        self.assertEqual(data, stored)

    def test_maintenance_links_are_rejected_in_primary_reading(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "docs").mkdir()
            (root / "docs/maintenance.md").write_text("Maintain")
            (root / "README.md").write_text("[Required first](docs/maintenance.md)")
            with patch("knowledge_access.load_release", return_value={}):
                with self.assertRaisesRegex(ValueError, "Maintenance promoted"):
                    audit(root)

    def test_secondary_metadata_does_not_become_required_reading(self):
        text = "Start with core.\n<details><summary>Advanced</summary>[Data](technical.json)</details>"
        self.assertEqual(visible_reading(text).strip(), "Start with core.")

    def test_overlong_core_is_detected_before_publication(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "knowledge").mkdir()
            (root / "README.md").write_text("[Core](knowledge/ai-knowledge.md)")
            (root / "knowledge/README.md").write_text("Guide")
            (root / "knowledge/ai-knowledge.md").write_text("word " * 1101)
            with patch("knowledge_access.load_release", return_value={}):
                with self.assertRaisesRegex(ValueError, "word budget"):
                    audit(root)

    def test_input_fingerprint_changes_with_content_not_evaluation_logs(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "knowledge").mkdir()
            (root / "evaluations").mkdir()
            (root / "README.md").write_text("Entry")
            (root / "knowledge/release.json").write_text("{}")
            (root / "knowledge/ai-knowledge.md").write_text("Core one")
            before, _ = input_fingerprint(root)
            (root / "evaluations/log.json").write_text('{"result":"changed"}')
            self.assertEqual(input_fingerprint(root)[0], before)
            (root / "knowledge/ai-knowledge.md").write_text("Core two")
            self.assertNotEqual(input_fingerprint(root)[0], before)

    def test_local_link_cannot_escape_repository(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            with self.assertRaisesRegex(ValueError, "escapes"):
                local_links(root / "README.md", "[Outside](../../outside.md)", root)

    def test_source_change_invalidates_its_dependents_not_all_source_reviews(self):
        release = {"references": [
            {"reference_id": "a", "source_path": "video/a.mp4", "analysis_path": "references/a/analysis.yaml"},
            {"reference_id": "b", "source_path": "video/b.mp4", "analysis_path": "references/b/analysis.yaml"}]}
        result = dependency_impact(["references/a/analysis.yaml"], release)
        self.assertEqual(result["affected_reference_ids"], ["a"])
        self.assertNotIn("b", result["source_specific_dependents"])
        self.assertIn("knowledge/reviews/a.json", result["source_specific_dependents"]["a"])
        self.assertTrue(result["requires_new_source_review"])
        self.assertEqual(dependency_impact(["references/new/analysis.yaml"], release)["affected_reference_ids"], [])

    def test_taxonomy_change_refreshes_mapping_without_faking_new_visual_review(self):
        release = {"references": [{"reference_id": "a", "source_path": "video/a.mp4",
                                   "analysis_path": "references/a/analysis.yaml"}]}
        result = dependency_impact(["knowledge/taxonomy/v2.0.0.json"], release)
        self.assertEqual(result["affected_reference_ids"], ["a"])
        self.assertFalse(result["requires_new_source_review"])
        self.assertNotIn("knowledge/reviews/a.json", result["source_specific_dependents"]["a"])
        mixed = dependency_impact(["knowledge/taxonomy/v2.0.0.json", "references/a/analysis.yaml"], release)
        self.assertTrue(mixed["requires_new_source_review"])
        self.assertIn("knowledge/reviews/a.json", mixed["source_specific_dependents"]["a"])


class RecordedRouteTests(unittest.TestCase):
    def test_retrieval_and_parsed_values_do_not_become_model_accuracy(self):
        bank, run = fixture()
        result = validate_remote_run(run, bank)
        self.assertEqual(result["mechanically_checked_cases"], 2)
        self.assertEqual(result["mechanical_checks_passed"], 2)
        self.assertIsNone(result["consumer_model_accuracy"])
        self.assertTrue(all(x["semantic_quality_score"] is None for x in result["cases"]))

    def test_missing_case_must_be_recorded_instead_of_hidden(self):
        bank, run = fixture()
        run["responses"].pop()
        with self.assertRaisesRegex(ValueError, "every frozen case"):
            validate_remote_run(run, bank)

    def test_mixed_commit_or_route_is_rejected(self):
        bank, run = fixture()
        for key, value in (("commit", "b" * 40), ("route", "web")):
            changed = copy.deepcopy(run)
            changed["access_events"][0][key] = value
            with self.assertRaisesRegex(ValueError, "Mixed commit/route"):
                validate_remote_run(changed, bank)

    def test_fabricated_excerpt_or_changed_text_is_rejected(self):
        bank, run = fixture()
        changed = copy.deepcopy(run)
        changed["responses"][0]["citations"][0]["excerpt"] = "shot_count: 99"
        with self.assertRaisesRegex(ValueError, "absent"):
            validate_remote_run(changed, bank)
        run["access_events"][0]["content"] += " modified"
        with self.assertRaisesRegex(ValueError, "Changed remote transcript"):
            validate_remote_run(run, bank)

    def test_parsed_annotation_cannot_be_filled_from_other_content(self):
        bank, run = fixture()
        run["access_events"][0]["annotation_text"] = "video:\n  id: fixture\n  shot_count: 99\n"
        with self.assertRaisesRegex(ValueError, "differs from fetched"):
            validate_remote_run(run, bank)

    def test_failed_web_fetch_never_uses_an_answer_from_another_route(self):
        bank, run = fixture()
        run["access_events"][0].update(status="failed", reason="cache miss")
        with self.assertRaisesRegex(ValueError, "unread/failed"):
            validate_remote_run(run, bank)

    def test_independent_accuracy_claim_is_rejected(self):
        bank, run = fixture()
        run["independent_model_evaluation"] = True
        run["consumer_model_accuracy"] = 1.0
        with self.assertRaisesRegex(ValueError, "independent model accuracy"):
            validate_remote_run(run, bank)

    def test_wrong_recorded_value_is_a_failure(self):
        bank, run = fixture()
        run["responses"][0]["answer_value"] = 99
        result = validate_remote_run(run, bank)
        self.assertEqual(result["mechanical_checks_passed"], 1)

    def test_blocked_case_cannot_contain_a_guessed_answer(self):
        bank, run = fixture()
        run["responses"][0]["status"] = "access_blocked"
        with self.assertRaisesRegex(ValueError, "fabricated answer"):
            validate_remote_run(run, bank)

    def test_recorded_remote_traces_remain_valid_when_available(self):
        result = remote_summary(ROOT)
        self.assertIsNone(result["consumer_model_accuracy"])
        for run in result["runs"]:
            self.assertFalse(run["independent_model_evaluation"])


if __name__ == "__main__":
    unittest.main()
