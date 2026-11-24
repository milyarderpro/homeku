"""2.4 full workflow, reports, readers, timing and portable input kit."""
import copy
import importlib.util
import io
import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from unittest.mock import patch
from jsonschema import Draft202012Validator
from tests.test_audit_authoring import EfficiencyCase
from tests.fixtures.factory import isolated_root
from homeku.authoring import prepare,complete
from homeku.audit_session import mark_viewed,add_frames
from homeku.common import LibraryError,read_json,dumps,snapshot_hash,sha256
from homeku.exporter import assemble_v2,review_v2,export_v2
from homeku.engine import ingest,check
from homeku.generation import render
from homeku.models import validate_audit
from homeku.reporting import render_report,render_config
from homeku.validation import CODE_ROOT,validate_folder
from homeku.reader import read_reference,search

class AuditEfficiencyTests(EfficiencyCase):
    def test_new_schemas_and_golden_reports_and_explicit_visual_estimates(self):
        for kind in ("audit","manifest","reference-reader","search-index"):
            Draft202012Validator.check_schema(read_json(CODE_ROOT/f"docs/contracts/{kind}-v2-4.schema.json"))
        for multi,(_,a,_) in self.inputs.items():
            text=render_report(a,render_config(version="2.2.3"))
            golden=CODE_ROOT/f"tests/fixtures/reports/efficiency-{'multi' if multi else 'normal'}-2.2.3.md"
            self.assertEqual(text,golden.read_text())
            self.assertEqual(sum(line.startswith("## ") for line in text.splitlines()),6)
            self.assertIn("**60–90 m²**",text)
            for name in ("performance","cache","scale_measurement","camera_checks"):self.assertNotIn(name,text)
        with self.assertRaises(LibraryError):render_report(self.audit,render_config(version="2.2.2"))
    def test_multi_area_prepare_add_selections_complete_and_input_valid(self):
        source,a,info=self.inputs[True]
        r=prepare(source,[],self.work/"multi");session=Path(r["session"])
        path=Path(r["audit"]);path.write_text(dumps(a));Path(r["audit_info"]).write_text(dumps(info))
        # Frame4 is an extra multi-area reveal, not part of default6FPS.
        added=add_frames(session,[4],reason="Panel reveal sintetis tambahan.")
        self.assertEqual(added["passes"][-1]["record"]["selected_frame_indices"],[4])
        mark_viewed(session,all_passes=True,all_frames=True);complete(path,session_path=session)
        from homeku.preflight import check_inputs
        result=check_inputs(source,read_json(path),read_json(Path(r["audit_info"])),purpose="fixture")
        self.assertTrue(result["ok"],result)
    def test_export_and_ingest_unchanged_snapshot_without_cache_or_video(self):
        path=self.path();d=assemble_v2(self.source,path,self.info,self.work/"candidate",purpose="fixture")
        folder=Path(d["candidate"]);review=review_v2(folder,self.work/"review.md",self.source)
        with patch("homeku.media.build_media",side_effect=AssertionError("export does not encode")):
            package=export_v2(folder,self.work/"packages",review["snapshot_sha256"],self.source)
        with zipfile.ZipFile(package["package"]) as z:
            self.assertEqual(len(z.namelist()),6)
            self.assertFalse(any("cache" in n or "performance" in n or n.endswith(".mp4") for n in z.namelist()))
        root=isolated_root(self.work/"root");(root/"video").mkdir()
        shutil.copyfile(self.source,root/"video"/self.source.name)
        result=ingest(root,[Path(package["package"])]);self.assertEqual(result["results"][0]["status"],"imported",result)
        self.assertEqual(ingest(root,[Path(package["package"])])["changed"],[])
        self.assertEqual(check(root)["status"],"ok")
        payload=read_reference(root,self.audit["id"],part="full")
        self.assertEqual(payload["schema_version"],"2.4")
        self.assertEqual(payload["reference"]["format_version"],"2.4")
        self.assertTrue(any("camera_checks" in p for p in payload["provenance"]))
        for pointer,proof in payload["provenance"].items():
            node=payload
            for p in pointer.strip("/").split("/"):node=node[int(p)] if isinstance(node,list) else node[p]
            for key in proof.get("evidence_ids",[]):self.assertIn(key,payload["evidence_inventory"])
        self.assertEqual(search(root,configuration="raised tub platform")["total"],1)
        (folder/"audit.json").write_bytes((folder/"audit.json").read_bytes()+b"\n")
        with self.assertRaisesRegex(LibraryError,"changed since"):
            export_v2(folder,self.work/"stale",review["snapshot_sha256"],self.source)
    def test_performance_is_outside_candidate_and_metadata_edit_decodes_zero(self):
        path=self.path();d=assemble_v2(self.source,path,self.info,self.work/"candidate",purpose="fixture")
        log=Path(d["performance_log"]);self.assertFalse(log.is_relative_to(Path(d["candidate"])))
        rows=[json.loads(line) for line in log.read_text().splitlines()]
        self.assertTrue(any(r["stage"]=="check-input" and r.get("state")=="complete" for r in rows))
        a=copy.deepcopy(self.audit);a["limitations"]+=" Metadata-only test.";path.write_text(dumps(a))
        again=assemble_v2(self.source,path,self.info,self.work/"candidate",purpose="fixture")
        self.assertEqual(again["cache"]["canonical_decodes"],0)
        self.assertEqual(again["cache"]["batch_passes"],0)
    def test_300_models_keep_index_bounded_and_sources_complete(self):
        path=self.path();d=assemble_v2(self.source,path,self.info,self.work/"candidate",purpose="fixture")
        _,model,_=validate_folder(Path(d["candidate"]),self.work,source_overrides={self.audit["id"]:self.source})
        root=isolated_root(self.work/"capacity")
        models={}
        for i in range(300):
            m=copy.deepcopy(model);m["id"]=f"eff-capacity-{i:03d}";models[m["id"]]=m
        output=render(root,models);text=output["data/search-index.json"]
        self.assertEqual(len(json.loads(text)["references"]),300);self.assertLess(len(text.encode()),4_000_000)
        for field in ("performance","camera_checks","viewed_frame_indices","scale_measurement"):self.assertNotIn(field,text)
    def test_portable_cli_prepare_viewed_complete_preflight_draft_review_export(self):
        from tests.test_audit import kit_builder
        chat=self.work/"chat";chat.mkdir()
        with zipfile.ZipFile(io.BytesIO(kit_builder.build_bytes())) as z:z.extractall(chat)
        def run(*args,ok=True):
            p=subprocess.run([sys.executable,*map(str,args)],cwd=chat,capture_output=True,text=True)
            self.assertEqual(p.returncode,0 if ok else 1,p.stdout+p.stderr);return json.loads(p.stdout)
        run(chat/"homeku_runtime.py","--output",chat)
        cuts=chat/"cuts.json";cuts.write_text("[]")
        prep=run(chat/"tools/audit.py","prepare",self.source,"--cuts-file",cuts,"--output",chat/"work")
        self.assertNotIn("frames",prep["passes"][0]);self.assertIn("sheets",prep["passes"][0])
        path=Path(prep["audit"]);path.write_text(dumps(self.audit));Path(prep["audit_info"]).write_text(dumps(self.info))
        run(chat/"tools/audit.py","mark-viewed",prep["session"],"--all-passes","--all")
        run(chat/"tools/audit.py","complete",path,"--session",prep["session"])
        checked=run(chat/"tools/audit.py","check-input",self.source,path,"--audit-info",prep["audit_info"])
        self.assertTrue(checked["ok"])
        draft=run(chat/"tools/audit.py","draft-v2",self.source,path,"--audit-info",prep["audit_info"],"--output",chat/"candidate")
        review=run(chat/"tools/audit.py","review",draft["candidate"],"--source",self.source,"--output",chat/"review.md")
        package=run(chat/"tools/audit.py","export-v2",draft["candidate"],"--source",self.source,
                    "--receipt",review["receipt"],"--output",chat/"final")
        self.assertEqual(package["snapshot_sha256"],draft["snapshot_sha256"])
        for name in kit_builder.BUNDLED:self.assertEqual((chat/name).read_bytes(),(CODE_ROOT/name).read_bytes())
    def test_benchmark_reports_cold_warm_invalid_and_changed_media(self):
        spec=importlib.util.spec_from_file_location("eff_benchmark",CODE_ROOT/"tools/benchmark_audit.py")
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        result=module.benchmark(self.source,self.path(),self.info,self.work/"benchmark")
        self.assertTrue(result["parity"]);self.assertFalse(result["invalid_preflight"]["ok"])
        cases={r["case"]:r for r in result["cases"]}
        self.assertEqual(cases["warm"]["cache"]["canonical_decodes"],0)
        self.assertEqual(cases["metadata"]["changed_media"],[])
        self.assertEqual(set(cases["camera"]["changed_media"]),{"media/shot-01.jpg","media/storyboard.jpg"})
