"""Source-backed contract replays and skill resources; not a live model evaluation.

The test runner reads repository YAML only to replay the two stage-3 acceptance
cases. Runtime source access remains GitHub URLs or the connector. Source bytes
were also fetched remotely and matched at COMMIT during implementation.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from urllib.parse import unquote, urlsplit

import yaml

from test_project_rules import PLUGIN, SKILL, VALIDATOR, WORKSPACE, blank, planning

REPOSITORY = WORKSPACE.parents[1]
COMMIT = "26c5e56cb0de66d5c1ab4f93a1285654180382a0"
SOURCE_HASHES = {
    "edh022": "dbb8bbd420ad738c49c72fd64e163e157b271c5753599afaac6464d6294229d9",
    "edh035": "ecf78f98ccd294aa60e301f8eaa26f1a02f09c56f83cf37a8069311a62877d96",
}
CASES = {
    # The source has a closing exterior shot; it is omitted to avoid repetition.
    "edh022": (("exterior", "living_to_kitchen", "bedroom", "bathroom"), 20),
    "edh035": (("exterior_to_living", "kitchen", "bedroom", "bathroom"), 18),
}
SOURCE_AREAS = {
    "exterior_front": ["exterior"],
    "combined_living_room_and_kitchen": ["living", "kitchen"],
    "exterior_front_to_living_room": ["exterior", "living"],
    "kitchen": ["kitchen"],
    "bedroom": ["bedroom"],
    "bathroom": ["bathroom"],
}


def source_case(reference_id):
    """Replay actual annotation structure; numeric camera choices remain adaptations."""
    raw = (REPOSITORY / "references" / reference_id / "analysis.yaml").read_bytes()
    if hashlib.sha256(raw).hexdigest() != SOURCE_HASHES[reference_id]:
        raise AssertionError("Source changed; review and repin the acceptance snapshot.")
    source = yaml.safe_load(raw)
    kinds, _ = CASES[reference_id]
    project = planning(kinds)
    project["project_id"] = "test-" + reference_id
    project["knowledge"].update(ref=None, commit=COMMIT, route="github_connector")
    project["knowledge"]["evidence"] = []
    project["design"].update(
        architecture=source["architecture"]["primary_style"],
        materials=", ".join(source["architecture"]["interior_style"]),
        lighting=", ".join(source["visual_style"]["lighting"]),
        environment=", ".join(source["visual_style"]["setting"]),
        ceiling="Test project decision; no measured source geometry is claimed.",
        connections=["Test adaptation of the annotated area connection."],
        anchors=source["architecture"]["exterior_features"][:2],
    )
    project["revision_notes"] = [
        "6/4-second duration, travel estimates and 12-degree pan are test project adaptations.",
        "Compound source labels do not prove the original timing relationship.",
        "Bedroom three-quarter/40-degree composition is a user preference adaptation, not a measured source angle.",
    ]
    for index, shot in enumerate(project["shots"]):
        annotated = source["shots"][index]
        project["knowledge"]["evidence"].append({
            "evidence_id": shot["evidence_ids"][0], "reference_id": reference_id,
            "shot_ids": [annotated["id"]],
            "analysis_url": f"https://github.com/milyarderpro/homeku/blob/{COMMIT}/references/{reference_id}/analysis.yaml",
            "field_paths": [f"/shots/{index}/scene", f"/shots/{index}/framing/start",
                            f"/shots/{index}/framing/end", f"/shots/{index}/camera/movements",
                            f"/shots/{index}/observation_note", f"/shots/{index}/transition_out"],
            "excerpt": annotated["scene"] + " | " + annotated["observation_note"],
            "covered_areas": SOURCE_AREAS[annotated["scene"]].copy(),
            "continuity": "annotated_continuous", "access_status": "read", "error": None,
        })
        shot["framing"] = {key: annotated["framing"][key] for key in ("start", "end")}
        shot["camera"]["description"] = "Test adaptation of source labels: " + ", ".join(annotated["camera"]["movements"])
    return project, source


class SourcePlanningTests(unittest.TestCase):
    def check_source_case(self, reference_id):
        project, source = source_case(reference_id)
        _, expected = CASES[reference_id]
        result = VALIDATOR.validate_project(project)
        self.assertTrue(result["valid"], result)
        self.assertEqual(result["total_duration_s"], expected)
        self.assertEqual(len(project["shots"]), 4)
        self.assertEqual(len(project["image_plan"]), 4)
        areas = [area for shot in project["shots"] for area in shot["covered_areas"]]
        self.assertEqual(len(areas), len(set(areas)))
        self.assertEqual(areas.count("kitchen"), 1)
        self.assertEqual(areas.count("bedroom"), 1)
        self.assertEqual(project["assets"], [])
        self.assertTrue(all(value is None for value in project["approvals"].values()))
        for evidence in project["knowledge"]["evidence"]:
            for pointer in evidence["field_paths"]:
                value = source
                for part in pointer.strip("/").split("/"):
                    value = value[int(part)] if isinstance(value, list) else value[part]
                self.assertTrue(value)
            index = int(evidence["shot_ids"][0].split("-")[1]) - 1
            self.assertIn(source["shots"][index]["observation_note"], evidence["excerpt"])
        (WORKSPACE / "runs").mkdir(exist_ok=True)
        with TemporaryDirectory(dir=WORKSPACE / "runs") as directory:
            path = Path(directory) / "project.json"
            path.write_text(json.dumps(project), encoding="utf-8")
            run = subprocess.run(
                [sys.executable, "-B", str(SKILL / "scripts/validate_project.py"), str(path)],
                capture_output=True, text=True,
            )
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertEqual(json.loads(run.stdout)["total_duration_s"], expected)
            # The same record cannot move into visual production without a decision.
            next_stage = deepcopy(project)
            next_stage["stage"] = "image_draft"
            self.assertFalse(VALIDATOR.validate_project(next_stage)["valid"])

    def test_living_kitchen_source_plan_is_twenty_seconds(self):
        self.check_source_case("edh022")

    def test_exterior_living_source_plan_is_eighteen_seconds(self):
        self.check_source_case("edh035")


class SkillResourcesTests(unittest.TestCase):
    def test_discovery_metadata_matches_skill_folder(self):
        text = (SKILL / "SKILL.md").read_text()
        self.assertTrue(text.startswith("---\n"))
        metadata = yaml.safe_load(text.split("---", 2)[1])
        self.assertEqual(metadata["name"], SKILL.name)
        self.assertIsInstance(metadata["description"], str)
        ui = yaml.safe_load((SKILL / "agents/openai.yaml").read_text())["interface"]
        self.assertTrue(ui["display_name"].strip())
        self.assertTrue(25 <= len(ui["short_description"]) <= 64)

    def test_all_packaged_markdown_links_resolve_inside_plugin(self):
        links = []
        root = PLUGIN.resolve()
        for document in PLUGIN.rglob("*.md"):
            for href in re.findall(r"\[[^\]]*\]\(([^)]+)\)", document.read_text()):
                parsed = urlsplit(href)
                if parsed.scheme or not parsed.path:
                    continue
                target = (document.parent / unquote(parsed.path)).resolve()
                self.assertTrue(target.is_relative_to(root), (document, href))
                self.assertTrue(target.is_file(), (document, href))
                links.append(target)
        self.assertIn((SKILL / "references/repo-access.md").resolve(), links)
        self.assertIn((SKILL / "references/preproduction.md").resolve(), links)


if __name__ == "__main__":
    unittest.main()
