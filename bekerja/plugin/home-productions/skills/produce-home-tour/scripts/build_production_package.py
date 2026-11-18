"""Export a validated prompt_package with its original images and per-shot prompts.

This creates a new project delivery folder, not a plugin archive. It never
invents prompt text, approvals or visual reviews.
Dependencies are listed in requirements.txt. No network access is used.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path, PurePosixPath
from shutil import copyfile, rmtree
from urllib.parse import quote

from validate_project import RULES, validate_project


def cell(value):
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def file_link(path):
    return f"[{cell(path)}]({quote(path, safe='/')})"


def production_guide(project):
    assets = {asset["asset_id"]: asset for asset in project["assets"]}
    knowledge = project["knowledge"]
    lines = [
        "# Paket produksi home tour", "",
        f"Proyek: {project['project_id']} · revisi {project['revision']} · aturan {project['rules_version']}.",
        f"{len(project['shots'])} shot · total {project['total_duration_s']} detik.", "",
        "## Konsep dan rumah", "",
        project["concept"]["title"], "", project["concept"]["summary"], "",
        "Brief: " + project["brief"], "",
    ]
    for key, label in (
        ("architecture", "Arsitektur"), ("layout", "Tata ruang"),
        ("materials", "Material"), ("lighting", "Cahaya"),
        ("environment", "Lingkungan"), ("anchors", "Elemen tetap"),
    ):
        value = project["design"][key]
        lines.append(f"- {label}: " + ("; ".join(value) if isinstance(value, list) else value))
    lines.extend([
        "", "## Peta shot, gambar dan prompt", "",
        "| Shot | Cakupan | Detik | Frame awal | Frame akhir | Prompt |",
        "| --- | --- | --- | --- | --- | --- |",
    ])
    for shot in project["shots"]:
        start, end = (assets[shot["frames"][role]]["path"] for role in RULES["frames"]["roles"])
        lines.append(
            f"| {shot['shot_id']} | {cell(', '.join(shot['covered_areas']))} | {shot['duration_s']} | "
            f"{file_link(start)} | {file_link(end)} | {file_link('prompts/' + shot['shot_id'] + '.txt')} |"
        )
    lines.extend([
        "", "## Cara menggunakan", "",
        "1. Buka dua PNG pada baris shot yang sama. Pasang frame awal sebagai gambar awal dan frame akhir sebagai gambar akhir.",
        "2. Salin teks dari file prompt shot tersebut. Pilih durasi pada tabel menggunakan kontrol yang tersedia di Omni Flash.",
        "3. Generate satu klip untuk satu shot. Total proyek bukan durasi satu permintaan generator.",
        "4. Periksa hasil visual dan dengarkan ambient bila audionya dapat diakses. Catat masalah yang belum diperiksa.",
        "5. Rangkai klip sesuai urutan di bawah. Jangan menambah shot pengulangan area atau musik pada editing.", "",
        RULES["prompt_constraints"]["audio"], "",
        "Panduan memakai dukungan pasangan awal–akhir dan durasi yang dikonfirmasi pengguna. "
        "Nama tombol, versi aplikasi dan parameter API tidak diasumsikan.", "",
        "## Framing, gerak dan urutan", "",
    ])
    motion_labels = {"single": "tunggal", "simultaneous": "bersamaan", "sequential": "berurutan"}
    for index, shot in enumerate(project["shots"]):
        following = project["shots"][index + 1]["shot_id"] if index + 1 < len(project["shots"]) else None
        lines.extend([
            f"### {shot['shot_id']} · {shot['kind']} · {shot['duration_s']} detik", "",
            "Awal: " + shot["framing"]["start"],
            "", "Gerak (" + motion_labels[shot["camera"]["motion_relationship"]] + "): " + shot["camera"]["description"],
            "", "Akhir: " + shot["framing"]["end"],
            "", "Bukti: " + ", ".join(shot["evidence_ids"]),
            "", ("Setelah klip ini, cut ke " + following + ".") if following else "Akhir urutan proyek.",
            "Catatan perangkaian ini berada di luar gerakan kontinu dalam klip.", "",
        ])
    lines.extend([
        "## Sumber dan versi keputusan", "",
        "Pustaka: " + knowledge["repository_url"],
        "Versi sumber: " + (knowledge["commit"] or knowledge["ref"]),
        "Jalur akses tercatat: " + knowledge["route"], "",
    ])
    for evidence in knowledge["evidence"]:
        if evidence["access_status"] != "read":
            continue
        lines.extend([
            f"- {evidence['evidence_id']}: [{evidence['reference_id']}]({evidence['analysis_url']}); "
            + ", ".join(evidence["shot_ids"]) + "; " + ", ".join(evidence["field_paths"]),
            "  Kutipan: " + cell(evidence["excerpt"]),
        ])
    for kind, approval in project["approvals"].items():
        lines.append(f"- Keputusan {kind}: revisi {approval['revision']}, {approval['by']}; {approval['note']}")
    if project["revision_notes"]:
        lines.extend(["", "Catatan revisi:", ""])
        lines.extend("- " + note for note in project["revision_notes"])
    lines.extend([
        "", "## Melanjutkan atau merevisi", "",
        "Bawa project.json, panduan ini dan file gambar asli. Nama file atau tautan sesi lama tidak menggantikan piksel gambar.",
        "Gunakan keputusan yang masih berlaku; periksa aset sebelum melanjutkan. "
        "Bila elemen tetap berubah, tinjau shot terdampak dan simpan revisi baru dengan pasangan/prompt yang sesuai.",
        "Paket ini menyiapkan produksi. Ia tidak menyatakan video/audio sudah diuji, video sudah dirangkai atau sudah dipublikasikan.", "",
    ])
    return "\n".join(lines)


def build_package(project_file, output):
    project_file, output = Path(project_file).resolve(), Path(output).resolve()
    project = json.loads(project_file.read_text(encoding="utf-8"))
    validation = validate_project(project, project_file.parent)
    if not validation["valid"]:
        raise ValueError("Project is not ready:\n" + "\n".join(validation["errors"]))
    if project["stage"] != "prompt_package":
        raise ValueError("Only stage prompt_package can be exported as a complete production package.")
    if output.exists():
        raise FileExistsError("Delivery folder already exists; choose a new revision folder.")
    for asset in project["assets"]:
        if PurePosixPath(asset["path"]).parts[0] in {"project.json", "production-guide.md", "prompts"}:
            raise ValueError("Asset path collides with a reserved delivery path: " + asset["path"])
    guide = production_guide(project)
    # The folder is new and belongs to this export; failed copies never replace an older delivery.
    output.mkdir(parents=True, exist_ok=False)
    try:
        for asset in project["assets"]:
            target = output / asset["path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            copyfile(project_file.parent / asset["path"], target)
        for shot in project["shots"]:
            target = output / "prompts" / (shot["shot_id"] + ".txt")
            target.parent.mkdir(exist_ok=True)
            target.write_text(shot["prompt"]["text"], encoding="utf-8")
        (output / "project.json").write_text(
            json.dumps(project, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
        )
        (output / "production-guide.md").write_text(guide, encoding="utf-8")
        copied = validate_project(project, output)
        if not copied["valid"]:
            raise ValueError("Copied package failed validation:\n" + "\n".join(copied["errors"]))
    except Exception:
        rmtree(output)
        raise
    assets = {asset["asset_id"]: asset for asset in project["assets"]}
    return {
        "project_id": project["project_id"], "revision": project["revision"],
        "shot_count": len(project["shots"]), "total_duration_s": project["total_duration_s"],
        "project": str(output / "project.json"),
        "guide": str(output / "production-guide.md"),
        "prompts": [str(output / "prompts" / (shot["shot_id"] + ".txt")) for shot in project["shots"]],
        "frames": [str(output / assets[shot["frames"][role]]["path"])
                   for shot in project["shots"] for role in RULES["frames"]["roles"]],
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
