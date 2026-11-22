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
           "tools/homeku/validation.py", "tools/homeku/exporter.py", "docs/contracts/manifest-v1.schema.json", "audit/template-analysis.md"]
GUIDES = ["audit/protocol.md", "audit/rubric.md", "audit/vocabulary.md", "audit/providers.md", "audit/calibration.md",
          "audit/prompts/01-audit.md", "audit/prompts/02-correct.md", "audit/prompts/03-export.md",
          "docs/contracts/package-v1.md", "docs/contracts/analysis-v1.md", "docs/contracts/ai-reader-v1.md"]


def build_bytes():
    parts = ["# HOMEKU — kit audit chat\n\nKit input ini dipakai berulang bersama satu MP4 yang dilampirkan terpisah. Hasil setiap audit adalah satu ZIP referensi baru. Kit berisi sembilan file tanpa video/audio. Baca panduan berikut dan gunakan helper, bukan meminta pengguna mengedit file repo.\n",
             "## Helper di workspace chat\n\nBuka kit ke folder kerja. Dependensi Python: Pillow dan jsonschema; FFmpeg/ffprobe tersedia pada PATH. Gunakan alat yang benar-benar tersedia; error aktual dilaporkan spesifik. Perintah berikut dijalankan AI di workspace chat, bukan oleh pengguna di repo.\n\n"
             "```sh\npython tools/audit.py inspect /path/<id>.mp4\npython tools/audit.py sample /path/<id>.mp4 --output work/shot-01 --start 0 --end <AKHIR_SHOT_01> --shot-id shot-01\npython tools/audit.py sample /path/<id>.mp4 --output work/dense --native --start <AWAL_RENTANG> --end <AKHIR_RENTANG> --shot-id shot-01 --reason \"Pan atau orbit belum jelas\"\npython tools/audit.py draft /path/<id>.mp4 work/analysis.md --audit-info work/audit-info.json --output work/candidate\npython tools/audit.py review work/candidate/<id> --source /path/<id>.mp4 --output work/review.md\npython tools/audit.py export /path/<id>.mp4 work/analysis.md --audit-info work/audit-info.json --output work/final --reviewed-sha256 <SHA256_MD_YANG_DITINJAU> --include-source\n```\n\n"
             "inspect mengembalikan metadata/hash dan seluruh timestamp PTS; itu bukan bukti semua frame sudah dilihat. sample menghasilkan frame native dan contact sheet sementara. Pilih overview_timestamp_s dari PTS aktual. draft/export tidak mengubah isi MD; jika waktu overview bukan PTS sumber, perbaiki draft sebelum ditinjau.\n\n"
             "audit-info.json hanya instruksi kerja: objek reviewed_ranges (start_s/end_s/mode aktual), frame_reviews (record baseline/pendalaman), ai (provider/model/model_build), dan created_at opsional. method/limitations diambil dari MD. Mode hanya sampling, playback atau frame-by-frame yang benar-benar dilakukan; ekstraksi tidak sama dengan pemeriksaan. frame_reviews memakai review_record_template dari sampling.json: isi viewed_frame_indices hanya setelah benar-benar dilihat; baseline seluruh shot wajib selesai. Jumlah frame berasal dari daftar indeks. --native memakai semua frame asli tanpa interpolasi, termasuk sumber 60 FPS. Tidak ada status persetujuan pengguna yang diisi otomatis.\n\n"
             "Jika perlu, --extras menunjuk daftar objek shot_id/path/timestamp_s/crop, untuk reveal-NN atau detail-NN. crop null untuk frame utuh, atau [x,y,width,height] untuk detail. --supersedes menunjuk revision/content_sha256 versi aktif hanya untuk revisi berikutnya. JSON kerja ini tidak masuk ZIP referensi.\n\n"
             "Input MD dan video harus berada di luar folder kandidat. Setiap build membuat media/manifest baru. Hasil candidate/<id>/ dapat ditampilkan untuk review; ZIP ada di candidate/packages/. Digest --reviewed-sha256 hanya mengunci snapshot MD, bukan bukti otomatis persetujuan manusia. Gunakan export setelah pengguna menyatakan isi sesuai. Tidak diperlukan API AI atau akses repo dari chat.\n\n"
             "--include-source digunakan jika sumber belum terbukti ada dengan hash sama di repo; jika sumber cocok sudah ada, opsi ini dapat dihilangkan. Batas kontrak sumber tetap berlaku.\n"]
    for name in GUIDES:
        text = (ROOT / name).read_text(encoding="utf-8")
        # Relative doc links are flattened because their complete content is
        # embedded below; preserve external official documentation links.
        text = re.sub(r"\[([^\]]+)\]\((?!https?://)[^)]+\)", r"\1", text)
        parts.append(f"\n---\n\n<!-- Source: {name} -->\n\n{text}")
    parts.append("\n## Inventaris runtime\n\n| File | SHA-256 |\n| --- | --- |\n" + "".join(f"| {name} | {sha256(ROOT / name)} |\n" for name in RUNTIME))
    files = {name: (ROOT / name).read_bytes() for name in RUNTIME}
    files["README.md"] = "\n".join(parts).encode("utf-8")
    require(len(files) == 9 and not any(name.endswith((".mp4", ".mp3", ".wav")) for name in files), "Input kit must have nine non-media files")
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, content in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, content)
    return buffer.getvalue()


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
    print(f"Chat kit: 9 files, {len(expected)} bytes, SHA-256 {hashlib.sha256(expected).hexdigest()}")


if __name__ == "__main__":
    try:
        main()
    except (LibraryError, OSError) as error:
        raise SystemExit(str(error))
