# candidate-review-delivery Specification

## Purpose

Membantu auditor memeriksa kandidat dan menyimpan hasil audit yang sudah diekspor tanpa kehilangan hubungan antara paket dan snapshot yang ditampilkan.

## Requirements

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

Panduan SHALL mendukung satu chat per MP4 dengan kit dari root Drive HOMEKU dan MP4 asli dari subfolder Video. Setelah ekspor lulus, ChatGPT SHALL langsung menyimpan laporan, media, dan ZIP dari ekspor yang sama di `HOMEKU/Audit/<nama-video-tanpa-ekstensi>/` bila aksi Drive tersedia. ChatGPT SHALL mempertahankan jalur media relatif dan memverifikasi SHA-256 ZIP dengan mengunduh kembali byte dari Drive.

#### Scenario: Ekspor pertama tersimpan
- **WHEN** ZIP selesai diekspor dan konektor menyediakan penyimpanan ke folder tujuan
- **THEN** ChatGPT menyimpan `analysis.md`, file dalam `media/`, lalu ZIP dengan nama kanonis
- **AND** ChatGPT memverifikasi hasil dan memberikan tautan folder serta ZIP Drive bersama unduhan di chat

#### Scenario: Koreksi pada sumber yang sama
- **WHEN** sesi menghasilkan ekspor koreksi dan ID audit serta SHA-256 sumber cocok dengan ZIP Drive sebelumnya
- **THEN** ChatGPT memperbarui byte file bernama sama dengan ID Drive yang sama, melewati berkas yang masih identik, dan membuat berkas yang belum ada
- **AND** ChatGPT melaporkan media terdahulu yang sudah keluar dari inventaris tanpa menghapusnya

#### Scenario: Folder tujuan bertabrakan
- **WHEN** folder dengan nama yang sama merujuk sumber berbeda atau tujuan ambigu
- **THEN** ChatGPT melaporkan konflik sebelum mengubah hasil yang ada

#### Scenario: Aksi penyimpanan atau verifikasi terputus
- **WHEN** sesi tidak dapat menyelesaikan penyimpanan atau verifikasi
- **THEN** ChatGPT melaporkan langkah yang tertunda, mempertahankan unduhan ZIP, dan melanjutkan dari ekspor serta folder yang sudah terikat bila transfer bisa diteruskan

#### Scenario: Pengguna melanjutkan ke ingest
- **WHEN** pengguna menyerahkan ZIP pilihan dari Drive ke alur ingest
- **THEN** ingest memverifikasi paket terhadap MP4 asli kanonis yang tersedia secara terpisah
