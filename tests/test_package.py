"""Snapshot review and immutable export on synthetic media."""
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch
from . import test_prepare
from homeku.audit_session import mark_viewed, add_frames
from homeku.authoring import complete, prepare
from homeku.common import LibraryError, dumps, read_json
from homeku.derivations import referenced_frames
from homeku.exporter import draft, review, export
from homeku.validation import validate_folder

ROOT = Path(__file__).resolve().parents[1]


class PackageTests(test_prepare.VideoFixture, unittest.TestCase):
    def authored(self, name="normal"):
        source = self.video("camera-" + name)
        prepared = prepare(source, [], self.work / "audit")
        audit = read_json(ROOT / "audit/examples" / name / "audit.json")
        audit_path, info_path = Path(prepared["audit"]), Path(prepared["audit_info"])
        audit_path.write_text(dumps(audit))
        info_path.write_text(dumps({"method": "Fixture", "limitations": "Synthetic fixture",
                                    "ai": {"provider": "fixture", "model": "fixture", "model_build": None}}))
        selected = {i for p in prepared["passes"] for i in p["record"]["selected_frame_indices"]}
        extra = sorted(set(referenced_frames(audit)) - selected)
        if extra:
            add_frames(prepared["session"], extra, reason="Frame bukti fixture.")
        mark_viewed(prepared["session"], all_frames=True, all_passes=True)
        complete(audit_path, session_path=prepared["session"])
        return source, audit_path, read_json(info_path)

    def test_every_reviewed_file_is_exported_byte_for_byte_without_source_or_renderer(self):
        source, audit, logs = self.authored("multi")
        result = draft(source, audit, logs, self.work / "candidates", purpose="fixture")
        candidate = Path(result["candidate"])
        checked = review(candidate, self.work / "review.md")
        self.assertEqual(checked["snapshot_sha256"], result["snapshot_sha256"])
        self.assertFalse(Path(checked["receipt"]).is_relative_to(candidate))
        self.assertIn(str(candidate / "media/storyboard.jpg"), (self.work / "review.md").read_text())
        source.rename(self.work / "source.offline")
        with (patch("homeku.validation.probe_video", side_effect=AssertionError("export must not probe")),
              patch("homeku.validation.render_report", side_effect=AssertionError("export must not render"))):
            packaged = export(candidate, self.work / "out", Path(checked["receipt"]))
        with zipfile.ZipFile(packaged["package"]) as archive:
            names = {f"{candidate.name}/{p.relative_to(candidate).as_posix()}"
                     for p in candidate.rglob("*") if p.is_file()}
            self.assertEqual(set(archive.namelist()), names)
            for name in names:
                self.assertEqual(archive.read(name), (candidate.parent / name).read_bytes())

    def test_each_payload_change_requires_a_fresh_review(self):
        source, audit, logs = self.authored()
        result = draft(source, audit, logs, self.work / "candidates", purpose="fixture")
        candidate = Path(result["candidate"])
        checked = review(candidate, self.work / "review.md", source)
        for relative in ("audit.json", "analysis.md", "manifest.json", "media/shot-01.jpg",
                         "media/overview.jpg", "media/storyboard.jpg"):
            path = candidate / relative
            original = path.read_bytes()
            path.write_bytes(original + b" ")
            with self.subTest(relative=relative), self.assertRaisesRegex(LibraryError, "changed since"):
                export(candidate, self.work / "out", checked["receipt"])
            path.write_bytes(original)

    def test_invalid_input_fails_before_render_and_preserves_candidate(self):
        source, audit_path, logs = self.authored()
        result = draft(source, audit_path, logs, self.work / "candidates", purpose="fixture")
        audit = read_json(audit_path)
        del audit["design"]["size"]["floor_area_m2"]
        audit_path.write_text(dumps(audit))
        with patch("homeku.exporter.cached_media", side_effect=AssertionError("invalid audit rendered")):
            with self.assertRaisesRegex(LibraryError, "floor_area_m2"):
                draft(source, audit_path, logs, self.work / "candidates", purpose="fixture")
        candidate = Path(result["candidate"])
        _, model, _ = validate_folder(candidate, self.work, source_overrides={candidate.name: source})
        self.assertEqual(model["content_sha256"], result["snapshot_sha256"])

    def test_zip_allowlist_rejects_case_video_nested_traversal_and_duplicate(self):
        import stat
        import warnings
        from homeku.validation import extract_package
        path = self.work / "audit-r0001.zip"
        for name in ("source.mp4", "video/film.MOV", "media/SHOT-01.jpg", "media/shot-01/end.jpg",
                     "media/cache/frame.jpg", "media/../analysis.md", "../analysis.md", "work.json"):
            with self.subTest(name=name):
                with zipfile.ZipFile(path, "w") as archive:
                    archive.writestr("audit/manifest.json", b"{}")
                    archive.writestr("audit/" + name, b"bad")
                with self.assertRaises(LibraryError):
                    extract_package(path, self.work / "unpack")
                self.assertFalse((self.work / "unpack").exists())
        for mode in ("duplicate", "symlink"):
            with self.subTest(mode=mode):
                with zipfile.ZipFile(path, "w") as archive:
                    archive.writestr("audit/manifest.json", b"{}")
                    if mode == "duplicate":
                        with warnings.catch_warnings():
                            warnings.simplefilter("ignore", UserWarning)
                            archive.writestr("audit/manifest.json", b"{}")
                    else:
                        item = zipfile.ZipInfo("audit/audit.json")
                        item.create_system = 3
                        item.external_attr = (stat.S_IFLNK | 0o777) << 16
                        archive.writestr(item, "manifest.json")
                with self.assertRaises(LibraryError):
                    extract_package(path, self.work / "unpack")

    def test_hashes_and_unmanaged_candidates_are_rejected(self):
        source, audit, logs = self.authored()
        output = self.work / "candidates"
        result = draft(source, audit, logs, output, purpose="fixture")
        candidate = Path(result["candidate"])
        overrides = {candidate.name: source}

        def validate():
            validate_folder(candidate, self.work, source_overrides=overrides)

        media = candidate / "media/shot-01.jpg"
        original = media.read_bytes()
        media.write_bytes(original + b" ")
        with self.assertRaisesRegex(LibraryError, "Media SHA-256"):
            validate()
        media.write_bytes(original)
        item = candidate / "work.txt"
        item.write_text("Keep this work")
        with self.assertRaisesRegex(LibraryError, "Unmanaged"):
            draft(source, audit, logs, output, purpose="fixture")
        self.assertEqual(item.read_text(), "Keep this work")
        item.unlink()
        self.video(source.stem, rate=5)
        with self.assertRaisesRegex(LibraryError, "Source SHA-256"):
            validate()

    def test_legacy_md_and_unknown_packages_are_rejected_without_conversion(self):
        from homeku.validation import extract_package
        package = self.work / "retired-r0001.zip"
        for number, version in enumerate(("1.1", "2.5", "9.0")):
            with self.subTest(version=version):
                with zipfile.ZipFile(package, "w") as archive:
                    archive.writestr("retired/manifest.json", dumps({"contract_version": version}))
                    archive.writestr("retired/analysis.md", "# Historical report")
                original = package.read_bytes()
                folder = extract_package(package, self.work / f"extract-{number}")
                with patch("homeku.validation.probe_video", side_effect=AssertionError("old package probed")):
                    with self.assertRaisesRegex(LibraryError, "Unsupported package format.*current HOMEKU kit"):
                        validate_folder(folder, self.work)
                self.assertFalse((folder / "audit.json").exists())
                self.assertEqual(package.read_bytes(), original)
