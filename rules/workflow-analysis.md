# Homeku — Workflow Analisis Video v1.2

**Mode:** Sequential Save (satu proses penyimpanan sampai selesai sebelum berikutnya). **Produksi:** branch `main` pada repository `milyarderpro/homeku`.

**Alur:** **UPLOAD MP4 → ANALYZE → REVIEW/REVISE → pesan `save now` → REQUEST → GITHUB ACTIONS → VERIFY**.

## 1. Sumber kebenaran

Sebelum analisis, baca versi terbaru:
- `rules/workflow-analysis.md` (dokumen ini): izin menulis, sumber MP4, request, Actions, dan verifikasi.
- `rules/analysis.md`: isi, estimasi, label, standar visual, dan aturan asosiasi kawasan `common_regions`.
- `templates/video-analysis.yaml`: struktur YAML, `schema_version: "2.1"`.
- `templates/analysis.md`: **acuan struktur** laporan; implementasi Actions membentuk Markdown sendiri dari YAML melalui `scripts/save_analysis_action.py`.

Ruang lingkup hanya visual, tanpa analisis audio, ide konten, atau prompt generatif.

## 2. Fase 1 — UPLOAD / ANALYZE / REVIEW (GitHub READ ONLY)

1. Pengguna lebih dahulu mengunggah MP4 ke **`main/video/<nama-file>.mp4`**, langsung pada folder `video/`. Upload hanya ke chat atau branch pengujian **tidak** menyediakan MP4 bagi runner produksi.
2. AI membaca repo untuk menemukan path dan Git blob SHA sumber. Cocokkan nama secara persis, termasuk kapitalisasi. Bila byte video upload chat tersedia, hitung Git blob SHA dan bandingkan dengan GitHub; kesamaan nama saja tidak cukup membuktikan identitas. Bila tidak bisa memverifikasi byte, ungkapkan keterbatasan dan minta konfirmasi pengguna sebelum memakai sumber tersebut.
3. Analisis video dalam chat sesuai `rules/analysis.md`: urutan shot, start/end, arsitektur, kamera, warna, pencahayaan, properti, ukuran visual dan confidence. Pilih **satu timestamp keyframe per shot**, di dalam [start_s, end_s); jangan memakai waktu hardcoded dari video uji.
4. Susun draft YAML 2.1 dengan `video.id: PENDING`; pada draft, `shots[].keyframe` boleh `null` karena path final diberikan Actions. Tampilkan ringkasan, storyboard preview (jika tersedia), timeline, rincian setiap shot, kualitas dan ketidakpastian. Preview gambar boleh berbeda byte dari JPEG hasil FFmpeg runner; keduanya harus berasal dari shot yang sama.
5. Perbaiki draft aktif jika diminta. Satu chat memiliki paling banyak satu draft yang belum tersimpan. Jangan menimpa draft lain secara diam-diam.
6. **Selama semua tahap ini dilarang melakukan write GitHub**: tidak membuat request, blob, file, commit, atau memicu workflow simpan. Akses GitHub hanya read-only. Instruksi eksplisit untuk memperbarui dokumentasi/kode bukan persetujuan menyimpan data analisis video.

Jika video sumber tidak ditemukan, jangan mengarang path; jelaskan cara upload. Jangan mengklaim identitas sumber sudah diverifikasi apabila baru cocok namanya.

## 3. Fase 2 — Hanya pesan tersendiri `save now`

Satu-satunya perintah save standar ialah pesan pengguna yang setelah trim spasi dan tanpa membedakan kapitalisasi sama persis dengan `save now`. Penyebutan frasa itu dalam contoh, kutipan, pertanyaan, atau pesan yang mengandung teks lain **bukan** izin. Perintah berlaku hanya untuk draft terbaru yang telah ditampilkan dan berstatus menunggu review dalam **chat yang sama**. Pesan berulang pada draft yang sudah saved tidak membuat ID/request baru.

**Preflight:**
- MP4 tersedia di `main/video/<nama>.mp4` dan file sumber serta Git blob SHA diketahui; cocokkan byte dengan video chat bila memungkinkan, jangan mengklaim sudah cocok tanpa bukti.
- YAML lengkap schema 2.1, `video.filename` sama dengan basename MP4, shot_count benar, shot berurutan, durasi masuk akal, kamera/properti/catatan mengikuti rules analisis.
- Draft **baru** mencantumkan `architecture.common_regions` sebagai daftar kawasan gaya yang valid (boleh `[]`); jangan menyimpulkan lokasi asli bangunan. Data lama tanpa field tersebut tetap kompatibel.
- `keyframe_times_s` satu angka per shot, terletak di dalam [start_s, end_s) dan berasal dari review video tersebut.
- Request terdahulu selesai atau sudah dipastikan tidak sedang berjalan. **Tidak ada penguncian otomatis** yang menjamin dua request tidak bertabrakan.

AI memakai konektor GitHub **update_file** untuk memperbarui file teks `main/requests/save.json`, menggunakan blob SHA file saat ini. Jangan menulis dokumen/gambar/video lain melalui connector. Format request:

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
  "analysis_yaml": "<YAML 2.1 LENGKAP DARI REVIEW, bukan placeholder>"
}
```

Ini **ilustrasi**, bukan request siap kirim. `request_id` harus stabil (8–80 karakter, alfanumerik/dash/underscore, mulai alfanumerik) dan unik untuk satu persetujuan video. `blob_sha` adalah SHA Git blob file MP4 yang benar (40 hex), **bukan SHA-256**. `analysis_yaml` merupakan string berisi **seluruh YAML**, bukan hanya ringkasan dan bukan JSON object. ID di YAML boleh `PENDING`.

Pada repo yang sudah terinisialisasi ini, file `requests/save.json` **sudah ada**; gunakan `update_file`, bukan `create_file`. Bila hasil operasi ambigu, baca ulang request dan run sebelum retry menggunakan request_id **yang sama**. Konektor **tidak** mengirim byte MP4, JPG, ZIP atau Base64.

Setelah update request berhasil, laporkan **Processing/Queued**, bukan Saved.

## 4. Fase 3 — GitHub Actions di main

File `.github/workflows/save-analysis.yml` saat ini hanya terpicu oleh **push ke main yang mengubah `requests/save.json`**. Mengunggah MP4 saja tidak memicu save. Tidak ada perintah `workflow_dispatch` produksi.

Runner:
1. Checkout main dan persiapkan Python, PyYAML, Pillow, FFmpeg.
2. Jalankan tes lokal yang termasuk dalam repo, lalu proses request jika `approved`.
3. Cek apakah request_id sudah pernah disimpan (marker dalam `references/VID-*/analysis.md`); jika ya, jangan membuat video baru.
4. Validasi path video langsung `video/<nama>.mp4`, SHA Git blob file yang dilacak, nama file YAML, jumlah dan urutan shot, serta timestamp frame.
5. Pilih ID `VID-XXX` terkecil yang belum terpakai pada checkout; ekstrak **frame video** ke JPEG, buat storyboard, finalisasi YAML dan buat Markdown **dari YAML** melalui Python.
6. Validasi keseluruhan paket; baru kemudian lakukan **satu commit** yang menambahkan `references/VID-XXX/` dan memperbarui `requests/result.json`, push tanpa force.
7. Periksa commit di remote branch serta paket yang sudah dibuat. Jika terjadi konflik push atau validasi gagal, run gagal; tidak ada retry otomatis/force push.

**Tidak ada Save paralel**, sistem antrean khusus, penguncian ID, atau jalur Git Data API/Base64 dari ChatGPT. Pengguna harus menunggu sampai request ini selesai sebelum menerbitkan berikutnya. Jika sebuah run sudah gagal, lakukan pemeriksaan penyebab dan keadaan GitHub sebelum mengulang menggunakan ID request yang sama.

## 5. Fase 4 — VERIFIKASI DAN STATUS

- **Processing:** request sudah ditulis, run belum terbukti berhasil.
- **Saved:** run terkait request sukses, `requests/result.json` memuat `status: saved` serta **request_id yang sama persis**, file lengkap di `references/VID-XXX/` dapat diverifikasi pada `main`, dan commit terlihat. Tampilkan VID, jumlah shot, link analysis.md/YAML, serta commit.
- **Already saved:** request_id sudah memiliki paket lama; jangan membuat ulang.
- **Not saved:** run gagal, MP4 hilang/berbeda, result tidak cocok, push gagal, atau file/commit tidak lengkap. Jelaskan penyebab yang terlihat dan jangan mengarang link hasil.

**`requests/result.json` bukan status live.** Ia hanya ditulis saat **save baru berhasil**. Ketika run masih berjalan atau gagal, isinya bisa tetap menunjukkan request lain yang sudah sukses. Pastikan cocokkan request_id dan run. Jika tindakan pemantauan tidak dapat dilanjutkan pada giliran yang sama, jangan menjanjikan pemrosesan di latar belakang oleh ChatGPT; pengguna dapat meminta pengecekan status lagi.

## 6. Batasan, dokumentasi dan hasil pengujian

- MP4 harus disimpan manual di `main/video/`; AI tidak otomatis mengirim video upload chat ke repo.
- Keyframe diekstrak dari frame MP4 oleh FFmpeg dan dikodekan JPEG, **bukan byte-identik** dengan gambar preview ChatGPT.
- `templates/analysis.md` adalah acuan bentuk laporan, bukan template engine; tata letak laporan produksi ditentukan `markdown()` dalam script Actions.
- File MP4 sumber tetap tersimpan setelah save. Riwayat Git akan bertambah; sistem belum mendukung pengambilan Git LFS khusus.
- Edit dokumentasi di repo **tidak otomatis mengubah** Project Instructions ChatGPT.
- Bukti end-to-end ada pada **branch uji** (run `41454322381`), dan uji replay `41454495367`. Produksi `main` baru lulus tes dan `idle` (run `41454647109`); **belum ada video produksi baru yang selesai disimpan** melalui v1.2.

Panduan operasional: [docs/github-actions-save.md](../docs/github-actions-save.md).

**Prinsip:** Analyze = Read Only. Exact `save now` = Write Authorized. Actions = Generate + Commit. Verify before Saved.
