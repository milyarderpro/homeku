# Proposal

## Why

HOMEKU masih membawa beberapa generasi schema, parser, renderer dan panduan yang saling bergantung, sehingga audit chat lebih rumit dan aturan mudah bertentangan. Pustaka aktif sudah kosong setelah reset edh001; ini kesempatan mengganti struktur secara bersih sebelum referensi bertambah menjadi ratusan.

## What Changes

- **BREAKING**: gunakan hanya format 3.0 untuk audit, paket, report, media dan reader; hapus runtime, schema, aset, flag serta alias CLI format lama. Tolak paket/session lama secara jelas tanpa migrasi otomatis.
- Ringkas audit.json sebagai sumber final: profil desain ditulis sekali, fakta melekat pada kategori desain, kamera mempunyai satu notasi per fase, metadata turunan dihitung tanpa ditulis ulang.
- Pertahankan detail arsitektur/furnitur/lingkungan, nama gaya Inggris, luas lantai min–max wajib, status/negasi/bukti, multi area dan hubungan ruang.
- Satukan pengamatan kamera dan aturan angka opsional, baseline 6 FPS, pendalaman terarah, tempo independen dari fase gerak, serta helper statistik 2D opsional dengan ringkasan makro.
- Pertahankan analysis.md enam bagian sesuai template, tata letak media yang disetujui, review keseluruhan snapshot dan ZIP final tanpa video.
- Sesuaikan ingest, knowledge, pencarian dan reader dengan pointer sumber ringkas; hasil generator tetap deterministik tanpa sintesis AI.
- Pindahkan schema ke schemas/, aset ke tools/assets/ dan panduan/kontrak aktif ke audit/. Hilangkan ketergantungan operasi pada docs/ dan dokumen OpenSpec.
- Bangun kit mandiri hanya dari runtime aktif, konsolidasikan tes dan ukur ukuran/waktu berdasarkan fixture setara.

## Capabilities

### New Capabilities

Belum ada main spec dalam OpenSpec proyek ini. Perilaku berikut dibakukan sebagai capability baru; sebagian mempertahankan kebutuhan produk yang sudah ada.

- `audit-source`: sumber audit ringkas, profil DNA, fakta, scope area dan struktur shot kontinu.
- `camera-audit`: sampling/pengamatan, notasi fase, tempo dan statistik pendamping.
- `audit-package`: authoring, validasi, laporan/media, review snapshot dan ekspor final.
- `library-discovery`: ingest/revisi, keluaran generator, pencarian selektif dan provenance pembacaan AI.
- `runtime-distribution`: satu format aktif, kit portable, aset/panduan mandiri dan pemeriksaan kebersihan dependensi.

### Modified Capabilities

Tidak ada: inventaris main spec masih kosong. Perubahan ini sengaja menggantikan kebijakan kompatibilitas dalam dokumentasi repo saat ini sesuai keputusan pengguna.

## Impact

Terpengaruh: tools/homeku/, CLI audit/library, schemas/ baru, kontrak/panduan audit, template/layout, fixture/tes, kit, fingerprint generator dan workflow GitHub. Rincian file dan urutan pengerjaan berada dalam design.md serta tasks.md.

Tidak termasuk: audit ulang video pada tahap proposal, plugin produksi, AI API tambahan, pengujian manfaat lewat konsep/gambar, penghapusan MP4/arsip/hasil pilot, atau penghapusan massal dokumen historis pilihan pengguna. Implementasi tooling dan keberhasilan pilot dicatat terpisah.
