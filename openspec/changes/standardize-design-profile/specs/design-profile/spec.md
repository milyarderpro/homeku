# Spec Delta

## Purpose

Menstandarkan Profil Desain sebagai ringkasan visual yang mudah dibaca manusia dan dapat digunakan AI untuk mencari tipe rumah serta mengadopsi susunan ruang, palet, pencahayaan, dan atmosfer.

## ADDED Requirements

### Requirement: Every new audit assesses one house type

Kit baru SHALL mengarahkan auditor untuk menilai tepat satu tipe rumah. Label Inggris bersifat terbuka. Tipe spesifik yang diperkirakan secara wajar SHALL dapat dicatat sebagai `uncertain`, tipe umum SHALL dapat dipilih jika paling sesuai dengan bukti, dan `unknown` SHALL tersedia ketika video tidak mendukung klasifikasi apa pun.

#### Scenario: A house type is outside the starter list

- **WHEN** massa vertikal dan tipologi yang terlihat mendukung `Tower House`
- **THEN** audit menerima `Tower House` sebagai label asli tanpa perubahan taksonomi
- **AND** menyimpan status serta bukti frame klaim

#### Scenario: Type evidence is limited

- **WHEN** dua tipe sama-sama masuk akal berdasarkan frame
- **THEN** auditor memilih perkiraan paling masuk akal dan mencatat `uncertain`
- **AND** ketika tidak ada tipe yang dapat diperkirakan, auditor mencatat nilai kosong dengan state `unknown`

### Requirement: The house palette is structured and evidence bound

Audit baru SHALL menyimpan palet terstruktur sebagai sumber tunggal dengan nama warna, peran, HEX enam digit, dan bukti frame per entri. Auditor SHALL menargetkan empat sampai enam warna ketika cakupan video mendukungnya. Jumlah yang lebih sedikit SHALL diterima jika itu yang dapat direpresentasikan secara wajar.

#### Scenario: Choosing visual color references

- **WHEN** warna rumah dinilai dari permukaan yang pencahayaannya cukup merata
- **THEN** warna disimpan sebagai estimasi tampilan di frame, disertai nama, peran, kode `#RRGGBB`, dan indeks frame
- **AND** angka yang sama muncul di laporan manusia dan dapat dibaca melalui data identitas AI

#### Scenario: Invalid or duplicate palette source

- **WHEN** audit dengan palet terstruktur memuat HEX yang tidak valid, bukti yang tidak sah, atau palet teks kedua
- **THEN** validasi menolak field terkait sebelum render akhir

### Requirement: The report has one standard design profile

Audit baru SHALL merender Profil Desain dalam urutan identitas, susunan ruang utama, ciri khas, material, pencahayaan, atmosfer, lingkungan, dan tabel palet. Pencahayaan SHALL merangkum kondisi cahaya dan atmosfer SHALL merangkum kesan visual. Palet rumah SHALL tampil satu kali di Profil Desain.

#### Scenario: Rendering a full profile

- **WHEN** audit baru memiliki tipe rumah, susunan ruang, material, pencahayaan, atmosfer, lingkungan, dan palet
- **THEN** laporan menampilkan baris terpisah untuk masing-masing dan tabel Peran, Warna, HEX sebelum Ukuran & Proporsi
- **AND** laporan memiliki enam bagian utama dan Detail Shot tetap memuat konteks warna serta pencahayaan area

### Requirement: House type is a searchable reference facet

Pencarian SHALL mendukung satu filter tipe rumah yang dapat digabung dengan gaya, skala, dan filter shot. Alias terkurasi SHALL digunakan saat membandingkan label. Hasil identitas SHALL menyediakan profil dan bukti yang tersimpan di sumber.

#### Scenario: Searching by alias, style and scale

- **WHEN** pengguna mencari tipe `vila`, gaya `Organic Modern`, dan skala `small`
- **THEN** hasil mencakup referensi aktif yang memenuhi ketiganya dan menggunakan tipe ekuivalen `Villa`
- **AND** label sumber dan pointer tetap tersedia dalam hasil

#### Scenario: Searching by certainty

- **WHEN** sebuah tipe tercatat sebagai `uncertain`
- **THEN** pencarian biasa dapat menemukannya
- **AND** pencarian dengan `--observed-only` mengecualikannya

### Requirement: Original snapshots retain validation and publish by revision

Paket 3.0 yang sudah dibuat SHALL divalidasi terhadap template yang tercatat di manifest dan mempertahankan byte aslinya. Penerapan Profil Desain pada referensi aktif SHALL masuk melalui satu ZIP revisi yang menunjuk snapshot aktif sebelumnya.

#### Scenario: Reviewing an existing 3.0 package

- **WHEN** pustaka memvalidasi audit awal yang belum memuat profil baru
- **THEN** paket diperiksa dengan template awal dan data sumbernya tetap utuh
- **AND** audit baru dengan profil baku memerlukan template baru yang sesuai dengan isi auditnya

#### Scenario: Exporting and choosing an updated reference

- **WHEN** kandidat revisi profil selesai diperiksa secara teknis
- **THEN** ZIP diekspor segera dengan receipt yang sesuai dan tautannya diberikan bersama laporan serta media
- **AND** ingest mengganti referensi aktif melalui rantai revisi setelah pengguna memilih ZIP tersebut
