# Tujuh pilot nyata

Urutan pelaksanaan mengikuti instruksi terbaru: asisten mengaudit edh001 di chat ini terlebih dahulu; pengguna mengaudit enam video lainnya di ChatGPT/Gemini. Pembagian provider pada tabel adalah usulan pengujian, bukan catatan run yang sudah terjadi.

| Video | Pelaksana/lingkungan | Status nyata | Fokus |
| --- | --- | --- | --- |
| [edh001](../../video/edh001.mp4) | Codex, chat implementasi ini | Audit 1.1 disetujui pengguna; ZIP final r0001 di-ingest; aktif lokal sebagai 1 referensi/5 shot | Lima shot, arah kamera, tempo berfase, bathroom–laundry |
| [edh058](../../video/edh058.mp4) | Pengguna / ChatGPT | Belum dijalankan | Alur dasar lengkap dan wardrobe |
| [edh013](../../video/edh013.mp4) | Pengguna / Gemini | Belum dijalankan | Bentuk organik, platform bathroom, durasi stream/container |
| [edh033](../../video/edh033.mp4) | Pengguna / ChatGPT | Belum dijalankan | Open-plan, sleeping loft dan beberapa fungsi dalam satu shot |
| [edh049](../../video/edh049.mp4) | Pengguna / Gemini | Belum dijalankan | Perspektif bangunan/kitchen lengkung dan pembedaan pan/orbit |
| [edh056](../../video/edh056.mp4) | Pengguna / ChatGPT | Belum dijalankan | Lintasan exterior–interior, cut versus segmen fungsi |
| [dreamshome01](../../video/dreamshome01.mp4) | Pengguna / Gemini | Belum dijalankan | Pembanding arah, ritme dan perkembangan komposisi |

Tidak wajib menjalankan setiap sumber pada kedua model. Kedua lingkungan perlu terwakili sebelum kontrak dinyatakan stabil.

## edh001 yang sudah disetujui

- [Laporan lengkap](edh001/analysis.md), [storyboard](edh001/media/storyboard.jpg), dan [manifest teknis](edh001/manifest.json).
- [ZIP final edh001](packages/edh001-r0001.zip), 5 shot dan 22 JPEG. Pengguna menyetujui keseluruhan snapshot dan meminta ekspor final; hash MD terkunci pada ekspor.
- Sumber kanonis sudah ada di video/edh001.mp4 dan hash cocok; MP4 tidak diduplikasi dalam ZIP final.
- [ZIP penyerahan](../../incoming/edh001-r0001.zip) sudah berada di incoming/ dan di-ingest. [Referensi aktif](../../references/edh001/analysis.md), JSON pembaca, katalog dan knowledge terbentuk otomatis.

Pengguna memeriksa isi di chat sesuai alur yang disepakati. Setelah koreksi/penilaian selesai, bangun ekspor dari MD terbaru dan serahkan satu ZIP final. Tidak ada review isi tambahan setelah ZIP final diunggah.

## Menjalankan enam berikutnya

Gunakan [panduan audit](../README.md) dan kit yang sama untuk masing-masing sumber. Mulai dari edh058 untuk menguji alur standar di chat sehari-hari, lalu video yang lebih kompleks. Catat nama lingkungan/model yang benar-benar dipakai serta masalah ekspor yang ditemukan; jangan mengisi metadata run/review sebelum dijalankan.

Kriteria tiap pilot: storyboard dan kartu semua shot terlihat di chat, MD lengkap tersedia, koreksi masuk ke snapshot final, ZIP terbuka ulang dan valid, media/overview benar, serta ingest di repo memperbarui katalog/knowledge tanpa edit manual. Validasi teknis tidak menggantikan penilaian visual di chat. Hanya paket final yang diunggah pengguna menjadi penyerahan audit aktif.


Perangkat terbaru memakai format 1.1 dan audit adaptif 10 FPS dengan pendalaman native. edh001 di atas sudah diaudit ulang, diterima pengguna dan diekspor final dalam format 1.1; lihat [kartu tinjauan](edh001-review.md) dan [catatan audit ulang](../../docs/edh001-re-audit.md). Koreksi gerakan dan riwayat penerimaan dicatat pada calibration.md; persetujuan terbaru mencakup seluruh snapshot audit, setelah persetujuan khusus shot 02 sebelumnya. Gunakan kit terbaru saat mengerjakan pilot berikutnya.
