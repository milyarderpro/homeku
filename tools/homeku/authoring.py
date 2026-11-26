"""Mechanical authoring helpers; observations are written by the auditor."""
import copy
import re
from pathlib import Path
from jsonschema import Draft202012Validator
from . import FORMAT_VERSION
from .common import LibraryError, dumps, read_json, require
from .video_cache import FrameCache,atomic
from .audit_performance import timed,event
from .audit_session import (
    bind_audit, checked_camera_shots, load_session, make_shots, materialize, record_for, require_current_camera,
    save_camera_check, shot_camera_digests, workspace,
)
from .derivations import camera_summary
from .preflight import camera_input

ROOT=Path(__file__).resolve().parents[2]

def _baseline_records(cache, shots):
    records = []
    for shot in shots:
        record = record_for(cache, shot, shot["start_s"], shot["end_s"],
                            reason="Baseline 6 FPS/native dan batas shot dari cut terkonfirmasi.")
        records.append(record)
        if shot["middle"] not in record["selected_frame_indices"]:
            i = shot["middle"]
            end = min(shot["end_s"], cache.times[i + 1] if i + 1 < len(cache.times) else shot["end_s"])
            records.append(record_for(cache, shot, cache.times[i], end, native=True,
                                      reason="Frame midpoint calon panel; belum dinyatakan viewed."))
    return records


def prepare(source, cuts, output, *, resume=False):
    output = workspace(output)
    output.mkdir(parents=True, exist_ok=True)
    session_path, audit_path, info_path = (output / name for name in
                                           ("session.json", "audit.json", "audit-info.json"))
    if session_path.exists():
        require(resume, "Workspace already prepared; use --resume to preserve observations")
        path, session, cache = load_session(session_path)
        require(Path(source).resolve() == cache.source and cuts == session["cuts"],
                "Source/cuts differ; prepare a new workspace")
        bind_audit(read_json(audit_path), session, cache)
        require(info_path.is_file(), "Missing working audit-info.json")
        materialize(path, session, cache, _baseline_records(cache, session["shots"]))
        return {"session": str(path), "audit": str(audit_path), "audit_info": str(info_path),
                "resumed": True, "shots": session["shots"], "passes": session["passes"],
                "cache": cache.stats}
    require(not audit_path.exists() and not info_path.exists(),
            "Refusing to overwrite existing audit source")
    with timed(output / "performance.jsonl", "prepare"):
        cache = FrameCache(source, output / ".cache" / "frames", log=output / "performance.jsonl")
        rid = cache.source.stem
        require(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}", rid)
                and cache.source.suffix.casefold() == ".mp4", "Use the canonical MP4 filename")
        session = {"format_version": FORMAT_VERSION, "runtime_signature": cache.signature,
                   "source": {"path": str(cache.source), "sha256": cache.source_hash},
                   "cuts": cuts, "shots": make_shots(cache, cuts), "passes": []}
        audit = read_json(ROOT / "audit/template-audit.json")
        require(audit.get("schema_version") == FORMAT_VERSION, "Template format differs from runtime")
        audit["id"] = rid
        base = copy.deepcopy(audit["shots"][0])
        audit["areas"], audit["shots"] = [], []
        for n, row in enumerate(session["shots"]):
            shot = copy.deepcopy(base)
            shot.update(shot=row["shot"], start_s=row["start_s"], end_s=row["end_s"],
                        transition="end" if n == len(session["shots"]) - 1 else "cut",
                        area_ids=[])
            for p, key in zip(shot["panels"], ("first", "middle", "last")):
                p.update(frame_index=row[key], area_ids=[])
            for p in shot["overviews"]:
                p.update(frame_index=None, area_ids=[])
            for d in shot["design"]:
                d["area_ids"] = []
            for phase in shot["camera"]["phases"]:
                phase.update(start_s=row["start_s"], end_s=row["end_s"])
            audit["shots"].append(shot)
        atomic(audit_path, dumps(audit).encode())
        atomic(info_path, (ROOT / "audit/template-audit-info.json").read_bytes())
        atomic(session_path, dumps(session).encode())
        materialize(session_path, session, cache, _baseline_records(cache, session["shots"]))
    return {"session": str(session_path), "audit": str(audit_path), "audit_info": str(info_path),
            "resumed": False, "shots": session["shots"], "passes": session["passes"],
            "cache": cache.stats, "next": "View sheets, fill observations, then declare viewed explicitly."}

def check_camera(session_path, *, shot_id=None):
    """Validate and bind camera findings before entering the design phase."""
    session_bytes = workspace(session_path).read_bytes()
    path, session, cache = load_session(session_path)
    target = workspace(path.parent / "audit.json")
    original = target.read_bytes()
    audit = bind_audit(read_json(target), session, cache)
    pairs = list(zip(audit["shots"], session["shots"], strict=True))
    if shot_id is None:
        if "camera_check" in session:
            require_current_camera(session, audit)
        checkpoints = {}
    else:
        checkpoints = dict(checked_camera_shots(session))
        pairs = [(shot, native) for shot, native in pairs if shot["shot"] == shot_id]
        require(pairs, f"Unknown session shot: {shot_id}")
    records = [item["record"] for item in session["passes"]]
    for shot, native in pairs:
        shot["camera"] = camera_input(shot, native, records, cache.source, cache.info, cache.times)
        checkpoints[shot["shot"]] = shot_camera_digests(shot)
    cache.ensure_source()
    require(path.read_bytes() == session_bytes and target.read_bytes() == original,
            "Session or audit changed during check-camera; rerun the command")
    normalized = dumps(audit).encode()
    if normalized != original:
        atomic(target, normalized)
    save_camera_check(path, session, checkpoints)
    return {"session": str(path), "checked": [
        {"shot": shot["shot"], "camera_movement": camera_summary(shot),
         "tempo": shot["camera"]["tempo"]["description"],
         "production_start": shot.get("composition", {}).get("production_start"),
         "digests": checkpoints[shot["shot"]]} for shot, _ in pairs
    ]}


def update_shot(session_path, shot_id, patch_path):
    """Merge a JSON object into one working shot; replace arrays as a unit."""
    path, session, cache = load_session(session_path)
    target = workspace(path.parent / "audit.json")
    patch = read_json(Path(patch_path))
    require(isinstance(patch, dict) and patch, "Shot patch must be a nonempty JSON object")
    locked = {"shot", "start_s", "end_s", "transition"}
    require(not (locked & patch.keys()), "Shot ID, boundaries and transition are locked")
    audit = bind_audit(read_json(target), session, cache)
    index = next((i for i, shot in enumerate(audit["shots"]) if shot["shot"] == shot_id), None)
    require(index is not None, f"Unknown session shot: {shot_id}")

    def merge(old, changes):
        result = dict(old)
        for key, value in changes.items():
            previous = result.get(key)
            result[key] = merge(previous, value) if isinstance(previous, dict) and isinstance(value, dict) else value
        return result

    schema = read_json(ROOT / "schemas/audit.schema.json")
    validator = Draft202012Validator({"$defs": schema["$defs"], "$ref": "#/$defs/shot"})
    original = audit["shots"][index]
    updated = merge(original, patch)
    # The prepared skeleton can be incomplete. Reject new schema errors without
    # requiring observations in untouched fields or other shots.
    def error_key(error):
        return tuple(error.path), error.message

    existing = {error_key(error) for error in validator.iter_errors(original)}
    for error in validator.iter_errors(updated):
        suffix = "/".join(str(part) for part in error.path)
        require(error_key(error) in existing, f"{shot_id}/{suffix}: {error.message}")
    needs_camera_check = ("camera_check" in session
                          and checked_camera_shots(session)[shot_id] != shot_camera_digests(updated))
    audit["shots"][index] = updated
    atomic(target, dumps(audit).encode())
    return {"audit": str(target), "shot": shot_id, "camera_recheck_required": needs_camera_check}

def complete(audit_path, *, session_path=None, info_path=None):
    """Fill mechanical values and copy explicit declarations from the session."""
    audit_path = workspace(audit_path)
    require(session_path is not None, "Complete requires the source-bound session")
    path, session, cache = load_session(session_path)
    info_target = workspace(info_path or path.parent / "audit-info.json")
    require(len({audit_path.resolve(), path.resolve(), info_target.resolve()}) == 3,
            "Audit, session and audit-info must be separate files")
    audit = bind_audit(read_json(audit_path), session, cache)
    require_current_camera(session, audit)
    info = read_json(info_target)
    require(isinstance(info, dict), "Working audit-info must be a JSON object")
    changes = []

    def assign(obj, key, value, pointer):
        if obj.get(key) != value:
            obj[key] = value
            changes.append(f"{pointer}/{key}")

    log = path.parent / "performance.jsonl"
    with timed(log, "complete"):
        for i, (shot, row) in enumerate(zip(audit["shots"], session["shots"])):
            pointer = f"/shots/{i}"
            panels = shot["panels"]
            require(len(panels) >= 2, f"{pointer}/panels: retain first and last panels")
            if len(shot["area_ids"]) == 1:
                require(len(panels) == 3, f"{pointer}/panels: normal shot requires three panels")
                production_start = shot["composition"].get("production_start")
                if production_start is not None:
                    assign(panels[0], "frame_index", production_start["frame_index"], f"{pointer}/panels/0")
            else:
                assign(panels[0], "frame_index", row["first"], f"{pointer}/panels/0")
                assign(panels[-1], "frame_index", row["last"], f"{pointer}/panels/{len(panels)-1}")
            for group in ("panels", "overviews"):
                for j, item in enumerate(shot[group]):
                    frame = item.get("frame_index")
                    require(type(frame) is int and row["first"] <= frame <= row["last"],
                            f"{pointer}/{group}/{j}/frame_index: select a native frame within this shot")
                indices = [item["frame_index"] for item in shot[group]]
                require(indices == sorted(indices), f"{pointer}/{group}: selections must follow source chronology")
        records = [item["record"] for item in session["passes"]]
        info["frame_reviews"] = records
        info["reviewed_ranges"] = [
            {key: record[key] for key in ("start_s", "end_s", "mode")}
            for record in records if record["selected_frame_indices"] == record["viewed_frame_indices"]
            and record["viewed_frame_indices"]
        ]
        audit_bytes, info_bytes = dumps(audit).encode(), dumps(info).encode()
        cache.ensure_source()
        if changes:
            atomic(audit_path, audit_bytes)
        atomic(info_target, info_bytes)
        event(log, "complete-changes", paths=changes)
    return {"audit": str(audit_path), "audit_info": str(info_target),
            "changes": changes, "next": "Run check-input with the completed working files."}
