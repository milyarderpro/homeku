"""Batch ingest, revision checks, derived output publication, and consistency checks."""

from __future__ import annotations

import hashlib
import re
import shutil
import tempfile
from pathlib import Path

from .common import LibraryError, dumps, read_json, require, sha256
from .generation import load_models, render
from .storage import locked, publish
from .validation import CODE_ROOT, extract_package, validate_folder


def registry_at(root):
    path = root / "data/registry.json"
    registry = read_json(path) if path.exists() else {"version": 1, "references": {}}
    require(isinstance(registry, dict) and registry.get("version") == 1 and isinstance(registry.get("references"), dict), "Invalid registry version/shape")
    folded = set()
    for rid, entry in registry["references"].items():
        require(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}", rid), "Invalid registry ID")
        require(isinstance(entry, dict), f"Registry entry must be an object: {rid}")
        require(rid.casefold() not in folded, "Case collision in registry")
        folded.add(rid.casefold())
        require(isinstance(entry.get("revision"), int) and 1 <= entry["revision"] <= 9999, f"Invalid registry revision: {rid}")
        for key in ("content_sha256", "source_sha256", "package_sha256", "analysis_sha256", "manifest_sha256"):
            require(re.fullmatch(r"[a-f0-9]{64}", entry.get(key, "")), f"Invalid registry {key}: {rid}")
    return registry


def outputs_to_stage(stage, outputs):
    for name, text in outputs.items():
        path = stage / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")
    # Empty projections must also replace stale cache directories.
    (stage / "data/projections").mkdir(parents=True, exist_ok=True)
    return {name: stage / name for name in ("catalogs", "knowledge", "data/projections", "data/search-index.json", "data/dependencies.json", "data/build.json")}


def fixture_allowed(root, manifest):
    require(manifest["purpose"] == "reference" or
            (root.resolve() != CODE_ROOT.resolve() and (root / ".homeku-fixture-root").is_file()),
            "Synthetic fixture rejected: use an isolated root with .homeku-fixture-root for tests only")


def validate_package(root, package):
    with locked(root):
        with tempfile.TemporaryDirectory(prefix="validate-", dir=root / ".homeku") as work:
            folder = extract_package(package, Path(work) / "package")
            manifest, model, _ = validate_folder(folder, root, package.name)
            return {"id": manifest["id"], "revision": manifest["revision"], "content_sha256": model["content_sha256"]}


def ingest(root: Path, packages=None):
    with locked(root):
        packages = sorted(set(packages if packages is not None else (root / "incoming").glob("*.zip")), key=lambda p: p.name)
        registry = registry_at(root)
        ledger_path = root / "data/ingest.json"
        ledger = read_json(ledger_path) if ledger_path.exists() else {"version": 1, "packages": {}}
        require(isinstance(ledger, dict) and ledger.get("version") == 1 and isinstance(ledger.get("packages"), dict), "Invalid ingest ledger")
        models = load_models(root, registry)
        proposed, results, source_overrides = {}, [], {}
        with tempfile.TemporaryDirectory(prefix="batch-", dir=root / ".homeku") as work_name:
            work = Path(work_name)
            for index, package in enumerate(packages):
                package_hash = None
                try:
                    require(package.is_file() and not package.is_symlink(), f"Not a regular package: {package}")
                    package_hash = sha256(package)
                    record = ledger["packages"].get(package_hash)
                    if record and record.get("status") == "imported":
                        results.append({"package": package.name, "status": "unchanged", "id": record["id"], "revision": record["revision"]})
                        continue
                    folder = extract_package(package, work / f"package-{index}")
                    manifest, model, source = validate_folder(folder, root, package.name, source_overrides)
                    fixture_allowed(root, manifest)
                    rid, revision = manifest["id"], manifest["revision"]
                    existing = registry["references"].get(rid)
                    require(all(key.casefold() != rid.casefold() or key == rid for key in registry["references"]), f"Reference ID case collision: {rid}")
                    if existing and revision == existing["revision"]:
                        require(model["content_sha256"] == existing["content_sha256"], f"Conflicting content for {rid} revision {revision}")
                        results.append({"package": package.name, "status": "unchanged", "id": rid, "revision": revision})
                        continue
                    if existing:
                        require(revision == existing["revision"] + 1, f"{rid}: expected revision {existing['revision'] + 1}")
                        require(manifest["supersedes"] == {"revision": existing["revision"], "content_sha256": existing["content_sha256"]}, f"{rid}: supersedes does not match active revision")
                    else:
                        require(revision == 1 and manifest["supersedes"] is None, f"{rid}: first revision must be 1 with supersedes=null")
                        require(not (root / "references" / rid).exists(), f"Unregistered reference directory already exists: {rid}")
                    duplicate = next((key for key, entry in registry["references"].items() if key != rid and entry["source_sha256"] == manifest["source"]["sha256"]), None)
                    require(duplicate is None, f"Duplicate active source: {duplicate}")
                    destination = work / f"prepared-{index}/references" / rid
                    shutil.copytree(folder, destination, ignore=shutil.ignore_patterns("source.mp4"))
                    canonical = root / "video" / f"{rid}.mp4"
                    if canonical.is_file() and sha256(canonical) == manifest["source"]["sha256"]:
                        source_destination = canonical
                    else:
                        source_destination = work / f"prepared-{index}/video" / f"{rid}.mp4"
                        source_destination.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copyfile(source, source_destination)
                    entry = {"revision": revision, "content_sha256": model["content_sha256"],
                        "source_sha256": manifest["source"]["sha256"], "package_sha256": package_hash,
                        "analysis_sha256": sha256(folder / "analysis.md"), "manifest_sha256": sha256(folder / "manifest.json")}
                    result = {"package": package.name, "status": "imported", "id": rid, "revision": revision}
                    # Mutate state only after every copy and fingerprint succeeds.
                    proposed[f"references/{rid}"] = destination
                    proposed[f"video/{rid}.mp4"] = source_destination
                    source_overrides[rid] = source_destination
                    registry["references"][rid] = entry
                    models[rid] = model
                    ledger["packages"][package_hash] = result
                    results.append(result)
                except (LibraryError, OSError) as error:
                    result = {"package": package.name, "status": "failed", "error": str(error)}
                    results.append(result)
                    if package_hash:
                        ledger["packages"][package_hash] = result
            generated = render(root, models)
            proposed.update(outputs_to_stage(work / "generated", generated))
            for name, value in (("registry", registry), ("ingest", ledger)):
                path = work / f"{name}.json"
                path.write_text(dumps(value), encoding="utf-8")
                proposed[f"data/{name}.json"] = path
            changed = publish(root, proposed)
        return {"results": results, "changed": changed}


def build(root, full=False):
    with locked(root):
        registry = registry_at(root)
        models = load_models(root, registry, full=full)
        generated = render(root, models)
        with tempfile.TemporaryDirectory(prefix="build-", dir=root / ".homeku") as work:
            changed = publish(root, outputs_to_stage(Path(work), generated))
        return {"references": len(models), "shots": sum(len(m["shots"]) for m in models.values()), "changed": changed}


def check(root):
    with locked(root, recovery=False):
        registry = registry_at(root)
        models = load_models(root, registry, full=True)
        expected = render(root, models)
        actual = set()
        for name in ("catalogs", "knowledge", "data/projections"):
            folder = root / name
            if folder.exists():
                actual.update(p.relative_to(root).as_posix() for p in folder.rglob("*") if p.is_file())
        actual.update(name for name in ("data/search-index.json", "data/dependencies.json", "data/build.json") if (root / name).exists())
        require(actual == set(expected), f"Generated file inventory differs; run build. Missing/stale: {sorted(actual ^ set(expected))[:10]}")
        for name, text in expected.items():
            require((root / name).read_text(encoding="utf-8") == text, f"Generated output differs: {name}; run build")
        reference_dir = root / "references"
        if reference_dir.exists():
            found = {p.name for p in reference_dir.iterdir() if p.is_dir()}
            require(found == set(models), f"Unregistered reference folders: {sorted(found ^ set(models))}")
        return {"references": len(models), "shots": sum(len(m["shots"]) for m in models.values()), "status": "ok"}
