# Tasks

## 1. Pengukuran performa dan baseline

- [x] 1.1 Perluas `audit_performance` dengan penanda empat fase, ID percobaan, durasi, hasil, dan ringkasan. Uji pasangan event lengkap, fase atau percobaan terputus, dan pembacaan log lama.
- [x] 1.2 Hubungkan `check-camera`, `complete`, `check-input`, `draft`, `review`, dan `export` ke log workspace. Uji preflight `ok: false` yang dilanjutkan dengan percobaan berhasil, kegagalan CLI, korelasi review/ekspor lewat hash, serta ikatan sesi dan pencatatan kegagalan ekspor.
- [x] 1.3 Dokumentasikan penanda fase di panduan dan prompt.

Pengambilan baseline `dreamshome01` sebelum optimasi dilewati sesuai arahan pengguna.

## 2. Kesiapan, status sesi, dan cut

- [x] 2.1 Tambahkan pemeriksaan kesiapan runtime, akses tulis, dan decode satu frame. Dokumentasikan cara memakainya dan uji jalur sukses dan kegagalan saat OpenCV atau NumPy tidak tersedia.
- [x] 2.2 Tambahkan status sesi dari baseline, checkpoint kamera, dan receipt. Uji sesi parsial, status deklarasi lintas pass, koreksi satu shot, serta receipt yang hilang, usang, atau berasal dari sesi lain. Dokumentasikan cara melanjutkan dari hasil status.
- [x] 2.3 Tambahkan mode pratinjau `inspect` dengan pratinjau terbatas dan indeks/PTS native. Uji cut yang diketahui, cakupan PTS yang tidak seragam, dan alur ketika auditor mengabaikan dugaan cut. Perbarui tahap pemetaan shot di panduan.

## 3. Pengukuran jangkar kamera

- [x] 3.1 Tambahkan pengukuran manual dua titik pada dua frame native yang terikat sesi. Uji pembesaran, pengecilan, panjang nol, koordinat di luar frame, serta frame berbeda shot.
- [x] 3.2 Tambahkan usulan titik melalui OpenCV, periksa maju-mundur, dan sediakan keluaran visual untuk koreksi titik. Uji tracking dengan pergeseran terukur, tracking terputus, fallback manual, dan status `viewed` sebelum serta setelah pengukuran.
- [x] 3.3 Perbarui metode kamera dengan langkah `motion-hints`, konfirmasi titik, dan pemakaian hasil sebagai bukti skala 2D. Pedoman mewajibkan upaya estimasi visual per komponen dan alasan spesifik ketika estimasi dihilangkan. Verifikasi contoh perintah di kit yang diekstrak.

## 4. Pengisian dan koreksi audit

- [x] 4.1 Tambahkan operasi untuk satu fase kamera dan satu fakta area di audit kerja. Uji penambahan pada kerangka, koreksi satu entri, hash audit yang sudah usang, target atau bukti yang tidak valid, serta pelestarian isi dan asosiasi override pada perubahan notasi.
- [x] 4.2 Hubungkan perubahan kamera ke pemeriksaan ulang per shot. Tambahkan contoh koreksi di panduan JSON. Uji bahwa `check-camera --shot-id` memeriksa cakupan bukti override ketika visibilitas area sudah tercatat, termasuk setelah penyuntingan dengan `update-shot`.

## 5. Review, koreksi, dan penyerahan Drive

- [x] 5.1 Hasilkan lembar review dengan tautan ke laporan dan media kandidat. Uji hasil untuk shot biasa dan multi-area, provenance native dan deklarasi sesi, tautan yang tetap mengacu pada snapshot lama, serta kecocokan receipt dan retensi ZIP saat koreksi.
- [x] 5.2 Simpan ringkasan pembanding per sesi dan hash. Uji review pertama, review ulang terhadap hash yang sama, serta kandidat terkoreksi dengan perubahan notasi, frame dan cakupan bukti, komponen override, pilihan dan cakupan panel, serta hash media.
- [x] 5.3 Perbarui prompt mulai, koreksi, dan ekspor untuk folder HOMEKU. Periksa bahwa alur mencakup pemilihan satu MP4, review media dalam chat, ZIP pilihan pengguna, verifikasi SHA-256 di Drive, serta jalur unduhan ketika aksi unggah belum tersedia.

## 6. Verifikasi rilis

- [x] 6.1 Bangun ulang kit dengan runtime, panduan, dan prompt terbaru. Jalankan `python -m unittest discover -s tests -t . -v`, `python tools/library.py check`, dan `python tools/build_audit_kit.py --check`.
- [x] 6.2 Jalankan pilot `dreamshome01` dari folder HOMEKU di ChatGPT sampai ZIP final. Catat durasi fase dan percobaan. Jika tersedia baseline terukur, bandingkan keduanya. Periksa cut, fase dan arah kamera, `~×`, Production Start, serta keterbacaan perubahan setelah koreksi. Simpan hasil observasi dari build yang benar-benar digunakan pada pilot.
- [x] 6.3 Setelah pengguna memilih ZIP dari chat pilot, uji penyerahan di workspace ChatGPT target. Catat tautan Drive dan kecocokan SHA-256 setelah baca kembali, atau catat hasil jalur unduhan bila aksi unggah tidak tersedia. Catat review teknis, pilihan pengguna, ekspor, dan transfer Drive sebagai status terpisah.

### Bukti verifikasi

- **Build lokal terbaru.** 167 tes lulus. Pemeriksaan pustaka, OpenSpec, dan kesesuaian ZIP kit lulus untuk build `af15d70848283d147c4dcf0274dfc91f6a79f147dcb908ff3735a0da67d16888`.
- **Pilot ChatGPT dan transfer.** Hasil audit serta pembacaan ulang ZIP pilihan di Drive merujuk pada build terdahulu. Bukti tercatat di [catatan pilot](../../../audit/pilots/camera-release-check.md). Dampak panduan terbaru pada kelengkapan notasi masih perlu diuji di ChatGPT.
