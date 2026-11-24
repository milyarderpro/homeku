"""Cache correctness, resource bounds, and full/subset byte parity."""
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch
from . import test_prepare
from homeku.common import LibraryError, read_json
from homeku.media import build_media
from homeku.render_assets import render_config
from homeku.video import extract_frame
from homeku.video_cache import FrameCache, cached_media

ROOT = Path(__file__).resolve().parents[1]


class CacheTests(test_prepare.VideoFixture, unittest.TestCase):
    def test_full_partial_and_warm_media_are_byte_identical(self):
        source = self.video("cache")
        audit = read_json(ROOT / "audit/examples/normal/audit.json")
        cache = FrameCache(source, self.work / "cache")
        config = render_config()
        args = audit, source, cache.info, config, cache.times
        plain = self.work / "plain"
        full = build_media(plain, *args)
        with cache.activate():
            cold = cached_media(self.work / "cold", *args)
            with patch("homeku.media_incremental.render_missing_media",
                       side_effect=AssertionError("warm path must not render")):
                self.assertEqual(cached_media(self.work / "warm", *args), full)
            (next(cache.bucket.glob("media-*.jpg"))).unlink()
            self.assertEqual(cached_media(self.work / "partial", *args), full)
        self.assertEqual(cold, full)
        for path in (row["path"] for row in full):
            self.assertEqual((plain / path).read_bytes(), (self.work / "partial" / path).read_bytes())

    def test_change_only_rendered_dependencies(self):
        source = self.video("correction")
        audit = read_json(ROOT / "audit/examples/normal/audit.json")
        cache = FrameCache(source, self.work / "cache")
        config = render_config()
        with cache.activate():
            baseline = cached_media(self.work / "first", audit, source, cache.info, config, cache.times)
            audit["notes"] = "Koreksi catatan"
            with patch("homeku.media_incremental.render_missing_media",
                       side_effect=AssertionError("notes do not alter media")):
                self.assertEqual(cached_media(self.work / "notes", audit, source,
                                             cache.info, config, cache.times), baseline)
            audit["shots"][0]["camera"]["phases"][0]["notation"] = "Dolly-In + Pan Right"
            updated = cached_media(self.work / "correction", audit, source,
                                   cache.info, config, cache.times)
        self.assertNotEqual(updated[0]["sha256"], baseline[0]["sha256"])
        self.assertEqual(updated[1]["sha256"], baseline[1]["sha256"])
        self.assertNotEqual(updated[2]["sha256"], baseline[2]["sha256"])

    def test_native_batch_bound_retry_and_early_failure(self):
        source = self.video("batch", rate=30, duration=2.4)
        cache = FrameCache(source, self.work / "cache")
        sizes = []
        actual_run = subprocess.run

        def selective_failure(command, *args, **kwargs):
            count = int(command[command.index("-frames:v") + 1])
            sizes.append(count)
            if count > 16:
                raise subprocess.CalledProcessError(1, command, stderr=b"select expression parsing")
            return actual_run(command, *args, **kwargs)

        with patch("homeku.video_cache.subprocess.run", side_effect=selective_failure):
            self.assertEqual(len(cache.extract_many(range(64))), 64)
        self.assertEqual(sizes, [32, 16, 16, 32, 16, 16])
        self.assertEqual(cache.stats["batch_retries"], 2)
        with patch("homeku.video_cache.subprocess.run", side_effect=subprocess.CalledProcessError(
                1, "ffmpeg", stderr=b"damaged source stream")) as run:
            with self.assertRaisesRegex(LibraryError, "damaged source"):
                cache.extract_many(range(64, 70))
            run.assert_called_once()

    def test_canonical_bytes_and_corrupt_cache_recovery(self):
        source = self.video("canonical")
        cache = FrameCache(source, self.work / "cache")
        cache.extract_many([0, 6, 11])
        expected = extract_frame(source, 6)
        self.assertEqual(cache.frame(6), expected)
        (cache.bucket / "canonical-000006.jpg").write_bytes(b"corrupt")
        self.assertEqual(cache.frame(6), expected)
        self.assertEqual(cache.stats["canonical_decodes"], 2)
        with self.assertRaisesRegex(LibraryError, "Cache size limit"):
            FrameCache(source, self.work / "tiny", max_bytes=64)

    def test_changed_source_cannot_use_existing_cache(self):
        source = self.video("changed")
        cache = FrameCache(source, self.work / "cache")
        self.video("changed", rate=5)
        with self.assertRaisesRegex(LibraryError, "Source changed"):
            cache.frame(0)
