import base64
import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from prepare_git_payload import build_payload, choose_next_id, git_blob_sha
from test_validation import make_package


class PayloadTests(unittest.TestCase):
    def test_candidate_id_and_image_byte_fidelity(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = make_package(Path(tmp))
            payload = build_payload(source, "VID-008")
            self.assertEqual(len(payload["entries"]), 5)
            for e in payload["entries"]:
                raw = (source / Path(e["path"]).name).read_bytes() if e["path"].endswith(".jpg") else None
                if raw is not None:
                    self.assertEqual(base64.b64decode(e["content"], validate=True), raw)
                    self.assertEqual(e["sha256"], hashlib.sha256(raw).hexdigest())
                    self.assertEqual(e["sha1_git_blob"], git_blob_sha(raw))
                else:
                    self.assertIn("VID-008", e["content"])
            self.assertEqual(choose_next_id(["references/VID-001/analysis.yaml", "references/VID-003/analysis.md"]), "VID-002")


if __name__ == "__main__":
    unittest.main()
