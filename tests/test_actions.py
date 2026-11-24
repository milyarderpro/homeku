"""Exercise Git retry against a local bare remote with canonical MP4s."""
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
from homeku.validation import CODE_ROOT
from .fixtures.factory import isolated_root, make_package


class GitPublicationTests(unittest.TestCase):
    def test_push_race_retries_from_latest_branch_and_keeps_both_packages(self):
        with tempfile.TemporaryDirectory() as name:
            work = Path(name)
            remote = work / "remote.git"
            subprocess.run(["git", "init", "--bare", "--initial-branch=main", str(remote)],
                           check=True, capture_output=True)
            root = isolated_root(work / "runner")
            for directory in ("tools", "schemas", "sources"):
                shutil.copytree(CODE_ROOT / directory, root / directory,
                                ignore=shutil.ignore_patterns("__pycache__"))
            shutil.copyfile(CODE_ROOT / ".gitignore", root / ".gitignore")
            (root / "references/README.md").write_text("Synthetic test library.\n")
            make_package(work / "source-a", root, "race-a", purpose="reference")
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
            make_package(work / "source-b", writer, "race-b", purpose="reference")

            def inject_push(attempt, checkout):
                if attempt == 1:
                    git(writer, "add", "incoming", "video")
                    git(writer, "commit", "-m", "second simultaneous upload")
                    git(writer, "push", "origin", "main")

            result = publish_actions(root, "main", work, before_push=inject_push)
            self.assertEqual(result["publish_attempt"], 2)
            published = json.loads(git(remote, "show", "main:data/registry.json").stdout)
            self.assertEqual(set(published["references"]), {"race-a", "race-b"})
            self.assertEqual(len(git(root, "worktree", "list", "--porcelain").stdout.split("worktree ")) - 1, 1)
