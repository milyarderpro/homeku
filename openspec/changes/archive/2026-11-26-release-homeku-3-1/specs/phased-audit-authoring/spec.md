# Spec Delta

## Purpose

Menetapkan alur audit dalam satu chat, menjaga hasil pemeriksaan kamera, dan memilih frame panel yang layak ditampilkan dalam paket referensi.

## ADDED Requirements

### Requirement: Audit progresses through four phases in one chat

Panduan audit SHALL mengarahkan satu sesi audit untuk menjalankan pemetaan shot, audit kamera, audit desain dan kurasi media, lalu finalisasi dan ekspor secara berurutan. Panduan kamera dan desain SHALL tersedia secara terpisah dan dibaca pada fase terkait.

#### Scenario: Start an audit from the kit

- **WHEN** pengguna menyediakan kit dan MP4 sumber serta meminta audit lengkap
- **THEN** auditor memetakan batas shot sebelum mengaudit kamera, menyelesaikan pemeriksaan kamera sebelum audit desain, dan meneruskan ke ekspor dalam chat yang sama setelah validasi lulus

#### Scenario: Continuous take crosses areas

- **WHEN** satu take kontinu memperlihatkan beberapa area
- **THEN** pemetaan menghasilkan satu shot dengan kronologi kamera dan area dalam shot yang sama

### Requirement: Camera findings are verified before design authoring

Fase kamera SHALL menilai depth, translation, rotation, awal dan akhir tiap komponen, fase, tempo, besaran yang dapat diperkirakan, serta Production Start bila dipilih. Pemeriksaan kamera SHALL dapat selesai sebelum bagian desain diisi.

#### Scenario: Shot contains overlapping movements

- **WHEN** pemeriksaan frame berurutan memperlihatkan perubahan parallax dan perubahan arah pandang dalam fase yang sama
- **THEN** auditor mengevaluasi kemungkinan Orbit dan Pan bersama-sama dan mencatat semua komponen dan qualifier yang dapat didukung dalam notasi

#### Scenario: Components begin at different times

- **WHEN** pemeriksaan awal memperlihatkan Orbit sebelum pendekatan nyata, kemudian Dolly-In mulai berlangsung saat Orbit masih tampak
- **THEN** notasi fase membedakan Orbit yang lebih dulu, komponen simultan saat keduanya terlihat, dan pendekatan akhir sesuai bukti

#### Scenario: Baseline leaves a visual question open

- **WHEN** frame baseline belum cukup untuk menentukan perubahan fase, membedakan komponen, atau memastikan frame mulai produksi
- **THEN** auditor memeriksa frame tambahan pada bagian terkait sebelum menyelesaikan kamera menurut aturan sampling kit

### Requirement: Final package preserves verified camera findings

Finalisasi dan pembuatan kandidat SHALL mensyaratkan pemeriksaan kamera yang terikat pada MP4, batas shot, dan hasil kamera serta Production Start per shot. Perubahan isi yang terikat SHALL ditolak sebelum kandidat dibuat sampai bagian terkait diperiksa ulang.

#### Scenario: Camera fields change during design

- **WHEN** fase desain mengubah notasi, batas fase, tempo, observasi kamera, atau Production Start yang sudah diperiksa
- **THEN** finalisasi menunjukkan shot dan bagian yang berubah dan menahan pembuatan kandidat

#### Scenario: Only design findings change

- **WHEN** pengguna atau auditor mengubah deskripsi desain, area, atau kurasi media nonkamera dan seluruh aturan audit tetap terpenuhi
- **THEN** finalisasi menggunakan hasil pemeriksaan kamera yang masih berlaku dan renderer memuat data kamera yang sama dari JSON satu sumber

#### Scenario: Source or cut boundaries change

- **WHEN** MP4, batas shot, atau identitas shot berubah setelah pemeriksaan kamera
- **THEN** pemeriksaan sesi tersebut tidak berlaku dan hasil audit wajib dipetakan dan diperiksa kembali terhadap sumber baru

### Requirement: Deliberate camera corrections support scoped recheck

Auditor SHALL dapat memperbaiki satu shot yang sudah diperiksa dan memperbarui pemeriksaan hanya untuk shot itu setelah mengevaluasi ulang bukti dan validasi kamera.

#### Scenario: One shot is explicitly corrected

- **WHEN** auditor memperbarui gerakan atau frame mulai produksi pada satu shot dan memeriksa kembali frame untuk shot tersebut
- **THEN** sistem memperbarui status untuk shot itu dan mempertahankan hasil pemeriksaan shot lain yang masih cocok

### Requirement: Normal shot panels show selected clear frames

Panel `Start`, `Middle`, dan `End` pada shot biasa SHALL memakai frame jernih yang telah dilihat dalam urutan sumber. Start memakai frame jernih pertama atau Production Start bila dipilih. End memakai frame jernih terakhir. Middle memakai frame native jernih dengan PTS terdekat ke `(start_s + end_s) / 2`, dengan `start_s` dan `end_s` dari batas shot sumber. Pilih Middle di antara panel Start dan End. Timeline SHALL mengikuti batas native shot.

#### Scenario: Transition obscures a native endpoint

- **WHEN** frame awal atau akhir native mengandung blur transisi, motion blur berlebihan, atau artefak transisi
- **THEN** kolase dan Storyboard menampilkan frame jernih sesuai peran panel, serta batas native, durasi, fase dan notasi kamera tetap sesuai sumber

#### Scenario: Production Start is later than the native first frame

- **WHEN** auditor memilih Production Start karena awal shot tertutup transisi
- **THEN** panel Start memakai Production Start dan Camera Start tetap merujuk pada awal sumber

#### Scenario: A transition moves a selected endpoint

- **WHEN** salah satu panel ujung digeser agar bebas blur
- **THEN** auditor tetap menghitung midpoint dari batas shot sumber dan memilih frame jernih terdekat ke titik tersebut di antara panel Start dan End

#### Scenario: The selected frame lacks eligible evidence

- **WHEN** panel terpilih berada di luar shot, melanggar urutan, atau belum dinyatakan dilihat
- **THEN** kandidat ditahan sampai pilihan panel dan deklarasi viewed sesuai

### Requirement: Reviewed snapshot is exported in the same chat

Setelah input, kandidat, dan snapshot lolos pemeriksaan teknis, audit lengkap SHALL menawarkan ZIP final sesuai aturan paket HOMEKU. Berkas kerja verifikasi internal dan MP4 sumber MUST tetap di luar ZIP.

#### Scenario: Four phases pass

- **WHEN** fase finalisasi selesai dan receipt teknis mengikat snapshot kandidat yang valid
- **THEN** ekspor membungkus snapshot itu menjadi satu ZIP final dengan JSON, laporan, manifest dan media untuk diunduh
