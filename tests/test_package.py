"""Snapshot review and immutable export on synthetic media."""
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch
from . import test_prepare
from homeku.audit_review import review_changes, reviewed_summary
from homeku.audit_session import mark_viewed, add_frames
from homeku.authoring import check_camera, complete, prepare
from homeku.common import LibraryError, dumps, read_json, sha256
from homeku.derivations import referenced_frames
from homeku.exporter import draft, review, export
from homeku.models import validate_audit
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
        alias = candidate.parent / ".." / candidate.parent.name / candidate.name
        checked = review(alias, self.work / "review.md")
        receipt = read_json(Path(checked["receipt"]))
        self.assertEqual(receipt["candidate"], str(candidate.resolve()))
        self.assertEqual(checked["snapshot_sha256"], result["snapshot_sha256"])
        self.assertFalse(Path(checked["receipt"]).is_relative_to(candidate))
        report = Path(checked["review"])
        self.assertEqual(report.read_bytes(), (self.work / "review.md").read_bytes())
        self.assertIn(str(report.parent / "payload" / candidate.name / "media/storyboard.jpg"), report.read_text())
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

    def test_review_history_compares_distinct_validated_snapshots_in_same_session(self):
        source, audit, logs = self.authored("multi")
        session = audit.with_name("session.json")
        target = self.work / "candidates"
        output = self.work / "review.md"
        initial_audit = read_json(audit)
        initial_audit["shots"][0]["panels"][1]["label"] = "# Stair Landing"
        audit.write_text(dumps(initial_audit))
        first = draft(source, audit, logs, target, session_path=session, purpose="fixture")
        initial = review(Path(first["candidate"]), output, session_path=session)
        initial_sheet = Path(initial["checklist"]).read_text()
        self.assertNotIn("Perubahan sejak", initial_sheet)
        self.assertIn("- Panel # Stair Landing · F4", initial_sheet)
        self.assertTrue(Path(initial["receipt"]).is_file())
        initial_report = Path(initial["review"])
        initial_media = initial_report.parent / "payload" / Path(first["candidate"]).name / "media/shot-01.jpg"
        saved_media = initial_media.read_bytes()
        saved_report = initial_report.read_bytes()
        first_export = export(Path(first["candidate"]), self.work / "exports", initial["receipt"])

        edited = read_json(audit)
        shot = edited["shots"][0]
        phase = shot["camera"]["phases"][0]
        phase["notation"] = phase["notation"].replace("1.3", "1.4")
        phase["evidence"] = [0, 10]
        edited["design"]["house_type"]["evidence"] = [2]
        edited["design"]["palette"][0]["evidence"] = [2]
        shot["area_relations"][0]["evidence"] = [5]
        shot["panels"][1].update(frame_index=5, label="2. [Kitchen]\n> Bay")
        audit.write_text(dumps(edited))
        add_frames(session, [5, 10], reason="Frame perubahan fixture.")
        mark_viewed(session, all_frames=True, all_passes=True)
        check_camera(session, shot_id="shot-01")
        complete(audit, session_path=session)
        valid = draft(source, audit, read_json(audit.with_name("audit-info.json")), target,
                      session_path=session, purpose="fixture")
        candidate = Path(valid["candidate"])
        self.assertNotEqual(first["snapshot_sha256"], valid["snapshot_sha256"])
        current = review(candidate, output, session_path=session)
        sheet = Path(current["checklist"]).read_text()
        for text in ("Perubahan sejak", first["snapshot_sha256"], valid["snapshot_sha256"],
                     "**Notasi**", "**Bukti**", "**Panel**", "**Media berubah**", "media/shot-01.jpg"):
            self.assertIn(text, sheet)
        corrected_label = r"2. \[Kitchen\] \> Bay · F5"
        self.assertIn(f"- Panel {corrected_label}", sheet)
        panel_change = next(line for line in sheet.splitlines() if line.startswith("- **Panel**"))
        self.assertIn("# Stair Landing · F4", panel_change)
        self.assertIn(corrected_label, panel_change)
        self.assertTrue(Path(current["receipt"]).is_file())
        self.assertNotEqual(initial["checklist"], current["checklist"])
        self.assertEqual(Path(initial["checklist"]).read_text(), initial_sheet)
        self.assertEqual(initial_report.read_bytes(), saved_report)
        self.assertEqual(initial_media.read_bytes(), saved_media)
        self.assertNotEqual((candidate / "media/shot-01.jpg").read_bytes(), saved_media)
        self.assertIn(initial_media.as_posix(), initial_sheet)
        self.assertNotIn(initial_media.as_posix(), sheet)
        final = export(candidate, self.work / "exports", current["receipt"])
        self.assertEqual(Path(final["package"]).name, Path(first_export["package"]).name)
        self.assertNotEqual(final["package"], first_export["package"])
        for package in (first_export, final):
            self.assertEqual(sha256(Path(package["package"])), package["package_sha256"])
        self.assertEqual(export(candidate, self.work / "exports", current["receipt"]), final)
        for pointer, before, after in (("/design/house_type", "F0", "F2"),
                                       ("/design/palette/0", "F0", "F2"),
                                       ("/shots/0/area_relations/0", "F4", "F5")):
            self.assertIn(f"**Bukti** `{pointer}` · {before} → {after}", sheet)
        repeated = review(candidate, output, session_path=session)
        self.assertEqual(Path(repeated["checklist"]).read_text(), sheet)

    def test_review_reports_panel_scope_change_with_identical_media(self):
        source, audit_path, logs = self.authored("multi")
        session = audit_path.with_name("session.json")
        target = self.work / "candidates"
        output = self.work / "review.md"
        first = draft(source, audit_path, logs, target, session_path=session, purpose="fixture")
        candidate = Path(first["candidate"])
        review(candidate, output, session_path=session)
        original = read_json(audit_path)
        first_manifest = read_json(candidate / "manifest.json")
        previous = reviewed_summary(original, first_manifest, first["snapshot_sha256"])

        original["shots"][0]["panels"][1]["area_ids"] = ["kitchen-1"]
        audit_path.write_text(dumps(original))
        corrected = draft(source, audit_path, logs, target, session_path=session, purpose="fixture")
        self.assertNotEqual(first["snapshot_sha256"], corrected["snapshot_sha256"])
        manifest = read_json(candidate / "manifest.json")
        self.assertEqual(first_manifest["media"], manifest["media"])
        result = review(candidate, output, session_path=session)
        sheet = Path(result["checklist"]).read_text()
        self.assertIn("**Cakupan area panel** `/shots/0/panels/1` · living-1, kitchen-1 → kitchen-1", sheet)
        self.assertNotIn("cocok pada kedua snapshot", sheet)

        current = reviewed_summary(original, manifest, corrected["snapshot_sha256"])
        del previous["shots"]["shot-01"]["panel_areas"]
        comparison = "\n".join(review_changes(previous, current))
        self.assertIn("Riwayat sebelumnya belum mencatat cakupan area untuk semua panel.", comparison)
        self.assertNotIn("cocok pada kedua snapshot", comparison)

    def test_review_reports_evidence_scope_changes_with_identical_frames(self):
        audit = read_json(ROOT / "audit/examples/multi/audit.json")
        times = [i / 10 for i in range(12)]
        manifest = {"selections": [], "media": []}
        shot = audit["shots"][0]
        phase = shot["camera"]["phases"][0]
        phase.update(area_ids=["living-1"], evidence=[4, 7])
        block = shot["design"][0]
        block["area_ids"].append("kitchen-1")
        fact = block["architecture"]["facts"][0]
        fact.update(area_ids=["living-1"], evidence=[4])
        validate_audit(audit, 1.2, times)
        previous = reviewed_summary(audit, manifest, "old")

        phase["area_ids"] = ["kitchen-1"]
        fact["area_ids"] = ["kitchen-1"]
        validate_audit(audit, 1.2, times)
        current = reviewed_summary(audit, manifest, "new")
        sheet = "\n".join(review_changes(previous, current))
        for pointer in ("/shots/0/camera/phases/0", "/shots/0/design/0/architecture/facts/0"):
            self.assertIn(f"**Cakupan area bukti** `{pointer}` · living-1 → kitchen-1", sheet)
        self.assertNotIn("cocok pada kedua snapshot", sheet)

    def test_session_review_rejects_incomplete_native_provenance(self):
        source, audit, logs = self.authored()
        session = audit.with_name("session.json")
        drafted = draft(source, audit, logs, self.work / "candidates", session_path=session, purpose="fixture")
        candidate = Path(drafted["candidate"])
        report = self.work / "source-reviewed.md"
        checked = review(candidate, report, session_path=session)
        self.assertIn("PTS native, dan deklarasi viewed", Path(checked["checklist"]).read_text())
        fresh = prepare(source, [], self.work / "fresh-session")
        fresh_report = self.work / "fresh-review.md"
        with self.assertRaisesRegex(LibraryError, "frame declarations absent from the supplied session"):
            review(candidate, fresh_report, session_path=fresh["session"])
        self.assertFalse(fresh_report.with_suffix(".md.json").exists())
        manifest_path = candidate / "manifest.json"
        manifest = read_json(manifest_path)
        records = manifest["audit"]["frame_reviews"]
        record, unseen = next((row, index) for row in records for index in row["viewed_frame_indices"]
                              if str(index) not in manifest["frames"])
        record["viewed_frame_indices"].remove(unseen)
        manifest_path.write_text(dumps(manifest))
        offline = review(candidate, self.work / "offline.md")
        self.assertNotIn("PTS native, dan deklarasi viewed", Path(offline["checklist"]).read_text())
        bad_report = self.work / "bad-review.md"
        with self.assertRaisesRegex(LibraryError, "Frame review incomplete"):
            review(candidate, bad_report, session_path=session)
        self.assertFalse(bad_report.with_suffix(".md.json").exists())

    def test_review_reports_override_component_reassignment_with_identical_frames(self):
        audit = read_json(ROOT / "audit/examples/multi/audit.json")
        manifest = {"selections": [], "media": []}
        phase = audit["shots"][0]["camera"]["phases"][0]
        phase["overrides"] = [{"component_index": 0, "evidence": [0, 4]},
                              {"component_index": 1, "evidence": [7, 11]}]
        previous = reviewed_summary(audit, manifest, "old")
        phase["overrides"][0]["component_index"] = 1
        phase["overrides"][1]["component_index"] = 0
        current = reviewed_summary(audit, manifest, "new")

        sheet = "\n".join(review_changes(previous, current))
        self.assertIn("**Komponen override** `/shots/0/camera/phases/0/overrides/0` · Komponen 1 → Komponen 2", sheet)
        self.assertIn("**Komponen override** `/shots/0/camera/phases/0/overrides/1` · Komponen 2 → Komponen 1", sheet)
        self.assertNotIn("cocok pada kedua snapshot", sheet)

        del previous["shots"]["shot-01"]["override_components"]
        old_sheet = "\n".join(review_changes(previous, current))
        self.assertIn("Riwayat sebelumnya belum mencatat komponen yang dirujuk setiap override.", old_sheet)
        self.assertNotIn("cocok pada kedua snapshot", old_sheet)

    def test_review_history_with_partial_evidence_avoids_claiming_a_match(self):
        audit = read_json(ROOT / "audit/examples/multi/audit.json")
        manifest = {"selections": [], "media": []}
        previous = reviewed_summary(audit, manifest, "old")
        del previous["evidence"]
        del previous["shots"]["shot-01"]["evidence"]["/shots/0/area_relations/0"]
        audit["design"]["house_type"]["evidence"] = [2]
        audit["shots"][0]["camera"]["phases"][0]["evidence"] = [0, 10]
        current = reviewed_summary(audit, manifest, "new")
        sheet = "\n".join(review_changes(previous, current))
        self.assertIn("Riwayat sebelumnya hanya mencatat sebagian bukti", sheet)
        self.assertIn("`/shots/0/camera/phases/0` · F0, F11 → F0, F10", sheet)
        self.assertNotIn("area_relations", sheet)
        self.assertNotIn("cocok pada kedua snapshot", sheet)

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
