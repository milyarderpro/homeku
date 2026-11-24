# Verifikasi Media Tahap 1

> Status setelah reset 24 November 2026: data audit edh001 telah dihapus atas permintaan pengguna. Catatan edh001 di dokumen ini bersifat historis, bukan referensi aktif atau persetujuan audit baru.

Tanggal: 22 November 2026. Versi tampilan terbaru: **2.1.2**. Tahap 2 tidak dijalankan.

## Koreksi sesuai contoh pengguna

Header kolase cukup **SHOT 03 · Kitchen** beserta `8.30–11.57s · 3.27s`, satu baris bila muat. Tidak ada daftar timestamp panel dalam header.

Di bawah masing-masing foto, label **Start**, **Middle**, **End** (atau nomor/nama momen multi area) diikuti timestamp regular yang lebih kecil, misalnya **Start** · 8.30s. Font waktu sekitar 75% ukuran label bold dan sejajar pada baseline yang sama. Ini mengikuti gambar acuan pengguna. Caption panjang dapat membungkus tanpa menimpa foto.

Ukuran judul/nama area yang diperkecil 15% tetap dipertahankan. Storyboard tetap satu baris dengan header ID — Primary style — durasi — jumlah shot; font waktu overview di bawah foto juga lebih kecil daripada nama area. Presisi JSON, indeks/PTS, pilihan frame serta isi audit tidak berubah.

## Kompatibilitas dan pemeriksaan

Template 2.1.2 didaftarkan terpisah; versi sebelumnya dipertahankan melalui dispatch eksplisit. Implementasi 2.1.1 dibekukan pada tools/homeku/media_v2_1_1.py. Kit diperbarui hanya untuk dependensi teknis, tanpa mengerjakan prompt/protokol/provider atau pilot Tahap 2.

| Pemeriksaan | Hasil |
| --- | --- |
| Tes terarah media/report | 25 tes lulus |
| `python -m unittest discover -s tests -t . -v` | **100 tes lulus**, 124,301 detik |
| Library check | Lulus: 1 referensi, 5 shot |
| Kit check | Lulus: 25 file, 826.728 byte |
| Keutuhan sumber/aset/workflow | 41 file dipantau, seluruh hash sama |
| Kandidat 2.1.1 sebelum perubahan | Tetap valid dengan digest snapshot sama |
| Diff whitespace | Lulus |

Tes mencakup header hanya interval/durasi, timestamp kecil kembali ke panel, baseline sejajar, pembungkusan teks, batas foto/koordinat panel, font judul yang tetap kecil, dan kompatibilitas versi terdahulu. Suite penuh juga memeriksa ingest/ekspor, cache, reader serta kit portabel pada fixture terisolasi.

## Preview lokal

Galeri terbaru: `.homeku/previews/edh001-v2.1.2-layout/README.md`. Lima kolase berukuran 2260×1507 dan storyboard 3750×1577; enam JPEG berjumlah 4.839.260 byte. Preview memakai pilihan frame edh001 r0001 yang sudah tersedia dan bukan hasil audit ulang. Label gaya Inggris di preview tetap wording tampilan, bukan penetapan gaya audit V2.

Referensi/video/registry/ZIP edh001 r0001 tetap utuh. Tidak ada paket/revisi baru, fixture aktif, klaim pemeriksaan frame-by-frame baru, atau pelaksanaan Tahap 2.

Riwayat teknis: [2.1.0](v2-stage-1-media-2.1-verification.md), [2.1.1](v2-stage-1-media-2.1.1-verification.md). Keputusan tampilan terbaru pada dokumen ini menggantikan penempatan seluruh timestamp di header pada 2.1.1.
