"""Homeku v1.4 filename-based, independent runner and retry regression tests."""
from __future__ import annotations

import copy
import json
import time
from concurrent.futures import ThreadPoolExecutor
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from parallel_save import (
    SaveConflict, check_case_collisions, check_remote_case_collisions, event_request_path, filename_id,
    find_archive, inspect_remote, load_request, publish, remote_request_sha,
    render, request_id_from_path, request_path_for_video,
)
from test_action_save import ActionSaveTests
from test_validation import make_package
from validate_analysis import validate


def git(root, *args):
    return subprocess.check_output(
        ["git", *args], cwd=root, text=True, stderr=subprocess.PIPE
    ).strip()


class ParallelSaveTests(unittest.TestCase):
    def setUp(self):
        # Reuse the real two-shot FFmpeg fixture, but never write into production.
        self.fixture = ActionSaveTests("test_idle_request_does_nothing")
        self.fixture.setUp()
        self.root = self.fixture.root
        self.fixture.add_narratives()
        self.req = copy.deepcopy(self.fixture.req)
        self.pending = self.root / "requests/pending"
        self.pending.mkdir(parents=True)
        (self.root / "requests/results").mkdir()
        self.req_path = "requests/pending/test.json"
        self.write_request()

    def tearDown(self):
        self.fixture.tearDown()

    def write_request(self, request=None):
        (self.root / self.req_path).write_text(
            json.dumps(request or self.req, ensure_ascii=False), encoding="utf-8"
        )

    def commit_requests(self):
        git(self.root, "add", "requests/pending", "video")
        git(self.root, "commit", "-qm", "add reviewed parallel requests")
        return git(self.root, "rev-parse", "HEAD")

    def add_remote(self):
        remote = self.root / "origin.git"
        subprocess.run(["git", "init", "-q", "--bare", str(remote)], check=True)
        git(self.root, "remote", "add", "origin", str(remote))
        git(self.root, "push", "-q", "origin", "HEAD:main")
        return remote

    def test_filename_id_and_contract(self):
        self.assertEqual(filename_id("video/edh011.mp4"), "edh011")
        self.assertEqual(filename_id("video/dreamsHouse003.mp4"), "dreamsHouse003")
        self.assertEqual(request_id_from_path("requests/pending/edh011.json"), "edh011")
        self.assertEqual(request_path_for_video("video/edh011.mp4"),
                         "requests/pending/edh011.json")
        for path in ("video/../bad.mp4", "video/Foo.MP4", "video/a b.mp4",
                     "video/a/b.mp4", "video/PENDING.mp4", "video/VID-001.mp4",
                     "video/.hidden.mp4", "other/edh001.mp4"):
            with self.subTest(path=path), self.assertRaises(SaveConflict):
                filename_id(path)

    def test_valid_request_load(self):
        vid, req, data, narratives, times = load_request(self.root, self.req_path)
        self.assertEqual(vid, "test")
        self.assertEqual(req["request_id"], self.req["request_id"])
        self.assertEqual(data["video"]["id"], "PENDING")
        self.assertEqual(len(narratives), 2)
        self.assertEqual(times, [1, 4])

    def test_reject_missing_narratives(self):
        self.req.pop("shot_narratives")
        self.write_request()
        with self.assertRaisesRegex(SaveConflict, "requires shot_narratives"):
            load_request(self.root, self.req_path)

    def test_invalid_sha_fails_before_render(self):
        self.req["video"]["blob_sha"] = "0" * 40
        self.write_request()
        with self.assertRaisesRegex(SaveConflict, "SHA mismatch"):
            render(self.root, self.req_path)
        self.assertFalse((self.root / "references/test").exists())

    def test_mismatched_filename_id(self):
        self.req["video"]["path"] = "video/other.mp4"
        self.write_request()
        with self.assertRaisesRegex(SaveConflict, "Request ID differs"):
            load_request(self.root, self.req_path)

    def test_case_collision(self):
        (self.root / "video/Test.MP4").write_bytes(b"not a video")
        with self.assertRaisesRegex(SaveConflict, "Case collision"):
            check_case_collisions(self.root, "test")
        with self.assertRaisesRegex(SaveConflict, "Case collision"):
            load_request(self.root, self.req_path)

    def test_invalid_keyframe_and_narrative(self):
        self.req["keyframe_times_s"] = [3.9, 4.0]
        self.write_request()
        with self.assertRaisesRegex(SaveConflict, "Keyframe outside"):
            load_request(self.root, self.req_path)
        self.req["keyframe_times_s"] = [1.0, 4.0]
        self.req["shot_narratives"]["shot-01"]["architectural"]["covered_indices"] = []
        self.write_request()
        with self.assertRaisesRegex(ValueError, "covered_indices"):
            load_request(self.root, self.req_path)

    def test_legacy_duplicate_protected(self):
        legacy = make_package(self.root / "references", vid="VID-007")
        self.assertEqual(find_archive(self.root, "test.mp4"), "VID-007")
        out = render(self.root, self.req_path)
        self.assertEqual(out["status"], "already_saved")
        self.assertEqual(out["video_id"], "VID-007")
        self.assertFalse((self.root / "references/test").exists())
        self.assertTrue((legacy / "analysis.yaml").exists())

    def test_corrupt_legacy_fails_closed(self):
        folder = self.root / "references/VID-001"
        folder.mkdir()
        (folder / "analysis.yaml").write_text("not: [valid", encoding="utf-8")
        with self.assertRaisesRegex(SaveConflict, "Invalid existing archive"):
            find_archive(self.root, "test.mp4")

    def test_generate_five_files_and_safe_replay(self):
        result = render(self.root, self.req_path)
        self.assertEqual(result["status"], "saved")
        self.assertEqual(result["video_id"], "test")
        self.assertEqual(result["file_count"], 5)
        folder = self.root / "references/test"
        self.assertEqual(validate(folder, "test")["shot_count"], 2)
        self.assertEqual(yaml.safe_load((folder/"analysis.yaml").read_text())["video"]["id"],
                         "test")
        self.assertIn("<!-- homeku_detail_narratives: chat-reviewed -->",
                      (folder/"analysis.md").read_text())
        self.assertEqual(render(self.root, self.req_path)["status"], "already_saved")

    def test_push_event_requires_one_added_request(self):
        before = git(self.root, "rev-parse", "HEAD")
        after = self.commit_requests()
        event = {"ref": "refs/heads/main", "before": before, "after": after}
        self.assertEqual(event_request_path(self.root, event, "push", after), self.req_path)
        self.assertEqual(event_request_path(
            self.root, {"ref": "refs/heads/main", "inputs": {"request_path": self.req_path}},
            "workflow_dispatch", after), self.req_path)

    def test_batch_push_fails_closed(self):
        before = git(self.root, "rev-parse", "HEAD")
        (self.pending / "testb.json").write_text(json.dumps(self.req))
        after = self.commit_requests()
        event = {"ref": "refs/heads/main", "before": before, "after": after}
        with self.assertRaisesRegex(SaveConflict, "exactly one"):
            event_request_path(self.root, event, "push", after)

    def test_modified_request_fails_closed(self):
        self.commit_requests()
        before = git(self.root, "rev-parse", "HEAD")
        (self.root / self.req_path).write_text('{"status":"invalid"}')
        git(self.root, "add", self.req_path)
        git(self.root, "commit", "-qm", "modify immutable request")
        after = git(self.root, "rev-parse", "HEAD")
        with self.assertRaisesRegex(SaveConflict, "exactly one"):
            event_request_path(self.root, {"ref": "refs/heads/main",
                                           "before": before, "after": after}, "push", after)

    def test_dispatch_other_branch_fails_closed(self):
        with self.assertRaisesRegex(SaveConflict, "only permitted on main"):
            event_request_path(
                self.root,
                {"ref": "refs/heads/feature-unsafe",
                 "inputs": {"request_path": self.req_path}},
                "workflow_dispatch", "a" * 40)

    def test_remote_case_collision_after_checkout_is_rejected(self):
        sha = self.commit_requests()
        self.add_remote()
        other = self.root / "parallel-case-worktree"
        subprocess.run(["git", "clone", "-q", "--branch", "main",
                        str(self.root/"origin.git"), str(other)], check=True)
        (other / "requests/pending/TEST.json").write_text(json.dumps(self.req))
        git(other, "config", "user.name", "Test")
        git(other, "config", "user.email", "test@example.invalid")
        git(other, "add", "requests/pending/TEST.json")
        git(other, "commit", "-qm", "racing case-colliding request")
        git(other, "push", "-q", "origin", "HEAD:main")
        git(self.root, "fetch", "origin", "main")
        with self.assertRaisesRegex(SaveConflict, "Remote case collision"):
            check_remote_case_collisions(self.root, "origin/main", "test")
        with self.assertRaisesRegex(SaveConflict, "Remote case collision"):
            publish(self.root, self.req_path, sha)

    def test_dispatch_bad_path_fails_closed(self):
        with self.assertRaises(SaveConflict):
            event_request_path(self.root, {"inputs": {"request_path": "../bad"}},
                               "workflow_dispatch", "a" * 40)

    def test_publish_and_remote_replay(self):
        sha = self.commit_requests()
        self.add_remote()
        out = publish(self.root, self.req_path, sha)
        self.assertEqual(out["status"], "saved")
        self.assertEqual(json.loads(git(self.root, "show",
                         "origin/main:requests/results/test.json"))["request_id"],
                         self.req["request_id"])
        self.assertIsNone(inspect_remote_for_unrelated(self.root))
        second = publish(self.root, self.req_path, git(self.root, "rev-parse", "HEAD"))
        self.assertEqual(second["status"], "already_saved")
        self.assertEqual(second["video_id"], "test")

    def test_approval_request_id_reused_for_other_video_rejected(self):
        sha = self.commit_requests()
        self.add_remote()
        another = self.root / "duplicate-approval-worktree"
        subprocess.run(["git", "clone", "-q", "--branch", "main",
                        str(self.root/"origin.git"), str(another)], check=True)
        # This request is invalid for its own video but only its reused
        # approval ID is relevant to the other independent request.
        (another / "requests/pending/testb.json").write_text(
            json.dumps(self.req), encoding="utf-8")
        git(another, "config", "user.name", "Test")
        git(another, "config", "user.email", "test@example.invalid")
        git(another, "add", "requests/pending/testb.json")
        git(another, "commit", "-qm", "reuse approval id")
        git(another, "push", "-q", "origin", "HEAD:main")
        with self.assertRaisesRegex(SaveConflict, "request_id reused"):
            publish(self.root, self.req_path, sha)

    def test_changed_remote_mp4_blob_is_rejected(self):
        sha = self.commit_requests()
        self.add_remote()
        other = self.root / "source-change-worktree"
        subprocess.run(["git", "clone", "-q", "--branch", "main",
                        str(self.root/"origin.git"), str(other)], check=True)
        # A valid but different MP4 should not replace the approved input.
        (other / "video/test.mp4").write_bytes(b"changed remote video bytes")
        git(other, "config", "user.name", "Test")
        git(other, "config", "user.email", "test@example.invalid")
        git(other, "add", "video/test.mp4")
        git(other, "commit", "-qm", "change video after review")
        git(other, "push", "-q", "origin", "HEAD:main")
        with self.assertRaisesRegex(SaveConflict, "Video source Git blob SHA changed"):
            publish(self.root, self.req_path, sha)

    def test_changed_remote_request_blob_is_rejected(self):
        sha = self.commit_requests()
        self.add_remote()
        # Change published request, but keep original checkout pinned to sha.
        other = self.root / "other-worktree"
        subprocess.run(["git", "clone", "-q", "--branch", "main",
                        str(self.root/"origin.git"), str(other)], check=True)
        (other / self.req_path).write_text('{"status":"other"}', encoding="utf-8")
        git(other, "config", "user.name", "Test")
        git(other, "config", "user.email", "test@example.invalid")
        git(other, "add", self.req_path)
        git(other, "commit", "-qm", "tamper request")
        git(other, "push", "-q", "origin", "HEAD:main")
        with self.assertRaisesRegex(SaveConflict, "changed since trigger"):
            publish(self.root, self.req_path, sha)

    def test_five_distinct_workers_publish_concurrently_without_loss(self):
        # Five local Git/FFmpeg workers share one bare origin to exercise genuine
        # concurrent process/commit races, not just a sequential rebase.
        videos = ["test", "testb", "testc", "testd", "teste"]
        for stem in videos[1:]:
            shutil.copy2(self.root / "video/test.mp4",
                         self.root / f"video/{stem}.mp4")
        git(self.root, "add", "video")
        git(self.root, "commit", "-qm", "add concurrent synthetic source videos")
        for stem in videos[1:]:
            req = copy.deepcopy(self.req)
            req["request_id"] = f"{stem}-review-0001"
            req["video"]["path"] = f"video/{stem}.mp4"
            req["video"]["blob_sha"] = git(self.root, "rev-parse",
                                            f"HEAD:video/{stem}.mp4")
            yml = yaml.safe_load(req["analysis_yaml"])
            yml["video"]["filename"] = f"{stem}.mp4"
            req["analysis_yaml"] = yaml.safe_dump(yml, allow_unicode=True)
            (self.pending / f"{stem}.json").write_text(
                json.dumps(req, ensure_ascii=False), encoding="utf-8")
        trigger = self.commit_requests()
        remote = self.add_remote()
        work = []
        for index, stem in enumerate(videos, 1):
            folder = self.root / f"concurrent-worker-{index}"
            subprocess.run(["git", "clone", "-q", "--branch", "main",
                            str(remote), str(folder)], check=True)
            git(folder, "checkout", "-q", "--detach", trigger)
            work.append((folder, stem))
        starts = {}
        finishes = {}
        def save_one(item):
            folder, stem = item
            starts[stem] = time.monotonic()
            out = publish(folder, f"requests/pending/{stem}.json", trigger)
            finishes[stem] = time.monotonic()
            return out
        with ThreadPoolExecutor(max_workers=5) as pool:
            outputs = list(pool.map(save_one, work))
        self.assertEqual([out["status"] for out in outputs], ["saved"] * 5)
        # At least two saves overlapped while FFmpeg and Git were running.
        self.assertLess(max(starts.values()), min(finishes.values()))
        git(self.root, "fetch", "origin", "main")
        for stem in videos:
            remote_result = json.loads(git(
                self.root, "show", f"origin/main:requests/results/{stem}.json"))
            self.assertEqual(remote_result["video_id"], stem)
            self.assertEqual(remote_result["status"], "saved")
            self.assertEqual(len(git(
                self.root, "ls-tree", "-r", "--name-only", "origin/main",
                "--", f"references/{stem}").splitlines()), 5)

    def test_parallel_two_video_commits_rebase_without_loss(self):
        # Simulates two independent runners checking out the SAME commit.
        # Each one publishes only its own package and result.
        src2 = self.root / "video/testb.mp4"
        shutil.copy2(self.root / "video/test.mp4", src2)
        git(self.root, "add", "video/testb.mp4")
        git(self.root, "commit", "-qm", "add second source")
        sha2 = git(self.root, "rev-parse", "HEAD:video/testb.mp4")
        req2 = copy.deepcopy(self.req)
        req2["request_id"] = "test-video-00002"
        req2["video"]["path"] = "video/testb.mp4"
        req2["video"]["blob_sha"] = sha2
        data2 = yaml.safe_load(req2["analysis_yaml"])
        data2["video"]["filename"] = "testb.mp4"
        req2["analysis_yaml"] = yaml.safe_dump(data2, allow_unicode=True)
        (self.pending / "testb.json").write_text(json.dumps(req2), encoding="utf-8")
        trigger = self.commit_requests()
        remote = self.add_remote()
        a = self.root / "worker-a"
        b = self.root / "worker-b"
        for dest in (a, b):
            subprocess.run(["git", "clone", "-q", "--branch", "main",
                            str(remote), str(dest)], check=True)
            git(dest, "checkout", "-q", "--detach", trigger)
        first = publish(a, self.req_path, trigger)
        second = publish(b, "requests/pending/testb.json", trigger)
        self.assertEqual(first["status"], "saved")
        self.assertEqual(second["status"], "saved")
        git(self.root, "fetch", "origin", "main")
        self.assertIsNotNone(inspect_remote(
            self.root, "origin/main", "test", self.req))
        self.assertIsNotNone(inspect_remote(
            self.root, "origin/main", "testb", req2))
        self.assertTrue(git(self.root, "ls-tree", "-r", "--name-only",
                            "origin/main", "--", "references/testb"))


def inspect_remote_for_unrelated(root):
    """Helper exercises the untouched unrelated path branch."""
    return inspect_remote(
        root, "origin/main", "nonexistent",
        {"request_id": "nonexistent-1",
         "video": {"path": "video/nonexistent.mp4", "blob_sha": "0" * 40}},
    )


if __name__ == "__main__":
    unittest.main()
