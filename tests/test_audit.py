"""Portable chat helper tests; all generated sources/results stay in temp roots."""
from __future__ import annotations

import importlib.util
import json
import io
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from homeku.common import LibraryError, read_json, sha256
from homeku.engine import check, ingest
from homeku.exporter import assemble, extract_frame, frame_times, nearest, sample
from homeku.validation import CODE_ROOT
from tests.fixtures.factory import isolated_root, make_folder

spec = importlib.util.spec_from_file_location("build_audit_kit", CODE_ROOT / "tools/build_audit_kit.py")
kit_builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kit_builder)


class AuditHelperTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.shared = tempfile.TemporaryDirectory()
        cls.template = make_folder(Path(cls.shared.name) / "template", rid="audit-sample")

    @classmethod
    def tearDownClass(cls):
        cls.shared.cleanup()

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.work = Path(self.temporary.name)
        self.source = self.work / "audit-sample.mp4"
        shutil.copyfile(self.template / "source.mp4", self.source)
        self.analysis = self.work / "analysis.md"
        shutil.copyfile(self.template / "analysis.md", self.analysis)
        manifest = read_json(self.template / "manifest.json")
        self.info = {key: manifest["audit"][key] for key in ("reviewed_ranges", "ai", "created_at")}

    def tearDown(self):
        self.temporary.cleanup()

    def build(self, **kwargs):
        return assemble(self.source, self.analysis, self.info, self.work / "candidate", purpose="fixture", **kwargs)

    def test_integer_pts_avoids_30fps_rounding_crossing_cut(self):
        source = self.work / "thirty.mp4"
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i",
                        "testsrc2=size=96x160:rate=30", "-t", "0.2", "-c:v", "mpeg4", "-an", str(source)], check=True)
        times = frame_times(source)
        self.assertEqual(len(times), 6)
        self.assertEqual(times[1], 0.033333333)
        self.assertEqual(nearest(times, 0.03, 0, times[1]), 0)
        self.assertEqual(nearest(times, times[1], times[1], 0.1), 1)
        self.assertEqual(nearest(times, 0.1, 0, 0.1), 2)

    def test_sample_records_actual_frames_without_claiming_they_were_viewed(self):
        result = sample(self.source, self.work / "inspection", fps=4)
        times = frame_times(self.source)
        self.assertTrue(result["frames"])
        for row in result["frames"]:
            self.assertEqual(row["timestamp_s"], times[row["frame_index"]])
            self.assertTrue((self.work / "inspection" / row["path"]).exists())
        self.assertIn("not a declaration", result["note"])
        self.assertTrue((self.work / "inspection/sheet-001.jpg").exists())

    def test_sampling_does_not_merge_stale_evidence(self):
        output = self.work / "inspection"
        output.mkdir()
        (output / "sheet-001.jpg").write_bytes(b"previous pass")
        with self.assertRaisesRegex(LibraryError, "fresh sampling"):
            sample(self.source, output)
        self.assertEqual((output / "sheet-001.jpg").read_bytes(), b"previous pass")

    def test_extraction_uses_the_same_video_stream_as_metadata(self):
        source = self.work / "two-streams.mp4"
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i",
                        "color=red:size=96x160:rate=10", "-f", "lavfi", "-i", "color=blue:size=192x320:rate=10",
                        "-t", "0.2", "-map", "0:v", "-map", "1:v", "-c:v", "mpeg4", "-an", str(source)], check=True)
        with Image.open(io.BytesIO(extract_frame(source, 0))) as picture:
            self.assertEqual(picture.size, (96, 160))

    def test_draft_assembles_media_and_zip_then_ingests_without_manual_edits(self):
        result = self.build(include_source=True)
        self.assertEqual(result["mode"], "draft-for-chat-review")
        self.assertEqual(result["media_count"], 9)
        self.assertEqual(sha256(Path(result["candidate"]) / "analysis.md"), sha256(self.analysis))
        root = isolated_root(self.work / "isolated-repo")
        outcome = ingest(root, [Path(result["package"])])
        self.assertEqual(outcome["results"][0]["status"], "imported")
        self.assertEqual(check(root)["shots"], 2)

    def test_snapshot_digest_rejects_export_after_content_changes(self):
        digest = sha256(self.analysis)
        self.analysis.write_text(self.analysis.read_text().replace("Synthetic fixture", "Changed fixture"))
        with self.assertRaisesRegex(LibraryError, "changed since chat review"):
            self.build(reviewed_sha256=digest)
        result = self.build(reviewed_sha256=sha256(self.analysis))
        self.assertEqual(result["mode"], "reviewed-export")
        with zipfile.ZipFile(result["package"]) as package:
            self.assertEqual(package.read("audit-sample/analysis.md"), self.analysis.read_bytes())

    def test_regeneration_removes_stale_extras_and_preserves_latest_md(self):
        extras = [{"shot_id": "shot-01", "path": "media/shot-01/detail-01.jpg", "timestamp_s": 0.2, "crop": [0, 0, 20, 30]}]
        first = self.build(extras=extras)
        self.assertEqual(first["media_count"], 10)
        self.analysis.write_text(self.analysis.read_text().replace("raised tub platform", "revised configuration"))
        second = self.build()
        self.assertEqual(second["media_count"], 9)
        self.assertFalse((Path(second["candidate"]) / "media/shot-01/detail-01.jpg").exists())
        with zipfile.ZipFile(second["package"]) as package:
            self.assertNotIn("audit-sample/media/shot-01/detail-01.jpg", package.namelist())
            self.assertIn(b"revised configuration", package.read("audit-sample/analysis.md"))

    def test_regeneration_preserves_unmanaged_user_files(self):
        result = self.build()
        private = Path(result["candidate"]) / "my-notes.txt"
        private.write_text("User notes must be preserved")
        before = sha256(Path(result["candidate"]) / "analysis.md")
        with self.assertRaisesRegex(LibraryError, "Unmanaged files"):
            self.build()
        self.assertEqual(private.read_text(), "User notes must be preserved")
        self.assertEqual(sha256(Path(result["candidate"]) / "analysis.md"), before)

    def test_approximate_overview_timestamp_must_be_corrected_before_review(self):
        self.analysis.write_text(self.analysis.read_text().replace("| overview_timestamp_s | 0 |", "| overview_timestamp_s | 0.01 |", 1))
        with self.assertRaisesRegex(LibraryError, "actual PTS"):
            self.build()
        self.assertFalse((self.work / "candidate/audit-sample").exists())

    def test_input_kit_is_deterministic_nine_files_without_video_or_reference_data(self):
        first = kit_builder.build_bytes()
        self.assertEqual(first, kit_builder.build_bytes())
        target = self.work / "kit.zip"
        target.write_bytes(first)
        with zipfile.ZipFile(target) as archive:
            self.assertEqual(len(archive.namelist()), 9)
            self.assertFalse(any(name.endswith((".mp4", ".wav", ".mp3")) for name in archive.namelist()))
            self.assertFalse(any("pilots/edh001" in name for name in archive.namelist()))
            self.assertIn(b"--reviewed-sha256", archive.read("README.md"))
            self.assertIn(b"tools/audit.py", archive.read("README.md"))

    def test_export_runs_from_unpacked_kit_without_full_repository(self):
        target = self.work / "kit.zip"
        target.write_bytes(kit_builder.build_bytes())
        isolated = self.work / "chat-workspace"
        with zipfile.ZipFile(target) as archive:
            archive.extractall(isolated)
        info = self.work / "audit-info.json"
        info.write_text(json.dumps(self.info))
        command = subprocess.run([sys.executable, str(isolated / "tools/audit.py"), "draft", str(self.source), str(self.analysis),
                                  "--audit-info", str(info), "--output", str(self.work / "portable-output"), "--include-source"],
                                 cwd=isolated, text=True, capture_output=True)
        self.assertEqual(command.returncode, 0, command.stdout + command.stderr)
        result = json.loads(command.stdout)
        self.assertTrue(Path(result["package"]).is_file())
        self.assertEqual(result["analysis_sha256"], sha256(self.analysis))


if __name__ == "__main__":
    unittest.main()
