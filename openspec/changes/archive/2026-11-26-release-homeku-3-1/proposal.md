# Proposal

## Why

Pada pilot `dreamshome01`, audit kamera terfokus menangkap pergantian fase dan kombinasi Orbit serta Pan yang hilang dalam audit penuh, meski ZIP penuh lolos validasi teknis. HOMEKU 3.1 memberi audit kamera tahap tersendiri dan mengikat hasilnya sampai ekspor, sekaligus merapikan pustaka ke satu versi aktif sebelum dipakai lebih luas. Hasil penuh ChatGPT dan Gemini di 3.1 sama-sama lolos validasi teknis. Keduanya memperlihatkan kebutuhan untuk mempertegas fase awal kamera, memilih panel jernih, dan merapikan kosakata filter area.

## What Changes

- Jalankan empat fase berurutan dalam satu chat dari satu prompt: pemetaan shot, audit kamera, audit desain dan kurasi media, lalu finalisasi dan ekspor.
- Pisahkan panduan kamera dan desain. Selesaikan verifikasi kamera sebelum mengisi desain. Simpan hasil audit di satu `audit.json` dan simpan status verifikasi di workspace audit.
- Periksa bahwa kamera dan Production Start yang sudah diverifikasi tetap sama sampai paket dibuat. Koreksi yang disengaja diperiksa ulang untuk shot terkait.
- Perjelas pemeriksaan awal, overlap, dan akhir komponen kamera. Gunakan frame jernih untuk panel shot biasa, termasuk Production Start sebagai panel Start bila dipilih.
- Normalkan ejaan label dan fungsi area pada indeks serta kueri. Perluas alias yang setara dari semua hasil pilot yang tersedia dan pertahankan label asli pada sumber serta laporan.
- **BREAKING** Terbitkan hanya kit, skema dan kontrak paket HOMEKU 3.1. Hapus penerimaan paket 3.0 serta cabang renderer, template dan layout lama dari runtime aktif.
- **BREAKING** Ganti referensi aktif dengan ZIP hasil audit ulang 3.1 yang dipilih pengguna. Pertahankan ID, MP4 sumber, dan urutan revisi. Perbarui registry dan semua keluaran pustaka bersamaan.

## Capabilities

### New Capabilities

- `phased-audit-authoring` mencakup urutan audit dalam satu chat, pemeriksaan kamera terfokus, pilihan panel jernih, dan ekspor dari hasil yang sudah diverifikasi.
- `library-format-cutover` mencakup kontrak tunggal HOMEKU 3.1, penggantian referensi aktif, dan konsistensi discovery area pada hasil rilis.

### Modified Capabilities

## Impact

- Panduan dan prompt dalam `audit/`, CLI `tools/audit.py`, pengelolaan sesi audit, dan builder kit.
- Skema offline, renderer laporan dan media, validasi paket, registry, ledger, generator katalog dan Knowledge, taksonomi area, indeks pencarian, serta verifikasi GitHub Actions.
- `edh001` saat ini aktif pada revisi 2 dan perlu ZIP pengganti 3.1. `dreamshome01` menjadi pilot audit penuh untuk memeriksa regresi kamera dan panel jernih sebelum rilis.
