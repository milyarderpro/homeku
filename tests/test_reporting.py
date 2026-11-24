"""Golden reports and structural checks for normal and multi-area takes."""
import copy
import re
import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from homeku.common import LibraryError, read_json
from homeku.derivations import camera_summary
from homeku.reporting import render_report
from homeku.report_validation import HEADINGS, validate_report

ROOT = Path(__file__).resolve().parents[1]
PTS = [i / 10 for i in range(12)]


class ReportingTests(unittest.TestCase):
    def audit(self, name):
        return read_json(ROOT / "audit" / "examples" / name / "audit.json")

    def test_golden_reports_preserve_all_source_narratives_and_notation(self):
        for name in ("normal", "multi"):
            with self.subTest(name=name):
                audit = self.audit(name)
                original = copy.deepcopy(audit)
                report = render_report(audit, PTS)
                golden = ROOT / "tests/fixtures/reports" / f"{name}.md"
                self.assertEqual(report, golden.read_text())
                self.assertEqual(re.findall(r"^## .+$", report, re.M), HEADINGS)
                self.assertIn("**60–90 m²**", report)
                for shot in audit["shots"]:
                    self.assertIn("**Camera:** " + camera_summary(shot), report)
                    self.assertIn(shot["camera"]["description"], report)
                    for block in shot["design"]:
                        for key in ("architecture", "furnishings", "environment"):
                            self.assertIn(block[key]["text"], report)
                    for overview in shot["overviews"]:
                        self.assertIn(overview["composition_summary"], report)
                self.assertEqual(audit, original)

    def test_damage_to_template_structure_is_rejected(self):
        audit = self.audit("normal")
        text = render_report(audit, PTS)
        for damaged in (text + "\n## 7. Extra\n", text.replace("#### **B.", "#### **D."),
                        text.replace("**Arsitektur**", "**Extra**"),
                        text.replace("media/shot-01.jpg", "media/missing.jpg"),
                        text.replace("| Duration |", "| Extra | Duration |")):
            with self.subTest(damaged=damaged[:30]), self.assertRaises(LibraryError):
                validate_report(damaged, audit, PTS)

    def test_inline_characters_cannot_create_new_links_or_emphasis(self):
        audit = self.audit("normal")
        audit["areas"][0]["label"] = "Bath_[A] | Laundry"
        audit["shots"][0]["camera"]["description"] = "Memutar ke [A] dan *aksen*."
        text = render_report(audit, PTS)
        self.assertIn(r"Bath\_\[A\] \| Laundry", text)
        self.assertIn(r"Memutar ke \[A\] dan \*aksen\*.", text)
        audit["shots"][0]["camera"]["description"] = "Kamera maju.\n\n## 7. Tambahan"
        with self.assertRaises(LibraryError):
            render_report(audit, PTS)
