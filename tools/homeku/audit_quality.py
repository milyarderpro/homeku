"""Deterministic source-quality checks; no visual inference or prose synthesis."""
import bisect
import re
import math
from .common import require
from .report_validation import display_audit, CATEGORIES


def resolve(key, audit, times=None):
    selections = {p["id"]: p for s in audit["shots"] for group in ("panels", "overviews") for p in s[group]}
    if key in selections:
        p = selections[key]
        return p["shot_id"], p["frame_index"], p["timestamp_s"]
    m = re.fullmatch(r"frame:(shot-[0-9]{2,}):([0-9]+)", key)
    require(m is not None, f"Unknown evidence: {key}")
    index = int(m[2])
    require(times is None or index < len(times), f"Evidence index outside video: {key}")
    return m[1], index, times[index] if times is not None else None


def validate_quality(audit, times=None):
    display_audit(audit)
    profile = audit["profile"]
    for c in profile:
        if c["aspect"] in {"primary-style", "style-influence", "interior-style"}:
            require(not re.search(r"[;,|\r\n]", c["value"]),
                    f"/profile/{c['id']}: one English style name per claim")
    for aspect, value in [("primary-style", audit["identity"]["primary_style"]),
                          ("interior-style", audit["identity"]["interior_style"])]:
        claims = [c for c in profile if c["aspect"] == aspect]
        require(len(claims) == 1 and claims[0]["value"] == value,
                f"/identity: {aspect} requires one matching profile claim")
    influences = [c["value"] for c in profile if c["aspect"] == "style-influence" and c["state"] in {"observed", "uncertain"}]
    require(len(influences) == len(set(influences)), "/profile: duplicate style influence")
    require(audit["identity"]["influences"] == ("; ".join(influences) if influences else "unknown"),
            "/identity/influences: use ordered individual profile style-influence names or unknown")
    scale = audit["size"]["scale"]
    scales = [c for c in profile if c["aspect"] == "apparent-scale"]
    require(len(scales) == 1 and all(c["value"] == scale for c in scales), "/size/scale: contradictory scale profile")
    if scale == "unknown":
        require(all(c["state"] == "unknown" for c in scales), "/size/scale: unknown requires unknown state")
    for si, shot in enumerate(audit["shots"]):
        path = f"/shots/{si}"
        facts = {f["id"]: f for f in shot["facts"]}
        for di, d in enumerate(shot["design"]):
            for category in CATEGORIES:
                cov = d["fact_coverage"][category]
                label = path + f"/design/{di}/fact_coverage/{category}"
                require(cov["basis"].strip(), label + ": basis required")
                if cov["state"] == "mapped":
                    require(cov["fact_ids"] and set(cov["fact_ids"]) <= set(facts), label + ": missing/unknown fact IDs")
                    selected = [facts[k] for k in cov["fact_ids"]]
                    require(all(set(f["area_ids"]) & set(d["area_ids"]) for f in selected),
                            label + ": fact outside design area")
                    require(set(d["area_ids"]) <= {aid for f in selected for aid in f["area_ids"]},
                            label + ": facts must cover every design area")
                else:
                    require(not cov["fact_ids"], label + ": unresolved coverage cannot claim mapped facts")
        for pi, phase in enumerate(shot["phases"]):
            label = path + f"/phases/{pi}"
            components = phase["components_parsed"]
            observations = phase["motion_observations"]
            require(sorted(o["component_index"] for o in observations) == list(range(len(components))),
                    label + ": exactly one observation per camera component required")
            def phase_proof(keys, moving):
                frames = set()
                inside = False
                for key in keys:
                    sid, index, pts = resolve(key, audit, times)
                    require(sid == shot["shot"], label + ": proof belongs to another shot")
                    frames.add(index)
                    if pts is not None:
                        lo, hi = phase["start_s"], phase["end_s"]
                        if times is None:
                            require(lo <= pts < hi, label + ": proof outside phase")
                        else:
                            first = bisect.bisect_left(times, shot["start_s"])
                            last = bisect.bisect_left(times, shot["end_s"]) - 1
                            left = max(first, bisect.bisect_left(times, lo) - 1)
                            right = min(last, bisect.bisect_left(times, hi))
                            require(left <= index <= right, label + ": proof outside phase boundary tolerance")
                        inside = inside or lo <= pts < hi
                require(not moving or len(frames) >= 2, label + ": movement requires two distinct frames")
                require(not moving or inside or (times is None and any(resolve(k, audit)[2] is None for k in keys)),
                        label + ": movement needs an in-phase frame")
                return frames
            known = any(c["movement"] != "Uncertain" for c in components)
            phase_proof(phase["evidence"], known)
            for obs in observations:
                component = components[obs["component_index"]]
                require(set(obs["evidence"]) <= set(phase["evidence"]), label + ": observation proof must be listed in phase evidence")
                phase_proof(obs["evidence"], component["movement"] != "Uncertain")
                require(obs["basis"].strip(), label + ": motion observation basis required")
                qualifiers = {q.casefold() for q in component["qualifiers"]}
                if "decelerating" in qualifiers:
                    require(phase["speed_change"] in {"decelerating", "variable"},
                            label + ": Decelerating notation conflicts with speed_change")
                if component["estimates"]:
                    require(obs["estimate_basis"] is not None and obs["estimate_basis"].strip(),
                            label + ": numeric camera estimate requires estimate_basis")
                if component["movement"] == "Uncertain" or phase["confidence"] in {"low", "unknown"}:
                    require(obs["alternatives"] is not None and obs["alternatives"].strip(),
                            label + ": ambiguous motion requires alternatives")
            labels = {t["tempo"] for t in shot["tempo_profile"] if
                      t["start_s"] < phase["end_s"] and t["end_s"] > phase["start_s"]}
            expected = next(iter(labels)) if len(labels) == 1 else "variable"
            require(phase["tempo"] == expected,
                    label + ": tempo conflicts with overlapping tempo_profile")
    if audit["schema_version"] in {"2.3", "2.4"}:
        validate_method(audit, times)
    return audit


def validate_viewed_evidence(audit, reviews, times):
    viewed = {(r["shot_id"], index) for r in reviews for index in r["viewed_frame_indices"]}
    keys = {p["id"] for s in audit["shots"] for group in ("panels", "overviews") for p in s[group]}
    claims = list(audit["profile"]) + list(audit["relations"]) + list(audit["identity"]["style_relations"])
    for s in audit["shots"]:
        claims += s["facts"] + s["phases"] + s["area_relations"]
        claims += [o for p in s["phases"] for o in p["motion_observations"]]
    if audit["schema_version"] in {"2.3", "2.4"}:
        for s in audit["shots"]:
            for p in s["phases"]:
                claims += list(p["camera_checks"].values())
                for o in p["motion_observations"]:
                    if o["scale_measurement"]:
                        m = o["scale_measurement"]
                        keys |= {m["start_evidence"], m["end_evidence"]}
    keys |= {k for c in claims for k in c["evidence"]}
    for key in keys:
        sid, index, _ = resolve(key, audit, times)
        require((sid, index) in viewed, f"Evidence {key}: frame not declared viewed; finish inspection before review")


def validate_method(audit, times=None):
    """2.3 declarations are internally checkable; image semantics remain visual."""
    for shot in audit["shots"]:
        for phase in shot["phases"]:
            label = shot["shot"] + "/" + phase["phase"]
            def proof(keys):
                require(set(keys) <= set(phase["evidence"]), label + ": checks/measurement evidence must be listed in phase")
                rows = [resolve(k, audit, times) for k in keys]
                require(all(sid == shot["shot"] for sid, _, _ in rows), label + ": check outside shot")
                require(len({i for _, i, _ in rows}) >= 2, label + ": checks need two distinct frames")
                inside = False
                for _, index, pts in rows:
                    if times is not None:
                        lo = max(bisect.bisect_left(times, shot["start_s"]),
                                 bisect.bisect_left(times, phase["start_s"]) - 1)
                        hi = min(bisect.bisect_left(times, shot["end_s"]) - 1,
                                 bisect.bisect_left(times, phase["end_s"]))
                        require(lo <= index <= hi, label + ": check outside phase boundary tolerance")
                    if pts is not None:
                        inside |= phase["start_s"] <= pts < phase["end_s"]
                        if times is None:
                            require(phase["start_s"] <= pts < phase["end_s"], label + ": check outside phase")
                require(inside or (times is None and any(t is None for _, _, t in rows)),
                        label + ": check needs an in-phase frame")
                return rows
            for check in phase["camera_checks"].values():
                require(check["basis"].strip(), label + ": camera check basis required")
                proof(check["evidence"])
            scales = []
            for obs in phase["motion_observations"]:
                c = phase["components_parsed"][obs["component_index"]]
                movement = c["movement"]
                expected = movement.startswith(("Dolly-", "Zoom-", "Pan ", "Orbit "))
                if expected:
                    require(obs["estimate_basis"] is not None and obs["estimate_basis"].strip(),
                            label + ": estimate_basis required for angle/scale or a specific limitation")
                ratios = [e for e in c["estimates"] if e.endswith("×")]
                angles = [e for e in c["estimates"] if e.endswith("°")]
                require(not angles or movement.startswith(("Pan ", "Orbit ", "Tilt ")),
                        label + ": angle estimate is not applicable to this component")
                if audit["schema_version"] == "2.4":
                    required_unit = "°" if movement.startswith(("Pan ", "Orbit ")) else "×" if movement.startswith(("Dolly-", "Zoom-")) else None
                    if required_unit and phase["confidence"] in {"high", "medium"}:
                        require(any(e.endswith(required_unit) for e in c["estimates"]),
                                label + ": clear camera movement requires a visual ~" + required_unit + " estimate; calibration is not required")
                    for estimate in c["estimates"]:
                        require(re.search(r"\([^)]*" + re.escape(estimate) + r"[^)]*\)", c["raw"]) is not None,
                                label + ": write numeric camera estimates inside parentheses")
                if audit["schema_version"] == "2.4":
                    for value in ratios:
                        match=re.fullmatch(r"~([0-9]+(?:\.[0-9])?)(?:[–−-]([0-9]+(?:\.[0-9])?))?×",value)
                        require(match is not None and 1<=float(match[1])<=float(match[2] or match[1]),
                                label + ": visual scale uses a positive ordered IN/OUT magnitude, at most one decimal")
                    for value in angles:
                        match=re.fullmatch(r"~([0-9]+(?:\.[0-9]+)?)(?:°?[–−-]([0-9]+(?:\.[0-9]+)?))?°",value)
                        require(match is not None and 0<float(match[1])<=float(match[2] or match[1]),
                                label + ": visual angle uses a positive ordered estimate/range")
                measure = obs["scale_measurement"]
                if not ratios:
                    require(measure is None, label + ": scale_measurement needs a stated scale estimate")
                    continue
                require(len(ratios) == 1 and movement in {"Dolly-In", "Dolly-Out", "Zoom-In", "Zoom-Out"},
                        label + ": scale estimate requires an IN/OUT Dolly or Zoom component")
                if measure is None and audit["schema_version"] == "2.4":
                    continue
                require(measure is not None, label + ": numeric scale requires scale_measurement")
                require(measure["anchor"].strip(), label + ": scale anchor required")
                keys = [measure["start_evidence"], measure["end_evidence"]]
                require(set(keys) <= set(obs["evidence"]), label + ": measurement evidence outside observation")
                rows = proof(keys)
                require(rows[0][1] < rows[1][1], label + ": measurement frames must be chronological and distinct")
                start, end = measure["start_px"], measure["end_px"]
                require(all(math.isfinite(v) and v > 0 for v in (start, end)), label + ": pixel sizes must be finite and positive")
                ratio = end / start if movement.endswith("In") else start / end
                require(ratio > 1, label + ": IN/OUT scale ratio must exceed one")
                match = re.fullmatch(r"~([0-9]+(?:\.[0-9])?)(?:[–−-]([0-9]+(?:\.[0-9])?))?×", ratios[0])
                require(match is not None, label + ": scale notation uses one decimal or an ordered range")
                lower = float(match[1]); upper = float(match[2] or match[1])
                require(1 <= lower <= upper and lower-.050000001 <= ratio <= upper+.050000001,
                        label + ": scale notation conflicts with measured IN/OUT ratio")
                scales.append((movement, measure))
            # Same total scale must not be attributed twice to an inseparable Dolly+Zoom.
            for m1, x in scales:
                for m2, y in scales:
                    if m1.startswith("Dolly") and m2.startswith("Zoom"):
                        require(x != y, label + ": Dolly+Zoom cannot share the total scale measurement")
            ranks = {"slow": 0, "moderate": 1, "fast": 2}
            seq = [t["tempo"] for t in shot["tempo_profile"]
                   if t["start_s"] < phase["end_s"] and t["end_s"] > phase["start_s"]]
            values = [ranks[t] for t in seq if t in ranks]
            if len(values) > 1 and len(values) == len(seq):
                if phase["speed_change"] == "accelerating":
                    require(all(a <= b for a, b in zip(values, values[1:])),
                            label + ": accelerating conflicts with decreasing tempo_profile")
                if phase["speed_change"] == "decelerating":
                    require(all(a >= b for a, b in zip(values, values[1:])),
                            label + ": decelerating conflicts with increasing tempo_profile")
