"""Single-format schema behavior; no production reference or video claims."""
import copy
import json
import unittest
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def schema(name):
    return json.loads((ROOT / "schemas" / (name + ".schema.json")).read_text())


def claim(value="Modern Cottage", state="observed"):
    return {"value": value, "state": state, "evidence": [] if state == "unknown" else [0, 1]}


class SchemaTests(unittest.TestCase):
    def validate_part(self, part, value):
        audit = schema("audit")
        Draft202012Validator({"$defs": audit["$defs"], **audit["$defs"][part]}).validate(value)

    def design(self):
        return {
            "name": "Contoh Sintetis",
            "styles": {"primary": claim(), "influences": [claim("Scandinavian Contemporary")],
                       "interior": [claim("Cozy Minimalist")]},
            "size": {**{key: claim(value) for key, value in
                       [("scale", "small"), ("levels", "single story"),
                        ("footprint", "compact"), ("proportions", "horizontal")]},
                     "floor_area_m2": {"min": 60, "max": 90}},
            "features": [dict(claim("curvilinear"), aspect="massing")]
        }

    def test_all_schemas_are_valid_and_local_refs_resolve(self):
        def walk(value, root):
            if isinstance(value, dict):
                if "$ref" in value:
                    self.assertTrue(value["$ref"].startswith("#/"))
                    found = root
                    for part in value["$ref"][2:].split("/"):
                        found = found[part.replace("~1", "/").replace("~0", "~")]
                for item in value.values():
                    walk(item, root)
            elif isinstance(value, list):
                for item in value:
                    walk(item, root)
        for name in ("audit", "audit-info", "manifest", "reference-reader", "search-index"):
            value = schema(name)
            Draft202012Validator.check_schema(value)
            walk(value, value)

    def test_only_one_format_is_accepted(self):
        for name, field in [("audit", "schema_version"), ("manifest", "contract_version"),
                            ("reference-reader", "schema_version"), ("search-index", "schema_version")]:
            for version in ("1.0", "2.5", "future"):
                errors = list(Draft202012Validator(schema(name)).iter_errors({field: version}))
                self.assertTrue(any(e.validator == "const" and list(e.path) == [field] for e in errors))

    def test_design_has_discrete_styles_and_no_fixed_profile_quota(self):
        value = self.design()
        self.validate_part("design", value)
        value["features"] = []
        self.validate_part("design", value)
        value["styles"]["influences"] = "Scandinavian; Farmhouse"
        with self.assertRaises(Exception):
            self.validate_part("design", value)

    def test_design_profile_accepts_open_types_and_validates_palette(self):
        value = self.design()
        color = {**claim("Putih gading"), "role": "Dominan", "hex": "#F0E8DA"}
        value.update(house_type=claim("Tower House", "uncertain"), palette=[color])
        self.validate_part("design", value)
        value["house_type"] = claim(None, "unknown")
        self.validate_part("design", value)
        for changes in ({"house_type": claim("Villa", "unknown")},
                        {"house_type": claim(None, "observed")},
                        {"palette": [dict(color, hex="red")]},
                        {"palette": [dict(color, evidence=[])]},
                        {"palette": [color] * 7}):
            with self.subTest(changes=changes), self.assertRaises(Exception):
                self.validate_part("design", {**value, **changes})

    def test_floor_area_is_required_positive_and_needs_no_basis(self):
        value = self.design()
        self.validate_part("design", value)
        for mutate in (
            lambda d: d["size"].pop("floor_area_m2"),
            lambda d: d["size"]["floor_area_m2"].pop("max"),
            lambda d: d["size"]["floor_area_m2"].update(min=0),
            lambda d: d["size"]["floor_area_m2"].update(max=-1),
        ):
            bad = copy.deepcopy(value)
            mutate(bad)
            with self.assertRaises(Exception):
                self.validate_part("design", bad)

    def test_claim_states_and_unassessed_confidence_are_not_defaulted(self):
        for state in ("observed", "uncertain", "not-visible", "not-present", "unknown"):
            value = claim("cabinet", state)
            before = copy.deepcopy(value)
            self.validate_part("claim", value)
            self.assertEqual(value, before)
            self.assertNotIn("confidence", value)
        bad = claim()
        bad.pop("state")
        with self.assertRaises(Exception):
            self.validate_part("claim", bad)

    def test_fact_category_does_not_require_parallel_coverage(self):
        value = {**claim("corner cabinet"), "subject": "cabinet", "attribute": "configuration",
                 "facet_roles": ["configuration"]}
        self.validate_part("fact", value)
        self.validate_part("category", {"text": "Kabinet sudut terlihat.", "facts": [value]})
        self.assertNotIn("id", value)
        self.assertNotIn("basis", value)

    def test_overlap_reentry_and_distinct_physical_area_ids(self):
        living = {"id": "living-1", "label": "living", "functions": ["living"],
                  "visible_intervals": [{"start_s": 0, "end_s": 0.7},
                                        {"start_s": 0.9, "end_s": 1.2}]}
        kitchen = {"id": "kitchen-1", "label": "kitchen", "functions": ["kitchen"],
                   "visible_intervals": [{"start_s": 0.4, "end_s": 1.2}]}
        self.validate_part("area", living)
        self.validate_part("area", kitchen)
        route = {"area_id": "living-1", "start_s": 0, "end_s": 1.2,
                 "connector": "awal", "focus": "living"}
        self.validate_part("route", route)
        self.assertNotEqual(route["end_s"], living["visible_intervals"][0]["end_s"])
        second = dict(living, id="living-2")
        self.validate_part("area", second)
        self.assertNotEqual(living["id"], second["id"])

    def test_tempo_can_change_inside_one_phase_and_numbers_are_optional(self):
        phase = {"start_s": 0, "end_s": 1.2, "notation": "Dolly-In + Pan Right",
                 "depth_direction": "IN", "focus": "bukaan", "evidence": [0, 11],
                 "observations": {"depth": "Jangkar membesar.",
                                  "translation": "Garis tepi membuka ruang.",
                                  "rotation": "Arah pandang berputar ke kanan."}}
        camera = {"description": "Kamera maju sambil memutar pandangan.",
                  "phases": [phase],
                  "tempo": {"description": "Sedang kemudian cepat.",
                            "segments": [{"start_s": 0, "end_s": 0.6, "label": "moderate",
                                          "description": "Sedang."},
                                         {"start_s": 0.6, "end_s": 1.2, "label": "fast",
                                          "description": "Cepat."}]}}
        self.validate_part("camera", camera)
        self.assertEqual(len(camera["phases"]), 1)
        self.assertNotIn("tempo", phase)
        self.assertNotIn("components_parsed", phase)

    def test_selections_do_not_repeat_mechanical_metadata(self):
        panel = {"frame_index": 11, "area_ids": ["kitchen-1"]}
        overview = dict(panel, composition_summary="Kamera serong dari bukaan kiri.")
        self.validate_part("panel", panel)
        self.validate_part("overview", overview)
        for forbidden in ("timestamp_s", "shot_id", "id"):
            with self.subTest(forbidden=forbidden), self.assertRaises(Exception):
                self.validate_part("panel", dict(panel, **{forbidden: 1}))

    def test_delivered_examples_retain_all_facts_and_omit_derivative_fields(self):
        for name, count in (("normal", 7), ("multi", 12)):
            value = json.loads((ROOT / "audit/examples" / name / "audit.json").read_text())
            Draft202012Validator(schema("audit")).validate(value)
            facts = [f for shot in value["shots"] for d in shot["design"]
                     for category in ("architecture", "furnishings", "environment")
                     for f in d[category]["facts"]]
            self.assertEqual(len(facts), count)
            self.assertNotIn("profile", value)
            shot = value["shots"][0]
            self.assertNotIn("camera_summary", shot)
            self.assertNotIn("components_parsed", shot["camera"]["phases"][0])
            self.assertTrue(any(f["state"] == "not-visible" for f in facts))
            self.assertTrue(any(f["state"] == "unknown" for f in facts))
            self.assertTrue(any(f["value"] == "Dinding berpanel sintetis" for f in facts))
