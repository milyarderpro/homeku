"""Versioned source models. V2 semantics are authored JSON, never extracted prose."""
from __future__ import annotations
import bisect
import copy
import re
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker
from .common import LibraryError, read_json, require

ROOT = Path(__file__).resolve().parents[2]


def schema_check(value, name):
    validator = Draft202012Validator(read_json(ROOT / "docs/contracts" / name), format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(value), key=lambda e: str(list(e.path)))
    if errors:
        e = errors[0]
        raise LibraryError(f"{name}/{'/'.join(map(str, e.path))}: {e.message}")


def normalized(value):
    return re.sub(r"\s+", " ", value).strip().rstrip(".")


def selections(audit):
    return [p for s in audit["shots"] for key in ("panels", "overviews") for p in s[key]]


def validate_audit(audit, duration=None, times=None):
    schema_check(audit, "audit-v2.schema.json")
    def filled(value):
        if isinstance(value,str):return "{{" not in value and "}}" not in value
        if isinstance(value,dict):return all(filled(v) for v in value.values())
        if isinstance(value,list):return all(filled(v) for v in value)
        return True
    require(filled(audit), "Unfilled template placeholders")
    area_ids = [a["id"] for a in audit["areas"]]
    require(len(area_ids) == len(set(area_ids)), "Duplicate area ID")
    areas = {a["id"]: a for a in audit["areas"]}
    shots = audit["shots"]
    require([s["shot"] for s in shots] == [f"shot-{i:02d}" for i in range(1, len(shots)+1)], "Shot IDs must be sequential")
    end = shots[-1]["end_s"]
    require(abs(shots[0]["start_s"]) < 1e-6, "Timeline must start at zero")
    if duration is not None:
        require(abs(end-duration) < 1e-6, "Timeline must cover source duration")
    for a in areas.values():
        prior = -1
        for interval in a["visible_intervals"]:
            lo, hi = interval["start_s"], interval["end_s"]
            require(0 <= lo < hi <= end and lo >= prior, "Invalid/unordered area visibility intervals")
            prior = hi
        require(len(a["functions"]) == len(set(a["functions"])), "Duplicate area function")
    floor = audit["size"]["floor_area_m2"]
    require(floor["min"] < floor["max"], "Floor area requires a positive ordered range")
    chosen = selections(audit)
    ids = [p["id"] for p in chosen]
    require(len(ids) == len(set(ids)), "Duplicate panel/overview selection ID")
    choice = {p["id"]: p for p in chosen}
    shot_map = {s["shot"]: s for s in shots}

    def scope(values, allowed, label, nonempty=False):
        require((not nonempty or values) and len(values) == len(set(values)) and set(values) <= set(allowed), f"Invalid {label} scope")

    def evidence(claim, sid=None):
        require(claim["evidence"] or claim.get("state") == "unknown", "Claim requires evidence unless unknown")
        covered_areas=set(); unresolved_native=False
        for key in claim["evidence"]:
            if key in choice:
                p = choice[key]
                require(sid is None or p["shot_id"] == sid, "Evidence must belong to this shot")
                covered_areas.update(p["area_ids"])
            else:
                m = re.fullmatch(r"frame:(shot-[0-9]{2,}):([0-9]+)", key)
                require(m is not None and m[1] in shot_map and (sid is None or m[1] == sid), "Unknown evidence ID")
                if times is not None:
                    i = int(m[2]); s = shot_map[m[1]]
                    require(i < len(times) and s["start_s"] <= times[i] < s["end_s"], "Evidence frame outside shot")
                    covered_areas.update(a["id"] for a in areas.values() if a["id"] in s["area_ids"] and any(v["start_s"]<=times[i]<v["end_s"] for v in a["visible_intervals"]))
                else:
                    unresolved_native=True
        if not unresolved_native and claim.get("state")!="unknown":
            require(set(claim.get("area_ids",[]))<=covered_areas,"Evidence does not cover claim area scope")

    cursor = 0
    for s in shots:
        sid, lo, hi = s["shot"], s["start_s"], s["end_s"]
        require(abs(cursor-lo) < 1e-6 and lo < hi, "Timeline gap/overlap")
        cursor = hi
        scope(s["area_ids"], areas, "shot area", True)
        for aid in s["area_ids"]:
            require(any(v["start_s"] < hi and v["end_s"] > lo for v in areas[aid]["visible_intervals"]), "Shot area is not visible in shot")
        for group in ("panels", "overviews"):
            ps = s[group]
            require([p["timestamp_s"] for p in ps] == sorted(p["timestamp_s"] for p in ps), "Panels must be chronological")
            for p in ps:
                require(p["shot_id"] == sid and lo <= p["timestamp_s"] < hi, "Panel outside shot")
                scope(p["area_ids"], s["area_ids"], "panel area", True)
                for aid in p["area_ids"]:
                    require(any(v["start_s"] <= p["timestamp_s"] < v["end_s"] for v in areas[aid]["visible_intervals"]), "Panel area not visible at selection time")
                if times is not None:
                    require(p["frame_index"] < len(times) and abs(times[p["frame_index"]]-p["timestamp_s"]) < 1e-6, "Panel frame index/PTS mismatch")
        ps = s["panels"]
        if len(s["area_ids"]) == 1:
            require(len(ps) == 3 and [p["role"] for p in ps] == ["start", "middle", "end"], "Normal shot requires exactly three start/middle/end panels")
        else:
            require(len({p["frame_index"] for p in ps})==len(ps), "Multi area collage must not repeat the same frame")
            require(ps[0]["role"] == "start" and ps[-1]["role"] == "end" and s["journey_dna"], "Multi area requires start/end and journey DNA")
        if times is not None:
            first, last = bisect.bisect_left(times, lo), bisect.bisect_left(times, hi)-1
            require(first<len(times) and abs(times[first]-lo)<1e-6,"Shot boundary must use native PTS")
            require(ps[0]["frame_index"] == first and ps[-1]["frame_index"] == last, "Start/end must be exact native shot boundaries")
            if len(s["area_ids"]) == 1:
                from .video import nearest
                require(ps[1]["frame_index"] == nearest(times, (lo+hi)/2, lo, hi), "Middle panel must be nearest native midpoint")
        require(set(s["area_ids"]) <= {a for p in s["overviews"] for a in p["area_ids"]}, "Storyboard must cover every shot area")
        scope([a for d in s["design"] for a in d["area_ids"]], s["area_ids"], "design area", True)
        require(set(s["area_ids"]) == {a for d in s["design"] for a in d["area_ids"]}, "Every shot area requires design narratives")
        previous = lo
        for r in s["route"]:
            require(r["area_id"] in s["area_ids"] and lo <= r["start_s"] < r["end_s"] <= hi and r["start_s"] >= previous, "Route traversal must be ordered, scoped and nonoverlapping")
            require(any(v["start_s"] <= r["start_s"] and v["end_s"] >= r["end_s"] for v in areas[r["area_id"]]["visible_intervals"]), "Route outside area visibility")
            previous = r["end_s"]
        for group in (s["phases"], s["tempo_profile"]):
            previous = lo
            for p in group:
                require(abs(p["start_s"]-previous)<1e-6 and previous < p["end_s"] <= hi, "Phase/tempo intervals must cover shot without gaps/overlaps")
                previous = p["end_s"]
            require(abs(previous-hi)<1e-6, "Phase/tempo intervals do not cover shot")
        require(normalized(s["camera_summary"]) == normalized(" → ".join(p["components"] for p in s["phases"])), "Camera summary differs from ordered phase components")
        require([p["phase"] for p in s["phases"]]==[f"phase-{i:02d}" for i in range(1,len(s["phases"])+1)],"Phase IDs must be sequential")
        for p in s["phases"]:
            scope(p["area_ids"], s["area_ids"], "phase area", True)
            from .markdown import component
            for c in p["components_parsed"]:
                require(c==component(c["raw"]), "Parsed component metadata differs from raw notation")
                if "accelerating" in {q.casefold() for q in c["qualifiers"]}:
                    require(p["speed_change"] in {"accelerating","variable"}, "Accelerating notation conflicts with speed_change")
            require(normalized(p["components"]) == normalized(" + ".join(c["raw"] for c in p["components_parsed"])), "Parsed components differ from technical notation")
            evidence(p, sid)
        for f in s["facts"]:
            scope(f["area_ids"], s["area_ids"], "fact area", True)
            evidence(f, sid)
        require(len({f["id"] for f in s["facts"]}) == len(s["facts"]), "Duplicate fact ID")
        for r in s["area_relations"]:
            require(r["from"] in s["area_ids"] and r["to"] in s["area_ids"], "Unknown related area")
            evidence(r, sid)
    require(len({c["id"] for c in audit["profile"]}) == len(audit["profile"]), "Duplicate DNA claim ID")
    from .markdown import PROFILE_ASPECTS
    require(set(PROFILE_ASPECTS)<={c["aspect"] for c in audit["profile"]},"DNA profile must cover all legacy aspects explicitly; use unknown when needed")
    for c in audit["profile"]:
        scope(c["area_ids"], areas, "profile area")
        evidence(c)
    for r in audit["relations"]:
        require(r["from"] in shot_map and r["to"] in shot_map, "Unknown related shot")
        evidence(r)
    for r in audit["identity"]["style_relations"]:
        evidence(r)
    require(any(c["aspect"] == "primary-style" and c["value"] == audit["identity"]["primary_style"] for c in audit["profile"]), "Primary style must match explicit DNA claim")
    require(any(c["aspect"] == "apparent-scale" and c["value"] == audit["size"]["scale"] for c in audit["profile"]), "Scale must match explicit DNA claim")
    return audit


def v2_model(audit, manifest, digest, times=None):
    """Add operational fields without changing any authored value or label."""
    m = copy.deepcopy(audit)
    m.update(format_version="2.0", title=audit["identity"]["name"], source=manifest["source"],
             media=manifest["media"], audit=manifest["audit"], render=manifest["render"], content_sha256=digest)
    labels = {a["id"]: a["label"] for a in m["areas"]}
    for s in m["shots"]:
        s["areas"] = [labels[a] for a in s["area_ids"]]
    if times is not None:
        claims=list(audit["profile"])+list(audit["relations"])+list(audit["identity"]["style_relations"])
        for shot in audit["shots"]:claims+=shot["facts"]+shot["phases"]+shot["area_relations"]
        keys={key for claim in claims for key in claim["evidence"] if key.startswith("frame:")}
        m["native_evidence"]={key:times[int(key.rsplit(":",1)[1])] for key in sorted(keys)}
    return m


def legacy_model(model):
    """Explicit adapter: no new style, area identities or floor estimates inferred."""
    require(model["format_version"] in {"1.0", "1.1"}, "Unsupported legacy model")
    return model


def evidence_inventory(model):
    """Each proof is stored once. Claims retain stable IDs, including native-only frames."""
    if model["format_version"] != "2.0":
        return {m["path"]:dict(m) for m in model["media"]}
    result={}
    for m in model["media"]:
        for p in m["panels"]:
            result[p["id"]]={"path":m["path"],**p}
    claims=list(model["profile"])+list(model["relations"])+list(model["identity"]["style_relations"])
    for s in model["shots"]:claims+=s["facts"]+s["phases"]+s["area_relations"]
    native=[]
    for c in claims:
        for key in c["evidence"]:
            if key not in result:native.append(key)
    if native:
        for key in set(native):
            _,sid,index=key.split(":");index=int(index)
            timestamp=model.get("native_evidence",{}).get(key)
            require(timestamp is not None,"Native evidence timestamp missing")
            result[key]={"path":model["source"]["path"],"shot_id":sid,"frame_index":index,"timestamp_s":timestamp,
                         "area_ids":[a["id"] for a in model["areas"] if any(v["start_s"]<=timestamp<v["end_s"] for v in a["visible_intervals"])]}
    return result
