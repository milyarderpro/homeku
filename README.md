# Homeku — Library Analisis Visual Video Rumah

Homeku menyimpan analisis **visual** video desain rumah sebagai **YAML schema 2.1** (sumber fakta) dan laporan Markdown dengan satu JPEG per shot serta satu storyboard. Tidak mencakup audio, ide konten, atau prompt generatif.

**Asosiasi kawasan gaya:** draft baru mencantumkan `architecture.common_regions` (`north_america`, `south_america`, `europe`, `asia`, `africa`, `oceania`), misalnya `[north_america, europe]`. Beberapa kawasan boleh dipilih; gunakan `[]` jika tidak diketahui. Ini **bukan** lokasi aktual rumah atau klaim popularitas terukur. Arsip lama tanpa field tetap valid; pada Markdown nilainya ditampilkan sebagai **Tidak diketahui**.

## Alur aktif: v1.3 — Detailed Visual Analysis + Sequential Save

1. **Pengguna lebih dulu mengunggah MP4 ke branch `main`, folder `video/`**, misalnya `video/dreamsHouse002.mp4`. File MP4 tetap disimpan setelah analisis; upload MP4 saja **tidak** menjalankan proses save.
2. Pengguna mengunggah **video yang sama** ke ChatGPT. AI membaca aturan dan template, menemukan sumber di `main/video/`, lalu menganalisis **seluruh durasi shot** secara detail: exterior, lingkungan/lanskap, interior, tata ruang, material, warna, properti, kamera. ChatGPT membuat **YAML teknis Inggris** serta **narasi bahasa Indonesia natural** untuk tiga kategori `visible_details` di **chat**, kemudian menampilkan keduanya untuk review/revisi. Akses GitHub selama fase ini **read-only**. Bila memungkinkan, cocokkan Git blob SHA; kecocokan nama belum membuktikan byte identik.
3. Hanya pesan pengguna **tersendiri** yang persis `save now` mengizinkan ChatGPT menulis **satu file teks** `requests/save.json` melalui konektor GitHub. Isinya: YAML lengkap, `shot_narratives` yang sudah direview (kategori dan indeks cakupan per shot), path dan Git blob SHA MP4, timestamp keyframe, dan request_id unik/stabil. **Request historis tanpa narasi** tetap didukung.
4. Perubahan request memicu **GitHub Actions** di `main`. Runner **tanpa AI/API key AI** memvalidasi YAML dan `shot_narratives`, mengambil MP4, mengekstrak JPEG dengan FFmpeg, membuat storyboard dengan Pillow, dan menyusun Markdown deterministik dari YAML + paragraf Indonesia yang dibuat di chat. Runner menolak narasi invalid, tetapi menerima request lama tanpa properti narasi melalui formatter lama. Paket dan `requests/result.json` di-commit atomik. Tidak ada file biner dikirim dari ChatGPT.
5. ChatGPT boleh mengatakan **Saved** hanya setelah memastikan run terkait sukses, result.json sesuai **request_id aktif**, dan semua file serta commit sudah tersedia di `main`. Jika run masih berjalan: **Processing**. Jika gagal: **Not saved**. Pengguna menunggu satu save selesai sebelum save lain.

**Storyboard otomatis:** 1–5 shot ditampilkan dalam **satu baris** (kolom = jumlah shot), 6 shot atau lebih menggunakan **3 kolom**. Desain mengikuti referensi pengguna: judul/subtitle, frame portrait sejajar, label scene, waktu shot, dan gerakan kamera. Kode render: [`scripts/storyboard.py`](scripts/storyboard.py). Pembaruan generator berlaku untuk penyimpanan berikutnya; **storyboard VID yang sudah disimpan tidak diubah otomatis**.

**Pemisahan data:** `analysis.yaml` (Schema 2.1) adalah **satu-satunya sumber fakta**, memakai label English `snake_case`. Paragraf Indonesia natural hanya untuk penyajian `analysis.md`. Setiap detail visual wajib tercakup melalui indeks item `covered_indices` dalam request. Python memvalidasi cakupan secara struktural; **kesetaraan makna direview ChatGPT dan pengguna** sebelum `save now`.

**Catatan penting:** `requests/result.json` berisi **hasil sukses terakhir**, bukan status real-time. Bila Actions gagal, file ini dapat berisi request video sebelumnya; jangan menyatakan Saved hanya karena isinya bertuliskan saved. Format `analysis.md` dibuat oleh `scripts/save_analysis_action.py`, sedangkan `templates/analysis.md` adalah acuan struktur, **bukan template yang dieksekusi langsung**. Laporan yang tersimpan bisa berbeda tata letak dari preview chat, tetapi fakta tidak boleh berbeda dari YAML.

## Struktur repo

```text
video/                              # pengguna unggah MP4 di main
references/VID-XXX/
  analysis.yaml                     # sumber fakta, schema 2.1
  analysis.md                       # laporan manusia dari YAML + narasi yang direview di chat
  storyboard.jpg
  shot-01.jpg ... shot-NN.jpg        # satu frame video/JPEG per shot
requests/save.json                  # satu request, awalnya status=idle
requests/result.json                # hasil sukses terbaru, awalnya idle
.github/workflows/save-analysis.yml
scripts/save_analysis_action.py
scripts/validate_analysis.py
rules/workflow-analysis.md
rules/analysis.md
templates/video-analysis.yaml
templates/analysis.md
templates/shot-narratives.json        # contoh bentuk narasi di request, bukan artefak VID
docs/github-actions-save.md
```

Video sumber hanya dikenali runner pada path **`video/<nama-file>.mp4` langsung di dalam folder video**, bukan subfolder bertingkat. Nama harus sama persis (case-sensitive).

## Dokumentasi utama

- [Alur, izin GitHub, dan status save](rules/workflow-analysis.md)
- [Standar analisis visual](rules/analysis.md)
- [Template YAML schema 2.1](templates/video-analysis.yaml)
- [Template acuan Markdown](templates/analysis.md)
- [Template narasi request](templates/shot-narratives.json)
- [Operasi GitHub Actions dan troubleshooting](docs/github-actions-save.md)
- [Cara menaruh MP4](video/README.md)
- [Contoh hasil lama VID-001](references/VID-001/analysis.md)

**Bukti produksi sebelum v1.3:** [VID-004](references/VID-004/analysis.md) berhasil disimpan melalui Actions run [41636775788](https://github.com/milyarderpro/homeku/actions/runs/41636775788), dengan 5 shot. Itu membuktikan jalur save historis, **belum** pengujian jalur narasi v1.3. Pengujian v1.3 dilakukan pada PR/branch pengujian terlebih dahulu sebelum merge ke produksi.

## Project Instructions ChatGPT (diatur terpisah)

Agar aturan ini konsisten untuk setiap chat baru dalam Project Homeku, salin instruksi berikut ke pengaturan **Project Instructions ChatGPT**. Mengedit README atau rules di GitHub **tidak otomatis** mengubah pengaturan tersebut.

> Untuk analisis video Homeku, baca versi terbaru rules/workflow-analysis.md, rules/analysis.md, templates/video-analysis.yaml, templates/analysis.md, dan templates/shot-narratives.json dari repo GitHub milyarderpro/homeku. Analisis seluruh durasi shot secara detail (exterior, interior, lingkungan, warna/material, posisi objek). Buat analysis.yaml Schema 2.1 berbahasa Inggris teknis serta shot_narratives berbahasa Indonesia natural di chat; review agar detail dan covered_indices sama. Pada analisis baru isi architecture.common_regions (atau []), bukan lokasi asli rumah. Cocokkan video chat dengan main/video/<filename>.mp4 dan SHA bila memungkinkan; ungkapkan keterbatasan identitas. Saat ANALYZE/REVIEW GitHub read-only. Hanya pesan tersendiri persis save now mengizinkan update requests/save.json melalui konektor GitHub. Jangan unggah JPEG/MP4 lewat konektor. Runner tidak menggunakan AI API. Setelah request dibuat, verifikasi run, request_id, requests/result.json, dan references/VID-XXX/ sebelum menyatakan Saved. Simpan secara berurutan.
