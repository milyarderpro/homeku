"""Build/check source-bound stage 3–5 knowledge, never production instructions."""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import date
import hashlib
import json
from pathlib import Path
import re

from knowledge_library import (ROOT, dump, load_release, md, read_archives,
                               resolve_pointer, validate_contract)
from verify_source_integrity import sha256_file

RELATIONS = (
    ("in_front_of", "in_front_of"), ("to_left_of", "left_of"),
    ("to_right_of", "right_of"), ("left_of", "left_of"), ("right_of", "right_of"),
    ("next_to", "beside"), ("visible_through", "visible_through"),
    ("centered_on", "centered_on"), ("facing", "facing"), ("behind", "behind"),
    ("above", "above"), ("below", "below"), ("beneath", "below"),
    ("under", "below"), ("between", "between"), ("beside", "beside"),
    ("flanking", "flanking"),
)
UNCERTAIN = re.compile(r"(?:^|_)(?:or|possibly|possible|unidentified|uncertain|no|not|without)(?:_|$)")
COMMON_LIMITS = [
    "Image-relative appearance, not measured geometry or a reconstructed floorplan.",
    "Recorded annotations and AI visual review have separate evidence bases.",
    "Material names describe appearance; composition, dimensions and structural feasibility remain unknown.",
]


def stable_id(ident, scope, value):
    return ident + "." + scope + "." + hashlib.sha256(value.encode()).hexdigest()[:16]


def relation_from_tag(raw):
    """Literal one-edge parse; retain unparsed compound objects as source mentions."""
    if not isinstance(raw, str) or UNCERTAIN.search(raw):
        return None
    for marker, predicate in RELATIONS:
        token = "_" + marker + "_"
        if token in raw:
            subject, target = raw.split(token, 1)
            if subject and target:
                # "Stone facing" is cladding; "front-facing" is a modifier,
                # and "warm under-cabinet lighting" has no object before "under".
                # Preserve these complete mentions without inventing a role edge.
                if subject in {"front", "rear", "back", "side", "north", "south", "east", "west",
                               "warm", "cool", "soft", "white", "black", "integrated", "built_in",
                               "recessed", "concealed", "led", "linear", "slim"}:
                    continue
                if marker == "facing" and target.startswith(("on_", "beneath_", "below_", "under_")):
                    continue
                return {"subject_mention": subject, "predicate": predicate,
                        "object_mention": target,
                        "coordinate_system": "camera_view_relative",
                        "world_orientation": None,
                        "limitations": [
                            "Literal source mentions; compound targets are not resolved into a measured object graph.",
                            "Left/right/depth refer to this view, never cardinal directions or a permanent house coordinate.",
                        ]}
    return None


def co_visible_functions(shot):
    scene = shot["scene"]
    # A scene transition does not mean simultaneous occupancy of one room.
    if "_to_" in scene or UNCERTAIN.search(scene):
        return []
    details = shot.get("visible_details", {}).get("architectural", [])
    explicit = ("open_plan" in scene or
                any("open_plan" in x and not UNCERTAIN.search(x) for x in details))
    if not explicit:
        return []
    functions = []
    for key, needles in (
        ("living", ("living",)), ("kitchen", ("kitchen",)),
        ("dining", ("dining",)), ("sleeping_loft", ("sleeping_loft", "bedroom_loft")),
    ):
        if any(n in scene for n in needles):
            functions.append(key)
    return functions if len(functions) > 1 else []


def checked_media(root, item):
    path = (root / item["path"]).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError("Unsafe evidence path")
    if not path.is_file() or sha256_file(path) != item["sha256"]:
        raise ValueError("Stale or missing evidence: " + item["path"])


def load_review_notes(root, filename, sources):
    path = root / "knowledge/reviews" / filename
    if not path.exists():
        return {"references": {}}
    data = json.loads(path.read_text())
    date.fromisoformat(data["reviewed_on"])
    for ident, item in data["references"].items():
        if ident not in sources:  # Historical events outside this release remain stored.
            continue
        if item["source"] != sources[ident]:
            raise ValueError("Stale AI review source: " + ident)
        for evidence in item["evidence"]:
            checked_media(root, evidence)
    return data


def validate_temporal(root, source, doc):
    path = root / "knowledge/temporal" / source["reference_id"] / "index.json"
    if not path.exists():
        return None
    data = json.loads(path.read_text())
    if data["source"] != source:
        raise ValueError("Stale temporal source")
    if len(data["shots"]) != len(doc["shots"]):
        raise ValueError("Temporal shot count differs")
    checked_media(root, {"path": data["contact_path"], "sha256": data["contact_sha256"]})
    for recorded, sampled in zip(doc["shots"], data["shots"]):
        if recorded["id"] != sampled["shot_id"]:
            raise ValueError("Temporal shot identity differs")
        a, b = float(recorded["start_s"]), float(recorded["end_s"])
        if (sampled["annotation_start_s"] != a or sampled["annotation_end_s"] != b
                or abs(sampled["sample_end_limit_s"] -
                       min(b, data["video_stream_duration_s"])) > 0.000001):
            raise ValueError("Temporal timing differs")
        frames = sampled["frames"]
        if [f["label"] for f in frames] != ["start", "middle", "end"]:
            raise ValueError("Temporal sample labels differ")
        times = [f["timestamp_s"] for f in frames]
        if not a < times[0] < times[1] < times[2] < min(b, data["video_stream_duration_s"]):
            raise ValueError("Temporal sample outside shot/stream")
        for frame in frames:
            checked_media(root, frame)
    return data


def make_observation(source, shot_id, pointer, statement, confidence, basis,
                     evidence, raw=None, key=None):
    result = {"schema_version": "1.0",
              "id": stable_id(source["reference_id"], shot_id or "overview", key or pointer),
              "source": source, "shot_id": shot_id, "field_path": pointer,
              "statement": str(statement), "claim_type": "OBSERVATION",
              "confidence": confidence, "basis": basis, "raw": raw,
              "evidence": evidence, "limitations": COMMON_LIMITS + (
                  ["This reports a saved annotation; it is not a new visual endorsement of that label."]
                  if basis == "recorded_annotation" else
                  ["Selected characteristics only; other tags at this location have not all been rechecked."])}
    validate_contract("observation", result)
    return result


def build_reference(root, source, doc, visual, temporal_notes):
    ident = source["reference_id"]
    selected = visual.get("references", {}).get(ident)
    temporal_review = temporal_notes.get("references", {}).get(ident)
    temporal = validate_temporal(root, source, doc)
    observations, reviews, relations, shots = [], [], [], []
    if selected:
        findings = []
        for key, pointer in (("exterior", "/architecture/exterior_features"),
                             ("interior", "/architecture/interior_style")):
            findings.append({"field_path": pointer, "status": "supported",
                             "reason": selected[key] + " Scope: selected appearance only, not every source tag."})
            observations.append(make_observation(
                source, None, pointer, selected[key], "medium", "ai_storyboard_review",
                selected["evidence"], key="visual." + key))
        findings += [{"field_path": "/architecture/building_scale/estimated_floor_area_m2",
                      "status": "unknown", "reason": "No measured dimensions available from storyboard."}]
        review = {"schema_version": "1.0", "id": ident + ".review.storyboard",
                  "source": source, "method": "ai_visual_review",
                  "reviewer": visual["reviewer"], "model_version": None,
                  "reviewed_on": visual["reviewed_on"], "scope": [visual["scope"]],
                  "evidence": selected["evidence"], "findings": findings}
        validate_contract("review", review)
        reviews.append(review)
    by_shot_review = {x["shot_id"]: x for x in temporal_review["shots"]} if temporal_review else {}
    if temporal_review:
        if not temporal:
            raise ValueError("Temporal review has no source samples")
        if set(by_shot_review) != {s["id"] for s in doc["shots"]}:
            raise ValueError("Temporal reviewed-shot coverage differs")
        review = {"schema_version": "1.0", "id": ident + ".review.temporal",
                  "source": source, "method": "ai_visual_review",
                  "reviewer": temporal_notes["reviewer"], "model_version": None,
                  "reviewed_on": temporal_notes["reviewed_on"],
                  "scope": [temporal_notes["scope"]],
                  "evidence": temporal_review["evidence"],
                  "findings": [{"field_path": f"/shots/{n}/framing", "status": "supported",
                                "reason": by_shot_review[s["id"]]["finding"] +
                                " This supports sampled framing changes, not the exact saved camera label."}
                               for n, s in enumerate(doc["shots"])]}
        validate_contract("review", review)
        reviews.append(review)
    for n, shot in enumerate(doc["shots"]):
        prefix = f"/shots/{n}"
        frame = shot["keyframe"]
        evidence = [{"path": frame, "sha256": sha256_file(root / frame), "kind": "source_keyframe"}]
        # A pointer to a keyframe is evidence availability, not proof it was separately reviewed.
        for suffix in ("scene", "focal_subject", "framing/start", "framing/end",
                       "framing/view_angle", "camera/movements", "camera/speed",
                       "lighting", "transition_out", "observation_note"):
            try:
                raw = resolve_pointer(doc, prefix + "/" + suffix)
            except KeyError:
                continue
            if raw is None or raw == [] or raw == "":
                continue
            observations.append(make_observation(
                source, shot["id"], prefix + "/" + suffix,
                "Recorded " + suffix + ": " + (", ".join(raw) if isinstance(raw, list) else str(raw)),
                shot.get("confidence", {}).get("camera" if suffix.startswith("camera") else "visual_details", "medium"),
                "recorded_annotation", evidence, raw=raw,
                key=shot["id"] + ":" + suffix))
        entities = []
        for category, role in (("architectural", "architectural_anchor_candidate"),
                               ("furniture_and_props", "furniture_or_prop"),
                               ("environment", "environment")):
            tags = shot.get("visible_details", {}).get(category, [])
            for k, raw in enumerate(tags):
                pointer = prefix + f"/visible_details/{category}/{k}"
                # Attribute descriptions remain intact, including shape, relative scale and occlusion.
                entities.append({"id": stable_id(ident, shot["id"] + ".mention", category + ":" + raw),
                                 "source_mention": raw, "field_path": pointer,
                                 "source_category": category, "role": role,
                                 "role_basis": "source_category_inference",
                                 "physical_identity_across_shots": "unknown"})
                parsed = relation_from_tag(raw)
                if parsed:
                    relation = {"schema_version": "1.0",
                                "id": stable_id(ident, shot["id"] + ".relation", category + ":" + raw),
                                "source": source, "shot_id": shot["id"], "field_path": pointer,
                                "raw": raw, "claim_type": "OBSERVATION",
                                "basis": "recorded_annotation_literal_relation",
                                "confidence": shot.get("confidence", {}).get("visual_details", "medium"),
                                **parsed}
                    validate_contract("relation", relation)
                    relations.append(relation)
        sampled = temporal["shots"][n] if temporal else None
        note = by_shot_review.get(shot["id"])
        if note:
            observations.append(make_observation(
                source, shot["id"], prefix + "/framing", note["finding"], "medium",
                "ai_sampled_temporal_review",
                [{"path": f["path"], "sha256": f["sha256"], "kind": "sampled_video_frame"}
                 for f in sampled["frames"]], key=shot["id"] + ":sampled_framing"))
        shots.append({
            "shot_id": shot["id"], "scene": shot["scene"], "field_path": prefix,
            "focal_subject": shot.get("focal_subject"),
            "framing_recorded": shot.get("framing"), "camera_recorded": shot.get("camera"),
            "subject_motion": {"state": "unknown", "reason": "No independent object-motion track; still samples cannot prove stillness."},
            "transition_recorded": shot.get("transition_out"),
            "light_recorded": shot.get("lighting"), "entities": entities,
            "co_visible_functions": co_visible_functions(shot),
            "co_visibility_basis": "explicit_open_plan_annotation" if co_visible_functions(shot) else "unknown",
            "window_world_mentions": [e for e in entities if e["source_category"] == "environment"
                                      and any(x in e["source_mention"] for x in ("window", "glazing", "door"))],
            "temporal_samples": sampled,
            "temporal_visual_review": {"state": "sampled_review" if note else "pending",
                                      "finding": note["finding"] if note else None,
                                      "reason": "Three sampled instants; intervals not verified." if note else
                                      ("Samples available; no new temporal visual review recorded for this source." if sampled else
                                       "Temporal sampling pending; no new visual review recorded for this source.")},
        })
    # Compare recorded scene aliases without asserting a source correction.
    aliases = doc["video_structure"]["scene_sequence"]
    consistency = []
    for n, shot in enumerate(doc["shots"]):
        if n < len(aliases) and aliases[n] != shot["scene"]:
            consistency.append({"field_path": f"/video_structure/scene_sequence/{n}",
                                "status": "ambiguous",
                                "reason": f"Overview alias {aliases[n]} differs from shot label {shot['scene']}; "
                                          "retained as aliases, not a proven factual error."})
    package = {"schema_version": "1.0", "source": source,
               "review_coverage": {"storyboard": "selected_characteristics" if selected else "pending",
                                  "temporal": "sampled_pilot" if temporal_review else "pending",
                                  "pending_reason": "Continuous playback/exact camera mechanism not reviewed in this enrichment pass."},
               "reviews": reviews, "annotation_discrepancies": consistency,
               "observations": observations, "relations": relations, "shots": shots,
               "sequence_links": [{"from_shot": a["id"], "to_shot": b["id"],
                                   "relation": "edit_sequence_only",
                                   "physical_room_adjacency": "unknown"}
                                  for a, b in zip(doc["shots"], doc["shots"][1:])],
               "unknowns": ["measured_floorplan", "cardinal_orientation", "physical_dimensions",
                            "geological_material_identity", "physical_building_existence",
                            "exact_lens_focal_length", "camera_path_in_world_coordinates",
                            "structural_feasibility", "same_physical_object_across_cuts"],
               "limitations": COMMON_LIMITS}
    validate_contract("design_evidence", package)
    return package


def render_reference(package, release_id):
    ident = package["source"]["reference_id"]
    lines = [f"# {ident} — design and temporal evidence", "",
             f"Release: {release_id}. [Profile](../reference-profiles/{ident}.md) · [All evidence](README.md) · "
             f"[Structured records]({ident}.json) · [Source](../../references/{ident}/analysis.yaml)", "",
             "## Review scope", "",
             "Review coverage is limited to the events listed below. Temporal review covers sampled instants only where explicitly recorded. "
             "Saved camera labels remain interpretations. No global verification flag or creative eligibility gate is used.", ""]
    if not package["reviews"]:
        lines += ["No new visual review recorded for this source; source annotations remain available.", ""]
    if package["annotation_discrepancies"]:
        lines += ["Metadata discrepancies retained without a source correction:", ""]
        lines += [f"- {x['field_path']}: {x['reason']}" for x in package["annotation_discrepancies"]]
        lines.append("")
    for review in package["reviews"]:
        lines += [f"### {review['id']}", "", f"{review['method']}; {review['reviewed_on']}; {review['reviewer']}.",
                  "Model build: unavailable, recorded as null. Scope: " + " ".join(review["scope"]), ""]
        for finding in review["findings"]:
            lines.append(f"- {finding['status']} — {md(finding['field_path'])}: {md(finding['reason'])}")
        lines.append("")
    lines += ["## Sampled shot progression", "",
              "| Shot | Recorded subject and framing | Camera / transition | Temporal scope |",
              "| --- | --- | --- | --- |"]
    for shot in package["shots"]:
        framing = shot["framing_recorded"] or {}
        camera = shot["camera_recorded"] or {}
        sample = shot["temporal_samples"]
        state = shot["temporal_visual_review"]
        link = f"[start / middle / end](../temporal/{ident}/contact.jpg)" if sample else "pending sampling"
        lines.append(f"| {shot['shot_id']} | {md(shot['focal_subject'])}; {md(framing.get('start'))} → "
                     f"{md(framing.get('end'))} | {md(', '.join(camera.get('movements', [])))}; "
                     f"{md(shot['transition_recorded'])} | {link}; {state['state']} |")
        if state["finding"]:
            lines.append(f"| | {md(state['finding'])} | sampled observation | |")
    lines += ["", "Object motion is unknown unless separately evidenced. A framing change does not establish a physical dolly path. "
              "Three frames cannot verify all intervening motion or continuity.", "",
              "## Explicit relations in saved annotations", "",
              "These are literal relation mentions, not newly verified geometry. Positions are relative to the camera view. "
              "Compound target phrases remain unresolved; object identity across shots is unknown.", "",
              "| Evidence ID | Shot | Subject → relation → target | Source pointer |",
              "| --- | --- | --- | --- |"]
    for row in package["relations"][:24]:
        lines.append(f"| {row['id']} | {row['shot_id']} | {md(row['subject_mention'])} → "
                     f"{row['predicate']} → {md(row['object_mention'])} | {md(row['field_path'])} |")
    if len(package["relations"]) > 24:
        lines += ["", f"Showing 24 of {len(package['relations'])} literal relations; full set is in the structured records."]
    shared = [s for s in package["shots"] if s["co_visible_functions"]]
    lines += ["", "## Spatial and continuity limits", ""]
    for shot in shared:
        lines.append(f"- {shot['shot_id']}: explicit open-plan annotation co-lists " +
                     ", ".join(shot["co_visible_functions"]) + "; no distances or measured adjacency asserted.")
    lines += ["", "Cross-shot links record edit order only. Exterior/interior cuts do not prove connected rooms. "
              "Architectural anchors are candidates derived from source categories; furniture/props and environment are separate. "
              "Original shape, proportion, texture, placement, occlusion and opening-view phrases remain in each shot's entity records.", "",
              "**Unknown:** " + ", ".join(package["unknowns"]) + ".", "",
              "## Creative interpretation", "",
              "DESIGN_PRINCIPLE: when designing a new house, choose a coherent mass/roof, opening family, fixed anchors, "
              "palette and window world. This is a creative design principle, not proof that this source resolves all of them. "
              "Low source confidence does not prevent choosing natural stone or a new spatial relationship for a new concept.", ""]
    return "\n".join(lines)


def aggregate_records(release, refs, packages):
    ids = sorted(refs)
    def any_scene(doc, term):
        return any(term in s["scene"] for s in doc["shots"])
    definitions = [
        ("exterior_opening", "Recorded first scene includes exterior", "/shots/0/scene contains exterior",
         lambda i: "exterior" in refs[i]["shots"][0]["scene"]),
        ("exterior_return", "Recorded last scene returns to exterior", "/shots/-1/scene contains exterior",
         lambda i: "exterior" in refs[i]["shots"][-1]["scene"]),
        ("shared_open_plan", "Explicit open-plan annotation co-lists multiple functions",
         "At least one shot passes explicit_open_plan_annotation; transitions excluded",
         lambda i: any(s["co_visible_functions"] for s in packages[i]["shots"])),
        ("sleeping_loft_scene", "Recorded scene names a sleeping/bedroom loft",
         "scene contains sleeping_loft or bedroom_loft",
         lambda i: any(any(t in s["scene"] for t in ("sleeping_loft", "bedroom_loft")) for s in refs[i]["shots"])),
        ("bathroom_scene", "Recorded scene includes bathroom", "Any scene contains bathroom",
         lambda i: any_scene(refs[i], "bathroom")),
        ("kitchen_scene", "Recorded scene includes kitchen", "Any scene contains kitchen",
         lambda i: any_scene(refs[i], "kitchen")),
    ]
    rows = []
    for key, statement, measurement, predicate in definitions:
        supported = [i for i in ids if predicate(i)]
        item = {"schema_version": "1.0", "id": "aggregate." + key,
                "release_id": release["release_id"], "claim_type": "AGGREGATE",
                "statement": statement, "measurement": measurement,
                "numerator": len(supported), "denominator": len(ids),
                "reference_ids": supported, "exceptions": [i for i in ids if i not in supported],
                "limitations": ["Counts published video references once each, not tags, rooms or verified independent physical houses.",
                                "No label is not proof of physical absence; annotation wording affects recall.",
                                "Video SHA uniqueness does not prove content or physical-house independence.",
                                "Frequency does not establish design quality, causal effect or audience performance."]}
        validate_contract("aggregate", item)
        rows.append(item)
    return rows


def diversity_report(release, refs, root):
    dimensions = {"primary_style": Counter(), "perceived_size": Counter(),
                  "recorded_scenes": Counter(), "setting_labels": Counter()}
    sources = {k: {} for k in dimensions}
    for ident, doc in refs.items():
        values = {"primary_style": {doc["architecture"]["primary_style"]},
                  "perceived_size": {doc["architecture"]["building_scale"]["perceived_size"]},
                  "recorded_scenes": {s["scene"] for s in doc["shots"]},
                  "setting_labels": set(doc["visual_style"].get("setting", []))}
        for dimension, labels in values.items():
            for label in sorted(labels):
                dimensions[dimension][label] += 1
                sources[dimension].setdefault(label, []).append(ident)
    # Versioned normalized concepts complement, never replace, literal labels.
    normalized = {}
    for ident in refs:
        data = json.loads((root / f"knowledge/enrichment/{ident}.json").read_text())
        binding = next(x for x in release["references"] if x["reference_id"] == ident)
        if data["source"] != binding:
            raise ValueError("Stale normalized diversity source")
        unique = {(m["dimension"], m["concept_id"])
                  for row in data["mappings"] for m in row["matches"]}
        for dimension, concept in unique:
            normalized.setdefault(dimension, {}).setdefault(concept, []).append(ident)
    return {"schema_version": "1.0", "release_id": release["release_id"],
            "denominator": len(refs), "unit": "published_video_reference",
            "taxonomy_version": release["taxonomy_version"],
            "normalized_dimensions": {dimension: [
                {"concept_id": c, "count": len(ids), "reference_ids": sorted(ids)}
                for c, ids in sorted(concepts.items())]
                for dimension, concepts in sorted(normalized.items())},
            "dimensions": {k: [{"label": label, "count": count, "reference_ids": sorted(sources[k][label])}
                               for label, count in sorted(v.items(), key=lambda row: (-row[1], row[0]))]
                           for k, v in dimensions.items()},
            "limitations": ["Exact recorded labels; synonyms may split categories. Multi-label rows need not sum to denominator.",
                            "Setting describes visual appearance, not confirmed season/geography.",
                            "Counts do not prove independent houses or population representativeness."]}


def render_corpus(release, aggregates, diversity, packages):
    lines = ["# Corpus patterns and diversity", "",
             f"Release: {release['release_id']}; {release['reference_count']} published video references; "
             f"{release['shot_count']} shots. [Evidence coverage](design-evidence/README.md) · "
             "[Count definitions and full source lists](aggregates.json) · [Diversity data](diversity.json)", "",
             "## Counted patterns — AGGREGATE", "",
             "Each reference is counted once. Unique video files do not establish independent physical houses. "
             "Possible content overlaps remain candidates in the [similarity report](similarity/README.md).", "",
             "| Pattern / evidence ID | Count | Examples | Counterexamples: label absent |",
             "| --- | --- | --- | --- |"]
    links = lambda ids: ", ".join(f"[{i}](reference-profiles/{i}.md)" for i in ids[:4]) or "none"
    for row in aggregates:
        lines.append(f"| {row['statement']} — {row['id']} | {row['numerator']}/{row['denominator']} | "
                     f"{links(row['reference_ids'])} | {links(row['exceptions'])} |")
    lines += ["", "Absent labels are annotation exceptions, not proof that a physical feature is absent. "
              "These frequencies describe this library, not a universal rule or proof of quality.", "",
              "## Design synthesis", "",
              "- **INFERENCE — recurring identity cues:** repeated opening shapes, warm pale surfaces, timber-like accents and "
              "garden views can help readers recognize a visual family. This does not establish the same material or object across cuts. "
              "Compare [arched stone-like edh020](design-evidence/edh020.md), [organic edh013](design-evidence/edh013.md), "
              "and the rectilinear [edh060](design-evidence/edh060.md). The last is a counterexample to requiring arches.",
              "- **DESIGN_PRINCIPLE — architecture and interior:** carry a selected geometry, opening family and palette into a new concept. "
              "Compatibility depends on proportions and functional circulation chosen for that new design; source edits do not supply its plan.",
              "- **DESIGN_PRINCIPLE — landscape and light:** coordinate the outside-window world, exterior planting and selected light state. "
              "Compare snowy-looking [edh059](design-evidence/edh059.md) with green-garden [edh042](design-evidence/edh042.md). "
              "Appearance does not establish season, location, or an obligatory climate.",
              "- **INFERENCE — space:** shared-function views can communicate compactness without implying a measured plan. "
              "[edh033](design-evidence/edh033.md) and [edh060](design-evidence/edh060.md) show useful loft examples. "
              "[edh058](design-evidence/edh058.md) presents functions in separate edited views; adjacency remains unknown.",
              "- **INFERENCE — camera and composition:** in pilot samples, changing foreground occlusion and subject size provide cues to a changing "
              "viewpoint/framing. Three stills cannot distinguish all zoom, dolly, generated deformation or edit contributions. "
              "[VID-001](design-evidence/VID-001.md) ends its first sampled shot in transition blur, so its endpoint is not a clean architectural view.",
              "- **DESIGN_PRINCIPLE — continuity and originality:** for a new house, choose consistent fixed anchors and geometry while varying "
              "composition and removable props deliberately. Combine principles from sources instead of reproducing a single source's entire signature. "
              "New relationships and material choices are creative decisions, not recovered source facts.", "",
              "## Diversity and collection gaps", "",
              "Exact source-label counts below preserve wording. Normalized discovery remains in the [directories](directories/README.md).", ""]
    for key in ("primary_style", "perceived_size", "recorded_scenes"):
        lines += [f"### {key}", "", "| Label | References |", "| --- | --- |"]
        for row in diversity["dimensions"][key][:18]:
            lines.append(f"| {md(row['label'])} | {row['count']}/{diversity['denominator']} |")
        lines.append("")
    lines += ["Prioritize future references that add a different scale, shared-function configuration, light state, opening geometry, "
              "or garden relationship. Review exact-label fragmentation before interpreting a rare label as a real collection gap. "
              "No target quota is inferred from this non-random library.", "",
              "## Review limits", "",
              f"{sum(p['review_coverage']['storyboard'] != 'pending' for p in packages.values())}/{len(packages)} storyboards received a selected-characteristic AI review. "
              f"{sum(p['review_coverage']['temporal'] != 'pending' for p in packages.values())}/{len(packages)} sources received a visual review "
              "of three temporal samples per shot. Other temporal samples have review explicitly pending. "
              "No full-clip revalidation of every saved tag is claimed.", ""]
    return "\n".join(lines)


def build_outputs(root=ROOT):
    root = Path(root)
    release = load_release(root)
    archives = read_archives(root)
    sources = {s["reference_id"]: s for s in release["references"]}
    refs = {i: archives[i] for i in sources}
    visual = load_review_notes(root, "visual-notes.json", sources)
    temporal_notes = load_review_notes(root, "temporal-notes.json", sources)
    outputs, packages = {}, {}
    for ident, source in sources.items():
        package = build_reference(root, source, refs[ident], visual, temporal_notes)
        packages[ident] = package
        outputs[f"knowledge/design-evidence/{ident}.json"] = dump(package)
        outputs[f"knowledge/design-evidence/{ident}.md"] = render_reference(package, release["release_id"])
        outputs[f"knowledge/reviews/{ident}.json"] = dump({"schema_version": "1.0", "source": source,
                                                         "reviews": package["reviews"]})
    aggregates = aggregate_records(release, refs, packages)
    diversity = diversity_report(release, refs, root)
    outputs["knowledge/aggregates.json"] = dump({"schema_version": "1.0", "release_id": release["release_id"],
                                               "source_bindings": list(sources.values()), "records": aggregates})
    outputs["knowledge/diversity.json"] = dump(diversity)
    outputs["knowledge/corpus-patterns.md"] = render_corpus(release, aggregates, diversity, packages)
    counts = {"references": len(packages), "shots": sum(len(p["shots"]) for p in packages.values()),
              "observations": sum(len(p["observations"]) for p in packages.values()),
              "literal_relations": sum(len(p["relations"]) for p in packages.values()),
              "storyboard_reviews": sum(p["review_coverage"]["storyboard"] != "pending" for p in packages.values()),
              "sampled_temporal_reviews": sum(p["review_coverage"]["temporal"] != "pending" for p in packages.values()),
              "sampled_frames": sum(len(s["temporal_samples"]["frames"])
                                    for p in packages.values() for s in p["shots"] if s["temporal_samples"])}
    coverage = {"schema_version": "1.0", "release_id": release["release_id"], "counts": counts,
                "sources": [{"source": p["source"], "coverage": p["review_coverage"],
                             "observation_count": len(p["observations"]), "relation_count": len(p["relations"])}
                            for p in packages.values()]}
    outputs["knowledge/design-evidence/coverage.json"] = dump(coverage)
    lines = ["# Design evidence coverage", "", f"Release: {release['release_id']}. "
             "[Core knowledge](../ai-knowledge.md) · [Corpus patterns](../corpus-patterns.md) · "
             "[Coverage data](coverage.json) · [Review method](../reviews/README.md)", "",
             "OBSERVATION records distinguish saved annotations from selected AI visual observations. "
             "Literal relation extraction never proves world coordinates or room adjacency. "
             "All saved references remain usable for creative inspiration.", "",
             " · ".join(f"{k}: {v}" for k, v in counts.items()), "",
             "| Reference | Storyboard review | Temporal review | Relations |", "| --- | --- | --- | --- |"]
    for ident, p in packages.items():
        c = p["review_coverage"]
        lines.append(f"| [{ident}]({ident}.md) | {c['storyboard']} | {c['temporal']} | {len(p['relations'])} |")
    lines += ["", "Pending temporal review means samples exist without a new visual review event. It does not exclude a reference. "
              "Full continuous motion and exact camera mechanics remain outside this sample-based enrichment pass.", ""]
    outputs["knowledge/design-evidence/README.md"] = "\n".join(lines)
    return outputs, coverage


def run(root=ROOT, write=False):
    root = Path(root)
    outputs, coverage = build_outputs(root)
    for relative, content in outputs.items():
        path = root / relative
        if write:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        elif not path.is_file() or path.read_text() != content:
            raise ValueError("Stale generated design evidence: " + relative)
    return coverage


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    print(dump(run(args.root, args.write)["counts"]))


if __name__ == "__main__":
    main()
