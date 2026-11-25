"""Collect independent input errors before any final JPEG is rendered."""
import re
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker
from . import FORMAT_VERSION
from .audit_quality import validate_audit_logs, validate_frame_reviews
from .common import LibraryError, read_json, require, sha256
from .models import ROOT, _clean, validate_audit, validate_profile
from .video import frame_times, probe_video


def check_inputs(source, audit, audit_info, *, limit=100, supersedes=None, purpose="reference",
                 cache_dir=None, log=None):
    errors = []

    def add(path, group, message, action="Perbaiki field ini, lalu jalankan check-input kembali."):
        if len(errors) < limit:
            errors.append({"path": path, "group": group, "message": message, "action": action})

    def capture(path, group, fn, action=None):
        try:
            return fn()
        except (LibraryError, OSError) as exc:
            message = str(exc)
            if message.startswith("/"):
                pointer, sep, detail = message.partition(": ")
                if sep:
                    path, message = path + pointer, detail
            add(path, group, message, *([action] if action else []))
            return None

    def schema(value, spec, prefix):
        entries = sorted(Draft202012Validator(spec, format_checker=FormatChecker()).iter_errors(value),
                         key=lambda error: str(list(error.path)))
        for error in entries:
            parts = list(error.path)
            if error.validator == "required":
                field = re.match(r"'([^']+)' is a required property", error.message)
                if field:
                    parts.append(field[1])
            pointer = prefix + "".join("/" + str(key).replace("~", "~0").replace("/", "~1")
                                       for key in parts)
            add(pointer, "schema", error.message,
                "Lengkapi struktur sesuai template dan catat pengamatan yang tersedia.")
        return not entries

    def result(context=None):
        return {"ok": not errors, "errors": errors, "context": context if not errors else None}

    require(type(limit) is int and limit > 0, "Error limit must be positive")
    if not isinstance(audit, dict) or audit.get("schema_version") != FORMAT_VERSION:
        add("/audit/schema_version", "schema", "Unsupported audit format; use the current HOMEKU kit")
        return result()
    schema(audit, read_json(ROOT / "schemas/audit.schema.json"), "/audit")
    schema(audit_info, read_json(ROOT / "schemas/audit-info.schema.json"), "/audit-info")
    header = read_json(ROOT / "schemas/manifest.schema.json")["properties"]
    schema(supersedes, header["supersedes"], "/manifest/supersedes")
    schema(purpose, header["purpose"], "/manifest/purpose")
    if errors:
        return result()
    capture("/audit", "observations", lambda: _clean(audit))
    design = audit["design"]
    for field in ("house_type", "palette"):
        if field not in design:
            add("/audit/design/" + field, "profile", "New audit drafts require the standard design profile.")
    capture("/audit", "profile", lambda: validate_profile(design))
    capture("/audit-info", "observations", lambda: _clean(audit_info))
    size = audit["design"]["size"]["floor_area_m2"]
    if size["min"] > size["max"]:
        add("/audit/design/size/floor_area_m2", "semantics", "Minimum exceeds maximum")
    if not ((audit["revision"] == 1 and supersedes is None) or
            (isinstance(supersedes, dict) and supersedes["revision"] == audit["revision"] - 1)):
        add("/manifest/supersedes", "revision", "Use null for revision 1 and identify the preceding revision otherwise")
    source = Path(source).resolve()
    if source.stem != audit["id"] or source.suffix.casefold() != ".mp4":
        add("/audit/id", "source", "ID must match original MP4 stem")
    if not source.is_file():
        add("/source", "source", "Source unavailable")
    if errors:
        return result()
    cache = None
    if cache_dir is not None:
        from .video_cache import FrameCache
        cache = capture("/source", "metadata", lambda: FrameCache(source, cache_dir, log=log))
        if cache is None:
            return result()
        info, times = cache.info, cache.times
    else:
        info = capture("/source", "metadata", lambda: probe_video(source))
        if info is None:
            return result()
        times = capture("/source", "timestamps", lambda: frame_times(source, info=info))
        if times is None:
            return result()
    capture("/audit", "semantics", lambda: validate_audit(audit, info["duration_s"], times))
    frames_ok = True
    for i, row in enumerate(audit_info["frame_reviews"]):
        checked = capture(f"/audit-info/frame_reviews/{i}", "frames",
                          lambda: validate_frame_reviews([row], audit["shots"], source, info,
                                                         times=times, check_coverage=False),
                          "Gunakan mark-viewed setelah frame benar-benar diperiksa.")
        frames_ok = frames_ok and checked is not None
    if frames_ok and not errors:
        capture("/audit-info", "coverage",
                lambda: validate_audit_logs(audit_info, audit, source, info, times=times))
    if errors:
        return result()
    digest = cache.source_hash if cache else capture("/source", "hash", lambda: sha256(source))
    return result({"info": info, "times": times, "logs": audit_info, "sha256": digest, "cache": cache})


def require_inputs(source, audit, audit_info, **kwargs):
    result = check_inputs(source, audit, audit_info, **kwargs)
    if not result["ok"]:
        import json
        raise LibraryError("Input preflight failed before media render: " +
                           json.dumps(result["errors"], ensure_ascii=False))
    return result["context"]
