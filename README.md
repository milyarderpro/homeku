# Homeku — Library Analisis Visual Video Rumah

Homeku menyimpan analisis **visual** video desain rumah sebagai **YAML schema 2.1** (sumber fakta) dan laporan Markdown dengan satu JPEG per shot serta satu storyboard. Tidak mencakup audio, ide konten, atau prompt generatif.

## Alur aktif: v1.2 — Sequential Save

1. **Pengguna lebih dulu mengunggah MP4 ke branch `main`, folder `video/`**, misalnya `video/dreamsHouse002.mp4`. File MP4 tetap disimpan setelah analisis; upload MP4 saja **tidak** menjalankan proses save.
2. Pengguna mengunggah **video yang sama** ke ChatGPT. AI membaca aturan dan template terbaru, mencari sumber di `main/video/`, melakukan analisis visual, dan menampilkan draft untuk review/revisi. Selama tahap ini akses GitHub **read-only**. Bila memungkinkan, cocokkan Git blob SHA video lokal dengan GitHub; kecocokan nama saja tidak membuktikan byte identik.
3. Hanya pesan pengguna **tersendiri** yang persis `save now` mengizinkan ChatGPT menulis **satu file teks** `requests/save.json` melalui konektor GitHub. Isinya: YAML lengkap, path dan Git blob SHA MP4 di repo, satu timestamp keyframe untuk setiap shot, dan request_id unik serta stabil.
4. Perubahan file request melalui konektor GitHub memicu **GitHub Actions** di `main`. Runner mengambil MP4 dari repo, mengekstrak satu JPEG per shot menggunakan FFmpeg, membuat storyboard dengan Pillow, menyusun YAML dan Markdown dari fakta YAML, memvalidasi, lalu melakukan satu commit berisi `references/VID-XXX/` serta `requests/result.json`. Tidak ada pengiriman file biner dari ChatGPT ke konektor.
5. ChatGPT boleh mengatakan **Saved** hanya setelah memastikan run terkait sukses, result.json sesuai **request_id aktif**, dan semua file serta commit sudah tersedia di `main`. Jika run masih berjalan: **Processing**. Jika gagal: **Not saved**. Pengguna menunggu satu save selesai sebelum save lain.

**Catatan penting:** `requests/result.json` berisi **hasil sukses terakhir**, bukan status real-time. Bila Actions gagal, file ini dapat berisi request video sebelumnya; jangan menyatakan Saved hanya karena isinya bertuliskan saved. Format `analysis.md` dibuat oleh `scripts/save_analysis_action.py`, sedangkan `templates/analysis.md` adalah acuan struktur, **bukan template yang dieksekusi langsung**. Laporan yang tersimpan bisa berbeda tata letak dari preview chat, tetapi fakta tidak boleh berbeda dari YAML.

## Struktur repo

```text
video/                              # pengguna unggah MP4 di main
references/VID-XXX/
  analysis.yaml                     # sumber fakta, schema 2.1
  analysis.md                       # laporan Markdown yang dirender dari YAML
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
docs/github-actions-save.md
```

Video sumber hanya dikenali runner pada path **`video/<nama-file>.mp4` langsung di dalam folder video**, bukan subfolder bertingkat. Nama harus sama persis (case-sensitive).

## Dokumentasi utama

- [Alur, izin GitHub, dan status save](rules/workflow-analysis.md)
- [Standar analisis visual](rules/analysis.md)
- [Template YAML schema 2.1](templates/video-analysis.yaml)
- [Template acuan Markdown](templates/analysis.md)
- [Operasi GitHub Actions dan troubleshooting](docs/github-actions-save.md)
- [Cara menaruh MP4](video/README.md)
- [Contoh hasil lama VID-001](references/VID-001/analysis.md)

**Bukti pengujian:** Run [41454322381](https://github.com/milyarderpro/homeku/actions/runs/41454322381) di **branch uji** berhasil menghasilkan dan menyimpan 7 file dari MP4 asli menggunakan **data analisis uji, bukan laporan review final**. Run [41454495367](https://github.com/milyarderpro/homeku/actions/runs/41454495367) tidak menghasilkan duplikat setelah request yang sama diputar ulang. Run [41454647109](https://github.com/milyarderpro/homeku/actions/runs/41454647109) di **main** lulus 8 tes dan memproses request `idle` tanpa commit video. **Belum ada penyimpanan video produksi pertama di main melalui save now yang teruji.**

## Project Instructions ChatGPT (diatur terpisah)

Agar aturan ini konsisten untuk setiap chat baru dalam Project Homeku, salin instruksi berikut ke pengaturan **Project Instructions ChatGPT**. Mengedit README atau rules di GitHub **tidak otomatis** mengubah pengaturan tersebut.

> Untuk analisis video Homeku, baca versi terbaru rules/workflow-analysis.md, rules/analysis.md, templates/video-analysis.yaml dan templates/analysis.md dari repo GitHub milyarderpro/homeku. Cocokkan video yang diunggah ke chat dengan main/video/<filename>.mp4; jika identitas sumber belum pasti, jelaskan sebelum menyimpan. Selama ANALYZE/REVIEW akses GitHub read-only. Hanya pesan pengguna tersendiri persis save now yang mengizinkan update requests/save.json melalui konektor GitHub. Jangan mengunggah JPEG/MP4 melalui konektor. Setelah request dibuat, cek run GitHub Actions, request_id, requests/result.json, dan references/VID-XXX/ sebelum menyatakan Saved. Simpan satu video sampai tuntas sebelum menyimpan berikutnya.
