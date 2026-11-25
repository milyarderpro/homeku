# Koreksi audit HOMEKU 3.0

Terapkan koreksi saya pada `audit.json` kerja. Temukan bukti terkait lalu periksa ulang bagian yang masih ambigu dengan pendalaman 10 FPS atau native. Pertahankan catatan yang sudah cocok. Jika koreksi menyangkut kamera, baca `audit/camera-cases.md` sebelum memeriksa fase yang terdampak. Nilai kembali jenis, arah, lintasan, intensitas, profil laju, dan besaran setiap komponen. Cantumkan rincian dan estimasi ~× atau ~° yang didukung frame di `notation`.

Jika koreksi menyangkut Profil Desain, perbarui klaim tipe rumah atau aspek terkait pada sumber audit. Untuk koreksi palet, perbarui entri `design.palette` dan bukti frame yang bersangkutan.

Koreksi label area dan label momen di sumber audit agar laporan dan media konsisten. Pakai bahasa Inggris Title Case, `&` untuk fungsi dalam satu area, serta fungsi eksplisit di `areas[].functions`. Pemisah ` / ` ditambahkan renderer antararea. Gunakan istilah Inggris pada nilai teknis pencarian dan bahasa Indonesia pada narasi.

Selaraskan fakta, narasi, komposisi, notasi, fase, dan tempo yang terdampak. Jika koreksi terpusat pada satu shot, gunakan `update-shot` dengan file patch JSON. Isi deklarasi viewed hanya untuk frame yang benar-benar sudah dilihat. Jalankan complete dan draft.

Ikuti checklist isi di `audit/authoring.md`. Untuk koreksi kamera, cocokkan kembali `notation` dengan `observations` dan bukti temporal sebelum ekspor. Setelah kandidat terbaru lulus validasi, jalankan `review` dan langsung `export --receipt` dengan receipt terbaru. Tampilkan ulang laporan dan tautan unduhan ZIP terbaru.
