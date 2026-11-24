"""Ingest, revision, freshness, and canonical source on isolated fixture roots."""
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from . import test_prepare
from .fixtures.factory import isolated_root, make_package, make_source
from homeku.common import LibraryError, read_json, sha256
from homeku.engine import build, check, ingest, registry_at
from homeku.reader import search


class LibraryTests(test_prepare.VideoFixture, unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.root = isolated_root(self.work / "repo")

    def package(self, rid, **kwargs):
        with tempfile.TemporaryDirectory(dir=self.work) as work:
            return make_package(Path(work), self.root, rid, **kwargs)

    def test_empty_library_has_no_implicit_discovery_and_clears_stale_outputs(self):
        (self.root / "archive").mkdir()
        (self.root / "archive/analysis.md").write_text("Not active")
        (self.root / "data/projections").mkdir()
        (self.root / "data/projections/old.json").write_text("{}")
        self.assertEqual(build(self.root)["references"], 0)
        self.assertEqual(check(self.root)["shots"], 0)
        self.assertFalse((self.root / "data/projections/old.json").exists())

    def test_ingest_replay_and_full_rebuild_preserve_snapshot(self):
        valid = self.package("repeat")
        source = self.root / "video/repeat.mp4"
        initial_source = sha256(source)
        result = ingest(self.root)
        self.assertEqual(result["results"][0]["status"], "imported", result)
        self.assertNotIn("video/repeat.mp4", result["changed"])
        self.assertEqual(ingest(self.root, [valid])["results"][0]["status"], "unchanged")
        self.assertEqual(ingest(self.root, [valid])["changed"], [])
        self.assertEqual(build(self.root, full=True)["changed"], [])
        self.assertEqual(check(self.root)["references"], 1)
        self.assertEqual(sha256(source), initial_source)
        self.assertEqual(search(self.root, area=["kamar mandi"])["total"], 1)

    def test_search_resolves_hyphenated_area_labels(self):
        def label_areas(audit):
            for area, label in zip(audit["areas"], ("living-room", "walk-in-closet"), strict=True):
                area.update(label=label, functions=[label])

        package = self.package("area-aliases", multi=True, edit=label_areas)
        self.assertEqual(ingest(self.root, [package])["results"][0]["status"], "imported")
        for spelling in ("living", "living room", "living-room", "walk-in closet", "walk-in-closet"):
            with self.subTest(spelling=spelling):
                references = search(self.root, area=[spelling])["results"]
                self.assertEqual([reference["id"] for reference in references], ["area-aliases"])
                shots = references[0]["shots"]
                self.assertEqual([shot["shot"] for shot in shots], ["shot-01"])
                self.assertEqual(shots[0]["areas"], ["living-room", "walk-in-closet"])

    def test_bad_supersedes_blocks_revision_and_correct_revision_clears_old_fact(self):
        first = self.package("rev")
        self.assertEqual(ingest(self.root, [first])["results"][0]["status"], "imported")
        old = registry_at(self.root)["references"]["rev"]
        supersedes = {"revision": 1, "content_sha256": old["content_sha256"]}
        bad = self.package("rev", revision=2, supersedes={**supersedes, "content_sha256": "0" * 64},
                           out=self.work / "wrong")
        failed = ingest(self.root, [bad])
        self.assertIn("supersedes", failed["results"][0]["error"])
        self.assertEqual(registry_at(self.root)["references"]["rev"], old)

        def correct(audit):
            audit["shots"][0]["design"][0]["architecture"]["facts"][0]["value"] = "walk-in shower"

        valid = self.package("rev", revision=2, supersedes=supersedes, edit=correct)
        result = ingest(self.root, [valid])
        self.assertEqual(result["results"][0]["revision"], 2, result)
        self.assertEqual(search(self.root, configuration="raised tub platform")["total"], 0)
        self.assertEqual(search(self.root, configuration="walk-in shower")["total"], 1)
        knowledge = [p.read_text() for p in (self.root / "knowledge/comparisons").rglob("page-*.json")]
        self.assertTrue(any("walk-in shower" in text for text in knowledge))
        self.assertFalse(any("raised tub platform" in text for text in knowledge))
        self.assertEqual(check(self.root)["references"], 1)

    def test_duplicate_source_and_canonical_mismatch_are_rejected(self):
        first = self.package("first")
        canonical = self.root / "video/first.mp4"
        shutil.copyfile(canonical, self.root / "video/clone.mp4")
        later = self.package("clone")
        result = ingest(self.root, [first])
        self.assertEqual(result["results"][0]["status"], "imported", result)
        self.assertIn("Duplicate active source", ingest(self.root, [later])["results"][0]["error"])
        unique = self.package("unique")
        path = self.root / "video/unique.mp4"
        make_source(path, stamp="different-bytes")
        digest = sha256(path)
        failed = ingest(self.root, [unique])["results"][0]
        self.assertIn("Source SHA-256 mismatch", failed["error"])
        self.assertEqual(sha256(path), digest)

    def test_valid_batch_item_publishes_when_another_item_fails(self):
        invalid = self.root / "incoming/bad-r0001.zip"
        invalid.write_bytes(b"not a zip")
        valid = self.package("good")
        result = ingest(self.root, [invalid, valid])
        self.assertEqual([row["status"] for row in result["results"]], ["failed", "imported"])
        self.assertEqual(check(self.root)["references"], 1)
        self.assertEqual(ingest(self.root, [invalid])["changed"], [])

    def test_fixture_with_no_marker_cannot_be_ingested(self):
        fixture = self.package("synthetic")
        (self.root / ".homeku-fixture-root").unlink()
        result = ingest(self.root, [fixture])
        self.assertIn("Synthetic fixture rejected", result["results"][0]["error"])
        self.assertEqual(check(self.root)["references"], 0)

    def test_two_importers_share_lock_without_losing_active_entries(self):
        from concurrent.futures import ThreadPoolExecutor
        first, second = [self.package(rid) for rid in ("parallel-a", "parallel-b")]
        with ThreadPoolExecutor(max_workers=2) as pool:
            calls = [pool.submit(ingest, self.root, [p]) for p in (first, second)]
            statuses = [call.result(timeout=30)["results"][0]["status"] for call in calls]
        self.assertEqual(statuses, ["imported", "imported"])
        self.assertEqual(check(self.root)["references"], 2)

    def test_publication_error_rolls_back_and_interruption_recovers(self):
        from unittest.mock import patch
        from homeku.storage import locked, publish
        package = self.package("rollback")
        build(self.root)
        baseline = (self.root / "data/build.json").read_bytes()

        class Interrupted(BaseException):
            pass

        for error in (OSError("injected install failure"), Interrupted()):
            def fault(index, relative):
                if index == 1:
                    raise error

            def broken(root, proposed):
                return publish(root, proposed, after_install=fault)

            with (self.subTest(error=error), patch("homeku.engine.publish", side_effect=broken),
                  self.assertRaises(type(error))):
                ingest(self.root, [package])
            with locked(self.root):
                self.assertEqual((self.root / "data/build.json").read_bytes(), baseline)
            self.assertEqual(check(self.root)["references"], 0)
        self.assertEqual(ingest(self.root, [package])["results"][0]["status"], "imported")
