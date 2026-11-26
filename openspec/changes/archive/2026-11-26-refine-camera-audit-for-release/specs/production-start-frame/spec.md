# Spec Delta

## Purpose

Memberi pengguna dan AI acuan framing awal yang bisa dipakai untuk produksi ketika transisi menutupi frame pertama video sumber.

## ADDED Requirements

### Requirement: A transition can have a separate production start

Jika transisi mengaburkan awal shot, audit SHALL dapat menunjuk satu frame native jernih dalam shot tersebut dan menyimpan deskripsi framing singkat. Batas shot, panel Start native, Camera Start sumber, dan pilihan Overview SHALL tetap merekam perannya masing-masing.

#### Scenario: Living room starts during a blur transition

- **WHEN** `dreamshome01` Shot 02 mulai pada frame 184 yang kabur dan frame 194 telah menampilkan ruang tamu dengan jelas
- **THEN** audit mempertahankan frame 184 sebagai Start sumber dan dapat menunjuk frame 194 sebagai acuan produksi
- **AND** deskripsi acuan produksi menjelaskan posisi, arah, dan framing dari frame 194

### Requirement: Production start is traceable to native source evidence

Acuan produksi SHALL memiliki indeks valid, PTS dalam shot setelah Start sumber, dan deklarasi frame sudah dilihat. Laporan SHALL menampilkan acuan hanya bila tersedia. Reader SHALL menyediakan penunjuk sumber, framing, dan waktu yang dapat dipakai untuk mengambil frame native dari MP4 kanonis. ZIP SHALL tetap memakai inventaris media 3.0.

#### Scenario: Production frame has no stored panel

- **WHEN** frame acuan valid dan tidak dipilih sebagai salah satu panel
- **THEN** frame tetap dapat dirujuk melalui metadata dan diekstrak dari MP4 kanonis
- **AND** paket tidak menambah JPEG atau video untuk acuan itu

#### Scenario: The choice is outside the shot or was not viewed

- **WHEN** indeks menunjuk frame dari shot lain atau tidak tercakup deklarasi viewed
- **THEN** validasi menolak pilihan tersebut dan menunjukkan bagian yang perlu diperbaiki

### Requirement: Production uses the documented start when available

Alur produksi SHALL memakai framing acuan produksi untuk awal sesuai kronologi sumber jika pilihan itu tersedia. Saat awal sudah jernih, alur SHALL memakai Camera Start dan panel Start biasa. Paket 3.0 tanpa acuan opsional SHALL tetap dapat divalidasi dan dibaca sesuai snapshot asal.

#### Scenario: Older or clear-start package omits an alternate

- **WHEN** paket 3.0 tidak menyimpan acuan produksi terpisah
- **THEN** laporan dan reader mempertahankan data awal sumber yang sudah tersedia
- **AND** jika pengguna mengetahui Start tertutup transisi, alur produksi memeriksa frame sumber sebelum menyusun prompt
