"""Safe Parallel Save transaction engine (adapter-injected; no GitHub credentials stored).

This module does NOT run ChatGPT connector tools by itself. A host bridge must
implement Connector protocol and provide binary-safe content transport.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Protocol

from prepare_git_payload import build_payload, choose_next_id
from validate_analysis import validate


class SaveConflict(RuntimeError):
    """Expected GitHub branch SHA changed. Retry against a fresh snapshot."""


class SaveFailure(RuntimeError):
    pass


class Connector(Protocol):
    def snapshot(self) -> tuple[str, str, list[str]]:
        """Return (HEAD commit SHA, HEAD base tree SHA, all HEAD tree paths)."""

    def blob(self, content: str, encoding: str) -> str:
        """Create a Git blob and return its SHA."""

    def tree(self, base_tree_sha: str, elements: list[dict]) -> str: ...
    def commit(self, parent_sha: str, tree_sha: str, message: str) -> str: ...
    def update_ref(self, new_sha: str, expected_sha: str, force: bool = False) -> bool: ...
    def verify(self, commit_sha: str, entries: list[dict]) -> bool:
        """Check commit reachable from main and all file bytes match SHA-256."""


def safe_save(package: Path, connector: Connector, max_attempts: int = 3) -> dict:
    """Save a reviewed draft only AFTER external exact 'save now' authorization.

    `package` is local, NOT streamed through tool text. The connector bridge
    must transport each blob content losslessly. Any unavailable transport must
    fail closed before doing repository writes.
    """
    if not 1 <= max_attempts <= 3:
        raise ValueError("max_attempts must be within 1..3")
    validate(package)
    for attempt in range(1, max_attempts + 1):
        head, base_tree, paths = connector.snapshot()
        video_id = choose_next_id(paths)
        if any(p == f"references/{video_id}" or p.startswith(f"references/{video_id}/") for p in paths):
            raise SaveFailure("Target video ID already exists")
        payload = build_payload(package, video_id)
        elements = []
        for entry in payload["entries"]:
            sha = connector.blob(entry["content"], entry["encoding"])
            if sha != entry["sha1_git_blob"]:
                raise SaveFailure(f"Blob SHA mismatch for {entry['path']}")
            elements.append({"path": entry["path"], "mode": "100644", "type": "blob", "sha": sha})
        tree_sha = connector.tree(base_tree, elements)
        commit_sha = connector.commit(head, tree_sha, f"Add {video_id} video analysis")
        try:
            updated = connector.update_ref(commit_sha, expected_sha=head, force=False)
            if not updated:
                raise SaveConflict("HEAD changed")
        except SaveConflict:
            if attempt == max_attempts:
                raise SaveFailure("HEAD conflict after 3 attempts")
            continue
        # NEVER retry as a new video ID if ref update might have succeeded.
        # Read GitHub state and resolve any ambiguous network error first.
        if not connector.verify(commit_sha, payload["entries"]):
            raise SaveFailure("Commit update returned success but post-save verification failed")
        return {"status": "saved", "video_id": video_id, "sha": commit_sha, "shot_count": payload["shot_count"], "files": len(elements), "attempts": attempt}
    raise SaveFailure("Save did not complete")
