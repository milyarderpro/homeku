"""Source-backed catalogs and comparisons, with bounded pages and explicit states."""

from __future__ import annotations
from .versions import JSON_CONTRACTS, OVERVIEW_CONTRACTS

import hashlib
import os
from collections import defaultdict
from pathlib import Path

from . import GENERATOR_VERSION
from .common import LibraryError, cell, content_hash, dumps, read_json, require, sha256, slug
from .validation import CODE_ROOT, validate_folder
from .models import evidence_inventory

PAGE_SIZE = 40


def generator_fingerprint(root: Path):
    inputs = [(p.name, sha256(p)) for p in sorted((CODE_ROOT / "tools/homeku").glob("*.py"))]
    inputs += [(p.name, sha256(p)) for p in sorted((CODE_ROOT / "docs/contracts").glob("*.schema.json"))]
    inputs += [(p.relative_to(CODE_ROOT).as_posix(), sha256(p)) for p in sorted((CODE_ROOT / "tools/assets").rglob("*")) if p.is_file()]
    inputs += [("approved-template", sha256(CODE_ROOT / "docs/template-analysis-v2.md"))]
    inputs += [("fact-facets", sha256(CODE_ROOT / "sources/fact-facets.json")), ("principles", sha256(CODE_ROOT / "sources/design-principles.json")), ("taxonomy", sha256(root / "data/taxonomy.json")), ("version", GENERATOR_VERSION)]
    return hashlib.sha256(dumps(inputs).encode()).hexdigest()


def load_models(root: Path, registry, full=False):
    """Reuse projections only when every reference byte and source still match."""
    models = {}
    build_path = root / "data/build.json"
    try:
        previous_build = read_json(build_path) if build_path.is_file() else {}
    except (LibraryError, OSError):
        previous_build = {}
    if not isinstance(previous_build, dict):
        previous_build = {}
    fingerprint = generator_fingerprint(root)
    for reference_id, entry in sorted(registry["references"].items()):
        folder = root / "references" / reference_id
        require(folder.is_dir() and not folder.is_symlink(), f"Missing/symlinked registered reference: {reference_id}")
        actual_hash = content_hash(folder)
        require(actual_hash == entry["content_sha256"], f"Unapproved edits to references/{reference_id}; submit a new ZIP revision")
        require(sha256(folder / "analysis.md") == entry["analysis_sha256"] and sha256(folder / "manifest.json") == entry["manifest_sha256"],
                f"Registry document hash mismatch: {reference_id}")
        manifest = read_json(folder / "manifest.json")
        require(entry.get("contract_version",manifest["contract_version"])==manifest["contract_version"],f"Registry source version differs: {reference_id}")
        if manifest["contract_version"] in JSON_CONTRACTS:
            require(entry.get("contract_version")==manifest["contract_version"] and sha256(folder/"audit.json")==entry.get("audit_sha256"),f"Registry audit JSON hash mismatch: {reference_id}")
        require(manifest["id"] == reference_id and manifest["revision"] == entry["revision"], f"Registry identity mismatch: {reference_id}")
        require(manifest["source"]["path"] == f"video/{reference_id}.mp4", f"Invalid registered source path: {reference_id}")
        source = root / manifest["source"]["path"]
        require(source.is_file() and sha256(source) == entry["source_sha256"], f"Registered source changed: {reference_id}")
        cache = root / "data/projections" / f"{reference_id}.json"
        expected = hashlib.sha256((actual_hash + fingerprint).encode()).hexdigest()
        if not full and cache.is_file():
            try:
                cached = read_json(cache)
            except (ValueError, OSError):
                cached = {}
            if not isinstance(cached, dict):
                cached = {}
            # Cache is disposable. It cannot be used if its own payload was edited.
            if (previous_build.get("projections", {}).get(reference_id) == expected and
                    previous_build.get("projection_sha256", {}).get(reference_id) == sha256(cache) and
                    cached.get("schema_version") == "2.5" and cached.get("kind") == "homeku.reference"):
                models[reference_id] = cached["reference"]
                continue
        _, model, _ = validate_folder(folder, root)
        models[reference_id] = model
    return models


def render(root: Path, models):
    taxonomy = read_json(root / "data/taxonomy.json")
    require(isinstance(taxonomy.get("version"), int) and isinstance(taxonomy.get("areas"), dict), "Invalid taxonomy")
    alias_groups = {}
    for group, entries in taxonomy.items():
        if group == "style_relations" or not isinstance(entries, dict):
            continue
        group_aliases = {}
        for canonical, values in sorted(entries.items()):
            require(isinstance(values, list) and all(isinstance(v, str) for v in values), "Invalid alias list")
            for name in [canonical, *values]:
                key = name.casefold()
                require(key not in group_aliases or group_aliases[key] == canonical, f"Ambiguous {group} alias: {name}")
                group_aliases[key] = canonical
        alias_groups[group] = group_aliases
    aliases = alias_groups["areas"]

    def canonical(group, value):
        return alias_groups.get(group, {}).get(value.casefold(), value)

    facet_map = read_json(CODE_ROOT / "sources/fact-facets.json")
    require(facet_map.get("schema_version") == "1.0" and isinstance(facet_map.get("attributes"), dict), "Invalid fact facet map")
    for attr, roles in facet_map["attributes"].items():
        require(isinstance(attr, str) and isinstance(roles, list) and roles and
                all(isinstance(r, str) and r for r in roles) and len(set(roles)) == len(roles), "Invalid facet roles")
    unmapped = {}
    def design_facets(model, shot, pointer):
        result = []
        for j, fact in enumerate(shot["facts"]):
            if model["format_version"] in {"2.3", "2.4", "2.5"}:
                roles = fact["facet_roles"]
                origin = {"json": f"references/{model['id']}/audit.json",
                          "source_pointer": f"/shots/{model['shots'].index(shot)}/facts/{j}/facet_roles", "version": model["format_version"]}
            else:
                roles = facet_map["attributes"].get(fact["attribute"], [])
                origin = {"json": "sources/fact-facets.json",
                          "source_pointer": "/attributes/" + fact["attribute"].replace("~","~0").replace("/","~1"), "version": facet_map["schema_version"]}
                if not roles:
                    unmapped.setdefault(fact["attribute"], []).append({"reference":model["id"], "pointer":pointer+f"/facts/{j}"})
            if roles:
                result.append({**{k:fact[k] for k in ("domain","subject","attribute","value","state","confidence")},
                               "area_ids":fact.get("area_ids", []), "pointer":pointer+f"/facts/{j}",
                               "facet_roles":roles, "role_source":origin})
        return result
    inventories={rid:evidence_inventory(model) for rid,model in models.items()}
    outputs, dependencies = {}, {}
    all_ids = sorted(models)
    count_shots = sum(len(m["shots"]) for m in models.values())

    def emit(path, text, ids):
        outputs[path] = text.rstrip() + "\n"
        dependencies[path] = sorted(set(ids))

    def link(page, path, label):
        destination = os.path.relpath(path, str(Path(page).parent)).replace(os.sep, "/")
        return f"[{cell(label)}]({destination})"

    def source(page, rid, sid):
        return link(page, f"references/{rid}/analysis.md#{sid}", f"{rid} / {sid}")

    def media_link(page, rid, sid):
        path=f"media/{sid}.jpg" if models[rid]["format_version"] in JSON_CONTRACTS else f"media/{sid}/area-overview.jpg"
        return link(page, f"references/{rid}/{path}", "kolase shot" if models[rid]["format_version"] in JSON_CONTRACTS else "gambar area")

    def proof_path(rid, key):
        item=inventories[rid][key]
        name=item["path"]
        if name.startswith("media/"):name=f"references/{rid}/{name}"
        if "bbox" in item:name+="#xywh="+",".join(map(str,item["bbox"]))
        elif name.startswith("video/"):name+=f"#t={item['timestamp_s']}"
        return name

    def proof_link(page,rid,key):
        return link(page,proof_path(rid,key),"bukti")

    def paged(base, title, records, columns, row_fn):
        index_path = f"{base}/README.md"
        index = [f"# {title}", "", f"{len(records)} entri tercatat; rincian dan ketidakpastian mengikuti sumber.", ""]
        ids = []
        for offset in range(0, len(records), PAGE_SIZE):
            chunk = records[offset:offset + PAGE_SIZE]
            path = f"{base}/page-{offset // PAGE_SIZE + 1:03d}.md"
            text = [f"# {title} — {offset // PAGE_SIZE + 1}", "", "| " + " | ".join(columns) + " |",
                    "| " + " | ".join("---" for _ in columns) + " |"]
            for record in chunk:
                text.append("| " + " | ".join(row_fn(path, record)) + " |")
            chunk_ids = [r[0] for r in chunk]
            emit(path, "\n".join(text), chunk_ids)
            index.append("- " + link(index_path, path, f"Halaman {offset // PAGE_SIZE + 1}"))
            ids += chunk_ids
        if not records:
            index.append("Belum ada entri aktif.")
        emit(index_path, "\n".join(index), ids)
        return index_path

    references = ["# Referensi aktif", "", f"{len(models)} referensi; {count_shots} shot. Video sumber yang belum diaudit tidak dihitung.", "",
                  "| Referensi | Judul | Shot |", "| --- | --- | --- |"]
    shots, facts, phases, rooms = [], [], [], defaultdict(list)
    for rid, model in sorted(models.items()):
        references.append(f"| {link('catalogs/references.md', f'references/{rid}/analysis.md', rid)} | {cell(model['title'])} | {len(model['shots'])} |")
        for shot in model["shots"]:
            shots.append((rid, shot))
            room_labels=set(shot["areas"])
            if model["format_version"] in JSON_CONTRACTS:
                room_labels|={f for a in model["areas"] if a["id"] in shot["area_ids"] for f in a["functions"]}
            for area in sorted({aliases.get(a.casefold(), a) for a in room_labels}):
                rooms[area].append((rid, shot))
            facts += [(rid, shot, fact) for fact in shot["facts"]]
            phases += [(rid, shot, phase) for phase in shot["phases"]]
    emit("catalogs/references.md", "\n".join(references), all_ids)
    room_index = ["# Ruang dan fungsi", "", "Label berasal dari timeline. Beberapa fungsi dalam satu shot tetap ditampilkan bersama.", "",
                  "| Label | Referensi | Shot | Rincian |", "| --- | --- | --- | --- |"]
    for area, records in sorted(rooms.items()):
        base = f"catalogs/rooms/{slug(area)}"
        index = paged(base, area, records, ["Sumber", "Fungsi asli", "Posisi dan pandangan", "Peran overview", "Bukti"],
                      lambda p, r: [source(p, r[0], r[1]["shot"]), cell("; ".join(r[1]["areas"])),
                                    cell(r[1]["composition"]["camera_position"] + "; " + r[1]["composition"]["camera_direction"] + "; " + r[1]["composition"]["view_angle"]),
                                    cell(r[1]["composition"].get("overview_role", "panel storyboard") + "; " + r[1]["composition"].get("overview_reason", "Pilihan eksplisit pada audit.json")), media_link(p, r[0], r[1]["shot"])])
        room_index.append(f"| {cell(area)} | {len({r[0] for r in records})} | {len(records)} | {link('catalogs/rooms/README.md', index, 'Buka')} |")
    emit("catalogs/rooms/README.md", "\n".join(room_index), all_ids)

    domains = defaultdict(list)
    for record in facts:
        domains[record[2]["domain"]].append(record)
    domain_index = ["# Desain, arsitektur dan lingkungan", "", "Seluruh domain eksplisit dipertahankan, termasuk label baru dan klaim nonpositif.", ""]
    for domain, records in sorted(domains.items()):
        index = paged(f"catalogs/design/{slug(domain)}", domain, records,
                      ["Sumber / fakta", "Subjek", "Atribut", "Nilai tercatat", "Status", "Confidence", "Bukti"],
                      lambda p, r: [source(p, r[0], r[1]["shot"]) + " / " + cell(r[2]["id"]),
                                    cell(r[2]["subject"]+(" ["+", ".join(r[2]["area_ids"])+"]" if "area_ids" in r[2] else "")), cell(r[2]["attribute"]), cell(r[2]["value"]), cell(r[2]["state"]), cell(r[2]["confidence"]),
                                    "; ".join(proof_link(p, r[0], v) for v in r[2]["evidence"]) or "—"])
        domain_index.append("- " + link("catalogs/design/README.md", index, domain))
    emit("catalogs/design/README.md", "\n".join(domain_index), all_ids)

    paged("catalogs/composition", "Posisi kamera dan komposisi", shots,
          ["Sumber", "Posisi / arah / sudut", "Ketinggian / tilt", "Foreground / kedalaman", "Reveal", "Awal → akhir", "Overview / kecocokan gerak"],
          lambda p, r: [source(p, r[0], r[1]["shot"]), cell("; ".join(r[1]["composition"][k] for k in ("camera_position", "camera_direction", "view_angle"))),
                        cell("; ".join(r[1]["composition"][k] for k in ("camera_height", "camera_tilt"))),
                        cell("; ".join(r[1]["composition"][k] for k in ("foreground", "depth"))), cell(r[1]["composition"]["reveal"]),
                        cell(r[1]["composition"]["start_composition"] + " → " + r[1]["composition"]["end_composition"]),
                        media_link(p, r[0], r[1]["shot"]) + "; " + cell(r[1]["composition"].get("overview_role", "panel storyboard") + "; " + r[1]["composition"]["motion_compatibility"])])
    paged("catalogs/camera", "Gerakan dan ritme kamera", phases,
          ["Sumber / fase", "Interval (s)", "Ringkasan shot", "Komponen fase", "Jangkar", "Tempo / perubahan", "Dasar", "Confidence / batas", "Bukti"],
          lambda p, r: [source(p, r[0], r[1]["shot"]) + " / " + cell(r[2]["phase"]), cell(f"{r[2]['start_s']}–{r[2]['end_s']}"),
                        cell(r[1]["camera_summary"]), cell(r[2]["components"]), cell(r[2]["anchor"]),
                        cell(r[2]["tempo"] + "; " + r[2]["speed_change"]), cell(r[2]["basis"]),
                        cell(r[2]["confidence"] + "; " + r[2]["uncertainty"]),
                        "; ".join(proof_link(p, r[0], v) for v in r[2]["evidence"])])

    comparisons = defaultdict(list)
    for record in facts:
        fact = record[2]
        comparisons[(fact["domain"], fact["subject"], fact["attribute"])].append(record)
    knowledge = ["# Knowledge berbasis audit", "", f"Sumber: {len(models)} referensi, {count_shots} shot aktif.", "",
                 "Perbandingan berikut menyalin fakta eksplisit. Status uncertain/not-visible/not-present/unknown tetap terpisah dari observed.", "",
                 "Hitungan adalah kemunculan pada laporan shot, bukan jumlah rumah independen atau bukti penyebab virality. Label yang tidak tercatat tidak dianggap absen.", ""]
    topics = []
    for key, records in sorted(comparisons.items()):
        title = " / ".join(key)
        # Summaries count unique reference/shot pairs, never repeated fact rows.
        denominator = len({(r[0], r[1]["shot"]) for r in records})
        variants = defaultdict(list)
        for record in records:
            variants[(record[2]["state"], record[2]["value"])].append(record)
        # Each variant may have several sources: keep all rows, bounded into pages.
        expanded = []
        for (state, value), items in sorted(variants.items()):
            refs = len({r[0] for r in items})
            occurrences = len({(r[0], r[1]["shot"]) for r in items})
            for rid, shot, fact in items:
                expanded.append((rid, shot, fact, refs, occurrences, denominator))
        index = paged(f"knowledge/comparisons/{slug(title)}", title, expanded,
                      ["Nilai", "Status", "Referensi", "Shot / denominator tercatat", "Sumber / fakta", "Confidence"],
                      lambda p, r: [cell(r[2]["value"]), cell(r[2]["state"]), str(r[3]), f"{r[4]} / {r[5]}",
                                    source(p, r[0], r[1]["shot"]) + " / " + cell(r[2]["id"]), cell(r[2]["confidence"])])
        json_base = f"knowledge/comparisons/{slug(title)}"
        json_pages = []
        for offset in range(0, len(expanded), PAGE_SIZE):
            json_path = f"{json_base}/page-{offset // PAGE_SIZE + 1:03d}.json"
            chunk = expanded[offset:offset + PAGE_SIZE]
            rows = [{"reference": r[0], "shot": r[1]["shot"], "fact": r[2], "reference_count": r[3],
                     "shot_count": r[4], "denominator": r[5],
                     "source": f"references/{r[0]}/analysis.md#{r[1]['shot']}",
                     "json": f"data/projections/{r[0]}.json",
                     "evidence": [proof_path(r[0],v) for v in r[2]["evidence"]]} for r in chunk]
            emit(json_path, dumps({"schema_version": "1.0", "kind": "homeku.fact-comparisons", "claims": rows}), [r[0] for r in chunk])
            json_pages.append(json_path)
        emit(f"{json_base}/index.json", dumps({"schema_version": "1.0", "attribute": list(key), "denominator": denominator, "pages": json_pages}), [r[0] for r in records])
        topics.append((records[0][0], key, denominator, index))
    paged("knowledge/topics", "Daftar perbandingan", topics,
          ["Domain", "Subjek", "Atribut", "Shot yang mencatat atribut", "Rincian"],
          lambda p, r: [cell(r[1][0]), cell(r[1][1]), cell(r[1][2]), str(r[2]), link(p, r[3], "Buka perbandingan")])
    emit("knowledge/topics/index.json", dumps({"schema_version": "1.0", "kind": "homeku.knowledge-topics",
                                               "topics": [{"attribute": list(key), "denominator": denom,
                                                           "json": path.removesuffix("README.md") + "index.json"}
                                                          for _, key, denom, path in topics]}), all_ids)
    # A topic's denominator can depend on any source, not just its first example.
    for path in list(dependencies):
        if path.startswith("knowledge/topics/"):
            dependencies[path] = all_ids
    knowledge.append("[Daftar perbandingan menurut domain, subjek dan atribut](topics/README.md)")
    if not comparisons:
        knowledge.append("Belum ada audit aktif. Tidak ada pengetahuan baru yang disimpulkan dari arsip.")
    emit("catalogs/README.md", "# Katalog HOMEKU\n\n" + f"{len(models)} referensi aktif; {count_shots} shot.\n\n" +
         "\n".join(f"- [{label}]({target})" for label, target in [("Semua referensi", "references.md"), ("Ruang dan fungsi", "rooms/README.md"),
                      ("Desain, arsitektur dan lingkungan", "design/README.md"), ("Posisi kamera dan komposisi", "composition/README.md"),
                      ("Gerakan dan ritme", "camera/README.md"), ("Knowledge dan perbandingan", "../knowledge/README.md")]), all_ids)
    # Curated general principles are published verbatim; no archived audit facts.
    principles = read_json(CODE_ROOT / "sources/design-principles.json")
    require(principles.get("schema_version") == "1.0" and isinstance(principles.get("principles"), list), "Invalid curated principles")
    require(len({p["id"] for p in principles["principles"]}) == len(principles["principles"]), "Duplicate principle IDs")
    principle_lines = ["# Prinsip desain terkurasi", "", "Prinsip umum, bukan pengamatan video atau keputusan konsep baru.", ""]
    for item in principles["principles"]:
        require(item["claim_type"] == "design-principle", "General principles must remain distinct from audit facts")
        principle_lines += [f"## {item['title']}", "", item["guidance"], "", "Batas: " + item["limitations"], ""]
    emit("knowledge/principles.md", "\n".join(principle_lines), [])
    emit("knowledge/principles.json", dumps(principles), [])
    knowledge += ["", "[Prinsip desain umum terkurasi](principles.md) · [Data prinsip untuk AI](principles.json)"]
    emit("knowledge/README.md", "\n".join(knowledge), all_ids)

    dna_records = [(rid, claim) for rid, model in sorted(models.items()) for claim in model.get("profile", [])]
    paged("catalogs/dna", "Profil DNA, gaya dan skala", dna_records,
          ["Sumber", "Aspek", "Nilai", "Status", "Confidence", "Bukti"],
          lambda p, r: [link(p, f"references/{r[0]}/analysis.md#profil-dna", r[0] + " / " + r[1]["id"]),
                        cell(r[1]["aspect"]), cell(r[1]["value"]), cell(r[1]["state"]), cell(r[1]["confidence"]),
                        "; ".join(proof_link(p, r[0], v) for v in r[1]["evidence"]) or "—"])
    outputs["catalogs/README.md"] += "- [Profil DNA, gaya dan skala](dna/README.md)\n"

    fingerprint = generator_fingerprint(root)
    projection_fingerprints, projection_hashes, search = {}, {}, []
    for rid, model in sorted(models.items()):
        md_path = f"references/{rid}/analysis.md"
        json_path = f"data/projections/{rid}.json"
        inventory=inventories[rid]
        def proof_ids(paths):
            return list(paths)
        audit_path=f"references/{rid}/audit.json" if model["format_version"] in JSON_CONTRACTS else None
        pointers = {"/reference": {"md": md_path, "manifest": f"references/{rid}/manifest.json", "json": audit_path, "source_pointer":""}}
        for i, claim in enumerate(model.get("profile", [])):
            pointers[f"/reference/profile/{i}"] = {"md": md_path + "#profil-dna", "json":audit_path,"source_pointer":f"/profile/{i}","claim_id": claim["id"], "evidence_ids": proof_ids(claim["evidence"])}
        if audit_path:
            for section in ("identity","size","areas","limitations","timeline_notes"):
                pointers[f"/reference/{section}"]={"md":md_path,"json":audit_path,"source_pointer":f"/{section}"}
        if model["format_version"] in OVERVIEW_CONTRACTS:
            pointers["/reference/camera_pattern"]={"md":md_path,"json":audit_path,"source_pointer":"/shots", "derivation":"one depth pattern per shot"}
        indexed_shots = []
        for i, shot in enumerate(model["shots"]):
            pointer = f"/reference/shots/{i}"
            shot_md = md_path + "#" + shot["shot"]
            pointers[pointer] = {"md": shot_md,"json":audit_path,"source_pointer":f"/shots/{i}", "interval_s": [shot["start_s"], shot["end_s"]]}
            for group in ("facts", "phases"):
                for j, claim in enumerate(shot[group]):
                    pointers[f"{pointer}/{group}/{j}"] = {"md": shot_md,"json":audit_path,"source_pointer":f"/shots/{i}/{group}/{j}", "claim_id": claim.get("id", claim.get("phase")), "evidence_ids": proof_ids(claim["evidence"])}
            if audit_path:
                for section in ("design","composition","route","area_relations","tempo_profile","panels","overviews","camera_simple","journey_dna"):
                    pointers[f"{pointer}/{section}"]={"md":shot_md,"json":audit_path,"source_pointer":f"/shots/{i}/{section}"}
            if model["format_version"] in OVERVIEW_CONTRACTS:
                pointers[f"{pointer}/camera_pattern"]={"md":shot_md,"json":audit_path,"source_pointer":f"/shots/{i}/phases", "derivation":"depth_direction sequence", "evidence_ids":list(dict.fromkeys(key for phase in shot["phases"] for key in phase["evidence"]))}
                for j,overview in enumerate(shot["overviews"]):
                    pointers[f"{pointer}/overviews/{j}/composition_summary"]={"md":md_path,"json":audit_path,"source_pointer":f"/shots/{i}/overviews/{j}/composition_summary","evidence_ids":[overview["id"]]}
            if model["format_version"] in {"2.2", "2.3", "2.4", "2.5"}:
                for j, design in enumerate(shot["design"]):
                    for category, coverage in design["fact_coverage"].items():
                        pointers[f"{pointer}/design/{j}/fact_coverage/{category}"] = {
                            "md": shot_md, "json": audit_path,
                            "source_pointer": f"/shots/{i}/design/{j}/fact_coverage/{category}",
                            "evidence_ids": list(dict.fromkeys(key for fact in shot["facts"]
                                if fact["id"] in coverage["fact_ids"] for key in fact["evidence"]))}
                for j, phase in enumerate(shot["phases"]):
                    for k, observation in enumerate(phase["motion_observations"]):
                        pointers[f"{pointer}/phases/{j}/motion_observations/{k}"] = {
                            "md": shot_md, "json": audit_path,
                            "source_pointer": f"/shots/{i}/phases/{j}/motion_observations/{k}",
                            "evidence_ids": list(observation["evidence"])}
            if model["format_version"] in {"2.3", "2.4", "2.5"}:
                for j, phase in enumerate(shot["phases"]):
                    for axis, check in phase["camera_checks"].items():
                        key = f"{pointer}/phases/{j}/camera_checks/{axis}"
                        pointers[key] = {"md":shot_md, "json":audit_path,
                            "source_pointer":f"/shots/{i}/phases/{j}/camera_checks/{axis}", "evidence_ids":list(check["evidence"])}
                    for k, obs in enumerate(phase["motion_observations"]):
                        if obs["scale_measurement"]:
                            measurement = obs["scale_measurement"]
                            pointers[f"{pointer}/phases/{j}/motion_observations/{k}/scale_measurement"] = {
                                "md":shot_md, "json":audit_path,
                                "source_pointer":f"/shots/{i}/phases/{j}/motion_observations/{k}/scale_measurement",
                                "evidence_ids":[measurement["start_evidence"],measurement["end_evidence"]]}
                for j, fact in enumerate(shot["facts"]):
                    pointers[f"{pointer}/facts/{j}/facet_roles"] = {"md":shot_md,"json":audit_path,
                        "source_pointer":f"/shots/{i}/facts/{j}/facet_roles"}
            is_v2=model["format_version"] in JSON_CONTRACTS
            labels=list(shot["areas"])
            if is_v2:
                labels=sorted(set(labels)|{f for a in model["areas"] if a["id"] in shot["area_ids"] for f in a["functions"]})
            indexed_shots.append({"shot": shot["shot"], "areas": labels,
                                  "areas_canonical": sorted({canonical("areas", a) for a in labels}),
                                  "multi_area": len(shot["area_ids"])>1 if is_v2 else None,
                                  "route": [next(a["label"] for a in model["areas"] if a["id"]==r["area_id"]) for r in shot["route"]] if is_v2 else [],
                                  "continuity":shot["continuity"],
                                  "view_angle": shot["composition"]["view_angle"],
                                  "view_angle_canonical": canonical("view_angles", shot["composition"]["view_angle"]),
                                  "camera": shot["camera_summary"],
                                  "movements": sorted({canonical("movements", c["movement"] if c["movement"] != "other" else c["raw"])
                                                       for p in shot["phases"] for c in p["components_parsed"]}),
                                  "camera_qualifiers": sorted({q for p in shot["phases"] for c in p["components_parsed"] for q in c["qualifiers"]}),
                                  "tempos": sorted({t["tempo"] for t in shot.get("tempo_profile",[])}|{p["tempo"] for p in shot["phases"]}),
                                  "design_facets": design_facets(model, shot, pointer),
                                  "path": shot_md, "json_pointer": pointer,
                                  "overview": f"references/{rid}/media/overview.jpg" if model["format_version"]in OVERVIEW_CONTRACTS else f"references/{rid}/media/storyboard.jpg" if is_v2 else f"references/{rid}/media/{shot['shot']}/area-overview.jpg",
                                  "overview_selection_ids": [p["id"] for p in shot["overviews"]] if is_v2 else [],
                                  "collage": f"references/{rid}/media/{shot['shot']}.jpg" if is_v2 else f"references/{rid}/media/{shot['shot']}/area-overview.jpg",
                                  "storyboard": f"references/{rid}/media/storyboard.jpg",
                                  "camera_pattern": shot.get("camera_pattern")})
        for i, relation in enumerate(model["relations"]):
            pointers[f"/reference/relations/{i}"] = {"md": md_path if audit_path else md_path+"#hubungan-antarshot","json":audit_path,"source_pointer":f"/relations/{i}","evidence_ids":proof_ids(relation["evidence"])}
        reader = {"schema_version": "2.5", "kind": "homeku.reference", "reference": model,
                  "paths": {"analysis": md_path, "manifest": f"references/{rid}/manifest.json", "source": model["source"]["path"],"audit":audit_path},
                  "provenance": pointers}
        # Inventory is shared once; no full media objects on every fact/phase pointer.
        reader["evidence_inventory"]=inventory
        validate_reader(reader, "reference-reader-v2-5.schema.json")
        fp = hashlib.sha256((model["content_sha256"] + fingerprint).encode()).hexdigest()
        projection_fingerprints[rid] = fp
        emit(json_path, dumps(reader), [rid])
        projection_hashes[rid] = hashlib.sha256(outputs[json_path].encode()).hexdigest()
        facets = [{**{k: c[k] for k in ("id", "aspect", "value", "state", "confidence")},
                   "canonical": canonical("styles" if c["aspect"] in {"primary-style", "style-influence", "interior-style"}
                                          else "scales" if c["aspect"] == "apparent-scale" else c["aspect"], c["value"]),
                   "pointer": f"/reference/profile/{i}"} for i, c in enumerate(model.get("profile", []))]
        search.append({"id": rid, "title": model["title"], "revision": model["revision"], "json": json_path,
                       "camera_pattern":model.get("camera_pattern"), "format_version":model["format_version"],"floor_area_m2":{k:model["size"]["floor_area_m2"][k] for k in ("min","max")} if model["format_version"] in JSON_CONTRACTS else None,
                       "style_relations":[{k:r[k] for k in ("from","to","relation","state","confidence")} for r in model.get("identity",{}).get("style_relations",[])],
                       "profile_available": bool(model.get("profile")), "profile_facets": facets, "shots": indexed_shots})
    index = {"schema_version": "2.5", "kind": "homeku.search-index", "taxonomy": "data/taxonomy.json",
             "principles": "knowledge/principles.json", "knowledge": "knowledge/topics/index.json", "references": search}
    validate_reader(index, "search-index-v2-5.schema.json")
    emit("data/search-index.json", dumps(index), all_ids)
    emit("data/dependencies.json", dumps({"generator_fingerprint": fingerprint,
                                         "unmapped_fact_attributes": unmapped,
                                         "source_files": ["sources/fact-facets.json", "data/taxonomy.json", "sources/design-principles.json", "docs/template-analysis-v2.md", "tools/assets/"],
                                         "outputs": dependencies.copy()}), all_ids)
    emit("data/build.json", dumps({"generator_fingerprint": fingerprint, "projections": projection_fingerprints,
                                  "projection_sha256": projection_hashes,
                                  "outputs": {path: hashlib.sha256(value.encode()).hexdigest() for path, value in sorted(outputs.items())}}), all_ids)
    return outputs


def validate_reader(value, schema_name):
    from jsonschema import Draft202012Validator
    validator = Draft202012Validator(read_json(CODE_ROOT / "docs/contracts" / schema_name))
    errors = sorted(validator.iter_errors(value), key=lambda e: str(list(e.path)))
    require(not errors, f"Invalid {schema_name}: {errors[0].message}" if errors else "")
