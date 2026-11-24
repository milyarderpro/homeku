# Verifikasi Penyempurnaan Tampilan Tahap 1 — 2.1.0

> Status setelah reset 24 November 2026: data audit edh001 telah dihapus atas permintaan pengguna. Catatan edh001 di dokumen ini bersifat historis, bukan referensi aktif atau persetujuan audit baru.

Tanggal: 22 November 2026. **Selesai; Tahap 2 tidak dijalankan.**

**Pembaruan terbaru:** [tampilan 2.1.1](v2-stage-1-media-2.1.1-verification.md) memperkecil judul dan memindahkan semua waktu kolase ke blok samping judul. Isi di bawah adalah catatan historis versi 2.1.0.

Penyempurnaan ini menerapkan keputusan pengguna tentang keterbacaan kolase/storyboard serta istilah gaya bahasa Inggris. Ini melanjutkan [fondasi Tahap 1](v2-stage-1-verification.md), tanpa audit ulang atau revisi referensi.

## Hasil

- Judul kolase dan nama area memakai font bold asli. Rentang waktu/durasi berada pada baris kedua, misalnya `8.30–11.57s · 3.27s`.
- Caption normal tepat **Start · 8.30s**, **Middle · 9.93s**, **End · 11.53s**, tanpa mengulang “Tampilan awal” atau ID shot di setiap panel.
- Multi area mempertahankan Start/End; panel antara memakai nama momen sumber, termasuk bila role internalnya middle. Nomor panel menjaga urutan baca.
- Header storyboard: **ID — Primary style — durasi x.xxs — jumlah shot**, mengambil identity.primary_style tanpa menebak dari nama rumah.
- Caption storyboard: nomor shot/nama area tebal, lalu `Overview · x.xxs`. Beberapa area satu shot mempertahankan nomor yang sama.
- Font lebih besar, rata kiri dan ruang caption sejajar. Teks panjang membungkus di luar foto; storyboard lebar tetap menjaga caption di kolom masing-masing. Foto tetap mempertahankan ukuran/rasio sumber.
- Dua desimal hanya tampilan; JSON, frame index/PTS, scope dan pointer sumber tidak dibulatkan atau dimutasi.

## Istilah dan kompatibilitas

Nama gaya utama, pengaruh gaya serta gaya interior memakai bahasa Inggris; prosa penjelasan tetap bahasa Indonesia. Metadata identity.style_names_language=en wajib untuk renderer 2.1.0. Nama ditulis auditor dan dipertahankan apa adanya oleh generator; deklarasi bahasa tidak menjadi mekanisme penerjemahan atau klasifikasi gaya otomatis.

Kontrak source/paket dan reader tetap 2.0. Report/media terbaru 2.1.0 memiliki template beku serta hash font regular/bold; pasangan report/media harus cocok. Renderer 2.0.0 tetap membaca paket lamanya tanpa field bahasa/font bold baru. Implementasi media lama dipertahankan pada tools/homeku/media_v2_0.py, identik byte dengan implementasi sebelum perubahan. Template 2.0.0 dan font regular lama tidak ditimpa.

Kit input diperbarui hanya pada dependensi teknis: modul kompatibilitas, template 2.1.0 dan font bold berlisensi. Prompt/protokol/provider/workflow audit dan pilot Tahap 2 tidak dikerjakan.

## Pemeriksaan aktual

| Pemeriksaan | Hasil |
| --- | --- |
| Tes terarah media/report | 20 tes lulus |
| `python -m unittest discover -s tests -t . -v` | **95 tes lulus**, 126,084 detik |
| `python tools/library.py check` | Lulus: 1 referensi, 5 shot |
| `python tools/build_audit_kit.py --check` | Lulus: 21 file, 811.147 byte |
| `git diff --check` | Lulus |
| Keutuhan referensi/aset | 30 file yang dipantau sama SHA-256 dengan sebelum perubahan |
| Kandidat sintetis 2.0.0 sebelum perubahan | Tetap valid dan digest snapshot tidak berubah |
| Preview akhir | 6 JPEG; hash/dimensi sesuai renderer akhir |

Regresi mencakup teks panjang tanpa overlap foto, caption storyboard lebar tetap dalam kolom, font benar-benar Bold, header memakai primary style, nomor shot multi area tetap, label normal tanpa pengulangan, label momen multi area serta presisi sumber. Jalur ingest/ekspor, reader, cache, kapasitas dan kit portabel turut lulus melalui suite penuh.

## Preview nyata tanpa audit ulang

Lima kolase dan satu storyboard dihasilkan dari pilihan frame edh001 r0001 yang sudah tersedia, menggunakan renderer 2.1.0. Preview lokal berada di `.homeku/previews/edh001-v2.1-layout/`; README di sana menampilkan seluruh gambar. Workspace ini tidak masuk registry, incoming atau paket final.

Kolase per shot berukuran 2260×1588; storyboard 3750×1625. Total enam JPEG **4.928.352 byte**. Jumlah file lebih sedikit tidak diklaim otomatis memperkecil byte. Resolusi dan pengaturan kompresi tetap eksplisit.

Label Contemporary Modern pada preview adalah wording tampilan Inggris untuk menunjukkan header baru, bukan hasil audit gaya V2 atau perubahan nama gaya yang telah diterima. Penetapan gaya V2 tetap pada audit Tahap 2. Data audit/manifest/media, video, ZIP r0001 dan registry edh001 tetap utuh. Tidak ada pemeriksaan frame-by-frame baru yang diklaim, persetujuan isi V2, r0002 atau pilot baru.
