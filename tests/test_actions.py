"""Exercise the real Git retry path against a disposable local bare remote."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from homeku.actions import git, publish_actions
from homeku.common import dumps, read_json
from homeku.validation import CODE_ROOT
from tests.fixtures.factory import copy_fixture, isolated_root, make_folder, package_folder


class GitPublicationTests(unittest.TestCase):
    def test_concurrent_git_push_retries_from_latest_snapshot_and_keeps_both_zips(self):
        with tempfile.TemporaryDirectory() as name:
            work = Path(name)
            remote = work / "remote.git"
            subprocess.run(["git", "init", "--bare", "--initial-branch=main", str(remote)], check=True, capture_output=True)
            root = isolated_root(work / "runner")
            for directory in ("tools", "docs/contracts", "sources"):
                shutil.copytree(CODE_ROOT / directory, root / directory, ignore=shutil.ignore_patterns("__pycache__"))
            shutil.copyfile(CODE_ROOT / ".gitignore", root / ".gitignore")
            (root / "references").mkdir()
            (root / "references/README.md").write_text("Temporary test library only.")
            template = make_folder(work / "template")
            def make_zip(parent, rid, target):
                folder = copy_fixture(parent, rid, template)
                manifest = read_json(folder / "manifest.json")
                # Simulate the production-purpose contract only inside this
                # disposable bare repo; the real library is never touched.
                manifest["purpose"] = "reference"
                (folder / "manifest.json").write_text(dumps(manifest))
                return package_folder(folder, target / f"{rid}-r0001.zip")
            make_zip(work / "source-a", "race-a", root / "incoming")
            git(root, "init", "-b", "main")
            git(root, "config", "user.name", "Fixture")
            git(root, "config", "user.email", "fixture@example.invalid")
            git(root, "add", ".")
            git(root, "commit", "-m", "synthetic test baseline")
            git(root, "remote", "add", "origin", str(remote))
            git(root, "push", "origin", "main")
            writer = work / "other-writer"
            subprocess.run(["git", "clone", str(remote), str(writer)], check=True, capture_output=True)
            git(writer, "config", "user.name", "Other fixture")
            git(writer, "config", "user.email", "other@example.invalid")
            def inject_push(attempt, checkout):
                if attempt == 1:
                    make_zip(work / "source-b", "race-b", writer / "incoming")
                    git(writer, "add", "incoming")
                    git(writer, "commit", "-m", "second simultaneous upload")
                    git(writer, "push", "origin", "main")
            result = publish_actions(root, "main", work, before_push=inject_push)
            self.assertEqual(result["publish_attempt"], 2)
            published = json.loads(git(remote, "show", "main:data/registry.json").stdout)
            self.assertEqual(set(published["references"]), {"race-a", "race-b"})
            self.assertEqual(len(git(remote, "worktree", "list", "--porcelain").stdout.split("worktree ")) - 1, 1)
