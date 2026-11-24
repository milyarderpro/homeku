"""Generate from explicit source facts with no prose inference."""
import json
import unittest
from pathlib import Path
from . import test_prepare
from homeku.common import read_json
from homeku.derivations import frame_map, selections
from homeku.generation import render
from homeku.media import expected_media
from homeku.render_assets import render_config

ROOT = Path(__file__).resolve().parents[1]
TIMES = [i / 10 for i in range(12)]


def model(name):
    audit = read_json(ROOT / "audit/examples" / name / "audit.json")
    rid = audit["id"]
    manifest = {"source": {"path": f"video/{rid}.mp4", "sha256": "1" * 64, "duration_s": 1.2,
                           "width": 96, "height": 160, "fps": {"numerator": 10, "denominator": 1},
                           "video_stream_index": 0},
                "frames": frame_map(audit, TIMES), "selections": list(selections(audit, TIMES)), "media": []}
    manifest["media"] = [{**row, "sha256": "2" * 64}
                         for row, _, _ in expected_media(audit, manifest["source"], render_config(), TIMES)]
    return {"id": rid, "revision": 1, "audit": audit, "manifest": manifest, "content_sha256": "a" * 64}


class GenerationTests(unittest.TestCase):
    def test_facts_states_scope_notes_and_facets_come_from_source(self):
        item = model("normal")
        audit = item["audit"]
        arch = audit["shots"][0]["design"][0]["architecture"]
        arch["text"] += " Tidak boleh menjadi fakta otomatis."
        fact = arch["facts"][0]
        fact.update(value="Brand new layout", note="Jenis layout belum pasti.", state="uncertain")
        fact.pop("confidence")
        outputs = render(ROOT, {item["id"]: item})
        index = json.loads(outputs["data/search-index.json"])
        shot = index["references"][0]["shots"][0]
        explicit = next(f for f in shot["design_facets"] if f["attribute"] == "layout")
        self.assertEqual(explicit["value"], "Brand new layout")
        self.assertEqual(explicit["state"], "uncertain")
        self.assertNotIn("confidence", explicit)
        self.assertEqual(explicit["area_ids"], ["bath-1"])
        claims = [row for name, contents in outputs.items()
                  if name.startswith("knowledge/comparisons/") and "/page-" in name and name.endswith(".json")
                  for row in json.loads(contents)["claims"]]
        self.assertTrue(any(c["fact"].get("note") == fact["note"] for c in claims))
        self.assertTrue(any(c["fact"]["state"] == "not-visible" for c in claims))
        self.assertTrue(any(c["fact"]["domain"] == "new-domain" for c in claims))
        self.assertEqual(len(claims), 7)
        self.assertNotIn("Tidak boleh menjadi fakta otomatis", "".join(
            text for name, text in outputs.items() if name.startswith("knowledge/")))

    def test_empty_registry_output_and_explicit_profile_categories(self):
        empty = render(ROOT, {})
        self.assertEqual(json.loads(empty["data/search-index.json"])["references"], [])
        item = model("multi")
        output = render(ROOT, {item["id"]: item})
        index = json.loads(output["data/search-index.json"])["references"][0]
        self.assertTrue({"primary-style", "style-influence", "interior-style", "apparent-scale", "massing"} <=
                        {facet["aspect"] for facet in index["profile_facets"]})
        self.assertEqual(index["shots"][0]["route"], ["living", "kitchen"])

    def test_projection_pointers_resolve_audit_and_manifest(self):
        from homeku.derivations import resolve
        for name in ("normal", "multi"):
            item = model(name)
            generated = render(ROOT, {item["id"]: item})
            payload = json.loads(generated[f"data/projections/{item['id']}.json"])
            index = json.loads(generated["data/search-index.json"])["references"][0]
            pointers = payload["provenance"]
            for key, info in pointers.items():
                value = resolve(payload, key)
                document = item[info["document"]]
                if "source_pointer" in info:
                    self.assertEqual(value, resolve(document, info["source_pointer"]))
                else:
                    self.assertTrue(info["inputs"])
                    for pointer in info["inputs"]:
                        self.assertIsNotNone(resolve(document, pointer))
            for entry in index["profile_facets"] + index["style_relations"] + index["shots"][0]["design_facets"]:
                self.assertIsInstance(resolve(item["audit"], entry["source_pointer"]), dict)
            self.assertIn("/reference/shots/0/camera/tempo/segments/1", pointers)
            self.assertIn("/reference/shots/0/camera/phases/0/observations", pointers)
            self.assertIn("/evidence_inventory/frames/2", pointers)
            self.assertIn("/evidence_inventory/media/2", pointers)
            self.assertIn("/derived/shots/0", pointers)
            if name == "multi":
                self.assertIn("/reference/shots/0/area_relations/0", pointers)
                self.assertIn("/reference/shots/0/route/1", pointers)
