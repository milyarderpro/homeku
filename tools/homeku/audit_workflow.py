"""Readiness and source-bound aids for the audit workspace."""
import shutil
import subprocess
import sys
import tempfile
from importlib import import_module

from .audit_performance import safe_path
from .common import LibraryError, read_json, require, sha256, snapshot_hash

CUT_PREVIEW_MIN_DIFFERENCE = 0.05


def readiness(source, output):
    checks = []

    def record(name, ok, action):
        checks.append({"check": name, "ok": ok, **({} if ok else {"action": action})})

    record("python", sys.version_info >= (3, 11), "Use Python 3.11 or newer")
    modules = ("PIL", "jsonschema", "numpy", "cv2")
    available = {}
    for name in modules:
        try:
            import_module(name)
            available[name] = True
        except (ImportError, OSError):
            available[name] = False
        record(name, available[name], "Install requirements.txt in this Python environment")
    binaries = {name: shutil.which(name) for name in ("ffprobe", "ffmpeg")}
    for name, binary in binaries.items():
        record(name, bool(binary), f"Install {name} and make it available on PATH")

    if available["PIL"]:
        from .audit_session import workspace
        from .video import extract_frame, probe_video

        try:
            directory = workspace(output / "readiness-check").parent
            directory.mkdir(parents=True, exist_ok=True)
            with tempfile.TemporaryFile(dir=directory) as probe:
                probe.write(b"HOMEKU")
                probe.flush()
        except (LibraryError, OSError) as error:
            record("workspace", False, str(error))
        else:
            record("workspace", True, "")

        if binaries["ffprobe"]:
            try:
                require(source.suffix.casefold() == ".mp4" and source.is_file(), "Select the original MP4")
                info = probe_video(source)
            except (LibraryError, OSError) as error:
                record("mp4", False, str(error))
            else:
                record("mp4", True, "")
                if binaries["ffmpeg"]:
                    try:
                        extract_frame(source, 0, info["video_stream_index"])
                    except (LibraryError, OSError) as error:
                        record("frame", False, str(error))
                    else:
                        record("frame", True, "")
    return {"ok": all(check["ok"] for check in checks), "checks": checks}


def session_status(session_path, *, candidate=None, receipt=None):
    from .audit_session import (
        bind_audit, checked_camera_shots, load_session, pass_id, record_for, shot_camera_digests,
    )

    path, session, cache = load_session(session_path)
    audit = bind_audit(read_json(path.with_name("audit.json")), session)
    pass_ids = set()
    viewed_by_shot = {shot["shot"]: set() for shot in session["shots"]}
    incomplete_passes = {shot["shot"]: [] for shot in session["shots"]}
    for row in session["passes"]:
        pass_ids.add(row["id"])
        record = row["record"]
        shot_id = record["shot_id"]
        viewed = set(record["viewed_frame_indices"])
        viewed_by_shot[shot_id].update(viewed)
        selected = record["selected_frame_indices"]
        if record["viewed_frame_indices"] != selected:
            incomplete_passes[shot_id].append({
                "id": row["id"],
                "undeclared_frame_indices": [index for index in selected if index not in viewed],
            })
    verified = checked_camera_shots(session) if "camera_check" in session else {}
    shots = []
    for shot, observed in zip(session["shots"], audit["shots"], strict=True):
        baseline = record_for(cache, shot, shot["start_s"], shot["end_s"], reason="Status baseline")
        baseline_id = pass_id(session, baseline)
        shot_id = shot["shot"]
        viewed = viewed_by_shot[shot_id]
        camera = "unchecked"
        if shot_id in verified:
            camera = "current" if verified[shot_id] == shot_camera_digests(observed) else "stale"
        shots.append({"shot": shot_id, "baseline_pass": baseline_id if baseline_id in pass_ids else None,
                      "baseline_unviewed": [i for i in baseline["selected_frame_indices"] if i not in viewed],
                      "incomplete_passes": incomplete_passes[shot_id],
                      "camera": camera})

    candidate = safe_path(candidate) if candidate is not None else None
    receipt = safe_path(receipt) if receipt is not None else None
    missing = []
    if candidate is None or not candidate.is_dir():
        missing.append("candidate")
    if receipt is None or not receipt.is_file():
        missing.append("receipt")
    review = {"state": "missing", "missing": missing}
    if not missing:
        current = snapshot_hash(candidate)
        approved = read_json(receipt)
        matches = (isinstance(approved, dict) and approved.get("candidate") == str(candidate.resolve())
                   and approved.get("snapshot_sha256") == current)
        wrong_session = isinstance(approved, dict) and "session" in approved and approved["session"] != str(path.resolve())
        review = {"state": "matches" if matches and not wrong_session else "stale", "snapshot_sha256": current}
        if wrong_session:
            review["reason"] = "different-session"
    cache.ensure_source()
    return {"session": str(path), "shots": shots, "receipt": review}


def cut_preview(source, info, times, source_hash, output):
    """Suggest visual discontinuities using decoder order and keep native PTS."""
    from .audit_session import workspace
    from .motion_analysis import require_backend
    from .video import extract_frame
    from .video_cache import atomic

    destination = workspace(output / source_hash / "preview.jpg").parent
    cv, np = require_backend()
    source = source.resolve()
    dimension = 32
    frame_bytes = dimension * dimension * 3
    stream = info["video_stream_index"]
    scores = []
    with tempfile.TemporaryFile() as picture_data:
        try:
            subprocess.run([
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-protocol_whitelist", "file,pipe",
                "-i", str(source), "-map", f"0:{stream}", "-vf", f"scale={dimension}:{dimension}",
                "-pix_fmt", "rgb24", "-fps_mode", "passthrough", "-frames:v", str(len(times) + 1),
                "-threads", "1", "-f", "rawvideo", "pipe:1",
            ], stdout=picture_data, stderr=subprocess.PIPE, check=True, timeout=120)
        except (OSError, subprocess.SubprocessError) as error:
            raise LibraryError(f"Cannot scan the MP4 for suspected cuts: {error}") from error
        require(picture_data.tell() == len(times) * frame_bytes, "Cut scan frame count differs from native PTS")
        picture_data.seek(0)
        previous = np.frombuffer(picture_data.read(frame_bytes), dtype=np.uint8)
        for index in range(1, len(times)):
            current = np.frombuffer(picture_data.read(frame_bytes), dtype=np.uint8)
            difference = cv.mean(cv.absdiff(previous, current))[0] / 255
            if difference >= CUT_PREVIEW_MIN_DIFFERENCE:
                scores.append((difference, index))
            previous = current

    candidates = []
    for difference, index in sorted(sorted(scores, key=lambda row: (-row[0], row[1]))[:12],
                                    key=lambda row: row[1]):
        frames = []
        for native_index in (index - 1, index):
            image = destination / f"frame-{native_index:06d}.jpg"
            atomic(image, extract_frame(source, native_index, stream))
            frames.append({"index": native_index, "pts_s": times[native_index], "image": str(image)})
        candidates.append({"before": frames[0], "after": frames[1], "difference": round(difference, 4)})
    require(sha256(source) == source_hash, "Source changed during cut preview")
    return candidates
