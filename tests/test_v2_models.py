"""V2 semantic structure tests, entirely synthetic and isolated."""
import copy
import tempfile
import unittest
from pathlib import Path
from tests.fixtures.factory import make_v2_inputs
from homeku.common import LibraryError,read_json
from homeku.models import validate_audit,schema_check
from homeku.video import frame_times


class V2ModelsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory();cls.root=Path(cls.temp.name)
        cls.source,path,cls.info=make_v2_inputs(cls.root,multi=True)
        cls.audit=read_json(path);cls.times=frame_times(cls.source)

    @classmethod
    def tearDownClass(cls):cls.temp.cleanup()

    def test_multi_area_one_phase_and_overlapping_visibility(self):
        validate_audit(self.audit,1.2,self.times)
        self.assertEqual(len(self.audit["shots"]),1)
        self.assertEqual(len(self.audit["shots"][0]["phases"]),1)

    def test_floor_estimate_is_required_positive_ordered_and_not_unknown(self):
        for change in [None,"unknown",{"min":0,"max":90,"basis":"x","uncertainty":"x"},{"min":90,"max":60,"basis":"x","uncertainty":"x"}]:
            with self.subTest(change=change):
                a=copy.deepcopy(self.audit);a["size"]["floor_area_m2"]=change
                with self.assertRaises(LibraryError):validate_audit(a)

    def test_bad_scope_phase_overlap_and_fake_native_frame_rejected(self):
        mutations=[lambda a:a["shots"][0]["facts"][0].update(area_ids=["not-here"]),
                   lambda a:a["shots"][0]["phases"][0].update(start_s=0.1),
                   lambda a:a["shots"][0]["panels"][0].update(frame_index=1)]
        for change in mutations:
            a=copy.deepcopy(self.audit);change(a)
            with self.assertRaises(LibraryError):validate_audit(a,1.2,self.times)
        a=copy.deepcopy(self.audit);a["shots"][0]["facts"][0]["evidence"]=["frame:shot-01:999"]
        with self.assertRaisesRegex(LibraryError,"outside shot"):validate_audit(a,1.2,self.times)

    def test_reentry_visibility_is_separate_from_camera_route(self):
        a=copy.deepcopy(self.audit)
        a["areas"][0]["visible_intervals"]=[{"start_s":0,"end_s":0.3},{"start_s":0.4,"end_s":1.0}]
        a["shots"][0]["route"]=[]
        validate_audit(a,1.2,self.times)
        self.assertEqual(a["shots"][0]["route"],[])

    def test_all_schemas_are_valid_draft_2020(self):
        from jsonschema import Draft202012Validator
        from homeku.validation import CODE_ROOT
        for p in (CODE_ROOT/"docs/contracts").glob("*-v2.schema.json"):
            Draft202012Validator.check_schema(read_json(p))

    def test_json_key_order_does_not_act_like_template_braces(self):
        import json
        # Source field order is irrelevant, including adjacent nested closing braces.
        validate_audit(json.loads(json.dumps(self.audit)),1.2,self.times)
        a=copy.deepcopy(self.audit);a["identity"]["name"]="{{UNFILLED}}"
        with self.assertRaisesRegex(LibraryError,"placeholders"):validate_audit(a)

    def test_parsed_direction_cannot_disagree_with_technical_notation(self):
        a=copy.deepcopy(self.audit)
        a["shots"][0]["phases"][0]["components_parsed"][1]["direction"]="left"
        with self.assertRaisesRegex(LibraryError,"metadata differs"):validate_audit(a)

    def test_one_phase_can_use_collective_evidence_across_separate_areas(self):
        a=copy.deepcopy(self.audit)
        a["shots"][0]["phases"][0]["evidence"]=["p-start","p-end"]
        validate_audit(a,1.2,self.times)

    def test_multiple_phases_in_one_area_do_not_create_new_shots(self):
        from homeku.markdown import component
        with tempfile.TemporaryDirectory() as d:
            source,path,_=make_v2_inputs(Path(d));a=read_json(path)
            s=a["shots"][0];first=copy.deepcopy(s["phases"][0]);second=copy.deepcopy(first)
            first["end_s"]=0.6;second.update(phase="phase-02",start_s=0.6,components="Orbit Left (~15°)",components_parsed=[component("Orbit Left (~15°)")])
            s["phases"]=[first,second];s["camera_summary"]=first["components"]+" → "+second["components"]+"."
            validate_audit(a,1.2,frame_times(source))
            self.assertEqual(len(a["shots"]),1)
            # Two declared cuts in the same physical area stay two shots.
            original=copy.deepcopy(a["shots"][0]);shots=[]
            for index,(start,finish,frames) in enumerate([(0,0.6,[0,3,5]),(0.6,1.2,[6,9,11])],1):
                part=copy.deepcopy(original);sid=f"shot-{index:02d}"
                part.update(shot=sid,start_s=start,end_s=finish,transition="cut" if index==1 else "end")
                phase=copy.deepcopy(original["phases"][0]);phase.update(phase="phase-01",start_s=start,end_s=finish)
                part["phases"]=[phase];part["camera_summary"]=phase["components"]
                part["tempo_profile"]=[{"start_s":start,"end_s":finish,"tempo":"moderate","description":"Tempo sintetis"}]
                for p,frame in zip(part["panels"],frames):
                    p.update(id=f"s{index}-{p['role']}",shot_id=sid,frame_index=frame,timestamp_s=frame/10)
                overview=copy.deepcopy(part["overviews"][0]);overview.update(id=f"s{index}-overview",shot_id=sid,frame_index=frames[-1],timestamp_s=frames[-1]/10)
                part["overviews"]=[overview]
                for claim in part["facts"]+part["phases"]:
                    claim["evidence"]=[part["panels"][0]["id"]] if claim.get("state")!="unknown" else []
                shots.append(part)
            a["shots"]=shots
            for claim in a["profile"]+a["identity"]["style_relations"]:
                if claim["evidence"]:claim["evidence"]=["s1-start"]
            validate_audit(a,1.2,frame_times(source))
            self.assertEqual(len(a["shots"]),2)
            self.assertEqual(a["shots"][0]["area_ids"],a["shots"][1]["area_ids"])

    def test_one_area_multiple_functions_and_unknown_camera_label_are_preserved(self):
        from homeku.markdown import component
        with tempfile.TemporaryDirectory() as d:
            source,path,_=make_v2_inputs(Path(d));a=read_json(path)
            s=a["shots"][0];raw="Floating spiral (~20°)"
            s["camera_summary"]=raw;s["phases"][0].update(components=raw,components_parsed=[component(raw)])
            validate_audit(a,1.2,frame_times(source))
            self.assertEqual(len(s["area_ids"]),1)
            self.assertEqual(a["areas"][0]["functions"],["bathroom","laundry"])
            self.assertEqual(s["phases"][0]["components_parsed"][0]["movement"],"other")

    def test_incomplete_viewing_wrong_summary_and_wrong_phase_ids_rejected(self):
        from homeku.validation import validate_frame_reviews
        a=copy.deepcopy(self.audit);a["shots"][0]["camera_summary"]="Pan Left (~15°)"
        with self.assertRaisesRegex(LibraryError,"summary differs"):validate_audit(a)
        a=copy.deepcopy(self.audit);a["shots"][0]["phases"][0]["phase"]="phase-99"
        with self.assertRaisesRegex(LibraryError,"sequential"):validate_audit(a)
        logs=copy.deepcopy(self.info["frame_reviews"]);logs[0]["viewed_frame_indices"].pop()
        from homeku.video import probe_video
        with self.assertRaisesRegex(LibraryError,"incomplete"):
            validate_frame_reviews(logs,self.audit["shots"],self.source,probe_video(self.source))
