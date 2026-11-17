"""Build/check a published knowledge snapshot independently of the growing archive.

--publish RELEASE creates an explicit immutable release from selected sources.
--write rebuilds the current release without promoting new references.
Readers need only GitHub web/file access; these commands are maintenance tools.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from functools import lru_cache
from datetime import date as CalendarDate
import hashlib
import json
from pathlib import Path
import re

from jsonschema import Draft202012Validator
import yaml

from verify_source_integrity import sha256_file, verify_sources

ROOT = Path(__file__).resolve().parents[1]
RELEASE = Path("knowledge/release.json")
TAXONOMY_VERSION = "1.0.1"
SCHEMA_ROOT = Path(__file__).resolve().parents[1] / "schemas/knowledge.schema.json"
BT = chr(96)
ALL_DIMENSIONS = {
    "style_family", "style_influence", "room_type", "configuration", "roof_form",
    "opening", "material_appearance", "lighting", "camera", "mood", "scale",
}
IDENT = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]*\Z")


def dump(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


@lru_cache(maxsize=None)
def contract_validator(name):
    definitions = json.loads(SCHEMA_ROOT.read_text())["$defs"]
    schema = {"$schema": "https://json-schema.org/draft/2020-12/schema",
              "$defs": definitions, "$ref": f"#/$defs/{name}"}
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def validate_contract(name, value):
    contract_validator(name).validate(value)
    if name == "release":
        CalendarDate.fromisoformat(value["published_on"])
    if name == "review":
        CalendarDate.fromisoformat(value["reviewed_on"])
    if name == "aggregate" and value["numerator"] > value["denominator"]:
        raise ValueError("Aggregate numerator exceeds denominator")


def read_archives(root=ROOT):
    result = {}
    for path in sorted((Path(root) / "references").glob("*/analysis.yaml")):
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        ident = path.parent.name
        if doc["video"]["id"] != ident or doc["video"]["shot_count"] != len(doc["shots"]):
            raise ValueError(f"Invalid archive identity/count: {ident}")
        result[ident] = doc
    if not result:
        raise ValueError("No reference analyses")
    return result


def source_binding(root, ident, doc):
    if not IDENT.fullmatch(ident):
        raise ValueError(f"Unsafe reference ID: {ident}")
    filename = doc["video"]["filename"]
    if Path(filename).name != filename:
        raise ValueError(f"Unsafe source filename: {ident}")
    analysis = Path("references") / ident / "analysis.yaml"
    video = Path("video") / filename
    record = {"reference_id": ident, "analysis_path": analysis.as_posix(),
              "analysis_sha256": sha256_file(root / analysis),
              "source_path": video.as_posix(), "source_sha256": sha256_file(root / video)}
    validate_contract("source", record)
    return record


def load_release(root=ROOT, *, validate_sources=True):
    root = Path(root)
    release = json.loads((root / RELEASE).read_text())
    validate_contract("release", release)
    ids = [s["reference_id"] for s in release["references"]]
    if len(ids) != len(set(ids)) or ids != sorted(ids):
        raise ValueError("Release reference IDs must be unique and sorted")
    if release["reference_count"] != len(ids):
        raise ValueError("Release reference count mismatch")
    taxonomy_path = root / f"knowledge/taxonomy/v{release['taxonomy_version']}.json"
    if sha256_file(taxonomy_path) != release["taxonomy_sha256"]:
        raise ValueError("Published taxonomy changed; publish a new taxonomy version/release")
    archived = root / "knowledge/releases" / (release["release_id"] + ".json")
    if not archived.is_file() or json.loads(archived.read_text()) != release:
        raise ValueError("Current release differs from immutable release manifest")
    if validate_sources:
        refs = read_archives(root)
        for source in release["references"]:
            ident = source["reference_id"]
            if ident not in refs:
                raise ValueError(f"Published reference removed: {ident}")
            if source_binding(root, ident, refs[ident]) != source:
                raise ValueError(f"Published source/annotation changed: {ident}; explicit new release required")
        selected = [refs[i] for i in ids]
        if release["shot_count"] != sum(len(d["shots"]) for d in selected):
            raise ValueError("Release shot count mismatch")
        if release["visual_detail_count"] != detail_count(selected):
            raise ValueError("Release visual detail count mismatch")
    return release


def published_references(root=ROOT):
    root = Path(root)
    release = load_release(root)
    refs = read_archives(root)
    return {s["reference_id"]: refs[s["reference_id"]] for s in release["references"]}


def detail_count(documents):
    return sum(len(items) for d in documents for s in d["shots"]
               for items in s.get("visible_details", {}).values())


def normalize_text(value):
    return re.sub(r"\s+", " ", re.sub(r"[_-]+", " ", value.casefold())).strip()


class Taxonomy:
    def __init__(self, path):
        self.path = Path(path)
        self.data = json.loads(self.path.read_text())
        self.version = self.data["version"]
        if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", self.version) or self.path.name != f"v{self.version}.json":
            raise ValueError("Taxonomy version must match its versioned filename")
        self.sha256 = sha256_file(self.path)
        self.concepts = {c["id"]: c for c in self.data["concepts"]}
        if len(self.concepts) != len(self.data["concepts"]):
            raise ValueError("Duplicate taxonomy concept ID")
        self.aliases = []
        owners = {}
        for concept in self.concepts.values():
            if concept["dimension"] not in ALL_DIMENSIONS:
                raise ValueError("Unknown taxonomy dimension")
            if not concept["label"].get("en") or not concept["label"].get("id"):
                raise ValueError("English and Indonesian labels required")
            for alias in concept["aliases"]:
                normalized = normalize_text(alias)
                if not normalized:
                    raise ValueError("Empty taxonomy alias")
                key = (concept["dimension"], normalized)
                if key in owners and owners[key] != concept["id"]:
                    raise ValueError(f"Ambiguous taxonomy alias: {alias}")
                owners[key] = concept["id"]
                self.aliases.append((concept, normalized, re.compile(
                    r"(?<!\w)" + re.escape(normalized) + r"(?!\w)")))

    def map(self, raw, dimensions, *, presence=True):
        base = {"raw": raw, "presence": presence, "state": "unmapped",
                "coverage": "none", "matches": [], "candidates": [],
                "qualifiers": [], "reason": "No scoped alias; awaiting AI mapping review"}
        if not presence:
            return {**base, "state": "missing", "reason": "Field absent from source"}
        if raw == []:
            return {**base, "state": "empty", "reason": "Empty source list; does not prove physical absence"}
        if raw is None:
            return {**base, "state": "unknown", "reason": "Source explicitly records null"}
        if not isinstance(raw, str):
            raise ValueError("Normalized source values must be strings, null or empty lists")
        text = normalize_text(raw)
        special = {"unknown": "unknown", "not visible": "not_visible",
                   "not applicable": "not_applicable", "n a": "not_applicable"}
        if text in special:
            return {**base, "state": special[text], "reason": "Explicit source state"}
        matches, exact = {}, False
        for concept, alias, pattern in self.aliases:
            if concept["dimension"] in dimensions and pattern.search(text):
                matches[concept["id"]] = {"concept_id": concept["id"],
                                         "dimension": concept["dimension"]}
                exact |= text == alias
        values = [matches[k] for k in sorted(matches)]
        if re.search(r"\b(or|atau|possible|possibly|uncertain|unidentified|without|no|not|tanpa|tidak)\b", text):
            return {**base, "state": "ambiguous", "candidates": values,
                    "reason": "Alternative, uncertainty or negation in source; no positive concept asserted"}
        qualifiers = [q for q in ("slow", "slight", "subtle", "gentle", "gradual", "smooth")
                      if re.search(r"\b" + q + r"\b", text)] if "camera" in dimensions else []
        if values:
            return {**base, "state": "mapped", "coverage": "exact" if exact else "partial",
                    "matches": values, "qualifiers": qualifiers,
                    "reason": "Scoped lexical alias; not independent visual verification"}
        return base


def source_terms(doc):
    """Enumerate source values without replacing any original label."""
    roots = {
        "architecture/primary_style": ["style_family", "style_influence"],
        "architecture/secondary_influences": ["style_family", "style_influence"],
        "architecture/interior_style": ["style_influence", "material_appearance"],
        "architecture/exterior_features": ["roof_form", "opening", "material_appearance"],
        "architecture/building_scale/perceived_size": ["scale"],
        "visual_style/lighting": ["lighting"], "visual_style/mood": ["mood"],
    }

    def emit(value, path, dims, shot=None, presence=True):
        if isinstance(value, list) and value:
            for i, item in enumerate(value):
                yield path + "/" + str(i), item, dims, shot, True
        else:
            yield path, value, dims, shot, presence

    for path, dims in roots.items():
        current, present = doc, True
        for piece in path.split("/"):
            if not isinstance(current, dict) or piece not in current:
                current, present = None, False
                break
            current = current[piece]
        yield from emit(current, "/" + path, dims, presence=present)
    for index, shot in enumerate(doc["shots"]):
        prefix = f"/shots/{index}"
        for field, dims in (("scene", ["room_type", "configuration"]),
                            ("lighting", ["lighting"])):
            yield from emit(shot.get(field), prefix + "/" + field, dims, shot["id"], field in shot)
        yield from emit(shot.get("camera", {}).get("movements"),
                        prefix + "/camera/movements", ["camera"], shot["id"],
                        "movements" in shot.get("camera", {}))
        for category in ("architectural", "furniture_and_props", "environment"):
            details = shot.get("visible_details", {})
            yield from emit(details.get(category), prefix + "/visible_details/" + category,
                            ["roof_form", "opening", "material_appearance"], shot["id"],
                            category in details)


def normalize_reference(doc, source, taxonomy):
    records = []
    for pointer, raw, dimensions, shot, presence in source_terms(doc):
        record = taxonomy.map(raw, dimensions, presence=presence)
        key = hashlib.sha256((pointer + "\0" + json.dumps(raw, ensure_ascii=False)).encode()).hexdigest()[:16]
        records.append({"id": source["reference_id"] + "-" + key, "field_path": pointer,
                        "shot_id": shot, **record})
    result = {"schema_version": "1.0", "taxonomy_version": taxonomy.version,
              "taxonomy_sha256": taxonomy.sha256, "source": source, "mappings": records}
    validate_contract("normalization", result)
    return result


def resolve_pointer(doc, pointer):
    value = doc
    for part in pointer.lstrip("/").split("/"):
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def concept_ids(normalized):
    return {m["concept_id"] for row in normalized["mappings"] for m in row["matches"]}


def search_examples(query, root=ROOT):
    """Optional maintenance prototype; reading Markdown never requires this."""
    root = Path(root)
    release = load_release(root)
    taxonomy = Taxonomy(root / f"knowledge/taxonomy/v{release['taxonomy_version']}.json")
    requested = {m["concept_id"] for m in taxonomy.map(query, ALL_DIMENSIONS)["matches"]}
    if not requested:
        return []
    found = []
    for source in release["references"]:
        path = root / f"knowledge/enrichment/{source['reference_id']}.json"
        normalized = json.loads(path.read_text())
        if normalized["source"] != source or normalized["taxonomy_sha256"] != taxonomy.sha256:
            raise ValueError("Stale search normalization; rebuild the published release")
        if requested <= concept_ids(normalized):
            found.append(source["reference_id"])
    return found


def md(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def profile(doc, normalized, taxonomy, release_id):
    source = normalized["source"]
    ident = source["reference_id"]
    link = f"../../references/{ident}"
    scale = doc["architecture"]["building_scale"]
    by_dimension = defaultdict(set)
    for cid in concept_ids(normalized):
        concept = taxonomy.concepts[cid]
        by_dimension[concept["dimension"]].add(cid)
    lines = [f"# {ident} — source design profile", "",
             f"Published knowledge: {BT}{release_id}{BT}. Source: [{ident} analysis]({link}/analysis.yaml).",
             f"Repository path: {BT}{source['analysis_path']}{BT}.",
             "", "[All profiles](README.md) · [Core knowledge](../ai-knowledge.md) · [Vocabulary](../taxonomy/README.md)", "",
             f"**Recorded style:** {md(doc['architecture']['primary_style'])}. "
             f"**Perceived scale:** {md(scale['perceived_size'])}; {md(scale['vertical_scale'])}.",
             "", "## Readable source summary", "",
             "This text restates saved labels; it does not independently verify their physical meaning.",
             "The recorded design is " + md(doc["architecture"]["primary_style"].replace("_", " ")) +
             ", with " + md(scale["vertical_scale"].replace("_", " ")) + ".",
             "Interior: " + "; ".join(md(x.replace("_", " ")) for x in doc["architecture"].get("interior_style", [])) + ".",
             "", "## Source signature", "",
             "- Exterior: " + "; ".join(md(x) for x in doc["architecture"].get("exterior_features", [])),
             "- Palette: " + "; ".join(md(c["name"]) + " " + str(c.get("hex_approx")) for c in doc["visual_style"].get("dominant_colors", [])),
             "- Lighting: " + "; ".join(md(x) for x in doc["visual_style"].get("lighting", [])),
             "- Mood: " + "; ".join(md(x) for x in doc["visual_style"].get("mood", [])),
             "", "## Normalized vocabulary", "",
             "These are scoped lexical mappings of the labels above and below, not a new visual review. Materials describe appearance.",
             "", "| Dimension | English / Indonesian concepts |", "| --- | --- |"]
    for dimension, ids in sorted(by_dimension.items()):
        labels = [f"{taxonomy.concepts[i]['label']['en']} / {taxonomy.concepts[i]['label']['id']}" for i in sorted(ids)]
        lines.append(f"| {dimension} | {md('; '.join(labels))} |")
    lines += ["", "## Shot evidence", "",
              "| Shot | Recorded scene | Recorded camera labels | Source frame |",
              "| --- | --- | --- | --- |"]
    for shot in doc["shots"]:
        lines.append(f"| {shot['id']} | {md(shot.get('scene'))} | "
                     f"{md(' + '.join(shot.get('camera', {}).get('movements', [])))} | "
                     f"[{shot['id']}]({link}/{shot['id']}.jpg) |")
    states = Counter(r["state"] for r in normalized["mappings"])
    lines += ["", "## Limits", "",
              "Separate cuts do not establish room adjacency or a measured floorplan. Camera labels are pixel-based interpretations.",
              "Confidence qualifies claims about this source; all saved references remain usable for new creative decisions.",
              "- Recorded uncertainties: " + "; ".join(md(x) for x in doc["analysis_quality"].get("uncertainties", [])),
              "- Mapping states: " + ", ".join(f"{k}: {v}" for k, v in sorted(states.items())),
              "", f"[Full report]({link}/analysis.md) · [Storyboard]({link}/storyboard.jpg)", "",
              "<details>", "<summary>Source binding and normalization — supporting metadata</summary>", "",
              f"Annotation SHA-256: {BT}{source['analysis_sha256']}{BT}. Source SHA-256: {BT}{source['source_sha256']}{BT}.",
              f"[Structured mappings](../enrichment/{ident}.json). These hashes identify revisions, not visual certainty.",
              "", "</details>", ""]
    return "\n".join(lines)


def render_outputs(root, release):
    root = Path(root)
    refs = read_archives(root)
    taxonomy = Taxonomy(root / f"knowledge/taxonomy/v{release['taxonomy_version']}.json")
    outputs, normalized_all = {}, {}
    issues = {}
    for source in release["references"]:
        ident = source["reference_id"]
        normalized = normalize_reference(refs[ident], source, taxonomy)
        normalized_all[ident] = normalized
        outputs[f"knowledge/enrichment/{ident}.json"] = dump(normalized)
        outputs[f"knowledge/reference-profiles/{ident}.md"] = profile(refs[ident], normalized, taxonomy, release["release_id"])
        evidence_path = root / f"knowledge/design-evidence/{ident}.json"
        if evidence_path.is_file():
            evidence = json.loads(evidence_path.read_text())
            state = "Source-bound enrichment" if evidence.get("source") == source else "Older source revision; review/rebuild required"
            outputs[f"knowledge/reference-profiles/{ident}.md"] += (
                f"\n## Design relationships and temporal evidence\n\n"
                f"{state}: [readable evidence](../design-evidence/{ident}.md) · "
                f"[structured records](../design-evidence/{ident}.json). "
                "The evidence page states the actual review scope; available samples are not automatically reviewed.\n")
        for row in normalized["mappings"]:
            if row["state"] in ("unmapped", "ambiguous"):
                key = (row["state"], json.dumps(row["raw"], ensure_ascii=False))
                item = issues.setdefault(key, {"state": row["state"], "raw": row["raw"],
                                              "reason": row["reason"], "occurrences": []})
                item["occurrences"].append({"reference_id": ident, "field_path": row["field_path"]})
    issue_list = [issues[k] for k in sorted(issues)]
    outputs["knowledge/taxonomy/mapping-issues.json"] = dump({
        "schema_version": "1.0", "release_id": release["release_id"], "items": issue_list})
    states = Counter(r["state"] for n in normalized_all.values() for r in n["mappings"])
    outputs["knowledge/taxonomy/normalization-report.md"] = "\n".join([
        "# Vocabulary coverage", "", f"Release: {BT}{release['release_id']}{BT}; taxonomy {BT}{taxonomy.version}{BT}.",
        "", "| State | Source values |", "| --- | ---: |",
        *[f"| {state} | {count} |" for state, count in sorted(states.items())], "",
        f"{len(issue_list)} distinct ambiguous/unmapped labels are retained in [mapping-issues.json](mapping-issues.json).",
        "Partial lexical coverage does not mean every attribute was normalized. No source label is discarded or rewritten.",
        "Empty lists mean no items recorded, not proof that an object is physically absent.", ""])
    glossary = ["# HOMEKU bilingual vocabulary", "",
                f"Version {BT}{taxonomy.version}{BT}; [versioned dictionary](v{taxonomy.version}.json).",
                "Normalization decomposes source labels by dimension; labels are preserved and uncertain matches remain candidates.",
                "The dictionary is a design/search aid, not a verified material identification or geographic classification.", "",
                "[Coverage](normalization-report.md) · [Unresolved labels](mapping-issues.json) · [Core knowledge](../ai-knowledge.md)", ""]
    for dimension in sorted(ALL_DIMENSIONS):
        glossary += [f"## {dimension}", "", "| ID | English | Indonesian | Aliases |", "| --- | --- | --- | --- |"]
        for concept in taxonomy.concepts.values():
            if concept["dimension"] == dimension:
                glossary.append("| " + " | ".join(md(x) for x in (
                    concept["id"], concept["label"]["en"], concept["label"]["id"], ", ".join(concept["aliases"]))) + " |")
        glossary.append("")
    glossary += ["## Missing and uncertain values", "",
                 "- unknown: explicitly unknown/null in the source.",
                 "- not_visible: explicitly labeled not visible; not a claim of physical absence.",
                 "- not_applicable: explicitly labeled inapplicable.",
                 "- missing: field absent; empty: explicitly empty list.",
                 "- ambiguous: alternatives/negation remain unresolved candidates; unmapped: no scoped alias.",
                 "- mapped: one or more lexical concepts; coverage is exact or partial.", ""]
    outputs["knowledge/taxonomy/README.md"] = "\n".join(glossary)
    index = ["# Published reference profiles", "",
             f"Release {BT}{release['release_id']}{BT}: {release['reference_count']} sources / {release['shot_count']} shots.",
             "One file per source. Archive additions do not silently join this published snapshot.",
             "", "[Core knowledge](../ai-knowledge.md) · [Directories](../directories/README.md) · [Archive inventory](../source-manifest.json)", "",
             "| Reference | Recorded style | Scale |", "| --- | --- | --- |"]
    for ident in normalized_all:
        doc = refs[ident]
        index.append(f"| [{ident}]({ident}.md) | {md(doc['architecture']['primary_style'])} | {md(doc['architecture']['building_scale']['perceived_size'])} |")
    outputs["knowledge/reference-profiles/README.md"] = "\n".join(index + [""])
    dirs = ["# Direktori contoh desain", "", f"Snapshot: {BT}{release['release_id']}{BT}.",
            "Pilih dimensi yang relevan, lalu buka beberapa profil yang sesuai. Tidak perlu membuka semua daftar.",
            "Hasil pengelompokan mengikuti label sumber dan alias; satu referensi dapat berada di beberapa kelompok.", "",
            "[Pengetahuan inti](../ai-knowledge.md) · [Peta bacaan](../README.md) · [Semua profil](../reference-profiles/README.md)", "",
            "| Kebutuhan | Direktori |", "| --- | --- |",
            "| Bentuk dan identitas rumah | [Keluarga gaya](style_family.md), [pengaruh gaya](style_influence.md), [atap](roof_form.md), [bukaan](opening.md), [skala](scale.md) |",
            "| Fungsi dan susunan ruang | [Jenis ruang](room_type.md), [konfigurasi](configuration.md) |",
            "| Tampilan dan suasana | [Material appearance](material_appearance.md), [cahaya](lighting.md), [mood](mood.md) |",
            "| Pengungkapan pandangan | [Bahasa gerak kamera](camera.md) |", "",
            "Alias Indonesia/Inggris tersedia dalam [kamus](../taxonomy/README.md). Kategori skala merupakan kesan visual; material dan kamera tetap interpretasi sumber.", ""]
    for dimension in sorted(ALL_DIMENSIONS):
        lines = [f"# Directory: {dimension}", "", "[All directories](README.md) · [Vocabulary](../taxonomy/README.md)", ""]
        for cid, concept in taxonomy.concepts.items():
            if concept["dimension"] != dimension:
                continue
            found = [ident for ident, n in normalized_all.items() if cid in concept_ids(n)]
            if found:
                lines += [f"## {concept['label']['en']} / {concept['label']['id']}", "",
                          f"Concept ID: {BT}{cid}{BT}.",
                          ", ".join(f"[{i}](../reference-profiles/{i}.md)" for i in found), ""]
        outputs[f"knowledge/directories/{dimension}.md"] = "\n".join(lines)
    outputs["knowledge/directories/README.md"] = "\n".join(dirs).rstrip() + "\n"
    from refresh_design_catalog import render_catalog
    outputs["knowledge/reference-catalog.md"] = render_catalog(
        {ident: refs[ident] for ident in normalized_all}, release_id=release["release_id"])
    return outputs


def is_managed_artifact(path):
    """Only generated artifacts may be removed; preserve unrelated notes."""
    if path.suffix == ".md":
        return path.read_text(encoding="utf-8").startswith(
            f"# {path.stem} — source design profile\n")
    if path.suffix == ".json":
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (ValueError, UnicodeDecodeError):
            return False
        return (isinstance(value, dict) and value.get("schema_version") == "1.0"
                and isinstance(value.get("source"), dict)
                and value["source"].get("reference_id") == path.stem
                and isinstance(value.get("mappings"), list))
    return False


def check_library(root=ROOT):
    root = Path(root)
    release = load_release(root)
    outputs = render_outputs(root, release)
    stale = [path for path, text in outputs.items()
             if not (root / path).is_file() or (root / path).read_text(encoding="utf-8") != text]
    published_ids = {s["reference_id"] for s in release["references"]}
    for path in (root / "knowledge/enrichment").glob("*.json"):
        if path.stem not in published_ids and is_managed_artifact(path):
            stale.append(str(path.relative_to(root)))
    for path in (root / "knowledge/reference-profiles").glob("*.md"):
        if path.stem not in published_ids and is_managed_artifact(path):
            stale.append(str(path.relative_to(root)))
    if stale:
        raise ValueError("Stale generated knowledge: " + ", ".join(stale[:12]))
    return release


def write_outputs(root, release):
    root = Path(root)
    outputs = render_outputs(root, release)
    # Only files in these managed namespaces are eligible for stale-file removal.
    ids = {s["reference_id"] for s in release["references"]}
    for namespace, suffix in (("enrichment", ".json"), ("reference-profiles", ".md")):
        for path in (root / "knowledge" / namespace).glob("*" + suffix):
            if path.stem not in ids and is_managed_artifact(path):
                path.unlink()
    for relative, text in outputs.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


def publish_release(root, release_id, date, reference_ids=None, taxonomy_version=TAXONOMY_VERSION):
    root = Path(root)
    if not IDENT.fullmatch(release_id):
        raise ValueError("Unsafe release ID")
    verify_sources(root)
    refs = read_archives(root)
    ids = sorted(refs if reference_ids is None else reference_ids)
    if not ids or len(ids) != len(set(ids)) or any(i not in refs for i in ids):
        raise ValueError("Invalid release selection")
    taxonomy = Taxonomy(root / f"knowledge/taxonomy/v{taxonomy_version}.json")
    if (root / RELEASE).exists():
        previous = json.loads((root / RELEASE).read_text())
        if previous["taxonomy_version"] == taxonomy.version and previous["taxonomy_sha256"] != taxonomy.sha256:
            raise ValueError("Published taxonomy is immutable; create a new version")
    release = {"schema_version": "1.0", "release_id": release_id, "published_on": date,
               "taxonomy_version": taxonomy.version, "taxonomy_sha256": taxonomy.sha256,
               "reference_count": len(ids), "shot_count": sum(len(refs[i]["shots"]) for i in ids),
               "visual_detail_count": detail_count([refs[i] for i in ids]),
               "references": [source_binding(root, i, refs[i]) for i in ids]}
    validate_contract("release", release)
    # Precompute/validate all artifacts before touching the current release.
    render_outputs(root, release)
    archived = root / "knowledge/releases" / (release_id + ".json")
    if archived.exists() and json.loads(archived.read_text()) != release:
        raise ValueError("Release IDs are immutable; use a new release ID")
    archived.parent.mkdir(parents=True, exist_ok=True)
    archived.write_text(dump(release), encoding="utf-8")
    (root / RELEASE).write_text(dump(release), encoding="utf-8")
    write_outputs(root, release)
    return release


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--check", action="store_true")
    group.add_argument("--write", action="store_true")
    group.add_argument("--publish", metavar="RELEASE")
    parser.add_argument("--date", help="Explicit YYYY-MM-DD release date")
    parser.add_argument("--references", nargs="+", help="IDs to publish; default all archives")
    parser.add_argument("--taxonomy-version", default=TAXONOMY_VERSION)
    args = parser.parse_args()
    if args.publish:
        if not args.date:
            parser.error("--publish requires --date")
        release = publish_release(args.root, args.publish, args.date, args.references, args.taxonomy_version)
    elif args.write:
        release = load_release(args.root)
        write_outputs(args.root, release)
    else:
        release = check_library(args.root)
    print(f"Knowledge verified: {release['release_id']}; {release['reference_count']} references / "
          f"{release['shot_count']} shots. Archive growth is independent of publication.")


if __name__ == "__main__":
    main()
