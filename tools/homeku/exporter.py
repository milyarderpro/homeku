"""Render, review and package an audit snapshot."""
from __future__ import annotations
import os
import re
import shutil
import tempfile
import zipfile
from contextlib import nullcontext
from pathlib import Path
from . import FORMAT_VERSION
from .audit_performance import safe_path, timed
from .audit_quality import fact_inventory
from .audit_session import workspace
from .common import dumps, read_json, require, sha256, snapshot_hash
from .media import expected_media
from .package_manifest import build_manifest
from .preflight import require_inputs
from .render_assets import DEFAULT_COLUMNS, render_config
from .reporting import render_report
from .storage import locked
from .validation import extract_package, package_files, validate_folder
from .video_cache import atomic, cached_media


def _managed_candidate(candidate):
    for name in ("manifest.json", "audit.json"):
        require((candidate / name).is_file() and not (candidate / name).is_symlink(),
                "Refusing to replace unmanaged candidate")
    manifest = read_json(candidate / "manifest.json")
    require(isinstance(manifest, dict) and manifest.get("contract_version") == FORMAT_VERSION
            and manifest.get("id") == candidate.name, "Refusing to replace unmanaged candidate")
    audit = read_json(candidate / "audit.json")
    from .models import schema_check
    schema_check(audit, "audit.schema.json")
    require(audit["id"] == candidate.name, "Existing candidate has a different audit ID")
    package_files(candidate, audit)


def draft(source, audit_path, audit_info, output_root, *, session_path, supersedes=None, purpose="reference",
          quality=91, scale=1.0, columns=DEFAULT_COLUMNS, overview_scale=1.0, storyboard_scale=1.0,
          cache_dir=None):
    source, audit_path = Path(source).absolute(), workspace(audit_path)
    require(not any(p.is_symlink() for p in (source, *source.parents)), "Use the original source path")
    output_root = workspace(output_root)
    content = audit_path.read_bytes()
    audit = read_json(audit_path)
    cache_root = workspace(cache_dir or (audit_path.parent / ".cache" / "frames"))
    log = audit_path.parent / "performance.jsonl"
    with timed(log, "draft"), locked(output_root, recovery=False):
        context = require_inputs(source, audit, audit_info, session_path=session_path, supersedes=supersedes,
                                 purpose=purpose, cache_dir=cache_root, log=log)
        cache = context["cache"]
        info = {**context["info"], "path": f"video/{audit['id']}.mp4", "sha256": context["sha256"]}
        times = context["times"]
        config = render_config(quality=quality, scale=scale, columns=columns,
                               overview_scale=overview_scale, storyboard_scale=storyboard_scale)
        candidate = safe_path(output_root / audit["id"])
        require(all(not path.resolve().is_relative_to(candidate.resolve())
                    for path in (source, audit_path, Path(session_path).absolute(), cache_root)),
                "Source, working files and cache must stay outside candidate")
        if candidate.exists():
            _managed_candidate(candidate)
        report = render_report(audit, times)
        plan = list(expected_media(audit, info, config, times))
        with tempfile.TemporaryDirectory(prefix=".draft-", dir=output_root) as scratch:
            folder = Path(scratch) / audit["id"]
            folder.mkdir()
            (folder / "audit.json").write_bytes(content)
            (folder / "analysis.md").write_bytes(report.encode())
            with cache.activate() if cache else nullcontext():
                media = cached_media(folder, audit, source, info, config, times, plan=plan)
            manifest = build_manifest(audit, info, context["logs"], sha256(folder / "audit.json"),
                                      config, times, media, supersedes=supersedes, purpose=purpose)
            (folder / "manifest.json").write_text(dumps(manifest), encoding="utf-8")
            _, model, _ = validate_folder(folder, output_root, source_overrides={audit["id"]: source},
                                          context=context, plan=plan, report=report)
            cache.ensure_source()
            require(audit_path.read_bytes() == content, "Audit changed during draft")
            backup = Path(scratch) / "previous"
            if candidate.exists():
                os.replace(candidate, backup)
            try:
                os.replace(folder, candidate)
            except OSError:
                if backup.exists():
                    os.replace(backup, candidate)
                raise
    return {"mode": "draft-for-chat-review", "candidate": str(candidate),
            "snapshot_sha256": model["content_sha256"], "media_count": len(media),
            "media_bytes": sum((candidate / row["path"]).stat().st_size for row in media),
            "cache": cache.stats, "performance_log": str(log)}


def review(candidate, output, source=None):
    candidate, output = safe_path(candidate), workspace(output)
    require(not output.resolve().is_relative_to(candidate.resolve()), "Keep review outside candidate")
    require(output.suffix == ".md", "Use a Markdown path for the review")
    receipt = output.with_suffix(".md.json")
    inventory = output.with_suffix(".md.facts.json")
    digest = snapshot_hash(candidate)
    overrides = {candidate.name: Path(source)} if source else None
    manifest, model, _ = validate_folder(candidate, candidate.parent, source_overrides=overrides,
                                          require_source=source is not None)
    body = (candidate / "analysis.md").read_text(encoding="utf-8")
    for row in manifest["media"]:
        rel = row["path"]
        path = (candidate / rel).as_posix()
        body = body.replace(f"]({rel})", f"](<{path}>)")
    require(snapshot_hash(candidate) == digest, "Candidate changed during review")
    atomic(output, body.encode())
    atomic(inventory, dumps(fact_inventory(model["audit"])).encode())
    atomic(receipt, dumps({"candidate": str(candidate.resolve()), "snapshot_sha256": digest,
                           "report": str(output)}).encode())
    return {"review": str(output), "receipt": str(receipt), "snapshot_sha256": digest,
            "fact_inventory": str(inventory)}


def export(candidate, output_root, receipt):
    candidate, output_root, receipt = safe_path(candidate), workspace(output_root), safe_path(receipt)
    require(not any(path.resolve().is_relative_to(candidate.resolve()) for path in (output_root, receipt)),
            "Receipt and ZIP must stay outside candidate")
    reviewed = read_json(receipt)
    require(isinstance(reviewed, dict) and reviewed.get("candidate") == str(candidate.resolve()),
            "Review receipt belongs to another candidate")
    digest = reviewed.get("snapshot_sha256")
    require(isinstance(digest, str) and re.fullmatch(r"[a-f0-9]{64}", digest),
            "Invalid review receipt digest")
    require(snapshot_hash(candidate) == digest, "Candidate changed since whole-snapshot review")
    manifest = read_json(candidate / "manifest.json")
    require(manifest.get("contract_version") == FORMAT_VERSION, f"Unsupported package format; audit again with the current HOMEKU kit ({FORMAT_VERSION})")
    paths = package_files(candidate, read_json(candidate / "audit.json"))
    name = f"{candidate.name}-r{manifest['revision']:04d}.zip"
    output_root.mkdir(parents=True, exist_ok=True)
    destination = safe_path(output_root / name)
    with tempfile.TemporaryDirectory(prefix=".export-", dir=output_root) as scratch:
        temp = Path(scratch) / name
        with zipfile.ZipFile(temp, "w", zipfile.ZIP_DEFLATED) as archive:
            for relative in paths:
                info = zipfile.ZipInfo(f"{candidate.name}/{relative}", date_time=(1980, 1, 1, 0, 0, 0))
                info.external_attr = 0o100644 << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                with (candidate / relative).open("rb") as source, archive.open(info, "w") as stream:
                    shutil.copyfileobj(source, stream)
        unpacked = extract_package(temp, Path(scratch) / "roundtrip")
        require(snapshot_hash(unpacked) == digest and snapshot_hash(candidate) == digest,
                "Export snapshot mismatch")
        os.replace(temp, destination)
    return {"mode": "reviewed-export", "package": str(destination), "snapshot_sha256": digest,
            "package_sha256": sha256(destination), "package_bytes": destination.stat().st_size}
