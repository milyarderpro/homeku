# Homeku — Workflow Analisis Video v1.4 (Filename-Based Parallel Save)

**Sumber kebenaran:** `main` pada `milyarderpro/homeku`. **Alur:** UPLOAD → ANALYZE/REVIEW (read-only) → pesan `save now` → satu immutable per-video request → independent GitHub Actions → safe Git publication → VERIFY.

## 1. Baca sebelum analisis
Baca versi terbaru `rules/workflow-analysis.md`, `rules/analysis.md`, `templates/video-analysis.yaml`, `templates/analysis.md`, dan `templates/shot-narratives.json`. Analisis **visual saja**: exterior, interior, lanskap, warna/material/posisi objek, relasi spasial, pergerakan kamera, estimasi dan confidence. Tidak menganalisis audio, membuat ide konten, atau prompt generatif.

Pengguna menaruh MP4 **terlebih dahulu** pada `main/video/<filename>.mp4` (langsung di folder video), lalu mengunggah video yang sama ke chat. Baca path dan Git blob SHA dari `main`; bila byte upload chat tersedia, bandingkan Git blob SHA; jangan menganggap nama file sama sebagai bukti byte identik.

## 2. Analyze / Review — GitHub READ ONLY
- Analisis durasi **penuh** setiap shot, tidak hanya keyframe. Pilih tepat satu timestamp keyframe per shot dalam `[start_s, end_s)`.
- Buat YAML Schema 2.1, English snake_case visual details, `architecture.common_regions` sebagai kawasan **gaya** (atau `[]`), bukan lokasi asli. Draft `video.id: PENDING` dan `shots[].keyframe: null` boleh.
- Di **ChatGPT** buat `shot_narratives` untuk tiap `shot-XX` dengan tepat tiga kategori `architectural`, `furniture_and_props`, `environment`. Kalimat bahasa Indonesia natural hanya dari YAML, `covered_indices` 0-based harus mencakup semua item kategori tepat sekali; kategori YAML kosong => `{"text":null,"covered_indices":[]}`. Tinjau kesetaraan makna dua arah sebelum meminta persetujuan.
- Tampilkan analisis, timeline, detail semua shot, contoh paragraf per kategori, storyboard preview (jika tersedia), kualitas dan ketidakpastian. Satu chat maksimal satu draft belum disimpan; revisi YAML berarti revisi narasi/indeks bersama-sama.
- **Tidak boleh melakukan write ke GitHub** selama tahap analisis/review. Tidak ada permintaan save otomatis atau upload JPEG/MP4/Base64 melalui connector.

## 3. Exact `save now` — persetujuan penyimpanan
Hanya pesan pengguna yang, setelah trim dan case-insensitive, **persis** `save now` dan berdiri sendiri (kecuali ditegaskan pemilik dengan izinnya), berlaku untuk draft terbaru yang sudah ditampilkan/direview di **chat yang sama**. Penyebutan frasa dalam kutipan, pertanyaan, contoh, atau pesan dengan teks lain **bukan** izin. Replay untuk draft sama menggunakan request_id yang sama.

**ID baru:** basename MP4 **tanpa** `.mp4`, mempertahankan kapitalisasi. `video/edh011.mp4` → `edh011` → `references/edh011/`; `video/dreamsHouse003.mp4` → `dreamsHouse003`. Stem baru cocok `[A-Za-z0-9][A-Za-z0-9_.-]{0,63}`, case-sensitive, ekstensi harus `.mp4` persis. ID `PENDING` dan `VID-XXX` disisihkan untuk draft/arsip legacy; tidak ada counter atau alokasi nomor VID baru. Tolak slash/backslash/spasi/traversal, dan case-insensitive collision terhadap nama yang sudah ada.

**Preflight WAJIB sebelum write:**
1. MP4 ada di `main/video/<filename>.mp4` dan Git blob SHA (40 lowercase hex) benar. Filename pada YAML identik dengan basename MP4, jumlah/timeline shot/ketepatan keyframe sesuai.
2. YAML 2.1 dan narasi Indonesia lengkap untuk **setiap shot dan tiga kategori**, `covered_indices` tepat, arti telah ditinjau. Runner tidak menulis narasi.
3. Periksa semua `references/*/analysis.yaml`: jika `video.filename` sama (termasuk case-insensitive) dengan video baru, **Already saved** dan tautkan arsip legacy / baru. Contoh `edh010.mp4` sudah tersimpan sebagai `VID-010`. Jangan buat duplikat. Bila metadata existing rusak, **fail closed**.
4. Periksa `requests/pending/<stem>.json` dan `requests/results/<stem>.json`; jika existing dan request sama, tampilkan status/replay. Jika berbeda, nyatakan **conflict**, **jangan overwrite**. Periksa tabrakan kapitalisasi pada video/request/result/folder.
5. `request_id` 8–80 karakter dengan pola `[A-Za-z0-9][A-Za-z0-9_-]{7,79}`, unik untuk persetujuan ini dan stabil saat retry.

**Satu-satunya write normal ChatGPT:** GitHub connector **`create_file`** untuk file **baru** `main/requests/pending/<stem>.json`, berisi JSON UTF-8 sesuai schema request `1.0`, `status=approved`, `request_id`, `video.path`, `video.blob_sha`, `keyframe_times_s`, string `analysis_yaml` lengkap, dan `shot_narratives` lengkap. **Jangan `update_file` untuk request normal; jangan menyentuh `requests/save.json` legacy.**

Jika API error/timeout/409/422 atau respons ambiguous: baca ulang **file yang sama di main**. Jika sama payload+request_id → berhasil/replay; jika berbeda → conflict; jika file masih absen → retry dengan **ID, path dan payload yang sama**, maksimum 3 kali. Jangan memilih ID baru atau mengklaim Saved setelah create_file.

Setelah create_file berhasil laporkan **Queued/Processing**, bukan Saved. Chat lain boleh menerbitkan `save now` video **berbeda** tanpa menunggu.

## 4. GitHub Actions independen di main
`.github/workflows/save-analysis.yml` dipicu oleh **push file baru ke `requests/pending/*.json`**; tersedia `workflow_dispatch` manual dengan input `request_path` untuk pemulihan. Tidak ada concurrency group global.

- Snapshot run **dipatok ke Git SHA pemicu**. Pada push, ambil file `added` di `before..after`; tepat satu pending request harus baru dan tidak ada modifikasi/deletion. Jika batch >1 atau invalid, fail closed, tampilkan path dan jalankan `workflow_dispatch` satu per path. Jangan memilih latest request.
- Pada `workflow_dispatch` gunakan satu path valid pada SHA checkout. Saat publish cek blob SHA pending di remote `main` masih sama; request yang diperbaiki lewat PR tidak boleh diproses dari snapshot lama.
- Runner memvalidasi request, source Git blob, ID filename, narasi, duplicate legacy dan timestamp; mengekstrak JPEG FFmpeg, membuat storyboard Pillow, merender Markdown Python dari YAML + narasi chat, dan memvalidasi paket. AI tidak berjalan di Actions.
- Paket `references/<stem>/` dan `requests/results/<stem>.json` dipublikasikan **bersamaan dalam satu commit**, hanya path video itu, tanpa force. Jika `main` bergerak, lakukan fetch/recheck/rebase/push fast-forward maksimal **5 kali** (backoff kecil). Pembuatan paket dan FFmpeg boleh berjalan paralel dengan video lain; hanya publikasi ref Git yang bersaing.
- Jika hasil remote dengan request_id identik sudah **lengkap dan valid**, return `already_saved` tanpa commit; jika hasil berbeda/parsial, request SHA drift, atau konflik isi, **fail closed**. Runner verifikasi remote sebelum menyatakan saved.
- `requests/results/<stem>.json` berisi `status=saved`, `request_id`, `video_id`, `video_path`, `source_blob_sha`, `shot_count`, `file_count` dan `run_id`. Ini hasil sukses bukan status live.

**Recovery:** request pending **immutable secara normal** dan tetap ada setelah run gagal. Maintainer memakai manual `workflow_dispatch` pada **path yang sama**, tanpa create-file atau request_id baru. Bila request harus diperbaiki, **cancel run**, pastikan tidak ada output sukses, lakukan PR perbaikan berizin dan teraudit, lalu dispatch request baru dari SHA terbaru. Jangan mengubah request normal diam-diam.

## 5. Verifikasi dan status
- **Queued / Processing:** request sudah ada, run masih pending/in_progress atau belum terverifikasi.
- **Saved:** run yang sesuai sukses, `requests/results/<id>.json` berisi request_id sama, paket `references/<id>` lengkap di remote `main`, Markdown marker dan gambar valid, serta commit terbukti. Jangan hanya percaya status result yang tidak cocok.
- **Already saved:** arsip legacy/filename-based untuk `video.filename` itu sudah ada, atau replay identik sudah diproses. Tautkan ID arsip sebenarnya.
- **Not saved / Failed:** run gagal, source SHA tidak cocok, request korup, konflik git, atau remote tidak lengkap. Tampilkan error dan jalur `workflow_dispatch` untuk recovery, jangan membuat request baru.

## 6. Kompatibilitas dan batasan
- Semua paket `references/VID-XXX/` lama dan video historis tetap utuh, tidak dimigrasi. Validator menerima ID legacy dan filename-based baru.
- `requests/save.json`/`requests/result.json` legacy tetap read-only; tidak dipakai oleh jalur baru.
- `analysis.yaml` tetap Schema 2.1 (tanpa `shot_narratives`); narasi Indonesia hanya disisipkan ke Markdown. Request baru wajib punya narasi lengkap. Legacy renderer tetap tersedia untuk membaca/tes arsip lama.
- **Optimasi instalasi FFmpeg terpisah** dari v1.4; pengujian regresi tetap berjalan.
- Perubahan rules/README **tidak otomatis mengubah Project Instructions ChatGPT**. Salin instruksi pembaruan dari README ke Project agar semua chat memahami v1.4.
- Jika konektor tidak dapat melakukan `create_file` baru dengan aman, jangan mengubah `save.json` lama sebagai fallback.

**Prinsip:** Analyze = Read Only · exact `save now` = one new immutable per-video request · independent Actions = render + optimistic publish · Verify remote before Saved.
