"""Validate project structure and production rules; never infer visual truth.

Run: python validate_project.py /path/to/project.json
Required packages are listed in requirements.txt. No network access is used.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
from io import BytesIO
import json
from pathlib import Path, PurePosixPath
from urllib.parse import quote

from jsonschema import Draft202012Validator
from PIL import Image
import yaml

SKILL_ROOT = Path(__file__).resolve().parents[1]
RULES = yaml.safe_load((SKILL_ROOT / "references/production-rules.yaml").read_text())
SCHEMA = json.loads((SKILL_ROOT / "assets/project.schema.json").read_text())
Draft202012Validator.check_schema(SCHEMA)
STRUCTURE = Draft202012Validator(SCHEMA)
LIMITS = [
    "Validasi struktural dan berkas tidak membuktikan kebenaran kutipan referensi atau geometri rumah.",
    "Status review/approval adalah catatan keputusan; validator tidak menggantikan melihat gambar atau mendengar audio.",
    "Sumber diakses oleh workflow web/konektor; validator ini tidak membuat permintaan jaringan.",
]


def _schema_errors(project):
    return sorted(
        ("/" + "/".join(map(str, error.absolute_path)) + ": " + error.message)
        for error in STRUCTURE.iter_errors(project)
    )


def _index(items, key, errors):
    result = {}
    for item in items:
        value = item[key]
        if value in result:
            errors.append(f"{key} berulang: {value}")
        result[value] = item
    return result


def _source_url_matches(item, knowledge):
    version = knowledge["commit"] or knowledge["ref"]
    if not version:
        return False
    repository = RULES["knowledge_repository"]
    owner_repo = repository.removeprefix("https://github.com/")
    version = quote(version, safe="")
    path = f"references/{item['reference_id']}/analysis.yaml"
    return item["analysis_url"] in {
        f"{repository}/blob/{version}/{path}",
        f"https://raw.githubusercontent.com/{owner_repo}/{version}/{path}",
    }


def _asset_path(value, project_root):
    relative = PurePosixPath(value)
    if relative.is_absolute() or ".." in relative.parts or "\\" in value or "\x00" in value or not relative.parts:
        raise ValueError("Path aset harus relatif dan tetap di dalam folder proyek.")
    if project_root is None:
        return None
    root = Path(project_root).resolve()
    resolved = (root / relative).resolve()
    if not resolved.is_relative_to(root):
        raise ValueError("Path/symlink aset keluar dari folder proyek.")
    return resolved


def _check_file(asset, path, errors):
    prefix = f"assets/{asset['asset_id']}"
    if path is None or not path.is_file():
        errors.append(prefix + ": file asli tidak tersedia di folder proyek.")
        return
    try:
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != asset["sha256"]:
            errors.append(prefix + ": SHA-256 file berbeda dari catatan aset.")
        with Image.open(BytesIO(raw)) as image:
            image.load()
            if image.format != RULES["frames"]["format"]:
                errors.append(prefix + ": format file harus PNG.")
            if image.size != (asset["width"], asset["height"]):
                errors.append(prefix + ": dimensi aktual berbeda dari catatan aset.")
            if asset["role"] in RULES["frames"]["roles"]:
                x, y = RULES["frames"]["aspect_ratio"]
                if image.width * y != image.height * x:
                    errors.append(prefix + ": frame aktual harus tepat 9:16.")
    except (OSError, ValueError, Image.DecompressionBombError) as error:
        errors.append(prefix + ": gambar tidak dapat dibuka: " + str(error))


def validate_project(project, project_root=None):
    errors = _schema_errors(project)
    if errors:
        return {"valid": False, "errors": errors, "limits": LIMITS}
    stage = project["stage"]
    if stage not in RULES["stages"]:
        return {"valid": False, "errors": ["stage tidak dikenal: " + stage], "limits": LIMITS}
    rank = RULES["stages"].index(stage)
    revision = project["revision"]
    if project["rules_version"] != RULES["rules_version"]:
        errors.append("rules_version tidak cocok dengan aturan yang dibundel.")
    if project["audio"] != RULES["audio"]:
        errors.append("audio harus ambient halus tanpa musik, narasi, dialog atau efek dramatis.")
    knowledge = project["knowledge"]
    if knowledge["repository_url"] != RULES["knowledge_repository"]:
        errors.append("knowledge.repository_url harus menunjuk pustaka HOMEKU yang ditetapkan.")
    evidence = _index(knowledge["evidence"], "evidence_id", errors)
    allowed_areas = set(RULES["canonical_areas"])
    for item in evidence.values():
        if not _source_url_matches(item, knowledge):
            errors.append(item["evidence_id"] + ": URL anotasi tidak cocok dengan repo, versi atau ID referensi.")
        if not set(item["covered_areas"]) <= allowed_areas:
            errors.append(item["evidence_id"] + ": sumber mencatat area di luar kontrak saat ini.")
    if rank >= 1:
        for label, text in (("brief", project["brief"]), ("concept.title", project["concept"]["title"]),
                            ("concept.summary", project["concept"]["summary"])):
            if not text.strip():
                errors.append(label + " wajib diisi pada tahap konsep dan berikutnya.")
        if knowledge["route"] is None or not (knowledge["commit"] or knowledge["ref"]):
            errors.append("Jalur akses dan versi sumber wajib dicatat.")
        if not any(item["access_status"] == "read" for item in evidence.values()):
            errors.append("Minimal satu bukti sumber benar-benar dibaca diperlukan.")
    for kind, approval in project["approvals"].items():
        if approval is not None and approval["revision"] != revision:
            errors.append("approval/" + kind + ": keputusan berasal dari revisi proyek lain.")
    if rank >= 2:
        if not project["shots"]:
            errors.append("Rancangan shot wajib berisi minimal satu shot.")
        for key, value in project["design"].items():
            if not value:
                errors.append("design/" + key + " wajib diisi sebelum rancangan shot selesai.")
            elif isinstance(value, str) and not value.strip():
                errors.append("design/" + key + " tidak boleh hanya whitespace.")
    if rank >= 3:
        for kind in ("concept", "shot_plan"):
            if project["approvals"][kind] is None:
                errors.append("approval/" + kind + " diperlukan sebelum produksi visual.")
    if rank >= 4 and project["approvals"]["visual"] is None:
        errors.append("approval/visual diperlukan untuk visual final.")

    shots = _index(project["shots"], "shot_id", errors)
    assets = _index(project["assets"], "asset_id", errors)
    paths = {}
    for asset in assets.values():
        ident = asset["asset_id"]
        if asset["shot_id"] not in shots:
            errors.append(ident + ": aset menunjuk shot yang tidak ada.")
        if asset["revision"] != revision:
            errors.append(ident + ": versi aset tidak cocok dengan revisi proyek.")
        try:
            path = _asset_path(asset["path"], project_root)
            path_key = str(path) if path is not None else asset["path"]
            if path_key in paths:
                errors.append(ident + ": file dipakai oleh dua catatan aset berbeda.")
            paths[path_key] = ident
        except ValueError as error:
            errors.append(ident + ": " + str(error))
            path = None
        if asset["reviewed"] and (asset["review_origin"] is None or not asset["review_note"].strip()):
            errors.append(ident + ": review memerlukan asal dan catatan pemeriksaan.")
        if asset["role"] in RULES["frames"]["roles"]:
            x, y = RULES["frames"]["aspect_ratio"]
            if asset["width"] * y != asset["height"] * x:
                errors.append(ident + ": dimensi frame pada catatan harus tepat 9:16.")
        if rank >= 4:
            _check_file(asset, path, errors)

    counts = Counter()
    selected_frames = set()
    for index, shot in enumerate(project["shots"], 1):
        ident = shot["shot_id"]
        if ident != f"shot-{index:02d}":
            errors.append(ident + ": urutan ID shot harus berurutan mulai shot-01.")
        areas = set(shot["covered_areas"])
        counts.update(areas)
        kind = RULES["shot_kinds"].get(shot["kind"])
        if kind is None:
            errors.append(ident + ": jenis shot tidak dikenal.")
        else:
            if shot["duration_s"] != kind["duration_s"]:
                errors.append(ident + ": durasi tidak sesuai jenis shot.")
            if areas not in [set(group) for group in kind["coverage_sets"]]:
                errors.append(ident + ": cakupan area tidak cocok dengan pola shot yang diizinkan.")
        if not areas <= allowed_areas:
            errors.append(ident + ": area tidak dikenal; jangan mengganti nama bedroom untuk menambah kamar.")
        if not shot["continuous"]:
            errors.append(ident + ": setiap shot wajib kontinu tanpa cut.")
        linked_evidence = []
        for key in shot["evidence_ids"]:
            item = evidence.get(key)
            if item is None or item["access_status"] != "read":
                errors.append(ident + ": bukti sumber tidak ada atau belum dibaca: " + key)
            else:
                linked_evidence.append(item)
        if not any(set(item["covered_areas"]) == areas and
                   item["continuity"] in ("annotated_continuous", "reviewed_continuous")
                   for item in linked_evidence):
            errors.append(ident + ": perlu bukti struktur continuous shot dengan cakupan yang sama.")
        for role in RULES["frames"]["roles"]:
            asset_id = shot["frames"][role]
            if asset_id is None:
                if rank >= 4:
                    errors.append(ident + ": frame " + role + " belum lengkap.")
                continue
            selected_frames.add(asset_id)
            asset = assets.get(asset_id)
            if asset is None or asset["shot_id"] != ident or asset["role"] != role or asset["revision"] != revision:
                errors.append(ident + ": pengikatan frame " + role + " salah shot, peran atau versi.")
            elif rank >= 4 and not asset["reviewed"]:
                errors.append(ident + ": frame " + role + " belum diperiksa secara visual.")
        prompt = shot["prompt"]
        if rank >= 5 and prompt is None:
            errors.append(ident + ": prompt final belum tersedia.")
        if prompt is not None:
            if prompt["revision"] != revision:
                errors.append(ident + ": versi prompt tidak cocok.")
            if prompt["duration_s"] != shot["duration_s"]:
                errors.append(ident + ": durasi prompt tidak cocok.")
            if any(prompt[role + "_asset_id"] != shot["frames"][role] for role in RULES["frames"]["roles"]):
                errors.append(ident + ": prompt memakai pasangan frame yang berbeda.")
            for name, instruction in RULES["prompt_constraints"].items():
                if instruction not in prompt["text"]:
                    errors.append(ident + ": instruksi " + name + " wajib ada dalam prompt.")

    if project["shots"] and RULES["coverage"]["opening_area"] not in project["shots"][0]["covered_areas"]:
        errors.append("Shot pertama harus mengungkap exterior sesuai pola referensi.")
    for area, count in counts.items():
        if count > 1 and not RULES["coverage"]["allow_repeat"]:
            errors.append("Area sudah tercakup dan tidak boleh diulang: " + area)
    sleeping_count = sum(counts[area] for area in RULES["coverage"]["sleeping_areas"])
    if sleeping_count > RULES["coverage"]["max_sleeping_area_count"]:
        errors.append("Maksimal satu area tidur (bedroom/sleeping_loft) yang ditampilkan.")
    if rank >= 4:
        for asset in assets.values():
            if asset["role"] in RULES["frames"]["roles"] and asset["asset_id"] not in selected_frames:
                errors.append(asset["asset_id"] + ": frame tidak dipilih oleh shot final.")
    if project["total_duration_s"] != sum(shot["duration_s"] for shot in project["shots"]):
        errors.append("total_duration_s tidak sama dengan jumlah durasi shot.")
    return {
        "valid": not errors, "stage": stage, "revision": revision,
        "shot_count": len(project["shots"]), "total_duration_s": project["total_duration_s"],
        "errors": sorted(set(errors)), "limits": LIMITS,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    args = parser.parse_args()
    try:
        project = json.loads(args.project.read_text())
        result = validate_project(project, args.project.resolve().parent)
    except (OSError, ValueError) as error:
        parser.exit(2, str(error) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
