# Design

## Context

Fase 5 menghasilkan ZIP dengan nama `<id>-rNNNN.zip` di `HOMEKU/Audit/<nama-video>/`. Koreksi yang belum di-ingest dapat memperbarui byte ZIP pada ID Drive yang sama. Pustaka lokal menyimpan revisi aktif dan hash di `data/registry.json`, serta keberhasilan ingest sebelumnya di `data/ingest.json`. `tools/homeku/engine.py` sudah memvalidasi seluruh paket, mencocokkan MP4, memeriksa `supersedes`, dan menerbitkan hasil batch lewat transaksi repo.

## Goals / Non-Goals

**Tujuan.** Satu perintah terminal menangani pemindaian, persetujuan, pengunduhan, dan ingest. Pengguna dapat menjalankan pemindaian untuk melihat daftar terlebih dahulu saat diperlukan.

**Batas desain.** Proses berjalan selama perintah dipanggil dan berakhir di pustaka lokal. Format 3.1, publikasi Git yang ada, dan pengiriman hasil audit oleh ChatGPT tetap menjadi kontrak integrasi.

## Decisions

### Perintah lokal dengan akses Drive baca

Gunakan `python tools/ingest_drive.py` sebagai usulan titik masuk. Opsi `--list` menampilkan inventaris dan status paket tanpa persetujuan atau perubahan pustaka. Alur interaktif menampilkan nama, ID audit, revisi, lokasi, dan status. Pengguna dapat memilih semua kandidat yang memenuhi syarat atau daftar nomor, lalu memberi satu konfirmasi. Pilihan kosong dan pembatalan mengakhiri proses. Persetujuan berlaku selama satu pemanggilan.

Gunakan Drive API dengan OAuth aplikasi desktop dan cakupan `drive.readonly`. Siapkan ID root HOMEKU dan kredensial secara lokal satu kali. Simpan token dengan izin lokal terbatas di luar repo, serta pisahkan dependensi Drive dari runtime audit dan kit. Root yang dikonfigurasi membatasi kandidat yang dibaca oleh perintah. Cakupan OAuth sendiri memberi akses baca sesuai izin akun. Mount folder Drive dipertimbangkan sebagai sumber file lokal, tetapi tidak menyediakan ID Drive dan metadata yang dibutuhkan untuk mengikat persetujuan. [Otorisasi aplikasi desktop](https://developers.google.com/identity/protocols/oauth2/native-app) · [Cakupan Drive](https://developers.google.com/workspace/drive/api/guides/api-specific-auth)

### Inventaris berdasarkan parent Drive dan hash

Resolusi root memakai ID, lalu anak langsung `Audit` dan `Video` memakai nama serta tipe folder. Pindai ZIP kanonis dari satu tingkat folder video di bawah `Audit`. Arsip longgar yang masih ada langsung di `Audit` berada di luar inventaris batch ini. Ikuti semua halaman, cek status pencarian yang belum lengkap, dan pisahkan benturan nama atau identitas. [Kontrak daftar file Drive](https://developers.google.com/workspace/drive/api/reference/rest/v3/files/list)

Gunakan ID, nama, parent, ukuran, serta SHA-256 ketika tersedia. Untuk ZIP tanpa SHA-256 dari Drive, gunakan unduhan sementara dengan batas ZIP yang sudah berlaku dan hitung hash sebelum menampilkan paket sebagai kandidat. Bandingkan hash paket dengan registri dan riwayat sukses. Jika nomor revisi sama dengan yang aktif tetapi hash ZIP berbeda, bandingkan hash isi snapshot yang diekstrak memakai utilitas HOMEKU agar paket yang dikemas ulang dengan isi identik tetap dikenali. Pakai nomor revisi dan daftar paket untuk menunjukkan pendahulu yang diperlukan. Mesin ingest tetap menentukan validitas `supersedes`. [Metadata dan checksum Drive](https://developers.google.com/workspace/drive/api/reference/rest/v3/files)

### Pilihan terikat ke snapshot dan staging terisolasi

Simpan daftar yang disetujui selama proses berjalan sebagai ID file, parent, nama kanonis, dan SHA-256. Baca ulang metadata dan verifikasi byte unduhan atas pilihan itu. Saat checksum metadata tidak tersedia, pastikan hasil unduhan untuk ingest cocok dengan hash yang ditampilkan sebelum konfirmasi. Perubahan identitas atau isi menandai paket untuk persetujuan baru. Simpan hasil transfer secara sementara di bawah `.homeku/` dan siapkan daftar path ZIP eksplisit. Dengan staging ini, ingest batch hanya menerima paket yang disetujui dan direktori `incoming/` tetap dapat dipakai oleh alur manual.

### Sumber kanonis dan transaksi ingest

Ambil rujukan sumber dari manifest ZIP yang sudah diperiksa secara aman. Pakai `video/<id>.mp4` jika hash cocok. Bila belum ada, cocokkan nama video berdasarkan nama folder audit, lalu verifikasi SHA-256 sumber dari `Video` sebelum pemasangan. Untuk kandidat sumber bernama sama, gunakan hash sebagai pembeda hanya jika tepat satu file cocok. Sumber lokal yang berbeda atau hasil pencarian yang ambigu masuk laporan. Pemasangan MP4 baru menggunakan staging di filesystem yang sama, operasi atomik, dan pengecekan ulang di bawah lock repo agar sumber yang sudah ada tidak tertimpa.

Kirim daftar ZIP yang siap secara eksplisit ke `ingest(root, packages)` yang sudah ada. Jalankan unduhan dan konfirmasi di luar lock repo. Lepas lock pemasangan MP4 sebelum memanggil ingest karena mesin ingest mengambil lock sendiri dan membaca ulang registry. Mesin mengurutkan nama kanonis, memverifikasi sumber, menerapkan urutan revisi, dan menghasilkan laporan per paket. Gabungkan hasil itu dengan alasan paket yang ditahan sebelum ingest. Publikasi dari pemanggilan bersamaan bergantung pada lock repo dan riwayat hash yang sama.

## Risks / Trade-offs

- **ZIP ditimpa saat daftar sudah terbuka** → Verifikasi ID, parent, nama, dan SHA-256 pada saat transfer. Permintaan berikutnya menampilkan snapshot baru untuk persetujuan.
- **Checksum metadata kosong** → Sebagian ZIP perlu dibaca saat pemindaian. Gunakan staging sementara yang dibatasi dan jangan membaca media terpisah.
- **Drive terputus atau sumber hilang** → Tandai pekerjaan yang tertunda dan lanjutkan paket lain yang independen setelah inventaris dikonfirmasi lengkap. Unduhan parsial tetap berada di staging. Pemanggilan ulang memakai registry dan riwayat sukses untuk menentukan pekerjaan tersisa.
- **Urutan revisi atau registri berubah** → Ingatkan dependensi saat memilih. Mesin ingest memeriksa ulang urutan dan `supersedes` berdasarkan isi repo terbaru pada saat publikasi.

## Migration Plan

1. Pasang dependensi akses Drive secara lokal dan konfigurasikan kredensial serta ID root HOMEKU.
2. Jalankan mode daftar terlebih dahulu. Cocokkan jumlah paket yang sudah masuk, kandidat, dan konflik dengan kondisi Drive.
3. Jalankan satu batch kecil dan periksa status ingest beserta hasil `library.py check`. Perintah lokal bersifat pilihan dan dapat dihentikan dengan kembali ke alur ingest manual. Referensi yang sudah diterima mengikuti aturan revisi pustaka yang sama.
