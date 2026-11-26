"""Serialized local publication with a rollback journal and crash recovery."""

from __future__ import annotations

import fcntl
import os
import shutil
import tempfile
from contextlib import contextmanager
from pathlib import Path

from .common import atomic_text, dumps, read_json, require, safe_relative, sha256


def remove(path):
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    elif path.exists() or path.is_symlink():
        path.unlink()


def same(left, right):
    if not left.exists() or left.is_symlink() or right.is_symlink():
        return False
    if left.is_file() and right.is_file():
        return sha256(left) == sha256(right)
    if left.is_dir() and right.is_dir():
        def inventory(folder):
            return {p.relative_to(folder).as_posix(): sha256(p) for p in folder.rglob("*") if p.is_file()}
        return inventory(left) == inventory(right)
    return False


def copy(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    if source.is_dir():
        shutil.copytree(source, target)
    else:
        shutil.copyfile(source, target)


def publication_path(name):
    relative = safe_relative(name)
    require(relative == "incoming" or relative.split("/")[0] in
            {"references", "video", "catalogs", "knowledge", "data"}, "Invalid publication destination")
    return relative


def recover(root):
    journal_path = root / ".homeku/transaction.json"
    if not journal_path.exists():
        return False
    journal = read_json(journal_path)
    txn_name = safe_relative(journal["transaction"])
    require("/" not in txn_name and txn_name.startswith("publish-"), "Invalid recovery transaction")
    transaction = root / ".homeku" / txn_name
    if not journal["committed"]:
        for op in reversed(journal["operations"]):
            relative = publication_path(op["path"])
            target, backup = root / relative, transaction / "old" / relative
            if backup.exists():
                remove(target)
                target.parent.mkdir(parents=True, exist_ok=True)
                os.replace(backup, target)
            elif not op["existed"]:
                remove(target)
    journal_path.unlink()
    remove(transaction)
    return True


@contextmanager
def locked(root, *, recovery=True):
    state = root / ".homeku"
    state.mkdir(parents=True, exist_ok=True)
    with (state / "lock").open("a") as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        if recovery:
            recover(root)
        else:
            require(not (state / "transaction.json").exists(), "Pending transaction: run recover before checking")
        try:
            yield
        finally:
            fcntl.flock(stream, fcntl.LOCK_UN)


def publish(root: Path, proposed, after_install=None):
    """Caller holds lock; stage first, then install, with registry installed last.

    A git commit publishes one snapshot externally. Local lock-aware readers see a
    consistent state; a process interruption is rolled back on next write.
    """
    changes = {name: path for name, path in proposed.items() if not same(root / name, path)}
    if not changes:
        return []
    transaction = Path(tempfile.mkdtemp(prefix="publish-", dir=root / ".homeku"))
    operations = []
    for relative, source in sorted(changes.items(), key=lambda r: (r[0] == "data/registry.json", r[0])):
        publication_path(relative)
        require(not any((root / relative).parents[i].is_symlink() for i in range(len((root / relative).parents))), "Symlinked destination parent")
        require(not (root / relative).is_symlink(), f"Symlinked destination: {relative}")
        copy(source, transaction / "new" / relative)
        operations.append({"path": relative, "existed": (root / relative).exists()})
    journal = {"transaction": transaction.name, "committed": False, "operations": operations}
    journal_path = root / ".homeku/transaction.json"
    atomic_text(journal_path, dumps(journal))
    try:
        for index, op in enumerate(operations):
            relative = op["path"]
            target, backup = root / relative, transaction / "old" / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            if op["existed"]:
                backup.parent.mkdir(parents=True, exist_ok=True)
                os.replace(target, backup)
            os.replace(transaction / "new" / relative, target)
            if after_install:
                after_install(index, relative)
        journal["committed"] = True
        atomic_text(journal_path, dumps(journal))
    except Exception:
        recover(root)
        raise
    recover(root)  # A committed journal is cleaned up, never rolled back.
    return sorted(changes)
