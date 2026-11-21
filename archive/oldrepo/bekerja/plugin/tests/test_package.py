"""Checks for the actual private-release ZIP, not host behavior."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from shutil import copytree
from tempfile import TemporaryDirectory
import unittest
from zipfile import ZipFile

from test_project_rules import PLUGIN, WORKSPACE

SPEC = importlib.util.spec_from_file_location("home_productions_packaging", WORKSPACE / "tooling/package_plugin.py")
PACKAGER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PACKAGER)


class PluginArchiveTests(unittest.TestCase):
    def setUp(self):
        (WORKSPACE / "runs").mkdir(exist_ok=True)
        self.temp = TemporaryDirectory(dir=WORKSPACE / "runs")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "home-productions"
        copytree(PLUGIN, self.source)
        self.output = self.root / "release.zip"

    def test_archive_is_complete_deterministic_and_contains_only_plugin_source(self):
        first = PACKAGER.build_archive(self.source, self.output)
        second = PACKAGER.build_archive(self.source, self.root / "repeat.zip")
        self.assertEqual(first["sha256"], second["sha256"])
        expected = {str(path.relative_to(self.source)) for path in self.source.rglob("*") if path.is_file()}
        with ZipFile(self.output) as archive:
            self.assertEqual(set(archive.namelist()), expected)
            self.assertIn("plugin.json", archive.namelist())
            self.assertIn("skills/produce-home-tour/SKILL.md", archive.namelist())
            self.assertIsNone(archive.testzip())
            for name in archive.namelist():
                self.assertEqual(archive.read(name), (self.source / name).read_bytes())
                self.assertEqual(archive.getinfo(name).external_attr >> 16, 0o100644)
        self.assertEqual(first["skills"], ["produce-home-tour"])
        self.assertFalse({"README.md", "implementation-plan.md", "knowledge/", "tests/"} & expected)

    def test_development_files_and_symlinks_are_rejected(self):
        for relative in (".env", "skills/produce-home-tour/__pycache__/stale.pyc", "README.md"):
            with self.subTest(relative=relative):
                path = self.source / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b"unrelated fixture")
                with self.assertRaises(ValueError):
                    PACKAGER.build_archive(self.source, self.output)
                self.assertFalse(self.output.exists())
                path.unlink()
                if "__pycache__" in path.parts:
                    path.parent.rmdir()
        (self.source / "skills/produce-home-tour/scripts/link.py").symlink_to(self.root / "outside.py")
        with self.assertRaisesRegex(ValueError, "Symlinks"):
            PACKAGER.build_archive(self.source, self.output)

    def test_missing_or_escaping_skill_references_are_rejected(self):
        skill = self.source / "skills/produce-home-tour/SKILL.md"
        original = skill.read_text()
        for href in ("references/missing.md", "../../../outside.md"):
            with self.subTest(href=href):
                skill.write_text(original + f"\n[missing]({href})\n")
                with self.assertRaisesRegex(ValueError, "packaged reference"):
                    PACKAGER.build_archive(self.source, self.output)
                self.assertFalse(self.output.exists())
        skill.write_text(original)

    def test_manifest_and_skill_identity_are_checked_before_packaging(self):
        path = self.source / "plugin.json"
        original = json.loads(path.read_text())
        bad = json.loads(path.read_text())
        bad["extensions"]["com.openai"]["interface"]["shortDescription"] = "x" * 31
        path.write_text(json.dumps(bad))
        with self.assertRaisesRegex(ValueError, "shortDescription"):
            PACKAGER.build_archive(self.source, self.output)
        path.write_text(json.dumps(original))
        skill = self.source / "skills/produce-home-tour/SKILL.md"
        skill.write_text(skill.read_text().replace("name: produce-home-tour", "name: unrelated", 1))
        with self.assertRaisesRegex(ValueError, "Skill name"):
            PACKAGER.build_archive(self.source, self.output)
        self.assertFalse(self.output.exists())

    def test_existing_archive_is_not_overwritten(self):
        self.output.write_bytes(b"old release")
        with self.assertRaises(FileExistsError):
            PACKAGER.build_archive(self.source, self.output)
        self.assertEqual(self.output.read_bytes(), b"old release")

    def test_archive_cannot_be_written_into_plugin_source(self):
        with self.assertRaisesRegex(ValueError, "outside"):
            PACKAGER.build_archive(self.source, self.source / "release.zip")
        self.assertFalse((self.source / "release.zip").exists())


if __name__ == "__main__":
    unittest.main()
