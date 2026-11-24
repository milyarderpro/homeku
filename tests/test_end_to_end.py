"""Normal/multi fixtures through authoring, reviewed bytes, publication and replay."""
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch
from . import test_prepare
from .fixtures.factory import isolated_root, make_inputs, make_source
from homeku.common import read_json
from homeku.derivations import resolve
from homeku.engine import check, ingest
from homeku.exporter import draft, export, review
from homeku.preflight import check_inputs
from homeku.reader import read_reference, extract_panel
from homeku.reporting import render_report


class EndToEndTests(test_prepare.VideoFixture, unittest.TestCase):
    def test_normal_and_multi_reviewed_sources_survive_ingest_and_replay(self):
        root = isolated_root(self.work / "library")
        packages = []
        for name in ("normal", "multi"):
            rid = "tested-" + name
            work = self.work / name
            source = make_source(root / "video" / (rid + ".mp4"))
            audit, logs = make_inputs(work / "authoring", source, multi=name == "multi")
            source_audit = read_json(audit)
            preflight = check_inputs(source, source_audit, logs, purpose="fixture")
            self.assertTrue(preflight["ok"], preflight["errors"])
            candidate = draft(source, audit, logs, work / "candidate", purpose="fixture")
            folder = Path(candidate["candidate"])
            receipt = review(folder, work / "review.md")
            packaged = export(folder, root / "incoming", receipt["receipt"])
            self.assertEqual(packaged["snapshot_sha256"], candidate["snapshot_sha256"])
            packages.append(Path(packaged["package"]))
        with patch("homeku.exporter.review", side_effect=AssertionError("ingest cannot ask for another review")):
            result = ingest(root, packages)
            self.assertEqual([row["status"] for row in result["results"]], ["imported", "imported"])
            replay = ingest(root, packages)
            self.assertEqual([row["status"] for row in replay["results"]], ["unchanged", "unchanged"])
        self.assertEqual(replay["changed"], [])
        self.assertEqual(check(root)["shots"], 2)
        for package in packages:
            with zipfile.ZipFile(package) as archive:
                rid = archive.namelist()[0].split("/")[0]
                for name in archive.namelist():
                    self.assertEqual((root / "references" / name).read_bytes(), archive.read(name))
            reference = root / "references" / rid
            audit = read_json(reference / "audit.json")
            manifest = read_json(reference / "manifest.json")
            self.assertEqual((reference / "analysis.md").read_text(), render_report(audit, manifest["frames"]))
            projection = read_reference(root, rid, part="full")
            for key, doc in projection["provenance"].items():
                if "source_pointer" in doc:
                    source = audit if doc["document"] == "audit" else manifest
                    self.assertEqual(resolve(projection, key), resolve(source, doc["source_pointer"]))
            path = self.work / (rid + ".png")
            panel = extract_panel(root, rid, manifest["selections"][0]["id"], path)
            self.assertTrue(path.is_file())
            self.assertEqual(panel["location"]["path"], "media/shot-01.jpg")
