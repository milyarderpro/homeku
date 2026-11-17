"""Verify source bytes, reference bindings and retired IDs; read-only by default.

--write explicitly refreshes knowledge/source-manifest.json after source review.
This checks provenance/integrity, not the semantic accuracy of video annotations.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = Path("knowledge/source-manifest.json")
FILENAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]*\.mp4\Z")
IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]*\Z")


class SourceIntegrityError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise SourceIntegrityError(message)


def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_manifest(root):
    path = root / MANIFEST
    require(path.is_file(), f"Source manifest missing: {MANIFEST}")
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict) and value.get("schema_version") == "1.0",
            "Unsupported source manifest")
    require(isinstance(value.get("retired_references"), list),
            "Missing retired_references ledger")
    return value


def scan_sources(root, retired_references=()):
    """Hash every MP4; bind each archive to one existing, unique source."""
    root = Path(root).resolve()
    inventory = {}
    by_hash = {}
    by_case = {}
    for path in sorted((root / "video").iterdir()):
        if path.suffix.casefold() != ".mp4":
            continue
        require(FILENAME.fullmatch(path.name) is not None,
                f"Invalid source filename: {path.name}")
        require(path.is_file() and not path.is_symlink() and path.stat().st_size > 0,
                f"Invalid or empty source: {path.name}")
        folded = path.name.casefold()
        require(folded not in by_case, f"Source filename case collision: {path.name}")
        by_case[folded] = path.name
        digest = sha256_file(path)
        require(digest not in by_hash,
                f"Duplicate video content: {by_hash.get(digest)} and {path.name}")
        by_hash[digest] = path.name
        inventory[path.name] = {
            "source_path": f"video/{path.name}",
            "sha256": digest,
            "size_bytes": path.stat().st_size,
        }
    require(bool(inventory), "No source MP4 files")

    references = []
    used = {}
    ref_cases = set()
    shot_count = 0
    for folder in sorted((root / "references").iterdir()):
        if not folder.is_dir():
            continue
        ident = folder.name
        require(IDENTIFIER.fullmatch(ident) is not None and not folder.is_symlink(),
                f"Invalid reference directory: {ident}")
        require(ident.casefold() not in ref_cases, f"Reference case collision: {ident}")
        ref_cases.add(ident.casefold())
        analysis = folder / "analysis.yaml"
        require(analysis.is_file(), f"Missing analysis.yaml: {ident}")
        data = yaml.safe_load(analysis.read_text(encoding="utf-8"))
        require(isinstance(data, dict) and isinstance(data.get("video"), dict),
                f"Invalid video metadata: {ident}")
        video = data["video"]
        require(video.get("id") == ident, f"Reference identifier mismatch: {ident}")
        filename = video.get("filename")
        require(isinstance(filename, str) and FILENAME.fullmatch(filename) is not None,
                f"Unsafe or invalid video.filename: {ident}")
        require(filename in inventory, f"Missing source for {ident}: video/{filename}")
        require(filename not in used,
                f"Source shared by multiple references: {used.get(filename)} and {ident}")
        used[filename] = ident
        shots = data.get("shots")
        require(isinstance(shots, list) and len(shots) > 0
                and video.get("shot_count") == len(shots),
                f"Shot count mismatch: {ident}")
        shot_count += len(shots)
        references.append({"reference_id": ident, **inventory[filename]})
    require(bool(references), "No reference analyses")

    active = {item["reference_id"]: item for item in references}
    retired_ids = set()
    for record in retired_references:
        require(isinstance(record, dict), "Invalid retirement record")
        ident, canonical = record.get("reference_id"), record.get("canonical_reference_id")
        require(isinstance(ident, str) and IDENTIFIER.fullmatch(ident) is not None,
                "Invalid retired reference ID")
        require(ident.casefold() not in retired_ids, f"Duplicate retirement: {ident}")
        retired_ids.add(ident.casefold())
        require(ident.casefold() not in ref_cases, f"Retired reference restored: {ident}")
        require(canonical in active, f"Retirement canonical source missing: {canonical}")
        require(record.get("sha256") == active[canonical]["sha256"],
                f"Retirement canonical source changed: {canonical}")
        require(bool(record.get("reason")) and bool(record.get("retired_on")),
                f"Missing retirement provenance: {ident}")
        for relative in (f"video/{ident}.mp4", f"requests/pending/{ident}.json",
                         f"requests/results/{ident}.json"):
            parent = root / Path(relative).parent
            require(not parent.is_dir() or not any(
                item.name.casefold() == Path(relative).name.casefold()
                for item in parent.iterdir()
            ), f"Retired artifact restored: {relative}")

    return {
        "schema_version": "1.0",
        "hash_algorithm": "sha256",
        "reference_count": len(references),
        "shot_count": shot_count,
        "references": references,
        "unannotated_sources": [value for name, value in inventory.items() if name not in used],
        "retired_references": list(retired_references),
    }


def verify_sources(root=ROOT):
    root = Path(root)
    recorded = load_manifest(root)
    actual = scan_sources(root, recorded["retired_references"])
    require(actual == recorded,
            "Source manifest differs from current files/bindings; review changes, then "
            "run scripts/verify_source_integrity.py --write")
    return actual


def write_manifest(root=ROOT):
    root = Path(root)
    retired = load_manifest(root)["retired_references"] if (root / MANIFEST).exists() else []
    actual = scan_sources(root, retired)
    (root / MANIFEST).parent.mkdir(parents=True, exist_ok=True)
    (root / MANIFEST).write_text(
        json.dumps(actual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return actual


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = parser.parse_args()
    try:
        report = write_manifest(args.root) if args.write else verify_sources(args.root)
    except (SourceIntegrityError, OSError, ValueError, yaml.YAMLError) as exc:
        parser.exit(1, f"Source integrity failed: {exc}\n")
    print(f"Source integrity verified: {report['reference_count']} references / "
          f"{report['shot_count']} shots; all sources available; no duplicate MP4 bytes; "
          f"{len(report['unannotated_sources'])} unannotated sources")


if __name__ == "__main__":
    main()
