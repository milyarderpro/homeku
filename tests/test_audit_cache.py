"""Disposable cache correctness and frozen-image parity."""
import copy
import io
import json
from pathlib import Path
from unittest.mock import patch
from tests.test_audit_authoring import EfficiencyCase
from homeku.common import LibraryError,read_json,dumps,sha256
from homeku.video_cache import FrameCache
from homeku.video import extract_frame,frame_times,probe_video
from homeku.exporter import assemble_v2
from homeku.media_v2_2 import build_media as frozen_media
from homeku.reporting import render_config

class AuditCacheTests(EfficiencyCase):
    def test_batch_pictures_and_canonical_frames_match_original_bytes(self):
        cache=FrameCache(self.source,self.work/"cache");batch=cache.extract_many([0,6,11])
        self.assertEqual(cache.stats["batch_passes"],1)
        for i in batch:self.assertEqual(batch[i],extract_frame(self.source,i))
        with cache.activate():
            for i in batch:self.assertEqual(extract_frame(self.source,i),batch[i])
        self.assertEqual(cache.stats["canonical_decodes"],3)
        with patch("homeku.video._extract_frame_uncached",side_effect=AssertionError("must reuse canonical")):
            with cache.activate():
                for i in batch:extract_frame(self.source,i)
        self.assertEqual(cache.stats["canonical_decodes"],3)
    def test_warm_metadata_and_frames_skip_decode(self):
        cache=FrameCache(self.source,self.work/"cache");cache.frame(6)
        with patch("homeku.video._frame_times_uncached",side_effect=AssertionError("cached PTS")):
            warm=FrameCache(self.source,self.work/"cache")
        with warm.activate():
            self.assertEqual(frame_times(self.source),warm.times);self.assertEqual(probe_video(self.source),warm.info)
            with patch("homeku.video._extract_frame_uncached",side_effect=AssertionError("warm frame")):extract_frame(self.source,6)
        self.assertEqual(warm.stats["canonical_decodes"],0)
    def test_corrupt_frame_rebuilds_and_symlink_is_rejected(self):
        cache=FrameCache(self.source,self.work/"cache");wanted=cache.frame(6)
        (cache.bucket/"canonical-000006.jpg").write_bytes(b"broken")
        self.assertEqual(cache.frame(6),wanted)
        link=self.work/"link";link.symlink_to(self.work/"cache",target_is_directory=True)
        with self.assertRaisesRegex(LibraryError,"Symlink"):FrameCache(self.source,link)
        meta=cache.bucket/"metadata.json";meta.unlink();meta.symlink_to(self.work/"missing")
        with self.assertRaisesRegex(LibraryError,"Symlink"):FrameCache(self.source,self.work/"cache")
    def test_changed_source_invalidates_and_quota_is_enforced(self):
        first=FrameCache(self.source,self.work/"cache")
        other=self.work/self.source.name;other.write_bytes(self.source.read_bytes()+b"unrelated trailing bytes")
        second=FrameCache(other,self.work/"cache")
        self.assertNotEqual(first.bucket,second.bucket)
        with self.assertRaisesRegex(LibraryError,"limit"):FrameCache(self.source,self.work/"tiny",max_bytes=1)
    def test_frozen_media_byte_parity_and_warm_no_render(self):
        path=self.path();frozen=self.work/"frozen";frozen.mkdir()
        cache=FrameCache(self.source,self.work/"cache")
        baseline=frozen_media(frozen,self.audit,self.source,cache.info,render_config(version="2.2.3"))
        d=assemble_v2(self.source,path,self.info,self.work/"candidate",purpose="fixture")
        m=read_json(Path(d["candidate"])/"manifest.json")
        self.assertEqual([p["sha256"] for p in baseline],[p["sha256"] for p in m["media"]])
        with patch("homeku.media_incremental.render_missing_media",side_effect=AssertionError("must reuse images")):
            warm=assemble_v2(self.source,path,self.info,self.work/"candidate",purpose="fixture")
        self.assertEqual(warm["snapshot_sha256"],d["snapshot_sha256"])
        self.assertEqual(warm["cache"]["canonical_decodes"],0)
    def test_metadata_and_fact_edits_reuse_images_but_camera_updates_dependencies(self):
        path=self.path();first=assemble_v2(self.source,path,self.info,self.work/"candidate",purpose="fixture")
        folder=Path(first["candidate"]);old={m["path"]:m["sha256"] for m in read_json(folder/"manifest.json")["media"]}
        a=copy.deepcopy(self.audit);a["shots"][0]["phases"][0]["basis"]+=" A corrected observation basis."
        a["shots"][0]["facts"][0]["basis"]+=" Clarified evidence."
        path.write_text(dumps(a))
        with patch("homeku.media_incremental.render_missing_media",side_effect=AssertionError("unchanged pixels")):
            assemble_v2(self.source,path,self.info,self.work/"candidate",purpose="fixture")
        from homeku.markdown import component
        p=a["shots"][0]["phases"][0];p["components"]+=" toward test-only target"
        p["components_parsed"]=[component(c.strip()) for c in p["components"].split("+")]
        a["shots"][0]["camera_summary"]=p["components"]+".";path.write_text(dumps(a))
        assemble_v2(self.source,path,self.info,self.work/"candidate",purpose="fixture")
        now={m["path"]:m["sha256"] for m in read_json(folder/"manifest.json")["media"]}
        self.assertEqual(old["media/overview.jpg"],now["media/overview.jpg"])
        self.assertNotEqual(old["media/shot-01.jpg"],now["media/shot-01.jpg"])
        self.assertNotEqual(old["media/storyboard.jpg"],now["media/storyboard.jpg"])
    def test_area_label_and_panel_config_invalidate_correct_media(self):
        path=self.path();d=assemble_v2(self.source,path,self.info,self.work/"candidate",purpose="fixture")
        folder=Path(d["candidate"]);old={m["path"]:m["sha256"] for m in read_json(folder/"manifest.json")["media"]}
        a=copy.deepcopy(self.audit);a["areas"][0]["label"]="Bathroom / revised display label";path.write_text(dumps(a))
        assemble_v2(self.source,path,self.info,self.work/"candidate",purpose="fixture",scale=.7)
        now={m["path"]:m["sha256"] for m in read_json(folder/"manifest.json")["media"]}
        self.assertNotEqual(old,now)
    def test_stream_mismatch_and_invalid_batch_are_rejected(self):
        cache=FrameCache(self.source,self.work/"cache")
        with self.assertRaises(LibraryError):cache.frame(0,stream=999)
        for indices in ([],[-1],[999]):
            with self.assertRaises(LibraryError):cache.extract_many(indices)

    def test_source_mutation_during_decode_cannot_poison_cache(self):
        source=self.work/self.source.name;source.write_bytes(self.source.read_bytes())
        cache=FrameCache(source,self.work/"cache")
        original=extract_frame(self.source,6)
        def changed(*args,**kwargs):
            source.write_bytes(source.read_bytes()+b"source changed")
            return original
        with patch("homeku.video._extract_frame_uncached",side_effect=changed):
            with self.assertRaisesRegex(LibraryError,"Source changed"):cache.frame(6)
        self.assertFalse((cache.bucket/"canonical-000006.jpg").exists())
