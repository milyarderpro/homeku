"""Generate tiny real MP4/JPEG files with explicitly synthetic audit data."""

from __future__ import annotations

import json
import shutil
import struct
import subprocess
import sys
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from homeku.common import dumps, sha256
from homeku.markdown import COMPOSITION, COVERAGE, FACTS, IDENTITY, PHASES, RELATIONS, TIMELINE
from homeku.validation import CODE_ROOT, probe_video


def table(columns, rows):
    return "\n".join(["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"] +
                     ["| " + " | ".join(str(c).replace("|", "\\|") for c in row) + " |" for row in rows])


def fields(values):
    return table(("field", "value"), values.items())


def make_base_video(folder):
    path = folder / "base.mp4"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i",
                    "testsrc2=size=96x160:rate=10", "-t", "1.2", "-c:v", "mpeg4", "-q:v", "5", "-an", str(path)], check=True)
    return path


def isolated_root(folder):
    folder.mkdir(parents=True, exist_ok=True)
    (folder / ".homeku-fixture-root").write_text("Synthetic test root only.\n")
    (folder / "data").mkdir()
    shutil.copyfile(CODE_ROOT / "data/taxonomy.json", folder / "data/taxonomy.json")
    (folder / "incoming").mkdir()
    return folder


def make_folder(parent, rid="fixture-demo", revision=1, supersedes=None, base=None,
                source_bytes=None, layout="raised tub platform", purpose="fixture", variant=0):
    folder = parent / rid
    folder.mkdir(parents=True)
    source = folder / "source.mp4"
    if source_bytes is None:
        base = base or make_base_video(parent)
        payload = (rid + str(variant)).encode()
        source_bytes = base.read_bytes() + struct.pack(">I4s", len(payload) + 8, b"free") + payload
    source.write_bytes(source_bytes)
    metadata = {"path": f"video/{rid}.mp4", "sha256": sha256(source), **probe_video(source)}
    audit = {"method": "synthetic-fixture", "reviewed_ranges": [{"start_s": 0, "end_s": 1.2, "mode": "sampling"}],
             "limitations": "Data sintetis untuk tes kontrak; bukan audit rumah atau video referensi.",
             "created_at": "2026-11-21T00:00:00Z", "ai": {"provider": "synthetic", "model": "not-an-audit", "model_build": None}}
    media, overviews = [], []
    for index, times in enumerate(((0.0, 0.3, 0.5), (0.6, 0.9, 1.1)), 1):
        sid = f"shot-{index:02d}"
        selected = times[0] if index == 1 else times[-1]
        for kind, timestamp in (("area-overview", selected), ("start", times[0]), ("middle", times[1]), ("end", times[2])):
            path = folder / "media" / sid / f"{kind}.jpg"
            path.parent.mkdir(parents=True, exist_ok=True)
            result = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-ss", str(timestamp), "-i", str(source),
                                     "-frames:v", "1", "-f", "image2pipe", "-vcodec", "mjpeg", "-threads", "1", "-"], capture_output=True, check=True)
            path.write_bytes(result.stdout)
            media.append({"path": path.relative_to(folder).as_posix(), "sha256": sha256(path), "kind": kind,
                          "shot_id": sid, "timestamp_s": timestamp, "width": 96, "height": 160, "crop": None, "derived_from": []})
            if kind == "area-overview":
                overviews.append(path)
    board = Image.new("RGB", (240, 384), "white")
    for index, path in enumerate(overviews):
        with Image.open(path) as picture:
            board.paste(picture, (72, index * 192 + 32))
        label = "01 bathroom/laundry 0.00s" if index == 0 else "02 kitchen 1.10s"
        ImageDraw.Draw(board).text((4, index * 192 + 6), label, fill="black")
    board_path = folder / "media/storyboard.jpg"
    board.save(board_path, "JPEG", quality=90)
    media.insert(0, {"path": "media/storyboard.jpg", "sha256": sha256(board_path), "kind": "storyboard", "shot_id": None,
                    "timestamp_s": None, "width": 240, "height": 384, "crop": None,
                    "derived_from": [path.relative_to(folder).as_posix() for path in overviews]})
    chunks = ["# Synthetic fixture — not a reference", "", "## Identitas", "", fields(dict(zip(IDENTITY, ("1.0", rid, revision, f"Synthetic fixture {rid}")))),
              "", "## Ringkasan", "", "Contoh sintetis untuk validasi pustaka. Tidak menggambarkan rumah nyata.", "", "## Cakupan", "",
              fields({key: audit[key] for key in COVERAGE}), "", "## Timeline", "",
              table(TIMELINE, [("shot-01", 0, 0.6, "bathroom; laundry", "cut", "unknown"), ("shot-02", 0.6, 1.2, "kitchen", "end", "unknown")]),
              "", "![Storyboard](media/storyboard.jpg)"]
    for index, sid in enumerate(("shot-01", "shot-02")):
        comp = dict(zip(COMPOSITION, (0 if index == 0 else 1.1, "start" if index == 0 else "end", "Cakupan area paling jelas dalam fixture.", "-",
                    "Di dekat sudut masuk area; estimasi visual fixture.", "Serong menuju subjek.", "oblique", "unknown", "unknown", "Bukaan di tepi layar.",
                    "Lapisan dekat dan jauh.", "Bagian samping area terlihat.", "Cakupan awal.", "Cakupan akhir.", "Adaptasi posisi serong serta peran awal/akhir sesuai gerakan sumber.")))
        evidence = f"[awal](media/{sid}/start.jpg); [akhir](media/{sid}/end.jpg)"
        component = "Dolly-In (~1.3×) + gentle Pan Right (~15°)" if index == 0 else "Dolly-Out (~1.3×)"
        facts = [("f-01", "space", "bathroom" if index == 0 else "kitchen", "layout", layout if index == 0 else "curved island", "observed", "medium", evidence),
                 ("f-02", "furnishing", "bathroom" if index == 0 else "kitchen", "storage", "vanity cabinet", "not-visible", "low", evidence),
                 ("f-03", "material", "wall", "finish", "unknown", "unknown", "unknown", "-")]
        chunks += ["", f'<a id="{sid}"></a>', f"## Shot {sid}", "", "### Desain dan konfigurasi", "", "Contoh uraian sintetis; fakta untuk katalog berada pada tabel berikut.",
                   "", "### Fakta", "", table(FACTS, facts), "", "### Komposisi", "", fields(comp), "", f"![Gambaran area](media/{sid}/area-overview.jpg)",
                   "", "### Kamera", "", "```text", component + ".", "```", "",
                   table(PHASES, [("phase-01", index * 0.6, (index + 1) * 0.6, component, "subjek fixture", "moderate", "constant",
                   "Angka adalah contoh sintaks fixture, bukan pengukuran kamera.", evidence, "low", "Simulasi kontrak, bukan audit gerakan.")]),
                   "", "### Ketidakpastian", "", "Seluruh isi merupakan data uji sintetis."]
    chunks += ["", "## Hubungan antarshot", "", table(RELATIONS, []), "", "## Keterbatasan", "", audit["limitations"]]
    (folder / "analysis.md").write_text("\n".join(chunks) + "\n", encoding="utf-8")
    manifest = {"contract_version": "1.0", "purpose": purpose, "id": rid, "revision": revision, "supersedes": supersedes,
                "source": metadata, "audit": audit, "media": media}
    (folder / "manifest.json").write_text(dumps(manifest), encoding="utf-8")
    return folder


def package_folder(folder, target, include_source=True):
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(folder.rglob("*")):
            if path.is_file() and (include_source or path.name != "source.mp4"):
                info = zipfile.ZipInfo(f"{folder.name}/{path.relative_to(folder).as_posix()}", date_time=(2026, 11, 21, 0, 0, 0))
                info.external_attr = 0o100644 << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(info, path.read_bytes())
    return target


def copy_fixture(parent, rid, template, revision=1, supersedes=None, source_bytes=None, layout=None):
    folder = parent / rid
    shutil.copytree(template, folder)
    manifest = json.loads((folder / "manifest.json").read_text())
    original = manifest["id"]
    manifest.update(id=rid, revision=revision, supersedes=supersedes)
    if source_bytes is None:
        payload = rid.encode()
        source_bytes = (folder / "source.mp4").read_bytes() + struct.pack(">I4s", len(payload) + 8, b"free") + payload
    (folder / "source.mp4").write_bytes(source_bytes)
    manifest["source"].update(path=f"video/{rid}.mp4", sha256=sha256(folder / "source.mp4"))
    (folder / "manifest.json").write_text(dumps(manifest))
    text = (folder / "analysis.md").read_text().replace(original, rid).replace("| revision | 1 |", f"| revision | {revision} |")
    if layout:
        text = text.replace("raised tub platform", layout)
    (folder / "analysis.md").write_text(text)
    return folder
