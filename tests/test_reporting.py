"""Golden reports and structural checks for normal and multi-area takes."""
import copy
import re
import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from homeku.common import LibraryError, read_json
from homeku.derivations import camera_summary, frame_map
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
                design = audit["design"]
                del design["house_type"], design["palette"]
                design["features"].append({"aspect": "palette", "value": "Putih, kayu tampak terang dan aksen gelap."})
                next(c for c in design["features"] if c["aspect"] == "lighting")["value"] = "unknown"
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

    def test_multi_area_labels_follow_shot_and_overview_scope(self):
        audit = self.audit("multi")
        audit["areas"][0]["label"] = "Open-Plan Living"
        audit["areas"][1]["label"] = "Sleeping Loft"
        report = render_report(audit, PTS)
        self.assertIn("### Shot 01 · Open-Plan Living / Sleeping Loft", report)
        overview = report.split(HEADINGS[3], 1)[1].split(HEADINGS[4], 1)[0]
        self.assertIn("**Shot 01 · Open-Plan Living · ", overview)
        self.assertIn("**Shot 01 · Sleeping Loft · ", overview)
        self.assertNotIn("Open-Plan Living / Sleeping Loft", overview)

    def test_standard_profile_order_and_palette_escaping(self):
        audit = self.audit("multi")
        design = audit["design"]
        design.update(house_type={"value": "Tower House", "state": "uncertain", "evidence": [0]},
                      palette=[{"value": "Gading [hangat]", "role": "Aksen | utama", "hex": "#F0E8DA",
                                "state": "observed", "evidence": [0]}])
        report = render_report(audit, PTS)
        self.assertEqual(re.findall(r"^## .+$", report, re.M), HEADINGS)
        profile = report.split(HEADINGS[1], 1)[0]
        labels = re.findall(r"^- \*\*(.+?):\*\*", profile, re.M)
        self.assertEqual(labels, ["Nama desain", "Tipe rumah", "Gaya utama", "Pengaruh gaya",
                                  "Gaya interior", "Susunan ruang utama", "Ciri khas", "Material utama",
                                  "Pencahayaan", "Atmosfer", "Lingkungan"])
        self.assertIn(r"| Aksen \| utama | Gading \[hangat\] | `#F0E8DA` |", profile)
        self.assertEqual(report.count("### Palet warna"), 1)
        with self.assertRaises(LibraryError):
            validate_report(report.replace("### Palet warna", "### Extra"), audit, PTS)

    def test_production_start_is_conditional_and_uses_manifest_pts(self):
        audit = self.audit("normal")
        original = render_report(audit, PTS)
        composition = audit["shots"][0]["composition"]
        composition["production_start"] = {"frame_index": 4, "composition_summary": "Dari dekat pintu [kiri]."}
        report = render_report(audit, frame_map(audit, PTS))
        row = r"- **Production Start:** F4 · 0.40s · Dari dekat pintu \[kiri\]."
        self.assertIn(row, report)
        self.assertEqual(report.replace(row + "\n", ""), original)
        self.assertEqual(re.findall(r"^## .+$", report, re.M), HEADINGS)

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
