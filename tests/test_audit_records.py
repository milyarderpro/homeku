"""Targeted authoring operations on incomplete and checked synthetic audits."""
import json
import unittest

from . import test_prepare
from .fixtures.factory import make_inputs
from .test_audit import cli
from homeku.authoring import edit_record, update_shot
from homeku.common import LibraryError, dumps, read_json, sha256


class AuditRecordTests(test_prepare.VideoFixture, unittest.TestCase):
    def test_append_new_fact_and_reject_invalid_retry_without_mutation(self):
        audit, _ = make_inputs(self.work / "writing", self.video("facts"))
        session = audit.with_name("session.json")
        patch = self.work / "patch.json"
        original = read_json(audit)["shots"][0]
        fact = {"subject": "Penyekat kayu", "attribute": "bentuk", "value": "Label baru",
                "state": "not-present", "evidence": [0], "note": "Contoh fiktif."}
        write_options = {"block_index": 0, "category": "architecture", "expected_audit_sha256": sha256(audit)}
        for invalid in ({**fact, "evidence": []}, {**fact, "area_ids": ["wrong-area"]}):
            patch.write_text(dumps(invalid))
            before = audit.read_bytes()
            with self.assertRaises(LibraryError):
                edit_record(session, "shot-01", "fact", patch, **write_options)
            self.assertEqual(audit.read_bytes(), before)

        patch.write_text(dumps(fact))
        result = edit_record(session, "shot-01", "fact", patch, **write_options)
        self.assertIn("/design/0/architecture/facts/", result["source_pointer"])
        updated = read_json(audit)["shots"][0]
        expected = original["design"][0]["architecture"]
        self.assertEqual(updated["design"][0]["architecture"], {**expected, "facts": [*expected["facts"], fact]})
        self.assertEqual(updated["camera"], original["camera"])
        before = audit.read_bytes()
        write_options["expected_audit_sha256"] = sha256(audit)
        with self.assertRaisesRegex(LibraryError, "duplicate fact"):
            edit_record(session, "shot-01", "fact", patch, **write_options)
        self.assertEqual(audit.read_bytes(), before)

    def test_indexed_edit_requires_the_audit_used_to_choose_the_index(self):
        audit, _ = make_inputs(self.work / "writing", self.video("stale-index"))
        session = audit.with_name("session.json")
        prior_sha = sha256(audit)
        design = read_json(audit)["shots"][0]["design"]
        facts = design[0]["architecture"]["facts"]
        intended = facts[0]
        facts[0], facts[1] = facts[1], facts[0]
        patch = self.work / "patch.json"
        patch.write_text(dumps({"design": design}))
        update_shot(session, "shot-01", patch)

        patch.write_text(dumps({"note": "Koreksi untuk fakta yang dipilih."}))
        options = {"block_index": 0, "category": "architecture"}
        before = audit.read_bytes()
        for guard, message in ((None, "requires --expect-audit-sha256"), (prior_sha, "changed since it was read")):
            with self.subTest(guard=guard), self.assertRaisesRegex(LibraryError, message):
                edit_record(session, "shot-01", "fact", patch, record_index=0, expected_audit_sha256=guard, **options)
            self.assertEqual(audit.read_bytes(), before)
        edited = edit_record(session, "shot-01", "fact", patch, record_index=1,
                             expected_audit_sha256=sha256(audit), **options)
        self.assertEqual(edited["record"], {**intended, "note": "Koreksi untuk fakta yang dipilih."})

    def test_new_fact_rejects_a_design_block_index_from_an_older_audit(self):
        audit, _ = make_inputs(self.work / "writing", self.video("stale-block"), multi=True)
        session = audit.with_name("session.json")
        previous_sha = sha256(audit)
        design = read_json(audit)["shots"][0]["design"]
        area_ids = design[0]["area_ids"]
        design[0], design[1] = design[1], design[0]
        patch = self.work / "patch.json"
        patch.write_text(dumps({"design": design}))
        update_shot(session, "shot-01", patch)
        patch.write_text(dumps({"subject": "Penyekat", "attribute": "bentuk", "value": "Melengkung",
                                "state": "observed", "evidence": [4]}))
        before = audit.read_bytes()
        with self.assertRaisesRegex(LibraryError, "changed since it was read"):
            edit_record(session, "shot-01", "fact", patch, block_index=0, category="architecture",
                        expected_audit_sha256=previous_sha)
        self.assertEqual(audit.read_bytes(), before)
        edit_record(session, "shot-01", "fact", patch, block_index=1, category="architecture",
                    expected_audit_sha256=sha256(audit))
        self.assertEqual(read_json(audit)["shots"][0]["design"][1]["area_ids"], area_ids)

    def test_component_reorder_requires_an_explicit_override_change(self):
        audit, _ = make_inputs(self.work / "writing", self.video("component-order"), multi=True)
        session = audit.with_name("session.json")
        patch = self.work / "patch.json"
        phase = read_json(audit)["shots"][0]["camera"]["phases"][0]
        override = {"component_index": 0, "note": "Bukti untuk komponen mendekat.", "evidence": phase["evidence"]}
        patch.write_text(dumps({"overrides": [override]}))
        edit_record(session, "shot-01", "phase", patch, record_index=0, expected_audit_sha256=sha256(audit))
        notation = phase["notation"].replace("1.3", "1.4")
        patch.write_text(dumps({"notation": notation}))
        result = edit_record(session, "shot-01", "phase", patch, record_index=0, expected_audit_sha256=sha256(audit))
        self.assertEqual(result["record"]["overrides"], [override])

        reordered = " + ".join(reversed(notation.split(" + ")))
        before = audit.read_bytes()
        patch.write_text(dumps({"notation": reordered}))
        with self.assertRaisesRegex(LibraryError, "supply overrides for the new component order"):
            edit_record(session, "shot-01", "phase", patch, record_index=0, expected_audit_sha256=sha256(audit))
        self.assertEqual(audit.read_bytes(), before)
        patch.write_text(dumps({"notation": reordered, "overrides": [{**override, "component_index": 1}]}))
        result = edit_record(session, "shot-01", "phase", patch, record_index=0, expected_audit_sha256=sha256(audit))
        self.assertEqual(result["record"]["overrides"], [{**override, "component_index": 1}])

    def test_shrink_initial_phase_and_append_to_prepared_skeleton(self):
        from pathlib import Path
        from homeku.authoring import prepare

        result = prepare(self.video("phases"), [], self.work / "writing")
        session, audit = Path(result["session"]), Path(result["audit"])
        patch = self.work / "patch.json"
        patch.write_text(dumps({"end_s": .6}))
        edit_record(session, "shot-01", "phase", patch, record_index=0, expected_audit_sha256=sha256(audit))
        before = audit.read_bytes()
        for evidence, error in (([999], "unknown native evidence"), ([11], "outside phase")):
            with self.subTest(evidence=evidence):
                patch.write_text(dumps({"evidence": evidence}))
                with self.assertRaisesRegex(LibraryError, error):
                    edit_record(session, "shot-01", "phase", patch, record_index=0, expected_audit_sha256=sha256(audit))
                self.assertEqual(audit.read_bytes(), before)
        patch.write_text(dumps({"evidence": [2]}))
        result = edit_record(session, "shot-01", "phase", patch, record_index=0, expected_audit_sha256=sha256(audit))
        first = result["record"]
        self.assertEqual(first["evidence"], [2])
        self.assertEqual(first["notation"], "{{NOTATION}}")
        phase = {"start_s": .6, "end_s": 1.2, "notation": "Static", "depth_direction": "NO IN/OUT",
                 "focus": "Pintu.", "evidence": [6, 11],
                 "observations": {"depth": "Tetap.", "translation": "Tetap.", "rotation": "Tetap."}}
        patch.write_text(dumps(phase))
        appended = edit_record(session, "shot-01", "phase", patch)
        self.assertEqual(appended["source_pointer"], "/shots/0/camera/phases/1")
        self.assertEqual(read_json(audit)["shots"][0]["camera"]["phases"], [first, phase])
        with self.assertRaisesRegex(LibraryError, "unknown record index"):
            edit_record(session, "shot-01", "phase", patch, record_index=2, expected_audit_sha256=sha256(audit))

    def test_phase_evidence_must_be_visible_in_its_area_scope(self):
        audit, _ = make_inputs(self.work / "writing", self.video("phase-scope"), multi=True)
        session = audit.with_name("session.json")
        patch = self.work / "patch.json"
        before = audit.read_bytes()
        scope = {"area_ids": ["kitchen-1"]}
        for fields in (scope, {**scope, "evidence": [4, 11],
                              "overrides": [{"component_index": 0, "evidence": [0, 11]}]}):
            with self.subTest(fields=fields):
                patch.write_text(dumps(fields))
                with self.assertRaisesRegex(LibraryError, "evidence outside area visibility"):
                    edit_record(session, "shot-01", "phase", patch, record_index=0, expected_audit_sha256=sha256(audit))
                self.assertEqual(audit.read_bytes(), before)
        patch.write_text(dumps({**scope, "evidence": [4, 11]}))
        result = edit_record(session, "shot-01", "phase", patch, record_index=0, expected_audit_sha256=sha256(audit))
        self.assertTrue(result["camera_recheck_required"])
        self.assertEqual(result["record"]["area_ids"], ["kitchen-1"])

    def test_camera_checkpoint_rejects_override_outside_known_area_after_shot_patch(self):
        from homeku.authoring import check_camera

        audit, _ = make_inputs(self.work / "writing", self.video("checkpoint-scope"), multi=True)
        session = audit.with_name("session.json")
        patch = self.work / "patch.json"
        phase = read_json(audit)["shots"][0]["camera"]["phases"][0]
        phase.update(area_ids=["kitchen-1"], evidence=[4, 11],
                     overrides=[{"component_index": 0, "evidence": [0, 11]}])
        patch.write_text(dumps({"camera": {"phases": [phase]}}))
        update_shot(session, "shot-01", patch)
        previous_checkpoint = session.read_bytes()
        with self.assertRaisesRegex(LibraryError, r"/overrides/0: evidence outside area visibility"):
            check_camera(session, shot_id="shot-01")
        self.assertEqual(session.read_bytes(), previous_checkpoint)

        phase["overrides"][0]["evidence"] = [4, 11]
        patch.write_text(dumps({"camera": {"phases": [phase]}}))
        update_shot(session, "shot-01", patch)
        result = check_camera(session, shot_id="shot-01")
        self.assertEqual(result["checked"][0]["shot"], "shot-01")

    def test_phase_correction_through_cli_and_scoped_recheck(self):
        audit, _ = make_inputs(self.work / "writing", self.video("correction"))
        session = audit.with_name("session.json")
        before = read_json(audit)["shots"][0]
        notation = before["camera"]["phases"][0]["notation"].replace("1.3", "1.4")
        patch = self.work / "patch.json"
        patch.write_text(dumps({"notation": notation}))
        result = cli("edit-record", session, "--shot-id", "shot-01", "--kind", "phase",
                     "--record-index", 0, "--expect-audit-sha256", sha256(audit), "--patch", patch)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)["camera_recheck_required"])
        self.assertEqual(cli("check-camera", session).returncode, 1)
        recheck = cli("check-camera", session, "--shot-id", "shot-01")
        self.assertEqual(recheck.returncode, 0, recheck.stderr)
        original_phase = before["camera"]["phases"][0]
        updated = read_json(audit)["shots"][0]
        self.assertEqual(updated["camera"]["phases"][0], {**original_phase, "notation": notation})
        self.assertEqual(updated["design"], before["design"])
