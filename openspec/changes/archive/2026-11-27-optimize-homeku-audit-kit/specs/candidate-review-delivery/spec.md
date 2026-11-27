# Candidate Review and Delivery

## Purpose

Membantu auditor memeriksa kandidat dan menyerahkan ZIP yang dipilih pengguna tanpa kehilangan hubungan antara paket dan snapshot yang ditampilkan.

## ADDED Requirements

### Requirement: Lembar pemeriksaan kandidat

Review SHALL menghasilkan satu lembar ringkas di luar kandidat dari snapshot yang diperiksa. Lembar SHALL memuat hasil pemeriksaan teknis, daftar pemeriksaan visual, dan tautan ke laporan lengkap, Overview, Storyboard, serta kolase dari snapshot tersebut. Saat sesi diberikan, review SHALL memverifikasi metadata sumber, PTS native, dan deklarasi kandidat terhadap sesi.

#### Scenario: Kandidat siap diperiksa
- **WHEN** review teknis lulus untuk kandidat dengan beberapa shot
- **THEN** lembar menampilkan fase kamera, tempo, Production Start bila ada, serta pilihan dan waktu panel untuk tiap shot
- **AND** pemeriksaan visual dapat dicentang setelah dilakukan, dengan memakai media dari kandidat yang sama
- **AND** receipt mengikat snapshot yang akan langsung dibungkus oleh ekspor

#### Scenario: Kandidat memakai deklarasi dari sesi lain
- **WHEN** kandidat merujuk deklarasi frame yang belum dicatat pada sesi yang diberikan, meskipun sumber dan batas shot cocok
- **THEN** review dengan sesi menolak penerbitan receipt

#### Scenario: Kandidat kerja diganti setelah review
- **WHEN** koreksi menghasilkan snapshot berbeda pada folder kandidat yang sama
- **THEN** tautan laporan dan media pada checklist terdahulu tetap membuka file dari snapshot terdahulu
- **AND** ekspor dengan nama kanonis yang sama untuk snapshot berbeda mempertahankan ZIP terdahulu dan mengembalikan jalur paket baru

### Requirement: Ringkasan perubahan kandidat

Lembar review SHALL menunjukkan perubahan notasi, frame dan cakupan bukti, komponen override, pilihan dan cakupan panel, serta media bila ada kandidat sebelumnya yang ditinjau dalam sesi yang sama. Ringkasan SHALL mengidentifikasi kedua snapshot yang dibandingkan.

#### Scenario: Koreksi shot menghasilkan kandidat baru
- **WHEN** kandidat terbaru berhasil direview setelah koreksi satu shot
- **THEN** lembar mengelompokkan perubahan yang relevan pada shot itu dan menunjukkan media yang berubah
- **AND** ringkasan merujuk ke snapshot yang ditinjau sebelumnya dan snapshot terbaru

#### Scenario: Review pertama atau riwayat pembanding belum tersedia
- **WHEN** kandidat belum memiliki snapshot pembanding untuk sesi tersebut
- **THEN** lembar tetap memuat pemeriksaan lengkap untuk kandidat saat ini
- **AND** jika riwayat lama hanya menyimpan sebagian data pembanding, lembar menyatakan cakupan yang tersedia

### Requirement: Penyerahan melalui folder Google Drive HOMEKU

Panduan SHALL mendukung satu chat per MP4 dengan kit dari root Drive HOMEKU yang ditentukan pengguna dan MP4 asli dari subfolder Video. Setelah pengguna memeriksa laporan dan media di chat serta memilih ZIP, ChatGPT SHALL menggunakan subfolder Hasil Audit sebagai tujuan bila aksi unggah tersedia.

#### Scenario: ZIP pilihan pengguna terunggah
- **WHEN** pengguna memilih hasil di chat dan konektor menyediakan unggah ke folder tujuan
- **THEN** ChatGPT mengunggah ZIP ekspor dengan nama `<id>-rNNNN.zip`, memeriksa kembali file dari tujuan, dan memberikan tautan Drive bersama unduhan di chat
- **AND** ChatGPT menyatakan transfer terverifikasi setelah SHA-256 file dari Drive cocok dengan ZIP ekspor

#### Scenario: Aksi unggah atau verifikasi tidak tersedia
- **WHEN** sesi ChatGPT tidak dapat mengunggah ZIP ke folder tujuan atau memastikan hasil transfer
- **THEN** ChatGPT melaporkan status tersebut dan tetap menyediakan ZIP ekspor di chat untuk disimpan ke Drive

#### Scenario: Percobaan unggah diulang
- **WHEN** ZIP dengan nama yang sama sudah ada pada tujuan
- **THEN** ChatGPT memakai tautan yang sudah ada jika SHA-256 sama dan menunjukkan konflik jika isinya berbeda

#### Scenario: Pengguna melanjutkan ke ingest
- **WHEN** pengguna menyerahkan ZIP pilihan dari Drive ke alur ingest
- **THEN** ingest memverifikasi paket terhadap MP4 asli kanonis yang tersedia secara terpisah
