# Spec Delta

## Purpose

Menjaga penamaan area dan panel konsisten untuk manusia dan AI, serta menata kolase multi-area dalam Storyboard dengan geometri yang dapat diverifikasi.

## ADDED Requirements

### Requirement: Area labels are consistent across outputs

Audit baru SHALL memakai nama area Inggris yang singkat dan memakai Title Case. Satu label SHALL mewakili satu area fisik. `&` menggabungkan fungsi dalam area itu, sedangkan `/` ditampilkan antararea fisik. Storyboard, Overview, kolase shot, dan laporan SHALL bersumber dari label audit yang sama.

#### Scenario: Titles pair open-plan and loft areas

- **WHEN** shot menampilkan dua area yang dilabeli `Open-Plan Living` dan `Sleeping Loft`
- **THEN** judul shot menampilkan `Open-Plan Living / Sleeping Loft` sesuai urutan area dalam audit
- **AND** caption Overview menyebut label dari area yang masuk dalam frame terpilih

#### Scenario: Bathroom and laundry share one physical area

- **WHEN** bathroom dan laundry menggunakan satu ruang yang sama
- **THEN** media dan laporan dapat menampilkan `Bathroom & Laundry` untuk area itu
- **AND** fungsi `Bathroom` dan `Laundry` tercatat terpisah untuk pencarian

### Requirement: Searchable labels use explicit terms and aliases

Audit baru SHALL mencatat fungsi ruang dan istilah teknis pencarian dengan kosakata Inggris yang konsisten. Pencarian SHALL mempertahankan alias Indonesia yang setara serta label sumber. Hubungan antarfungsi SHALL berasal dari audit.

#### Scenario: Open-plan functions can each be found

- **WHEN** satu area berlabel `Open-Plan Living` memiliki fungsi `Living Room`, `Dining Area`, dan `Kitchen`
- **THEN** pencarian masing-masing fungsi mengembalikan shot yang relevan
- **AND** alias Indonesia seperti `ruang makan` menemukan fungsi dining yang sama

### Requirement: Captions identify panels and camera consistently

Kolase baru SHALL memakai `Start`, `Middle`, dan `End` pada shot biasa. Panel antara pada shot multi-area SHALL memakai label momen Inggris singkat dengan Title Case ketika momen dikurasi. Waktu panel SHALL berada di bawah foto bersama labelnya. Baris notasi di kolase dan Storyboard SHALL memakai `Camera:`.

#### Scenario: The multi-area panels communicate the route

- **WHEN** frame terpilih mencakup awal, fasad yang terbuka, ambang pintu, ruang tamu dan dapur, serta akhir
- **THEN** caption panel tampil berurutan sebagai `Start`, `Facade Reveal`, `Doorway`, `Living & Kitchen`, dan `End`
- **AND** label tampil tebal dengan waktu lebih kecil, sementara notasi kamera tetap mengikuti audit

### Requirement: Storyboard blocks use a shared width and alignment

Layout baru SHALL memakai satu lebar blok berdasarkan shot tiga panel. Pada layout standar, lima panel multi-area SHALL muat dalam satu baris. Jumlah yang memerlukan beberapa baris SHALL dibagi seimbang. Judul, tepi kiri gambar dan baris `Camera:` SHALL sejajar antarshot, dengan waktu shot di sisi kanan.

#### Scenario: Five-panel shot followed by normal shots

- **WHEN** shot multi-area lima panel disusun bersama shot biasa tiga panel dalam Storyboard
- **THEN** lima panel tampil dalam satu baris dengan proporsi foto terjaga dan lebar blok sama dengan shot biasa
- **AND** setiap blok memakai margin kiri bersama

#### Scenario: Six or seven panels use balanced rows

- **WHEN** layout standar menerima enam atau tujuh momen terpilih
- **THEN** panel tersusun masing-masing sebagai tiga tambah tiga atau empat tambah tiga
- **AND** semua panel dalam satu shot mempertahankan urutan sumber

### Requirement: Media crops keep the recorded frame and bounds

Storyboard SHALL tersusun dari kolase shot dan Overview SHALL tetap menjadi satu baris frame wide. Koordinat media SHALL sesuai dengan gambar yang disimpan sehingga pembaca dapat memotong panel atau blok shot melalui metadata manifest.

#### Scenario: Stored crop resolves after adaptive layout

- **WHEN** pembaca meminta panel atau blok shot dari Storyboard dengan layout baru
- **THEN** hasil crop berasal dari selection atau shot yang diminta dengan batas yang sesuai
- **AND** penyesuaian ukuran foto tidak mengganti waktu, urutan, atau isi frame terpilih

### Requirement: Published snapshots retain their layout compatibility

Draft baru SHALL memakai layout baru secara default dalam format paket 3.0. Paket yang sudah dibuat SHALL divalidasi menggunakan layout yang ditunjuk fingerprint manifest. Fingerprint yang tidak dikenal SHALL ditolak.

#### Scenario: An original package is validated after the change

- **WHEN** referensi aktif atau ZIP pilot 3.0 memakai fingerprint layout asal
- **THEN** laporan, korespondensi media, dan metadata tetap dapat divalidasi sesuai snapshot asal
- **AND** file audit serta JPEG yang sudah disimpan tidak ditulis ulang oleh pemeriksaan
