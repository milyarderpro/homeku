"""Temporal/source quality checks; these never invent visual observations."""
import bisect
from .common import require, schema_check
from .camera_notation import parse
from .camera_pattern import validate_direction
from .derivations import claims, referenced_frames
from .video import selected_indices, frame_times


def camera_evidence(shot):
    for phase in shot["camera"]["phases"]:
        yield from phase["evidence"]
        for override in phase.get("overrides", []):
            yield from override.get("evidence", ())
    choice = shot["composition"].get("production_start")
    if choice is not None:
        yield choice["frame_index"]


def validate_motion(audit, times=None, *, allow_placeholder=False):
    for shot in audit["shots"]:
        for phase in shot["camera"]["phases"]:
            notation = phase["notation"]
            parsed = None if allow_placeholder and "{{" in notation else parse(notation)
            if parsed is not None:
                validate_direction(phase)
            overrides = phase.get("overrides", [])
            indices = [o["component_index"] for o in overrides]
            require(len(indices) == len(set(indices)) and
                    all(type(i) is int and (parsed is None or i < len(parsed)) for i in indices),
                    "Invalid/duplicate component override")
            if times is None:
                continue

            def temporal(evidence, required=True):
                unique = set(evidence)
                require(not required or len(unique) >= 2,
                        "Movement requires at least two distinct temporal native frames")
                lo = bisect.bisect_left(times, phase["start_s"])
                hi = bisect.bisect_left(times, phase["end_s"])
                shot_lo = bisect.bisect_left(times, shot["start_s"])
                shot_hi = bisect.bisect_left(times, shot["end_s"])
                require(all(type(i) is int and shot_lo <= i < shot_hi and
                            max(shot_lo, lo - 1) <= i <= min(shot_hi - 1, hi)
                            for i in unique), "Camera evidence outside phase/native-boundary tolerance")
                require(not unique or any(lo <= i < hi for i in unique),
                        "At least one camera evidence frame must be within the phase")

            temporal(phase["evidence"], parsed is not None and any(c["movement"] != "Uncertain" for c in parsed))
            for override in overrides:
                temporal(override.get("evidence", phase["evidence"]),
                         parsed is not None and parsed[override["component_index"]]["movement"] != "Uncertain")


def _cover(intervals, start, end, message):
    cursor = start
    for left, right in sorted(intervals):
        if right <= cursor:
            continue
        require(left <= cursor + 1e-6, message)
        cursor = max(cursor, right)
        if cursor >= end - 1e-6:
            return
    require(cursor >= end - 1e-6, message)


def validate_frame_reviews(reviews, shots, source, info, *, times=None, check_coverage=True):
    """Declarations are checked against native PTS; actual viewing remains explicit."""
    times = frame_times(source) if times is None else times
    fps = info["fps"]["numerator"] / info["fps"]["denominator"]
    shot_map = {s["shot"]: s for s in shots}
    coverage = {sid: [] for sid in shot_map}
    for review in reviews:
        sid = review["shot_id"]
        require(sid in shot_map, "Frame review has unknown shot")
        shot = shot_map[sid]
        start, end = review["start_s"], review["end_s"]
        require(shot["start_s"] <= start < end <= shot["end_s"], "Frame review outside shot")
        native = review["mode"] == "frame-by-frame"
        rate = review["sampling_fps"]
        require((native and rate is None) or (not native and rate is not None),
                "Native review requires null sampling FPS; sampling declares FPS")
        expected = selected_indices(times, start, end, rate or 6, native=native, source_fps=fps)
        require(review["selected_frame_indices"] == expected, "Selected indices differ from native PTS")
        require(review["viewed_frame_indices"] == expected,
                "Frame review incomplete: only declare frames actually viewed")
        require(review["reason"].strip(), "Frame review needs a visual question/reason")
        qualified = native or rate >= min(6, fps)
        if fps <= 6 or shot["end_s"] - shot["start_s"] < 1:
            qualified = expected == selected_indices(times, start, end, native=True)
        if qualified:
            coverage[sid].append((start, end))
    if check_coverage:
        for sid, shot in shot_map.items():
            _cover(coverage[sid], shot["start_s"], shot["end_s"],
                   f"Every shot requires complete 6 FPS/native viewed coverage: {sid}")
    return times


def validate_production_start_viewed(audit, reviews):
    for i, shot in enumerate(audit["shots"]):
        choice = shot["composition"].get("production_start")
        if choice is None:
            continue
        index = choice["frame_index"]
        require(any(row["shot_id"] == shot["shot"] and index in row["selected_frame_indices"]
                    and index in row["viewed_frame_indices"] for row in reviews),
                f"/frame_reviews: frame not actually declared viewed for /shots/{i}/composition/production_start/frame_index")


def validate_referenced_frames_viewed(audit, reviews):
    validate_production_start_viewed(audit, reviews)
    viewed = {index for row in reviews for index in row["viewed_frame_indices"]}
    require(set(referenced_frames(audit)) <= viewed, "Evidence/panel/Overview not actually declared viewed")


def validate_audit_logs(logs, audit, source, info, *, times=None):
    schema_check(logs, "audit-info.schema.json")
    times = validate_frame_reviews(logs["frame_reviews"], audit["shots"], source, info, times=times)
    ranges = []
    for row in logs["reviewed_ranges"]:
        require(0 <= row["start_s"] < row["end_s"] <= info["duration_s"],
                "Invalid declared reviewed range")
        if row["mode"] == "frame-by-frame":
            _cover([(p["start_s"], p["end_s"]) for p in logs["frame_reviews"]
                    if p["mode"] == "frame-by-frame"], row["start_s"], row["end_s"],
                   "Native coverage claim lacks native viewed records")
        ranges.append((row["start_s"], row["end_s"]))
    _cover(ranges, 0, info["duration_s"], "Declared reviewed ranges do not cover source")
    validate_referenced_frames_viewed(audit, logs["frame_reviews"])
    return times


def fact_inventory(audit):
    """Workspace review aid with source pointers; not a second source or ZIP member."""
    rows = []
    for pointer, claim, areas, shot, category in claims(audit):
        if category == "camera":
            continue
        row = {"source_pointer": pointer, "category": category, "area_ids": areas,
               "shot": shot, "state": claim["state"], "evidence": claim["evidence"]}
        row.update({k: claim[k] for k in ("subject", "attribute", "value", "confidence", "note")
                    if k in claim})
        rows.append(row)
    return rows
