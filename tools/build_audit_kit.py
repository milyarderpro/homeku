#!/usr/bin/env python3
"""Build the reusable chat input kit; no videos or audit results are included."""
from __future__ import annotations

import argparse
import hashlib
import io
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from homeku.common import LibraryError, require, sha256

RUNTIME = ["tools/audit.py", "tools/homeku/__init__.py", "tools/homeku/common.py", "tools/homeku/markdown.py",
           "tools/homeku/validation.py", "tools/homeku/exporter.py", "docs/contracts/manifest-v1.schema.json", "audit/template-analysis.md",
           "tools/homeku/video.py", "tools/homeku/models.py", "tools/homeku/media.py", "tools/homeku/reporting.py",
           "docs/contracts/audit-v2.schema.json", "docs/contracts/manifest-v2.schema.json",
           "tools/homeku/media_v2_0.py", "tools/homeku/media_v2_1.py", "tools/homeku/media_v2_1_1.py", "tools/assets/templates/analysis-2.1.2.md", "tools/assets/templates/analysis-2.1.1.md", "tools/assets/fonts/DejaVuSans-Bold.ttf", "tools/assets/templates/analysis-2.1.0.md",
           "tools/assets/fonts/DejaVuSans.ttf", "tools/assets/fonts/LICENSE.txt", "tools/assets/templates/analysis-2.0.0.md"]
RUNTIME += ["tools/homeku/reporting_v2_legacy.py", "tools/homeku/media_v2_1_2.py",
            "tools/homeku/camera_pattern.py", "tools/homeku/media_v2_2.py", "tools/homeku/reporting_v2_2.py",
            "docs/contracts/audit-v2-1.schema.json", "docs/contracts/manifest-v2-1.schema.json",
            "tools/assets/templates/analysis-2.2.0.md", "tools/assets/layouts/media-2.2.0.json"]
# The authoring document can be a draft; the active kit uses its implemented renderer template.
GUIDES = ["audit/README.md", "audit/json-guide.md", "audit/protocol.md", "audit/rubric.md", "audit/vocabulary.md", "audit/providers.md", "audit/calibration.md",
          "audit/prompts/01-audit.md", "audit/prompts/02-correct.md", "audit/prompts/03-export.md",
          "docs/contracts/package-v2-1.md", "docs/contracts/analysis-v2-2.md", "tools/assets/templates/analysis-2.2.0.md"]
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
    files = {name: (ROOT / name).read_bytes() for name in RUNTIME}
    payload = zip_bytes(files)
    inventory = {name: hashlib.sha256(content).hexdigest() for name, content in files.items()}
    # This standard-library bootstrap restores the complete, versioned runtime.
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
    parts = ["# HOMEKU — kit audit V2\n\nInput: satu ZIP ini dan satu MP4 terpisah.\n\n"
             "Ekstrak empat file input, lalu jalankan `python homeku_runtime.py --output .`. "
             "Bootstrap memulihkan seluruh runtime/schema/font/lisensi dari payload lokal yang diinventarisasi; tidak mengunduh kode. "
             "Dependensi runtime: Python 3.11+, Pillow, jsonschema, FFmpeg/ffprobe. "
             "Baca seluruh panduan berikut. Placeholder template wajib diganti dengan hasil audit nyata. "
             "Versi sumber/paket 2.1; renderer/media/template 2.2.0. Jangan mengubah renderer versi lama.\n"]
    for name in GUIDES:
        body = (ROOT / name).read_text(encoding="utf-8")
        body = re.sub(r"\[([^\]]+)\]\((?!https?://)[^)]+\)", r"\1", body)
        parts.append(f"\n---\n\n<!-- Source: {name} -->\n\n{body}")
    parts.append("\n## Inventaris runtime terpulihkan\n\n| File | SHA-256 |\n| --- | --- |\n" + "".join(f"| {name} | {sha256(ROOT / name)} |\n" for name in RUNTIME))
    files = {"README.md": "\n".join(parts).encode(), "homeku_runtime.py": bootstrap_source(),
             "template-audit.json": (ROOT / "audit/template-audit.json").read_bytes(),
             "template-audit-info.json": (ROOT / "audit/template-audit-info.json").read_bytes()}
    require(set(files)==OUTER_FILES and len(files)<=10, "Incomplete input kit inventory")
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
    print(f"Chat kit: {len(OUTER_FILES)} input files, {len(RUNTIME)} runtime files, {len(expected)} bytes, SHA-256 {hashlib.sha256(expected).hexdigest()}")


if __name__ == "__main__":
    try:
        main()
    except (LibraryError, OSError) as error:
        raise SystemExit(str(error))
