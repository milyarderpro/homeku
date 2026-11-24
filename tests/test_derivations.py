"""Pure views preserve authored values and provenance."""
import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from homeku.common import LibraryError
from homeku.derivations import (camera_summary, phase_tempo, selections, frame_map,
                                claims, fact_claims, derived_shot, resolve)
from homeku.camera_pattern import shot_pattern, validate_direction, provenance

ROOT = Path(__file__).resolve().parents[1]


class DerivationTests(unittest.TestCase):
    def audit(self, name="normal"):
        return json.loads((ROOT / "audit/examples" / name / "audit.json").read_text())

    def test_summary_tempo_scope_and_views_do_not_mutate_source(self):
        value = self.audit()
        before = copy.deepcopy(value)
        shot = value["shots"][0]
        result = derived_shot(shot, 0)
        self.assertEqual(result["camera_summary"], "Dolly-In (~1.3×) + gentle Pan Right (~15°).")
        self.assertEqual(result["phase_tempos"], ["variable"])
        self.assertEqual(result["camera_pattern"], "IN")
        self.assertEqual(value, before)
        for pointer in result["inputs"]:
            self.assertIsNotNone(resolve(value, pointer))
        self.assertNotIn("camera_summary", shot)

    def test_every_claim_pointer_resolves_to_original_claim(self):
        for name, expected in (("normal", 7), ("multi", 12)):
            value = self.audit(name)
            self.assertEqual(len(list(fact_claims(value["shots"][0], 0))), expected)
            for pointer, claim, _, _, _ in claims(value):
                self.assertIs(resolve(value, pointer), claim)
        with self.assertRaises(LibraryError):
            resolve(value, "/shots/99")

    def test_selection_ids_and_pts_are_mechanical(self):
        value = self.audit("multi")
        times = [i / 10 for i in range(12)]
        rows = list(selections(value, times))
        self.assertEqual(len(rows), 6)
        self.assertEqual(rows[0]["label"], "Start")
        self.assertEqual(rows[3]["label"], "End")
        self.assertEqual(rows[0]["id"], "s01-panel-01")
        self.assertEqual(rows[1]["timestamp_s"], 0.4)
        for row in rows:
            self.assertEqual(resolve(value, row["source_pointer"])["frame_index"], row["frame_index"])
        mapping = frame_map(value, times)
        self.assertIn("2", mapping)
        self.assertLess(len(mapping), len(times))
        self.assertEqual(rows, list(selections(value, mapping)))

    def test_unknown_tempo_is_not_defaulted_to_moderate(self):
        value = self.audit()
        shot = value["shots"][0]
        shot["camera"]["tempo"]["segments"][1]["label"] = "unknown"
        self.assertEqual(phase_tempo(shot, shot["camera"]["phases"][0]), "unknown")

    def test_depth_pattern_uses_explicit_classification(self):
        value = self.audit()
        shot = value["shots"][0]
        phase = shot["camera"]["phases"][0]
        phase["notation"] = "Zoom-In (~2×)"
        phase["depth_direction"] = "NO IN/OUT"
        self.assertEqual(shot_pattern(shot), "NO IN/OUT")
        validate_direction(phase)
        phase["depth_direction"] = None
        self.assertIsNone(shot_pattern(shot))
        phase["notation"] = "Dolly-Out"
        phase["depth_direction"] = "IN"
        with self.assertRaises(LibraryError):
            validate_direction(phase)
        proof = provenance(shot, 0)[0]
        self.assertEqual(proof["source_pointer"], "/shots/0/camera/phases/0/depth_direction")
