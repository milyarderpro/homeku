"""Validate project structure and production rules; never infer visual truth.

Run: python validate_project.py /path/to/project.json
Required packages are listed in requirements.txt. No network access is used.
"""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
import hashlib
from io import BytesIO
import json
import math
from pathlib import Path, PurePosixPath
import re
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
    "Batch serentak, naturalitas, plafon dan sudut aktual video harus dibuktikan dari pelaksanaan/media, bukan JSON.",
]


def _schema_errors(project):
    def leaves(error):
        if error.validator in ("anyOf", "oneOf") and error.context:
            for child in error.context:
                if child.validator == "type" and child.schema.get("type") == "null":
                    continue
                yield from leaves(child)
        else:
            yield "/" + "/".join(map(str, error.absolute_path)) + ": " + error.message
    return sorted(message for error in STRUCTURE.iter_errors(project) for message in leaves(error))


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
    prefix = asset["asset_id"] + ": "
    if path is None or not path.is_file():
        errors.append(prefix + "file asli tidak tersedia.")
        return
    try:
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != asset["sha256"]:
            errors.append(prefix + "SHA-256 berbeda.")
        with Image.open(BytesIO(raw)) as image:
            image.load()
            if getattr(image, "n_frames", 1) != 1:
                errors.append(prefix + "referensi harus satu gambar individual statis.")
            if image.format != asset["format"] or image.format not in RULES["images"]["formats"]:
                errors.append(prefix + "format aktual berbeda atau tidak didukung.")
            if image.size != (asset["width"], asset["height"]):
                errors.append(prefix + "dimensi aktual berbeda.")
    except (OSError, ValueError, Image.DecompressionBombError) as error:
        errors.append(prefix + "gambar tidak dapat dibuka: " + str(error))


def _camera_errors(shot, errors):
    camera, duration = shot["camera"], shot["duration_s"]
    components = camera["components"]
    relation = camera["motion_relationship"]
    prefix = shot["shot_id"] + ": "
    if (relation == "single" and len(components) != 1) or (relation != "single" and len(components) < 2):
        errors.append(prefix + "jumlah komponen tidak cocok dengan hubungan gerak.")
    previous_end = 0
    for item in components:
        values = [item["start_s"], item["duration_s"], item["distance_m"], item["angle_deg"]]
        if any(value is not None and not math.isfinite(value) for value in values):
            errors.append(prefix + "nilai kamera harus finite.")
            continue
        start, length = item["start_s"], item["duration_s"]
        if start + length > duration + 1e-6:
            errors.append(prefix + "gerak melampaui durasi shot.")
        if relation in ("single", "simultaneous"):
            if not math.isclose(start, 0, abs_tol=1e-6) or not math.isclose(length, duration, abs_tol=1e-6):
                errors.append(prefix + "gerak tunggal/bersamaan harus mencakup durasi shot yang sama.")
        elif not math.isclose(start, previous_end, abs_tol=1e-6):
            errors.append(prefix + "fase berurutan harus tersambung tanpa overlap atau jeda tak tercatat.")
        previous_end = start + length
        if item["kind"] in ("pan", "orbit"):
            if item["angle_deg"] is None or item["angle_deg"] < RULES["camera"]["minimum_rotation_deg"]:
                errors.append(prefix + "pan/orbit minimal 12 derajat.")
        if item["kind"] == "translation" and (item["distance_m"] is None or item["distance_m"] <= 0):
            errors.append(prefix + "translasi memerlukan perkiraan jarak positif.")
        if item["kind"] == "tilt" and (item["angle_deg"] is None or item["angle_deg"] <= 0):
            errors.append(prefix + "tilt memerlukan sudut positif.")
    if relation == "sequential" and not math.isclose(previous_end, duration, abs_tol=1e-6):
        errors.append(prefix + "alokasi fase berurutan harus berakhir pada durasi shot.")


def migrate_project(project):
    """Convert a schema-2.0 COPY; never invent composition, approval or merged pixels."""
    legacy = deepcopy(SCHEMA)
    legacy["properties"]["schema_version"]["const"] = "2.0"
    legacy["properties"]["rules_version"]["const"] = "2.0.0"
    for node, key in (
        (legacy["properties"]["design"], "area_specs"),
        (legacy["$defs"]["image"], "composition"),
        (legacy["$defs"]["camera"], "spatial_plan"),
        (legacy["$defs"]["shot"], "reference_choice"),
    ):
        del node["properties"][key]
        node["required"].remove(key)
    if not Draft202012Validator(legacy).is_valid(project):
        raise ValueError("Migrasi memerlukan proyek schema 2.0/rules 2.0.0 yang terstruktur; sumber tidak diubah.")
    converted = deepcopy(project)
    converted.update(schema_version="2.1", rules_version="2.1.0")
    converted["design"]["area_specs"] = []
    for image in converted["image_plan"]:
        image["composition"] = None
        if image["asset_id"] is not None:
            image["status"] = "available"
        elif image["status"] != "failed":
            image["status"] = "planned"
    for asset in converted["assets"]:
        asset.update(reviewed=False, review_origin=None, review_note="")
    for shot in converted["shots"]:
        shot["camera"]["spatial_plan"] = None
        shot["reference_choice"] = None
        shot["prompt"] = None
    prior_visual = converted["approvals"]["visual"]
    converted["approvals"]["visual"] = None
    prior_stage = converted["stage"]
    if RULES["stages"].index(prior_stage) >= 2:
        converted["stage"] = "concept"
    pending = [
        "Lengkapi area_specs, komposisi gambar dan spatial_plan kamera dari rancangan yang sama.",
        "Catat pilihan 1/2 referensi exterior-to-living; living-to-kitchen default satu foto gabungan baru.",
        "Tinjau gambar terhadap aturan baru sebelum visual final; tulis ulang prompt tanpa ID/nama file.",
    ] if converted["shots"] else []
    converted["revision_notes"].append(
        "Migrasi salinan schema 2.0 ke 2.1; tahap asal " + prior_stage +
        ". Brief, sumber, konsep, mode dan keputusan konsep/shot dipertahankan; "
        "komposisi/gerak baru belum diisi, aset lama tidak digabung atau diklaim memenuhi review baru."
    )
    if prior_visual is not None:
        converted["revision_notes"].append("Keputusan visual historis sebelum perbaikan: " +
                                           json.dumps(prior_visual, ensure_ascii=False))
    return {"project": converted, "needs_review": pending, "source_stage": prior_stage}


def _composition_errors(image, errors):
    composition = image["composition"]
    prefix = image["image_id"] + ": "
    if composition is None:
        errors.append(prefix + "komposisi gambar wajib direncanakan.")
        return
    if not math.isfinite(composition["height_m"]):
        errors.append(prefix + "tinggi kamera harus finite.")
    if "exterior" in image["area_ids"] and not composition["full_exterior"]:
        errors.append(prefix + "gambar exterior wajib memuat seluruh rumah dengan tepi aman.")
    if "bedroom" in image["area_ids"]:
        angle = composition["view_angle_deg"]
        low, high = RULES["images"]["bedroom_angle_range_deg"]
        if (composition["subject_view"] != RULES["images"]["bedroom_view"] or angle is None
                or not math.isfinite(angle) or not low <= angle <= high or not composition["bed_diagonal"]):
            errors.append(prefix + "bedroom memerlukan front three-quarter 35–45 derajat terhadap sumbu panjang bed dan bed diagonal.")


def _reference_errors(shot, refs, errors):
    prefix = shot["shot_id"] + ": "
    choice = shot["reference_choice"]
    if choice is None or choice["count"] != len(refs):
        errors.append(prefix + "pilihan jumlah referensi belum tercatat atau tidak cocok.")
    if shot["kind"] == "exterior_to_living" and choice is not None and choice["by"] == "default":
        errors.append(prefix + "exterior-to-living memakai pilihan pengguna/delegasi 1 atau 2 referensi.")
    if shot["kind"] == "living_to_kitchen" and len(refs) > 1 and choice is not None and choice["by"] == "default":
        errors.append(prefix + "referensi tambahan living-to-kitchen perlu pilihan pengguna/delegasi.")
    rule = RULES["shot_kinds"][shot["kind"]]
    if "reference_counts" in rule and len(refs) not in rule["reference_counts"]:
        errors.append(prefix + "shot penghubung menerima 1 atau 2 referensi sesuai rancangan.")
    if any(item is None for item in refs):
        errors.append(prefix + "referensi gambar tidak ada.")
        return
    areas = set(shot["covered_areas"])
    union = set().union(*(set(item["area_ids"]) for item in refs))
    if shot["kind"] == "exterior_to_living":
        valid = bool(union) and union <= areas
        if len(refs) == 2:
            valid = valid and {item["primary_area"] for item in refs} == {"exterior", "living"} and union == areas
    else:
        valid = union == areas and set(rule["required_primary_areas"]) <= {item["primary_area"] for item in refs}
        if shot["kind"] == "living_to_kitchen" and len(refs) == 1:
            valid = valid and {"living", "kitchen"} <= set(refs[0]["area_ids"])
    if not valid:
        errors.append(prefix + "referensi area tidak cocok dengan cakupan/pilihan shot.")


def _prompt_body_errors(shot, images, assets, errors, shot_ids):
    body = "\n".join(shot["prompt"]["sections"].values())
    if "```" in body or "~~~" in body:
        errors.append(shot["shot_id"] + ": badan prompt harus teks siap salin tanpa pagar Markdown.")
    identifiers = set(images) | set(assets) | set(shot_ids)
    filenames = {Path(asset["path"]).name for asset in assets.values()}
    if (any(re.search(r"(?<![A-Za-z0-9_-])" + re.escape(key) + r"(?![A-Za-z0-9_-])",
                      body, re.IGNORECASE) for key in identifiers)
            or any(name.casefold() in body.casefold() for name in filenames)
            or re.search(r"\b[^\s<>]+\.(?:png|jpe?g|webp|gif|json)\b|/mnt/|file://", body, re.IGNORECASE)):
        errors.append(shot["shot_id"] + ": nama file/path/ID internal harus di luar badan prompt video.")
    role = shot["prompt"]["sections"]["REFERENCE IMAGE ROLE"]
    if RULES["prompt_constraints"]["reference_role"] not in role:
        errors.append(shot["shot_id"] + ": peran referensi wajib tegas bukan frame awal/akhir wajib.")


def validate_project(project, project_root=None):
    if isinstance(project, dict) and project.get("schema_version") == "1.0":
        return {"valid": False, "errors": [
            "Proyek V1 (schema 1.0) terdeteksi. Gunakan salinan proyek untuk peninjauan/migrasi V2; "
            "pasangan frame dan persetujuan visual lama tidak otomatis menjadi referensi area R2V."
        ], "limits": LIMITS}
    if isinstance(project, dict) and project.get("schema_version") == "2.0":
        return {"valid": False, "errors": ["Proyek schema 2.0 terdeteksi. Gunakan migrate_project pada salinan, lengkapi komposisi dan tinjau gambar; jangan menimpa sumber."], "limits": LIMITS}
    errors = _schema_errors(project)
    if errors:
        return {"valid": False, "errors": errors, "limits": LIMITS}
    stage, revision = project["stage"], project["revision"]
    rank = RULES["stages"].index(stage)
    ready = stage in ("image_final", "prompt_package")
    knowledge = project["knowledge"]
    if knowledge["repository_url"] != RULES["knowledge_repository"]:
        errors.append("knowledge.repository_url harus menunjuk pustaka HOMEKU.")
    if project["audio"] != RULES["audio"]:
        errors.append("audio harus ambient halus tanpa musik, narasi, dialog atau efek dramatis.")
    evidence = _index(knowledge["evidence"], "evidence_id", errors)
    for item in evidence.values():
        if not set(item["covered_areas"]) <= set(RULES["canonical_areas"]):
            errors.append(item["evidence_id"] + ": bukti mencatat area di luar kontrak.")
        if not _source_url_matches(item, knowledge):
            errors.append(item["evidence_id"] + ": URL anotasi tidak cocok dengan repo, versi atau ID referensi.")
    if rank >= 1:
        if not project["brief"].strip() or not all(value.strip() for value in project["concept"].values()):
            errors.append("brief dan konsep pilihan wajib diisi.")
        if knowledge["route"] is None or not (knowledge["commit"] or knowledge["ref"]):
            errors.append("Jalur akses dan versi sumber wajib dicatat.")
        if not any(item["access_status"] == "read" for item in evidence.values()):
            errors.append("Minimal satu bukti sumber benar-benar dibaca diperlukan.")
    for kind, approval in project["approvals"].items():
        if approval is not None and approval["revision"] != revision:
            errors.append("approval/" + kind + ": keputusan berasal dari revisi lain.")
    if rank >= 2:
        if not project["shots"] or not project["image_plan"]:
            errors.append("Rancangan wajib memuat shot dan rencana gambar area.")
        for key, value in project["design"].items():
            if not value or (isinstance(value, str) and not value.strip()):
                errors.append("design/" + key + " wajib diisi pada rancangan.")
    if rank >= 3:
        if project["image_mode"] is None:
            errors.append("Mode gambar wajib dipilih.")
        for kind in ("concept", "shot_plan"):
            if project["approvals"][kind] is None:
                errors.append("approval/" + kind + " diperlukan sebelum produksi gambar.")
    if stage == "image_prompt_package" and project["image_mode"] != "prompt_to_image":
        errors.append("image_prompt_package hanya untuk mode prompt_to_image.")
    if ready and project["approvals"]["visual"] is None:
        errors.append("approval/visual diperlukan untuk gambar final.")
    batch = project["image_batch"]
    if batch["request_mode"] == "one_by_one" and not (batch["user_instruction"] or "").strip():
        errors.append("Generate satu per satu memerlukan instruksi eksplisit pengguna.")
    if batch["execution"] != "not_started" and not batch["note"].strip():
        errors.append("Pelaksanaan gambar memerlukan catatan dasar yang sebenarnya.")
    if ready and project["image_mode"] == "prompt_to_image" and batch["execution"] not in ("external", "unknown"):
        errors.append("Perolehan gambar eksternal perlu dicatat sebelum final.")
    if ready and project["image_mode"] == "generate_image":
        expected = "parallel" if batch["request_mode"] == "all_at_once" else "sequential"
        if batch["execution"] != expected:
            errors.append("Pelaksanaan batch belum tercatat sesuai permintaan " + batch["request_mode"] + ".")
    images = _index(project["image_plan"], "image_id", errors)
    assets = _index(project["assets"], "asset_id", errors)
    shots = _index(project["shots"], "shot_id", errors)
    if rank >= 2:
        area_specs = _index(project["design"]["area_specs"], "area", errors)
        covered = set().union(*(set(shot["covered_areas"]) for shot in shots.values()))
        if set(area_specs) != covered:
            errors.append("design/area_specs harus menetapkan satu posisi/plafon/lampu untuk setiap area rancangan.")
        for area, spec in area_specs.items():
            if area != "exterior" and not spec["fixtures"]:
                errors.append("design/area_specs/" + area + ": interior wajib mempunyai armatur lampu.")
        for image in images.values():
            _composition_errors(image, errors)
        for shot in shots.values():
            if shot["camera"]["spatial_plan"] is None:
                errors.append(shot["shot_id"] + ": spatial_plan posisi, lintasan dan akhir wajib diisi.")
    paths, hashes = set(), set()
    for asset in assets.values():
        ident = asset["asset_id"]
        image = images.get(asset["image_id"])
        if image is None or image["asset_id"] != ident:
            errors.append(ident + ": aset tidak terikat ke gambar aktif.")
        if asset["revision"] != revision:
            errors.append(ident + ": versi aset tidak cocok.")
        if asset["sha256"] in hashes:
            errors.append(ident + ": file gambar identik tidak boleh menyamar sebagai referensi area lain.")
        hashes.add(asset["sha256"])
        if asset["reviewed"] and (asset["review_origin"] is None or not asset["review_note"].strip()):
            errors.append(ident + ": review memerlukan asal dan catatan nyata.")
        try:
            path = _asset_path(asset["path"], project_root)
            key = str(path) if path is not None else asset["path"]
            if key in paths:
                errors.append(ident + ": file dipakai oleh dua aset.")
            paths.add(key)
            if project_root is not None or ready:
                _check_file(asset, path, errors)
        except (OSError, ValueError) as error:
            errors.append(ident + ": " + str(error))
    for image in images.values():
        ident = image["image_id"]
        if image["primary_area"] not in image["area_ids"]:
            errors.append(ident + ": area tujuan harus tercakup pada area_ids.")
        if image["revision"] != revision:
            errors.append(ident + ": versi prompt/gambar tidak cocok.")
        if rank >= 3 and (not image["prompt"].strip() or re.search(r"\{\{[^{}]+\}\}", image["prompt"])):
            errors.append(ident + ": prompt gambar belum lengkap.")
        if image["status"] == "failed":
            if not (image["error"] or "").strip() or image["asset_id"] is not None:
                errors.append(ident + ": kegagalan harus mencatat error dan tidak mengklaim aset.")
        elif image["error"] is not None:
            errors.append(ident + ": error hanya dicatat pada status failed.")
        if image["status"] in ("planned", "prompt_ready", "failed") and image["asset_id"] is not None:
            errors.append(ident + ": status gambar belum sesuai dengan keberadaan aset.")
        asset = assets.get(image["asset_id"])
        if image["status"] in ("available", "reviewed") and asset is None:
            errors.append(ident + ": file aset belum tersedia.")
        if asset is not None and asset["image_id"] != ident:
            errors.append(ident + ": aset salah gambar.")
        if image["status"] == "reviewed" and (asset is None or not asset["reviewed"]):
            errors.append(ident + ": review gambar belum lengkap.")
        if ready and (image["status"] != "reviewed" or asset is None or not asset["reviewed"]):
            errors.append(ident + ": gambar final memerlukan aset dan review aktual.")
        used_by = {shot["shot_id"] for shot in shots.values() if ident in shot["reference_image_ids"]}
        if set(image["shot_ids"]) != used_by:
            errors.append(ident + ": peta shot pemakai tidak cocok atau gambar tidak digunakan.")
    counts = Counter()
    for index, shot in enumerate(project["shots"], 1):
        ident, areas = shot["shot_id"], set(shot["covered_areas"])
        if ident != f"shot-{index:02d}":
            errors.append(ident + ": urutan ID shot harus dimulai shot-01 dan berurutan.")
        counts.update(areas)
        rule = RULES["shot_kinds"][shot["kind"]]
        if shot["duration_s"] != rule["duration_s"]:
            errors.append(ident + ": durasi tidak sesuai jenis shot.")
        if areas not in [set(group) for group in rule["coverage_sets"]]:
            errors.append(ident + ": cakupan tidak sesuai pola sumber yang diizinkan.")
        if not shot["continuous"]:
            errors.append(ident + ": setiap shot wajib kontinu tanpa cut.")
        linked = [evidence.get(key) for key in shot["evidence_ids"]]
        if any(item is None or item["access_status"] != "read" for item in linked):
            errors.append(ident + ": bukti sumber tidak ada atau belum dibaca.")
        if not any(item and item["access_status"] == "read"
                   and set(item["covered_areas"]) == areas
                   and item["continuity"] in ("annotated_continuous", "reviewed_continuous") for item in linked):
            errors.append(ident + ": perlu bukti continuous shot dengan cakupan yang sama.")
        refs = [images.get(key) for key in shot["reference_image_ids"]]
        if rank >= 2:
            _reference_errors(shot, refs, errors)
        elif any(item is None for item in refs):
            errors.append(ident + ": referensi gambar tidak ada.")
        _camera_errors(shot, errors)
        prompt = shot["prompt"]
        if stage == "prompt_package" and prompt is None:
            errors.append(ident + ": prompt R2V belum tersedia.")
        if prompt is not None:
            if prompt["revision"] != revision or prompt["duration_s"] != shot["duration_s"]:
                errors.append(ident + ": revisi/durasi prompt tidak cocok.")
            if prompt["reference_image_ids"] != shot["reference_image_ids"]:
                errors.append(ident + ": prompt memakai referensi berbeda.")
            if any(re.search(r"\{\{[^{}]+\}\}", value) for value in prompt["sections"].values()):
                errors.append(ident + ": prompt masih berisi penanda template.")
            _prompt_body_errors(shot, images, assets, errors, shots)
            ending_rules = prompt["sections"]["CONTINUITY AND AUDIO RULES"]
            for instruction in (RULES["prompt_constraints"][key] for key in ("continuous", "audio")):
                if instruction not in ending_rules:
                    errors.append(ident + ": instruksi continuous/ambient wajib ada pada aturan prompt.")
    if project["shots"] and "exterior" not in project["shots"][0]["covered_areas"]:
        errors.append("Shot pertama harus mengungkap exterior.")
    for area, count in counts.items():
        if count > 1:
            errors.append("Area sudah tercakup dan tidak boleh diulang: " + area)
    if sum(counts[area] for area in RULES["coverage"]["sleeping_areas"]) > 1:
        errors.append("Maksimal satu area tidur (bedroom/sleeping_loft).")
    if project["total_duration_s"] != sum(shot["duration_s"] for shot in project["shots"]):
        errors.append("total_duration_s tidak sama dengan penjumlahan shot.")
    return {
        "valid": not errors, "stage": stage, "revision": revision,
        "shot_count": len(shots), "image_count": len(images),
        "available_image_count": sum(item["asset_id"] in assets for item in images.values()),
        "reviewed_image_count": sum(item["status"] == "reviewed" for item in images.values()),
        "total_duration_s": project["total_duration_s"], "batch_execution": batch["execution"],
        "errors": sorted(set(errors)), "limits": LIMITS,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("--migrate-to", type=Path, help="Convert schema 2.0 to a new checkpoint, never the source.")
    parser.add_argument("--fallback-root", type=Path)
    args = parser.parse_args()
    try:
        project = json.loads(args.project.read_text(encoding="utf-8"))
        if args.migrate_to is not None:
            if args.migrate_to.resolve() == args.project.resolve():
                raise ValueError("Tujuan migrasi harus berbeda dari proyek sumber.")
            from save_project import save_project
            report = migrate_project(project)
            result = save_project(report["project"], args.migrate_to,
                                  source_root=args.project.resolve().parent, fallback_root=args.fallback_root)
            result.update(needs_review=report["needs_review"], source_stage=report["source_stage"])
            print(json.dumps(result, ensure_ascii=False, indent=2))
            raise SystemExit(0 if result["saved"] else 1)
        result = validate_project(project, args.project.resolve().parent)
    except (OSError, ValueError) as error:
        parser.exit(2, str(error) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
