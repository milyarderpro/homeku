"""Active runtime must work independently of planning files and checkout paths."""
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import unittest
import zipfile
from pathlib import Path
from . import test_prepare
from .fixtures.factory import isolated_root, make_source
from homeku.audit_quality import camera_evidence
from homeku.audit_session import shot_camera_digests
from homeku.common import dumps, read_json
from homeku.derivations import referenced_frames
from tools import build_audit_kit as kit

ROOT = Path(__file__).resolve().parents[1]
LIBRARY_FILES = ["tools/library.py", "tools/build_audit_kit.py", "sources/design-principles.json",
                 "audit/concept-workflow.md"] + [
                     f"tools/homeku/{module}.py" for module in ("reader", "generation", "engine", "actions")]


class RepositoryIntegrityTests(test_prepare.VideoFixture, unittest.TestCase):
    def command(self, directory, *args, as_json=True):
        env = os.environ.copy()
        env.pop("PYTHONPATH", None)
        result = subprocess.run([sys.executable, "-B", *map(str, args)], cwd=directory,
                                env=env, capture_output=True, text=True, timeout=120)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return json.loads(result.stdout) if as_json else result.stdout

    def fixture_workflow(self, directory, source, work, name):
        work.mkdir(parents=True)
        cuts = work / "cuts.json"
        cuts.write_text("[]")
        audit_cli = "tools/audit.py"
        prepared = self.command(directory, audit_cli, "prepare", source, "--cuts-file", cuts,
                                "--output", work / "authoring")
        audit = read_json(directory / "audit/examples" / name / "audit.json")
        audit["id"] = source.stem
        path, info, session = map(Path, (prepared["audit"], prepared["audit_info"], prepared["session"]))
        phase_two = read_json(path)
        phase_two["shots"][0]["camera"] = audit["shots"][0]["camera"]
        phase_two["shots"][0]["composition"]["production_start"] = {
            "frame_index": 4, "composition_summary": "Arah serong setelah ambang.",
        }
        path.write_text(dumps(phase_two))

        def inspect_evidence(indices):
            state = read_json(session)
            available = {index for item in state["passes"] for index in item["record"]["selected_frame_indices"]}
            missing = sorted(set(indices) - available)
            if missing:
                self.command(directory, audit_cli, "sample", "--session", session, "--frames", *missing,
                             "--reason", "Inspect additional native fixture evidence")
            self.command(directory, audit_cli, "mark-viewed", session, "--all-passes", "--all")

        inspect_evidence(camera_evidence(phase_two["shots"][0]))
        checkpoint, = self.command(directory, audit_cli, "check-camera", session)["checked"]
        phase_two = read_json(path)
        self.assertEqual(phase_two["areas"], [])
        self.assertIsNone(phase_two["design"]["size"]["floor_area_m2"]["min"])

        audit["shots"][0]["camera"] = phase_two["shots"][0]["camera"]
        audit["shots"][0]["composition"]["production_start"] = phase_two["shots"][0]["composition"]["production_start"]
        path.write_text(dumps(audit))
        inspect_evidence(referenced_frames(audit))
        info.write_text(dumps({"method": "Synthetic fixture", "limitations": "Synthetic fixture",
                              "ai": {"provider": "fixture", "model": "fixture", "model_build": None}}))
        self.command(directory, audit_cli, "complete", path, "--session", session)
        self.assertTrue(self.command(directory, audit_cli, "check-input", source, path,
                                     "--audit-info", info, "--session", session)["ok"])
        draft = self.command(directory, audit_cli, "draft", source, path, "--audit-info", info,
                             "--output", work / "candidates", "--session", session, "--fixture")
        cards = self.command(directory, audit_cli, "review", draft["candidate"], "--output", work / "review.md")
        result = self.command(directory, audit_cli, "export", draft["candidate"],
                              "--receipt", cards["receipt"], "--output", work / "exports")
        self.assertEqual(draft["snapshot_sha256"], result["snapshot_sha256"])
        self.assertEqual(read_json(Path(cards["receipt"]))["snapshot_sha256"], result["snapshot_sha256"])
        with zipfile.ZipFile(result["package"]) as archive:
            prefix = source.stem + "/"
            shipped = json.loads(archive.read(prefix + "audit.json"))
            self.assertEqual(shot_camera_digests(shipped["shots"][0]), checkpoint["digests"])
            text = archive.read(prefix + "analysis.md").decode()
            self.assertIn("**Camera:** " + checkpoint["camera_movement"], text)
            self.assertIn("**Production Start:** F4", text)
            manifest = json.loads(archive.read(prefix + "manifest.json"))
            for media in manifest["media"]:
                self.assertEqual(hashlib.sha256(archive.read(prefix + media["path"])).hexdigest(),
                                 media["sha256"])
        return result

    def test_active_import_graph_has_no_legacy_modules_or_cycles(self):
        import ast
        modules = {p.stem: p for p in (ROOT / "tools/homeku").glob("*.py")}

        def legacy(name):
            return name in {"versions", "markdown"} or name.startswith(("media_v", "reporting_v"))

        self.assertFalse([name for name in modules if legacy(name)])
        graph = {module: set() for module in modules}
        for name, path in modules.items():
            for node in ast.walk(ast.parse(path.read_text(), filename=str(path))):
                if isinstance(node, ast.ImportFrom) and node.level:
                    targets = [node.module] if node.module else [alias.name for alias in node.names]
                    for target in targets:
                        key = target.split(".")[0]
                        self.assertFalse(legacy(key), (name, target))
                        if node.module:
                            self.assertIn(key, modules)
                        if key in modules:
                            graph[name].add(key)
        inspected = set()

        def visit(name, stack):
            self.assertNotIn(name, stack, " -> ".join((*stack, name)))
            if name not in inspected:
                for target in graph[name]:
                    visit(target, (*stack, name))
                inspected.add(name)

        for name in graph:
            visit(name, ())

    def test_kit_standalone_on_workspace_without_host_checkout(self):
        portable = self.work / "kit"
        portable.mkdir()
        with zipfile.ZipFile(io.BytesIO(kit.build_bytes())) as archive:
            archive.extractall(portable)
        self.command(portable, "homeku_runtime.py", "--output", portable)
        result = self.fixture_workflow(portable, make_source(self.work / "chat-source.mp4"),
                                       self.work / "workflow", "multi")
        with zipfile.ZipFile(result["package"]) as archive:
            self.assertEqual(len(archive.namelist()), 6)
        for name in ("docs", "openspec", "video"):
            self.assertFalse((portable / name).exists())

    def test_runtime_copy_without_docs_or_openspec_builds_kit_and_library(self):
        copy = self.work / "runtime"
        for name in [*kit.BUNDLED, *LIBRARY_FILES]:
            target = copy / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target)
        self.command(copy, "tools/build_audit_kit.py", as_json=False)
        self.command(copy, "tools/build_audit_kit.py", "--check", as_json=False)
        self.assertEqual((copy / "audit/homeku-audit-kit.zip").read_bytes(), kit.build_bytes())
        library = isolated_root(self.work / "library")
        source = make_source(library / "video/fixture-nodocs.mp4")
        exported = self.fixture_workflow(copy, source, self.work / "fixture", "normal")
        prefix = ("tools/library.py", "--root", library)
        self.assertEqual(self.command(copy, *prefix, "build")["references"], 0)
        result = self.command(copy, *prefix, "ingest", exported["package"])
        self.assertEqual(result["results"][0]["status"], "imported")
        self.assertEqual(self.command(copy, *prefix, "build", "--full")["changed"], [])
        self.assertEqual(self.command(copy, *prefix, "check")["references"], 1)
        self.assertEqual(self.command(copy, *prefix, "search", "--limit", 5)["results"][0]["id"],
                         "fixture-nodocs")
        self.assertEqual(self.command(copy, *prefix, "read", "fixture-nodocs", "--part", "shot",
                                      "--shot", "shot-01")["shot"]["composition"]["production_start"]["frame_index"], 4)
        self.assertIn("fixture-nodocs", (library / "catalogs/references.md").read_text())
        knowledge = read_json(library / "knowledge/topics/index.json")
        self.assertEqual(knowledge["schema_version"], "3.1")
        self.assertTrue(knowledge["topics"])
        self.assertFalse((copy / "docs").exists())
        self.assertFalse((copy / "openspec").exists())
