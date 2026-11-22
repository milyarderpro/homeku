# Tujuh pilot nyata

Urutan pelaksanaan mengikuti instruksi terbaru: asisten mengaudit edh001 di chat ini terlebih dahulu; pengguna mengaudit enam video lainnya di ChatGPT/Gemini. Pembagian provider pada tabel adalah usulan pengujian, bukan catatan run yang sudah terjadi.

| Video | Pelaksana/lingkungan | Status nyata | Fokus |
| --- | --- | --- | --- |
| [edh001](../../video/edh001.mp4) | Codex, chat implementasi ini | V2 r0002 disetujui pengguna, diekspor dan di-ingest; aktif lokal sebagai 1 referensi/5 shot | Lima shot, arah kamera, tempo berfase, bathroom–laundry |
| [edh058](../../video/edh058.mp4) | Pengguna / ChatGPT | Belum dijalankan | Alur dasar lengkap dan wardrobe |
| [edh013](../../video/edh013.mp4) | Pengguna / Gemini | Belum dijalankan | Bentuk organik, platform bathroom, durasi stream/container |
| [edh033](../../video/edh033.mp4) | Pengguna / ChatGPT | Belum dijalankan | Open-plan, sleeping loft dan beberapa fungsi dalam satu shot |
| [edh049](../../video/edh049.mp4) | Pengguna / Gemini | Belum dijalankan | Perspektif bangunan/kitchen lengkung dan pembedaan pan/orbit |
| [edh056](../../video/edh056.mp4) | Pengguna / ChatGPT | Belum dijalankan | Lintasan exterior–interior, cut versus segmen fungsi |
| [dreamshome01](../../video/dreamshome01.mp4) | Pengguna / Gemini | Belum dijalankan | Pembanding arah, ritme dan perkembangan komposisi |

Tidak wajib menjalankan setiap sumber pada kedua model. Kedua lingkungan perlu terwakili sebelum kontrak dinyatakan stabil.

## Riwayat edh001 r0001 — format legacy

- [Laporan lengkap](edh001/analysis.md), [storyboard](edh001/media/storyboard.jpg), dan [manifest teknis](edh001/manifest.json).
- [ZIP final edh001](packages/edh001-r0001.zip), 5 shot dan 22 JPEG. Pengguna menyetujui keseluruhan snapshot dan meminta ekspor final; hash MD terkunci pada ekspor.
- Sumber kanonis sudah ada di video/edh001.mp4 dan hash cocok; MP4 tidak diduplikasi dalam ZIP final.
- [ZIP penyerahan](../../incoming/edh001-r0001.zip) sudah berada di incoming/ dan di-ingest. [Referensi aktif](../../references/edh001/analysis.md), JSON pembaca, katalog dan knowledge terbentuk otomatis.

Pengguna memeriksa isi di chat sesuai alur yang disepakati. Setelah koreksi/penilaian selesai, ekspor snapshot yang disetujui sesuai versi kontraknya dan serahkan satu ZIP final. Tidak ada review isi tambahan setelah ZIP final diunggah.

## Menjalankan enam berikutnya

Gunakan [panduan audit](../README.md) dan kit yang sama untuk masing-masing sumber. Mulai dari edh058 untuk menguji alur standar di chat sehari-hari, lalu video yang lebih kompleks. Catat nama lingkungan/model yang benar-benar dipakai serta masalah ekspor yang ditemukan; jangan mengisi metadata run/review sebelum dijalankan.

Kriteria tiap pilot: storyboard dan kartu semua shot terlihat di chat, MD lengkap tersedia, koreksi masuk ke snapshot final, ZIP terbuka ulang dan valid, media/overview benar, serta ingest di repo memperbarui katalog/knowledge tanpa edit manual. Validasi teknis tidak menggantikan penilaian visual di chat. Hanya paket final yang diunggah pengguna menjadi penyerahan audit aktif.


Perangkat terbaru memakai sumber audit.json 2.0, laporan/media 2.1.2 dan audit adaptif 10 FPS dengan pendalaman native. Riwayat edh001 r0001 di atas diaudit ulang, diterima pengguna dan diekspor final dalam format 1.1; lihat [kartu tinjauan](edh001-review.md) dan [catatan audit ulang](../../docs/edh001-re-audit.md). Koreksi gerakan dan riwayat penerimaan dicatat pada calibration.md; penerimaan r0001 mencakup seluruh snapshot audit, setelah persetujuan khusus shot 02 sebelumnya. Gunakan kit terbaru saat mengerjakan pilot berikutnya.

## edh001 V2 r0002 — disetujui dan aktif

[Laporan review lengkap](edh001-v2-review.md) memuat identitas/gaya Inggris, estimasi luas lantai, tiga kategori desain per shot, komposisi awal/akhir serta kamera sederhana dan teknis. [Kandidat lengkap](v2-candidates/edh001/analysis.md) disimpan terpisah dari paket r0001; sumber JSON, manifest dan enam JPEG berada dalam folder kandidat yang sama.

Pemeriksaan baru: 455 frame unik dari 552; baseline 10 FPS seluruh lima shot, native penuh shot 01/02/04 serta 9,8–11,567 s shot 03. Audio tidak diperiksa. Seluruh 128 fakta r0001 dipertahankan dengan bukti frame sumber, 30 klaim DNA lama dipetakan dan dua klaim gaya interior/pengaruh ditambahkan. Perubahan label gaya utama ke Contemporary Modern menyatakan nama teknis Inggris dari pembacaan kurva kontemporer sebelumnya; bukan perubahan bentuk sumber.

Pengguna menyetujui keseluruhan snapshot V2 di chat dengan “ya saya setuju”. [ZIP final r0002](packages/edh001-r0002.zip) diekspor memakai receipt terakhir tanpa render ulang, disalin ke [incoming/](../../incoming/edh001-r0002.zip) lalu di-ingest. [Laporan aktif](../../references/edh001/analysis.md) dan [JSON pembaca](../../data/projections/edh001.json) kini revisi 2; r0001 tetap tersimpan. Enam pilot berikutnya menggunakan kit V2 terbaru, satu chat per video dan kedua provider terwakili sesuai run nyata.

- Snapshot lengkap: `71e949c51a3ca82f0a8d22c26ad98c82c6283d8c40413b8b0a24ef99e178ca45`; JSON/MD/manifest/enam JPEG dalam ZIP dan referensi aktif identik dengan kandidat yang ditinjau.
- ZIP: 4,600,760 byte, SHA-256 `c290e7f81642498330cdb4b0b4b2ecaf2238c5074b83761bf31b08040e74c26f`. Source MP4 kanonis dipakai tanpa duplikasi.
- Validasi roundtrip dan pointer AI lulus. Ingest ulang kedua ZIP menghasilkan unchanged tanpa perubahan berkas. Katalog/knowledge dibangun generator; tidak ada review isi kedua.
