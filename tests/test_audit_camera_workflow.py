"""2.5 integration; synthetic evidence only and all mutations in temp roots."""
import copy
import io
import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from unittest.mock import patch
from PIL import Image
from jsonschema import Draft202012Validator
from tests.test_camera_notation import CameraCase,set_motion
from tests.fixtures.factory import isolated_root
from homeku.authoring import prepare,complete
from homeku.audit_session import mark_viewed,add_frames
from homeku.common import dumps,read_json,LibraryError,sha256
from homeku.exporter import assemble_v2,review_v2,export_v2
from homeku.reporting import render_config,render_report
from homeku.media import expected_media
from homeku.media_v2_2_1 import build_media as full_media
from homeku.video_cache import FrameCache
from homeku.engine import ingest,check
from homeku.reader import read_reference,search
from homeku.preflight import check_inputs
from homeku.validation import CODE_ROOT

class CameraWorkflowTests(CameraCase):
    def path(self,a):
        p=self.work/"audit.json";p.write_text(dumps(a));return p
    def test_current_schemas_and_golden_reports(self):
        for kind in ("audit","manifest","reference-reader","search-index"):
            Draft202012Validator.check_schema(read_json(CODE_ROOT/f"docs/contracts/{kind}-v2-5.schema.json"))
        for multi,(_,a,_) in self.inputs.items():
            got=render_report(a,render_config(version="2.2.4"))
            golden=CODE_ROOT/f"tests/fixtures/reports/camera-{'multi' if multi else 'normal'}-2.2.4.md"
            self.assertEqual(got,golden.read_text())
            self.assertEqual(sum(v.startswith("## ") for v in got.splitlines()),6)
            self.assertNotIn("scale_measurement",got)
    def test_prepare_complete_optional_angles_and_old_session_guard(self):
        r=prepare(self.source,[],self.work/"work");session=Path(r["session"])
        self.assertEqual(read_json(session)["contract_version"],"2.5")
        a=set_motion(self.audit,"Dolly-In (~1.6×) + Subtle Pan Right")
        a["shots"][0]["phases"][0]["components"]="Dolly-In (~1,6x) + Subtle Pan Right"
        p=Path(r["audit"]);p.write_text(dumps(a));Path(r["audit_info"]).write_text(dumps(self.info))
        mark_viewed(session,all_passes=True,all_frames=True);complete(p,session_path=session)
        got=read_json(p);self.assertEqual(got["shots"][0]["phases"][0]["components"],"Dolly-In (~1.6×) + Subtle Pan Right")
        self.assertTrue(check_inputs(self.source,got,read_json(Path(r["audit_info"])))["ok"])
        got["schema_version"]="2.4";p.write_text(dumps(got))
        with self.assertRaisesRegex(LibraryError,"contracts differ"):complete(p,session_path=session)
    def test_full_workflow_export_ingest_and_qualifier_search(self):
        a=set_motion(self.audit,"Dolly-Out (~1.6×) + Orbit Left + Subtle Pan Right (Ease-Out)")
        path=self.path(a);d=assemble_v2(self.source,path,self.info,self.work/"candidate",purpose="fixture")
        folder=Path(d["candidate"]);m=read_json(folder/"manifest.json")
        self.assertEqual(m["render"]["media"],"2.2.1")
        r=review_v2(folder,self.work/"review.md",self.source)
        self.assertTrue(Path(r["fact_inventory"]).is_file());self.assertFalse(Path(r["fact_inventory"]).is_relative_to(folder))
        with patch("homeku.media.build_media",side_effect=AssertionError("export cannot render")):
            result=export_v2(folder,self.work/"final",r["snapshot_sha256"],self.source)
        with zipfile.ZipFile(result["package"]) as z:
            self.assertEqual(len(z.namelist()),6)
            self.assertFalse(any(v.endswith(".mp4") or "facts.json" in v or "cache" in v for v in z.namelist()))
        root=isolated_root(self.work/"library");(root/"video").mkdir()
        shutil.copyfile(self.source,root/"video"/self.source.name)
        ingest(root,[Path(result["package"])]);self.assertEqual(check(root)["status"],"ok")
        payload=read_reference(root,a["id"],part="full")
        self.assertEqual(payload["reference"]["format_version"],"2.5")
        self.assertEqual(payload["reference"]["shots"][0]["camera_summary"],a["shots"][0]["camera_summary"])
        self.assertEqual(search(root,movement="Pan Right",camera_qualifier="Ease-Out")["total"],1)
        self.assertEqual(search(root,camera_qualifier="Subtle")["total"],1)
        self.assertEqual(search(root,tempo="slow")["total"],0)
        self.assertEqual(ingest(root,[Path(result["package"])])["changed"],[])
    def test_caption_and_subset_cache_match_full_new_engine(self):
        a=set_motion(self.audit,"Dolly-In + Moderate Pan Right")
        config=render_config(version="2.2.4");cache=FrameCache(self.source,self.work/"frames")
        expected=list(expected_media(a,cache.info,config));design=expected[0][2]
        texts=design["texts"]
        self.assertIn("Start",[r["text"] for r in texts])
        self.assertTrue(any(r["text"].startswith(" · ") for r in texts))
        self.assertLess(design["fonts"]["caption_time"].size,design["fonts"]["caption_bold"].size)
        self.assertFalse(any("shot-01 start" in r["text"] for r in texts))
        full=self.work/"full";full.mkdir();baseline=full_media(full,a,self.source,cache.info,config)
        d=assemble_v2(self.source,self.path(a),self.info,self.work/"candidate",purpose="fixture")
        self.assertEqual([p["sha256"] for p in baseline],[p["sha256"] for p in read_json(Path(d["candidate"])/"manifest.json")["media"]])
        with patch("homeku.media_incremental.render_missing_media",side_effect=AssertionError("warm must reuse")):
            warm=assemble_v2(self.source,self.path(a),self.info,self.work/"candidate",purpose="fixture")
        self.assertEqual(warm["cache"]["canonical_decodes"],0)
    def test_multi_area_and_extra_selection_pipeline(self):
        source,a,info=self.inputs[True];r=prepare(source,[],self.work/"multi")
        session=Path(r["session"]);add_frames(session,[4],reason="Synthetic multi-area reveal")
        p=Path(r["audit"]);p.write_text(dumps(a));Path(r["audit_info"]).write_text(dumps(info))
        mark_viewed(session,all_passes=True,all_frames=True);complete(p,session_path=session)
        d=assemble_v2(source,p,read_json(Path(r["audit_info"])),self.work/"candidate",purpose="fixture")
        m=read_json(Path(d["candidate"])/"manifest.json")
        self.assertEqual(len(m["media"][0]["panels"]),4)
        self.assertEqual(len(m["media"][1]["panels"]),2)
    def test_duplicate_content_rejected_without_fact_quota(self):
        a=copy.deepcopy(self.audit);duplicate=copy.deepcopy(a["shots"][0]["facts"][0]);duplicate["id"]="new-duplicate"
        a["shots"][0]["facts"].append(duplicate)
        with self.assertRaisesRegex(LibraryError,"duplicate fact content"):
            assemble_v2(self.source,self.path(a),self.info,self.work/"candidate",purpose="fixture")
    def test_invalid_preflight_does_not_render_and_video_is_forbidden(self):
        path=self.path(self.audit);info=copy.deepcopy(self.info);info["frame_reviews"][0]["mode"]="native"
        with patch("homeku.media.build_media",side_effect=AssertionError("invalid cannot render")):
            with self.assertRaisesRegex(LibraryError,"preflight"):
                assemble_v2(self.source,path,info,self.work/"candidate",purpose="fixture")
        with self.assertRaisesRegex(LibraryError,"forbids"):
            assemble_v2(self.source,path,self.info,self.work/"candidate",include_source=True,purpose="fixture")
    def test_132_batch_bounded_retry_partial_cache_and_fail_fast(self):
        source=self.work/"batch.mp4"
        subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-f","lavfi","-i","testsrc2=size=96x160:rate=30","-t","4.4","-c:v","mpeg4",str(source)],check=True)
        cache=FrameCache(source,self.work/"cache");original=subprocess.run;attempts=[]
        def limited(args,**kw):
            if "-vf" in args:
                count=args[args.index("-vf")+1].count("eq(");attempts.append(count)
                if count>8:raise subprocess.CalledProcessError(244,args,stderr=b"Error while parsing expression for select")
            return original(args,**kw)
        with patch("homeku.video_cache.subprocess.run",side_effect=limited):
            frames=cache.extract_many(list(range(132)))
        self.assertEqual(len(frames),132);self.assertLessEqual(max(attempts),32)
        self.assertGreater(cache.stats["batch_retries"],0)
        calls=cache.stats["ffmpeg_calls"]
        cache.extract_many(list(range(132)));self.assertEqual(cache.stats["ffmpeg_calls"],calls)
        fresh=FrameCache(source,self.work/"other")
        error=subprocess.CalledProcessError(1,[],stderr=b"Permission denied")
        with patch("homeku.video_cache.subprocess.run",side_effect=error) as run:
            with self.assertRaises(LibraryError):fresh.extract_many([0,1])
            self.assertEqual(run.call_count,1)
    def test_portable_default_25_without_optional_dependencies(self):
        from tests.test_audit import kit_builder
        chat=self.work/"chat";chat.mkdir()
        with zipfile.ZipFile(io.BytesIO(kit_builder.build_bytes())) as z:z.extractall(chat)
        def run(*args):
            p=subprocess.run([sys.executable,*map(str,args)],cwd=chat,capture_output=True,text=True)
            self.assertEqual(p.returncode,0,p.stdout+p.stderr);return json.loads(p.stdout)
        run(chat/"homeku_runtime.py","--output",chat)
        cuts=chat/"cuts.json";cuts.write_text("[]")
        prep=run(chat/"tools/audit.py","prepare",self.source,"--cuts-file",cuts,"--output",chat/"work")
        self.assertEqual(read_json(Path(prep["audit"]))["schema_version"],"2.5")
        a=set_motion(self.audit,"Dolly-In + Subtle Pan Right")
        Path(prep["audit"]).write_text(dumps(a));Path(prep["audit_info"]).write_text(dumps(self.info))
        run(chat/"tools/audit.py","mark-viewed",prep["session"],"--all-passes","--all")
        run(chat/"tools/audit.py","complete",prep["audit"],"--session",prep["session"])
        draft=run(chat/"tools/audit.py","draft-v2",self.source,prep["audit"],"--audit-info",prep["audit_info"],"--output",chat/"candidate")
        review=run(chat/"tools/audit.py","review",draft["candidate"],"--source",self.source,"--output",chat/"review.md")
        final=run(chat/"tools/audit.py","export-v2",draft["candidate"],"--source",self.source,"--receipt",review["receipt"],"--output",chat/"final")
        self.assertEqual(final["snapshot_sha256"],draft["snapshot_sha256"])
