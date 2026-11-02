"""Prepare deterministic Git blob payloads; produce a LOCAL JSON manifest, never upload."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
import tempfile
from pathlib import Path
from typing import Any

import yaml

from validate_analysis import validate, InvalidPackage

VIDEO_RE = re.compile(r"VID-\d{3,}\Z")


def choose_next_id(paths: list[str]) -> str:
    """Lowest available VID ID; caller MUST read paths from a single HEAD snapshot."""
    existing = {int(match.group(1)) for path in paths if (match := re.match(r"references/VID-(\d{3,})(?:/|$)", path))}
    number = 1
    while number in existing:
        number += 1
    return f"VID-{number:03d}"


def git_blob_sha(content: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest()


def build_payload(source: Path, target_id: str) -> dict[str, Any]:
    """Build a payload for ONE candidate ID. Rebuild after each conflicting HEAD."""
    if not VIDEO_RE.fullmatch(target_id):
        raise InvalidPackage("Target ID must be VID-XXX")
    source = source.resolve(strict=True)
    validate(source)
    old_id = source.name
    # Build into an ephemeral directory so local source files are never edited.
    with tempfile.TemporaryDirectory() as scratch:
        work = Path(scratch) / target_id
        work.mkdir()
        y = yaml.safe_load((source / "analysis.yaml").read_text(encoding="utf-8"))
        y["video"]["id"] = target_id
        for s in y["shots"]:
            s["keyframe"] = f"references/{target_id}/{s['id']}.jpg"
        (work / "analysis.yaml").write_text(yaml.safe_dump(y, allow_unicode=True, sort_keys=False), encoding="utf-8")
        md = (source / "analysis.md").read_text(encoding="utf-8")
        # Only replace ID tokens, not other facts.
        md = re.sub(rf"(?<![\w-]){re.escape(old_id)}(?![\w-])", target_id, md)
        (work / "analysis.md").write_text(md, encoding="utf-8")
        for source_file in source.glob("*.jpg"):
            (work / source_file.name).write_bytes(source_file.read_bytes())
        summary = validate(work, target_id)
        entries = []
        for name in summary["files"]:
            raw = (work / name).read_bytes()
            entries.append({
                "path": f"references/{target_id}/{name}", "mode": "100644", "type": "blob",
                "encoding": "base64" if name.endswith(".jpg") else "utf-8",
                "content": base64.b64encode(raw).decode("ascii") if name.endswith(".jpg") else raw.decode("utf-8"),
                "sha1_git_blob": git_blob_sha(raw), "sha256": hashlib.sha256(raw).hexdigest(), "size": len(raw),
            })
        return {"video_id": target_id, "shot_count": summary["shot_count"], "entries": entries}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("package", type=Path)
    p.add_argument("--id", required=True, help="Candidate ID from latest GitHub HEAD")
    p.add_argument("--output", type=Path, required=True, help="Private local file; includes Base64 JPEG bytes")
    args = p.parse_args()
    manifest = build_payload(args.package, args.id)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"video_id": manifest["video_id"], "files": len(manifest["entries"]), "manifest": str(args.output)}))


if __name__ == "__main__":
    main()
