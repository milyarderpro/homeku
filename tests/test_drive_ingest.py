"""Drive ingest tests with disposable state and a fake Drive transport."""
from collections import Counter
from contextlib import nullcontext, redirect_stdout
from dataclasses import replace
import hashlib
import os
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from zipfile import ZipFile
import unittest

from . import test_prepare
from .fixtures.factory import isolated_root, make_package
from tools.homeku.common import LibraryError, read_json, sha256
from tools.homeku.drive_client import DriveClient, DriveItem, FOLDER
from tools.homeku.drive_ingest import classify, ensure_source, inspect_batch, process_batch, report_batch, scan, stage_zip
from tools.homeku.engine import registry_at, validate_package


class FakeDrive:
    def __init__(self, *items):
        self.items = {item.id: item for item in items}
        self.blobs = {}

    def download(self, item, destination, *, limit=None):
        data = self.blobs[item.id]
        if limit is not None and len(data) > limit:
            raise LibraryError('ZIP terlalu besar')
        destination.write_bytes(data)
        return sha256(destination)

    def metadata(self, file_id):
        return self.items[file_id]

    def children(self, parent_id):
        return [item for item in self.items.values() if item.is_child(parent_id)]


def item(file_id, name, parent=None, mime=FOLDER, **kwargs):
    return DriveItem(file_id, name, mime, (parent,) if parent else (), **kwargs)


class ScanTests(unittest.TestCase):
    def test_uses_only_direct_video_folders_in_homeku_audit(self):
        drive = FakeDrive(
            item("root", "HOMEKU"), item("audit", "Audit", "root"), item("video", "Video", "root"),
            item("foreign", "HOMEKU"), item("elsewhere", "Audit", "foreign"),
            item("room", "Rumah", "audit"), item("sub", "media", "room"),
            item("zip", "rumah-r0001.zip", "room", "application/zip"),
            item("zero", "rumah-r0000.zip", "room", "application/zip"),
            item("flat", "flat-r0001.zip", "audit", "application/zip"),
            item("nested", "nested-r0001.zip", "sub", "application/zip"),
            item("trashed", "trash-r0001.zip", "room", "application/zip", trashed=True),
            item("shortcut", "link-r0001.zip", "room", "application/vnd.google-apps.shortcut"),
            item("md", "analysis.md", "room", "text/markdown"),
            item("fake", "foto-r0001.zip", "room", "image/jpeg"),
        )
        inventory = scan(drive, "root")
        self.assertEqual(inventory.audit.id, "audit")
        self.assertEqual([folder.id for folder in inventory.video_folders], ["video"])
        self.assertEqual([(pkg.file.id, pkg.id, pkg.revision) for pkg in inventory.packages],
                         [("zip", "rumah", 1)])
        drive.items["second"] = item("second", "Audit", "root")
        with self.assertRaisesRegex(LibraryError, "satu folder Audit"):
            scan(drive, "root")

    def test_list_follows_every_page_and_filters_parent_and_trash(self):
        data = lambda file_id, **extra: dict(name=file_id, id=file_id, mimeType=FOLDER, parents=["home"], **extra)
        pages = [{"files": [data("one")], "nextPageToken": "next"},
                 {"files": [data("two"), data("trashed", trashed=True),
                            {**data("outside"), "parents": ["different"]}]}]
        drive = DriveClient(None)
        with patch.object(drive, "request") as request:
            request.return_value.__enter__.return_value.json.side_effect = pages
            self.assertEqual([item.id for item in drive.children("home")], ["one", "two"])
        self.assertEqual(request.call_args.kwargs["params"]["pageToken"], "next")

    def test_incomplete_lists_fail_even_on_a_later_page(self):
        drive = DriveClient(None)
        with patch.object(drive, "request") as request:
            request.return_value.__enter__.return_value.json.side_effect = [
                {"nextPageToken": "second"}, {"incompleteSearch": True}]
            with self.assertRaisesRegex(LibraryError, "belum lengkap"):
                drive.children("home")


class ClassifyTests(unittest.TestCase):
    def test_twenty_results_with_twelve_already_ingested(self):
        packages = [item(f"zip{i}", f"rumah{i:02d}-r0001.zip", "room", "application/zip", sha256=f"{i:064x}")
                    for i in range(20)]
        drive = FakeDrive(item("root", "HOMEKU"), item("audit", "Audit", "root"),
                          item("room", "Rumah", "audit"), *packages)
        registry = {f"rumah{i:02d}": {"revision": 1, "package_sha256": f"{i:064x}"}
                    for i in range(7)}
        ledger = {f"{i:064x}": {"status": "imported", "id": f"rumah{i:02d}", "revision": 1,
                                "package": f"rumah{i:02d}-r0001.zip"}
                  for i in range(7, 12)}
        rows = classify(drive, scan(drive, "root"), registry, ledger, None)
        self.assertEqual(Counter(row.status for row in rows), {"imported": 12, "ready": 8})
        self.assertEqual([row.package.file.id for row in rows if row.status == "ready"],
                         [f"zip{i}" for i in range(12, 20)])

    def test_revisions_and_snapshot_conflicts(self):
        drive = FakeDrive(item("root", "HOMEKU"), item("audit", "Audit", "root"), item("room", "Rumah", "audit"),
                          item("same", "rumah-r0001.zip", "room", "application/zip", sha256="a" * 64),
                          item("next", "rumah-r0002.zip", "room", "application/zip", sha256="b" * 64),
                          item("after", "rumah-r0003.zip", "room", "application/zip", sha256="c" * 64),
                          item("gap", "rumah-r0005.zip", "room", "application/zip", sha256="d" * 64))
        registry = {"rumah": {"revision": 1, "package_sha256": "a" * 64, "content_sha256": "e" * 64}}
        rows = classify(drive, scan(drive, "root"), registry, {}, None)
        self.assertEqual([entry.status for entry in rows], ["imported", "ready", "ready", "blocked"])
        self.assertEqual(rows[2].predecessors, (2,))
        self.assertIn("r0004", rows[-1].reason)

        registry["rumah"]["package_sha256"] = "f" * 64
        with patch("tools.homeku.drive_ingest._inspect_zip", return_value=("a" * 64, "e" * 64)):
            rows = classify(drive, scan(drive, "root"), registry, {}, None)
            self.assertEqual(rows[0].status, "imported")
        with patch("tools.homeku.drive_ingest._inspect_zip", return_value=("a" * 64, "0" * 64)):
            rows = classify(drive, scan(drive, "root"), registry, {}, None)
            self.assertEqual(rows[0].status, "conflict")

    def test_missing_checksum_is_established_from_a_bounded_zip(self):
        drive = FakeDrive(item("root", "HOMEKU"), item("audit", "Audit", "root"), item("room", "Rumah", "audit"),
                          item("valid", "rumah-r0001.zip", "room", "application/zip"),
                          item("bad", "other-r0001.zip", "room", "application/zip"))
        with TemporaryDirectory() as scratch:
            work = Path(scratch)
            payload = work / "rumah-r0001.zip"
            with ZipFile(payload, "w") as archive:
                archive.writestr("rumah/analysis.md", "contoh")
            drive.blobs = {"valid": payload.read_bytes(), "bad": b"damaged"}
            rows = classify(drive, scan(drive, "root"), {}, {}, work)
            self.assertEqual([entry.status for entry in rows], ["blocked", "ready"])
            self.assertEqual(rows[-1].digest, sha256(payload))


class LocalConfigurationTests(unittest.TestCase):
    def test_saved_root_is_used_without_a_flag_and_allows_overrides(self):
        from tools import ingest_drive

        with TemporaryDirectory() as scratch, patch("pathlib.Path.home", return_value=Path(scratch)):
            with patch.dict(os.environ, {}, clear=True):
                self.assertIsNone(ingest_drive.parser().parse_args([]).drive_root)
                with self.assertRaisesRegex(ValueError, "drive-root.id"):
                    ingest_drive.drive_root_id(None)
                config = ingest_drive.config_dir()
                config.mkdir(parents=True)
                (config / "drive-root.id").write_text("saved-root\n", encoding="utf-8")
                self.assertEqual(ingest_drive.drive_root_id(None), "saved-root")
            with patch.dict(os.environ, {"HOMEKU_DRIVE_ROOT_ID": "environment-root"}):
                self.assertEqual(ingest_drive.drive_root_id(ingest_drive.parser().parse_args([]).drive_root),
                                 "environment-root")
                explicit = ingest_drive.parser().parse_args(["--drive-root", "manual-root"])
                self.assertEqual(ingest_drive.drive_root_id(explicit.drive_root), "manual-root")


class ApprovalTests(unittest.TestCase):
    def test_list_abort_and_partial_choice_do_not_write_to_library(self):
        drive = FakeDrive(item("root", "HOMEKU"), item("audit", "Audit", "root"), item("room", "Rumah", "audit"),
                          item("a", "rumah-a-r0001.zip", "room", "application/zip", sha256="a" * 64),
                          item("b", "rumah-b-r0001.zip", "room", "application/zip", sha256="b" * 64))
        with TemporaryDirectory() as scratch:
            work = Path(scratch)
            output = []
            for answers, list_only, expected in (([], True, []), ([""], False, []),
                                                (["1", ""], False, []), (["2", "ya"], False, ["b"])):
                with self.subTest(answers=answers):
                    responses = iter(answers)
                    _, selected = inspect_batch(drive, work, "root", work, list_only=list_only,
                                                read=lambda prompt: next(responses), emit=output.append)
                    self.assertEqual([entry.package.file.id for entry in selected], expected)
                    self.assertFalse((work / "data/registry.json").exists())
                    self.assertFalse((work / "video").exists())
            self.assertIn("Drive b | SHA-256 " + "b" * 64, "\n".join(output))

    def test_following_revision_requires_selecting_predecessor(self):
        drive = FakeDrive(item("root", "HOMEKU"), item("audit", "Audit", "root"), item("room", "Rumah", "audit"),
                          item("a", "rumah-r0001.zip", "room", "application/zip", sha256="a" * 64),
                          item("b", "rumah-r0002.zip", "room", "application/zip", sha256="b" * 64))
        with TemporaryDirectory() as scratch:
            work = Path(scratch)
            responses = iter(["2"])
            with self.assertRaisesRegex(LibraryError, "Pilih rumah-r0001"):
                inspect_batch(drive, work, "root", work, read=lambda prompt: next(responses), emit=lambda line: None)


class TransferTests(unittest.TestCase):
    def setUp(self):
        scratch = TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        self.work = Path(scratch.name)
        self.payload = b"ZIP selected in the snapshot"
        self.digest = hashlib.sha256(self.payload).hexdigest()
        self.drive = FakeDrive(item("root", "HOMEKU"), item("audit", "Audit", "root"),
                               item("room", "Rumah", "audit"), item("zip", "rumah-r0001.zip", "room",
                                    "application/zip", sha256=self.digest))
        self.drive.blobs = {"zip": self.payload}
        self.inventory = scan(self.drive, "root")
        self.entry, = classify(self.drive, self.inventory, {}, {}, self.work)

    def test_download_uses_the_selected_snapshot(self):
        path = stage_zip(self.drive, self.inventory, self.entry, self.work)
        self.assertEqual(path.name, "rumah-r0001.zip")
        self.assertEqual(path.read_bytes(), self.payload)

    def test_same_id_overwrite_and_move_refuse_before_download(self):
        original = self.drive.items["zip"]
        for changed in (replace(original, sha256="c" * 64), replace(original, parents=("another",))):
            with self.subTest(changed=changed), patch.object(self.drive, "download") as download:
                self.drive.items["zip"] = changed
                with self.assertRaisesRegex(LibraryError, "lokasi Drive berubah"):
                    stage_zip(self.drive, self.inventory, self.entry, self.work)
                download.assert_not_called()

    def test_wrong_hash_and_interrupted_transfer_leave_no_staged_zip(self):
        self.drive.blobs["zip"] = b"mismatching bytes"
        with self.assertRaisesRegex(LibraryError, "SHA-256 ZIP berbeda"):
            stage_zip(self.drive, self.inventory, self.entry, self.work)

        def interrupted(item, path, *, limit):
            path.write_bytes(b"part of the download")
            raise LibraryError("Transfer dari Drive terputus.")

        with patch.object(self.drive, "download", side_effect=interrupted):
            with self.assertRaisesRegex(LibraryError, "terputus"):
                stage_zip(self.drive, self.inventory, self.entry, self.work)
        self.assertEqual(list(self.work.iterdir()), [])


class SourceTests(unittest.TestCase):
    def setUp(self):
        scratch = TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        self.work = Path(scratch.name)
        self.video = b"source video bytes"
        self.digest = hashlib.sha256(self.video).hexdigest()
        self.drive = FakeDrive(
            item("root", "HOMEKU"), item("audit", "Audit", "root"), item("video", "Video", "root"),
            item("room", "File Asli", "audit"), item("zip", "rumah-r0001.zip", "room", "application/zip"),
            item("mp4", "File Asli.MP4", "video", "video/mp4"),
        )
        self.drive.blobs = {"mp4": self.video}
        self.inventory = scan(self.drive, "root")
        self.package, = self.inventory.packages
        self.canonical = self.work / "video/rumah.mp4"

    def install(self):
        return ensure_source(self.drive, self.inventory, self.package, self.work, self.digest, self.work)

    def test_local_matching_source_bypasses_drive_and_conflict_preserves_local(self):
        self.canonical.parent.mkdir()
        self.canonical.write_bytes(self.video)
        with patch.object(self.drive, "download") as download:
            self.assertEqual(self.install(), self.canonical)
            self.canonical.write_bytes(b"existing original")
            with self.assertRaisesRegex(LibraryError, "MP4 kanonis lokal berbeda"):
                self.install()
            self.assertEqual(self.canonical.read_bytes(), b"existing original")
            download.assert_not_called()

    def test_source_download_uses_original_name_and_writes_canonical_name(self):
        self.assertEqual(self.install(), self.canonical)
        self.assertEqual(self.canonical.read_bytes(), self.video)

    def test_missing_ambiguous_and_wrong_hash_leave_canonical_absent(self):
        original = self.drive.items.pop("mp4")
        with self.assertRaisesRegex(LibraryError, "tidak ditemukan"):
            self.install()
        self.drive.items["mp4"] = original
        self.drive.blobs["mp4"] = b"other bytes"
        with self.assertRaisesRegex(LibraryError, "berbeda dari manifest"):
            self.install()
        self.drive.items["duplicate"] = replace(original, id="duplicate")
        self.drive.blobs = {"mp4": self.video, "duplicate": self.video}
        with self.assertRaisesRegex(LibraryError, "Lebih dari satu MP4"):
            self.install()
        self.assertFalse(self.canonical.exists())

    def test_source_rechecks_local_file_after_download(self):
        original_download = self.drive.download

        def download_and_create(item, destination, **kwargs):
            digest = original_download(item, destination, **kwargs)
            self.canonical.parent.mkdir()
            self.canonical.write_bytes(b"concurrent source")
            return digest

        with patch.object(self.drive, "download", side_effect=download_and_create):
            with self.assertRaisesRegex(LibraryError, "MP4 kanonis lokal berbeda"):
                self.install()
        self.assertEqual(self.canonical.read_bytes(), b"concurrent source")


class BatchTests(test_prepare.VideoFixture, unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.origin = isolated_root(self.work / "origin")
        self.root = isolated_root(self.work / "local")
        self.drive = FakeDrive(item("root", "HOMEKU"), item("audit", "Audit", "root"), item("video", "Video", "root"))
        self.staging = self.work / "staging"
        self.staging.mkdir()

    def add_package(self, rid, revision=1, *, supersedes=None, damage=False):
        name = f"{rid}-r{revision:04d}"
        path = make_package(self.work / name, self.origin, rid, revision=revision, supersedes=supersedes)
        content = validate_package(self.origin, path)["content_sha256"]
        if damage:
            damaged = self.work / "bad" / path.name
            damaged.parent.mkdir(exist_ok=True)
            with ZipFile(path) as original, ZipFile(damaged, "w") as archive:
                for member in original.namelist():
                    data = b"changed report" if member.endswith("/analysis.md") else original.read(member)
                    archive.writestr(member, data)
            path = damaged
        folder_id = f"folder-{rid}"
        self.drive.items[folder_id] = item(folder_id, f"Asli {rid}", "audit")
        self.drive.items[name] = item(name, path.name, folder_id, "application/zip", sha256=sha256(path))
        video = self.origin / "video" / f"{rid}.mp4"
        self.drive.items[f"video-{rid}"] = item(f"video-{rid}", f"Asli {rid}.mp4", "video",
                                               "video/mp4", sha256=sha256(video))
        self.drive.blobs.update({name: path.read_bytes(), f"video-{rid}": video.read_bytes()})
        return content

    def select(self, *answers, list_only=False):
        responses = iter(answers)
        output = []
        inventory, selected = inspect_batch(self.drive, self.root, "root", self.staging, list_only=list_only,
                                            read=lambda prompt: next(responses), emit=output.append)
        return inventory, selected, output

    def test_mixed_batch_revisions_and_retry(self):
        good = self.add_package("bagus")
        self.add_package("bagus", 2, supersedes={"revision": 1, "content_sha256": good})
        bad = self.add_package("cacat", damage=True)
        self.add_package("cacat", 2, supersedes={"revision": 1, "content_sha256": bad})
        self.add_package("independen")

        inventory, selected, output = self.select("semua", "ya")
        rows = process_batch(self.drive, inventory, selected, self.root, self.staging)
        self.assertEqual([(row["package"], row["status"]) for row in rows],
                         [("bagus-r0001.zip", "imported"), ("bagus-r0002.zip", "imported"),
                          ("cacat-r0001.zip", "failed"), ("cacat-r0002.zip", "pending"),
                          ("independen-r0001.zip", "imported")])
        self.assertIn("analysis.md", rows[2]["error"])
        self.assertIn("Menunggu cacat-r0001.zip", rows[3]["error"])
        self.assertEqual(registry_at(self.root)["references"]["bagus"]["revision"], 2)
        self.assertEqual(report_batch(rows, output.append), 1)
        self.assertIn("3 berhasil, 0 sudah masuk, 1 tertunda, 1 gagal.", "\n".join(output))
        _, _, next_output = self.select(list_only=True)
        self.assertIn("3 sudah masuk, 2 dapat dipilih", next_output[0])


    def test_terminal_list_selection_publication_and_replay(self):
        from tools import ingest_drive

        self.add_package("ambil")
        self.add_package("tunda")
        incoming = self.root / "incoming" / "di-luar-batch-r0001.zip"
        incoming.write_bytes(b"must never reach ingest")
        args = ["--root", str(self.root), "--drive-root", "root"]

        def run(options, answers):
            output = StringIO()
            with (patch("homeku.drive_client.connect", return_value=nullcontext(self.drive)),
                  patch("builtins.input", side_effect=answers) as input_mock,
                  redirect_stdout(output)):
                status = ingest_drive.main(args + options)
            self.assertEqual(input_mock.call_count, len(answers))
            self.assertEqual(status, 0)
            return output.getvalue()

        with patch.object(self.drive, "download", wraps=self.drive.download) as download:
            first = run(["--list"], [])
            self.assertIn("2 dapat dipilih", first)
            self.assertFalse((self.root / "data/registry.json").exists())
            self.assertEqual(list((self.root / "video").iterdir()), [])
            download.assert_not_called()

            result = run([], ["1", "ya"])
            self.assertIn("1 berhasil", result)
            self.assertEqual([call.args[0].id for call in download.call_args_list], ["ambil-r0001", "video-ambil"])
            self.assertEqual(list(registry_at(self.root)["references"]), ["ambil"])
            self.assertEqual(sha256(self.root / "video/ambil.mp4"), sha256(self.origin / "video/ambil.mp4"))
            self.assertFalse((self.root / "video/tunda.mp4").exists())
            ledger = read_json(self.root / "data/ingest.json")["packages"]
            self.assertEqual(list(ledger), [self.drive.items["ambil-r0001"].sha256])
            self.assertEqual(incoming.read_bytes(), b"must never reach ingest")
            self.assertIn("1 sudah masuk, 1 dapat dipilih", run(["--list"], []))
            self.assertEqual(download.call_count, 2)
