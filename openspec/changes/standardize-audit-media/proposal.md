# Proposal

## Why

Judul media pilot `edh033` mencampur label Indonesia dan Inggris, serta memakai kapitalisasi yang berbeda untuk area sejenis. Pada `edh056`, lima panel multi-area dibagi menjadi empat panel dan satu panel tersendiri, lalu kolase yang berbeda lebar membuat judul serta gambar antarshot bergeser.

## What Changes

- Tetapkan label Inggris singkat dengan Title Case untuk nama area dan caption panel. Catat fungsi ruang secara terpisah agar pencarian bisa menemukan setiap fungsi yang terlihat. Gunakan istilah Inggris yang konsisten untuk nilai teknis yang dipakai pencarian, dengan alias Indonesia terkurasi.
- Selaraskan label sumber di Storyboard, Overview, kolase shot, dan `analysis.md`. Gunakan `&` untuk fungsi dalam satu ruang dan `/` saat menggabungkan label area fisik yang berbeda pada sebuah shot.
- Pertahankan tiga panel pada shot biasa. Dalam mode otomatis, tampilkan lima panel multi-area dalam satu baris pada lebar blok yang sama dengan shot tiga panel. Seimbangkan baris saat panel lebih banyak dan sejajarkan judul, gambar, waktu, serta baris `Camera:` antarshot.
- Terapkan layout baru pada draft berikutnya. Paket 3.0 yang sudah dibuat tetap menggunakan fingerprint layout yang tercatat dalam manifest.
- Sediakan dua preview berdasarkan masalah pada `edh033` dan `edh056`, serta satu ZIP kit yang sudah dibangun ulang.

## Capabilities

### New Capabilities

- `audit-media-presentation` — Label area dan panel yang konsisten, layout kolase dan Storyboard, serta kompatibilitas media paket 3.0.

### Modified Capabilities

## Impact

- Panduan dan prompt audit, nilai label sumber, taksonomi area, renderer media, pemilihan aset layout, serta validasi dan crop media.
- Kit audit mandiri, fixture geometri, dan pemeriksaan kompatibilitas paket aktif serta pilot.
