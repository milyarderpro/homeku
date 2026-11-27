"""Prepare a Drive delivery from one exported audit snapshot."""
from __future__ import annotations

import os
import tempfile
from pathlib import Path

from .audit_session import read_session_metadata, workspace
from .common import atomic_text, dumps, require, safe_relative, sha256, snapshot_hash
from .storage import locked
from .validation import extract_package, validate_folder


def _unpack(package, directory):
    folder = extract_package(package, directory)
    manifest, model, _ = validate_folder(folder, directory, package.name, require_source=False)
    return folder, manifest, model["content_sha256"]


def _delivery_hashes(folder, manifest, name, digest):
    return {
        "analysis.md": sha256(folder / "analysis.md"),
        **{media["path"]: media["sha256"] for media in manifest["media"]},
        name: digest,
    }


def delivery_plan(package, expected_digest, work, video_name, *, previous=None):
    """List exact upload bytes in order and compare them with a prior Drive ZIP."""
    safe_relative(video_name)
    video = Path(video_name)
    require(video.name == video_name and video.suffix.lower() == ".mp4",
            "Use the exact original Drive MP4 filename")
    _, session = read_session_metadata(work / "session.json")
    package = workspace(package)
    require(package.is_file() and sha256(package) == expected_digest, "Exported ZIP SHA-256 mismatch")
    plan_path = workspace(work / "delivery" / expected_digest / "plan.json")
    output = plan_path.parent
    with locked(output, recovery=False), tempfile.TemporaryDirectory(prefix=".extract-", dir=output) as tmp:
        scratch = Path(tmp)
        folder, manifest, content_digest = _unpack(package, scratch / "current")
        require(sha256(package) == expected_digest, "Exported ZIP changed while preparing delivery")
        source_digest = manifest["source"]["sha256"]
        require(source_digest == session["source"]["sha256"], "Exported ZIP belongs to a different session source")
        hashes = _delivery_hashes(folder, manifest, package.name, expected_digest)
        prior_hashes = {}
        prior_digest = None
        if previous is not None:
            previous = workspace(previous)
            prior_digest = sha256(previous)
            prior_folder, prior_manifest, _ = _unpack(previous, scratch / "previous")
            require(sha256(previous) == prior_digest, "Previous Drive ZIP changed while preparing delivery")
            require(prior_manifest["source"]["sha256"] == source_digest,
                    "Drive folder conflicts with a different video source")
            require(prior_manifest["id"] == manifest["id"], "Drive folder conflicts with a different audit ID")
            require(prior_manifest["revision"] <= manifest["revision"], "Drive folder contains a newer revision")
            prior_hashes = _delivery_hashes(prior_folder, prior_manifest, previous.name, prior_digest)

        retained = workspace(output / "payload") / folder.name
        if retained.parent.exists():
            require(snapshot_hash(retained) == content_digest, "Retained delivery payload differs from exported ZIP")
        else:
            os.replace(folder.parent, retained.parent)
        files = [
            {
                "relative_path": name,
                "path": str(package if name == package.name else retained / name),
                "sha256": digest,
                "comparison": ("new" if name not in prior_hashes
                               else "identical" if prior_hashes[name] == digest else "changed"),
            }
            for name, digest in hashes.items()
        ]
        plan = {
            "drive_path": ["Audit", video.stem],
            "video_name": video_name,
            "source_sha256": source_digest,
            "package_sha256": expected_digest,
            "previous_package_sha256": prior_digest,
            "files": files,
            "obsolete_media": sorted(name for name in prior_hashes.keys() - hashes.keys() if name.startswith("media/")),
            "plan": str(plan_path),
        }
        # Validate the temporary name used by atomic_text as well as its destination.
        workspace(plan_path.with_suffix(".json.tmp"))
        atomic_text(plan_path, dumps(plan))
    return plan
