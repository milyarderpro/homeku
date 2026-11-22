# Membaca referensi

Manusia mulai dari katalog lalu analysis.md terpilih. Laporan V2 mempunyai lima bagian: identitas desain, ukuran/proporsi, timeline, storyboard dan detail shot A/B/C. Nama gaya utama, rentang luas, detail rumah, posisi awal, kamera sederhana/teknis dan ritme tersedia tanpa tabel proses teknis.

V2 menyimpan audit.json sebagai sumber, analysis.md hasil render dan manifest.json teknis. Media memakai satu kolase per shot: normal tiga panel, multi area dinamis. Storyboard overview seluruh area satu baris; satu take tanpa cut yang melalui beberapa area tetap satu shot. Overview awal IN/akhir OUT adalah pilihan frame, bukan JPEG mandiri. Untuk gambar awal video, baca panel awal dan posisi/arah kamera; overview akhir Dolly-Out bukan posisi awal.

AI memakai data/search-index.json lalu tools/library.py read untuk identitas/shot/area terpilih; JSON lengkap di data/projections/. [Kontrak pembaca](../docs/contracts/ai-reader-v2.md) menjelaskan pointer, status dan bukti. Area yang terlihat dibedakan dari rute kamera yang benar-benar dilalui.

Referensi legacy 1.0/1.1 tetap memakai MD sebagai sumber dan media frame terpisah menurut kontraknya. edh001 aktif kini r0002/2.0, disetujui dan masuk melalui ZIP revisi eksplisit; paket r0001 disimpan sebagai riwayat. Tidak ada konversi atau penambahan luas/gaya otomatis. Laporan contoh V2 bukan sumber aktif.

Folder aktif hanya diisi importer dari ZIP final. Koreksi isi memakai revisi ZIP; jangan edit audit.json/MD aktif atau katalog/knowledge secara manual. Arsip tidak menjadi input build.
