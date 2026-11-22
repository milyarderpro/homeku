# Verifikasi improvement — langkah 1, 2 dan 3

Tanggal: 22 November 2026. Lingkup yang selesai adalah kontrak/format, perangkat audit serta tooling. Audit ulang edh001 dan penyelesaian tujuh pilot tetap pekerjaan berikutnya; kontrak belum dibekukan.

## Perubahan yang tersedia

| Bagian | Hasil |
| --- | --- |
| Laporan manusia | Template MD 1.1: profil DNA/palet, storyboard, ikhtisar dan uraian shot, komposisi serta kamera; tabel teknis dapat dilipat |
| Data untuk AI | Kontrak reader 1.0, proyeksi lengkap per referensi, indeks dengan profil/alias/status dan pointer; metadata cache terpisah pada build.json |
| Pengetahuan | Prinsip umum terkurasi di sources/ diterbitkan verbatim sebagai MD/JSON; perbandingan fakta juga tersedia dalam halaman JSON berbukti |
| Audit kamera | Aturan arah/fase, tiga tes pan/orbit/truck, estimasi berbukti, pemisahan ritme/rasio/percepatan dan penyaringan tilt tipis pada protokol/rubrik/prompt |
| Sampling | Default 10 FPS dan --native tanpa interpolasi; PTS asli, frame pertama/terakhir, ekstraksi terbatasi dan contact sheet sementara |
| Log aktual | frame_reviews menyimpan indeks pilihan/pemeriksaan, FPS, rentang dan alasan; cakupan gabungan setiap shot harus lengkap; ekstraksi tidak otomatis menjadi klaim pemeriksaan |
| Review dan ekspor | Helper review menghasilkan kartu dari snapshot MD yang sama; ekspor mengunci byte MD lewat digest dan memvalidasi ZIP setelah dibuka ulang |
| Otomasi | Parser membaca 1.1 dan legacy 1.0 secara eksplisit; generator menghasilkan turunan; CI/ingest mencakup perubahan sources/ |

Pemetaan kemampuan lama tersedia pada [capability-map.md](capability-map.md). Kontrak [laporan](contracts/analysis-v1.md), [paket](contracts/package-v1.md) dan [pembaca AI](contracts/ai-reader-v1.md) menjelaskan bentuk data. Tidak ada analysis.json yang diedit terpisah, sintesis AI dalam generator, atau penggabungan fakta arsip.

## Pemeriksaan yang benar-benar dijalankan

- `python -m unittest discover -s tests -t . -v`: **51 pengujian lulus** dalam 79.136 detik. Termasuk 17 regresi improvement, pengujian helper dan fondasi; kapasitas 300 referensi/600 shot sintetis, revisi/regenerasi, konkurensi/pemulihan dan benturan push pada remote Git lokal sementara.
- `python tools/library.py build`: turunan repo diperbarui dari sumber/tooling.
- `python tools/library.py check`: lulus; rebuild penuh cocok dengan turunan.
- `python tools/build_audit_kit.py` dan `--check`: kit dibangun ulang serta cocok secara deterministik, sembilan file tanpa video/audio.
- `git diff --check`: lulus.

Regresi improvement mencakup pelestarian narasi/profil/status/bukti MD–JSON, pointer yang dapat dibuka, alias eksplisit dan konflik alias, legacy tanpa pengayaan rekaan, prinsip terpisah dari fakta, revisi DNA/knowledge tanpa turunan usang, cache rusak, log pemeriksaan tidak lengkap, cakupan tanpa gap, pendalaman tumpang tindih, native 60 FPS, FPS rendah/timestamp tidak seragam, dan kartu/ZIP dari snapshot yang sama. Kit dibuka di workspace terisolasi: ekspor portabel diuji dengan paket legacy, dan review portabel diuji dengan paket format 1.1. Ekspor paket 1.1 juga diuji melalui fungsi assemble beserta validasi dan round-trip ZIP.

Satu kegagalan awal ditemukan pada fixture simulasi publikasi Git yang belum menyalin folder sources/ baru. Fixture diperbaiki, kemudian seluruh suite diulang dan lulus. Pengujian ini tidak menjalankan publikasi hosted GitHub atau audit akun ChatGPT/Gemini pengguna.

## Status referensi nyata pada akhir langkah 1–3

Satu draf audit nyata edh001 tetap tersedia di audit/pilots/edh001/, beserta kandidat ZIP lama. Draf tersebut belum disetujui seluruhnya, masih format 1.0, dan tidak diubah pada pekerjaan ini. Koreksi kamera shot 02 yang diterima hanya dicatat sebagai kalibrasi; penerapannya masuk langkah audit ulang.

Registry produksi belum berisi referensi final aktif. Status teknis ini tidak berarti draf edh001 tidak ada. Tidak ada fixture yang dimasukkan sebagai referensi aktif dan tidak ada klaim audit ulang yang belum dilakukan.

Langkah berikutnya: audit ulang seluruh edh001 menggunakan format/metode baru, tampilkan kartu untuk koreksi, lalu ekspor setelah pengguna menyatakan sesuai. Enam pilot lain tetap dikerjakan pengguna di ChatGPT/Gemini. Tidak ada benchmark manfaat pustaka atau percobaan membuat konsep/gambar dalam kriteria pekerjaan ini.


Perkembangan setelah verifikasi langkah 1–3: [audit ulang edh001](edh001-re-audit.md) telah menghasilkan laporan 1.1 dan kartu yang disetujui pengguna, ZIP final serta ingest lokal yang lulus. Registry kini berisi edh001 sebagai 1 referensi/5 shot aktif. Catatan format 1.0 di atas menjelaskan keadaan sebelum audit ulang, bukan status terkini.
