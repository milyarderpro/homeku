"""Shared renderer imports must not pull old engines into the active graph."""
import subprocess
import sys
import unittest
from pathlib import Path
from . import test_prepare  # Load the local runtime path.
from homeku.common import LibraryError, sha256
from homeku.render_assets import LAYOUT, TEMPLATE, render_config, verify_renderer

ROOT = Path(__file__).resolve().parents[1]


class RenderAssetTests(unittest.TestCase):
    def test_media_and_report_import_without_version_modules(self):
        code = ("import sys; sys.path.insert(0, 'tools'); "
                "import homeku.media, homeku.reporting, homeku.render_assets; "
                "assert not [m for m in sys.modules if m.startswith('homeku.media_v') "
                "or m.startswith('homeku.reporting_v')]")
        subprocess.run([sys.executable, "-B", "-c", code], cwd=ROOT, check=True)

    def test_only_canonical_template_and_layout_fingerprints_are_accepted(self):
        config = render_config()
        self.assertEqual(config["layout_sha256"], sha256(LAYOUT))
        self.assertEqual(config["template_sha256"], sha256(TEMPLATE))
        verify_renderer(config)
        for field in ("layout_sha256", "template_sha256"):
            with self.subTest(field=field), self.assertRaises(LibraryError):
                verify_renderer({**config, field: "0" * 64})

    def test_neutral_template_and_layout_preserve_approved_hierarchy(self):
        import json
        template = (ROOT / "tools/assets/templates/analysis.md").read_text()
        self.assertEqual(sum(line.startswith("## ") for line in template.splitlines()), 6)
        layout = json.loads((ROOT / "tools/assets/layouts/media.json").read_text())
        self.assertEqual(layout["version"], "3.1")
        self.assertLess(layout["caption_time_size"], layout["caption_size"])
        self.assertTrue((ROOT / "tools/assets/fonts/LICENSE.txt").is_file())
