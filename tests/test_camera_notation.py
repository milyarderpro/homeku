"""Camera cases are synthetic contract tests, not new reference audits."""
import copy
import tempfile
import unittest
from pathlib import Path
from tests.fixtures.factory import make_v2_inputs
from homeku.markdown import component
from homeku.camera_notation import bounds,normalize,validate_component
from homeku.authoring import notation
from homeku.models import validate_audit
from homeku.common import read_json,LibraryError
from homeku.video import frame_times

CASES=[
"Pure Orbit Left → Accelerating Dolly-In (~2.0×)",
"Pure Orbit Right → Accelerating Dolly-In (~2.1×)",
"Straight Dolly-In → Dolly-In + Strong Pan Right (~25°–30°)",
"Accelerating Dolly-In (~2.2×) + Accelerating Pan Left (~25°–30°)",
"Dolly-In (~2.0×) + Subtle Pan Right (~15°)",
"Dolly-Out (~1.6×) + Orbit Left + Subtle Pan Right (Ease-Out)",
"Dolly-Out (~1.75×) + Orbit Right + Strong Pan Left (Ease-Out)",
"Mild Dolly-Out (~1.3×) + Orbit Left + Strong Pan Right (~35°, Ease-Out)",
"Diagonal Dolly-Out (~2.5×) + Moderate Pan Right (Ease-Out)",
"Diagonal Dolly-Out (~1.75×) + Subtle Pan Left (Ease-Out)",
"Dolly-Out (~1.6×) + Orbit Left + Pan Right",
"Pan Right","Dolly-In","Static Distance + Orbit Left"]

class CameraCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.shared=tempfile.TemporaryDirectory();cls.inputs={}
        for multi in (False,True):
            source,path,info=make_v2_inputs(Path(cls.shared.name)/str(multi),rid="camera-multi" if multi else "camera-normal",multi=multi,version="2.5")
            cls.inputs[multi]=(source,read_json(path),info)
    @classmethod
    def tearDownClass(cls):cls.shared.cleanup()
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.work=Path(self.tmp.name)
        self.source,a,i=self.inputs[False];self.audit=copy.deepcopy(a);self.info=copy.deepcopy(i)
    def tearDown(self):self.tmp.cleanup()

def set_motion(a,text):
    s=a["shots"][0];original=s["phases"][0];parts=text.split(" → ");end=s["end_s"];phases=[]
    for j,part in enumerate(parts):
        p=copy.deepcopy(original);p.update(phase=f"phase-{j+1:02d}",start_s=j*end/len(parts),end_s=(j+1)*end/len(parts),
            components=part,components_parsed=[component(v.strip(),"2.5") for v in part.split("+")],
            confidence="high",speed_change="variable",tempo="moderate")
        first=0 if j==0 else 6;last=11 if j==len(parts)-1 else 5
        evidence=[f"frame:shot-01:{first}",f"frame:shot-01:{last}"]
        p["evidence"]=evidence
        p["camera_checks"]={k:{"evidence":evidence,"basis":"Synthetic interval observation."} for k in ("depth","translation","rotation")}
        p["depth_direction"]="IN" if "Dolly-In" in part else "OUT" if "Dolly-Out" in part else "NO IN/OUT"
        p["motion_observations"]=[{"component_index":i,"evidence":evidence,"basis":"Synthetic visual observation.",
            "estimate_basis":"Synthetic visual estimate." if c["estimates"] else None,"alternatives":None,"scale_measurement":None}
            for i,c in enumerate(p["components_parsed"])]
        phases.append(p)
    s["phases"]=phases;s["camera_summary"]=text+"."
    s["tempo_profile"]=[{"start_s":0,"end_s":end,"tempo":"moderate","description":"Synthetic steady moderate tempo."}]
    return a

class CameraNotationTests(CameraCase):
    def test_all_experiment_cases_validate_without_mandatory_angles(self):
        for text in CASES:
            with self.subTest(text=text):
                validate_audit(set_motion(copy.deepcopy(self.audit),text),1.2,frame_times(self.source))
    def test_without_numbers_preserves_high_confidence(self):
        a=set_motion(self.audit,"Dolly-Out + Orbit Left + Pan Right")
        validate_audit(a,1.2,frame_times(self.source))
        self.assertEqual(a["shots"][0]["phases"][0]["confidence"],"high")
        self.assertTrue(all(o["estimate_basis"] is None for o in a["shots"][0]["phases"][0]["motion_observations"]))
    def test_normalization_changes_units_and_decimal_only(self):
        self.assertEqual(notation("Dolly-Out (~1,75x) + Orbit Left","2.5"),"Dolly-Out (~1.75×) + Orbit Left")
        raw="Simultaneous: Diagonal Dolly-Out (~1.75×)"
        self.assertEqual(component(raw,"2.5")["raw"],raw)
        self.assertEqual(component(raw,"2.5")["qualifiers"],["Diagonal"])
    def test_unknown_labels_and_descriptors_are_preserved(self):
        c=component("Subtle Novel Move toward arch","2.5")
        self.assertEqual(c["movement"],"other");self.assertEqual(c["qualifiers"],["Subtle"])
        self.assertEqual(c["toward"],"arch")
    def test_legacy_parser_unchanged_and_24_still_requires_numbers(self):
        self.assertEqual(component("Subtle Pan Right")["qualifiers"],[])
        self.assertEqual(component("Subtle Pan Right","2.5")["qualifiers"],["Subtle"])
        a=set_motion(self.audit,"Dolly-In");a["schema_version"]="2.4"
        with self.assertRaisesRegex(LibraryError,"estimate_basis|requires a visual"):
            validate_audit(a,1.2,frame_times(self.source))
    def test_invalid_and_reversed_values_are_rejected(self):
        for value in ["~0×","~.8×","~2–1×","~0°","~30–10°","~NaN×","~1e309×"]:
            with self.subTest(value=value),self.assertRaises(LibraryError):
                c=component("Dolly-In ("+value+")" if value.endswith("×") else "Pan Right ("+value+")","2.5")
                validate_component(c,{"speed_change":"variable"})
    def test_easing_is_component_specific_and_requires_consistent_curve(self):
        c=component("Subtle Pan Right (Ease-Out)","2.5")
        with self.assertRaises(LibraryError):validate_component(c,{"speed_change":"constant"})
        validate_component(c,{"speed_change":"variable"})
        a=set_motion(self.audit,CASES[5]);validate_audit(a,1.2,frame_times(self.source))
        self.assertNotIn("Ease-Out",a["shots"][0]["phases"][0]["components_parsed"][0]["qualifiers"])
    def test_numeric_estimate_basis_needed_only_when_present(self):
        a=set_motion(self.audit,"Dolly-In (~2×)")
        a["shots"][0]["phases"][0]["motion_observations"][0]["estimate_basis"]=None
        with self.assertRaisesRegex(LibraryError,"estimate_basis"):
            validate_audit(a,1.2,frame_times(self.source))
    def test_false_parsed_metadata_is_rejected(self):
        a=set_motion(self.audit,"Straight Dolly-In")
        a["shots"][0]["phases"][0]["components_parsed"][0]["qualifiers"]=[]
        with self.assertRaisesRegex(LibraryError,"metadata"):
            validate_audit(a,1.2,frame_times(self.source))
