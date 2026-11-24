"""Exercise capacity on 300 valid synthetic models with native media and sources."""
import copy
import struct
import unittest
from pathlib import Path
from unittest.mock import patch
from . import test_prepare
from .fixtures.factory import isolated_root, make_inputs, make_source
from homeku.common import dumps, read_json, sha256, snapshot_hash
from homeku.derivations import selections
from homeku.engine import build
from homeku.exporter import draft
from homeku.media import build_media
from homeku.reader import read_reference, search
from homeku.reporting import render_report
from homeku.video import extract_frame

ROOT = Path(__file__).resolve().parents[1]


class CapacityTests(test_prepare.VideoFixture, unittest.TestCase):
    def test_300_models_match_full_and_incremental_with_selective_pages(self):
        root = isolated_root(self.work / "library")
        production_registry = sha256(ROOT / "data/registry.json")
        source = make_source(self.work / "seed.mp4")
        audit_path, logs = make_inputs(self.work / "authoring", source)
        result = draft(source, audit_path, logs, self.work / "seed-candidate", purpose="fixture")
        folder = Path(result["candidate"])
        audit = read_json(folder / "audit.json")
        template = read_json(folder / "manifest.json")
        pts, source_bytes = template["frames"], source.read_bytes()
        frames = {p["frame_index"]: extract_frame(source, p["frame_index"], 0)
                  for p in template["selections"]}
        registry = {}
        with patch("homeku.media.extract_frame", side_effect=lambda source, i, stream: frames[i]):
            for number in range(300):
                rid = f"capacity-{number:03d}"
                native = root / "video" / (rid + ".mp4")
                # A valid free box varies the source hash without changing video frames or PTS.
                tag = rid.encode()
                native.write_bytes(source_bytes + struct.pack(">I4s", len(tag) + 8, b"free") + tag)
                reference = root / "references" / rid
                reference.mkdir()
                audit_copy = {**audit, "id": rid}
                manifest = copy.deepcopy(template)
                manifest.update(id=rid, selections=list(selections(audit_copy, pts)))
                manifest["source"].update(path=f"video/{rid}.mp4", sha256=sha256(native))
                manifest["media"] = build_media(reference, audit_copy, native, manifest["source"],
                                                 manifest["render"], pts)
                (reference / "audit.json").write_text(dumps(audit_copy))
                (reference / "analysis.md").write_text(render_report(audit_copy, pts))
                manifest["audit_sha256"] = sha256(reference / "audit.json")
                (reference / "manifest.json").write_text(dumps(manifest))
                digest = snapshot_hash(reference)
                # Directly seed fixture registry entries so capacity measures build/reader.
                registry[rid] = {"revision": 1, "contract_version": "3.0", "content_sha256": digest,
                                 "package_sha256": digest, "audit_sha256": manifest["audit_sha256"],
                                 "source_sha256": manifest["source"]["sha256"],
                                 "analysis_sha256": sha256(reference / "analysis.md"),
                                 "manifest_sha256": sha256(reference / "manifest.json")}
        (root / "data/registry.json").write_text(dumps({"version": 1, "references": registry}))
        self.assertEqual(build(root, full=True)["references"], 300)
        with patch("homeku.generation.validate_folder", side_effect=AssertionError("expected verified cache reuse")):
            incremental = build(root)
        self.assertEqual(incremental["changed"], [])
        self.assertEqual(incremental["shots"], 300)
        index_path = root / "data/search-index.json"

        def read_search_file(path):
            self.assertNotIn("projections", path.parts)
            return read_json(path)

        with patch("homeku.reader.read_json", side_effect=read_search_file):
            page = search(root, area=["kamar mandi"], offset=280, limit=17)
        self.assertEqual(page["total"], 300)
        self.assertEqual(len(page["results"]), 17)
        self.assertEqual(page["results"][0]["id"], "capacity-280")
        self.assertEqual(page["next_offset"], 297)
        self.assertEqual(len(search(root, offset=297)["results"]), 3)
        with patch("homeku.reader.read_json", wraps=read_json) as reads:
            result = read_reference(root, "capacity-280", part="shot", shot="shot-01")
        self.assertEqual(result["id"], "capacity-280")
        projections = [args.args[0].name for args in reads.call_args_list if "projections" in args.args[0].parts]
        self.assertEqual(projections, ["capacity-280.json"])
        self.assertNotIn("frame_reviews", index_path.read_text())
        self.assertNotIn("observations", index_path.read_text())
        self.assertLess(index_path.stat().st_size, 3 * 1024 * 1024)
        self.assertEqual(sha256(ROOT / "data/registry.json"), production_registry)
        print(f"Capacity fixture: 300 references, {index_path.stat().st_size:,} index bytes")
