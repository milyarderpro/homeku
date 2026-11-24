"""Independent camera parser; experiment syntax without visual audit claims."""
import ast
import unittest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from homeku.camera_notation import component, normalize, parse, bounds
from homeku.common import LibraryError

CASES = ['Pure Orbit Left → Accelerating Dolly-In (~2.0×)', 'Pure Orbit Right → Accelerating Dolly-In (~2.1×)', 'Straight Dolly-In → Dolly-In + Strong Pan Right (~25°–30°)', 'Accelerating Dolly-In (~2.2×) + Accelerating Pan Left (~25°–30°)', 'Dolly-In (~2.0×) + Subtle Pan Right (~15°)', 'Dolly-Out (~1.6×) + Orbit Left + Subtle Pan Right (Ease-Out)', 'Dolly-Out (~1.75×) + Orbit Right + Strong Pan Left (Ease-Out)', 'Mild Dolly-Out (~1.3×) + Orbit Left + Strong Pan Right (~35°, Ease-Out)', 'Diagonal Dolly-Out (~2.5×) + Moderate Pan Right (Ease-Out)', 'Diagonal Dolly-Out (~1.75×) + Subtle Pan Left (Ease-Out)', 'Dolly-Out (~1.6×) + Orbit Left + Pan Right', 'Pan Right', 'Dolly-In', 'Static Distance + Orbit Left']


class CameraParserTests(unittest.TestCase):
    def test_all_experiment_cases_with_optional_numbers(self):
        for notation in CASES:
            with self.subTest(notation=notation):
                for phase in notation.split(" → "):
                    parsed = parse(phase)
                    self.assertEqual(" + ".join(c["raw"] for c in parsed), phase)
                    self.assertTrue(parsed)

    def test_normalization_and_literal_target(self):
        self.assertEqual(normalize("Dolly-Out (~1,6x)"), "Dolly-Out (~1.6×)")
        value = component("Subtle Pan Right (Ease-Out) toward teak door")
        self.assertEqual(value["movement"], "Pan Right")
        self.assertEqual(value["qualifiers"], ["Subtle", "Ease-Out"])
        self.assertEqual(value["toward"], "teak door")
        self.assertEqual(value["estimates"], [])

    def test_unknown_labels_remain_literal(self):
        value = component("Subtle Novel Move toward arch")
        self.assertEqual(value["movement"], "other")
        self.assertEqual(value["raw"], "Subtle Novel Move toward arch")
        self.assertEqual(value["qualifiers"], ["Subtle"])

    def test_invalid_ranges_and_numbers_fail(self):
        for value in ("~0×", "~.8×", "~2–1×", "~0°", "~30–10°", "~NaN×", "~1e309×"):
            with self.subTest(value=value), self.assertRaises(LibraryError):
                component("Dolly-In (" + value + ")")
        self.assertEqual(bounds("~25°–30°", "°"), (25, 30))

    def test_easing_is_component_specific_not_overall_tempo(self):
        values = parse("Dolly-Out (~1.6×) + Orbit Left + Subtle Pan Right (Ease-Out)")
        self.assertNotIn("Ease-Out", values[0]["qualifiers"])
        self.assertIn("Ease-Out", values[-1]["qualifiers"])
        self.assertNotIn("tempo", values[-1])

    def test_no_legacy_import(self):
        path = Path(__file__).resolve().parents[1] / "tools/homeku/camera_notation.py"
        tree = ast.parse(path.read_text())
        self.assertFalse(any(isinstance(n, ast.ImportFrom) and n.module == "markdown"
                             for n in ast.walk(tree)))
