# Homeku — Workflow Analisis Video v1.2 (Sequential GitHub Actions Save)

> Repository: milyarderpro/homeku; branch produksi: main.
> **UPLOAD MP4 → ANALYZE → REVIEW/REVISE → exact save now → REQUEST → ACTIONS → VERIFY.**

## 1. Sumber aturan

Baca versi terbaru dari GitHub sebelum analisis video:
- rules/workflow-analysis.md — proses dan izin GitHub.
- rules/analysis.md — kualitas observasi visual, estimasi, keyframe, dan ketidakpastian.
- templates/video-analysis.yaml — sumber data YAML schema_version 2.1 (tidak berubah).
- templates/analysis.md — struktur laporan manusia; harus mengikuti YAML.

Analisis hanya mencakup visual. Jangan menghasilkan ide video, prompt produksi, atau analisis audio.

## 2. Phase 1: UPLOAD / ANALYZE / REVIEW — GitHub READ ONLY

1. Pengguna **sudah mengunggah MP4 ke main/video/** sebelum mengirim video yang sama ke ChatGPT.
2. Baca rules dan templates terbaru, cari video/<nama-file>.mp4 di main. Cocokkan nama dan, jika byte video lokal tersedia, **Git blob SHA-1** dari video yang diunggah dengan SHA blob dalam tree GitHub. Bila berbeda, jangan menganggap file sama. Jika tidak bisa memverifikasi identitas, jelaskan keterbatasan dan minta konfirmasi sumber video.
3. Catat nama path, Git blob SHA, serta metadata video. File di main/video/ tetap tersimpan sebagai sumber; jangan memindahkan/menghapusnya.
4. Analisis video sepenuhnya menurut rules/analysis.md: shot awal/akhir, scene, pergerakan kamera, pencahayaan, properti, desain rumah, estimasi luas m² dan confidence. Buat **satu timestamp keyframe per shot**, di dalam rentang shot; **bukan** timestamp hardcoded.
5. Tampilkan hasil lengkap di chat: storyboard jika tersedia, gaya, ukuran, warna, timeline, semua detail shot, ketidakpastian, draft YAML schema 2.1, dan laporan. Draft id adalah PENDING.
6. Izinkan revisi pada draft yang sama. Satu chat hanya memiliki satu draft analisis aktif.
7. **Sebelum pesan valid save now: hanya boleh MEMBACA GitHub.** Jangan menulis request, blob, file, commit, atau menjalankan job penyimpanan. Pembaruan kode/rules oleh instruksi eksplisit terpisah dari penyimpanan analisis.

Bila MP4 tidak ditemukan di main/video/, berhenti dan jelaskan cara upload, jangan mengarang path.

## 3. Phase 2: exact save now — kirim SATU request teks

Hanya pesan pengguna tersendiri yang setelah trim dan case-insensitive sama persis dengan **save now** merupakan persetujuan menyimpan draft terbaru di chat yang sama. Penyebutan sebagai kutipan, contoh, atau pertanyaan **tidak sah**. Perintah ulang pada draft yang sudah tersimpan tidak membuat request baru.

Lakukan preflight: draft YAML lengkap (schema 2.1), file sumber di main/video/, blob SHA GitHub, shot_count sesuai shots[], timestamp frame di dalam setiap shot, dan user sudah melihat review. Jangan menyimpan jika sumber berbeda/hilang.

ChatGPT menggunakan konektor GitHub yang sudah ada untuk **membuat atau memperbarui UTF-8 requests/save.json** di main. Schema:

    {
      "schema_version": "1.0",
      "status": "approved",
      "request_id": "unique-stable-id-8chars-min",
      "video": {"path": "video/example.mp4", "blob_sha": "<40 hex Git blob SHA>"},
      "keyframe_times_s": [2.5, 7.3],
      "analysis_yaml": "<SELURUH YAML schema 2.1 sebagai string>"
    }

Request_id harus unik antarvideo dan STABIL untuk retries/reviews; jangan membuat ID baru hanya karena panggilan API tidak pasti. Bila responses GitHub ambigu, baca requests/save.json sebelum retry. Satu request aktif pada satu waktu; jangan mengganti request saat Actions belum selesai. Saat pertama kali repo diinisialisasi, requests/save.json berisi status idle. Setelahnya gunakan GitHub connector **update_file** dengan blob SHA terbaru; jangan membuat file baru untuk setiap video. Format teks YAML boleh tetap berisi video.id PENDING karena ID final ditetapkan runner.

**ChatGPT TIDAK mengunggah JPEG, ZIP, MP4, atau data biner ke konektor.** Hanya teks request.

Setelah update berhasil, sampaikan status **Processing/Queued**, bukan Saved. Periksa GitHub Actions run pada branch main, requests/result.json, dan files references; jangan menganggap commit request sama dengan commit video.

## 4. Phase 3: GitHub Actions memproses request

.github/workflows/save-analysis.yml dipicu oleh push pada main yang mengubah **hanya requests/save.json** (path filter). Actions memeriksa status approved, request_id, video path aman, SHA MP4, data YAML dan timestamps. Tanpa MP4/tidak cocok, job gagal tanpa menyimpan paket parsial.

scripts/save_analysis_action.py:
1. Periksa request_id pada marker Markdown video yang sudah tersimpan, untuk mencegah duplikasi meski request diulang.
2. Baca MP4 yang sudah ada di main/video/. Pastikan SHA Git blob sesuai request.
3. Ambil ID terkecil yang kosong dari references/VID-XXX/ pada HEAD branch terbaru.
4. Finalisasi video.id dan shots[].keyframe. Ekstrak tepat satu JPG per shot dari timestamp request via FFmpeg.
5. Buat storyboard.jpg melalui Pillow; susun analysis.yaml dan analysis.md dari YAML yang sama.
6. Jalankan scripts/validate_analysis.py untuk memeriksa semua file/JPEG/shot.
7. Simpan references/VID-XXX/ dan requests/result.json dalam **satu commit** lalu push main tanpa force.
8. Verifikasi commit ada di branch dan file tersedia. Action GitHub token commit tidak boleh memicu simpan ulang. Kesalahan validasi/push dilaporkan lewat log Actions; hasil sebelumnya pada result.json tidak boleh dianggap hasil terbaru.

Tidak ada penyimpanan paralel (pengguna menunggu satu penyimpanan selesai). Tidak ada sistem antrean khusus dan tidak ada transfer file JPEG Base64 dari Python ChatGPT.

## 5. Phase 4: VERIFY / status

- **Saved** hanya jika run Actions sukses, result.json.status=saved, result.request_id sama dengan request aktif, dan seluruh file references/VID-XXX/ dapat ditemukan pada main; tampilkan ID, shot_count, analysis.md, analysis.yaml, serta commit Actions.
- **Processing** jika Actions masih queued/in progress.
- **Not saved** jika Actions gagal, file tidak lengkap, result.json tidak sesuai atau penyimpanan tidak terjadi. Jangan mengklaim sukses hanya karena requests/save.json berhasil diperbarui.
- Jika request sebelumnya tersimpan, gunakan ID sama; jangan melakukan penyimpanan baru.
- Jangan memulai save video lain sebelum status video sebelumnya telah dikonfirmasi.

## 6. Batas teknis

GitHub Actions mengambil MP4 dari **main/video/**; ChatGPT tidak dapat otomatis memindahkan MP4 upload chat ke GitHub. MP4 wajib diunggah pengguna terlebih dahulu. File besar membuat riwayat Git membesar. Upload browser GitHub punya batas ukuran; jangan menggunakan Git LFS tanpa adaptasi downloader.

GitHub Project Instructions harus mengarahkan AI membaca keempat file aturan/template terbaru. Dokumen ini tidak otomatis mengeksekusi tool.

## 7. Mode uji dan rujukan

Runner juga mengizinkan branch actions-jpg-test khusus untuk tes isolasi yang nyata, tanpa menulis references di main. Data produksi hanya berasal dari request main dengan persetujuan save now.

Detail teknis dan troubleshoot: docs/github-actions-save.md.

**Prinsip:** Analyze = Read Only. Exact save now = Write Authorized. Actions = Generate and commit. Verify before Saved.
