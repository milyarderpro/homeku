# Pilot audit penuh sebelum rilis HOMEKU 3.1

## Jalankan di ChatGPT dengan Google Drive

Buka satu chat ChatGPT untuk [MP4 dreamshome01](../../video/dreamshome01.mp4). Berikan tautan root Drive `HOMEKU`. Ambil MP4 asli dari `Video` dan [kit 3.1](../homeku-audit-kit.zip) dari root. Gunakan [prompt audit lengkap](../prompts/01-audit.md) dan jalankan empat fase sampai ZIP final. Tampilkan laporan, media, dan ZIP di chat. Setelah pengguna memilih paket, verifikasi byte ZIP di Drive sesuai [panduan ekspor](../prompts/03-export.md).

Simpan ringkasan kamera fase 2 beserta keluaran `check-camera` dan ZIP final. Catat provider dan model yang diketahui, ringkasan `performance` per fase dan percobaan, interval 10 FPS/native tambahan, serta penggunaan `motion-hints` dan pengukuran jangkar. Cocokkan notasi per shot di fase 2 dengan `audit.json` dan `analysis.md` dalam ZIP. Jika ada koreksi setelah fase 2, sertakan hasil scoped recheck terkait.

## Acuan review `dreamshome01`

Bandingkan dengan [ZIP pilot awal](../../docs/runpilot/dreamshome01-r0001.zip) dan [MP4 kanonis](../../video/dreamshome01.mp4). Waktu pada tabel mengikuti video utuh. Sudut dan skala adalah estimasi visual, sehingga kesesuaian fase, komponen, dan arah dinilai terpisah.

| Shot dan interval | Pembanding dan bukti yang diperiksa |
| --- | --- |
| 01 · 0,00–6,13 s | Orbit Right di awal, lalu Straight Dolly-In (~1.6×–2×) menuju tangga dan teras. Bandingkan F0, F60 dan F176. Pohon dekat bergeser ke kiri relatif terhadap rumah dan sisi kanan teras terbuka. Nilai pembesaran awal sebelum memakai Pure. |
| 02 · 6,13–9,60 s | Dolly-Out (~1.75×) + Orbit Right + Pan Left berlangsung bersamaan. Dari F194–F287, perapian mengecil dan tersapu ke kanan sementara orientasi meja terhadap dinding berubah. F184 adalah Start native yang kabur dan F194 pada 6,47 s adalah pembanding acuan produksi. |
| 03 · 9,60–13,10 s | Straight Dolly-In → Dolly-In + Strong Pan Right (~25°). Wastafel relatif terpusat pada F288–F348, kemudian bergeser ke kiri hingga F392 saat bidang kompor makin terbuka. Tentukan batas fase dari perbandingan di sekitar kemunculan sapuan. |
| 04 · 13,10–16,57 s | Diagonal Dolly-Out (~1.75×) + Gentle Pan Left. Bandingkan F393, F445 dan F496 untuk pelebaran ruang serta pergeseran bukaan. |
| 05 · 16,57–20,03 s | Dolly-In (~2.5×) + Gentle Pan Right (~15°). Bandingkan bagian bawah bingkai jendela pada F497–F600 untuk pertumbuhan skala dan koreksi arah pandang. |

## Dua cek tambahan

- **`edh033` Shot 02.** Bandingkan F268, F336, dan F384 (8,93–12,80 s). Apakah ranjang dan jangkar dekat membesar secara berbeda saat kamera mendongak? Nilai dukungan untuk Dolly-In bersama Tilt-Up. [MP4](../../video/edh033.mp4) · [ZIP pilot](../../docs/runpilot/v3.0/edh033-r0001.zip)
- **`edh056` Shot 01.** Bandingkan F0, F20, F40, F60 dan F75 (0–2,50 s). Nilai arah gerak pohon dekat relatif terhadap fasad dan perubahan sudut bidang rumah. Tentukan apakah pola mendukung Orbit Left dengan Pan Right atau tafsir lain. [MP4](../../video/edh056.mp4) · [ZIP pilot](../../docs/runpilot/v3.0/edh056-r0001.zip)

## Pemeriksaan visual terdahulu

- **`dreamshome01` Shot 01–03.** F0–F60 memperlihatkan sisi kanan teras terbuka dan perubahan skala mulai terlihat, sehingga fase orbit didukung sementara qualifier Pure masih perlu kehati-hatian. F194–F287 memperlihatkan perapian mengecil dan bergeser ke kanan relatif terhadap perubahan orientasi meja. Ini mendukung Orbit Right dan Pan Left saat mundur. Di dapur, sapuan kanan mulai terbaca setelah F348 dan paling jelas menuju F392. PTS batas persis mengikuti analisis di sekitar perubahan.
- **`dreamshome01` Shot 04–05.** Ruang kamar tidur membuka ke kiri saat kamera mundur. Lebar bagian bawah bingkai jendela kamar mandi bertambah dari sekitar 170 menjadi 425 piksel. Dukungan untuk Dolly-In sekitar 2,5× lebih jelas daripada estimasi sudut Pan yang mengikuti perubahan arah pandang.
- **`edh033` Shot 02.** F268–F384 memperlihatkan lebih banyak plafon, dengan ranjang loft dan meja bawah ikut membesar. Bukti menunjukkan kemungkinan pendekatan bersamaan dengan Tilt-Up, terutama di bagian akhir. Awal pendekatan dan rasionya masih perlu pembeda karena rotasi juga mengubah proyeksi.
- **`edh056` Shot 01.** Batang terdekat bergerak lebih ke kanan daripada fasad hingga sekitar F40, sementara bidang sisi rumah berubah. Ini mendukung lintasan Orbit Left. Pan Right sebagai kompensasi masih berupa tafsir visual dan sudutnya belum dipisahkan.
- **Production Start.** Preview terisolasi dari ZIP `dreamshome01-r0001.zip` menampilkan F194 (6,47 s) setelah Camera Start. F184 (6,13 s) tetap menjadi Start native pada Shot 02. Ekstraksi keduanya melalui reader cocok byte demi byte dengan ekstraksi dari MP4 kanonis, dan pilihan panel serta batas audit tetap sesuai sumber. Preview memakai notasi kamera dari ZIP pilot agar perubahan acuan produksi dapat diperiksa tersendiri.

## Catatan perbandingan

| Provider dan model | Shot / PTS | Fase | Komponen dan arah | Estimasi | Frame pembeda / pendalaman | Hasil vs. acuan |
| --- | --- | --- | --- | --- | --- | --- |

Catat satu baris per shot dan tandai hasil yang sesuai, berbeda, atau masih ambigu. Periksa tiga keputusan utama sebelum menyatakan siap rilis. Shot 01 dan 03 harus menangkap perubahan urutan. Shot 02 harus menangkap komponen simultan dan memilih frame produksi yang layak. Bandingkan waktu dan percobaan dengan baseline jika baseline terukur tersedia. Periksa interval yang memerlukan pendalaman dan perubahan yang terlihat pada lembar review setelah koreksi.

## Hasil pilot rilis 26 November 2026

Pilot ChatGPT yang memakai GPT-6.2 melaporkan OpenCV 4.13.0 dan NumPy 2.3.5 lulus `readiness`. [Chat pilot dreamshome01](https://chatgpt.com/g/g-p-6b07e31e53dc8191b48648575e8a7984-home-drive/c/6b080488-6858-83ec-a266-e84708b381a3)

| Fase | Durasi yang dilaporkan |
| --- | --- |
| Pemetaan shot | 38,89 dtk |
| Kamera | 169,98 dtk |
| Desain dan media | 69,33 dtk |
| Validasi dan ekspor | 140,29 dtk |

Empat fase berjumlah 418,49 detik dan mencakup 11 percobaan yang tercatat pada enam perintah utama. Semua 11 percobaan lulus. Checklist melaporkan perubahan bukti pada Shot 01 setelah koreksi. Data waktu berasal dari ringkasan di chat pilot. Baseline terinstrumentasi dilewati sesuai arahan pengguna.

ZIP unduhan lulus validasi lokal terhadap MP4 kanonis, termasuk frame map, laporan hasil renderer, dan tujuh JPEG. SHA-256 ZIP cocok dengan hasil ekspor, yaitu `df318b0e88fa009656ed81ad31d44f89648194358d08e3d59df24be213b5e98f`. Hash snapshot adalah `acb072d59327a570795cfc63eb08ef0b25bede8afcdeff25c265fcfab4976750`. Cut F184, F288, F393, dan F497 membentuk lima shot. Overview dan Storyboard ditinjau dari ZIP unduhan.

- **Shot 02.** F184 menampilkan transisi kabur. F192 pada 6,40 detik tampak jernih dan tampil sebagai Production Start serta panel Start. F194 yang dipakai pembanding juga jernih.
- **Shot 03.** Pengukuran yang dilaporkan untuk F288–F338 memberi 154→191,28 px atau sekitar 1,24× pada bagian awal fase. Frame pembanding memperlihatkan pembesaran diikuti sapuan kanan yang paling jelas menuju F392.
- **Shot 05.** Estimasi `~1.7×` dalam ZIP perlu dikoreksi sebelum memilih paket. Pada F497 dan F600, pembacaan manual tepi bawah daun jendela yang sama memberi panjang sekitar 160→430 px atau sekitar 2,7×, searah dengan acuan terdahulu yang sekitar 2,5×. Komponen Pan Right perlu dinilai tersendiri dari frame di sepanjang shot.

ZIP pertama selesai diekspor dan unduhannya tervalidasi sebelum koreksi Shot 05.

### Koreksi Shot 05

ZIP koreksi r0001 lulus validasi terhadap MP4 kanonis. SHA-256 hasil unduhan cocok dengan ekspor dari chat pilot, yaitu `e8779f7e84ec331f88a368ce2f454f5e21e1e1fe39ed3a65a2e6fc14e72dbc0f`. Hash snapshot hasil koreksi adalah `8cc764e8eea134ba799a62736e2e8d227b6c091e82d71c0bd54eb48d7518e111`.

Shot 05 memakai `Dolly-In (~2.7×) (Ease-Out)`. Pengukuran tepi bawah daun jendela yang sama pada F497–F600 memberi 159,00→428,73 px atau 2,696×. Posisi pusat jendela bergeser sedikit ke kiri lalu kembali ke kanan. Bukti tersebut belum menguatkan Pan Right sebagai komponen tersendiri. Selisih isi audit terbatas pada blok kamera Shot 05. Pilihan frame panel cocok dengan versi pertama. Media yang berbeda adalah kolase Shot 05 dan Storyboard.

### Penyerahan ke Google Drive

- **Review teknis.** ZIP terkoreksi lulus validasi lokal terhadap MP4 kanonis dan perbandingan dengan ekspor sebelum koreksi.
- **Pilihan paket.** Saat pengguna meminta hasil akhir disimpan di HOMEKU, paket yang diserahkan adalah ekspor terkoreksi Shot 05.
- **Ekspor.** Paket r0001 dari sesi pilot berukuran 8.945.135 byte.
- **Transfer.** Paket tersimpan di `HOMEKU/Hasil Audit`. Baca kembali dari Drive menghasilkan SHA-256 `e8779f7e84ec331f88a368ce2f454f5e21e1e1fe39ed3a65a2e6fc14e72dbc0f`, cocok dengan ekspor. [ZIP final terkoreksi](https://drive.google.com/file/d/1IYIQLCJXKp8GRWsBPky5m2KyOUJuWJyU/view)
- **Verifikasi di ChatGPT.** Chat pilot membaca struktur HOMEKU dan melaporkan bahwa byte ZIP dari Drive identik dengan hasil koreksi. [Chat pilot dreamshome01](https://chatgpt.com/g/g-p-6b07e31e53dc8191b48648575e8a7984-home-drive/c/6b080488-6858-83ec-a266-e84708b381a3)
