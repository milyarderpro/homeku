# Mulai audit HOMEKU 3.0

Audit video MP4 terlampir untuk pustaka HOMEKU. Ekstrak kit, jalankan `python homeku_runtime.py --output .`, lalu baca `audit/visual-audit.md` dan `audit/authoring.md`. Wajib baca `audit/camera-cases.md` sebelum analisis kamera.

Konfirmasi cut nyata dan jalankan prepare. Periksa baseline 6 FPS serta frame batas native. Sumber ≤6 FPS dan shot <1 detik memakai seluruh native. Gunakan 10 FPS atau native tambahan untuk menjawab pertanyaan visual tertentu. Satu take kontinu boleh memperlihatkan beberapa area.

Cari batas fase dari awal, tengah, akhir, dan frame di sekitar perubahan. Periksa depth, translation, dan rotation. Gunakan jangkar dekat, jangkar jauh, dan sudut bidang untuk membedakan lintasan badan dari sapuan Pan. Setelah komponen dan arahnya jelas, isi `notation` dengan qualifier serta estimasi ~× atau ~° yang didukung. Gunakan interval waktu setara untuk profil laju dan nilai tempo tersendiri.

Isi Profil Desain dari frame. Pilih tipe rumah paling sesuai dalam bahasa Inggris, termasuk label baru bila relevan. Gunakan `uncertain` untuk perkiraan yang wajar. Tulis susunan ruang, pencahayaan, atmosfer, dan lingkungan. Pilih warna utama dari bagian frame yang pencahayaannya merata, lalu isi nama, peran, HEX, dan bukti tiap warna.

Tulis nama gaya dalam bahasa Inggris, luas lantai sebagai rentang angka, serta uraian arsitektur, furnitur, lingkungan, dan framing dalam bahasa Indonesia. Catat fakta eksplisit dengan bukti dan statusnya. Camera Start menjelaskan awal sumber. Overview menjelaskan frame wide yang dipilih.

Tulis nama area dan caption momen multi-area dalam bahasa Inggris dengan Title Case. Gunakan `&` untuk fungsi dalam ruang yang sama, simpan setiap fungsi yang terlihat di `areas[].functions`, dan biarkan renderer memakai ` / ` antararea. Gunakan kosakata teknis Inggris untuk filter serta pertahankan narasi Indonesia. Lihat `audit/vocabulary.md`.

Deklarasikan viewed setelah melihat frame. Ikuti checklist di `audit/authoring.md`. Cocokkan `notation`, `observations`, dan frame sebelum review, terutama untuk fase yang terlewat, Orbit/Pan, dan arah yang salah. Jalankan `complete`, `check-input`, dan `draft`. Jika kandidat lulus validasi, jalankan `review` dan langsung `export --receipt` untuk membuat ZIP tanpa MP4 dalam sesi ini. Berikan tautan unduhan ZIP bersama hasil audit.
