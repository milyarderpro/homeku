# Spec Delta

## Purpose

Menetapkan satu kontrak aktif untuk kit dan pustaka HOMEKU serta menjamin bahwa penggantian referensi diterbitkan sebagai satu keadaan yang konsisten.

## ADDED Requirements

### Requirement: HOMEKU 3.1 is the sole supported audit format

Kit, skema audit dan paket, runtime, serta sumber dan keluaran aktif pustaka SHALL menerapkan satu kontrak HOMEKU 3.1. Jalur operasional MUST menolak input audit HOMEKU 3.0 dan memakai satu template laporan serta satu layout media kanonis.

#### Scenario: Validate prior format in the new runtime

- **WHEN** ZIP, folder kandidat, atau sesi dengan format audit 3.0 diberikan ke jalur 3.1
- **THEN** alat menolak input dengan petunjuk untuk mengaudit ulang MP4 memakai kit 3.1

#### Scenario: Build the current kit

- **WHEN** kit dibangun dari file runtime dan kontrak aktif
- **THEN** kit dapat dijalankan mandiri dan hanya memuat skema, panduan, template, dan layout yang dipakai HOMEKU 3.1

### Requirement: Replacement references come from fresh audits

Penggantian referensi aktif SHALL menggunakan ZIP 3.1 hasil audit ulang yang dipilih pengguna dan divalidasi terhadap MP4 kanonis. Penggantian MUST mempertahankan ID referensi dan mencatat revisi serta predecessor secara eksplisit.

#### Scenario: Replace the existing reference

- **WHEN** pengguna memilih paket 3.1 hasil audit ulang untuk referensi aktif dan paket cocok dengan MP4 serta predecessor terkini
- **THEN** penggantian memakai ID yang sama dan menerbitkan revisi berikutnya yang menunjuk revisi terdahulu

#### Scenario: Package is missing or stale

- **WHEN** ada referensi aktif tanpa paket pengganti yang dipilih atau metadata sumber dan predecessor sudah berubah
- **THEN** penerbitan berhenti dan pustaka aktif saat itu tetap tersedia

### Requirement: Cutover publishes a consistent library

Tooling, kit, referensi aktif, registry, dan keluaran generator SHALL berpindah ke 3.1 sebagai satu keadaan pustaka yang telah diverifikasi. Discovery, katalog, indeks, dan Knowledge MUST hanya memakai registry 3.1 dan data referensi yang terdaftar.

#### Scenario: Publish all replacements

- **WHEN** semua paket yang dipilih telah lulus pemeriksaan dan keluaran pustaka sudah dibangun ulang
- **THEN** snapshot yang diterbitkan memuat tooling dan kit 3.1 beserta referensi, incoming aktif, registry, ledger, katalog, indeks, dan Knowledge yang konsisten

#### Scenario: A preparation step fails

- **WHEN** validasi paket atau pemeriksaan ulang pustaka gagal saat menyiapkan cutover
- **THEN** snapshot campuran tidak diterbitkan

### Requirement: Area filters normalize equivalent wording

Pembuatan indeks dan pencarian SHALL memakai normalisasi yang sama untuk huruf besar-kecil, spasi, tanda hubung kata, serta alias area dan fungsi yang setara. Label asli SHALL dipertahankan dalam sumber dan laporan. Istilah dengan makna berbeda SHALL tetap dapat dicari secara khusus.

#### Scenario: Find an area through a spelling variant

- **WHEN** auditor menulis fungsi `dining-area` atau `dining area` dan pengguna mencari `dining`
- **THEN** pencarian menemukan shot terkait melalui fungsi area yang tercatat

#### Scenario: Discover new wording without a predefined alias

- **WHEN** auditor memperkenalkan fungsi `Reading Nook` dan pengguna mencari `reading-nook`
- **THEN** pencarian menemukan fungsi itu melalui variasi penulisan dan label asli tetap terlihat di referensi

#### Scenario: Multi-function area matches its explicit functions

- **WHEN** satu area berlabel `Kitchen & Dining` memuat fungsi kitchen dan dining
- **THEN** pencarian menemukan shot untuk setiap fungsi maupun kombinasi keduanya dan laporan mempertahankan label area asli
