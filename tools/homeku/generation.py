"""Source-backed catalogs and comparisons, with bounded pages and explicit states."""

from __future__ import annotations

import hashlib
import os
from collections import defaultdict
from pathlib import Path

from . import GENERATOR_VERSION
from .common import cell, content_hash, dumps, read_json, require, sha256, slug
from .validation import CODE_ROOT, SCHEMA, validate_folder

PAGE_SIZE = 40


def generator_fingerprint(root: Path):
    inputs = [(p.name, sha256(p)) for p in sorted((CODE_ROOT / "tools/homeku").glob("*.py"))]
    inputs += [("schema", sha256(SCHEMA)), ("taxonomy", sha256(root / "data/taxonomy.json")), ("version", GENERATOR_VERSION)]
    return hashlib.sha256(dumps(inputs).encode()).hexdigest()


def load_models(root: Path, registry, full=False):
    """Reuse projections only when every reference byte and source still match."""
    models = {}
    for reference_id, entry in sorted(registry["references"].items()):
        folder = root / "references" / reference_id
        require(folder.is_dir() and not folder.is_symlink(), f"Missing/symlinked registered reference: {reference_id}")
        actual_hash = content_hash(folder)
        require(actual_hash == entry["content_sha256"], f"Unapproved edits to references/{reference_id}; submit a new ZIP revision")
        require(sha256(folder / "analysis.md") == entry["analysis_sha256"] and sha256(folder / "manifest.json") == entry["manifest_sha256"],
                f"Registry document hash mismatch: {reference_id}")
        manifest = read_json(folder / "manifest.json")
        require(manifest["id"] == reference_id and manifest["revision"] == entry["revision"], f"Registry identity mismatch: {reference_id}")
        require(manifest["source"]["path"] == f"video/{reference_id}.mp4", f"Invalid registered source path: {reference_id}")
        source = root / manifest["source"]["path"]
        require(source.is_file() and sha256(source) == entry["source_sha256"], f"Registered source changed: {reference_id}")
        cache = root / "data/projections" / f"{reference_id}.json"
        expected = hashlib.sha256((actual_hash + generator_fingerprint(root)).encode()).hexdigest()
        if not full and cache.is_file():
            try:
                cached = read_json(cache)
            except (ValueError, OSError):
                cached = {}
            if not isinstance(cached, dict):
                cached = {}
            # Cache is disposable. It cannot be used if its own payload was edited.
            if cached.get("fingerprint") == expected:
                payload = cached.get("model")
                digest = hashlib.sha256(dumps(payload).encode()).hexdigest()
                if digest == cached.get("model_sha256"):
                    models[reference_id] = payload
                    continue
        _, model, _ = validate_folder(folder, root)
        models[reference_id] = model
    return models


def render(root: Path, models):
    taxonomy = read_json(root / "data/taxonomy.json")
    require(isinstance(taxonomy.get("version"), int) and isinstance(taxonomy.get("areas"), dict), "Invalid taxonomy")
    aliases = {}
    for canonical, values in sorted(taxonomy["areas"].items()):
        require(isinstance(values, list) and all(isinstance(v, str) for v in values), "Invalid area alias list")
        for name in [canonical, *values]:
            key = name.casefold()
            require(key not in aliases or aliases[key] == canonical, f"Ambiguous area alias: {name}")
            aliases[key] = canonical
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
        return link(page, f"references/{rid}/media/{sid}/area-overview.jpg", "gambar area")

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
            for area in sorted({aliases.get(a.casefold(), a) for a in shot["areas"]}):
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
                                    cell(r[1]["composition"]["overview_role"] + "; " + r[1]["composition"]["overview_reason"]), media_link(p, r[0], r[1]["shot"])])
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
                                    cell(r[2]["subject"]), cell(r[2]["attribute"]), cell(r[2]["value"]), cell(r[2]["state"]), cell(r[2]["confidence"]),
                                    "; ".join(link(p, f"references/{r[0]}/{v}", "frame") for v in r[2]["evidence"]) or "—"])
        domain_index.append("- " + link("catalogs/design/README.md", index, domain))
    emit("catalogs/design/README.md", "\n".join(domain_index), all_ids)

    paged("catalogs/composition", "Posisi kamera dan komposisi", shots,
          ["Sumber", "Posisi / arah / sudut", "Ketinggian / tilt", "Foreground / kedalaman", "Reveal", "Awal → akhir", "Overview / kecocokan gerak"],
          lambda p, r: [source(p, r[0], r[1]["shot"]), cell("; ".join(r[1]["composition"][k] for k in ("camera_position", "camera_direction", "view_angle"))),
                        cell("; ".join(r[1]["composition"][k] for k in ("camera_height", "camera_tilt"))),
                        cell("; ".join(r[1]["composition"][k] for k in ("foreground", "depth"))), cell(r[1]["composition"]["reveal"]),
                        cell(r[1]["composition"]["start_composition"] + " → " + r[1]["composition"]["end_composition"]),
                        media_link(p, r[0], r[1]["shot"]) + "; " + cell(r[1]["composition"]["overview_role"] + "; " + r[1]["composition"]["motion_compatibility"])])
    paged("catalogs/camera", "Gerakan dan ritme kamera", phases,
          ["Sumber / fase", "Interval (s)", "Ringkasan shot", "Komponen fase", "Jangkar", "Tempo / perubahan", "Dasar", "Confidence / batas", "Bukti"],
          lambda p, r: [source(p, r[0], r[1]["shot"]) + " / " + cell(r[2]["phase"]), cell(f"{r[2]['start_s']}–{r[2]['end_s']}"),
                        cell(r[1]["camera_summary"]), cell(r[2]["components"]), cell(r[2]["anchor"]),
                        cell(r[2]["tempo"] + "; " + r[2]["speed_change"]), cell(r[2]["basis"]),
                        cell(r[2]["confidence"] + "; " + r[2]["uncertainty"]),
                        "; ".join(link(p, f"references/{r[0]}/{v}", "frame") for v in r[2]["evidence"])])

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
        topics.append((records[0][0], key, denominator, index))
    paged("knowledge/topics", "Daftar perbandingan", topics,
          ["Domain", "Subjek", "Atribut", "Shot yang mencatat atribut", "Rincian"],
          lambda p, r: [cell(r[1][0]), cell(r[1][1]), cell(r[1][2]), str(r[2]), link(p, r[3], "Buka perbandingan")])
    # A topic's denominator can depend on any source, not just its first example.
    for path in list(dependencies):
        if path.startswith("knowledge/topics/"):
            dependencies[path] = all_ids
    knowledge.append("[Daftar perbandingan menurut domain, subjek dan atribut](topics/README.md)")
    if not comparisons:
        knowledge.append("Belum ada audit aktif. Tidak ada pengetahuan baru yang disimpulkan dari arsip.")
    emit("knowledge/README.md", "\n".join(knowledge), all_ids)
    emit("catalogs/README.md", "# Katalog HOMEKU\n\n" + f"{len(models)} referensi aktif; {count_shots} shot.\n\n" +
         "\n".join(f"- [{label}]({target})" for label, target in [("Semua referensi", "references.md"), ("Ruang dan fungsi", "rooms/README.md"),
                      ("Desain, arsitektur dan lingkungan", "design/README.md"), ("Posisi kamera dan komposisi", "composition/README.md"),
                      ("Gerakan dan ritme", "camera/README.md"), ("Knowledge dan perbandingan", "../knowledge/README.md")]), all_ids)
    fingerprint = generator_fingerprint(root)
    projection_fingerprints = {}
    for rid, model in sorted(models.items()):
        model_hash = hashlib.sha256(dumps(model).encode()).hexdigest()
        fp = hashlib.sha256((model["content_sha256"] + fingerprint).encode()).hexdigest()
        projection_fingerprints[rid] = fp
        emit(f"data/projections/{rid}.json", dumps({"fingerprint": fp, "model_sha256": model_hash, "model": model}), [rid])
    search = [{"id": rid, "title": model["title"], "revision": model["revision"],
               "shots": [{"shot": s["shot"], "areas": s["areas"], "view_angle": s["composition"]["view_angle"],
                          "camera": s["camera_summary"], "tempos": sorted({p["tempo"] for p in s["phases"]}),
                          "path": f"references/{rid}/analysis.md#{s['shot']}"} for s in model["shots"]]}
              for rid, model in sorted(models.items())]
    emit("data/search-index.json", dumps({"references": search}), all_ids)
    emit("data/dependencies.json", dumps({"generator_fingerprint": fingerprint, "outputs": dependencies.copy()}), all_ids)
    emit("data/build.json", dumps({"generator_fingerprint": fingerprint, "projections": projection_fingerprints,
                                  "outputs": {path: hashlib.sha256(value.encode()).hexdigest() for path, value in sorted(outputs.items())}}), all_ids)
    return outputs
