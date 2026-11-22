# Audit ulang edh001 — disetujui dan diekspor final

Tanggal: 22 November 2026. Audit ulang seluruh durasi telah dilaksanakan menggunakan format 1.1. Pengguna telah menyetujui keseluruhan snapshot dan meminta ekspor final dengan pesan “saya setuju dan eskpor final sekarang”. Ekspor final sudah dilakukan, kemudian pengguna meminta “unggah sekarang”. ZIP telah diserahkan melalui incoming/ dan di-ingest menjadi referensi aktif lokal.

- [Laporan sumber untuk manusia](../audit/pilots/edh001/analysis.md)
- [Kartu tinjauan dari snapshot yang sama](../audit/pilots/edh001-review.md)
- [Storyboard lima area](../audit/pilots/edh001/media/storyboard.jpg)
- [Manifest dan log frame](../audit/pilots/edh001/manifest.json)

## Cakupan pemeriksaan nyata

Video asli 18,4 detik, 30 FPS, 720×1280, 552 frame. Baseline memeriksa 189 pilihan frame pada 10 FPS beserta frame asli pertama/terakhir setiap shot. Delapan lintasan pendalaman native dan satu pemeriksaan frame media kandidat mencakup 415 frame, sebagian bertumpang tindih baseline. Total **461 frame unik** benar-benar ditampilkan dan diperiksa.

| Shot | Frame unik diperiksa | Frame asli dalam shot | Metode |
| --- | --- | --- | --- |
| 01 | 96 | 142 | Baseline + pendalaman transisi dan ekor |
| 02 | 107 | 107 | Baseline + seluruh frame native |
| 03 | 79 | 98 | Baseline + pendalaman awal/akhir dan frame tengah kandidat |
| 04 | 103 | 103 | Baseline + seluruh frame native |
| 05 | 76 | 102 | Baseline + pendalaman awal/akhir |

Seluruh 10 contact sheet baseline dan 31 contact sheet pendalaman native diperiksa, diikuti pembesaran frame awal/akhir dan pemeriksaan media/storyboard kandidat. Rangkaian frame pemeriksaan berada sementara di .homeku/ dan tidak masuk ZIP atau Git. Audit tidak diklaim sebagai seluruh 552 frame diperiksa. Audio tidak diperiksa.

## Isi snapshot yang disetujui

Laporan memuat 30 klaim profil DNA, narasi palet/karakter, lima shot, 128 fakta dan enam fase kamera. Tabel teknis dilipat; gambar dan uraian manusia terlihat langsung. Koreksi kamera shot 02 diterapkan, eksterior dibaca ulang sebagai orbit lalu pendekatan, dan orbit bedroom serta pan bathroom dicatat dengan bukti serta batas tafsirnya. Estimasi sudut/rasio bukan hasil rekonstruksi pose fisik.

Paket final mempunyai 22 JPEG: storyboard, empat gambar wajib per shot, dan satu reveal eksterior pada 2,2 detik untuk menjelaskan perpindahan fase. Area-overview tetap satu frame asli tiap shot, awal untuk IN dan akhir untuk OUT sesuai cakupan aktual. MP4 tidak diduplikasi karena sumber kanonis tersedia dan hash cocok.

## Verifikasi yang dijalankan

- Helper export mode reviewed-export memvalidasi folder serta ZIP setelah dibuka ulang dan mengunci hash MD yang disetujui.
- Kartu review dihasilkan dari MD yang sama; semua ringkasan kamera cocok secara literal.
- Kandidat nyata di-ingest dalam repo sementara: 1 referensi/5 shot. Kontrak JSON lengkap mempertahankan 30 klaim DNA dan 128 fakta.
- Check penuh pada root sementara lulus; build incremental berikutnya tidak menghasilkan perubahan.
- Ingest repo produksi lokal berhasil: 1 referensi/5 shot aktif. Check penuh lulus; build incremental tidak menghasilkan perubahan. MD aktif tetap identik dengan hash yang disetujui.
- Tidak ada perubahan tooling atau klaim pengujian generatif pada pekerjaan audit ini.

| Identitas | SHA-256 |
| --- | --- |
| Video sumber | 3ccf8acf75ca46922025d39b3198e3cf460f9cb3c96c4dc670be0fa2d23c0de8 |
| analysis.md yang ditinjau | 2d04d6bbd7fd35ee813ea7298322d593f195322f864dc2ca23142af57c4a260f |
| ZIP final r0001 | 8d2795ee808c88fa6285bb84e542fe4b4fd6041c007e54011fe34e719bf03b7f |

Ekspor final memakai --reviewed-sha256 untuk mengunci MD yang disetujui. Isi MD dipertahankan persis; sebutan draf/menunggu persetujuan di dalam snapshot menjelaskan tahap penyusunannya sebelum persetujuan pada chat berikutnya. Status persetujuan terbaru dicatat pada dokumen ini, tanpa menulis ulang audit saat ekspor.

[ZIP final edh001-r0001.zip](../audit/pilots/packages/edh001-r0001.zip) berukuran 4215439 byte. Setelah ekspor, CRC ZIP, seluruh hash media, sumber kanonis dan kecocokan MD dengan kartu/ZIP diperiksa ulang. [Paket penyerahan](../incoming/edh001-r0001.zip) sudah masuk incoming/ dan di-ingest tanpa review isi tambahan. [Referensi aktif](../references/edh001/analysis.md) serta [JSON pembaca AI](../data/projections/edh001.json) tersedia; katalog, indeks dan knowledge diperbarui generator. Publikasi GitHub belum dijalankan. Enam pilot lain tetap dikerjakan pengguna di ChatGPT/Gemini.
