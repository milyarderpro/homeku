"""Strict2.2 regression tests; every video and audit below is synthetic."""
import copy
import io
import shutil
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch
from jsonschema import Draft202012Validator
from tests.fixtures.factory import make_v2_inputs, isolated_root, package_folder
from homeku.common import LibraryError, read_json, dumps, snapshot_hash
from homeku.models import validate_audit
from homeku.reporting import render_report, render_config
from homeku.report_validation import validate_report
from homeku.validation import validate_frame_reviews, validate_folder, probe_video, CODE_ROOT
from homeku.video import frame_times, selected_indices
from homeku.audit_quality import validate_viewed_evidence
from homeku.exporter import assemble_v2, export_v2, review_v2
from homeku.engine import ingest, check
from homeku.reader import read_reference, search


class AuditQualityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.shared = tempfile.TemporaryDirectory()
        cls.inputs = {}
        for multi in (False, True):
            source, path, info = make_v2_inputs(Path(cls.shared.name)/str(multi),
                rid="quality-multi" if multi else "quality-normal", multi=multi, version="2.2")
            cls.inputs[multi] = (source, read_json(path), info)
    @classmethod
    def tearDownClass(cls):
        cls.shared.cleanup()
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.work = Path(self.temp.name)
        self.source, audit, info = self.inputs[False]
        self.audit, self.info = copy.deepcopy(audit), copy.deepcopy(info)
        self.times = frame_times(self.source)
    def tearDown(self):
        self.temp.cleanup()
    def test_schemas_and_dispatch(self):
        for kind in ("audit", "manifest", "reference-reader", "search-index"):
            Draft202012Validator.check_schema(read_json(CODE_ROOT/f"docs/contracts/{kind}-v2-2.schema.json"))
        validate_audit(self.audit, 1.2, self.times)
        bad = copy.deepcopy(self.audit); bad["schema_version"] = "999"
        with self.assertRaisesRegex(LibraryError,"Unsupported"):validate_audit(bad)
        with self.assertRaises(LibraryError):render_report(self.audit,render_config(version="2.2.0"))
    def test_full_report_golden_normal_and_multi(self):
        for multi, (_, a, _) in self.inputs.items():
            got = render_report(a,render_config(version="2.2.1"))
            golden = CODE_ROOT/f"tests/fixtures/reports/quality-{'multi' if multi else 'normal'}-2.2.1.md"
            self.assertEqual(got,golden.read_text())
            self.assertNotIn("fact_coverage",got);self.assertNotIn("motion_observations",got)
            self.assertIn("**60–90 m²**",got)
    def test_plain_text_cannot_add_report_structure(self):
        for value in ("Kamera maju.\n\n## 7. Tambahan","# Extra heading","<table>bad</table>",
                      "| x | y |",chr(96)*3+"text","- item"):
            a = copy.deepcopy(self.audit);a["shots"][0]["camera_simple"] = value
            with self.assertRaises(LibraryError):validate_audit(a)
            with self.assertRaises(LibraryError):render_report(a,render_config(version="2.2.1"))
    def test_inline_markup_is_plain_and_does_not_mutate_source(self):
        a=copy.deepcopy(self.audit);a["shots"][0]["camera_simple"]="Kamera menuju kabinet [A] dan *aksen*."
        before=copy.deepcopy(a);text=render_report(a,render_config(version="2.2.1"))
        self.assertIn(r"\[A\]",text);self.assertIn(r"\*aksen\*",text);self.assertEqual(a,before)
    def test_independent_structure_checker_rejects_damage(self):
        text=render_report(self.audit,render_config(version="2.2.1"))
        for broken in (text+"\n## 7. Extra\n",text.replace("#### **B.","#### **D."),
                       text.replace("**Arsitektur**","**Other**"),
                       text.replace("media/shot-01.jpg","media/missing.jpg"),
                       text.replace("| Duration |","| Extra | Duration |")):
            with self.assertRaises(LibraryError):validate_report(broken,self.audit)
    def test_scale_style_and_identity_consistency(self):
        mutations=[
            lambda a:a["size"].update(scale="Small (rumah mungil)"),
            lambda a:a["profile"].append({**a["profile"][0],"id":"style-extra","aspect":"style-influence","value":"English Country Cottage; Mediterranean Cottage"}),
            lambda a:a["identity"].update(interior_style="Different style"),
            lambda a:a["identity"].update(influences="Different influence")]
        for mutate in mutations:
            a=copy.deepcopy(self.audit);mutate(a)
            with self.assertRaises(LibraryError):validate_audit(a)
    def test_fact_coverage_empty_facts_unknown_ids_and_area_scope(self):
        a=copy.deepcopy(self.audit);a["shots"][0]["facts"]=[]
        with self.assertRaisesRegex(LibraryError,"fact IDs"):validate_audit(a)
        a=copy.deepcopy(self.inputs[True][1])
        a["shots"][0]["design"][1]["fact_coverage"]["architecture"]["fact_ids"]=["f-01"]
        with self.assertRaisesRegex(LibraryError,"area"):validate_audit(a)
        a=copy.deepcopy(self.audit)
        a["shots"][0]["design"][0]["fact_coverage"]["environment"]["fact_ids"]=["f-01"]
        with self.assertRaisesRegex(LibraryError,"unresolved"):validate_audit(a)
    def test_motion_proofs_and_estimates(self):
        for mutate in [
            lambda p:p.update(evidence=["p-start"]),
            lambda p:p["motion_observations"][0].update(evidence=["p-start"]),
            lambda p:p["motion_observations"][0].update(evidence=["p-start","frame:shot-01:0"]),
            lambda p:p["motion_observations"][0].update(estimate_basis=None),
            lambda p:p["motion_observations"][0].update(alternatives=None)]:
            a=copy.deepcopy(self.audit);mutate(a["shots"][0]["phases"][0])
            with self.assertRaises(LibraryError):validate_audit(a,times=self.times)
    def test_evidence_must_have_been_declared_viewed(self):
        reviews=copy.deepcopy(self.info["frame_reviews"]);reviews[0]["viewed_frame_indices"].remove(2)
        with self.assertRaisesRegex(LibraryError,"not declared viewed"):
            validate_viewed_evidence(self.audit,reviews,self.times)
    def test_later_phase_cannot_use_only_early_evidence(self):
        a=copy.deepcopy(self.audit);s=a["shots"][0];p=s["phases"][0]
        first=copy.deepcopy(p);first.update(end_s=.6,evidence=["p-start","frame:shot-01:5"],tempo="moderate")
        for o in first["motion_observations"]:o["evidence"]=first["evidence"]
        later=copy.deepcopy(p);later.update(phase="phase-02",start_s=.6,tempo="fast",evidence=["p-start","frame:shot-01:1"])
        for o in later["motion_observations"]:o["evidence"]=later["evidence"]
        s["phases"]=[first,later];s["camera_summary"]=" → ".join(p["components"] for p in s["phases"])
        with self.assertRaisesRegex(LibraryError,"outside phase"):validate_audit(a,times=self.times)
    def test_tempo_uniform_and_variable_consistency(self):
        a=copy.deepcopy(self.audit);a["shots"][0]["phases"][0]["tempo"]="slow"
        with self.assertRaisesRegex(LibraryError,"tempo conflicts"):validate_audit(a)
        a["shots"][0]["tempo_profile"]=[{"start_s":0,"end_s":1.2,"tempo":"fast","description":"Cepat"}]
        a["shots"][0]["phases"][0]["tempo"]="fast";validate_audit(a)
    def test_low_sampling_cannot_replace_baseline(self):
        reviews=copy.deepcopy(self.info["frame_reviews"]);r=reviews[0];r["sampling_fps"]=1
        indices=list(selected_indices(self.times,0,1.2,1,source_fps=10))
        r["selected_frame_indices"]=indices;r["viewed_frame_indices"]=indices
        with self.assertRaisesRegex(LibraryError,"10 FPS"):
            validate_frame_reviews(reviews,self.audit["shots"],self.source,probe_video(self.source),strict=True)
        validate_frame_reviews(reviews+self.info["frame_reviews"],self.audit["shots"],self.source,probe_video(self.source),strict=True)
        validate_frame_reviews(reviews,self.audit["shots"],self.source,probe_video(self.source))
    def test_low_native_fps_and_baseline_gap(self):
        source=self.work/"low.mp4"
        subprocess.run(["ffmpeg","-loglevel","error","-y","-f","lavfi","-i",
            "testsrc2=size=96x160:rate=5","-t","1.2","-c:v","mpeg4",str(source)],check=True)
        times=frame_times(source);info=probe_video(source);indices=list(range(len(times)))
        r={"shot_id":"shot-01","start_s":0,"end_s":1.2,"mode":"sampling","sampling_fps":10,
           "selected_frame_indices":indices,"viewed_frame_indices":indices,"reason":"Synthetic"}
        validate_frame_reviews([r],self.audit["shots"],source,info,strict=True)
        r["start_s"]=.2;r["selected_frame_indices"]=r["viewed_frame_indices"]=list(selected_indices(times,.2,1.2,10,source_fps=5))
        with self.assertRaisesRegex(LibraryError,"gap"):validate_frame_reviews([r],self.audit["shots"],source,info,strict=True)
    def test_roundtrip_without_video_and_forbidden_video(self):
        path=self.work/"audit.json";path.write_text(dumps(self.audit))
        with self.assertRaisesRegex(LibraryError,"forbids"):
            assemble_v2(self.source,path,self.info,self.work/"bad",include_source=True,purpose="fixture")
        result=assemble_v2(self.source,path,self.info,self.work/"candidate",purpose="fixture")
        folder=Path(result["candidate"]);manifest=read_json(folder/"manifest.json")
        self.assertEqual((manifest["render"]["report"],manifest["render"]["media"]),("2.2.1","2.2.0"))
        self.assertFalse((folder/"source.mp4").exists());shutil.copyfile(self.source,folder/"source.mp4")
        with self.assertRaisesRegex(LibraryError,"forbids video"):
            validate_folder(folder,self.work,source_overrides={self.audit["id"]:self.source})
        (folder/"source.mp4").unlink()
        reviewed=review_v2(folder,self.work/"review.md",self.source)
        with patch("homeku.media.build_media",side_effect=AssertionError("Do not rerender export")):
            package=export_v2(folder,self.work/"packages",read_json(Path(reviewed["receipt"]))["snapshot_sha256"],self.source)
        with zipfile.ZipFile(package["package"]) as z:self.assertFalse(any(n.lower().endswith(".mp4") for n in z.namelist()))
        root=isolated_root(self.work/"repo");(root/"video").mkdir()
        shutil.copyfile(self.source,root/"video"/self.source.name)
        outcome=ingest(root,[Path(package["package"])])
        self.assertEqual(outcome["results"][0]["status"],"imported",outcome)
        self.assertEqual(check(root)["references"],1);self.assertEqual(search(root,scale="small")["total"],1)
        data=read_reference(root,self.audit["id"],part="shot",shot="shot-01")
        self.assertIn("fact_coverage",data["shot"]["design"][0])
        self.assertTrue(any("motion_observations" in p for p in data["provenance"]))
        self.assertEqual(read_json(root/"data/registry.json")["references"][self.audit["id"]]["content_sha256"],snapshot_hash(folder))
    def test_current_kit_in_clean_workspace(self):
        from tests.test_audit import kit_builder
        chat=self.work/"chat";chat.mkdir()
        with zipfile.ZipFile(io.BytesIO(kit_builder.build_bytes())) as z:z.extractall(chat)
        def run(*args):
            p=subprocess.run([sys.executable,*map(str,args)],cwd=chat,capture_output=True,text=True)
            self.assertEqual(p.returncode,0,p.stdout+p.stderr);return json.loads(p.stdout)
        run(chat/"homeku_runtime.py","--output",chat)
        a=self.work/"audit.json";a.write_text(dumps(self.audit))
        info=self.work/"info.json";info.write_text(dumps(self.info))
        draft=run(chat/"tools/audit.py","draft-v2",self.source,a,"--audit-info",info,"--output",self.work/"portable")
        review=run(chat/"tools/audit.py","review",draft["candidate"],"--source",self.source,"--output",self.work/"portable-review.md")
        package=run(chat/"tools/audit.py","export-v2",draft["candidate"],"--source",self.source,
                    "--receipt",review["receipt"],"--output",self.work/"portable-packages")
        self.assertEqual(package["snapshot_sha256"],draft["snapshot_sha256"])

    def test_conflicting_primary_style_and_decelerating_tempo_are_rejected(self):
        a=copy.deepcopy(self.audit)
        a["profile"].append({**a["profile"][0],"id":"other-primary","value":"Different style"})
        with self.assertRaisesRegex(LibraryError,"one matching"):validate_audit(a)
        from homeku.markdown import component
        a=copy.deepcopy(self.audit);s=a["shots"][0];p=s["phases"][0]
        p["components"]="Decelerating "+p["components"]
        p["components_parsed"]=[component(v.strip()) for v in p["components"].split("+")]
        s["camera_summary"]=p["components"]
        with self.assertRaisesRegex(LibraryError,"Decelerating"):validate_audit(a)
    def test_inline_table_labels_keep_visible_characters(self):
        a=copy.deepcopy(self.audit);a["areas"][0]["label"]="Bath_[A] | Laundry"
        report=render_report(a,render_config(version="2.2.1"))
        row=next(v for v in report.splitlines() if v.startswith("| 01 |"))
        self.assertIn(r"Bath\_\[A\] \| Laundry",row)
        self.assertNotIn(r"Bath\\_",row)
        validate_report(report,a)
    def test_multi_area_style_search_and_video_ingest_rejection(self):
        source,a,info=self.inputs[True];a=copy.deepcopy(a)
        names=["English Country Cottage","Mediterranean Cottage"]
        for i,name in enumerate(names):
            a["profile"].append({**a["profile"][0],"id":f"influence-{i}",
                                 "aspect":"style-influence","value":name})
        a["identity"]["influences"]="; ".join(names)
        path=self.work/"multi.json";path.write_text(dumps(a))
        draft=assemble_v2(source,path,info,self.work/"multi-candidate",purpose="fixture")
        folder=Path(draft["candidate"]);root=isolated_root(self.work/"multi-root")
        (root/"video").mkdir();shutil.copyfile(source,root/"video"/source.name)
        shutil.copyfile(source,folder/"source.mp4")
        bad=self.work/"bad";bad.mkdir()
        package_folder(folder,bad/f"{a['id']}-r0001.zip")
        outcome=ingest(root,[bad/f"{a['id']}-r0001.zip"])
        self.assertEqual(outcome["results"][0]["status"],"failed")
        self.assertIn("forbids video",outcome["results"][0]["error"])
        self.assertEqual(read_json(root/"data/registry.json")["references"],{})
        (folder/"source.mp4").unlink()
        package=export_v2(folder,self.work/"good",snapshot_hash(folder),source)
        self.assertEqual(ingest(root,[Path(package["package"])])["results"][0]["status"],"imported")
        for name in names:self.assertEqual(search(root,style=name,style_role="style-influence")["total"],1)
        area=read_reference(root,a["id"],part="area",shot="shot-01",area="kitchen-1")
        self.assertEqual(area["shot"]["design"][0]["area_ids"],["kitchen-1"])
        self.assertEqual(check(root)["references"],1)
