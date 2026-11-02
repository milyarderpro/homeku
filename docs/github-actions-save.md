# Homeku v1.2 — Pengoperasian GitHub Actions (Sequential Save)

Dokumen ini menjelaskan **implementasi yang sudah ada** pada branch `main`, bukan rancangan fitur masa depan.

## Yang sudah dan belum dibuktikan

- **Lulus di branch pengujian:** Actions run [41454322381](https://github.com/milyarderpro/homeku/actions/runs/41454322381) mengambil MP4 asli `dreamsHouse002.mp4`, menerima request teks dari konektor GitHub, mengekstrak 4 JPEG + 1 storyboard, membentuk YAML/Markdown, dan meng-commit 7 berkas di branch `actions-jpg-test`. Analisis di run ini **fixture integrasi**, bukan draft final yang direview pengguna.
- **Lulus tes idempotensi di branch pengujian:** [41454495367](https://github.com/milyarderpro/homeku/actions/runs/41454495367) memproses request_id yang sama tanpa membuat folder video kedua.
- **Lulus di main (idle):** [41454647109](https://github.com/milyarderpro/homeku/actions/runs/41454647109) menjalankan 8 tes dan melewatkan commit video karena request masih `idle`.
- **Belum dibuktikan:** penyimpanan **video produksi pertama di main** melalui persetujuan `save now` dan review final. Jangan menyamakan keberhasilan branch uji dengan bukti penyimpanan produksi yang sudah terjadi.

Workflow produksi `.github/workflows/save-analysis.yml` sekarang hanya memicu pada **push ke main yang mengubah `requests/save.json`**. Workflow tidak memiliki `workflow_dispatch` dan tidak dipicu hanya oleh upload MP4. Jangan menyuruh pengguna memilih `actions-jpg-test` untuk prosedur produksi; itu branch pengujian historis.

## Prasyarat pengguna

1. Unggah MP4 ke `main/video/<nama-file>.mp4` sebelum analisis, **langsung** di dalam folder `video` (tanpa subfolder). Contoh: `video/dreamsHouse002.mp4`. Saat ini README di folder video hanya petunjuk; keberadaan folder bukan berarti semua MP4 sudah tersedia.
2. Upload video yang sama ke chat untuk dianalisis dan direview. AI boleh membaca GitHub sepanjang fase ini, tetapi **dilarang menulis** sebelum pesan valid `save now`.
3. Nama file sumber harus sama persis (case-sensitive) dengan `video.filename` di YAML. Video lokal yang nama filenya cocok **tidak otomatis terbukti memiliki byte identik**: sebaiknya bandingkan Git blob SHA-1 lokal dengan SHA pada tree main. Jika tidak bisa, jelaskan keterbatasan lalu minta konfirmasi pengguna sebelum menganggap sumber sesuai.
4. Pengguna menyimpan video **satu per satu**. Pastikan request sebelumnya sudah selesai/terverifikasi sebelum mengganti `requests/save.json`.
5. Izin Actions untuk menulis ke repository harus aktif; workflow sendiri mendeklarasikan `permissions: contents: write`. Jika push ditolak, periksa pengaturan GitHub dan log run.

MP4 asli tetap berada di `video/` setelah penyimpanan, sehingga ukuran riwayat Git dapat meningkat. Video berukuran besar mungkin memerlukan strategi penyimpanan lain; integrasi Git LFS **belum diterapkan**.

## Otorisasi dan format request

Pesan pengguna tersendiri persis `save now` (trim spasi, case-insensitive) adalah satu-satunya otorisasi standar untuk menyimpan hasil analisis. Pesan yang sekadar **menyebut** frasa itu bukan otorisasi. Pembaruan rules/kode lewat perintah terpisah tidak dihitung sebagai izin save analisis.

Saat pertama dibuat, `requests/save.json` berisi:

```json
{"schema_version": "1.0", "status": "idle"}
```

Setelah pesan `save now` valid, ChatGPT **menggunakan GitHub connector update_file** pada `main/requests/save.json`, menyertakan SHA blob request yang terbaru. Buat request_id stabil dan unik, lalu kirim **teks JSON** dengan struktur:

```json
{
  "schema_version": "1.0",
  "status": "approved",
  "request_id": "contoh-video-20261102-001",
  "video": {
    "path": "video/contoh.mp4",
    "blob_sha": "<SHA-GIT-BLOB-40-HEX-ASLI>"
  },
  "keyframe_times_s": [2.5, 7.3],
  "analysis_yaml": "<TEKS YAML 2.1 LENGKAP, bukan contoh ringkas>"
}
```

**Contoh di atas bukan request siap dikirim.** Ganti placeholder dengan path MP4 yang ditemukan, SHA aslinya, dan analisis YAML lengkap yang sudah direview; jumlah timestamp sama dengan `video.shot_count`, semuanya di dalam rentang waktu masing-masing shot. `video.id` boleh bernilai `PENDING` sampai runner menetapkan VID final. Tidak perlu mengirim `analysis_md`, JPEG, Base64, ZIP, atau MP4 melalui konektor.

Path MP4 yang diterima runner: `video/<nama>.mp4` langsung, nama diawali alfanumerik dan berisi alfanumerik, titik, underscore atau dash. `blob_sha` harus SHA Git blob sumber pada HEAD yang dipakai runner, **bukan checksum SHA-256**. Request_id dibatasi 8–80 karakter dari huruf/angka/dash/underscore, dimulai alfanumerik. Tidak ada penguncian otomatis yang mencegah pengguna mengganti request saat Actions masih berjalan: disiplin **sequential save** wajib dijaga.

Jika respons konektor saat update tidak pasti, **baca ulang requests/save.json dan daftar run** sebelum mencoba lagi; gunakan request_id yang sama. Setelah request berhasil ditulis, statusnya **Processing/Queued**, bukan Saved.

## Perilaku runner yang benar-benar diimplementasikan

Saat request `approved` ditemukan, `scripts/save_analysis_action.py`:
1. Menghindari penyimpanan ulang dari request_id yang sudah memiliki marker di `references/VID-*/analysis.md`.
2. Memastikan `video/` path aman, file ada, Git blob SHA dari checkout sesuai request, serta jumlah shot dan waktu keyframe konsisten.
3. Menentukan ID terkecil yang masih kosong `VID-XXX` berdasarkan folder yang ada pada checkout.
4. Mengambil frame video dari waktu yang dipilih, mengodekannya menjadi JPEG melalui FFmpeg, dan membuat storyboard JPEG dengan Pillow. **Keyframe berasal dari frame video**, bukan file JPEG byte-identik dengan file preview ChatGPT; kompresi/ukuran gambar dapat berbeda.
5. Memperbarui `video.id` dan `shots[].keyframe` di YAML; membentuk laporan Markdown lewat fungsi `markdown()` dalam script. `templates/analysis.md` adalah **referensi susunan**, bukan mesin template yang dipakai otomatis.
6. Memanggil `scripts/validate_analysis.py`, lalu menulis `requests/result.json` dengan status `saved` dan request_id.
7. GitHub Actions meng-commit paket `references/VID-XXX/` dan `requests/result.json` **bersamaan**, push tanpa force, serta memverifikasi keberadaan file dan hasil validator pada runner.

Proses tidak memakai antrean paralel, retry otomatis konflik HEAD, ataupun Git Data API untuk memindahkan byte JPEG. Jika branch berubah dan push ditolak, Actions **gagal**; periksa run dan branch sebelum mengulang request dengan ID yang sama.

Saat request sudah tersimpan, eksekusi ulang menghasilkan `already_saved` dan melewati commit. Ini mencegah duplikasi berdasarkan **request_id**, bukan otomatis mencegah video yang sama tersimpan dengan request_id baru.

## Bagaimana memeriksa status dengan benar

- **Processing:** update request sudah berhasil, tetapi run yang sesuai masih antre/berjalan atau belum dapat dibuktikan selesai.
- **Saved:** run yang relevan benar-benar `success`, `requests/result.json` berisi `status: saved` dengan **request_id persis sama** dengan `requests/save.json`, folder final tersedia di `main/references/VID-XXX/`, dan berkas serta commit terverifikasi.
- **Not saved:** run gagal, SHA video tidak cocok, request bermasalah, commit gagal, atau verifikasi tidak lengkap. Cari alasan pada log Actions.
- **Already saved:** request_id yang sama ditemukan pada laporan video lama; tampilkan ID lama dan jangan buat yang baru.

**Penting:** `requests/result.json` hanya diperbarui pada *save baru yang berhasil*, bukan saat antre/gagal dan bukan status live. Field `run_id` dalam hasil berasal dari lingkungan Actions dan membantu menghubungkan status dengan run yang benar. Jika file result berisi request_id lama, statusnya **bukan** Saved untuk request baru.

Catatan: GitHub-generated push menggunakan GITHUB_TOKEN tidak memicu workflow push baru. Tindakan berhasilnya update request melalui connector sudah diuji di branch uji, tetapi pengguna harus memastikan run baru pada branch main saat save produksi.

## Troubleshooting cepat

| Kondisi | Tindakan |
|---|---|
| `video/<file>.mp4` tidak ditemukan | Upload MP4 ke `main/video/`, jangan hanya ke chat atau branch uji |
| MP4 mirip namanya tetapi SHA berbeda | Cocokkan video yang benar; jangan memaksa SHA |
| Tidak ada run baru | Periksa commit yang **mengubah** requests/save.json di main dan konfigurasi Actions |
| Run gagal saat tes | Periksa log instalasi Python, Pillow, FFmpeg, dan 8 tes; jangan klaim Saved |
| Run gagal saat push | Periksa permission contents:write / branch protection dan perubahan HEAD; jangan force-push |
| Result JSON masih milik video lama | Jangan keliru menganggap Saved; periksa request_id dan run aktif |
| Request berulang tidak membuat commit | Normal jika sudah tersimpan dengan request_id sama |
| Tidak ada folder baru sesudah upload video | Normal: MP4 upload **bukan** pemicu save |

## Riwayat migrasi

Alur lama ChatGPT Python → Git Data API → Base64 JPG telah dihapus dari jalur produksi, termasuk script, fixture, dan dokumentasi yang terkait. Uji historis branch `actions-jpg-test` tidak dibawa sebagai sumber analisis produksi. Data lama `references/VID-001/` tetap utuh.
