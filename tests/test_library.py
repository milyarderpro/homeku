from __future__ import annotations

import copy
import json
import multiprocessing
import shutil
import stat
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from homeku.common import LibraryError, content_hash, dumps, read_json, sha256
from homeku.engine import build, check, ingest, registry_at, validate_package
from homeku.markdown import PHASES, parse
from homeku.storage import locked, publish, recover
from homeku.validation import extract_package, validate_folder
from tests.fixtures.factory import copy_fixture, isolated_root, make_folder, package_folder, table


def concurrent_ingest(root, package, queue):
    try:
        queue.put(ingest(Path(root), [Path(package)]))
    except Exception as error:
        queue.put(str(error))


class LibraryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.shared = tempfile.TemporaryDirectory()
        cls.template = make_folder(Path(cls.shared.name) / "template")

    @classmethod
    def tearDownClass(cls):
        cls.shared.cleanup()

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.work = Path(self.temporary.name)
        self.root = isolated_root(self.work / "repo")
        self.counter = 0

    def tearDown(self):
        self.temporary.cleanup()

    def folder(self, rid="sample", **kwargs):
        self.counter += 1
        return copy_fixture(self.work / f"source-{self.counter}", rid, self.template, **kwargs)

    def package(self, folder, include_source=True):
        manifest = read_json(folder / "manifest.json")
        return package_folder(folder, self.root / "incoming" / f"{folder.name}-r{manifest['revision']:04d}.zip", include_source)

    def active_snapshot(self):
        return {p.relative_to(self.root).as_posix(): sha256(p) for name in ("references", "catalogs", "knowledge", "video", "data/projections")
                for p in (self.root / name).rglob("*") if p.is_file()}

    def test_batch_scans_every_zip_and_excludes_archive_and_unused_video(self):
        for rid in ("sample-a", "sample-b"):
            self.package(self.folder(rid))
        archive = self.root / "archive/oldrepo/references/legacy"
        archive.mkdir(parents=True)
        (archive / "analysis.md").write_text("not a new audit")
        (self.root / "video").mkdir()
        shutil.copyfile(self.template / "source.mp4", self.root / "video/unused.mp4")
        result = ingest(self.root)
        self.assertEqual([r["status"] for r in result["results"]], ["imported", "imported"])
        self.assertEqual(check(self.root)["references"], 2)
        self.assertEqual((archive / "analysis.md").read_text(), "not a new audit")
        self.assertNotIn("legacy", (self.root / "catalogs/references.md").read_text())

    def test_replay_has_no_changes_and_full_build_matches_incremental(self):
        self.package(self.folder())
        ingest(self.root)
        before = self.active_snapshot()
        result = ingest(self.root)
        self.assertEqual(result["results"][0]["status"], "unchanged")
        self.assertEqual(result["changed"], [])
        self.assertEqual(build(self.root, full=True)["changed"], [])
        self.assertEqual(before, self.active_snapshot())

    def test_optional_source_is_bound_to_existing_canonical_bytes(self):
        folder = self.folder()
        (self.root / "video").mkdir()
        shutil.copyfile(folder / "source.mp4", self.root / "video/sample.mp4")
        package = self.package(folder, include_source=False)
        self.assertEqual(validate_package(self.root, package)["id"], "sample")
        self.assertEqual(ingest(self.root)["results"][0]["status"], "imported")
        self.assertFalse((self.root / "references/sample/source.mp4").exists())

    def test_first_revision_cannot_overwrite_an_existing_different_source(self):
        folder = self.folder()
        (self.root / "video").mkdir()
        existing = self.root / "video/sample.mp4"
        existing.write_bytes((self.template / "source.mp4").read_bytes())
        original = sha256(existing)
        self.package(folder)
        result = ingest(self.root)
        self.assertEqual(result["results"][0]["status"], "failed")
        self.assertEqual(sha256(existing), original)

    def test_two_revisions_in_one_batch_can_reuse_new_staged_source(self):
        folder = self.folder()
        initial = content_hash(folder)
        first = self.package(folder)
        revised = self.folder(revision=2, supersedes={"revision": 1, "content_sha256": initial},
                              source_bytes=(folder / "source.mp4").read_bytes(), layout="revised layout")
        self.package(revised, include_source=False)
        result = ingest(self.root)
        self.assertEqual([r["status"] for r in result["results"]], ["imported", "imported"])
        self.assertEqual(registry_at(self.root)["references"]["sample"]["revision"], 2)
        self.assertEqual(check(self.root)["references"], 1)

    def test_revision_replaces_old_variations_without_stale_knowledge(self):
        self.package(self.folder())
        ingest(self.root)
        previous = registry_at(self.root)["references"]["sample"]
        revised = self.folder(revision=2, supersedes={"revision": 1, "content_sha256": previous["content_sha256"]}, layout="sunken bathing court")
        self.package(revised)
        result = ingest(self.root)
        self.assertEqual([r["status"] for r in result["results"]], ["unchanged", "imported"])
        self.assertEqual(check(self.root)["references"], 1)
        knowledge = "\n".join(p.read_text() for p in (self.root / "knowledge").rglob("*.md"))
        self.assertIn("sunken bathing court", knowledge)
        self.assertNotIn("raised tub platform", knowledge)

    def test_revision_conflicts_and_wrong_supersedes_leave_active_outputs_intact(self):
        self.package(self.folder())
        ingest(self.root)
        before = self.active_snapshot()
        for revision, supersedes in ((1, None), (2, {"revision": 1, "content_sha256": "0" * 64})):
            with self.subTest(revision=revision):
                self.package(self.folder(revision=revision, supersedes=supersedes, layout="changed"))
                result = ingest(self.root)
                self.assertTrue(any(r["status"] == "failed" for r in result["results"]))
                self.assertEqual(before, self.active_snapshot())

    def test_valid_and_failed_packages_do_not_block_or_partially_publish_each_other(self):
        self.package(self.folder("good"))
        bad = self.folder("bad")
        (bad / "media/shot-01/start.jpg").write_bytes(b"broken")
        self.package(bad)
        result = ingest(self.root)
        self.assertEqual({r["package"]: r["status"] for r in result["results"]}, {"bad-r0001.zip": "failed", "good-r0001.zip": "imported"})
        self.assertFalse((self.root / "references/bad").exists())
        self.assertEqual(check(self.root)["references"], 1)

    def test_failed_replay_does_not_create_repeated_log_changes(self):
        folder = self.folder()
        path = folder / "media/shot-01/start.jpg"
        Image.new("RGB", (96, 160)).save(path, format="PNG")
        manifest = read_json(folder / "manifest.json")
        next(m for m in manifest["media"] if m["path"] == "media/shot-01/start.jpg")["sha256"] = sha256(path)
        (folder / "manifest.json").write_text(dumps(manifest))
        self.package(folder)
        first = ingest(self.root)
        second = ingest(self.root)
        self.assertEqual(first["results"][0]["status"], "failed")
        self.assertEqual(first["results"], second["results"])
        self.assertEqual(second["changed"], [])

    def test_duplicate_sources_are_rejected(self):
        first = self.folder("first")
        self.package(first)
        self.package(self.folder("second", source_bytes=(first / "source.mp4").read_bytes()))
        result = ingest(self.root)
        self.assertEqual([r["status"] for r in result["results"]], ["imported", "failed"])
        self.assertIn("Duplicate active source", result["results"][1]["error"])

    def test_case_colliding_ids_are_rejected(self):
        for rid in ("Sample", "sample"):
            self.package(self.folder(rid))
        result = ingest(self.root)
        self.assertEqual([r["status"] for r in result["results"]], ["imported", "failed"])

    def test_fixture_is_rejected_in_production_root(self):
        (self.root / ".homeku-fixture-root").unlink()
        self.package(self.folder())
        result = ingest(self.root)
        self.assertEqual(result["results"][0]["status"], "failed")
        self.assertEqual(registry_at(self.root)["references"], {})

    def test_invalid_media_coverage_source_and_md_are_rejected(self):
        mutations = {
            "source hash": lambda m: m["source"].update(sha256="0" * 64),
            "source metadata": lambda m: m["source"].update(width=100),
            "time outside shot": lambda m: m["media"][1].update(timestamp_s=0.8),
            "storyboard order": lambda m: m["media"][0]["derived_from"].reverse(),
            "coverage gap": lambda m: m["audit"]["reviewed_ranges"][0].update(start_s=0.2),
            "missing media": lambda m: m["media"].pop(),
            "duplicate media": lambda m: m["media"].append(copy.deepcopy(m["media"][1])),
        }
        for label, change in mutations.items():
            with self.subTest(label=label):
                folder = self.folder()
                manifest = read_json(folder / "manifest.json")
                change(manifest)
                (folder / "manifest.json").write_text(dumps(manifest))
                with self.assertRaises(LibraryError):
                    validate_folder(folder, self.root)
        for old, new in (("| id | sample |", "| id | other |"), ("| tempo", "| wrong"),
                         ("Dolly-Out (~1.3×).", "Dolly-In (~1.3×)."), ("| end |", "| unknown |")):
            folder = self.folder()
            path = folder / "analysis.md"
            text = path.read_text()
            if old == "| tempo":
                old, new = "| anchor | tempo |", "| anchor | wrong |"
            if old not in text:
                continue
            path.write_text(text.replace(old, new))
            with self.assertRaises(LibraryError):
                validate_folder(folder, self.root)

    def test_zip_traversal_special_files_duplicates_and_executables(self):
        for index, (name, mode, duplicate) in enumerate((
                ("../escape", 0o100644, False), ("/escape", 0o100644, False),
                ("sample/analysis.md", stat.S_IFLNK | 0o777, False),
                ("sample/analysis.md", 0o100755, False), ("sample/analysis.md", 0o100644, True),
                ("sample/media/shot-01/motion/frame.jpg", 0o100644, False))):
            package = self.work / "sample-r0001.zip"
            with zipfile.ZipFile(package, "w") as archive:
                info = zipfile.ZipInfo(name)
                info.external_attr = mode << 16
                archive.writestr(info, "payload")
                if duplicate:
                    archive.writestr("sample/ANALYSIS.md", "duplicate")
            with self.subTest(name=name), self.assertRaises(LibraryError):
                extract_package(package, self.work / f"extracted-{index}")
        self.assertFalse((self.work / "escape").exists())

    def test_unknown_labels_and_nonpositive_claims_are_preserved(self):
        folder = self.folder()
        path = folder / "analysis.md"
        path.write_text(path.read_text().replace("bathroom; laundry", "Kamar mandi; laundry; courtyard-nook"))
        self.package(folder)
        ingest(self.root)
        rooms = (self.root / "catalogs/rooms/README.md").read_text()
        self.assertIn("bathroom", rooms)
        self.assertIn("courtyard-nook", rooms)
        comparison = "\n".join(p.read_text() for p in (self.root / "knowledge").rglob("*.md"))
        self.assertIn("not-visible", comparison)
        self.assertIn("unknown", comparison)
        self.assertNotIn("| vanity cabinet | observed |", comparison)
        self.assertEqual(check(self.root)["shots"], 2)

    def test_three_camera_notations_round_trip(self):
        examples = ["Orbit Right (~15°–20°) →\nAccelerating Dolly-In (~2×) toward teak entrance door.",
                    "Dolly-In (~1.3×) +\nOrbit Left + strong Pan Right (~35°).",
                    "Dolly-In (~2×) +\ngentle Pan Right (~15°)."]
        for index, summary in enumerate(examples):
            folder = self.folder(f"camera-{index}")
            path = folder / "analysis.md"
            text = path.read_text()
            original = "Dolly-In (~1.3×) + gentle Pan Right (~15°)."
            text = text.replace(original, summary, 1)
            old_phase = table(PHASES, [("phase-01", 0.0, 0.6, original[:-1], "subjek fixture", "moderate", "constant",
                "Angka adalah contoh sintaks fixture, bukan pengukuran kamera.", "[awal](media/shot-01/start.jpg); [akhir](media/shot-01/end.jpg)", "low", "Simulasi kontrak, bukan audit gerakan.")])
            clauses = summary.split("→")
            new_rows = []
            for n, clause in enumerate(clauses):
                new_rows.append((f"phase-{n+1:02d}", n * 0.6 / len(clauses), (n+1) * 0.6 / len(clauses), " ".join(clause.strip().rstrip(".").split()),
                                 "door", "fast", "accelerating" if "Accelerating" in clause else "constant", "Basis visual fixture; estimasi.",
                                 "[awal](media/shot-01/start.jpg); [akhir](media/shot-01/end.jpg)", "low", "Fixture."))
            self.assertIn(old_phase, text)
            text = text.replace(old_phase, table(PHASES, new_rows), 1)
            path.write_text(text)
            parsed = parse(text)
            self.assertEqual(parsed["shots"][0]["camera_summary"], summary)
            self.package(folder)
        result = ingest(self.root)
        self.assertTrue(all(r["status"] == "imported" for r in result["results"]), result)
        camera = "\n".join(p.read_text() for p in (self.root / "catalogs/camera").rglob("*.md"))
        self.assertIn("~15°–20°", camera)
        self.assertIn("strong Pan Right (~35°)", camera)
        self.assertIn("fast", camera)
        self.assertIn("→", camera)
        self.assertIn("+", camera)

    def test_boundary_overview_rule_requires_explanation_for_exception(self):
        folder = self.folder()
        path = folder / "analysis.md"
        text = path.read_text().replace("Dolly-In (~1.3×) + gentle Pan Right (~15°)", "Dolly-Out (~1.3×)")
        path.write_text(text)
        with self.assertRaisesRegex(LibraryError, "overview exception"):
            validate_folder(folder, self.root)
        path.write_text(text.replace("| overview_exception | - |", "| overview_exception | Oklusi pada akhir; awal lebih jelas. |", 1))
        validate_folder(folder, self.root)

    def test_failed_preparation_does_not_replace_previous_revision(self):
        self.package(self.folder())
        ingest(self.root)
        previous = registry_at(self.root)["references"]["sample"]
        revised = self.folder(revision=2, supersedes={"revision": 1, "content_sha256": previous["content_sha256"]}, layout="new layout",
                              source_bytes=(self.root / "video/sample.mp4").read_bytes() + (8).to_bytes(4, "big") + b"free")
        self.package(revised)
        before = self.active_snapshot()
        real_copy = shutil.copyfile
        def fail_source_copy(source, destination, *args, **kwargs):
            if "/prepared-" in str(destination) and "/video/" in str(destination):
                raise OSError("simulated source staging failure")
            return real_copy(source, destination, *args, **kwargs)
        with patch("homeku.engine.shutil.copyfile", side_effect=fail_source_copy):
            result = ingest(self.root)
        self.assertTrue(any(r["status"] == "failed" for r in result["results"]))
        self.assertEqual(before, self.active_snapshot())
        self.assertEqual(check(self.root)["references"], 1)

    def test_cache_edits_are_rebuilt_and_unapproved_audit_edits_rejected(self):
        self.package(self.folder())
        ingest(self.root)
        cache = self.root / "data/projections/sample.json"
        value = read_json(cache)
        value["reference"]["title"] = "cache corruption"
        cache.write_text(dumps(value))
        build(self.root)
        self.assertNotEqual(read_json(cache)["reference"]["title"], "cache corruption")
        path = self.root / "references/sample/analysis.md"
        path.write_text(path.read_text() + "\nUnapproved edit\n")
        with self.assertRaisesRegex(LibraryError, "Unapproved edits"):
            build(self.root)

    def test_publication_error_rolls_back_and_crash_is_recoverable(self):
        build(self.root)
        original = (self.root / "catalogs/README.md").read_bytes()
        proposal = self.work / "replacement"
        proposal.mkdir()
        (proposal / "README.md").write_text("new catalogs")
        def fail(index, relative):
            raise OSError("simulated publication error")
        with locked(self.root), self.assertRaises(OSError):
            publish(self.root, {"catalogs": proposal}, after_install=fail)
        self.assertEqual((self.root / "catalogs/README.md").read_bytes(), original)
        class Crash(BaseException):
            pass
        def crash(index, relative):
            raise Crash()
        with self.assertRaises(Crash), locked(self.root):
            publish(self.root, {"catalogs": proposal}, after_install=crash)
        self.assertTrue((self.root / ".homeku/transaction.json").exists())
        with self.assertRaisesRegex(LibraryError, "Pending transaction"):
            check(self.root)
        with locked(self.root):
            pass
        self.assertEqual((self.root / "catalogs/README.md").read_bytes(), original)
        check(self.root)

    def test_concurrent_importers_preserve_both_uploads(self):
        packages = [self.package(self.folder(rid)) for rid in ("parallel-a", "parallel-b")]
        context = multiprocessing.get_context("fork")
        queue = context.Queue()
        processes = [context.Process(target=concurrent_ingest, args=(str(self.root), str(package), queue)) for package in packages]
        for process in processes:
            process.start()
        for process in processes:
            process.join(30)
            self.assertEqual(process.exitcode, 0)
        results = [queue.get(timeout=5), queue.get(timeout=5)]
        self.assertTrue(all(isinstance(r, dict) for r in results), results)
        self.assertEqual(check(self.root)["references"], 2)

    def test_300_reference_capacity_and_full_rebuild_equivalence(self):
        for index in range(300):
            self.package(self.folder(f"scale-{index:03d}", layout=f"configuration {index % 17}"))
        result = ingest(self.root)
        self.assertEqual(sum(r["status"] == "imported" for r in result["results"]), 300)
        self.assertEqual(check(self.root), {"references": 300, "shots": 600, "status": "ok"})
        self.assertEqual(build(self.root)["changed"], [])
        for path in (self.root / "catalogs").rglob("page-*.md"):
            self.assertLessEqual(sum(line.startswith("| ") for line in path.read_text().splitlines()), 42)
        self.assertEqual(len(read_json(self.root / "data/search-index.json")["references"]), 300)


if __name__ == "__main__":
    unittest.main()
