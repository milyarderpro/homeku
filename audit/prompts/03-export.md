# Prompt ekspor final HOMEKU 2.1

Keseluruhan kandidat audit terbaru yang saya tinjau sudah sesuai. Ekspor satu ZIP final HOMEKU dari snapshot tersebut.

Gunakan export-v2 atas folder kandidat dan receipt review terakhir, bukan menjalankan draft ulang. JSON, MD, manifest, JPEG dan created_at harus tetap sama dengan kandidat yang saya periksa. Jangan mengubah isi atau memperbarui media/metadata saat ekspor. Jika kandidat berubah atau receipt tidak cocok, tampilkan ulang perubahan sebelum meminta persetujuan versi baru.

Pastikan sumber/paket2.1, report/media2.2.0, dan inventaris N+2 JPEG lengkap: Overview satu baris, Storyboard seluruh kolase vertikal, kolase setiap take. Tidak mengubah versi paket lama diam-diam. Pastikan log mencatat pemeriksaan nyata dan sumber terikat hash yang sama. source.mp4 hanya disertakan jika sumber kanonis belum terverifikasi tersedia; jika diperlukan tetapi belum ada dalam kandidat yang disetujui, buat kandidat lengkap baru dan tampilkan kembali sebelum ekspor. Jangan menambahkan script, receipt, audit-info, frame sementara, motion/ atau klip shot ke ZIP referensi.

Jalankan validasi folder dan ZIP yang dibuka ulang serta kesamaan digest seluruh payload. Jika gagal, jelaskan error nyata; jangan menulis hash/bukti rekaan. Berikan satu tautan download <id>-rNNNN.zip, jumlah shot/gambar dan ringkasan pemeriksaan teknis singkat. Saya menaruh ZIP di incoming/ lokal lalu menjalankan ingest; tidak ada review isi kedua di repo.
