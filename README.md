# Homeku — Library Analisis Visual Video Rumah

**Workflow v1.4: Filename-Based Parallel Save** ([Issue #4](https://github.com/milyarderpro/homeku/issues/4)). ChatGPT menganalisis video rumah secara visual; hasilnya YAML Schema **2.1** (fakta teknis English snake_case), laporan Markdown bernarasi Indonesia natural, satu JPEG per shot, dan satu storyboard. Tanpa audio, konten generatif, atau AI API di runner.

## Cara penggunaan

1. **Upload MP4 ke `main/video/<nama>.mp4`** secara manual, tepat dalam folder `video/`. Upload saja tidak memicu proses save.
2. Unggah MP4 yang sama ke ChatGPT, baca `rules/workflow-analysis.md`, `rules/analysis.md`, template YAML/Markdown/narasi terbaru. Cocokkan Git blob SHA jika mungkin. Analisis setiap shot lengkap (exterior, interior, lanskap, warna, material, posisi/relasi objek, kamera), lalu tampilkan YAML dan narasi Indonesia `shot_narratives` (3 kategori per shot; `covered_indices` lengkap) untuk review. **Fase ini GitHub read-only**.
3. **Hanya pesan tunggal persis `save now`** yang mengizinkan ChatGPT membuat satu request dengan connector GitHub **`create_file`** pada `main/requests/pending/<stem>.json`. Misal `video/edh011.mp4` → `requests/pending/edh011.json`. Payload: JSON request schema 1.0, `approved`, YAML lengkap, narasi Indonesia yang sudah direview, Git blob SHA MP4, keyframe timestamps, dan request_id stabil. **Jangan update `requests/save.json` lama**.
4. Tiap request memicu GitHub Actions **independen**. Python/FFmpeg/Pillow memvalidasi dan membentuk `references/<stem>/analysis.yaml`, `analysis.md`, `storyboard.jpg`, `shot-XX.jpg`. Workflow memublikasikan folder itu dan `requests/results/<stem>.json` secara atomik, memakai safe fetch/rebase/push retry hingga 5 kali tanpa force. Tidak memanggil AI.
5. Status **Saved** hanya setelah result JSON untuk stem **dan request_id yang tepat** serta seluruh paket ditemukan dan tervalidasi pada `main`. Lihat run terkait untuk Processing/Failed. Untuk gagal jaringan/runner, **gunakan workflow_dispatch dengan request_path yang sama**; jangan buat request baru. Beberapa chat dengan video berbeda dapat melakukan `save now` tanpa menunggu.
6. Video yang sudah tersimpan sebagai arsip lama `VID-XXX` **tidak disimpan ulang**: cari `video.filename` di seluruh `references/*/analysis.yaml` sebelum create-file. Contoh `edh001.mp4`→`VID-004`, `edh014.mp4`→`VID-007`, `edh010.mp4`→`VID-010`. Update arsip yang sudah ada adalah workflow terpisah dengan persetujuan eksplisit, bukan `save now` ulang.

## Struktur

```text
video/
  edh011.mp4
requests/
  pending/
    edh011.json              # request approved immutable; satu per video
  results/
    edh011.json              # hasil sukses, bukan status live
references/
  edh011/
    analysis.yaml            # schema 2.1, video.id=edh011
    analysis.md              # natural Indonesian prose dari chat, source YAML
    storyboard.jpg
    shot-01.jpg ...
  VID-001/ ... VID-010/      # arsip legacy tidak dimigrasi
scripts/
  parallel_save.py           # event-specific request, rendering + safe publisher
  save_analysis_action.py    # renderer Markdown + legacy helper
  validate_analysis.py
.github/workflows/
  save-analysis.yml          # filename-based parallel production save
  test-v1.4.yml              # CI test & regression
```

**ID baru = basename MP4 tanpa ekstensi**, kapitalisasi dipertahankan (`dreamsHouse003`). Stem `[A-Za-z0-9][A-Za-z0-9_.-]{0,63}`; kasus beda kapitalisasi ditolak. Request tidak overwrite, tidak ada alokasi `VID-XXX` baru atau counter. Sumber MP4 di `main` diverifikasi menggunakan **Git blob SHA** (40 lowercase hex), bukan SHA-256.

**Gaya regional:** `architecture.common_regions` berisi kawasan terkait gaya desain (boleh `[]`; bukan lokasi rumah). Detail `visible_details` tetap English snake_case; narasi Indonesia dari ChatGPT saja, diverifikasi dengan `covered_indices`, tidak ditambahkan ke YAML.

**Batasan:** arsip dan request `requests/save.json`/`requests/result.json` legacy tetap dibaca/diarsipkan tetapi tidak ditulis oleh flow baru. `templates/analysis.md` merupakan acuan bentuk output, bukan template engine. Perbaikan FFmpeg download/cache adalah pekerjaan terpisah. Tidak ada database, server, queue baru, maupun API AI.

## Dokumentasi
- [Workflow & izin save v1.4](rules/workflow-analysis.md)
- [Standar analisis visual](rules/analysis.md)
- [Template YAML](templates/video-analysis.yaml)
- [Acuan laporan](templates/analysis.md)
- [Template narasi](templates/shot-narratives.json)
- [Operasional GitHub Actions, retry & troubleshooting](docs/github-actions-save.md)
- [Rencana v1.4 dan acceptance](https://github.com/milyarderpro/homeku/issues/4)

## Project Instructions ChatGPT — perlu diperbarui manual

**Perubahan file GitHub tidak otomatis mengubah Project Instructions di ChatGPT.** Salin teks berikut ke pengaturan Project untuk semua chat video baru:

> Untuk Homeku, baca file terbaru `rules/workflow-analysis.md`, `rules/analysis.md`, `templates/video-analysis.yaml`, `templates/analysis.md` dan `templates/shot-narratives.json` di `milyarderpro/homeku@main`. Analisis MP4 dari seluruh durasi shot, buat YAML Schema 2.1 dengan English snake_case detail exterior/interior/lingkungan/material/warna/posisi dan `architecture.common_regions` sebagai asosiasi gaya (atau `[]`), beserta `shot_narratives` Indonesia natural per shot dan 3 kategori dengan `covered_indices` lengkap. Cocokkan source `main/video/<filename>.mp4` dan Git blob SHA, ungkapkan ketidakpastian. Saat Analyze/Review GitHub READ ONLY; tampilkan draft dan tunggu review. **Hanya pesan tersendiri persis `save now`** yang mengizinkan create-file **baru** `main/requests/pending/<filename-stem>.json` setelah cek arsip legacy `references/*/analysis.yaml` dan request/result existing serta collision case-insensitive. **ID final = nama MP4 tanpa ekstensi**, jangan membuat VID numerik baru. Request immutable dengan request_id stabil, jangan overwrite. Actions independen melakukan render dan safe Git push retry; verifikasi status, result per-video dan paket remote sebelum mengaku Saved. Failed run dipulihkan via workflow_dispatch request_path sama; jangan membuat request kedua atau update `requests/save.json` lama.
