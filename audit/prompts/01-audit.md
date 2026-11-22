# Prompt mulai audit V2

Audit MP4 terlampir untuk pustaka HOMEKU. Buka homeku-audit-kit.zip, baca README, jalankan bootstrap runtime, lalu baca template JSON dan panduan pengisian. Kerjakan inspeksi video dan semua helper di workspace chat; saya cukup meninjau hasil dan mengunduh satu ZIP final.

Gunakan ID dari stem MP4. Jalankan inspect untuk hash/metadata/PTS aktual. Tentukan cut nyata, lalu periksa baseline 10 FPS sepanjang setiap shot termasuk frame native awal/akhir. Lihat gambar yang dipilih. Perdalam semua frame native pada rentang arah/fase/tempo/oklusi/detail yang belum jelas, termasuk seluruh shot bila perlu. Frame yang hanya diekstrak tidak ditandai viewed; model_build tidak diketahui null.

Tulis audit.json sebagai satu sumber: gaya utama/pengaruh/interior dengan istilah English dan style_names_language=en; estimasi luas lantai total berupa rentang angka wajib; detail Arsitektur, Furnitur dan properti, Lingkungan yang konkret; fakta konfigurasi/bukaan/penyimpanan/orientasi/status/bukti; posisi dan arah kamera awal, framing serta cahaya. Jangan mengisi ruangan generik atau memastikan material fisik yang tidak terlihat. Prosa penjelasan Indonesia; basis/uncertainty tetap JSON. MD luas cukup angka m² tanpa catatan tambahan.

Satu take tanpa cut tetap satu shot walau melewati beberapa area. Bedakan area fisik dari fungsi, visibility dari route, dan route dari fase kamera. Catat interval/rute/penghubung/reveal serta journey DNA multi area. Jangan mengarang denah atau kontinuitas dari urutan edit.

Terapkan aturan arah/fase: oklusi + paralaks + perspektif, pan berbeda dari orbit/truck; gerak benda di layar bukan arah kamera. Bedakan dolly/zoom dan smooth/tempo. Jitter vertikal kecil bukan tilt. Gunakan notasi English, + simultan, → berurutan, estimasi ~×/~° berdasar jangkar. Summary harus sejalan dengan fase; tempo_profile menyimpan perkembangan sedang/cepat/dll, bukan default slow. Pertahankan kronologi/durasi sumber tanpa reverse/default produksi.

Pilih frame asli untuk kolase: normal tepat Start/Middle/End; multi dinamis sesuai momen penting, bukan wajib lima. Pilih overview seluruh area penting, biasanya awal IN/akhir OUT. Overview bukan otomatis posisi awal produksi. Simpan pilihan indeks/PTS/bukti stabil; tidak ada JPEG frame kerja dalam ZIP final.

Jalankan draft-v2, periksa silang JSON/narasi/kamera/media, lalu review. Tampilkan storyboard, kolase semua shot dan analysis.md manusia lengkap yang dirender helper. Kamera sederhana dan teknis harus sejalan; semua bagian penting tetap tersedia tanpa tabel proses teknis dalam MD. Jangan mengarang fakta untuk lolos validator.

Tunggu koreksi atau pernyataan saya bahwa keseluruhan kandidat sesuai. Jangan membuat ZIP final dulu. Persetujuan satu gerakan atau tampilan bukan persetujuan seluruh audit. Tugas ini hanya audit/pengetahuan referensi, tanpa membuat konsep/gambar baru atau plugin produksi.
