Bagian yang paling banyak memakan waktu adalah **penulisan `audit.json` dan pencocokan bukti/struktur skema** (~6 menit dari total waktu dinding ~11 menit 16 detik, mulai `15:54:01Z` hingga `16:05:17Z`), disusul **ekstraksi dan pemeriksaan frame** (~2 menit 31 detik karena terkendala batas panjang ekspresi FFmpeg 5.1 sebelum `prepare` berhasil).

Berikut rincian kelima bagian berdasarkan log resmi `performance.jsonl` dan timestamp eksekusi aktual:

1. **Ekstraksi dan pemeriksaan frame (~2 menit 31 detik wall-clock, `15:55:28Z`–`15:57:59Z`)**
* Proses `prepare` yang berhasil sendiri hanya memakan **8,53 detik** (`performance.jsonl`: `15:56:40.20Z`–`15:56:48.73Z`, 132 frame dalam 3 batch).
* Namun sebelum itu dibutuhkan ~1 menit 12 detik untuk menangani kegagalan `prepare` pertama (lihat daftar pengulangan di bawah).
* Pemeriksaan visual seluruh 13 contact sheet (Shot 01–06 + midpoint) dan `mark-viewed` memakan ~56 detik (`15:57:03Z`–`15:57:59Z`).


2. **Analisis kamera, termasuk pengukuran piksel untuk estimasi ~×**
* **Pengukuran piksel (`scale_measurement`) tidak dijalankan (0 detik)** karena seluruh estimasi ~× dan ~° dibuat secara visual (`scale_measurement: null`) sesuai ketentuan sumber 2.4.
* Analisis visual arah/paralaks/jangkar (depth → translation → rotation) dilakukan menyatu saat pembacaan sheet dan penulisan narasi `audit.json`, sehingga durasinya tidak tercatat terpisah di log.


3. **Penulisan `audit.json` dan pencocokan bukti (~6 menit 3 detik wall-clock, `15:57:58Z`–`16:04:01Z` — bagian terlama)**
* ~2 menit 2 detik (`15:57:58Z`–`16:00:00Z`) dipakai membaca referensi tambahan (`json-guide.md`, `vocabulary.md`, `providers.md`, `template-audit.json`) dan mengecek definisi `audit-v2-4.schema.json`.
* ~4 menit 1 detik (`16:00:00Z`–`16:04:01Z`) adalah waktu sintesis dan penulisan penuh `audit.json` (19 klaim DNA, 6 shot, 36 fakta atomik + `facet_roles` + `fact_coverage`, `camera_checks`, `motion_observations`, serta pemisahan Camera Start vs Overview) dan `audit-info.json` — ini porsi waktu terbesar karena panjangnya payload JSON yang ditulis model.
* Eksekusi helper `complete` sendiri tercatat hanya **0,005 detik** (`performance.jsonl`: `16:04:01.935Z`–`16:04:01.940Z`).


4. **Perbaikan error validasi (~14 detik wall-clock, `16:04:01Z`–`16:04:15Z`)**
* Jumlah pengulangan: **1 kali** perbaikan dan `check-input` ulang.
* Error tercatat (3 item identik, grup `schema`):
* `/audit/identity/style_relations/0` — `Additional properties are not allowed ('uncertainty' was unexpected)`
* `/audit/identity/style_relations/1` — `Additional properties are not allowed ('uncertainty' was unexpected)`
* `/audit/identity/style_relations/2` — `Additional properties are not allowed ('uncertainty' was unexpected)`


* Setelah `uncertainty` dihapus dari `style_relations`, `check-input` ulang langsung lulus (`ok: true`, 0 error) dalam **0,047 detik** (`performance.jsonl`).


5. **Pembuatan kolase, laporan, dan ZIP (~1 menit 2 detik wall-clock, `16:04:15Z`–`16:05:17Z`)**
* `draft-v2` (render 8 JPEG: Overview, Storyboard, Shot 01–06, serta `analysis.md` dan `manifest.json`) memakan **15,51 detik** (`performance.jsonl`: `16:04:15.49Z`–`16:04:30.99Z`; khusus `render-media` **15,04 detik**).
* Pembuatan `review.md` + receipt `review.md.json` memakan ~4 detik (`16:04:31Z`–`16:04:35Z`), dan penampilan 9 file ke UI memakan ~25 detik (`16:04:51Z`–`16:05:17Z`).
* **Ekspor ZIP final (`export-v2`) belum dijalankan (0 detik)** karena menunggu persetujuan keseluruhan dari Anda.



**Pekerjaan yang diulang beserta penyebabnya:**

* **Ekstraksi `prepare` (diulang 1 kali + 1 kali gagal patch)**: FFmpeg 5.1 di sandbox gagal mem-parsing ekspresi filter `select=eq(n\,...)` dengan 132 frame sekaligus (`Cannot allocate memory` akibat batas rekursi parser ekspresi FFmpeg 5.1). Setelah satu kali gagal matching string saat menambal, `extract_many` di `video_cache.py` dipecah per 64 frame lalu `prepare` berjalan mulus.
* **Perintah `inspect` (diulang 1 kali)**: percobaan pertama memakai flag `--source`/`--output` yang tidak dikenali sebelum diulang dengan argumen posisional.
* **Pembacaan `template-audit.json` (diulang 1 kali)**: sempat mengakses path root alih-alih `audit/template-audit.json`.
* **Validasi `check-input` (diulang 1 kali)**: untuk menghapus properti `uncertainty` yang tidak diizinkan skema pada `identity.style_relations`.
* **Penampilan file kolase ke UI (1 kali retry untuk `shot-04.jpg`–`shot-06.jpg`)**: terjadi salah ketik nama tool pada pemanggilan `shot-04.jpg` sehingga tiga file terakhir dikirim ulang secara terpisah.