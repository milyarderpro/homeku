"""Bounded discovery and selective reads of registered reference sources."""
from __future__ import annotations
import copy
from . import FORMAT_VERSION
from .common import read_json, require, sha256
from .derivations import claims
from .generation import aliases, canonical, generator_fingerprint
from .models import schema_check

POSITIVE = {"observed", "uncertain"}
CONFIGURATION_ROLES = {"configuration", "layout"}


def _registry(root):
    from .engine import registry_at
    return registry_at(root)["references"]


def _generated(root, path):
    build = read_json(root / "data/build.json")
    require(isinstance(build, dict) and isinstance(build.get("outputs"), dict),
            "Invalid build metadata; run library.py build")
    require(build.get("generator_fingerprint") == generator_fingerprint(root),
            "Generated data stale; run library.py build")
    expected = build["outputs"].get(path)
    file = root / path
    require(expected is not None and file.is_file() and not file.is_symlink() and sha256(file) == expected,
            "Generated data changed; run library.py build")
    return read_json(file)


def search(root, *, style=None, style_role="primary-style", style_relation=None, house_type=None, scale=None, area=None,
           configuration=None, tempo=None, movement=None, camera_qualifier=None, route=None,
           limit=10, offset=0, include_uncertain=True):
    require(type(limit) is int and 1 <= limit <= 50 and type(offset) is int and offset >= 0,
            "Search limit must be 1–50 and offset nonnegative")
    registry = _registry(root)
    index = _generated(root, "data/search-index.json")
    require(index.get("schema_version") == FORMAT_VERSION, "Unsupported search index; run library.py build")
    require(len(index["references"]) == len(registry) and {r["id"] for r in index["references"]} == set(registry),
            "Registry/index differ; run library.py build")
    groups = aliases(read_json(root / "data/taxonomy.json"))
    allowed = POSITIVE if include_uncertain else {"observed"}

    def normalized(group, value):
        return canonical(groups, group, value).casefold()

    areas = {normalized("areas", value) for value in (area or [])}
    wanted_route = [normalized("areas", value) for value in (route or [])]
    term = normalized("movements", movement) if movement else None

    def facet(reference, aspect, value, group):
        wanted = normalized(group, value)
        return any(row["aspect"] == aspect and row["state"] in allowed
                   and isinstance(row["canonical"], str) and row["canonical"].casefold() == wanted
                   for row in reference["profile_facets"])

    results = []
    total = 0
    for reference in index["references"]:
        require(registry[reference["id"]]["revision"] == reference["revision"], "Stale revision in index")
        if style:
            direct = facet(reference, style_role, style, "styles")
            related = style_relation and any(
                row["relation"] == style_relation and row["state"] in allowed
                and normalized("styles", row["to"]) == normalized("styles", style)
                and facet(reference, "primary-style", row["from"], "styles")
                for row in reference["style_relations"])
            if not direct and not related:
                continue
        if house_type and not facet(reference, "house-type", house_type, "house_types"):
            continue
        if scale and not facet(reference, "apparent-scale", scale, "scales"):
            continue
        hits = []
        for shot in reference["shots"]:
            indexed_areas = {value.casefold() for value in shot["areas_canonical"]}
            if not areas <= indexed_areas:
                continue
            if tempo and tempo not in shot["tempos"]:
                continue
            if term and term not in {v.casefold() for v in shot["movements"]}:
                continue
            if camera_qualifier and camera_qualifier.casefold() not in {
                    qualifier.casefold() for qualifier in shot["camera_qualifiers"]}:
                continue
            matching_ids = {aid for aid, labels in shot["area_labels_by_id"].items()
                            if not areas or areas.intersection(v.casefold() for v in labels)}
            if configuration and not any(
                    f["state"] in allowed and bool(CONFIGURATION_ROLES.intersection(f["facet_roles"]))
                    and bool(matching_ids.intersection(f["area_ids"]))
                    and isinstance(f["value"], str) and f["value"].casefold() == configuration.casefold()
                    for f in shot["design_facets"]):
                continue
            if wanted_route:
                actual = [normalized("areas", value) for value in shot["route"]]
                if not shot["multi_area"] or not any(
                        actual[i:i + len(wanted_route)] == wanted_route
                        for i in range(len(actual) - len(wanted_route) + 1)):
                    continue
            hits.append(shot)
        if hits:
            if offset <= total < offset + limit:
                result = {k: reference[k] for k in ("id", "title", "revision", "json", "profile_facets", "floor_area_m2")}
                results.append({**result, "shots": hits})
            total += 1
    return {"schema_version": FORMAT_VERSION, "total": total, "offset": offset, "limit": limit,
            "results": results, "next_offset": offset + limit if offset + limit < total else None}


def load_reader(root, rid):
    registry = _registry(root)
    require(rid in registry, "Reference is not active in registry")
    entry = registry[rid]
    payload = _generated(root, f"data/projections/{rid}.json")
    schema_check(payload, "reference-reader.schema.json")
    audit = payload["reference"]
    require(payload["content_sha256"] == entry["content_sha256"] and audit["id"] == rid
            and audit["revision"] == entry["revision"], "Projection differs from registered revision")
    folder = root / "references" / rid
    require(folder.is_dir() and not folder.is_symlink(), "Registered reference folder unavailable")
    for name, key in (("audit.json", "audit_sha256"), ("manifest.json", "manifest_sha256")):
        path = folder / name
        require(path.is_file() and not path.is_symlink() and sha256(path) == entry[key],
                f"Registered {name} changed outside ZIP revision")
    require(payload["source"]["sha256"] == entry["source_sha256"]
            and payload["source"]["path"] == f"video/{rid}.mp4", "Projection source differs from registry")
    return payload


def _evidence(payload, indices, selected=()):
    inventory = payload["evidence_inventory"]
    identifiers = {p["id"] for p in selected}
    locations = [{"path": row["path"], "kind": row["kind"], **panel}
                 for row in inventory["media"] for panel in row["panels"]
                 if panel["selection_id"] in identifiers]
    return {"frames": {str(i): inventory["frames"][str(i)] for i in sorted(indices)},
            "selections": list(selected), "locations": locations}


def read_reference(root, rid, *, part="identity", shot=None, area=None):
    payload = load_reader(root, rid)
    audit = payload["reference"]
    if part == "full":
        return payload
    context = {"id": rid, "revision": audit["revision"], "schema_version": FORMAT_VERSION,
               "paths": payload["paths"]}
    if part == "identity":
        keys = {i for _, claim, _, sid, kind in claims(audit) if sid is None and kind != "shot-relation"
                for i in claim["evidence"]}
        return {**context, "design": audit["design"], "camera_pattern": payload["derived"]["camera_pattern"],
                "evidence": _evidence(payload, keys),
                "provenance": {k: v for k, v in payload["provenance"].items()
                               if k.startswith("/reference/design") or k == "/derived/camera_pattern"}}
    require(part in {"shot", "area"} and shot, "Choose a shot ID for shot/area reads")
    index = next((i for i, row in enumerate(audit["shots"]) if row["shot"] == shot), None)
    require(index is not None, "Unknown shot")
    found = audit["shots"][index]
    selected = copy.deepcopy(found)
    if part == "area":
        require(area in found["area_ids"], "Area reads require a physical area ID visible in this shot")
        selected["design"] = [block for block in selected["design"] if area in block["area_ids"]]
        for block in selected["design"]:
            for group in ("architecture", "furnishings", "environment"):
                block[group]["facts"] = [claim for claim in block[group]["facts"]
                                         if area in claim.get("area_ids", block["area_ids"])]
        context["area_id"] = area
    areas = [a for a in audit["areas"] if a["id"] in found["area_ids"]]
    selected_frames = [p for p in payload["evidence_inventory"]["selections"] if p["shot_id"] == shot]
    indices = {p["frame_index"] for p in selected_frames}
    production_start = found["composition"].get("production_start")
    if production_start is not None:
        indices.add(production_start["frame_index"])
    omitted = set()
    for pointer, claim, scope, sid, category in claims(audit):
        if sid != shot:
            continue
        if part == "area" and category in {"architecture", "furnishings", "environment"} and area not in scope:
            omitted.add(pointer)
            continue
        indices.update(claim["evidence"])
        for override in claim.get("overrides", []):
            indices.update(override.get("evidence", []))
    prefix = f"/reference/shots/{index}"
    provenance = {key: result for key, result in payload["provenance"].items()
                  if (key == prefix or key.startswith(prefix + "/") or key == f"/derived/shots/{index}")
                  and not any(key == "/reference" + p or key.startswith("/reference" + p + "/") for p in omitted)}
    return {**context, "shot": selected, "areas": areas, "derived": payload["derived"]["shots"][index],
            "evidence": _evidence(payload, indices, selected_frames), "provenance": provenance}


def _media_output(root, output):
    from .audit_performance import safe_path
    output = safe_path(output)
    require(not output.resolve().is_relative_to(root.resolve()),
            "Use a temporary output outside the repository")
    return output


def extract_panel(root, rid, panel, output, *, native=False):
    import io
    import re
    from PIL import Image
    from .media import crop_panel
    from .video import extract_frame
    payload = load_reader(root, rid)
    output = _media_output(root, output)
    evidence = payload["evidence_inventory"]
    item = next((p for p in evidence["selections"] if p["id"] == panel), None)
    if not native:
        require(item is not None, "Use a stored selection ID, or --native for evidence such as F2")
        return crop_panel(root / "references" / rid, evidence, panel, output)
    source_info = payload["source"]
    source = root / source_info["path"]
    require(source.is_file() and not source.is_symlink(),
            f"--native requires canonical MP4: {source_info['path']}")
    require(sha256(source) == source_info["sha256"], "Canonical source changed")
    if item is not None:
        index, time = item["frame_index"], item["timestamp_s"]
    else:
        match = re.fullmatch(r"F(0|[1-9][0-9]*)", panel)
        require(match is not None and match[1] in evidence["frames"], "Unknown referenced native frame")
        index, time = int(match[1]), evidence["frames"][match[1]]
    content = extract_frame(source, index, source_info["video_stream_index"])
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.suffix.casefold() == ".png":
        with Image.open(io.BytesIO(content)) as picture:
            picture.save(output, "PNG")
    else:
        output.write_bytes(content)
    return {"output": str(output), "frame_index": index, "timestamp_s": time}


def extract_shot_image(root, rid, shot, output, *, from_storyboard=False):
    import shutil
    from .media import crop_storyboard, verify_stored_media
    payload = load_reader(root, rid)
    output = _media_output(root, output)
    require(any(s["shot"] == shot for s in payload["reference"]["shots"]), "Unknown shot")
    evidence = payload["evidence_inventory"]
    folder = root / "references" / rid
    if from_storyboard:
        return crop_storyboard(folder, evidence, shot, output)
    item = next((row for row in evidence["media"] if row["path"] == f"media/{shot}.jpg"), None)
    require(item is not None, "No stored shot collage")
    photo = verify_stored_media(folder, item["path"], item["sha256"])
    output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(photo, output)
    return {"output": str(output), "width": item["width"], "height": item["height"],
            "source": item["path"]}
