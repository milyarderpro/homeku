"""Canonical audit validation. No Markdown source or legacy expanded model."""
import bisect
import math
import re
from pathlib import Path
from . import FORMAT_VERSION
from .common import require, schema_check
from .derivations import claims, fact_claims, CATEGORIES, tempo_segments

ROOT = Path(__file__).resolve().parents[2]


def _clean(value, path=""):
    if isinstance(value, dict):
        for key, item in value.items():
            _clean(item, path + "/" + key)
    elif isinstance(value, list):
        for i, item in enumerate(value):
            _clean(item, path + "/" + str(i))
    elif isinstance(value, float):
        require(math.isfinite(value), path + ": nonfinite number")
    elif isinstance(value, str):
        require(value.strip(), path + ": blank field")
        require("{{" not in value and "}}" not in value and "\x00" not in value,
                path + ": unfilled placeholder or NUL")


def validate_profile(design):
    require(not any(claim["aspect"] == "palette" for claim in design["features"]),
            "/design/palette: use the structured palette as the only palette source")


def validate_production_start(shot, frames=None, *, path):
    if "production_start" not in shot["composition"]:
        return
    index = shot["composition"]["production_start"]["frame_index"]
    path += "/composition/production_start/frame_index"
    require(type(index) is int and index >= 0,
            path + ": choose a native frame index after native Start in the same shot")
    if frames is not None:
        if isinstance(frames, dict):
            pts = frames.get(str(index))
        else:
            pts = frames[index] if index < len(frames) else None
        require(pts is not None and shot["start_s"] < pts < shot["end_s"],
                path + ": frame PTS must be after native Start and within the shot")


def validate_camera_timeline(shot):
    start, end = shot["start_s"], shot["end_s"]
    sid = shot["shot"]
    for group in (shot["camera"]["phases"], tempo_segments(shot)):
        cursor = start
        for item in group:
            require(start <= item["start_s"] < item["end_s"] <= end, sid + "/camera: invalid interval")
            require(abs(item["start_s"] - cursor) < 1e-6, sid + ": camera timeline gap/overlap")
            cursor = item["end_s"]
        require(abs(cursor - end) < 1e-6, sid + ": camera timeline incomplete")


def validate_claim_evidence(claim, ids, shot, times, visible, pointer, *, camera=False):
    require(claim.get("evidence") or claim.get("state") == "unknown" or camera,
            pointer + ": claim requires evidence unless unknown")
    if times is None:
        return
    evidence_sets = [(pointer, claim.get("evidence", []))]
    if camera:
        evidence_sets.extend((f"{pointer}/overrides/{number}", override["evidence"])
                             for number, override in enumerate(claim.get("overrides", ())) if "evidence" in override)
    for location, evidence in evidence_sets:
        for index in evidence:
            require(type(index) is int and 0 <= index < len(times), location + ": unknown native evidence")
            if shot is not None:
                require(shot["start_s"] <= times[index] < shot["end_s"], location + ": evidence outside shot")
            if ids:
                require(any(visible(aid, times[index]) for aid in ids), location + ": evidence outside area visibility")


def validate_audit(audit, duration=None, times=None):
    require(isinstance(audit, dict) and audit.get("schema_version") == FORMAT_VERSION,
            "Unsupported audit format; use the current HOMEKU kit and audit again")
    schema_check(audit, "audit.schema.json")
    _clean(audit)
    validate_profile(audit["design"])
    shots = audit["shots"]
    require([s["shot"] for s in shots] == [f"shot-{i:02d}" for i in range(1, len(shots) + 1)],
            "Shot IDs must be sequential")
    end = shots[-1]["end_s"]
    require(abs(shots[0]["start_s"]) < 1e-6, "Timeline must start at zero")
    require(duration is None or abs(end - duration) < 1e-6, "Timeline must cover source duration")
    area_map = {a["id"]: a for a in audit["areas"]}
    require(len(area_map) == len(audit["areas"]), "Duplicate physical area ID")
    styles = audit["design"]["styles"]
    require(all(c["value"] is None or isinstance(c["value"], str)
                for c in (styles["primary"], *styles["influences"], *styles["interior"])),
            "/design/styles: use a separate English style name or an explicit unknown claim")
    size = audit["design"]["size"]["floor_area_m2"]
    require(size["min"] <= size["max"], "/design/size/floor_area_m2: min exceeds max")
    for area in area_map.values():
        previous = 0
        for interval in area["visible_intervals"]:
            require(0 <= interval["start_s"] < interval["end_s"] <= end and
                    interval["start_s"] >= previous, "Invalid/unordered area visibility")
            previous = interval["end_s"]

    def scope(ids, available, label):
        require(ids and set(ids) <= set(available), label + ": unknown/out-of-scope area")

    def interval(value, start, finish, label):
        require(start <= value["start_s"] < value["end_s"] <= finish, label + ": invalid interval")

    def visible(aid, timestamp):
        return any(v["start_s"] <= timestamp < v["end_s"]
                   for v in area_map[aid]["visible_intervals"])

    previous = 0
    shot_map = {s["shot"]: s for s in shots}
    for si, shot in enumerate(shots):
        sid = shot["shot"]
        interval(shot, 0, end, sid)
        require(abs(shot["start_s"] - previous) < 1e-6, sid + ": timeline gap/overlap")
        previous = shot["end_s"]
        scope(shot["area_ids"], area_map, sid)
        require(all(any(v["start_s"] < shot["end_s"] and v["end_s"] > shot["start_s"]
                        for v in area_map[aid]["visible_intervals"]) for aid in shot["area_ids"]),
                sid + ": area is not visible in this shot")
        covered = set()
        for design in shot["design"]:
            scope(design["area_ids"], shot["area_ids"], sid + "/design")
            covered.update(design["area_ids"])
        require(covered == set(shot["area_ids"]), sid + ": missing area design")
        route_end = shot["start_s"]
        for route in shot.get("route", []):
            interval(route, shot["start_s"], shot["end_s"], sid + "/route")
            require(route["area_id"] in shot["area_ids"] and route["start_s"] >= route_end,
                    sid + ": invalid route identity/order")
            route_end = route["end_s"]
        for relation in shot.get("area_relations", []):
            scope([relation["from"], relation["to"]], shot["area_ids"], sid + "/area_relations")
        validate_camera_timeline(shot)
        for phase in shot["camera"]["phases"]:
            scope(phase.get("area_ids", shot["area_ids"]), shot["area_ids"], sid + "/phase")
        for key in ("panels", "overviews"):
            values = shot[key]
            require([p["frame_index"] for p in values] == sorted(p["frame_index"] for p in values),
                    sid + ": selections must follow source chronology")
            for p in values:
                scope(p["area_ids"], shot["area_ids"], sid + "/" + key)
                if times is not None:
                    i = p["frame_index"]
                    require(type(i) is int and 0 <= i < len(times) and shot["start_s"] <= times[i] < shot["end_s"],
                            sid + ": selection outside shot")
                    require(all(visible(aid, times[i]) for aid in p["area_ids"]),
                            sid + ": selected area not visible at this frame")
        require(set(aid for p in shot["overviews"] for aid in p["area_ids"]) == set(shot["area_ids"]),
                sid + ": Overview must cover every area")
        validate_production_start(shot, times, path=f"/shots/{si}")
        normal = len(shot["area_ids"]) == 1
        panels = shot["panels"]
        if normal:
            require(len(panels) == 3, sid + ": normal shot requires three panels")
            production_start = shot["composition"].get("production_start")
            if production_start is not None:
                require(panels[0]["frame_index"] == production_start["frame_index"],
                        f"/shots/{si}/panels/0/frame_index: Start must match Production Start")
        if times is not None:
            lo = bisect.bisect_left(times, shot["start_s"])
            hi = bisect.bisect_left(times, shot["end_s"])
            require(lo < hi and abs(times[lo] - shot["start_s"]) < 1e-6, sid + ": cut must use native PTS")
            if not normal:
                require(panels[0]["frame_index"] == lo and panels[-1]["frame_index"] == hi - 1,
                        sid + ": multi-area panels must retain exact native first/last frames")
        seen = set()
        for pointer, fact, ids, category in fact_claims(shot, si):
            scope(ids, shot["design"][int(pointer.split("/")[4])]["area_ids"], pointer)
            key = (tuple(sorted(ids)), fact["subject"], fact["attribute"],
                   repr(fact["value"]), fact["state"])
            require(key not in seen, pointer + ": duplicate fact content")
            seen.add(key)
    for relation in audit.get("relations", []):
        require(relation["from"] in shot_map and relation["to"] in shot_map, "Unknown related shot")
    for pointer, claim, ids, sid, category in claims(audit):
        validate_claim_evidence(claim, ids, shot_map.get(sid), times, visible, pointer, camera=category == "camera")
    from .audit_quality import validate_motion
    validate_motion(audit, times)
    return audit


def from_json(audit, manifest):
    """Small internal envelope; the authored reference is never expanded."""
    return {"id": audit["id"], "revision": audit["revision"], "audit": audit, "manifest": manifest}


def evidence_inventory(model):
    manifest = model["manifest"]
    return {"frames": manifest["frames"], "selections": manifest["selections"],
            "media": manifest["media"]}
