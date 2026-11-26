"""Snapshot review and immutable export on synthetic media."""
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch
from . import test_prepare
from homeku.audit_session import mark_viewed, add_frames
from homeku.authoring import check_camera, complete, prepare
from homeku.common import LibraryError, dumps, read_json, sha256
from homeku.derivations import referenced_frames
from homeku.exporter import draft, review, export
from homeku.validation import validate_folder
from homeku.render_assets import LAYOUT, TEMPLATE

ROOT = Path(__file__).resolve().parents[1]


class PackageTests(test_prepare.VideoFixture, unittest.TestCase):
    def authored(self, name="normal", *, production_start=None, panel_frames=None):
        source = self.video("camera-" + name)
        prepared = prepare(source, [], self.work / "audit")
        audit = read_json(ROOT / "audit/examples" / name / "audit.json")
        if production_start is not None:
            audit["shots"][0]["composition"]["production_start"] = production_start
        if panel_frames is not None:
            for panel, index in zip(audit["shots"][0]["panels"], panel_frames, strict=True):
                panel["frame_index"] = index
        audit_path, info_path = Path(prepared["audit"]), Path(prepared["audit_info"])
        audit_path.write_text(dumps(audit))
        info_path.write_text(dumps({"method": "Fixture", "limitations": "Synthetic fixture",
                                    "ai": {"provider": "fixture", "model": "fixture", "model_build": None}}))
        selected = {i for p in prepared["passes"] for i in p["record"]["selected_frame_indices"]}
        extra = sorted(set(referenced_frames(audit)) - selected)
        if extra:
            add_frames(prepared["session"], extra, reason="Frame bukti fixture.")
        mark_viewed(prepared["session"], all_frames=True, all_passes=True)
        check_camera(prepared["session"])
        complete(audit_path, session_path=prepared["session"])
        return source, audit_path, read_json(info_path)

    def test_every_reviewed_file_is_exported_byte_for_byte_without_source_or_renderer(self):
        source, audit, logs = self.authored("multi")
        result = draft(source, audit, logs, self.work / "candidates",
                       session_path=audit.with_name("session.json"), purpose="fixture")
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

    def test_clear_panels_roundtrip_without_changing_shot_or_camera(self):
        summary = "Kamera dekat ambang dan menghadap wastafel."
        source, audit_path, logs = self.authored(
            production_start={"frame_index": 4, "composition_summary": summary},
            panel_frames=(0, 5, 10))
        result = draft(source, audit_path, logs, self.work / "candidates",
                       session_path=audit_path.with_name("session.json"), purpose="fixture")
        candidate = Path(result["candidate"])
        checked = review(candidate, self.work / "review.md")
        packaged = export(candidate, self.work / "out", Path(checked["receipt"]))
        with zipfile.ZipFile(packaged["package"]) as archive:
            relative = {name.removeprefix(candidate.name + "/") for name in archive.namelist()}
            self.assertEqual(relative, {"audit.json", "analysis.md", "manifest.json", "media/shot-01.jpg",
                                        "media/overview.jpg", "media/storyboard.jpg"})
        manifest = read_json(candidate / "manifest.json")
        self.assertEqual(manifest["frames"]["4"], .4)
        selections = {p["role"]: p["frame_index"] for p in manifest["selections"]}
        self.assertEqual(selections, {"start": 4, "middle": 5, "end": 10, "overview": 11})
        shot, = read_json(candidate / "audit.json")["shots"]
        original, = read_json(ROOT / "audit/examples/normal/audit.json")["shots"]
        for field in ("start_s", "end_s", "camera"):
            self.assertEqual(shot[field], original[field])
        for media in manifest["media"]:
            if media["kind"] in {"shot-collage", "storyboard"}:
                self.assertEqual([p["selection_id"] for p in media["panels"]],
                                 [p["id"] for p in manifest["selections"] if p["role"] != "overview"])
        self.assertIn("- **Production Start:** F4 · 0.40s · " + summary,
                      (candidate / "analysis.md").read_text())

    def test_draft_binds_the_standard_profile_template(self):
        source, audit, logs = self.authored()
        result = draft(source, audit, logs, self.work / "candidates",
                       session_path=audit.with_name("session.json"), purpose="fixture")
        candidate = Path(result["candidate"])
        manifest_path = candidate / "manifest.json"
        manifest = read_json(manifest_path)
        self.assertEqual(manifest["render"]["template_sha256"], sha256(TEMPLATE))
        self.assertIn("### Palet warna", (candidate / "analysis.md").read_text())
        for fingerprint in ("922902a9b3431f1316ec563de8963371574d6332e9aee7a60b14f9b8038e831c", "a" * 64):
            with self.subTest(fingerprint=fingerprint), self.assertRaisesRegex(LibraryError, "audit profile"):
                manifest["render"]["template_sha256"] = fingerprint
                manifest_path.write_text(dumps(manifest))
                validate_folder(candidate, self.work, require_source=False)

    def test_validation_accepts_canonical_layout_and_rejects_other_hashes(self):
        source, audit, logs = self.authored("multi")
        result = draft(source, audit, logs, self.work / "candidates",
                       session_path=audit.with_name("session.json"), purpose="fixture")
        candidate = Path(result["candidate"])
        manifest_path = candidate / "manifest.json"
        manifest, _, _ = validate_folder(candidate, self.work, require_source=False)
        self.assertEqual(manifest["render"]["layout_sha256"], sha256(LAYOUT))
        for fingerprint in ("d68b9b5a84d6f1c336a5edf4cfa8a1848aa2c77840d503d488e2fcf3fc3ece37", "0" * 64):
            with self.subTest(fingerprint=fingerprint), self.assertRaisesRegex(LibraryError, "Unknown media layout fingerprint"):
                manifest["render"]["layout_sha256"] = fingerprint
                manifest_path.write_text(dumps(manifest))
                validate_folder(candidate, self.work, require_source=False)

    def test_each_payload_change_requires_a_fresh_review(self):
        source, audit, logs = self.authored()
        result = draft(source, audit, logs, self.work / "candidates",
                       session_path=audit.with_name("session.json"), purpose="fixture")
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
        result = draft(source, audit_path, logs, self.work / "candidates",
                       session_path=audit_path.with_name("session.json"), purpose="fixture")
        audit = read_json(audit_path)
        del audit["design"]["size"]["floor_area_m2"]
        audit_path.write_text(dumps(audit))
        with patch("homeku.exporter.cached_media", side_effect=AssertionError("invalid audit rendered")):
            with self.assertRaisesRegex(LibraryError, "floor_area_m2"):
                draft(source, audit_path, logs, self.work / "candidates",
                       session_path=audit_path.with_name("session.json"), purpose="fixture")
        candidate = Path(result["candidate"])
        _, model, _ = validate_folder(candidate, self.work, source_overrides={candidate.name: source})
        self.assertEqual(model["content_sha256"], result["snapshot_sha256"])

    def test_draft_and_complete_block_changed_camera_before_media_render(self):
        source, audit_path, logs = self.authored()
        session = audit_path.with_name("session.json")
        audit = read_json(audit_path)
        audit["shots"][0]["camera"]["description"] = "Hasil kamera telah disunting."
        audit_path.write_text(dumps(audit))
        with self.assertRaisesRegex(LibraryError, "shot-01/camera"):
            complete(audit_path, session_path=session)
        with patch("homeku.exporter.cached_media", side_effect=AssertionError("invalid audit rendered")):
            with self.assertRaisesRegex(LibraryError, "shot-01/camera"):
                draft(source, audit_path, logs, self.work / "blocked", session_path=session, purpose="fixture")
        self.assertFalse((self.work / "blocked" / source.stem).exists())

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
        result = draft(source, audit, logs, output, session_path=audit.with_name("session.json"), purpose="fixture")
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
            draft(source, audit, logs, output, session_path=audit.with_name("session.json"), purpose="fixture")
        self.assertEqual(item.read_text(), "Keep this work")
        item.unlink()
        self.video(source.stem, rate=5)
        with self.assertRaisesRegex(LibraryError, "Source SHA-256"):
            validate()

    def test_legacy_md_and_unknown_packages_are_rejected_without_conversion(self):
        from homeku.validation import extract_package
        package = self.work / "retired-r0001.zip"
        for number, version in enumerate(("1.1", "2.5", "3.0", "9.0")):
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
