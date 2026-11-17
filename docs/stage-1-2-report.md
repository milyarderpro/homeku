# Hasil implementasi tahap 1 dan 2

Tanggal: 17 November 2026. Status: implementasi dan verifikasi lokal selesai. Berkas baru belum di-commit/push; akses remote ke berkas baru melalui web dan konektor belum diuji.

## Hasil

| Bagian | Hasil |
| --- | --- |
| Snapshot pengetahuan | 2026-11-17-stage-1-2-r2 |
| Sumber snapshot | 57 referensi, 295 shot, 6.111 detail visual |
| Inventaris | 62 MP4: 57 terikat referensi dan 5 belum dianalisis |
| Profil | Satu Markdown per referensi; tautan grup lama dipertahankan |
| Kamus | Versi 1.0.1; 107 konsep, 11 dimensi, alias Indonesia/Inggris |
| Pemetaan | 8.743 nilai sumber dengan pointer field dan hash anotasi |
| Regresi | 119 tes lulus |
| Integritas | Sumber, katalog dan build pengetahuan lulus pemeriksaan |

[Mulai membaca](../knowledge/ai-knowledge.md) · [Direktori](../knowledge/directories/README.md) · [Kamus](../knowledge/taxonomy/README.md) · [Snapshot](../knowledge/release.json)

## Tahap 1

Inventaris arsip dipisahkan dari snapshot pengetahuan. Penambahan referensi tidak otomatis mengubah profil, katalog, kamus, jumlah sumber pada snapshot atau interpretasi tematik. Tes tidak lagi mengunci jumlah 57/295 atau delapan grup profil.

Snapshot menyimpan ID dan hash video/anotasi serta versi/hash kamus. Koreksi sumber membatalkan kecocokan snapshot lama sampai publikasi eksplisit. ID rilis dan versi kamus yang diterbitkan bersifat immutable. Source analysis tetap schema 2.1 dan tidak diubah pada implementasi ini.

Runner penyimpanan paralel menghitung ulang manifest setelah rebase. Tes lima worker dengan sumber MP4 berbeda membuktikan inventaris bersama memuat semua hasil tanpa kehilangan referensi. Sinkronisasi otomatis hanya menerima penambahan; perubahan sumber atau anotasi yang telah dipin memerlukan tindakan maintainer eksplisit.

Kontrak JSON Schema tersedia untuk sumber, snapshot, normalisasi, observasi, review AI dan agregat. Kontrak observasi/review/agregat menyiapkan tahap berikutnya; tidak ada review visual baru atau pengukuran rumah yang diklaim.

README, bacaan inti, direktori konsep dan profil menggunakan satu set path bagi pembaca web dan konektor. Pengujian lokal memeriksa navigasi dan identitas sumber. Akses gambar maupun pembacaan remote baru harus diuji setelah publikasi GitHub.

## Tahap 2

Pemetaan menyimpan label asli dan menambahkan konsep berdasarkan dimensi. Ruang, konfigurasi, gaya, pengaruh gaya, atap, bukaan, material appearance, cahaya, kamera, mood dan skala dipisahkan. Sinonim scene terbuka dan modifier kamera dipertahankan tanpa menyamakan pan dengan tracking.

Perbaikan revisi kamus: area tidur pada loft tidak otomatis menjadi kamar tidur terpisah; daylight hangat tidak otomatis menjadi lampu praktikal. Versi kamus sebelumnya dan snapshot awal tetap tercatat.

| Status pemetaan | Nilai |
| --- | ---: |
| mapped | 5.286 |
| unmapped | 3.360 |
| ambiguous | 56 |
| empty | 41 |

Jumlah tersebut mencakup label metadata dan butir shot terpilih; bukan jumlah objek unik. Terdapat 3.277 label ambigu/belum terpetakan yang berbeda dalam daftar tindak lanjut. Label tersebut tetap tersedia bagi AI. Nilai mapped dapat hanya mencakup sebagian atribut dalam satu tag panjang, dan tidak merupakan verifikasi visual.

[Daftar tindak lanjut](../knowledge/taxonomy/mapping-issues.json) · [Laporan cakupan](../knowledge/taxonomy/normalization-report.md)

unknown, missing, empty, not_visible dan not_applicable memiliki makna berbeda. Tidak ada syarat verifikasi manual atau filter yang melarang penggunaan kreatif berdasarkan confidence rendah.

## Verifikasi

- Seluruh 119 tes lulus, termasuk pertumbuhan arsip tanpa promosi snapshot, koreksi anotasi, sumber hilang, perlindungan versi, pemetaan bilingual dan penyimpanan paralel.
- Semua nilai yang dipetakan dapat ditelusuri ke field sumber dan tetap sama dengan nilai sumber.
- Rebuild menghasilkan artefak yang sama; perubahan sidecar terdeteksi.
- Tautan Markdown pengetahuan diperiksa; path grup lama tetap mengarah ke profil individual.
- Source integrity, published catalog dan knowledge build lulus.
- Tidak ada perubahan pada video, gambar, YAML/Markdown analisis sumber atau request historis.

## Batas hasil ini

Normalisasi masih leksikal. Review visual lebih dalam, pengayaan relasi dan evaluasi kreatif merupakan tahap berikutnya. Prototype bacaan inti memakai sintesis/prinsip yang sudah ada; tidak berisi workflow produksi atau prompt generator.

Implementasi ini menyiapkan dua jalur akses dengan korpus yang sama. Keberhasilan pembacaan konten baru melalui web/konektor belum diklaim sebelum berkas tersebut dipublikasikan. Lihat [kontrak akses](../knowledge/access-contract.md) untuk smoke test remote yang diperlukan.

[Petunjuk pemeliharaan](knowledge-maintenance.md) · [Rencana implementasi](knowledge-improvement-plan.md)
