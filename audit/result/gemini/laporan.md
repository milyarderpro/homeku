Berdasarkan catatan timestamp eksekusi nyata pada sesi ini (total durasi audit dari ekstraksi kit hingga kandidat siap tinjau sekitar **24 menit 7 detik**, pukul `20:28:37–20:52:44 WIB`, ditambah **11 detik** untuk ekspor ZIP pada `21:02:13–21:02:24 WIB`), dua bagian yang paling banyak memakan waktu adalah **penulisan `audit.json` & pembacaan kontrak/schema (~8 menit 26 detik)** dan **perbaikan error validasi berulang (~8 menit 23 detik)**—keduanya menyumbang sekitar dua pertiga dari keseluruhan waktu.

| Bagian Proses | Rentang Waktu Nyata (WIB) | Perkiraan Durasi Tercatat | Ringkasan Beban Waktu |
| --- | --- | --- | --- |
| **Persiapan awal** (ekstrak, bootstrap, inspect, deteksi cut) | `20:28:37–20:29:58` | ~1 menit 21 detik | Termasuk jeda gangguan server VM yang memaksa ekstraksi & bootstrap diulang sekali. |
| **1. Ekstraksi & pemeriksaan frame** (baseline 6 FPS, contact sheet, pendalaman native) | `20:30:15–20:32:46` + sisipan saat pendalaman & re-sample | ~2 menit 31 detik di awal (+ ~1 menit 2 detik tersebar saat pendalaman & re-sample) | Eksekusi `sample` 6 shot cepat (~18–23 detik/putaran), tetapi terakumulasi karena `sample` baseline diulang 3 kali dan pendalaman native dilakukan dalam 2 gelombang. |
| **2. Analisis kamera & ukur piksel `~×**` | `20:32:58–20:34:38` | ~1 menit 40 detik | Melihat 6 grid koordinat 720×1280 (`11 detik`) dan menghitung rasio skala serta verifikasi sumbu depth/translation/rotation (`~1 menit 29 detik`). Tidak ada pengulangan. |
| **3. Penulisan `audit.json` & pencocokan bukti** | `20:34:38–20:43:04` | ~8 menit 26 detik | **Terlama #1.** Membaca 6 dokumen panduan + schema + template (`~2 menit 1 detik`), lalu menyusun skrip `work/build_audit.py` berisi seluruh 18 klaim DNA, 6 shot, fakta, `camera_checks`, dan `scale_measurement` (`~5 menit 10 detik` dalam satu giliran). |
| **4. Perbaikan error validasi** | `20:43:04–20:50:55` | ~7 menit 51 detik (hingga percobaan ke-9 siap jalan) | **Terlama #2.** Tercatat **8 kali kegagalan validasi** beruntun sebelum lulus pada percobaan ke-9; 4 kegagalan terakhir masing-masing memakan ~23–27 detik karena `draft-v2` sudah sempat merender media sebelum gagal di validasi `manifest`/`audit-info`. |
| **5. Pembuatan kolase, laporan, verifikasi, & ZIP** | `20:50:55–20:52:44` & `21:02:13–21:02:24` | ~1 menit 36 detik (32 dtk render lulus + 53 dtk cek & tampilkan + 11 dtk ZIP) | Proses render final `draft-v2` + `review` yang lulus hanya **32 detik**, dan `export-v2` ZIP final hanya **11 detik**. |

### Rincian 8 Error Validasi Tercatat (Bagian 4)

Percobaan `draft-v2` dijalankan **9 kali** (8 gagal, lulus pada percobaan ke-9 di `20:50:55–20:51:27 WIB`):

1. **`relations/0: 'id' is a required property`** (`20:43:08`) — Objek `relations` belum menyertakan field wajib `id`, `description`, dan `uncertainty`.
2. **`Middle panel must be nearest native midpoint`** (`20:43:53`) — Penentuan *tie-breaker* titik tengah memilih `f79` (bukan `f80`) di shot-01 dan `f392` (bukan `f391`) di shot-04; memicu ekstraksi dan peninjauan visual tambahan untuk kedua frame tersebut.
3. **`Parsed component metadata differs from raw notation`** (`20:45:20`) — Nilai `direction` pada `components_parsed` tidak persis sama dengan parser internal kit (`homeku.markdown.component`). Sempat terjadi 1 kesalahan impor fungsi (`homeku.validation.parse`) di `20:46:00` sebelum menemukan fungsi yang tepat.
4. **`Unknown related shot`** (`20:46:32`) — Field `relations.from`/`to` sempat diisi ID area (`area-01`) alih-alih ID shot (`shot-01`).
5. **`frame_reviews/1/mode: 'native' is not one of ['sampling', 'frame-by-frame']`** (`20:47:06`, ~23 dtk) — Mode log pendalaman ditulis `"native"`, padahal schema mewajibkan `"frame-by-frame"`.
6. **`Selected frame indices differ from native PTS selection`** (`20:48:06`, ~27 dtk) — Daftar `selected_frame_indices` yang ditulis manual pada `audit-info.json` berbeda dari template `sampling.json` hasil `tools/audit.py sample`.
7. **`Frame review incomplete: declare only frames actually viewed`** (`20:49:01`, ~27 dtk) — Setiap record pendalaman native memilih 4–5 frame, sedangkan baru 2 frame per record yang ditandai `viewed`; mengharuskan pembuatan dan pemeriksaan lembar kontak 24 frame (`deep-all.jpg`).
8. **`Frame review outside shot`** (`20:49:58`, ~27 dtk) — Rentang `--start` pada `sample` baseline shot-03/04/05 sebelumnya dibulatkan 3 desimal (`8.366`, `11.533`, `14.566`) sehingga lebih awal `0.000667` detik dari `shot.start_s`.

### Pekerjaan yang Diulang dan Penyebabnya

* **Ekstraksi kit & bootstrap (diulang 1×):** Terputus akibat gangguan server VM (*server shutdown*) pada `20:29:07` sehingga direktori kerja sempat kosong dan harus diekstrak ulang.
* **Ekstraksi `sample` baseline 6 FPS (dijalankan 3×):**
* Putaran 1 (`20:30:15`): pembulatan `--end` membuat frame terakhir native shot-02 s.d. shot-05 kurang 1 frame.
* Putaran 2 (`20:32:30`): `--end` diperbaiki agar frame terakhir masuk, tetapi `--start` masih dibulatkan 3 desimal.
* Putaran 3 (`20:50:14`): diulang penuh untuk 6 shot memakai batas 9 desimal persis dari `audit.json` demi memperbaiki error `Frame review outside shot`.


* **Pendalaman native & pembacaan gambar kerja (2 gelombang + beberapa retry `view_file`):** Gelombang pertama (`20:36:37`) mengambil titik tengah shot-02/03/05/06; gelombang kedua (`20:44:51`) ditambahkan khusus untuk `f79` (shot-01) dan `f392` (shot-04) akibat *tie-breaker* midpoint. Beberapa pemanggilan `view_file` sempat gagal tepat setelah pembuatan file (`template-audit.json`, `midpoints-01-04.jpg`, `deep-all.jpg`) sehingga harus dibaca ulang pada giliran berikutnya.
* **Render media di dalam `draft-v2` (terulang 4× sebelum lulus):** Karena validator `manifest`/`audit-info` berjalan setelah tahap render JPEG, 4 kegagalan terakhir (#5–#8) masing-masing mengulang proses render media sebelum akhirnya gagal.

Tidak ada langkah audit atau hasil akhir yang diulang maupun diubah pada jawaban ini.