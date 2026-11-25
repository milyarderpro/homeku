# Mulai audit HOMEKU 3.0

Audit video MP4 terlampir untuk pustaka HOMEKU. Ekstrak kit, jalankan `python homeku_runtime.py --output .`, lalu baca `audit/visual-audit.md` dan `audit/authoring.md`. Wajib baca `audit/camera-cases.md` sebelum analisis kamera.

Konfirmasi cut nyata dan jalankan prepare. Periksa baseline 6 FPS serta frame batas native. Sumber ≤6 FPS dan shot <1 detik memakai seluruh native. Gunakan 10 FPS atau native tambahan untuk menjawab pertanyaan visual tertentu. Satu take kontinu boleh memperlihatkan beberapa area.

Periksa depth, translation, dan rotation sebelum menentukan gerak. Untuk setiap fase dan komponen, evaluasi jenis, arah, lintasan, intensitas, profil laju, dan besaran. Masukkan rincian yang didukung frame ke `notation`, termasuk gerak sekunder dan estimasi ~× atau ~° yang wajar. Bandingkan beberapa interval waktu setara untuk menilai perubahan laju. Pisahkan tempo dari fase dan intensitas. Ikuti kronologi video sumber.

Isi Profil Desain dari frame. Pilih tipe rumah paling sesuai dalam bahasa Inggris, termasuk label baru bila relevan. Gunakan `uncertain` untuk perkiraan yang wajar. Tulis susunan ruang, pencahayaan, atmosfer, dan lingkungan. Pilih warna utama dari bagian frame yang pencahayaannya merata, lalu isi nama, peran, HEX, dan bukti tiap warna.

Tulis nama gaya dalam bahasa Inggris, luas lantai sebagai rentang angka, serta uraian arsitektur, furnitur, lingkungan, dan framing dalam bahasa Indonesia. Catat fakta eksplisit dengan bukti dan statusnya. Camera Start menjelaskan awal sumber. Overview menjelaskan frame wide yang dipilih.

Deklarasikan viewed setelah melihat frame. Sebelum ekspor, ikuti checklist di `audit/authoring.md` dan cocokkan kelengkapan `notation` dengan `observations` serta frame bukti yang sudah dilihat. Jalankan `complete`, `check-input`, dan `draft`. Jika kandidat lulus validasi, jalankan `review` dan langsung `export --receipt` untuk membuat ZIP tanpa MP4 dalam sesi ini. Berikan tautan unduhan ZIP bersama hasil audit.
