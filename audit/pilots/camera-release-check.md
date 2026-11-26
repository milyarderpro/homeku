# Pilot audit penuh sebelum rilis HOMEKU 3.1

## Jalankan di GPT dan Gemini

Buka satu chat baru di setiap provider. Lampirkan [MP4 dreamshome01](../../video/dreamshome01.mp4) dan [kit 3.1](../homeku-audit-kit.zip) yang sama. Salin [prompt audit lengkap](../prompts/01-audit.md) dan jalankan empat fase sampai ZIP final. Gunakan acuan di halaman ini setelah hasil dari kedua chat tersedia.

Simpan ringkasan kamera fase 2 beserta keluaran `check-camera` dan ZIP final. Catat provider, model, waktu total, interval 10 FPS/native tambahan, serta penggunaan motion-hints. Cocokkan notasi per shot di fase 2 dengan `audit.json` dan `analysis.md` dalam ZIP. Jika ada koreksi setelah fase 2, sertakan hasil scoped recheck terkait.

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

Untuk tiap provider, catat satu baris per shot dan tandai hasil yang sesuai, berbeda, atau masih ambigu. Periksa tiga keputusan utama sebelum menyatakan siap rilis. Shot 01 dan 03 harus menangkap perubahan urutan. Shot 02 harus menangkap komponen simultan dan memilih frame produksi yang layak. Ukur waktu audit dari kedua sesi dan periksa apakah tambahan waktu berasal dari interval yang memang memerlukan pendalaman.
