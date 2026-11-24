"""Source2.4 helpers: synthetic declarations only, never active references."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tests.fixtures.factory import make_v2_inputs
from homeku.common import LibraryError,read_json,dumps
from homeku.authoring import prepare as current_prepare,complete

def prepare(*args,**kwargs):
    kwargs.setdefault("contract_version","2.4")
    return current_prepare(*args,**kwargs)
from homeku.audit_session import mark_viewed,add_pass,workspace
from homeku.preflight import check_inputs

class EfficiencyCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.shared=tempfile.TemporaryDirectory();cls.inputs={}
        for multi in (False,True):
            s,a,i=make_v2_inputs(Path(cls.shared.name)/str(multi),rid="efficiency-multi" if multi else "efficiency-normal",multi=multi,version="2.4")
            cls.inputs[multi]=(s,read_json(a),i)
    @classmethod
    def tearDownClass(cls):cls.shared.cleanup()
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.work=Path(self.tmp.name)
        self.source,a,i=self.inputs[False];self.audit=copy.deepcopy(a);self.info=copy.deepcopy(i)
    def tearDown(self):self.tmp.cleanup()
    def path(self,a=None):
        p=self.work/"audit.json";p.write_text(dumps(a if a is not None else self.audit));return p
    def prepared(self):
        result=prepare(self.source,[],self.work/"authoring")
        return result,Path(result["session"])

class AuditAuthoringTests(EfficiencyCase):
    def test_prepare_exact_bounds_midpoint_single_batch_and_no_viewed(self):
        r,session=self.prepared()
        self.assertEqual(r["cache"]["batch_passes"],1)
        row=r["shots"][0];self.assertEqual((row["first"],row["middle"],row["last"]),(0,6,11))
        records=[p["record"] for p in read_json(session)["passes"]]
        self.assertTrue(all(not p["viewed_frame_indices"] for p in records))
        self.assertTrue(any(p["mode"]=="frame-by-frame" and p["selected_frame_indices"]==[6] for p in records))
        a=read_json(Path(r["audit"]));self.assertEqual(a["areas"],[])
        self.assertEqual(sum(c["aspect"]=="interior-style" for c in a["profile"]),1)
    def test_resume_preserves_observations_and_viewed_and_decodes_nothing(self):
        r,session=self.prepared();path=Path(r["audit"]);a=read_json(path)
        a["identity"]["name"]="Isi auditor dipertahankan";path.write_text(dumps(a));before=path.read_bytes()
        mark_viewed(session,all_passes=True,all_frames=True)
        logs=read_json(session)["passes"]
        again=prepare(self.source,[],session.parent,resume=True)
        self.assertTrue(again["resumed"]);self.assertEqual(path.read_bytes(),before)
        self.assertEqual(again["passes"],logs);self.assertEqual(again["cache"]["batch_passes"],0)
        with self.assertRaisesRegex(LibraryError,"already prepared"):prepare(self.source,[],session.parent)
    def test_complete_fixes_mechanical_fields_only_and_uses_real_passes(self):
        r,session=self.prepared();path=Path(r["audit"]);a=copy.deepcopy(self.audit)
        a["shots"][0]["panels"][1]["frame_index"]=5
        a["shots"][0]["phases"][0]["components"]="Dolly-In ~1.3× + gentle Pan Right ~15°"
        a["shots"][0]["phases"][0]["components_parsed"]=[]
        a["shots"][0]["camera_summary"]="temporary stale summary"
        original_design=copy.deepcopy(a["shots"][0]["design"]);original_facts=copy.deepcopy(a["shots"][0]["facts"])
        path.write_text(dumps(a));Path(r["audit_info"]).write_text(dumps(self.info))
        mark_viewed(session,all_passes=True,all_frames=True)
        result=complete(path,session_path=session)
        got=read_json(path)
        self.assertEqual(got["shots"][0]["panels"][1]["frame_index"],6)
        self.assertIn("(~15°)",got["shots"][0]["camera_summary"])
        self.assertEqual(got["shots"][0]["design"],original_design);self.assertEqual(got["shots"][0]["facts"],original_facts)
        self.assertTrue(result["changes"])
        checked=check_inputs(self.source,got,read_json(Path(r["audit_info"])),purpose="fixture")
        self.assertTrue(checked["ok"],checked)
    def test_incomplete_viewing_remains_incomplete_after_complete(self):
        r,session=self.prepared();path=Path(r["audit"]);path.write_text(dumps(self.audit))
        Path(r["audit_info"]).write_text(dumps(self.info))
        complete(path,session_path=session)
        result=check_inputs(self.source,read_json(path),read_json(Path(r["audit_info"])),purpose="fixture")
        self.assertFalse(result["ok"]);self.assertTrue(any("view" in e["path"] or "view" in e["message"] for e in result["errors"]))
    def test_scope_and_old_contract_are_not_silently_rewritten(self):
        r,session=self.prepared();path=Path(r["audit"])
        a=copy.deepcopy(self.audit);a["schema_version"]="2.3";path.write_text(dumps(a))
        with self.assertRaisesRegex(LibraryError,"never converts"):complete(path,session_path=session)
        a=copy.deepcopy(self.audit);a["shots"][0]["overviews"][0]["shot_id"]="shot-02";path.write_text(dumps(a))
        before=path.read_bytes()
        with self.assertRaisesRegex(LibraryError,"scope explicitly"):complete(path,session_path=session)
        self.assertEqual(before,path.read_bytes())
    def test_viewed_and_deepening_require_explicit_valid_scope(self):
        r,session=self.prepared();pid=r["passes"][0]["id"]
        with self.assertRaises(LibraryError):mark_viewed(session,pid,[999])
        result=mark_viewed(session,pid,[0]);self.assertEqual(result["viewed"],1)
        self.assertFalse(result["complete"])
        with self.assertRaises(LibraryError):add_pass(session,"shot-01",reason=" ")
        result=add_pass(session,"shot-01",start=.2,end=.5,native=True,reason="Pertanyaan oklusi sintetis.")
        self.assertFalse(result["passes"][-1]["record"]["viewed_frame_indices"])
    def test_invalid_cut_source_change_and_workspace_are_rejected(self):
        for cuts in ([True],[0],[12],[5,4],[4,4]):
            with self.assertRaises(LibraryError):prepare(self.source,cuts,self.work/str(cuts))
        with self.assertRaises(LibraryError):workspace(Path(__file__).resolve().parents[1]/"references/edh001/audit.json")
        r,session=self.prepared()
        with self.assertRaisesRegex(LibraryError,"Source/cuts differ"):
            prepare(self.source,[6],session.parent,resume=True)
    def test_resume_recovers_interrupted_prepare_without_erasing_source(self):
        r,session=self.prepared();v=read_json(session);v["passes"]=[];session.write_text(dumps(v))
        before=Path(r["audit"]).read_bytes();again=prepare(self.source,[],session.parent,resume=True)
        self.assertTrue(again["passes"]);self.assertEqual(before,Path(r["audit"]).read_bytes())
