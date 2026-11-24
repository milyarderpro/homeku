Bagian yang paling banyak memakan waktu adalah **penulisan `audit.json` beserta pencocokan skema dan bukti** (sekitar **5 menit 26 detik** untuk generasi isi JSON saja, atau **~6 menit 31 detik** bila digabung dengan pembacaan panduan dan skema). Sebaliknya, seluruh eksekusi alat resmi di mesin (`prepare`, `motion-hints`, `complete`, `check-input`, `draft-v2`, dan `review`) total hanya memakan **~29,4 detik** berdasarkan `performance.jsonl`.

Berikut rincian kelima bagian berdasarkan timestamp eksekusi aktual (WIB) dan `performance.jsonl` (rentang total `14:18:18`–`14:30:44`, tidak ada durasi atau persentase yang dikarang):

1. **Ekstraksi dan pemeriksaan frame**
* **Ekstrak kit, bootstrap, baca panduan (`README.md`, `visual-audit.md`, `authoring.md`, `camera-cases.md`), dan `inspect` + deteksi cut:** `14:18:37`–`14:20:04` (~1 menit 27 detik).
* **`prepare` (ekstraksi 132 frame baseline 6 FPS + midpoint via 5 panggilan FFmpeg):** `14:20:17`–`14:20:26` (**9,31 detik** tercatat di `performance.jsonl`).
* **Pemeriksaan visual 13 lembar gambar (12 pass) hingga deklarasi `mark-viewed`:** `14:20:26`–`14:22:15` (~1 menit 49 detik, mencakup 2 batch pembacaan gambar dan penalaran visual sebelum `mark-viewed`). Tidak ada pendalaman 10 FPS atau native tambahan.


2. **Analisis kamera, termasuk pengukuran piksel untuk estimasi ~×**
* **Pengukuran piksel (`scale_measurement`):** tidak dijalankan (`0 detik`); seluruh estimasi `~×` dan `~°` dilakukan secara visual (`scale_measurement: null`).
* **Helper opsional `motion-hints` 2D (6 shot dari cache, 0 panggilan FFmpeg):** `14:22:16`–`14:22:19`, total **2,45 detik** (`shot-01`: 0,60s; `shot-02`: 0,39s; `shot-03`: 0,39s; `shot-04`: 0,38s; `shot-05`: 0,34s; `shot-06`: 0,36s).
* Penalaran arah kamera menyatu dalam tahap pemeriksaan visual (`14:20:26`–`14:22:15`) dan perumusan `camera_checks`/`motion_observations` saat menulis `audit.json` (tidak memiliki log durasi terpisah).


3. **Penulisan `audit.json` dan pencocokan bukti *(terlama)***
* **Membaca panduan skema (`json-guide.md`, `vocabulary.md`, `providers.md`, `audit-v2-5.schema.json`):** `14:22:14`–`14:23:19` (~1 menit 5 detik).
* **Menulis penuh `work/audit/audit.json` (6 shot lengkap, 18 item `profile`, 6 `areas`, 5 `relations`, `facts`, `facet_roles`, `fact_coverage`, `camera_checks`, `motion_observations`, `overviews`) dan `audit-info.json`:** `14:23:19`–`14:28:45` (**~5 menit 26 detik**). Sebagian besar jeda ini merupakan waktu generasi teks JSON panjang oleh model, bukan eksekusi sistem.


4. **Perbaikan error validasi**
* Total rentang: `14:28:46`–`14:29:22` (**~36 detik**, **2 kali putaran perbaikan**):
* **Putaran 1 (`14:28:46`–`14:29:04`):** `check-input` mencatat **2 error skema** pada `/audit/shots/2/panels/2` dan `/audit/shots/4/panels/2` (`'label' is a required property`), lalu diperbaiki dengan menambahkan `"label": "End"`.
* **Putaran 2 (`14:29:04`–`14:29:22`):** `check-input` dan preflight `draft-v2` (0,13 detik) mencatat **6 error**: 5 error `scope` pada `/relations/0` s.d. `/relations/4` (`Unknown related shot; area IDs belong in area_relations`) dan 1 error `semantics` pada `/audit` (`Ease-Out/Decelerating conflicts with speed_change`). Keduanya diperbaiki dengan mengganti `from`/`to` relasi ke ID shot (`shot-01`..`shot-06`) serta mengubah `speed_change` pada `shot-03` menjadi `"decelerating"`. Setelah itu `check-input` slulus (`ok: true`, 0,056 detik).




5. **Pembuatan kolase, laporan, dan ZIP**
* **`draft-v2` (render 8 JPEG + `analysis.md` + `manifest.json`):** `14:29:22`–`14:29:37` (**15,33 detik** total; render media 14,84 detik dari cache tanpa FFmpeg ulang).
* **`review` (`review.md`, receipt `review.md.json`, dan inventaris fakta):** `14:29:38`–`14:29:40` (**2,24 detik**).
* **Verifikasi visual hasil render, penyalinan file output, dan penayangan 9 file ke chat/Canvas:** `14:29:40`–`14:30:44` (~1 menit 4 detik).
* **Ekspor ZIP (`export-v2`):** belum dijalankan (`0 detik`) karena menunggu persetujuan keseluruhan Anda.



**Pekerjaan yang diulang dan penyebabnya**

* **`inspect` (1 kali pengulangan):** pemanggilan pertama gagal (`exit code 2`) karena memakai flag `--source`/`--work-dir`, lalu diulang dengan argumen posisional.
* **`complete` dan `check-input` (masing-masing dijalankan 3 kali; total komputasi < 0,1 detik):** diulang karena 2 error skema `label` panel yang terlewat pada putaran 1, lalu 5 error ID relasi dan 1 konflik `Ease-Out` vs `speed_change` pada putaran 2.
* **`draft-v2` dan `review` (1 kali gagal preflight sebelum sukses):** pada putaran perbaikan pertama keduanya dirangkai langsung setelah `check-input`, sehingga `draft-v2` berhenti di preflight (0,13 detik, belum merender gambar) dan `review` gagal karena kandidat belum terbentuk; keduanya sukses pada eksekusi berikutnya.
* **Tidak ada pengulangan ekstraksi frame maupun render ulang kolase** (`batch_retries: 0`, 8 media hanya dirender satu kali).