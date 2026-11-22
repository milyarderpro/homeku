"""Human report layout and snapshot checks; no video audit is claimed."""
import tempfile
import unittest
from pathlib import Path
from tests.fixtures.factory import make_v2_inputs
from homeku.common import LibraryError, read_json
from homeku.reporting import render_report, render_config, TEMPLATES


class V2ReportingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory()
        _,path,_=make_v2_inputs(Path(cls.temp.name),multi=True)
        cls.audit=read_json(path)
    @classmethod
    def tearDownClass(cls):cls.temp.cleanup()

    def test_five_sections_cards_and_authored_narratives_preserved(self):
        text=render_report(self.audit,render_config())
        self.assertEqual(sum(line.startswith("## ") for line in text.splitlines()),5)
        for phrase in ["#### A. Desain area","#### B. Komposisi dan cahaya","#### C. Gerakan kamera",'id="shot-01"']:self.assertIn(phrase,text)
        for row in self.audit["shots"][0]["design"]:
            for key in ("architecture","furnishings","environment"):self.assertIn(row[key],text)
        self.assertIn(self.audit["shots"][0]["camera_summary"],text)
        self.assertIn(self.audit["shots"][0]["camera_simple"],text)
        self.assertIn("**Timeline gerakan**",text)
        self.assertNotIn("frame_index",text)
        self.assertNotIn("{{",text)

    def test_area_estimate_displays_only_required_range(self):
        text=render_report(self.audit,render_config())
        row=next(line for line in text.splitlines() if "| Perkiraan luas lantai |" in line)
        self.assertEqual(row,"| Perkiraan luas lantai | **60–90 m²** |")
        self.assertNotIn(self.audit["size"]["floor_area_m2"]["basis"],text)
        self.assertNotIn("kepastian rendah",row)

    def test_normal_single_phase_omits_optional_sections(self):
        with tempfile.TemporaryDirectory() as d:
            _,path,_=make_v2_inputs(Path(d));a=read_json(path)
        text=render_report(a,render_config())
        self.assertNotIn("**Timeline gerakan**",text)
        self.assertNotIn("**Hubungan antararea**",text)
        self.assertNotIn("**DNA perjalanan:**",text)
        self.assertIn("media/shot-01.jpg",text)
        self.assertNotIn("area-overview.jpg",text)

    def test_registered_template_is_independent_of_later_authoring_template(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as d:
            # A new registered version does not change rendering of accepted 2.0.0.
            before=render_report(self.audit,render_config(version="2.0.0"))
            with patch.dict(TEMPLATES,{"2.1.0":Path(d)/"not-in-use.md"}):
                self.assertEqual(before,render_report(self.audit,render_config(version="2.0.0")))
        config=render_config();config["template_sha256"]="0"*64
        with self.assertRaisesRegex(LibraryError,"template hash"):render_report(self.audit,config)

    def test_new_style_language_contract_preserves_names_and_indonesian_explanations(self):
        import copy
        from homeku.models import schema_check
        a=copy.deepcopy(self.audit);a["identity"].update(primary_style="Organic Modern Cottage",interior_style="Warm Contemporary Cottage",influences="Modern Farmhouse pada bingkai jendela; Scandinavian pada furnitur ringan.")
        text=render_report(a,render_config())
        self.assertIn("**Gaya utama:** Organic Modern Cottage",text)
        self.assertIn(a["identity"]["interior_style"],text)
        self.assertIn(a["identity"]["influences"],text)
        a["identity"].pop("style_names_language")
        with self.assertRaisesRegex(LibraryError,"style_names_language=en"):
            render_report(a,render_config())
        render_report(a,render_config(version="2.0.0"))
        a["identity"]["style_names_language"]="id"
        with self.assertRaises(LibraryError):schema_check(a,"audit-v2.schema.json")

    def test_display_rounding_does_not_mutate_source_and_old_report_is_supported(self):
        import copy
        a=copy.deepcopy(self.audit);a["shots"][0]["panels"][0]["timestamp_s"]=0.033333333
        before=copy.deepcopy(a)
        text=render_report(a,render_config())
        self.assertIn("Start · 0.03s",text)
        self.assertEqual(a,before)
        self.assertIn("0.033",render_report(a,render_config(version="2.0.0")))

    def test_version_pairs_and_bold_font_digest_are_checked(self):
        from homeku.reporting import verify_renderer
        new=render_config();old=render_config(version="2.0.0")
        verify_renderer(old);verify_renderer(new)
        new["media"]="2.0.0"
        with self.assertRaisesRegex(LibraryError,"version pair"):verify_renderer(new)
        new=render_config();new["bold_font_sha256"]="0"*64
        with self.assertRaisesRegex(LibraryError,"bold font hash"):verify_renderer(new)
