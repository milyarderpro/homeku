"""Source integrity checks use isolated files, never production mutations."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from verify_source_integrity import (
    MANIFEST, SourceIntegrityError, scan_sources, sha256_file, verify_sources, write_manifest,
)


class SourceIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "video").mkdir()
        (self.root / "references").mkdir()
        self.add_source("kept", b"source bytes")
        write_manifest(self.root)

    def add_source(self, ident, content, filename=None):
        filename = filename or ident + ".mp4"
        (self.root / "video" / filename).write_bytes(content)
        folder = self.root / "references" / ident
        folder.mkdir()
        data = {"video": {"id": ident, "filename": filename, "shot_count": 1},
                "shots": [{"id": "shot-01"}]}
        (folder / "analysis.yaml").write_text(yaml.safe_dump(data))
        return folder

    def retire(self):
        manifest = json.loads((self.root / MANIFEST).read_text())
        manifest["retired_references"] = [{
            "reference_id": "removed", "canonical_reference_id": "kept",
            "sha256": sha256_file(self.root / "video/kept.mp4"),
            "retired_on": "2026-11-17", "reason": "exact_duplicate",
        }]
        (self.root / MANIFEST).write_text(json.dumps(manifest))
        write_manifest(self.root)

    def test_missing_source_rejected(self):
        (self.root / "video/kept.mp4").unlink()
        (self.root / "video/other.mp4").write_bytes(b"other")
        with self.assertRaisesRegex(SourceIntegrityError, "Missing source for kept"):
            verify_sources(self.root)

    def test_renamed_duplicate_rejected_before_refresh(self):
        (self.root / "video/alias.mp4").write_bytes(b"source bytes")
        with self.assertRaisesRegex(SourceIntegrityError, "Duplicate video content"):
            write_manifest(self.root)

    def test_changed_source_bytes_require_review(self):
        (self.root / "video/kept.mp4").write_bytes(b"replacement bytes")
        with self.assertRaisesRegex(SourceIntegrityError, "manifest differs"):
            verify_sources(self.root)

    def test_two_references_cannot_share_source(self):
        folder = self.root / "references/second"
        folder.mkdir()
        (folder / "analysis.yaml").write_text(yaml.safe_dump({
            "video": {"id": "second", "filename": "kept.mp4", "shot_count": 1},
            "shots": [{"id": "shot-01"}],
        }))
        with self.assertRaisesRegex(SourceIntegrityError, "shared by multiple"):
            write_manifest(self.root)

    def test_unsafe_filename_rejected(self):
        path = self.root / "references/kept/analysis.yaml"
        value = yaml.safe_load(path.read_text())
        value["video"]["filename"] = "../outside.mp4"
        path.write_text(yaml.safe_dump(value))
        with self.assertRaisesRegex(SourceIntegrityError, "Unsafe or invalid"):
            write_manifest(self.root)

    def test_unannotated_sources_are_separate_and_pinned(self):
        (self.root / "video/incoming.mp4").write_bytes(b"incoming")
        report = write_manifest(self.root)
        self.assertEqual(report["reference_count"], 1)
        self.assertEqual(report["unannotated_sources"][0]["source_path"], "video/incoming.mp4")
        self.assertEqual(verify_sources(self.root), report)

    def test_retired_request_cannot_be_reintroduced(self):
        self.retire()
        pending = self.root / "requests/pending"
        pending.mkdir(parents=True)
        (pending / "removed.json").write_text("{}")
        with self.assertRaisesRegex(SourceIntegrityError, "Retired artifact restored"):
            write_manifest(self.root)

    def test_retired_reference_cannot_be_reintroduced(self):
        self.retire()
        self.add_source("removed", b"different bytes")
        with self.assertRaisesRegex(SourceIntegrityError, "Retired reference restored"):
            write_manifest(self.root)

    def test_retirement_canonical_hash_stays_pinned(self):
        self.retire()
        (self.root / "video/kept.mp4").write_bytes(b"replacement")
        with self.assertRaisesRegex(SourceIntegrityError, "canonical source changed"):
            write_manifest(self.root)

    def test_repository_manifest(self):
        report = verify_sources(ROOT)
        self.assertEqual(report["reference_count"], 57)
        self.assertEqual(report["shot_count"], 295)
        self.assertNotIn("edh026", [r["reference_id"] for r in report["references"]])
        self.assertIn("edh027", [r["reference_id"] for r in report["references"]])
        restored = next(r for r in report["references"] if r["reference_id"] == "VID-001")
        self.assertEqual(restored["source_path"], "video/dreamshome01.mp4")


if __name__ == "__main__":
    unittest.main()
