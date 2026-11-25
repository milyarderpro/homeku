"""Canonical model semantics and evidence scope, without visual audit claims."""
import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from homeku.models import validate_audit
from homeku.common import LibraryError

ROOT = Path(__file__).resolve().parents[1]


class ModelTests(unittest.TestCase):
    def audit(self, name="normal"):
        return json.loads((ROOT / "audit/examples" / name / "audit.json").read_text())

    def validate(self, value):
        return validate_audit(value, 1.2, [i / 10 for i in range(12)])

    def test_complete_examples_validate_without_mutation_or_confidence_defaults(self):
        for name in ("normal", "multi"):
            value = self.audit(name)
            before = copy.deepcopy(value)
            self.validate(value)
            self.assertEqual(value, before)
            value["shots"][0]["camera"]["phases"][0].pop("confidence", None)
            self.validate(value)
            self.assertNotIn("confidence", value["shots"][0]["camera"]["phases"][0])

    def test_reversed_floor_range_and_placeholders_fail(self):
        value = self.audit()
        value["design"]["size"]["floor_area_m2"] = {"min": 90, "max": 60}
        with self.assertRaisesRegex(LibraryError, "min exceeds max"):
            self.validate(value)
        value = self.audit()
        value["design"]["name"] = "{{NAME}}"
        with self.assertRaisesRegex(LibraryError, "placeholder"):
            self.validate(value)

    def test_structured_palette_has_one_source(self):
        value = self.audit()
        design = value["design"]
        design.update(house_type={"value": "Tower House", "state": "uncertain", "evidence": [0]},
                      palette=[{"value": "Putih gading", "role": "Dominan", "hex": "#F0E8DA",
                                "state": "observed", "evidence": [0]}])
        design["features"] = [f for f in design["features"] if f["aspect"] != "palette"]
        self.validate(value)
        design["palette"][0]["evidence"] = [12]
        with self.assertRaisesRegex(LibraryError, "/design/palette/0: unknown native evidence"):
            self.validate(value)
        design["palette"][0]["evidence"] = [0]
        design["features"].append({"aspect": "palette", "value": "Ivory", "state": "observed",
                                   "evidence": [0]})
        with self.assertRaisesRegex(LibraryError, "only palette source"):
            self.validate(value)

    def test_wrong_area_evidence_and_override_scope_fail(self):
        value = self.audit("multi")
        fact = value["shots"][0]["design"][1]["architecture"]["facts"][0]
        fact["evidence"] = [0]
        with self.assertRaisesRegex(LibraryError, "area visibility"):
            self.validate(value)
        value = self.audit()
        fact = value["shots"][0]["design"][0]["architecture"]["facts"][0]
        fact["area_ids"] = ["missing-area"]
        with self.assertRaisesRegex(LibraryError, "area"):
            self.validate(value)

    def test_camera_needs_two_frames_and_consistent_explicit_depth(self):
        value = self.audit()
        phase = value["shots"][0]["camera"]["phases"][0]
        phase["evidence"] = [0]
        with self.assertRaisesRegex(LibraryError, "two distinct"):
            self.validate(value)
        phase["evidence"] = [0, 11]
        phase["depth_direction"] = "OUT"
        with self.assertRaisesRegex(LibraryError, "conflicts"):
            self.validate(value)

    def test_duplicate_facts_and_invalid_temporal_partition_fail(self):
        value = self.audit()
        facts = value["shots"][0]["design"][0]["architecture"]["facts"]
        facts.append(copy.deepcopy(facts[0]))
        with self.assertRaisesRegex(LibraryError, "duplicate fact"):
            self.validate(value)
        value = self.audit()
        value["shots"][0]["camera"]["tempo"]["segments"][1]["start_s"] = 0.7
        with self.assertRaisesRegex(LibraryError, "gap/overlap"):
            self.validate(value)

    def test_normal_midpoint_and_multi_selection_visibility(self):
        value = self.audit()
        value["shots"][0]["panels"][1]["frame_index"] = 5
        with self.assertRaisesRegex(LibraryError, "midpoint"):
            self.validate(value)
        value = self.audit("multi")
        value["shots"][0]["overviews"][1]["frame_index"] = 0
        with self.assertRaisesRegex(LibraryError, "visible"):
            self.validate(value)

    def test_all_moderate_and_optional_numbers_still_validate(self):
        value = self.audit()
        shot = value["shots"][0]
        shot["camera"]["tempo"] = {"label": "moderate", "description": "Sedang konstan."}
        phase = shot["camera"]["phases"][0]
        phase["notation"] = "Dolly-In + Pan Right"
        self.validate(value)
        phase["overrides"] = [{"component_index": 9, "evidence": [0, 11]}]
        with self.assertRaisesRegex(LibraryError, "override"):
            self.validate(value)

    def test_old_source_rejected_without_conversion(self):
        value = self.audit()
        value["schema_version"] = "2.5"
        with self.assertRaisesRegex(LibraryError, "Unsupported audit format"):
            self.validate(value)

    def test_independent_phases_need_their_own_temporal_evidence_and_three_axes(self):
        audit = self.audit()
        shot = audit["shots"][0]
        phase = shot["camera"]["phases"][0]
        first = {**phase, "end_s": .6, "evidence": [0, 5]}
        second = {**phase, "start_s": .6, "notation": "Orbit Left + Pan Right",
                  "depth_direction": "NO IN/OUT", "evidence": [6, 11]}
        shot["camera"]["phases"] = [first, second]
        self.validate(audit)
        second["evidence"] = [0, 1]
        with self.assertRaisesRegex(LibraryError, "phase"):
            self.validate(audit)
        second["evidence"] = [6, 11]
        second["observations"] = {**phase["observations"], "rotation": " "}
        with self.assertRaisesRegex(LibraryError, "blank"):
            self.validate(audit)
        second["observations"].pop("rotation")
        with self.assertRaisesRegex(LibraryError, "rotation"):
            self.validate(audit)
