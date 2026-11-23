"""2.3 regressions. Every video and declaration here is synthetic."""
import copy
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch
from jsonschema import Draft202012Validator
from tests.fixtures.factory import make_v2_inputs, isolated_root, make_folder, package_folder
from homeku.common import LibraryError, read_json, dumps, snapshot_hash, sha256
from homeku.models import validate_audit, v2_model
from homeku.validation import validate_frame_reviews, validate_folder, CODE_ROOT, probe_video
from homeku.video import frame_times, selected_indices
from homeku.audit_quality import validate_viewed_evidence
from homeku.markdown import component
from homeku.reporting import render_config, render_report
from homeku.exporter import assemble_v2, review_v2, export_v2, sample
from homeku.generation import render, generator_fingerprint
from homeku.engine import ingest, check
from homeku.reader import read_reference, search


class AuditMethodTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.shared = tempfile.TemporaryDirectory()
        cls.inputs = {}
        for multi in (False, True):
            source, path, info = make_v2_inputs(Path(cls.shared.name)/str(multi),
                rid="method-multi" if multi else "method-normal", multi=multi, version="2.3")
            cls.inputs[multi] = (source, read_json(path), info)
    @classmethod
    def tearDownClass(cls):
        cls.shared.cleanup()
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.work = Path(self.temp.name)
        self.source, a, info = self.inputs[False]
        self.audit = copy.deepcopy(a); self.info = copy.deepcopy(info)
        self.times = frame_times(self.source)
    def tearDown(self):
        self.temp.cleanup()
    def set_camera(self, notation, depth="NO IN/OUT"):
        s=self.audit["shots"][0]; p=s["phases"][0]
        p.update(components=notation,components_parsed=[component(c.strip()) for c in notation.split("+")],
                 depth_direction=depth,confidence="medium",tempo="moderate",speed_change="constant")
        s["camera_summary"]=notation+"."
        s["tempo_profile"]=[{"start_s":0,"end_s":1.2,"tempo":"moderate","description":"Sedang konstan, sintetis."}]
        p["motion_observations"]=[{"component_index":i,"evidence":["p-start","p-end"],
            "basis":"Fixture dua frame, bukan audit visual.",
            "estimate_basis":"Sudut tidak terpisahkan dari perubahan proyeksi test-pattern sintetis.",
            "alternatives":None,"scale_measurement":None} for i in range(len(p["components_parsed"]))]
        return p
    def assert_invalid(self, a=None, match=None):
        context=self.assertRaisesRegex(LibraryError,match) if match else self.assertRaises(LibraryError)
        with context:validate_audit(a or self.audit,times=self.times)

    def test_schemas_pairings_and_golden_reports(self):
        for name in ("audit","manifest","reference-reader","search-index"):
            Draft202012Validator.check_schema(read_json(CODE_ROOT/f"docs/contracts/{name}-v2-3.schema.json"))
        for multi,(_,a,_) in self.inputs.items():
            validate_audit(a,times=self.times)
            text=render_report(a,render_config(version="2.2.2"))
            golden=CODE_ROOT/f"tests/fixtures/reports/method-{'multi' if multi else 'normal'}-2.2.2.md"
            self.assertEqual(text,golden.read_text())
            self.assertEqual(sum(line.startswith("## ") for line in text.splitlines()),6)
            for field in ("camera_checks","scale_measurement","fact_coverage","facet_roles"):
                self.assertNotIn(field,text)
        with self.assertRaises(LibraryError):render_report(self.audit,render_config(version="2.2.1"))
        with self.assertRaises(LibraryError):
            path=self.work/"a.json";path.write_text(dumps(self.audit))
            assemble_v2(self.source,path,self.info,self.work/"bad",version="2.2.1")

    def synthetic_reviews(self, times, end, fps, source_fps=30, start=0, mode="sampling"):
        indices=selected_indices(times,start,end,fps,native=mode=="frame-by-frame",source_fps=source_fps)
        return [{"shot_id":"shot-01","start_s":start,"end_s":end,"mode":mode,
                 "sampling_fps":None if mode=="frame-by-frame" else fps,
                 "selected_frame_indices":indices,"viewed_frame_indices":list(indices),
                 "reason":"Pernyataan sintetis untuk tes coverage."}]
    def frame_check(self,times,reviews,end,version="2.3",fps=30):
        info={"fps":{"numerator":fps,"denominator":1}}
        shots=[{"shot":"shot-01","start_s":0,"end_s":end}]
        with patch("homeku.video.frame_times",return_value=times):
            return validate_frame_reviews(reviews,shots,self.source,info,contract_version=version)
    def test_six_fps_valid_new_not_old_and_three_fps_insufficient(self):
        times=[round(i/30,9) for i in range(60)]
        reviews=self.synthetic_reviews(times,2,6)
        self.frame_check(times,reviews,2)
        with self.assertRaisesRegex(LibraryError,"10 FPS"):self.frame_check(times,reviews,2,"2.2")
        with self.assertRaisesRegex(LibraryError,"6 FPS"):
            self.frame_check(times,self.synthetic_reviews(times,2,3),2)
    def test_native_low_fps_short_take_and_vfr_boundaries(self):
        for fps in (3,6):
            times=[round(i/fps,9) for i in range(fps*2)]
            self.frame_check(times,self.synthetic_reviews(times,2,6,source_fps=fps),2,fps=fps)
        times=[round(i/30,9) for i in range(15)]
        with self.assertRaisesRegex(LibraryError,"6 FPS"):
            self.frame_check(times,self.synthetic_reviews(times,.5,6),.5)
        self.frame_check(times,self.synthetic_reviews(times,.5,6,mode="frame-by-frame"),.5)
        # Variable PTS; exact source endpoints still present.
        times=[0,.03,.10,.17,.20,.31,.50,.71,.89,1.01,1.20,1.40]
        reviews=self.synthetic_reviews(times,1.5,6)
        self.assertEqual(reviews[0]["selected_frame_indices"][0],0)
        self.assertEqual(reviews[0]["selected_frame_indices"][-1],11)
        self.frame_check(times,reviews,1.5)
        broken=copy.deepcopy(reviews);broken[0]["selected_frame_indices"].pop()
        with self.assertRaisesRegex(LibraryError,"Selected"):self.frame_check(times,broken,1.5)
    def test_split_baseline_cannot_hide_gap_or_unviewed_frames(self):
        times=[round(i/30,9) for i in range(60)]
        reviews=self.synthetic_reviews(times,.9,6)
        reviews+=self.synthetic_reviews(times,2,6,start=1)
        with self.assertRaisesRegex(LibraryError,"gap"):self.frame_check(times,reviews,2)
        reviews=self.synthetic_reviews(times,2,6);reviews[0]["viewed_frame_indices"].pop()
        with self.assertRaisesRegex(LibraryError,"incomplete"):self.frame_check(times,reviews,2)
    def test_cli_default_sampling_and_short_native(self):
        result=sample(self.source,self.work/"six",shot_id="shot-01")
        self.assertEqual(result["selection"]["sampling_fps"],6)
        self.assertEqual(result["review_record_template"]["viewed_frame_indices"],[])
        result=sample(self.source,self.work/"short",start=0,end=.5,shot_id="shot-01")
        self.assertEqual(result["selection"]["mode"],"frame-by-frame")
        result=sample(self.source,self.work/"old",contract_version="2.2")
        self.assertEqual(result["selection"]["sampling_fps"],10)
    def test_missing_axis_same_physical_frame_and_unviewed_rejected(self):
        for mutate in (
            lambda p:p["camera_checks"].pop("translation"),
            lambda p:p["camera_checks"]["depth"].update(evidence=["p-start","frame:shot-01:0"]),
            lambda p:p["camera_checks"]["rotation"].update(basis=" "),
            lambda p:p["camera_checks"]["translation"].update(evidence=["p-start","frame:shot-02:11"])):
            a=copy.deepcopy(self.audit);mutate(a["shots"][0]["phases"][0]);self.assert_invalid(a)
        reviews=copy.deepcopy(self.info["frame_reviews"]);reviews[0]["viewed_frame_indices"].remove(11)
        with self.assertRaisesRegex(LibraryError,"not declared viewed"):
            validate_viewed_evidence(self.audit,reviews,self.times)
    def test_checks_cannot_borrow_early_frames_for_later_phase(self):
        s=self.audit["shots"][0];p=s["phases"][0]
        first=copy.deepcopy(p);first.update(end_s=.6,tempo="moderate",evidence=["p-start","frame:shot-01:5"])
        second=copy.deepcopy(p);second.update(phase="phase-02",start_s=.6,tempo="fast")
        # Existing observation quality already demands phase evidence; checks must do so independently.
        for x,keys in ((first,["p-start","frame:shot-01:5"]),(second,["frame:shot-01:6","p-end"])):
            x["evidence"]+=["p-start"]
            for obs in x["motion_observations"]:
                obs["evidence"]=keys;obs["scale_measurement"]=None
            x["components"]="Pan Right";x["components_parsed"]=[component("Pan Right")]
            x["motion_observations"]=x["motion_observations"][:1];x["depth_direction"]="NO IN/OUT"
            x["camera_checks"]={axis:{"evidence":keys,"basis":"Fixture batas fase."}
                                 for axis in ("depth","translation","rotation")}
        second["camera_checks"]["depth"]["evidence"]=["p-start","frame:shot-01:6"]
        s["phases"]=[first,second];s["camera_summary"]="Pan Right → Pan Right."
        self.assert_invalid(match="phase")
    def test_pan_static_zoom_unknown_and_combined_are_not_forced_dolly(self):
        for notation,depth in (("Pan Left","NO IN/OUT"),("Static","NO IN/OUT"),
                               ("Zoom-In","NO IN/OUT"),("Uncertain",None),
                               ("Dolly-Out + Orbit Left + Pan Right","OUT")):
            p=self.set_camera(notation,depth)
            if notation=="Uncertain":p["motion_observations"][0]["alternatives"]="Belum terpisahkan pada fixture."
            validate_audit(self.audit,times=self.times)
        self.set_camera("Dolly-In","OUT");self.assert_invalid(match="depth_direction")
    def test_scale_ratios_rounding_ranges_and_out_convention(self):
        m=self.audit["shots"][0]["phases"][0]["motion_observations"][0]["scale_measurement"]
        m["end_px"]=134.9
        validate_audit(self.audit,times=self.times)
        p=self.set_camera("Dolly-Out (~1.3×)","OUT")
        p["motion_observations"][0]["scale_measurement"]={**m,"start_px":130,"end_px":100}
        validate_audit(self.audit,times=self.times)
        p=self.set_camera("Dolly-Out (~1.2–1.5×)","OUT")
        p["motion_observations"][0]["scale_measurement"]={**m,"start_px":140,"end_px":100}
        validate_audit(self.audit,times=self.times)
    def test_scale_measurement_corruption_and_missing_limitation(self):
        for mutate in (
            lambda o:o.update(scale_measurement=None),
            lambda o:o["scale_measurement"].update(end_px=80),
            lambda o:o["scale_measurement"].update(end_px=220),
            lambda o:o["scale_measurement"].update(start_evidence="p-end"),
            lambda o:o["scale_measurement"].update(dimension="area"),
            lambda o:o["scale_measurement"].update(start_px=0),
            lambda o:o["scale_measurement"].update(anchor=" ")):
            a=copy.deepcopy(self.audit);mutate(a["shots"][0]["phases"][0]["motion_observations"][0]);self.assert_invalid(a)
        p=self.set_camera("Orbit Left")
        p["motion_observations"][0]["estimate_basis"]=None
        self.assert_invalid(match="estimate_basis")
    def test_dolly_zoom_total_ratio_not_double_attributed(self):
        old=self.audit["shots"][0]["phases"][0]["motion_observations"][0]["scale_measurement"]
        p=self.set_camera("Dolly-In (~1.3×) + Zoom-In (~1.3×)","IN")
        for obs in p["motion_observations"]:obs["scale_measurement"]=copy.deepcopy(old)
        self.assert_invalid(match="total scale")
        p=self.set_camera("Dolly-In + Zoom-In","IN")
        validate_audit(self.audit,times=self.times)
    def test_all_moderate_valid_and_conflicting_acceleration_rejected(self):
        p=self.set_camera("Dolly-Out","OUT");s=self.audit["shots"][0]
        # Repeat neutral labels without forcing artificial variations or phases.
        s["tempo_profile"]=[{"start_s":i*.2,"end_s":(i+1)*.2 if i<5 else 1.2,
            "tempo":"moderate","description":"Sedang."} for i in range(6)]
        validate_audit(self.audit,times=self.times)
        p["tempo"]="variable";p["speed_change"]="accelerating"
        s["tempo_profile"]=[{"start_s":0,"end_s":.6,"tempo":"fast","description":"Cepat."},
                            {"start_s":.6,"end_s":1.2,"tempo":"moderate","description":"Sedang."}]
        self.assert_invalid(match="accelerating")
        p["speed_change"]="decelerating"
        validate_audit(self.audit,times=self.times)

    def test_six_complete_shots_can_all_remain_moderate(self):
        a=copy.deepcopy(self.audit);original=copy.deepcopy(a["shots"][0])
        first_map={}
        a["shots"]=[]
        for i in range(6):
            shot=copy.deepcopy(original);sid=f"shot-{i+1:02d}";offset=round(i*1.2,9)
            labels={p["id"]:f"s{i+1:02d}-{p['id']}" for group in ("panels","overviews") for p in shot[group]}
            if i==0:first_map=labels
            def remap(value):
                if isinstance(value,dict):return {k:remap(v) for k,v in value.items()}
                if isinstance(value,list):return [remap(v) for v in value]
                if isinstance(value,str):
                    if value in labels:return labels[value]
                    if value.startswith("frame:shot-01:"):
                        return f"frame:{sid}:{int(value.rsplit(':',1)[1])+12*i}"
                return value
            shot=remap(shot);shot["shot"]=sid
            shot["start_s"]=offset;shot["end_s"]=round(offset+1.2,9)
            for group in ("panels","overviews"):
                for panel in shot[group]:
                    panel["shot_id"]=sid;panel["frame_index"]+=12*i
                    panel["timestamp_s"]=round(panel["timestamp_s"]+offset,9)
            for phase in shot["phases"]:
                phase.update(start_s=offset,end_s=shot["end_s"],tempo="moderate",speed_change="constant")
            shot["rhythm"]="Sedang sepanjang shot sintetis."
            shot["tempo_profile"]=[{"start_s":offset,"end_s":shot["end_s"],
                                     "tempo":"moderate","description":"Sedang konstan."}]
            a["shots"].append(shot)
        for c in a["profile"]+a["identity"]["style_relations"]:
            c["evidence"]=[first_map.get(k,k) for k in c["evidence"]]
        a["areas"][0]["visible_intervals"]=[{"start_s":0,"end_s":7.2}]
        a["timeline_notes"]="Enam shot sintetis, semuanya moderate."
        validate_audit(a,7.2,[round(i/10,9) for i in range(72)])

    def draft(self,multi=False):
        source,a,info=self.inputs[multi]
        path=self.work/"audit.json";path.write_text(dumps(a))
        d=assemble_v2(source,path,info,self.work/"candidate",purpose="fixture")
        return source,Path(d["candidate"]),d
    def test_roundtrip_reader_all_pointers_mixed_versions_and_snapshot(self):
        source,folder,d=self.draft(True)
        review=review_v2(folder,self.work/"review.md",source)
        self.assertEqual(review["snapshot_sha256"],d["snapshot_sha256"])
        with patch("homeku.media.build_media",side_effect=AssertionError("must not encode")):
            package=export_v2(folder,self.work/"packages",d["snapshot_sha256"],source)
        with zipfile.ZipFile(package["package"]) as z:
            self.assertFalse(any(n.endswith(".mp4") for n in z.namelist()))
            self.assertEqual(len(z.namelist()),6)
        root=isolated_root(self.work/"root");(root/"video").mkdir()
        shutil.copyfile(source,root/"video"/source.name)
        result=ingest(root,[Path(package["package"])]);self.assertEqual(result["results"][0]["status"],"imported",result)
        self.assertEqual(ingest(root,[Path(package["package"])])["changed"],[])
        payload=read_reference(root,folder.name,part="full");authored=read_json(folder/"audit.json")
        for pointer,proof in payload["provenance"].items():
            node=payload
            for part in pointer.strip("/").split("/"):node=node[int(part)] if isinstance(node,list) else node[part]
            if proof.get("json"):
                src=authored
                for part in proof["source_pointer"].strip("/").split("/") if proof["source_pointer"] else []:
                    src=src[int(part)] if isinstance(src,list) else src[part]
            for key in proof.get("evidence_ids",[]):self.assertIn(key,payload["evidence_inventory"])
        self.assertTrue(any("camera_checks" in k for k in payload["provenance"]))
        self.assertTrue(any("scale_measurement" in k for k in payload["provenance"]))
        legacy=make_folder(self.work/"legacy",rid="method-legacy")
        result=ingest(root,[package_folder(legacy,self.work/"method-legacy-r0001.zip")])
        self.assertEqual(result["results"][0]["status"],"imported",result)
        self.assertEqual(check(root)["references"],2)
        # New checks don't leak into the bounded index.
        text=(root/"data/search-index.json").read_text()
        for key in ("camera_checks","scale_measurement","motion_observations","frame_reviews"):
            self.assertNotIn(key,text)
        (folder/"analysis.md").write_text((folder/"analysis.md").read_text()+"\n")
        with self.assertRaisesRegex(LibraryError,"changed since"):
            export_v2(folder,self.work/"changed",d["snapshot_sha256"],source)
    def test_no_video_candidate_and_wrong_report_pairing(self):
        source,folder,d=self.draft()
        shutil.copyfile(source,folder/"source.mp4")
        with self.assertRaisesRegex(LibraryError,"forbids video"):validate_folder(folder,self.work,source_overrides={folder.name:source})
        path=self.work/"a.json";path.write_text(dumps(self.audit))
        with self.assertRaisesRegex(LibraryError,"forbids --include-source"):
            assemble_v2(self.source,path,self.info,self.work/"forbidden",include_source=True)
    def test_explicit_facets_legacy_mapping_unknown_negation_and_capacity(self):
        source,folder,_=self.draft()
        _,model,_=validate_folder(folder,self.work,source_overrides={folder.name:source})
        model=copy.deepcopy(model);facts=model["shots"][0]["facts"]
        facts[0].update(attribute="new-opening-shape",value="arched opening",facet_roles=["opening"])
        facts[1].update(attribute="new-roof-shape",value="roof",facet_roles=["roof"],state="not-visible")
        # Unknown/new labels are retained rather than guessed.
        root=isolated_root(self.work/"render-root")
        out=render(root,{model["id"]:model});index=json.loads(out["data/search-index.json"])
        facets=index["references"][0]["shots"][0]["design_facets"]
        self.assertEqual(facets[0]["facet_roles"],["opening"])
        self.assertEqual(facets[1]["state"],"not-visible")
        self.assertEqual(facets[0]["role_source"]["version"],"2.3")
        legacy=copy.deepcopy(model);legacy["format_version"]="2.2";legacy["schema_version"]="2.2"
        for f in legacy["shots"][0]["facts"]:f.pop("facet_roles")
        for p in legacy["shots"][0]["phases"]:
            p.pop("camera_checks")
            for o in p["motion_observations"]:o.pop("scale_measurement")
        legacy["shots"][0]["facts"][0]["attribute"]="opening-shape"
        legacy["shots"][0]["facts"][1]["attribute"]="massing-and-roof"
        legacy["render"]=render_config(version="2.2.1")
        out=render(root,{legacy["id"]:legacy})
        facets=json.loads(out["data/search-index.json"])["references"][0]["shots"][0]["design_facets"]
        self.assertEqual(facets[0]["facet_roles"],["opening"])
        self.assertEqual(facets[1]["facet_roles"],["massing","roof"])
        self.assertEqual(facets[0]["role_source"]["json"],"sources/fact-facets.json")
        self.assertIn("new-attribute",json.loads(out["data/dependencies.json"])["unmapped_fact_attributes"])
        models={}
        for i in range(300):
            m=copy.deepcopy(model);m["id"]=f"method-capacity-{i:03d}";models[m["id"]]=m
        before=generator_fingerprint(root)
        with patch("homeku.generation.sha256",
                   side_effect=lambda path:"0"*64 if str(path).endswith("sources/fact-facets.json") else sha256(path)):
            self.assertNotEqual(before,generator_fingerprint(root))
        out=render(root,models);text=out["data/search-index.json"]
        self.assertEqual(len(json.loads(text)["references"]),300)
        self.assertLess(len(text.encode()),4_000_000)
        for key in ("camera_checks","scale_measurement","viewed_frame_indices"):self.assertNotIn(key,text)
        self.assertEqual(out,render(root,models))
    def test_kit_portable_23_restores_guides_and_runs_exact_snapshot(self):
        from tests.test_audit import kit_builder
        chat=self.work/"chat";chat.mkdir()
        with zipfile.ZipFile(io.BytesIO(kit_builder.build_bytes())) as z:z.extractall(chat)
        def run(*args):
            r=subprocess.run([sys.executable,*map(str,args)],cwd=chat,capture_output=True,text=True)
            self.assertEqual(r.returncode,0,r.stdout+r.stderr);return json.loads(r.stdout)
        run(chat/"homeku_runtime.py","--output",chat)
        for name in kit_builder.BUNDLED:
            self.assertEqual((chat/name).read_bytes(),(CODE_ROOT/name).read_bytes())
        self.assertLess(len((chat/"README.md").read_text().split("## Inventaris")[0].split()),400)
        path=self.work/"a.json";path.write_text(dumps(self.audit))
        info=self.work/"i.json";info.write_text(dumps(self.info))
        draft=run(chat/"tools/audit.py","draft-v2",self.source,path,"--audit-info",info,"--output",self.work/"portable")
        review=run(chat/"tools/audit.py","review",draft["candidate"],"--source",self.source,"--output",self.work/"portable-review.md")
        package=run(chat/"tools/audit.py","export-v2",draft["candidate"],"--source",self.source,
                    "--receipt",review["receipt"],"--output",self.work/"portable-packages")
        self.assertEqual(package["snapshot_sha256"],draft["snapshot_sha256"])
