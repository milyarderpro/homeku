"""Design Intelligence knowledge and source-provenance regression tests."""
from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path
import json

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from refresh_design_catalog import read_references, verify_catalog, render_catalog, markdown_rows

KNOWLEDGE = ROOT / "knowledge"
THEMES = (
    "README.md", "methodology.md", "dna-summary.md", "reference-catalog.md",
    "architecture-dna.md", "landscape-dna.md", "interior-dna.md",
    "spatial-design-principles.md", "cinematography-dna.md",
    "design-compatibility.md", "originality-framework.md",
    "ai-knowledge.md", "access-contract.md", "taxonomy/README.md", "directories/README.md",
)
VALID_CLAIM_TYPES = {"OBSERVATION", "AGGREGATE", "INFERENCE", "DESIGN_PRINCIPLE"}
PATH_RE = re.compile(r"^shots\[(\d+)\](?:\.(.+))?$")


def resolve_field(document: dict, path: str):
    match = PATH_RE.match(path)
    if match:
        value = document["shots"][int(match.group(1))]
        pieces = (match.group(2) or "").split(".")
    else:
        value = document
        pieces = path.split(".")
    for piece in pieces:
        if piece:
            value = value[piece]
    return value


class DesignIntelligenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.references = read_references(published=True)

    def test_catalog_metadata_and_coverage(self):
        count, shots = verify_catalog()
        release = json.loads((KNOWLEDGE / "release.json").read_text())
        self.assertEqual(count, release["reference_count"])
        self.assertEqual(shots, release["shot_count"])


    def test_active_analyses_have_no_manual_verification_metadata(self):
        for ident, doc in self.references.items():
            self.assertNotIn("human_verified", doc["analysis_quality"], ident)
            report = (ROOT / "references" / ident / "analysis.md").read_text()
            self.assertNotIn("Verifikasi manusia", report, ident)
            self.assertNotIn("Diverifikasi manusia", report, ident)

    def test_catalog_refresh_renderer_is_complete(self):
        refreshed = markdown_rows(render_catalog())
        self.assertEqual(set(refreshed), set(self.references))

    def test_every_source_has_traceable_design_profile(self):
        profile_root = KNOWLEDGE / "reference-profiles"
        for ident, doc in self.references.items():
            profile = profile_root / (ident + ".md")
            self.assertTrue(profile.is_file(), ident)
            section = profile.read_text()
            self.assertIn(doc["architecture"]["primary_style"], section)
            self.assertIn(doc["architecture"]["building_scale"]["perceived_size"], section)
            self.assertIn(f"../../references/{ident}/analysis.yaml", section)
            for feature in doc["architecture"]["exterior_features"][:4]:
                self.assertIn(feature, section)
        # Older group URLs and heading anchors still lead to individual profiles.
        for old in profile_root.glob("[0-9][0-9]-*.md"):
            for ident in re.findall(r"### \[([^]]+)\]", old.read_text()):
                self.assertTrue((profile_root / (ident + ".md")).is_file())

    def test_knowledge_documents_present(self):
        for filename in THEMES:
            self.assertTrue((KNOWLEDGE / filename).is_file(), filename)

    def test_evidence_records_refer_to_real_fields(self):
        evidence = yaml.safe_load((KNOWLEDGE / "evidence-index.yaml").read_text(encoding="utf-8"))
        self.assertEqual(str(evidence["schema_version"]), "2.0")
        items = evidence["records"]
        self.assertGreaterEqual(len(items), 20)
        ids = [item["id"] for item in items]
        self.assertEqual(len(ids), len(set(ids)))
        for item in items:
            self.assertIn(item["claim_type"], VALID_CLAIM_TYPES)
            self.assertIn(item["confidence"], {"low", "medium", "high"})
            self.assertTrue(item["statement"])
            self.assertTrue(item["limitations"])
            self.assertTrue(item["sources"])
            for source in item["sources"]:
                ident = source["reference_id"]
                self.assertIn(ident, self.references)
                doc = self.references[ident]
                sid = source["shot_id"]
                self.assertIn(sid, [shot["id"] for shot in doc["shots"]])
                field = source["field_path"]
                result = resolve_field(doc, field)
                self.assertIsNotNone(result, (ident, field))
                if field.startswith("shots["):
                    index = int(PATH_RE.match(field).group(1))
                    self.assertEqual(doc["shots"][index]["id"], sid)

    def test_knowledge_entrypoint_lists_all_themes(self):
        readme = (KNOWLEDGE / "README.md").read_text(encoding="utf-8")
        for filename in THEMES:
            if filename == "README.md":
                continue
            self.assertIn("](" + filename + ")", readme, filename)
        self.assertIn("reference-profiles/README.md", readme)

    def test_local_markdown_links_resolve(self):
        link = re.compile(r"\]\(([^)]+)\)")
        for file in [ROOT / "README.md", *KNOWLEDGE.rglob("*.md")]:
            for relative in link.findall(file.read_text(encoding="utf-8")):
                if relative.startswith(("http:", "https:", "#")):
                    continue
                local = relative.split("#", 1)[0]
                if not local:
                    continue
                self.assertTrue((file.parent / local).exists(), f"{file}: {relative}")

    def test_production_rules_not_active(self):
        forbidden = [
            ROOT / "rules" / "workflow-production.md",
            ROOT / "templates" / "production.md",
            ROOT / "docs" / "production-lite-v1.1-implementation-plan.md",
        ]
        for file in forbidden:
            self.assertFalse(file.exists(), str(file))
        for file in KNOWLEDGE.glob("*.md"):
            text = file.read_text(encoding="utf-8")
            self.assertNotIn("workflow-production.md", text)
            self.assertNotIn("templates/production.md", text)
            self.assertNotIn("Omni Flash", text)


if __name__ == "__main__":
    unittest.main()
