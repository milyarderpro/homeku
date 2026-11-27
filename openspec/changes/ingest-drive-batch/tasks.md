# Tasks

## 1. Akses Drive dan inventaris

- [x] 1.1 Tambahkan akses Drive baca untuk perintah lokal, dengan konfigurasi ID root dan OAuth desktop di luar repo serta dependensi terpisah dari kit. Dokumentasikan penyiapan lokal di panduan pengguna. Verifikasi `--help` bisa dibuka tanpa konfigurasi Drive dan konfigurasi hilang memberi pesan yang dapat ditindaklanjuti.
- [x] 1.2 Resolusi anak folder `Audit` dan `Video` berdasarkan parent dan tipe. Pindai seluruh halaman dari folder video yang didukung. Uji dua halaman, folder ganda, item di luar cakupan, shortcut, item di sampah, dan respons daftar yang belum lengkap.

## 2. Status paket dan persetujuan

- [x] 2.1 Cocokkan ID, revisi, dan hash dengan registri serta riwayat sukses. Gunakan ekstraksi terbatas untuk checksum yang tidak tersedia dan pembandingan isi revisi aktif yang dikemas ulang. Uji inventaris 20 paket dengan 12 sudah masuk, revisi berikutnya, pendahulu yang hilang, serta paket identik dan konflik pada nomor yang sama.
- [x] 2.2 Tampilkan status, dependensi revisi, dan pilihan nomor atau semua kandidat. Ikat satu konfirmasi dengan ID, lokasi, nama, dan SHA-256 paket. Perbarui panduan untuk `--list`, persetujuan, dan pembatalan. Uji bahwa daftar, pembatalan, dan pilihan kosong tidak mengubah pustaka serta pemilihan sebagian hanya memproses pilihan itu.

## 3. Persiapan sumber dan ingest lokal

- [x] 3.1 Unduh ulang dan verifikasi hanya ZIP yang disetujui untuk ingest. Gunakan staging di `.homeku/` dan laporkan paket yang berubah atau gagal transfer. Uji penggantian isi pada ID yang sama, perpindahan parent, unduhan parsial, dan checksum yang berbeda.
- [x] 3.2 Pakai MP4 kanonis yang hash-nya cocok. Jika belum ada, temukan sumber di `Video`, verifikasi hash dari manifest, lalu pasang secara atomik dengan pengecekan di bawah lock repo. Uji salinan lokal cocok, pengunduhan yang valid, sumber hilang, ambiguitas, dan penolakan menimpa salinan lokal berbeda.
- [x] 3.3 Teruskan path ZIP terverifikasi secara eksplisit ke mesin ingest. Tampilkan ringkasan dan alasan per paket, lalu akhiri pemanggilan. Dokumentasikan cara membaca laporan dan menjalankan ulang. Uji batch campuran, revisi berurutan, pendahulu gagal, serta pengulangan yang melewati paket sukses.

## 4. Verifikasi integrasi

- [x] 4.1 Jalankan satu alur dari daftar hingga ingest dengan Drive tiruan dan pustaka fixture terisolasi. Periksa bahwa hanya ZIP yang dipilih menjadi aktif, MP4 terisi dengan hash yang benar, dan pemanggilan berikutnya menampilkan hasil yang sudah masuk.
- [x] 4.2 Jalankan `python -m unittest discover -s tests -t . -v`, `python tools/library.py check`, dan `python tools/build_audit_kit.py --check`. Pastikan perintah manual dan kit tetap dapat dijalankan.
