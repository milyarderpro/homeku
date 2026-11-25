"""Build deterministic discovery and knowledge from registered audit sources."""
from __future__ import annotations

import hashlib
import os
from collections import defaultdict
from pathlib import Path

from . import FORMAT_VERSION
from .common import LibraryError, cell, dumps, read_json, require, sha256, slug, snapshot_hash
from .derivations import claims, fact_claims, profile_claims, tempo_segments, camera_summary, derived_shot
from .camera_pattern import video_pattern
from .models import schema_check
from .validation import CODE_ROOT, validate_folder

PAGE_SIZE = 40
GENERATOR_MODULES = (
    "__init__", "audit_quality", "camera_notation", "camera_pattern", "common",
    "derivations", "generation", "media", "models", "package_manifest", "render_assets",
    "report_validation", "reporting", "validation", "video", "video_cache",
    "engine", "storage", "reader", "audit_performance",
)
SCHEMA_PATHS = ("audit", "audit-info", "manifest", "reference-reader", "search-index")
ASSETS = ("templates/analysis.md", "templates/analysis-profile.md",
          "layouts/media.json", "layouts/media-aligned.json", "fonts/DejaVuSans.ttf",
          "fonts/DejaVuSans-Bold.ttf", "fonts/LICENSE.txt")


def generator_fingerprint(root: Path):
    files = [CODE_ROOT / "tools/homeku" / f"{name}.py" for name in GENERATOR_MODULES]
    # A schema or asset is an operational input. Planning files are never inputs.
    files += [CODE_ROOT / "schemas" / f"{name}.schema.json" for name in SCHEMA_PATHS]
    files += [CODE_ROOT / "tools/assets" / name for name in ASSETS]
    files += [CODE_ROOT / "sources/design-principles.json"]
    hashes = [(p.relative_to(CODE_ROOT).as_posix(), sha256(p)) for p in sorted(files)]
    hashes += [("data/taxonomy.json", sha256(root / "data/taxonomy.json")), ("format", FORMAT_VERSION)]
    return hashlib.sha256(dumps(hashes).encode()).hexdigest()


def _fingerprint(content, runtime):
    return hashlib.sha256((content + runtime).encode()).hexdigest()


def load_models(root: Path, registry, full=False):
    """Reuse a verified projection's audit, bound to its accepted snapshot."""
    previous = root / "data/build.json"
    try:
        build = read_json(previous) if previous.is_file() else {}
    except (LibraryError, OSError):
        build = {}
    if not isinstance(build, dict):
        build = {}
    projections, hashes = (build.get(k) for k in ("projections", "projection_sha256"))
    if not isinstance(projections, dict) or not isinstance(hashes, dict):
        projections, hashes = {}, {}
    runtime = generator_fingerprint(root)
    models = {}
    for rid, entry in sorted(registry["references"].items()):
        folder = root / "references" / rid
        require(folder.is_dir() and not folder.is_symlink(), f"Missing/symlinked registered reference: {rid}")
        snapshot = snapshot_hash(folder)
        require(snapshot == entry["content_sha256"], f"Unapproved edits to references/{rid}; submit a new ZIP revision")
        for name, field in (("audit.json", "audit_sha256"), ("analysis.md", "analysis_sha256"),
                            ("manifest.json", "manifest_sha256")):
            require(sha256(folder / name) == entry[field], f"Registry document hash mismatch: {rid}/{name}")
        manifest = read_json(folder / "manifest.json")
        require(manifest.get("contract_version") == FORMAT_VERSION and manifest["revision"] == entry["revision"]
                and manifest["id"] == rid, f"Registry version or identity differs: {rid}")
        require(manifest["source"]["path"] == f"video/{rid}.mp4"
                and manifest["source"]["sha256"] == entry["source_sha256"], f"Registry source differs: {rid}")
        projection = root / "data/projections" / f"{rid}.json"
        if (not full and projection.is_file()
                and projections.get(rid) == _fingerprint(snapshot, runtime)
                and hashes.get(rid) == sha256(projection)):
            cached = read_json(projection)
            if (cached.get("schema_version") == FORMAT_VERSION and cached.get("content_sha256") == snapshot
                    and cached["reference"]["revision"] == entry["revision"]):
                video = root / manifest["source"]["path"]
                require(video.is_file() and not video.is_symlink() and sha256(video) == entry["source_sha256"],
                        f"Registered source changed or missing: {rid}")
                models[rid] = {"id": rid, "revision": entry["revision"], "audit": cached["reference"],
                               "manifest": manifest, "content_sha256": snapshot}
                continue
        _, models[rid], _ = validate_folder(folder, root)
    return models


def aliases(taxonomy):
    groups = {}
    require(isinstance(taxonomy.get("version"), int) and isinstance(taxonomy.get("areas"), dict),
            "Invalid taxonomy")
    for group, entries in taxonomy.items():
        if not isinstance(entries, dict):
            continue
        labels = {}
        for canonical, values in sorted(entries.items()):
            require(isinstance(values, list) and all(isinstance(v, str) for v in values), "Invalid alias list")
            for value in (canonical, *values):
                key = value.casefold()
                require(key not in labels or labels[key] == canonical, f"Ambiguous {group} alias: {value}")
                labels[key] = canonical
        groups[group] = labels
    return groups


def canonical(groups, group, value):
    return groups.get(group, {}).get(value.casefold(), value) if isinstance(value, str) else value


def facts_for(shot, index):
    for pointer, claim, area_ids, category in fact_claims(shot, index):
        yield {**claim, "domain": claim.get("domain", category), "category": category,
               "area_ids": area_ids, "source_pointer": pointer}


def profile_facets(audit, groups):
    for pointer, claim, aspect in profile_claims(audit):
        group = ("styles" if aspect in {"primary-style", "style-influence", "interior-style"}
                 else {"apparent-scale": "scales", "house-type": "house_types"}.get(aspect, aspect))
        yield {**claim, "aspect": aspect, "canonical": canonical(groups, group, claim["value"]),
               "source_pointer": pointer}


def indexed_shot(audit, shot, index, frames, groups):
    rid, sid = audit["id"], shot["shot"]
    areas = {a["id"]: a for a in audit["areas"]}
    labels = sorted({label for aid in shot["area_ids"]
                     for label in (areas[aid]["label"], *areas[aid]["functions"])})
    derived = derived_shot(shot, index)
    components = [part for phase in derived["components"] for part in phase]
    path = f"references/{rid}"
    return {"shot": sid, "areas": labels, "areas_canonical": sorted({canonical(groups, "areas", v) for v in labels}),
            "area_labels_by_id": {aid: sorted({canonical(groups, "areas", v) for v in
                                              (areas[aid]["label"], *areas[aid]["functions"])})
                                  for aid in shot["area_ids"]},
            "multi_area": len(shot["area_ids"]) > 1,
            "route": [areas[row["area_id"]]["label"] for row in shot.get("route", [])],
            "continuity": shot.get("continuity"),
            "view_angle": shot["composition"]["view_angle"],
            "camera": derived["camera_summary"], "camera_pattern": derived["camera_pattern"],
            "movements": sorted({canonical(groups, "movements", c["movement"] if c["movement"] != "other" else c["raw"])
                                 for c in components}),
            "camera_qualifiers": sorted({q for c in components for q in c["qualifiers"]}),
            "tempos": sorted({t["label"] for t in tempo_segments(shot)}),
            "design_facets": [{k: v for k, v in fact.items() if k not in {"evidence", "note"}}
                              for fact in facts_for(shot, index) if fact.get("facet_roles")],
            "path": f"{path}/analysis.md#{sid}", "source_pointer": f"/shots/{index}",
            "overview": f"{path}/media/overview.jpg", "collage": f"{path}/media/{sid}.jpg",
            "storyboard": f"{path}/media/storyboard.jpg",
            "overview_selection_ids": [p["id"] for p in frames if p["shot_id"] == sid and p["role"] == "overview"]}


def provenance_for(audit, manifest):
    pointers = {}

    def record(target, document, source):
        pointers[target] = {"document": document, "source_pointer": source}

    def direct(source):
        record("/reference" + source, "audit", source)

    direct("")
    for path in ("/design", "/design/name", "/design/styles", "/design/size",
                 "/design/size/floor_area_m2", "/areas", "/shots"):
        direct(path)
    if "notes" in audit:
        direct("/notes")
    for i, area in enumerate(audit["areas"]):
        direct(f"/areas/{i}")
        direct(f"/areas/{i}/visible_intervals")
        direct(f"/areas/{i}/functions")
    for key, claim, *_ in claims(audit):
        direct(key)
        if "facet_roles" in claim:
            direct(key + "/facet_roles")
        for i, _ in enumerate(claim.get("overrides", [])):
            direct(f"{key}/overrides/{i}")
    for i, shot in enumerate(audit["shots"]):
        base = f"/shots/{i}"
        direct(base)
        for key in ("composition", "design", "camera", "route", "area_relations", "notes", "continuity"):
            if key in shot:
                direct(base + "/" + key)
        for j, group in enumerate(shot["design"]):
            for category in ("architecture", "furnishings", "environment"):
                direct(f"{base}/design/{j}/{category}")
        for j, phase in enumerate(shot["camera"]["phases"]):
            for key in ("notation", "depth_direction", "observations"):
                direct(f"{base}/camera/phases/{j}/{key}")
        direct(base + "/camera/tempo")
        for j, _ in enumerate(shot["camera"]["tempo"].get("segments", [])):
            direct(f"{base}/camera/tempo/segments/{j}")
        for j, _ in enumerate(shot.get("route", [])):
            direct(f"{base}/route/{j}")
        for group in ("panels", "overviews"):
            for j, choice in enumerate(shot[group]):
                direct(f"{base}/{group}/{j}")
                if "composition_summary" in choice:
                    direct(f"{base}/{group}/{j}/composition_summary")
        pointers[f"/derived/shots/{i}"] = {
            "document": "audit", "derivation": "Camera notation, depth and tempo overlap",
            "inputs": [base + "/camera/phases", base + "/camera/tempo"]}
    pointers["/derived/camera_pattern"] = {
        "document": "audit", "derivation": "Ordered depth directions",
        "inputs": [f"/shots/{i}/camera/phases" for i, _ in enumerate(audit["shots"])]}
    record("/source", "manifest", "/source")
    for index in manifest["frames"]:
        record(f"/evidence_inventory/frames/{index}", "manifest", f"/frames/{index}")
    for group in ("selections", "media"):
        for i, _ in enumerate(manifest[group]):
            record(f"/evidence_inventory/{group}/{i}", "manifest", f"/{group}/{i}")
    return pointers


def projection(model):
    from .models import evidence_inventory
    audit, manifest = model["audit"], model["manifest"]
    path = f"references/{audit['id']}"
    return {"schema_version": FORMAT_VERSION, "kind": "homeku.reference",
            "content_sha256": model["content_sha256"], "reference": audit, "source": manifest["source"],
            "paths": {"analysis": f"{path}/analysis.md", "audit": f"{path}/audit.json",
                      "manifest": f"{path}/manifest.json", "source": manifest["source"]["path"]},
            "provenance": provenance_for(audit, manifest), "derived": {"camera_pattern": video_pattern(audit["shots"]),
                                          "shots": [derived_shot(s, i) for i, s in enumerate(audit["shots"])]},
            "evidence_inventory": evidence_inventory(model)}


def render(root: Path, models):
    groups = aliases(read_json(root / "data/taxonomy.json"))
    outputs, dependencies = {}, {}
    ids = sorted(models)
    count_shots = sum(len(m["audit"]["shots"]) for m in models.values())
    runtime = generator_fingerprint(root)

    def emit(path, text, references=()):
        outputs[path] = text.rstrip() + "\n"
        dependencies[path] = sorted(set(references))

    def link(page, path, label):
        destination = os.path.relpath(path, str(Path(page).parent)).replace(os.sep, "/")
        return f"[{cell(label)}]({destination})"

    def md_link(page, rid, sid=None):
        anchor = "#" + sid if sid else "#profil-dna"
        return link(page, f"references/{rid}/analysis.md{anchor}", f"{rid} / {sid}" if sid else rid)

    def paged(base, title, records, columns, row_fn):
        index_path = f"{base}/README.md"
        index = [f"# {title}", "", f"{len(records)} entri tercatat.", ""]
        for offset in range(0, len(records), PAGE_SIZE):
            chunk = records[offset:offset + PAGE_SIZE]
            path = f"{base}/page-{offset // PAGE_SIZE + 1:03d}.md"
            text = [f"# {title} — {offset // PAGE_SIZE + 1}", "",
                    "| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
            text.extend("| " + " | ".join(row_fn(path, item)) + " |" for item in chunk)
            emit(path, "\n".join(text), [item[0] for item in chunk])
            index.append("- " + link(index_path, path, f"Halaman {offset // PAGE_SIZE + 1}"))
        if not records:
            index.append("Belum ada entri aktif.")
        emit(index_path, "\n".join(index), [item[0] for item in records])
        return index_path

    references = ["# Referensi aktif", "", f"{len(ids)} referensi dan {count_shots} shot.", "",
                  "| Referensi | Judul | Shot |", "| --- | --- | --- |"]
    rooms, domains, comparisons = defaultdict(list), defaultdict(list), defaultdict(list)
    shots, phases, dna, search = [], [], [], []
    fingerprints, projection_hashes = {}, {}

    def digest(value):
        return hashlib.sha256(value.encode()).hexdigest()

    def proof(rid, index):
        m = models[rid]["manifest"]
        return {"source": m["source"]["path"], "frame_index": index,
                "timestamp_s": m["frames"][str(index)], "source_pointer": f"/frames/{index}"}

    def evidence_links(page, rid, evidence):
        result = []
        for index in evidence:
            item = proof(rid, index)
            result.append(link(page, item["source"] + f"#t={item['timestamp_s']}", f"F{index}"))
        return ", ".join(result) if result else "—"

    for rid in ids:
        model = models[rid]
        audit, manifest = model["audit"], model["manifest"]
        markdown, json_path = f"references/{rid}/analysis.md", f"data/projections/{rid}.json"
        references.append(f"| {link('catalogs/references.md', markdown, rid)} | {cell(audit['design']['name'])} | {len(audit['shots'])} |")
        index_shots = []
        for index, shot in enumerate(audit["shots"]):
            sid = shot["shot"]
            summary = indexed_shot(audit, shot, index, manifest["selections"], groups)
            index_shots.append(summary)
            shots.append((rid, shot, summary))
            for area in summary["areas_canonical"]:
                rooms[area].append((rid, shot, summary))
            for fact in facts_for(shot, index):
                item = (rid, sid, fact)
                domains[fact["domain"]].append(item)
                comparisons[(fact["domain"], fact["subject"], fact["attribute"])].append(item)
            for phase in shot["camera"]["phases"]:
                phases.append((rid, sid, phase))
        facets = list(profile_facets(audit, groups))
        dna.extend((rid, facet) for facet in facets)
        search.append({"id": rid, "title": audit["design"]["name"], "revision": audit["revision"],
                       "json": json_path, "camera_pattern": video_pattern(audit["shots"]),
                       "floor_area_m2": audit["design"]["size"]["floor_area_m2"],
                       "style_relations": [{**{k: v for k, v in relation.items() if k not in {"description", "evidence", "note"}},
                                           "source_pointer": f"/design/styles/relations/{i}"}
                                          for i, relation in enumerate(audit["design"]["styles"].get("relations", []))],
                       "profile_facets": [{k: v for k, v in item.items() if k not in {"evidence", "note"}} for item in facets],
                       "shots": index_shots})
        reader = projection(model)
        schema_check(reader, "reference-reader.schema.json")
        emit(json_path, dumps(reader), [rid])
        fingerprints[rid] = _fingerprint(model["content_sha256"], runtime)
        projection_hashes[rid] = digest(outputs[json_path])

    emit("catalogs/references.md", "\n".join(references), ids)

    def grouped_index(base, title, groups, columns, row_fn):
        page = f"{base}/README.md"
        lines = [f"# {title}", ""]
        registered = []
        for name, records in sorted(groups.items()):
            index = paged(f"{base}/{slug(name)}", name, records, columns, row_fn)
            lines.append(f"- {link(page, index, name)} · {len(records)}")
            registered.extend(item[0] for item in records)
        if not groups:
            lines.append("Belum ada entri aktif.")
        emit(page, "\n".join(lines), registered)

    grouped_index("catalogs/rooms", "Ruang dan fungsi", rooms,
                  ["Sumber", "Area dan fungsi", "Camera Start", "Kolase"],
                  lambda p, r: [md_link(p, r[0], r[1]["shot"]), cell(" / ".join(r[2]["areas"])),
                                cell(r[1]["composition"]["camera_position"]), link(p, r[2]["collage"], "Kolase")])
    grouped_index("catalogs/design", "Desain, arsitektur dan lingkungan", domains,
                  ["Sumber", "Subjek", "Atribut", "Nilai", "Status", "Catatan", "Bukti"],
                  lambda p, r: [md_link(p, *r[:2]), cell(r[2]["subject"]), cell(r[2]["attribute"]),
                                cell(r[2]["value"]), cell(r[2]["state"]), cell(r[2].get("note", "—")),
                                evidence_links(p, r[0], r[2]["evidence"])])
    paged("catalogs/composition", "Posisi kamera dan komposisi", shots,
          ["Sumber", "Posisi / arah / sudut", "Awal → akhir", "Kedalaman / cahaya", "Overview"],
          lambda p, r: [md_link(p, r[0], r[1]["shot"]),
                        cell(" · ".join(r[1]["composition"][k] for k in ("camera_position", "camera_direction", "view_angle"))),
                        cell(r[1]["composition"]["start_composition"] + " → " + r[1]["composition"]["end_composition"]),
                        cell(r[1]["composition"]["depth"] + " · " + r[1]["composition"]["lighting"]),
                        link(p, r[2]["overview"], "Overview")])
    paged("catalogs/camera", "Gerakan dan ritme", shots,
          ["Sumber", "Notasi fase", "Pola", "Tempo", "Kolase"],
          lambda p, r: [md_link(p, r[0], r[1]["shot"]), cell(camera_summary(r[1])),
                        cell(r[2]["camera_pattern"] or "—"), cell(r[1]["camera"]["tempo"]["description"]),
                        link(p, r[2]["collage"], "Kolase")])
    paged("catalogs/camera/phases", "Fase gerakan kamera", phases,
          ["Sumber", "Interval", "Notasi", "Arah", "Bukti"],
          lambda p, r: [md_link(p, *r[:2]), f"{r[2]['start_s']:.2f}–{r[2]['end_s']:.2f}s",
                        cell(r[2]["notation"]), cell(r[2]["depth_direction"] or "—"),
                        evidence_links(p, r[0], r[2]["evidence"])])
    outputs["catalogs/camera/README.md"] += "\n- [Fase gerakan kamera](phases/README.md)\n"
    paged("catalogs/dna", "Profil DNA, gaya dan skala", dna,
          ["Sumber", "Aspek", "Nilai", "Status", "Confidence", "Bukti"],
          lambda p, r: [md_link(p, r[0]), cell(r[1]["aspect"]), cell(r[1]["value"]),
                        cell(r[1]["state"]), cell(r[1].get("confidence") or "—"),
                        evidence_links(p, r[0], r[1]["evidence"])])

    topics = []
    for key, records in sorted(comparisons.items()):
        title = " / ".join(key)
        base = f"knowledge/comparisons/{slug(title)}"
        denominator = len({(rid, sid) for rid, sid, _ in records})
        variants = defaultdict(list)
        for rid, sid, item in records:
            variants[(item["state"], dumps(item["value"]))].append((rid, sid))
        rows = []
        for rid, sid, item in records:
            examples = variants[(item["state"], dumps(item["value"]))]
            rows.append((rid, sid, item, len({r for r, _ in examples}), len(set(examples))))
        paged(base, title, rows, ["Nilai", "Status", "Referensi", "Shot / tercatat", "Sumber"],
              lambda p, r: [cell(r[2]["value"]), cell(r[2]["state"]), str(r[3]),
                            f"{r[4]} / {denominator}", md_link(p, *r[:2])])
        pages = []
        referenced = [r[0] for r in rows]
        for offset in range(0, len(rows), PAGE_SIZE):
            chunk = rows[offset:offset + PAGE_SIZE]
            path = f"{base}/page-{offset // PAGE_SIZE + 1:03d}.json"
            claims = [{"reference": rid, "shot": sid, "fact": item, "reference_count": refs,
                       "shot_count": occurrences, "denominator": denominator,
                       "source": f"references/{rid}/audit.json",
                       "json": f"data/projections/{rid}.json",
                       "evidence": [proof(rid, i) for i in item["evidence"]]}
                      for rid, sid, item, refs, occurrences in chunk]
            emit(path, dumps({"schema_version": FORMAT_VERSION, "kind": "homeku.fact-comparisons",
                              "claims": claims}), referenced)
            pages.append(path)
        index = f"{base}/index.json"
        emit(index, dumps({"schema_version": FORMAT_VERSION, "attribute": list(key),
                           "denominator": denominator, "pages": pages}), referenced)
        topics.append({"attribute": list(key), "denominator": denominator, "json": index})
    topic_path = "knowledge/topics/index.json"
    emit(topic_path, dumps({"schema_version": FORMAT_VERSION, "kind": "homeku.knowledge-topics",
                            "topics": topics}), ids)
    emit("knowledge/topics/README.md", "# Daftar perbandingan\n\n" + ("\n".join(
        f"- {link('knowledge/topics/README.md', topic['json'].replace('index.json', 'README.md'), ' / '.join(topic['attribute']))}"
        for topic in topics) or "Belum ada klaim aktif."), ids)

    principles = read_json(CODE_ROOT / "sources/design-principles.json")
    items = principles["principles"]
    require(isinstance(items, list) and len(set(p["id"] for p in items)) == len(items),
            "Invalid curated principles")
    lines = ["# Prinsip desain terkurasi", ""]
    for item in items:
        require(item["claim_type"] == "design-principle", "Curated principles must remain distinct from audit facts")
        lines.extend([f"## {item['title']}", "", item["guidance"], "", "Batas: " + item["limitations"], ""])
    emit("knowledge/principles.json", dumps(principles))
    emit("knowledge/principles.md", "\n".join(lines))
    emit("knowledge/README.md", "# Knowledge berbasis audit\n\n" +
         f"{len(ids)} referensi dan {count_shots} shot aktif. Perbandingan mempertahankan status sumber.\n\n"
         "- [Perbandingan menurut atribut](topics/README.md)\n"
         "- [Prinsip umum terkurasi](principles.md)\n", ids)
    emit("catalogs/README.md", "# Katalog HOMEKU\n\n" + f"{len(ids)} referensi aktif, {count_shots} shot.\n\n" +
         "\n".join(f"- [{title}]({target})" for title, target in (
             ("Referensi", "references.md"), ("Ruang dan fungsi", "rooms/README.md"),
             ("Desain", "design/README.md"), ("Komposisi", "composition/README.md"),
             ("Gerakan dan tempo", "camera/README.md"), ("Profil DNA", "dna/README.md"),
             ("Knowledge", "../knowledge/README.md"))), ids)
    index = {"schema_version": FORMAT_VERSION, "kind": "homeku.search-index", "taxonomy": "data/taxonomy.json",
             "principles": "knowledge/principles.json", "knowledge": topic_path, "references": search}
    schema_check(index, "search-index.schema.json")
    emit("data/search-index.json", dumps(index), ids)
    emit("data/dependencies.json", dumps({"generator_fingerprint": runtime,
                                         "source_files": ["sources/design-principles.json", "data/taxonomy.json",
                                                          "schemas/", "tools/assets/", "tools/homeku/"],
                                         "outputs": dependencies.copy()}), ids)
    emit("data/build.json", dumps({"generator_fingerprint": runtime, "projections": fingerprints,
                                   "projection_sha256": projection_hashes,
                                   "outputs": {path: digest(value) for path, value in sorted(outputs.items())}}), ids)
    return outputs
