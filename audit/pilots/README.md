# Tujuh pilot nyata

Urutan pelaksanaan mengikuti instruksi terbaru: asisten mengaudit edh001 di chat ini terlebih dahulu; pengguna mengaudit enam video lainnya di ChatGPT/Gemini. Pembagian provider pada tabel adalah usulan pengujian, bukan catatan run yang sudah terjadi.

| Video | Pelaksana/lingkungan | Status nyata | Fokus |
| --- | --- | --- | --- |
| [edh001](../../video/edh001.mp4) | Codex, chat implementasi ini | r0003/2.1 disetujui, diekspor dan aktif melalui ingest (1 referensi/5 shot); r0001/r0002 tetap riwayat | Lima shot, arah kamera, tempo berfase, bathroom–laundry |
| [edh058](../../video/edh058.mp4) | Pengguna / ChatGPT dan Gemini | Dua hasil tersedia dan sudah dibandingkan; belum disetujui/di-ingest. [Catatan](edh058-comparison.md) | Alur dasar lengkap dan wardrobe |
| [edh013](../../video/edh013.mp4) | Pengguna / Gemini | Belum ada run terverifikasi dalam catatan ini | Bentuk organik, platform bathroom, durasi stream/container |
| [edh033](../../video/edh033.mp4) | Pengguna / ChatGPT | Belum ada run terverifikasi dalam catatan ini | Open-plan, sleeping loft dan beberapa fungsi dalam satu shot |
| [edh049](../../video/edh049.mp4) | Pengguna / Gemini | Belum ada run terverifikasi dalam catatan ini | Perspektif bangunan/kitchen lengkung dan pembedaan pan/orbit |
| [edh056](../../video/edh056.mp4) | Pengguna / ChatGPT | Belum ada run terverifikasi dalam catatan ini | Lintasan exterior–interior, cut versus segmen fungsi |
| [dreamshome01](../../video/dreamshome01.mp4) | Pengguna / Gemini | Belum ada run terverifikasi dalam catatan ini | Pembanding arah, ritme dan perkembangan komposisi |

Tidak wajib menjalankan setiap sumber pada kedua model. Kedua lingkungan perlu terwakili sebelum kontrak dinyatakan stabil.

## Riwayat edh001 r0001 — format legacy

- [Laporan lengkap](edh001/analysis.md), [storyboard](edh001/media/storyboard.jpg), dan [manifest teknis](edh001/manifest.json).
- [ZIP final edh001](packages/edh001-r0001.zip), 5 shot dan 22 JPEG. Pengguna menyetujui keseluruhan snapshot dan meminta ekspor final; hash MD terkunci pada ekspor.
- Sumber kanonis sudah ada di video/edh001.mp4 dan hash cocok; MP4 tidak diduplikasi dalam ZIP final.
- [ZIP penyerahan](../../incoming/edh001-r0001.zip) sudah berada di incoming/ dan di-ingest. [Referensi aktif](../../references/edh001/analysis.md), JSON pembaca, katalog dan knowledge terbentuk otomatis.

Pengguna memeriksa isi di chat sesuai alur yang disepakati. Setelah koreksi/penilaian selesai, ekspor snapshot yang disetujui sesuai versi kontraknya dan serahkan satu ZIP final. Tidak ada review isi tambahan setelah ZIP final diunggah.

## Menjalankan enam berikutnya

Gunakan [panduan audit](../README.md) dan kit yang sama untuk masing-masing sumber. Mulai dari edh058 untuk menguji alur standar di chat sehari-hari, lalu video yang lebih kompleks. Catat nama lingkungan/model yang benar-benar dipakai serta masalah ekspor yang ditemukan; jangan mengisi metadata run/review sebelum dijalankan.

Kriteria tiap pilot: Overview, Storyboard dan kolase semua shot terlihat di chat, MD lengkap tersedia, koreksi masuk ke snapshot final, ZIP terbuka ulang dan valid, media/overview benar, serta ingest di repo memperbarui katalog/knowledge tanpa edit manual. Validasi teknis tidak menggantikan penilaian visual di chat. Hanya paket final yang diunggah pengguna menjadi penyerahan audit aktif.


Perangkat terbaru memakai sumber audit.json2.3, laporan2.2.2/media2.2.0 dan baseline6FPS dengan pendalaman10FPS/native. Riwayat2.2 tetap10FPS. Riwayat edh001 r0001 di atas diaudit ulang, diterima pengguna dan diekspor final dalam format 1.1; lihat [kartu tinjauan](edh001-review.md) dan [catatan audit ulang](../../docs/edh001-re-audit.md). Koreksi gerakan dan riwayat penerimaan dicatat pada calibration.md; penerimaan r0001 mencakup seluruh snapshot audit, setelah persetujuan khusus shot 02 sebelumnya. Gunakan kit terbaru saat mengerjakan pilot berikutnya.

## Riwayat edh001 V2 r0002 — disetujui dan di-ingest saat itu

[Laporan review lengkap](edh001-v2-review.md) memuat identitas/gaya Inggris, estimasi luas lantai, tiga kategori desain per shot, komposisi awal/akhir serta kamera sederhana dan teknis. [Kandidat lengkap](v2-candidates/edh001/analysis.md) disimpan terpisah dari paket r0001; sumber JSON, manifest dan enam JPEG berada dalam folder kandidat yang sama.

Pemeriksaan baru: 455 frame unik dari 552; baseline 10 FPS seluruh lima shot, native penuh shot 01/02/04 serta 9,8–11,567 s shot 03. Audio tidak diperiksa. Seluruh 128 fakta r0001 dipertahankan dengan bukti frame sumber, 30 klaim DNA lama dipetakan dan dua klaim gaya interior/pengaruh ditambahkan. Perubahan label gaya utama ke Contemporary Modern menyatakan nama teknis Inggris dari pembacaan kurva kontemporer sebelumnya; bukan perubahan bentuk sumber.

Pengguna menyetujui keseluruhan snapshot V2 di chat dengan “ya saya setuju”. [ZIP final r0002](packages/edh001-r0002.zip) diekspor memakai receipt terakhir tanpa render ulang, disalin ke [incoming/](../../incoming/edh001-r0002.zip) lalu di-ingest. R0002 menjadi referensi aktif saat penerimaan tersebut; [kandidat r0002](v2-candidates/edh001/analysis.md) dan ZIP-nya tetap tersimpan sebagai riwayat setelah r0003 aktif. Enam pilot berikutnya menggunakan kit V2 terbaru, satu chat per video dan kedua provider terwakili sesuai run nyata.

- Snapshot lengkap: `71e949c51a3ca82f0a8d22c26ad98c82c6283d8c40413b8b0a24ef99e178ca45`; JSON/MD/manifest/enam JPEG dalam ZIP dan referensi aktif identik dengan kandidat yang ditinjau.
- ZIP: 4,600,760 byte, SHA-256 `c290e7f81642498330cdb4b0b4b2ecaf2238c5074b83761bf31b08040e74c26f`. Source MP4 kanonis dipakai tanpa duplikasi.
- Validasi roundtrip dan pointer AI lulus. Ingest ulang kedua ZIP menghasilkan unchanged tanpa perubahan berkas. Katalog/knowledge dibangun generator; tidak ada review isi kedua.

## Overview / Storyboard r0003 — disetujui dan aktif

Kit terbaru menggunakan format2.1/report 2.2.0 dan empat file input, dengan33 runtime. edh001 r0003 tersedia sebagai [laporan aktif](../../references/edh001/analysis.md); kandidat/receipt lokal tetap tersimpan di `.homeku/overview-storyboard-stage2/`. Tambahan: lima paragraf Overview, enam klasifikasi arah fase, serta format kamera satu paragraf; fakta/gerak/tempo/selection sumber diterima dipertahankan. Lima frame Overview diperiksa kembali; log audit r0002 dipertahankan. Tidak ada audit penuh ulang.

Pengguna menyetujui seluruh snapshot r0003 dengan “ya saya setuju”. [ZIP final r0003](packages/edh001-r0003.zip) dan [penyerahan incoming](../../incoming/edh001-r0003.zip) berisi byte kandidat yang sama; validasi roundtrip, ingest eksplisit, replay unchanged dan check berhasil. [Status dan bukti](../../docs/overview-storyboard-verification.md). ZIP yang berada di audit/result/ tidak dipakai sebagai bukti run selesai dan tidak di-ingest pada pekerjaan ini. Enam pilot berikutnya tetap dikerjakan pengguna, satu chat per video, dengan kit terbaru dan status/provider berdasarkan run nyata.


## Status sesudah hasil edh058 tersedia

Edh058 sudah memiliki dua hasil pengguna dari ChatGPT/Gemini, belum diterima sebagai referensi aktif; lihat [pembandingan](edh058-comparison.md). Lima pilot lain belum memiliki hasil tercatat. Dua hasil terbaru2.2 tersedia dan dibandingkan. Kit2.3 siap diuji, tetapi implementasi tooling dan fixture bukan run ulang atau persetujuan edh058. Catatan historis belum dijalankan pada bagian terdahulu berlaku pada waktu pencatatan itu.

## Pilot metode2.3 — disiapkan, belum dijalankan

Pembagian tetap: pengguna menjalankan enam pilot tersisa di chat provider; asisten menyiapkan workflow/tooling dan membandingkan hasil yang dikembalikan. Implementasi tooling tidak menjalankan akun ChatGPT/Gemini pengguna.

1. Mulai chat baru masing-masing ChatGPT/Gemini untuk edh058. Lampirkan video/edh058.mp4 dan audit/homeku-audit-kit.zip terbaru, kirim audit/prompts/01-audit.md.
2. Nilai hasil kamera lengkap/sederhana, ~×/~°, tempo, desain dan enam bagian MD beserta seluruh gambar. Koreksi lewat prompt02; jangan menyalin gerak/angka dari pembanding sebagai hasil pengamatan baru.
3. Setelah keseluruhan sesuai, gunakan prompt03. Unduh ZIP tanpa MP4. Simpan run terpisah, misalnya audit/result/gemini/v2.3/run-01/edh058-r0001.zip dan audit/result/gpt/v2.3/run-01/edh058-r0001.zip, agar hasil2.2 tidak tertimpa.
4. Catat provider/model yang diketahui, versi sumber/report, hash MP4/ZIP, frame unik benar-benar dilihat, pertanyaan pendalaman, perbedaan keputusan dan status review/export. Bedakan kesiapan tooling, run nyata, persetujuan, ekspor dan ingest.
5. Setelah hasil memadai, lanjutkan edh013,edh033,edh049,edh056,dreamshome01 sesuai pembagian. Tidak wajib menggandakan seluruh video di dua provider.

Kedua run edh058 harus memakai sumber kanonis hash823be3ce9ee96fc07a6ab263010a09a3d60e72cfcf334ef2fbe5a38e7a550731. Pembanding Gemini2.2 dan koreksi pengguna dipakai menilai keputusan, bukan template jawaban. Semua moderate boleh. Ukur kecukupan bukti/keterbacaan/beban pemeriksaan; lebih sedikit frame bukan otomatis lebih akurat. Persetujuan/ingest menunggu hasil nyata, tidak diisi dari tes sintetis.

## Pilot efisiensi2.4 — siap sesudah tooling, belum dijalankan

Dua hasil2.3 edh058 kini tersedia, dengan laporan proses di result/<provider>/laporan.md; lihat pembandingan terbaru. Bagian yang menyatakan run2.3 belum berjalan di atas adalah catatan pada akhir implementasi sebelumnya.

Pengguna menjalankan edh058 di chat baru ChatGPT/Gemini memakai MP4 kanonis dan kit2.4 terbaru. Sumber2.4/report2.2.3/media2.2.0, estimasi visual sah tanpa piksel wajib, helper authoring resmi dan baseline6FPS terarah. Gunakan prompt01; koreksi lewat02; ekspor setelah persetujuan keseluruhan lewat03.

Simpan run baru di audit/result/<provider>/v2.4/run-NN/<id>-rNNNN.zip agar hasil2.3 tidak ditimpa. Catat versi/model/hash kit/sumber/paket, waktu kandidat siap, retry dan log alat; pisahkan jeda persetujuan/ekspor. Periksa seluruh desain/fakta/estimasi/arah/tempo/Camera Start/Overview/MD/media. Semua moderate boleh; target efisiensi tidak mengurangi detail. Setelah memadai lanjutkan lima pilot lain.

Benchmark lokal hanya pengukuran helper dan kandidat fixture, bukan menit yang dijanjikan pada AI provider. Tooling siap, run nyata, persetujuan, ekspor dan ingest dicatat terpisah; pembagian enam pilot pengguna tetap.

## Lanjutan kamera2.5 — 24 November 2026

Dua hasil edh058 sumber2.4 kini tersedia/diperiksa, MD serta8JPEG sesuai renderer; belum disetujui/di-ingest. Pemeriksaan visual tambahan hanya18frame, bukan audit seluruh baseline. Laporan waktu provider bukan benchmark terkontrol. Implementasi kamera2.5 melanjutkan plan audit-camera-implementation-plan.md; run2.5 pengguna belum dijalankan. Status historis di atas berlaku pada saat dicatat.

Tooling2.5 kini selesai:214tes lulus tanpa skip, kit4file/90resource, caption baru dan parser angka opsional. Lihat docs/audit-camera-verification.md. Run provider2.5 tetap belum dijalankan.
