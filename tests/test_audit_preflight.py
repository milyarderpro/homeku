"""Input failures must be found before rendering expensive media."""
import copy
from pathlib import Path
from unittest.mock import patch
from tests.test_audit_authoring import EfficiencyCase
from homeku.common import LibraryError,dumps,read_json
from homeku.preflight import check_inputs
from homeku.exporter import assemble_v2
from homeku.markdown import component

class AuditPreflightTests(EfficiencyCase):
    def test_independent_schema_errors_collected_without_decode_or_render(self):
        a=copy.deepcopy(self.audit);a["relations"]=[{"from":"area-x","to":"area-y"}]
        info=copy.deepcopy(self.info);info["frame_reviews"][0]["mode"]="native";info["ai"].pop("provider")
        with patch("homeku.preflight.frame_times",side_effect=AssertionError("schema must fail first")):
            result=check_inputs(self.source,a,info,purpose="fixture")
        self.assertFalse(result["ok"]);self.assertGreaterEqual(len(result["errors"]),5)
        self.assertTrue(all(set(("path","group","message","action"))<=set(e) for e in result["errors"]))
    def test_invalid_audit_info_never_calls_build_media_or_replaces_candidate(self):
        path=self.path();draft=assemble_v2(self.source,path,self.info,self.work/"candidate",purpose="fixture")
        folder=Path(draft["candidate"]);before=(folder/"manifest.json").read_bytes()
        info=copy.deepcopy(self.info);info["frame_reviews"][0]["mode"]="native"
        with patch("homeku.media.build_media",side_effect=AssertionError("must preflight")):
            with self.assertRaisesRegex(LibraryError,"preflight failed before media"):
                assemble_v2(self.source,path,info,self.work/"candidate",purpose="fixture")
        self.assertEqual((folder/"manifest.json").read_bytes(),before)
    def test_midpoint_parser_relations_and_unviewed_failures_are_grouped(self):
        a=copy.deepcopy(self.audit);s=a["shots"][0];s["panels"][1]["frame_index"]=5
        s["phases"][0]["components_parsed"][0]["direction"]="Out"
        a["relations"]=[{"id":"r1","from":"area-01","to":"area-02","relation":"unknown","description":"Fixture",
                         "state":"unknown","confidence":"unknown","basis":"Fixture","uncertainty":"Fixture","evidence":[]}]
        info=copy.deepcopy(self.info);info["frame_reviews"][0]["viewed_frame_indices"].pop()
        r=check_inputs(self.source,a,info,purpose="fixture")
        self.assertFalse(r["ok"]);groups={e["group"] for e in r["errors"]}
        self.assertTrue({"scope","midpoint","notation","frames"}<=groups,r)
    def test_visual_estimates_work_without_pixel_measurements_and_23_stays_strict(self):
        a=copy.deepcopy(self.audit);a["shots"][0]["phases"][0]["confidence"]="high"
        self.assertTrue(check_inputs(self.source,a,self.info,purpose="fixture")["ok"])
        a["schema_version"]="2.3"
        r=check_inputs(self.source,a,self.info,purpose="fixture")
        self.assertFalse(r["ok"]);self.assertTrue(any("scale_measurement" in e["message"] for e in r["errors"]),r)
    def test_clear_pan_requires_visual_angle_not_calibration(self):
        a=copy.deepcopy(self.audit);p=a["shots"][0]["phases"][0];p["confidence"]="high"
        p["components"]="Dolly-In (~1.3×) + Pan Right"
        p["components_parsed"]=[component(c.strip()) for c in p["components"].split("+")]
        a["shots"][0]["camera_summary"]=p["components"]+"."
        r=check_inputs(self.source,a,self.info,purpose="fixture")
        self.assertFalse(r["ok"]);self.assertTrue(any("visual ~°" in e["message"] for e in r["errors"]))
        p["confidence"]="low";self.assertTrue(check_inputs(self.source,a,self.info,purpose="fixture")["ok"])
    def test_optional_pixel_measurement_still_needs_valid_ratio(self):
        a=copy.deepcopy(self.audit);p=a["shots"][0]["phases"][0]
        p["motion_observations"][0]["scale_measurement"]={"anchor":"Fixture","dimension":"width",
            "start_evidence":"p-start","end_evidence":"p-end","start_px":100,"end_px":220}
        r=check_inputs(self.source,a,self.info,purpose="fixture")
        self.assertFalse(r["ok"]);self.assertTrue(any("ratio" in e["message"] for e in r["errors"]))
    def test_invalid_supersedes_and_purpose_fail_before_media(self):
        with patch("homeku.media.build_media",side_effect=AssertionError("no images")):
            with self.assertRaisesRegex(LibraryError,"preflight"):assemble_v2(
                self.source,self.path(),self.info,self.work/"bad",purpose="bad",supersedes={"revision":2})
    def test_invalid_interval_produces_diagnostics_not_traceback(self):
        a=copy.deepcopy(self.audit);a["shots"][0]["start_s"]=.9;a["shots"][0]["end_s"]=.1
        r=check_inputs(self.source,a,self.info,purpose="fixture")
        self.assertFalse(r["ok"])

    def test_visual_estimates_still_reject_negative_reversed_or_out_convention(self):
        for notation in ("Dolly-In (~-2×) + Pan Right (~15°)",
                         "Dolly-Out (~0.7×) + Pan Right (~15°)",
                         "Dolly-In (~1.3×) + Pan Right (~20–10°)"):
            a=copy.deepcopy(self.audit);p=a["shots"][0]["phases"][0]
            p["components"]=notation;p["components_parsed"]=[component(c.strip()) for c in notation.split("+")]
            p["depth_direction"]="OUT" if "Dolly-Out" in notation else "IN";a["shots"][0]["camera_summary"]=notation+"."
            self.assertFalse(check_inputs(self.source,a,self.info,purpose="fixture")["ok"])
    def test_unreadable_source_returns_diagnostic(self):
        source=self.work/self.source.name;source.write_bytes(b"not a video")
        result=check_inputs(source,self.audit,self.info,purpose="fixture")
        self.assertFalse(result["ok"]);self.assertEqual(result["errors"][0]["group"],"metadata")
