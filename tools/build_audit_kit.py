#!/usr/bin/env python3
"""Build the reusable chat input kit; no videos or audit results are included."""
from __future__ import annotations

import argparse
import hashlib
import io
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from homeku.common import LibraryError, require, sha256

MODULES = (
    "__init__", "audit_performance", "audit_quality", "audit_review", "audit_session", "audit_workflow", "authoring",
    "camera_anchor", "camera_notation", "camera_pattern", "common", "delivery", "derivations", "exporter", "media",
    "media_incremental", "models", "motion_analysis", "package_manifest", "preflight",
    "render_assets", "report_validation", "reporting", "storage", "validation", "video", "video_cache",
)
RUNTIME = ["tools/audit.py", *(f"tools/homeku/{name}.py" for name in MODULES)]
SCHEMAS = [f"schemas/{name}.schema.json" for name in
           ("audit", "audit-info", "manifest", "reference-reader", "search-index")]
ASSETS = [
    "tools/assets/fonts/DejaVuSans.ttf", "tools/assets/fonts/DejaVuSans-Bold.ttf",
    "tools/assets/fonts/LICENSE.txt", "tools/assets/templates/analysis.md",
    "tools/assets/layouts/media.json",
]
GUIDES = [
    "audit/README.md", "audit/visual-audit.md", "audit/design-audit.md", "audit/authoring.md", "audit/json-guide.md",
    "audit/vocabulary.md", "audit/camera-cases.md", "audit/contracts/package.md",
    "audit/contracts/report.md", "audit/contracts/reader.md",
    "audit/prompts/01-audit.md", "audit/prompts/02-correct.md", "audit/prompts/03-export.md",
    "audit/template-audit.json", "audit/template-audit-info.json",
    "audit/examples/normal/audit.json", "audit/examples/multi/audit.json",
    "requirements.txt",
]
BUNDLED = RUNTIME + SCHEMAS + ASSETS + GUIDES
OUTER_FILES = {"README.md", "homeku_runtime.py", "template-audit.json", "template-audit-info.json"}


def zip_bytes(files):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, content in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, content)
    return buffer.getvalue()


def bootstrap_source():
    import base64, json
    files = {name: (ROOT / name).read_bytes() for name in BUNDLED}
    require(len(BUNDLED) == len(set(BUNDLED)), "Duplicate bundled resource path")
    payload = zip_bytes(files)
    inventory = {name: hashlib.sha256(content).hexdigest() for name, content in files.items()}
    # This standard-library bootstrap restores the complete, active runtime.
    # ZIP input has four members; video is always attached separately.
    template = r'''#!/usr/bin/env python3
"""Restore the bundled HOMEKU runtime; no network or AI calls."""
import argparse, base64, hashlib, io, json, zipfile
from pathlib import Path, PurePosixPath
PAYLOAD = __PAYLOAD__
DIGEST = __DIGEST__
INVENTORY = json.loads(__INVENTORY__)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("."))
    args=parser.parse_args()
    root=args.output.resolve()
    data=base64.b64decode(PAYLOAD, validate=True)
    if hashlib.sha256(data).hexdigest()!=DIGEST:
        raise SystemExit("Runtime payload hash mismatch")
    pending=[]
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        if len(archive.infolist())!=len(INVENTORY) or set(archive.namelist())!=set(INVENTORY):
            raise SystemExit("Runtime inventory mismatch")
        for entry in archive.infolist():
            name=entry.filename
            parts=PurePosixPath(name).parts
            if not parts or name.startswith("/") or ".." in parts or "\\" in name or (entry.external_attr>>16)&0o170000!=0o100000:
                raise SystemExit("Unsafe runtime path")
            target=root.joinpath(*parts)
            if not target.resolve().is_relative_to(root) or any(p.is_symlink() for p in [target,*target.parents] if p!=root.parent):
                raise SystemExit("Runtime path escapes workspace")
            content=archive.read(entry)
            if hashlib.sha256(content).hexdigest()!=INVENTORY[name]:
                raise SystemExit("Runtime file hash mismatch: "+name)
            if target.exists() and (not target.is_file() or target.read_bytes()!=content):
                raise SystemExit("Refusing to replace a different file: "+name)
            pending.append((target,content))
    for target,content in pending:
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(content)
    print(json.dumps({"status":"ok","runtime_files":len(pending),"output":str(root)}))

if __name__=="__main__":
    main()
'''
    return (template.replace("__PAYLOAD__", repr(base64.b64encode(payload).decode()))
            .replace("__DIGEST__", repr(hashlib.sha256(payload).hexdigest()))
            .replace("__INVENTORY__", repr(json.dumps(inventory, sort_keys=True)))).encode()


def build_bytes():
    parts = ["""# Kit audit HOMEKU 3.1

Siapkan satu MP4 sumber terpisah dan ekstrak keempat file kit ke workspace chat. Jalankan `python homeku_runtime.py --output .` untuk memulihkan resource lokal. Audit memakai Python 3.11+, FFmpeg/ffprobe, serta dependensi di requirements.txt termasuk OpenCV dan NumPy.

Untuk Google Drive, simpan kit di root HOMEKU dan MP4 asli di HOMEKU/Video. Hasil disimpan di HOMEKU/Audit/<nama-video-tanpa-ekstensi>/.

Baca `audit/authoring.md` dan jalankan lima fase dalam satu chat memakai `audit/prompts/01-audit.md`.

1. Petakan cut dan siapkan frame baseline dengan `prepare`.
2. Audit kamera dengan `audit/visual-audit.md` dan `audit/camera-cases.md`, lalu jalankan `check-camera`.
3. Lengkapi desain, framing, panel dan Overview dengan `audit/design-audit.md`.
4. Jalankan `complete → check-input → draft → review → export` untuk menghasilkan ZIP final tanpa MP4.
5. Simpan `analysis.md`, `media/`, dan ZIP itu ke Drive, lalu verifikasi hasilnya. Tampilkan laporan, media, unduhan ZIP, dan status penyimpanan di chat.

Gunakan `audit/prompts/02-correct.md` atau `03-export.md` untuk melanjutkan sesi yang sama. Contoh JSON berisi data sintetis.
"""]
    parts.append("\n## Inventaris resource lokal\n\n| File | SHA-256 |\n| --- | --- |\n" +
                 "".join(f"| {name} | {sha256(ROOT / name)} |\n" for name in BUNDLED))
    files = {"README.md": "\n".join(parts).encode(), "homeku_runtime.py": bootstrap_source(),
             "template-audit.json": (ROOT / "audit/template-audit.json").read_bytes(),
             "template-audit-info.json": (ROOT / "audit/template-audit-info.json").read_bytes()}
    require(set(files)==OUTER_FILES and len(files)==4, "Incomplete input kit inventory")
    return zip_bytes(files)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    target = ROOT / "audit/homeku-audit-kit.zip"
    expected = build_bytes()
    if args.check:
        require(target.is_file() and target.read_bytes() == expected, "Chat kit is stale; run tools/build_audit_kit.py")
    else:
        target.write_bytes(expected)
    print(f"Chat kit: {len(OUTER_FILES)} input files, {len(BUNDLED)} bundled resources, {len(expected)} bytes, SHA-256 {hashlib.sha256(expected).hexdigest()}")


if __name__ == "__main__":
    try:
        main()
    except (LibraryError, OSError) as error:
        raise SystemExit(str(error))
