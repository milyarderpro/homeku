"""Pure, source-backed derived views. Never expands or rewrites audit.json."""
from .common import LibraryError, require
from .camera_notation import parse
from .camera_pattern import shot_pattern

CATEGORIES = ("architecture", "furnishings", "environment")
SIZE_ASPECTS = {"scale": "apparent-scale", "levels": "levels-visible",
                "footprint": "footprint", "proportions": "proportions"}


def resolve(value, pointer):
    require(isinstance(pointer, str) and (pointer == "" or pointer.startswith("/")),
            "Invalid source JSON pointer")
    try:
        for raw in pointer.split("/")[1:] if pointer else []:
            key = raw.replace("~1", "/").replace("~0", "~")
            if isinstance(value, list):
                require(key.isdecimal(), "Invalid source array pointer")
                value = value[int(key)]
            else:
                value = value[key]
        return value
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        raise LibraryError("Unresolved source pointer: " + pointer) from exc


def profile_claims(audit):
    """Yield (pointer, claim, explicit aspect), without creating a second profile."""
    yield "/design/styles/primary", audit["design"]["styles"]["primary"], "primary-style"
    for group, aspect in (("influences", "style-influence"), ("interior", "interior-style")):
        for i, claim in enumerate(audit["design"]["styles"][group]):
            yield f"/design/styles/{group}/{i}", claim, aspect
    for key, aspect in SIZE_ASPECTS.items():
        yield f"/design/size/{key}", audit["design"]["size"][key], aspect
    for i, claim in enumerate(audit["design"]["features"]):
        yield f"/design/features/{i}", claim, claim["aspect"]


def fact_claims(shot, shot_index):
    for di, design in enumerate(shot["design"]):
        for category in CATEGORIES:
            for fi, claim in enumerate(design[category]["facts"]):
                pointer = f"/shots/{shot_index}/design/{di}/{category}/facts/{fi}"
                yield pointer, claim, claim.get("area_ids", design["area_ids"]), category


def claims(audit):
    for pointer, claim, aspect in profile_claims(audit):
        yield pointer, claim, [], None, aspect
    for i, relation in enumerate(audit["design"]["styles"].get("relations", [])):
        yield f"/design/styles/relations/{i}", relation, [], None, "style-relation"
    for si, shot in enumerate(audit["shots"]):
        for pointer, claim, areas, category in fact_claims(shot, si):
            yield pointer, claim, areas, shot["shot"], category
        for pi, phase in enumerate(shot["camera"]["phases"]):
            yield (f"/shots/{si}/camera/phases/{pi}", phase,
                   phase.get("area_ids", shot["area_ids"]), shot["shot"], "camera")
        for ri, relation in enumerate(shot.get("area_relations", [])):
            yield (f"/shots/{si}/area_relations/{ri}", relation,
                   [relation["from"], relation["to"]], shot["shot"], "area-relation")
    for i, relation in enumerate(audit.get("relations", [])):
        yield f"/relations/{i}", relation, [], None, "shot-relation"


def camera_summary(shot):
    return " → ".join(p["notation"].strip().rstrip(".") for p in shot["camera"]["phases"]) + "."


def tempo_segments(shot):
    tempo = shot["camera"]["tempo"]
    if "segments" in tempo:
        return [dict(value) for value in tempo["segments"]]
    return [{"start_s": shot["start_s"], "end_s": shot["end_s"],
             "label": tempo["label"], "description": tempo["description"]}]


def phase_tempo(shot, phase):
    labels = {t["label"] for t in tempo_segments(shot)
              if t["start_s"] < phase["end_s"] and t["end_s"] > phase["start_s"]}
    known = labels - {"unknown"}
    if len(known) > 1:
        return "variable"
    if "unknown" in labels or not labels:
        return "unknown"
    return next(iter(known))


def phase_tempo_text(shot, phase):
    return "; ".join(t["description"] for t in tempo_segments(shot)
                     if t["start_s"] < phase["end_s"] and t["end_s"] > phase["start_s"])


def selection_id(shot_id, group, index):
    return f"s{shot_id[5:]}-{'panel' if group == 'panels' else 'overview'}-{index + 1:02d}"


def selections(audit, frames):
    """frames is native PTS sequence or manifest frame map; no source decode."""
    for si, shot in enumerate(audit["shots"]):
        for group in ("panels", "overviews"):
            values = shot[group]
            for i, value in enumerate(values):
                index = value["frame_index"]
                require(type(index) is int and index >= 0, "Select a native frame index")
                try:
                    timestamp = frames[str(index)] if isinstance(frames, dict) else frames[index]
                except (KeyError, IndexError, TypeError) as exc:
                    raise LibraryError(f"Missing native PTS for selection frame {index}") from exc
                role = ("overview" if group == "overviews" else "start" if i == 0 else
                        "end" if i == len(values) - 1 else
                        "middle" if len(shot["area_ids"]) == 1 else "moment")
                label = {"start": "Start", "middle": "Middle", "end": "End",
                         "overview": "Overview"}.get(role, value.get("label", f"Moment {i + 1}"))
                yield {"id": selection_id(shot["shot"], group, i),
                       "source_pointer": f"/shots/{si}/{group}/{i}", "shot_id": shot["shot"],
                       "area_ids": list(value["area_ids"]), "frame_index": index,
                       "timestamp_s": timestamp, "role": role, "label": label}


def referenced_frames(audit):
    indices = set()
    for _, claim, _, _, _ in claims(audit):
        indices.update(claim.get("evidence", []))
        for override in claim.get("overrides", []):
            indices.update(override.get("evidence", []))
    for shot in audit["shots"]:
        for group in ("panels", "overviews"):
            indices.update(p["frame_index"] for p in shot[group])
    require(all(type(i) is int and i >= 0 for i in indices), "Invalid referenced frame index")
    return sorted(indices)


def frame_map(audit, times):
    result = {}
    for index in referenced_frames(audit):
        require(index < len(times), f"Evidence frame {index} outside source")
        result[str(index)] = times[index]
    return result


def derived_shot(shot, index):
    """Only useful derived values and their explicit source inputs."""
    return {"camera_summary": camera_summary(shot),
            "camera_pattern": shot_pattern(shot),
            "components": [parse(p["notation"]) for p in shot["camera"]["phases"]],
            "phase_tempos": [phase_tempo(shot, p) for p in shot["camera"]["phases"]],
            "inputs": [f"/shots/{index}/camera/phases", f"/shots/{index}/camera/tempo"]}


def shared_scope(shot, value):
    return value.get("area_ids", shot["area_ids"])
