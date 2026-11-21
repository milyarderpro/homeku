"""Save a validated checkpoint without overwriting an earlier file.

Call save_project(project, project_path, source_root=..., fallback_root=...) from
the live project dict. A failure returns saved=False; keep discussing from the
dict and do not claim a download. CLI accepts '-' as JSON input from stdin.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from shutil import copyfile, rmtree
from tempfile import NamedTemporaryFile, gettempdir, mkdtemp

from validate_project import _asset_path, validate_project


def _read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _publish(project, path, root):
    """Publish a verified temporary file atomically, exclusively; never replace."""
    temporary = None
    published = False
    try:
        with NamedTemporaryFile(mode="w", encoding="utf-8", prefix=".checkpoint-", suffix=".tmp",
                                dir=root, delete=False) as handle:
            temporary = Path(handle.name)
            json.dump(project, handle, ensure_ascii=False, indent=2, allow_nan=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        restored = _read_json(temporary)
        result = validate_project(restored, root)
        if restored != project or not result["valid"]:
            raise ValueError("Checkpoint sementara gagal baca balik/validasi: " + "; ".join(result["errors"]))
        # Atomic creation with no overwrite, including if another process creates path.
        os.link(temporary, path)
        published = True
        restored = _read_json(path)
        result = validate_project(restored, root)
        if restored != project or not result["valid"]:
            raise ValueError("Checkpoint terbit gagal baca balik/validasi: " + "; ".join(result["errors"]))
    except Exception:
        # Only this helper's newly created link, never an earlier checkpoint.
        if published and temporary is not None and path.exists() and path.samefile(temporary):
            path.unlink()
        raise
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def _candidate_paths(preferred, revision):
    yield preferred
    for sequence in range(1, 4):
        yield preferred.with_name(preferred.stem + f"-r{revision}-{sequence}" + preferred.suffix)


def _attempt(project, preferred):
    errors = []
    for candidate in _candidate_paths(preferred, project["revision"]):
        try:
            if candidate.exists() or candidate.is_symlink():
                continue
            _publish(project, candidate, preferred.parent)
            return candidate, errors
        except (OSError, ValueError) as error:
            errors.append(str(candidate) + ": " + str(error))
    return None, errors


def save_project(project, project_path, *, source_root=None, fallback_root=None):
    """Return the actual active path only after validated read-back.

    Old files and the caller's dict are never modified. A moved checkpoint
    carries only its registered readable assets with unchanged relative paths.
    """
    preferred = Path(project_path).absolute()
    origin = Path(source_root).absolute() if source_root is not None else preferred.parent
    errors = []
    validation = validate_project(project, origin)
    if not validation["valid"]:
        return {"saved": False, "path": None, "relocated": False, "errors": validation["errors"],
                "note": "Data sesi tetap tersedia; lengkapi data/aset sebelum mengklaim checkpoint/paket."}
    try:
        preferred.parent.mkdir(parents=True, exist_ok=True)
        if preferred.parent.resolve() == origin.resolve() or not project["assets"]:
            path, failures = _attempt(project, preferred)
            errors.extend(failures)
            if path is not None:
                return {"saved": True, "path": str(path), "relocated": preferred.parent.resolve() != origin.resolve(), "errors": errors}
    except OSError as error:
        errors.append(str(preferred.parent) + ": " + str(error))

    roots = ([Path(fallback_root)] if fallback_root is not None else
             [preferred.parent.parent, Path(gettempdir())])
    seen = set()
    for root in roots:
        owned = None
        try:
            root = root.resolve()
            if root in seen:
                continue
            seen.add(root)
            root.mkdir(parents=True, exist_ok=True)
            # Actual create/write/read-back below, never os.access as proof.
            owned = Path(mkdtemp(prefix=project["project_id"] + "-recovery-", dir=root))
            for asset in project["assets"]:
                source = _asset_path(asset["path"], origin)
                target = _asset_path(asset["path"], owned)
                target.parent.mkdir(parents=True, exist_ok=True)
                copyfile(source, target)
            target = owned / preferred.name
            path, failures = _attempt(project, target)
            errors.extend(failures)
            if path is not None:
                return {"saved": True, "path": str(path), "relocated": True, "errors": errors}
        except (OSError, ValueError) as error:
            errors.append(str(root) + ": " + str(error))
        if owned is not None:
            rmtree(owned, ignore_errors=True)  # only the newly created recovery folder
    return {"saved": False, "path": None, "relocated": False, "errors": errors,
            "note": "Belum tersimpan. Lanjutkan konsep dari data sesi; sediakan catatan teks, bukan tautan palsu."}


def main():
    import sys
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="Project JSON file, or '-' for the current dict via stdin")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--source-root", type=Path)
    parser.add_argument("--fallback-root", type=Path)
    args = parser.parse_args()
    try:
        project = json.load(sys.stdin) if args.input == "-" else _read_json(args.input)
        origin = args.source_root or (Path(args.input).resolve().parent if args.input != "-" else args.output.parent)
        result = save_project(project, args.output, source_root=origin, fallback_root=args.fallback_root)
    except (OSError, ValueError) as error:
        result = {"saved": False, "path": None, "errors": [str(error)]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["saved"] else 1)


if __name__ == "__main__":
    main()
