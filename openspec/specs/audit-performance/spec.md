# audit-performance Specification

## Purpose

Menyediakan pengukuran durasi audit dan percobaan yang dapat dibandingkan antara sesi serta ditelusuri setelah koreksi.

## Requirements

### Requirement: Durasi empat fase audit

Kit SHALL mencatat awal dan akhir setiap fase audit berdasarkan penanda sesi serta menampilkan durasi fase yang selesai. Durasi fase SHALL menunjukkan waktu berlalu, termasuk kegiatan antara perintah, dan tersedia terpisah dari durasi perintah.

#### Scenario: Fase validasi dan ekspor diselesaikan
- **WHEN** penanda mulai dan selesai tersedia untuk suatu fase
- **THEN** ringkasan menampilkan durasi antara kedua penanda tersebut secara terpisah dari durasi masing-masing perintah

#### Scenario: Fase terputus
- **WHEN** suatu fase punya penanda mulai dan belum punya penanda selesai
- **THEN** ringkasan menunjukkan fase belum selesai tanpa mengklaim durasi final

### Requirement: Durasi dan hasil setiap percobaan

Kit SHALL mencatat durasi, identitas percobaan, dan hasil `check-camera`, `complete`, `check-input`, `draft`, `review`, serta `export` di workspace. Ringkasan SHALL menghitung percobaan per operasi dalam sesi, mengaitkan shot dan snapshot bila tersedia, serta menyediakan catatan kegagalan yang cukup untuk menelusuri percobaan ulang.

#### Scenario: Preflight gagal lalu lulus
- **WHEN** `check-input` mengembalikan `ok: false` dan percobaan berikutnya berhasil
- **THEN** log menunjukkan dua percobaan berbeda dengan durasi masing-masing dan satu hasil gagal

#### Scenario: Review dan ekspor kandidat setelah koreksi
- **WHEN** kandidat terbaru berhasil direview dan diekspor dalam sesi yang sama
- **THEN** kedua operasi dapat ditelusuri ke hash snapshot terbaru dan dipisahkan dari percobaan snapshot sebelumnya

#### Scenario: Perintah terputus
- **WHEN** proses berhenti setelah perintah mulai dan catatan terminal belum tercatat
- **THEN** percobaan terlihat sebagai belum selesai pada ringkasan

### Requirement: Ikatan sesi untuk percobaan ekspor

Saat ekspor menerima opsi sesi, kit SHALL memverifikasi metadata sesi dan ikatan receipt atau kandidat yang tersedia. Setelah workspace teridentifikasi dan cocok dengan pengikatan yang tersedia, kit SHALL mencatat percobaan termasuk kegagalan kandidat atau receipt tanpa menulis ke log sesi lain.

#### Scenario: Jalur sesi salah atau receipt terikat sesi lain
- **WHEN** sesi yang diberikan tidak tersedia atau receipt mengikat sesi lain
- **THEN** kit menolak ekspor sebelum mencatat percobaan di jalur tersebut

#### Scenario: Receipt rusak pada sesi yang sah
- **WHEN** workspace sesi yang sah diberikan dan ekspor gagal karena receipt tidak bisa dibaca
- **THEN** ringkasan sesi mencatat percobaan ekspor yang gagal
