"""Small shared primitives; never discover sources by walking the archive."""

from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path, PurePosixPath


class LibraryError(ValueError):
    """A user-actionable package or library error."""


def require(condition, message):
    if not condition:
        raise LibraryError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def dumps(value) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n"


def read_json(path: Path):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, f"{path.name}: duplicate JSON key {key}")
            result[key] = value
        return result

    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=pairs,
                          parse_constant=lambda value: (_ for _ in ()).throw(LibraryError(f"Invalid number: {value}")))
    except (UnicodeError, json.JSONDecodeError, RecursionError) as error:
        raise LibraryError(f"{path}: invalid UTF-8/JSON: {error}") from error


def safe_relative(value: str) -> str:
    require(isinstance(value, str) and value, "Empty path")
    require("\\" not in value and not any(ord(c) < 32 for c in value), f"Unsafe path: {value!r}")
    path = PurePosixPath(value)
    require(not path.is_absolute() and all(p not in ("", ".", "..") for p in value.split("/")),
            f"Unsafe path: {value}")
    require(not re.match(r"^[A-Za-z]:", value), f"Unsafe drive path: {value}")
    return value


def atomic_text(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(content)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def content_hash(folder: Path) -> str:
    """Canonical revision identity ignores ZIP compression and optional source copy."""
    rows = []
    for path in sorted(folder.rglob("*")):
        require(not path.is_symlink(), f"Symlink not allowed: {path}")
        if path.is_file() and path.name != "source.mp4":
            rows.append([path.relative_to(folder).as_posix(), sha256(path)])
    return hashlib.sha256(dumps(rows).encode()).hexdigest()


def cell(value) -> str:
    """Escape generated table cells without dropping qualifiers or uncertainty."""
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")


def slug(value: str) -> str:
    # Hash suffix prevents categories such as 'A B' and 'A-B' from colliding.
    base = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")[:60] or "label"
    return base + "-" + hashlib.sha256(value.encode()).hexdigest()[:8]


def snapshot_hash(folder):
    """Bind every candidate payload byte, including an optional source copy."""
    require(folder.is_dir() and not folder.is_symlink(), "Invalid candidate folder")
    rows=[]
    for p in sorted(folder.rglob("*")):
        require(not p.is_symlink(), "Symlink in candidate")
        if p.is_file(): rows.append([p.relative_to(folder).as_posix(),sha256(p)])
    require(rows, "Empty candidate")
    return hashlib.sha256(dumps(rows).encode()).hexdigest()
