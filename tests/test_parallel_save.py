import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from save_analysis import SaveConflict, SaveFailure, safe_save
from test_validation import make_package


class FakeConnector:
    def __init__(self, conflict_once=False):
        self.head = "HEAD0"
        self.paths = ["references/VID-001/analysis.yaml"]
        self.objects = {}
        self.pending_tree = []
        self.conflict_once = conflict_once
        self.calls = []

    def snapshot(self):
        return self.head, "TREE0", self.paths.copy()

    def blob(self, content, encoding):
        import base64
        raw = base64.b64decode(content) if encoding == "base64" else content.encode()
        sha = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        self.objects[sha] = raw
        return sha

    def tree(self, base_tree_sha, elements):
        self.pending_tree = elements
        return "TREE-NEW"

    def commit(self, parent_sha, tree_sha, message):
        return "COMMIT-NEW"

    def update_ref(self, new_sha, expected_sha, force=False):
        self.calls.append((new_sha, expected_sha, force))
        assert force is False
        if self.conflict_once:
            self.conflict_once = False
            self.head = "HEAD-BY-OTHER"
            self.paths.append("references/VID-002/analysis.yaml")
            raise SaveConflict("external writer won")
        assert expected_sha == self.head
        self.head = new_sha
        self.paths.extend(x["path"] for x in self.pending_tree)
        return True

    def verify(self, commit_sha, entries):
        return self.head == commit_sha and all(self.objects[x["sha1_git_blob"]] for x in entries)


class ParallelTests(unittest.TestCase):
    def test_conflict_recalculates_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = safe_save(make_package(Path(tmp)), FakeConnector(conflict_once=True))
            self.assertEqual(result["video_id"], "VID-003")
            self.assertEqual(result["attempts"], 2)

    def test_normal_save(self):
        with tempfile.TemporaryDirectory() as tmp:
            connector = FakeConnector()
            result = safe_save(make_package(Path(tmp)), connector)
            self.assertEqual(result["video_id"], "VID-002")
            self.assertEqual(result["files"], 5)
            self.assertTrue(all(not c[2] for c in connector.calls))


if __name__ == "__main__":
    unittest.main()
