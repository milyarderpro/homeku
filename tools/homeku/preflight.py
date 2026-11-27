"""Collect independent input errors before any final JPEG is rendered."""
import copy
import re
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker
from . import FORMAT_VERSION
from .audit_session import bind_audit, load_session, require_current_camera
from .audit_quality import camera_evidence, validate_audit_logs, validate_frame_reviews, validate_motion
from .camera_notation import normalize, parse
from .common import LibraryError, read_json, require
from .models import (
    ROOT, _clean, validate_audit, validate_camera_timeline, validate_production_start, validate_profile,
)
from .video_cache import FrameCache


def canonical_notation(text):
    return " + ".join(clause["raw"] for clause in parse(normalize(text)))


def camera_input(shot, native, reviews, source, info, times):
    """Check one camera block against prepared native bounds before design is authored."""
    sid = native["shot"]
    composition = shot.get("composition", {})
    require(isinstance(composition, dict), f"{sid}/composition: expected an object")
    fields = [("camera", shot.get("camera"), "#/$defs/camera")]
    if "production_start" in composition:
        fields.append(("composition/production_start", composition["production_start"],
                       "#/$defs/composition/properties/production_start"))
    defs = read_json(ROOT / "schemas/audit.schema.json")["$defs"]
    for path, value, ref in fields:
        error = next(Draft202012Validator({"$defs": defs, "$ref": ref}).iter_errors(value), None)
        if error is not None:
            suffix = "".join(f"/{part}" for part in error.path)
            raise LibraryError(f"{sid}/{path}{suffix}: {error.message}")
        _clean(value, f"{sid}/{path}")
    normalized = {**native, "camera": copy.deepcopy(shot["camera"]), "composition": composition}
    for i, phase in enumerate(normalized["camera"]["phases"]):
        try:
            phase["notation"] = canonical_notation(phase["notation"])
        except ValueError as error:
            raise LibraryError(f"{sid}/camera/phases/{i}/notation: {error}") from error
    validate_camera_timeline(normalized)
    validate_production_start(normalized, times, path=sid)
    try:
        validate_motion({"shots": [normalized]}, times)
    except ValueError as error:
        raise LibraryError(f"{sid}/camera: {error}") from error
    records = [row for row in reviews if row["shot_id"] == sid]
    completed = [row for row in records
                 if row["selected_frame_indices"] == row["viewed_frame_indices"]]
    validate_frame_reviews(completed, [normalized], source, info, times=times)
    viewed = {index for row in completed for index in row["viewed_frame_indices"]}
    missing = sorted(set(camera_evidence(normalized)) - viewed)
    require(not missing, f"{sid}/camera: mark the evidence pass viewed for native frames {missing}")
    return normalized["camera"]


def check_inputs(source, audit, audit_info, *, session_path=None, limit=100, supersedes=None,
                 purpose="reference", cache_dir=None, log=None):
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
        add("/audit/schema_version", "schema", "Unsupported audit format",
            f"Audit ulang MP4 dengan kit HOMEKU {FORMAT_VERSION}.")
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
    def verified_cache():
        require(session_path is not None, "The source-bound session is required; run check-camera")
        _, session, bound_cache = load_session(session_path)
        require(source == bound_cache.source, "Source differs from the camera check session")
        bind_audit(audit, session)
        require_current_camera(session, audit)
        return bound_cache

    cache = capture("/session", "camera", verified_cache,
                    "Jalankan check-camera pada sesi sumber. Jika kamera dikoreksi, periksa ulang shot terkait.")
    if cache is None:
        return result()
    if cache_dir is not None and Path(cache_dir).resolve() != cache.root:
        render_cache = capture("/source", "metadata", lambda: FrameCache(source, cache_dir, log=log))
        if render_cache is None:
            return result()
        if render_cache.source_hash != cache.source_hash:
            add("/source", "camera", "Source changed after check-camera")
            return result()
        cache = render_cache
    info, times = cache.info, cache.times
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
    return result({"info": info, "times": times, "logs": audit_info, "sha256": cache.source_hash, "cache": cache})


def require_inputs(source, audit, audit_info, **kwargs):
    result = check_inputs(source, audit, audit_info, **kwargs)
    if not result["ok"]:
        import json
        raise LibraryError("Input preflight failed before media render: " +
                           json.dumps(result["errors"], ensure_ascii=False))
    return result["context"]
