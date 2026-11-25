"""Shared renderer imports must not pull old engines into the active graph."""
import subprocess
import sys
import unittest
from pathlib import Path
from . import test_prepare
from homeku.common import LibraryError, sha256
from homeku.render_assets import ALIGNED_LAYOUT, LAYOUT, PROFILE_TEMPLATE, TEMPLATE, render_config, verify_renderer

ROOT = Path(__file__).resolve().parents[1]


class RenderAssetTests(unittest.TestCase):
    def test_media_and_report_import_without_version_modules(self):
        code = ("import sys; sys.path.insert(0, 'tools'); "
                "import homeku.media, homeku.reporting, homeku.render_assets; "
                "assert not [m for m in sys.modules if m.startswith('homeku.media_v') "
                "or m.startswith('homeku.reporting_v')]")
        subprocess.run([sys.executable, "-B", "-c", code], cwd=ROOT, check=True)

    def test_layout_fingerprint_is_independent_of_report_template(self):
        self.assertEqual(sha256(LAYOUT), "d68b9b5a84d6f1c336a5edf4cfa8a1848aa2c77840d503d488e2fcf3fc3ece37")
        self.assertEqual(render_config()["layout_sha256"], sha256(ALIGNED_LAYOUT))
        for design, template in (({}, TEMPLATE), ({"house_type": {}}, PROFILE_TEMPLATE)):
            for layout in (LAYOUT, ALIGNED_LAYOUT):
                with self.subTest(template=template.name, layout=layout.name):
                    config = render_config(template_path=template, layout_path=layout)
                    self.assertEqual(verify_renderer(config, {"design": design}), template)
                    config["layout_sha256"] = "0" * 64
                    with self.assertRaisesRegex(LibraryError, "Unknown media layout fingerprint"):
                        verify_renderer(config, {"design": design})

    def test_neutral_template_and_layout_preserve_approved_hierarchy(self):
        import json
        template = (ROOT / "tools/assets/templates/analysis.md").read_text()
        self.assertEqual(sum(line.startswith("## ") for line in template.splitlines()), 6)
        layout = json.loads((ROOT / "tools/assets/layouts/media.json").read_text())
        self.assertEqual(layout["version"], "3.0")
        self.assertLess(layout["caption_time_size"], layout["caption_size"])
        self.assertTrue((ROOT / "tools/assets/fonts/LICENSE.txt").is_file())
