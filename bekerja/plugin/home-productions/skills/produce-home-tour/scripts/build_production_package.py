"""Export an image-prompt package or a final R2V package without inventing data.

The exporter copies listed originals and renders authored sections. It does not
generate images/video, infer batch execution, or grant review/approval.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path, PurePosixPath
from shutil import copyfile, rmtree
from urllib.parse import quote

from validate_project import RULES, validate_project


def cell(value):
    return str(value).replace("|", "\\|").replace("\n", "<br>").replace("[", "\\[").replace("]", "\\]")


def file_link(path):
    return f"[{cell(path)}]({quote(path, safe='/')})"


def render_video_prompt(prompt):
    return "\n\n".join(name + "\n" + prompt["sections"][name] for name in RULES["prompt_sections"]) + "\n"


def production_guide(project):
    final = project["stage"] == "prompt_package"
    images = {image["image_id"]: image for image in project["image_plan"]}
    assets = {asset["asset_id"]: asset for asset in project["assets"]}
    lines = [
        "# Paket " + ("R2V home tour" if final else "prompt gambar area"), "",
        f"Proyek {project['project_id']} · revisi {project['revision']} · schema {project['schema_version']}.",
        f"Mode gambar: {project['image_mode']}; {len(images)} gambar direncanakan, "
        f"{len(project['shots'])} shot, total {project['total_duration_s']} detik.", "",
        project["concept"]["title"], "", project["concept"]["summary"], "",
        "Brief: " + project["brief"], "", "## Satu rumah", "",
    ]
    for key, value in project["design"].items():
        lines.append("- " + key + ": " + ("; ".join(value) if isinstance(value, list) else value))
    lines.extend(["", "## Gambar area", "",
                  "| ID | Area tujuan | Prompt gambar | File referensi |",
                  "| --- | --- | --- | --- |"])
    for image in images.values():
        asset = assets.get(image["asset_id"])
        file = file_link(asset["path"]) if asset else "Belum tersedia"
        lines.append(f"| {image['image_id']} | {cell(image['primary_area'])} | "
                     f"{file_link('image-prompts/' + image['image_id'] + '.txt')} | {file} |")
    lines.extend(["", "## Peta shot dan referensi R2V", "",
                  "| Shot | Cakupan | Detik | ID gambar referensi | Prompt video |",
                  "| --- | --- | --- | --- | --- |"])
    for shot in project["shots"]:
        prompt = file_link("video-prompts/" + shot["shot_id"] + ".txt") if final else "Belum disiapkan"
        lines.append(f"| {shot['shot_id']} | {cell(', '.join(shot['covered_areas']))} | "
                     f"{shot['duration_s']} | {', '.join(shot['reference_image_ids'])} | {prompt} |")
    lines.extend(["", "## Cara menggunakan", ""])
    if final:
        lines.extend([
            "1. Gunakan mode Reference-to-Video (R2V). Pasang file sesuai ID referensi pada baris shot yang sama.",
            "2. Dua gambar pada shot penghubung menetapkan dua area satu rumah; bukan alternatif desain atau endpoint yang wajib disalin.",
            "3. Salin prompt video shot tersebut. Pilih durasi tabel dan video 9:16 melalui kontrol yang tersedia.",
            "4. Generate satu klip kontinu per shot. Periksa struktur, plafon, gerak dan ambient dari hasil yang tersedia.",
            "5. Rangkai klip sesuai urutan. Cut antarklip terpisah dari gerak kontinu di dalam klip; jangan menambah pengungkapan area atau musik.",
        ])
    else:
        lines.extend([
            "Paket ini berisi seluruh prompt individual. Ia belum menyatakan gambar dibuat, direview atau siap dipakai untuk video.",
            "Gunakan satu prompt untuk satu gambar pada generator pilihan Anda. Bawa file aslinya kembali untuk review dan penyusunan R2V.",
            "Jangan mengganti kumpulan prompt dengan kolase atau memakai rencana kamera sebagai bukti bahwa video sudah dihasilkan.",
        ])
    lines.extend(["", RULES["prompt_constraints"]["audio"], "",
                  "Nama tombol, versi aplikasi dan parameter API tidak diasumsikan.",
                  "", "## Framing, gerak dan keputusan", ""])
    for index, shot in enumerate(project["shots"]):
        following = project["shots"][index + 1]["shot_id"] if index + 1 < len(project["shots"]) else None
        lines.extend([
            f"### {shot['shot_id']} · {shot['kind']} · {shot['duration_s']} detik", "",
            "Awal: " + shot["framing"]["start"], "",
            "Gerak: " + shot["camera"]["description"],
            "Hubungan: " + shot["camera"]["motion_relationship"],
            "Bukti gerak yang ditargetkan: " + shot["camera"]["visible_motion_evidence"],
            "Alokasi ritme: " + shot["camera"]["timing_note"],
            "Akhir: " + shot["framing"]["end"], "",
        ])
        for component in shot["camera"]["components"]:
            details = [component["kind"] + ": " + component["description"],
                       f"mulai {component['start_s']}s, durasi {component['duration_s']}s"]
            if component["distance_m"] is not None:
                details.append(f"perkiraan jarak {component['distance_m']}m")
            if component["angle_deg"] is not None:
                details.append(f"perkiraan sudut {component['angle_deg']}°")
            lines.append("- " + "; ".join(details) + ".")
        lines.extend(["", "Setelah klip: " + ("cut ke " + following if following else "akhir urutan") + ".", ""])
    knowledge = project["knowledge"]
    lines.extend(["## Sumber dan revisi", "",
                  "Pustaka: " + knowledge["repository_url"],
                  "Versi sumber: " + (knowledge["commit"] or knowledge["ref"]),
                  "Jalur tercatat: " + knowledge["route"], ""])
    for evidence in knowledge["evidence"]:
        if evidence["access_status"] == "read":
            lines.append(f"- {evidence['evidence_id']}: [{evidence['reference_id']}]({evidence['analysis_url']}); "
                         + ", ".join(evidence["shot_ids"]) + "; " + cell(evidence["excerpt"]))
    for kind, approval in project["approvals"].items():
        if approval is not None:
            lines.append(f"- Keputusan {kind}: revisi {approval['revision']}, {approval['by']}; {approval['note']}")
    lines.extend("- " + note for note in project["revision_notes"])
    batch = project["image_batch"]
    lines.extend(["", f"Pelaksanaan gambar tercatat: {batch['request_mode']} / {batch['execution']}.",
                  batch["note"], "", "## Melanjutkan dan merevisi", "",
                  "Bawa project.json, panduan, prompt dan gambar asli yang tersedia. Nama file atau tautan sesi lama tidak menggantikan piksel.",
                  "Pertahankan keputusan yang masih berlaku. Jika desain berubah, tinjau area/shot terdampak dan simpan revisi baru.",
                  "Data batch/review adalah catatan pelaksanaan, bukan pengukuran otomatis. Paket ini tidak menyatakan video/audio sudah lulus, dirangkai atau dipublikasikan.", ""])
    return "\n".join(lines)


def build_package(project_file, output):
    project_file, output = Path(project_file).resolve(), Path(output).resolve()
    project = json.loads(project_file.read_text(encoding="utf-8"))
    result = validate_project(project, project_file.parent)
    if not result["valid"]:
        raise ValueError("Project is not ready:\n" + "\n".join(result["errors"]))
    if project["stage"] not in ("image_prompt_package", "prompt_package"):
        raise ValueError("Export requires image_prompt_package or prompt_package.")
    if output.exists():
        raise FileExistsError("Delivery folder already exists; use a new revision folder.")
    reserved = {"project.json", "production-guide.md", "image-prompts", "video-prompts"}
    for asset in project["assets"]:
        if PurePosixPath(asset["path"]).parts[0] in reserved:
            raise ValueError("Asset path collides with a reserved delivery path: " + asset["path"])
    output.mkdir(parents=True, exist_ok=False)
    try:
        for asset in project["assets"]:
            target = output / asset["path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            copyfile(project_file.parent / asset["path"], target)
        for image in project["image_plan"]:
            path = output / "image-prompts" / (image["image_id"] + ".txt")
            path.parent.mkdir(exist_ok=True)
            path.write_text(image["prompt"], encoding="utf-8")
        if project["stage"] == "prompt_package":
            for shot in project["shots"]:
                path = output / "video-prompts" / (shot["shot_id"] + ".txt")
                path.parent.mkdir(exist_ok=True)
                path.write_text(render_video_prompt(shot["prompt"]), encoding="utf-8")
        (output / "project.json").write_text(json.dumps(project, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (output / "production-guide.md").write_text(production_guide(project), encoding="utf-8")
        copied = validate_project(project, output)
        if not copied["valid"]:
            raise ValueError("Copied package failed validation:\n" + "\n".join(copied["errors"]))
    except Exception:
        rmtree(output)
        raise
    return {
        "stage": project["stage"], "project_id": project["project_id"], "revision": project["revision"],
        "shot_count": len(project["shots"]), "image_count": len(project["image_plan"]),
        "total_duration_s": project["total_duration_s"],
        "project": str(output / "project.json"), "guide": str(output / "production-guide.md"),
        "image_prompts": [str(output / "image-prompts" / (item["image_id"] + ".txt")) for item in project["image_plan"]],
        "video_prompts": ([str(output / "video-prompts" / (shot["shot_id"] + ".txt")) for shot in project["shots"]]
                          if project["stage"] == "prompt_package" else []),
        "reference_images": [str(output / asset["path"]) for asset in project["assets"]],
        "limits": copied["limits"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = build_package(args.project, args.output)
    except (OSError, ValueError) as error:
        parser.exit(1, str(error) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
