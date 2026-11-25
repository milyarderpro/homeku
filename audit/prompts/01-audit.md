# Mulai audit HOMEKU 3.0

Audit video MP4 terlampir untuk pustaka HOMEKU. Ekstrak kit, jalankan `python homeku_runtime.py --output .`, lalu baca `audit/visual-audit.md` dan `audit/authoring.md`.

Konfirmasi cut nyata dan jalankan prepare. Periksa baseline 6 FPS serta frame batas native. Sumber ≤6 FPS dan shot <1 detik memakai seluruh native. Gunakan 10 FPS atau native tambahan untuk menjawab pertanyaan visual tertentu. Satu take kontinu boleh memperlihatkan beberapa area.

Periksa depth, translation, dan rotation sebelum menentukan gerak. Evaluasi besaran setiap komponen per fase. Tulis estimasi ~× atau ~° yang dapat dibuat secara wajar dari frame. Angka tunggal dan rentang sama-sama sah. Hilangkan angka hanya pada komponen yang besarannya sulit diperkirakan secara wajar. Pisahkan tempo dari fase dan intensitas. Ikuti kronologi video sumber.

Tulis nama gaya dalam bahasa Inggris, luas lantai sebagai rentang angka, serta uraian arsitektur, furnitur, lingkungan, dan framing dalam bahasa Indonesia. Catat fakta eksplisit dengan bukti dan statusnya. Camera Start menjelaskan awal sumber. Overview menjelaskan frame wide yang dipilih.

Deklarasikan viewed setelah melihat frame. Sebelum menampilkan laporan, ikuti checklist di `audit/authoring.md` dan tinjau kembali komponen tanpa angka dari frame yang sudah dilihat. Jalankan `complete`, `check-input`, dan `draft`. Jika kandidat lulus validasi, jalankan `review` dan langsung `export --receipt` untuk membuat ZIP tanpa MP4 dalam sesi ini.
