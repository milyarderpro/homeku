"""Render, review and package an audit snapshot."""
from __future__ import annotations
import os
import re
import shutil
import tempfile
import zipfile
from contextlib import nullcontext
from pathlib import Path
from urllib.parse import quote
from . import FORMAT_VERSION
from .audit_performance import safe_path
from .audit_quality import fact_inventory
from .audit_review import checklist, review_changes, reviewed_summary
from .audit_session import bind_audit, camera_binding, load_session, pass_id, read_session_metadata, workspace
from .common import LibraryError, dumps, read_json, require, sha256, snapshot_hash
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
    with locked(output_root, recovery=False):
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


def _retain_review_payload(candidate, destination, digest):
    """Keep the exact reviewed bytes available after a replacement draft."""
    destination = safe_path(destination)
    if not destination.exists():
        destination.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix=".review-", dir=destination.parent) as scratch:
            copy = Path(scratch) / candidate.name
            shutil.copytree(candidate, copy, symlinks=True)
            require(snapshot_hash(copy) == digest, "Candidate changed during review")
            os.rename(copy, destination)
    require(snapshot_hash(destination) == digest, "Saved review payload differs from the reviewed snapshot")


def review(candidate, output, source=None, *, attempt=None, session_path=None):
    candidate, output = safe_path(candidate), workspace(output)
    require(not output.is_relative_to(candidate), "Keep review outside candidate")
    require(output.suffix == ".md", "Use a Markdown path for the review")
    history_path = None
    with locked(candidate.parent, recovery=False):
        digest = snapshot_hash(candidate)
        if attempt is not None:
            attempt["snapshot_sha256"] = digest
        context = None
        if session_path is not None:
            path, session, cache = load_session(session_path)
            if source is None:
                source = cache.source
            if Path(source).resolve() == cache.source:
                context = {"sha256": cache.source_hash, "info": cache.info, "times": cache.times}
            history_path = workspace(path.parent / ".homeku" / "reviews" / f"{camera_binding(session)}.json")
        overrides = {candidate.name: Path(source)} if source is not None else None
        manifest, model, _ = validate_folder(candidate, candidate.parent, source_overrides=overrides,
                                             require_source=source is not None, context=context)
        if session_path is not None:
            bind_audit(model["audit"], session)
            require(manifest["source"]["sha256"] == cache.source_hash, "Review candidate differs from session source")
            viewed = {row["id"]: row["record"]["viewed_frame_indices"] for row in session["passes"]}
            for record in manifest["audit"]["frame_reviews"]:
                require(viewed.get(pass_id(session, record)) == record["viewed_frame_indices"],
                        "Review candidate includes frame declarations absent from the supplied session")
            cache.ensure_source()
        report = workspace(output.with_suffix(".snapshots") / digest / output.name)
        payload = report.parent / "payload" / candidate.name
        _retain_review_payload(candidate, payload, digest)

    body = (payload / "analysis.md").read_text(encoding="utf-8")
    for row in manifest["media"]:
        rel = row["path"]
        media_path = quote((payload / rel).as_posix(), safe="/:")
        body = body.replace(f"]({rel})", f"](<{media_path}>)")

    receipt = report.with_suffix(".md.json")
    inventory = report.with_suffix(".md.facts.json")
    sheet = report.with_suffix(".checklist.md")
    lock = locked(path.parent, recovery=False) if history_path is not None else nullcontext()
    with lock:
        changes = ()
        if history_path is not None:
            current = reviewed_summary(model["audit"], manifest, digest)
            previous = None
            if history_path.is_file():
                history = read_json(history_path)
                latest = history["current"]
                previous = history["previous"] if latest["snapshot_sha256"] == digest else latest
            changes = review_changes(previous, current)
        checks = checklist(payload, report, model["audit"], manifest, digest, source_verified=source is not None,
                           changes=changes)
        require(snapshot_hash(candidate) == digest, "Candidate changed during review")
        facts = dumps(fact_inventory(model["audit"])).encode()
        receipt_data = {"candidate": str(candidate.resolve()), "snapshot_sha256": digest, "report": str(report)}
        if history_path is not None:
            receipt_data["session"] = str(path.resolve())
        receipt_bytes = dumps(receipt_data).encode()
        for target in (report, output):
            atomic(target, body.encode())
            atomic(target.with_suffix(".md.facts.json"), facts)
            atomic(target.with_suffix(".checklist.md"), checks.encode())
        if history_path is not None:
            atomic(history_path, dumps({"current": current, "previous": previous}).encode())
        atomic(receipt, receipt_bytes)
        atomic(output.with_suffix(".md.json"), receipt_bytes)
    return {"review": str(report), "receipt": str(receipt), "snapshot_sha256": digest,
            "fact_inventory": str(inventory), "checklist": str(sheet)}


def export_session_path(candidate, receipt, session_path):
    """Validate the logging destination using stored metadata, without the MP4."""
    path, session = read_session_metadata(session_path)
    path = path.resolve()
    candidate, receipt = safe_path(candidate), safe_path(receipt)
    try:
        reviewed = read_json(receipt)
    except (LibraryError, OSError):
        reviewed = None
    if isinstance(reviewed, dict) and "session" in reviewed:
        require(reviewed["session"] == str(path), "Review receipt belongs to another session")
        return path

    # Receipts from earlier kits have no session path. Check any available source binding
    # and let export report missing or corrupt inputs within the correct performance log.
    try:
        manifest = read_json(safe_path(candidate / "manifest.json"))
        audit = read_json(safe_path(candidate / "audit.json"))
    except (LibraryError, OSError):
        return path
    source = manifest.get("source") if isinstance(manifest, dict) else None
    if isinstance(source, dict) and isinstance(source.get("sha256"), str):
        require(source["sha256"] == session["source"]["sha256"], "Export candidate differs from session source")
    if isinstance(audit, dict) and isinstance(audit.get("shots"), list) and isinstance(audit.get("id"), str):
        bind_audit(audit, session)
    return path


def export(candidate, output_root, receipt, *, attempt=None):
    candidate, output_root, receipt = safe_path(candidate), workspace(output_root), safe_path(receipt)
    require(not any(path.resolve().is_relative_to(candidate.resolve()) for path in (output_root, receipt)),
            "Receipt and ZIP must stay outside candidate")
    reviewed = read_json(receipt)
    require(isinstance(reviewed, dict) and reviewed.get("candidate") == str(candidate.resolve()),
            "Review receipt belongs to another candidate")
    digest = reviewed.get("snapshot_sha256")
    require(isinstance(digest, str) and re.fullmatch(r"[a-f0-9]{64}", digest),
            "Invalid review receipt digest")
    current = snapshot_hash(candidate)
    if attempt is not None:
        attempt["snapshot_sha256"] = current
    require(current == digest, "Candidate changed since whole-snapshot review")
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
        package_sha256 = sha256(temp)
        package_bytes = temp.stat().st_size
        with locked(output_root, recovery=False):
            if destination.exists() and (not destination.is_file() or sha256(destination) != package_sha256):
                destination = safe_path(output_root / digest / name)
            if destination.exists():
                require(destination.is_file() and sha256(destination) == package_sha256,
                        "The saved ZIP differs from this export")
            else:
                destination.parent.mkdir(parents=True, exist_ok=True)
                os.replace(temp, destination)
    return {"mode": "reviewed-export", "package": str(destination), "snapshot_sha256": digest,
            "package_sha256": package_sha256, "package_bytes": package_bytes}
