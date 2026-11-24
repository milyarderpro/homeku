# Verifikasi HOMEKU 3.0

OpenSpec `simplify-homeku-single-version`. Implementasi mencakup satu format audit/paket/reader, alur chat, pustaka, dan kit. Pengujian menggunakan video pola sintetis dengan timestamp native.

## Hasil verifikasi

- Alur normal dan multi area lulus dari prepare, viewed, complete, check-input, draft, review, ekspor, hingga ingest dan replay. Setiap file ZIP sama dengan snapshot kandidat yang ditinjau. Ingest memeriksa struktur, hash, dan MP4 kanonis.
- Tes kapasitas memakai 300 model dan MP4 sintetis pada root sementara. Build penuh dan inkremental menghasilkan byte yang sama. Indeks berukuran 2.407.412 byte. Pencarian memakai pagination dan pembacaan shot hanya membuka satu proyeksi.
- Kit empat file memulihkan resource offline di workspace kosong. Salinan runtime tanpa `docs/` dan `openspec/` menjalankan alur fixture, membentuk kit, dan lulus build serta check pustaka.
- Paket dan sesi lama serta format tidak dikenal ditolak. Pemeriksaan SHA-256 mencocokkan 2.074 berkas MP4, arsip, dan hasil pilot dengan baseline. Registry produksi tetap kosong.
- Preview sintetis normal dan multi area memperlihatkan judul dan area tebal, interval dan durasi di header, label panel tebal, waktu panel lebih kecil di bawah foto, Overview satu baris, serta Storyboard vertikal.

Suite inti menjalankan 104 tes. Sebanyak 102 lulus dan dua tes tracking dilewati karena OpenCV/NumPy tidak tersedia pada Python inti. Pengujian terpisah dengan OpenCV/NumPy meluluskan delapan tes motion, termasuk dua tes tracking nyata. Build pustaka, check pustaka, build kit, pemeriksaan kit, dan `git diff --check` selesai dengan status berhasil. Keluaran yang dibangun ulang adalah katalog, Knowledge, indeks, dependencies, build metadata, dan ZIP kit.

## Ukuran dengan isi setara

| Fixture | Fakta tetap | Audit pretty lama → 3.0 | Audit compact lama → 3.0 | Audit + manifest 3.0 | Payload paket sebelum ZIP | ZIP final |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Normal | 7 | 18.023 → 10.610 B | 11.763 → 6.174 B | 16.333 B | 181.866 B | 146.340 B |
| Multi area | 12 | 23.977 → 14.726 B | 15.400 → 8.420 B | 22.057 B | 248.102 B | 195.103 B |

Perbandingan mencocokkan subjek, atribut, nilai, dan status setiap fakta dengan baseline. Tiga fakta kitchen pada fixture multi memakai indeks bukti yang berada dalam visibilitas kitchen. Kit turun dari 948.573 byte dan 90 resource menjadi 831.547 byte dan 52 resource (ukuran ZIP turun 12,3%). Baseline ukuran tersedia untuk audit dan kit. Ukuran payload dan ZIP pada tabel adalah pengukuran format 3.0.

## Waktu tooling pada fixture 1,2 detik

| Tahap | Normal | Multi area |
| --- | ---: | ---: |
| Prepare awal | 0,352 s | 0,336 s |
| Resume | 0,059 s | 0,063 s |
| Complete | 0,064 s | 0,064 s |
| Check-input | 0,123 s | 0,124 s |
| Draft awal | 0,421 s | 0,683 s |
| Draft dengan cache | 0,111 s | 0,118 s |
| Draft setelah koreksi notasi | 0,145 s | 0,142 s |
| Helper aktif, pertama / cache | 0,155 / 0,059 s | 0,159 / 0,062 s |
| Helper tidak dipanggil | 0 s | 0 s |

Draft awal dan draft dengan cache menghasilkan byte yang sama. Koreksi notasi mengubah kolase shot dan Storyboard, serta memakai kembali frame kanonis dan Overview. Angka waktu diukur lokal pada fixture. Durasi audit manusia atau provider bergantung pada video, pengamatan, dan koreksi di chat.

Lingkungan inti memakai Python 3.12.3, FFmpeg 6.1.1, Pillow 12.2.0 dan jsonschema 4.26.0. Benchmark dan tes tracking memakai Python 3.12.3, Pillow 10.2.0, jsonschema 4.10.3, OpenCV 4.14.0 dan NumPy 2.5.5. Log pengembangan dan preview sintetis tersedia pada workspace lokal `.homeku/single-version-baseline/`.

## Panduan aktif dan riwayat

- Panduan audit, authoring, prompt, tiga kontrak dan [alur konsep](../audit/concept-workflow.md) ada di [audit/](../audit/README.md). Kit dibangun dari inventaris aktif pada `tools/build_audit_kit.py`.
- Schema aktif berada di `schemas/`. Template, layout, font dan lisensi berada di `tools/assets/`. Prinsip desain disimpan di `sources/design-principles.json`.
- Plan, verifikasi lama, contoh historis di `docs/`, dan dokumen OpenSpec mencatat perkembangan. Panduan operasional dan fingerprint memakai aset aktif di luar folder tersebut.
- Hasil pilot nyata dicatat terpisah. Pengujian tooling tidak menilai akurasi visual pilot baru. [Status tujuh pilot](../audit/pilots/README.md)
