"""Verify downloaded GitHub files against the locally prepared payload."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
from pathlib import Path


def verify(payload: dict, downloaded: Path) -> dict:
    downloaded = downloaded.resolve(strict=True)
    for entry in payload["entries"]:
        file = downloaded / entry["path"]
        if not file.is_file():
            raise ValueError(f"Missing GitHub file: {entry['path']}")
        raw = file.read_bytes()
        actual = hashlib.sha256(raw).hexdigest()
        if actual != entry["sha256"]:
            raise ValueError(f"Different file bytes: {entry['path']}")
        if entry["encoding"] == "base64" and base64.b64decode(entry["content"], validate=True) != raw:
            raise ValueError(f"Different decoded bytes: {entry['path']}")
    return {"video_id": payload["video_id"], "verified_files": len(payload["entries"])}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("manifest", type=Path)
    p.add_argument("downloaded_repo_root", type=Path)
    args = p.parse_args()
    print(json.dumps(verify(json.loads(args.manifest.read_text(encoding="utf-8")), args.downloaded_repo_root)))


if __name__ == "__main__":
    main()
