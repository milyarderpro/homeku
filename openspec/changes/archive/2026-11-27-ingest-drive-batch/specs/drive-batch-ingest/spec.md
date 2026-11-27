# Spec Delta

## Purpose

Memungkinkan pengguna memilih beberapa ZIP audit dari Google Drive dan memasukkannya ke pustaka lokal dalam satu pemanggilan, dengan verifikasi atas paket yang dipilih dan sumber MP4.

## ADDED Requirements

### Requirement: Pemindaian lokal berdasarkan permintaan

Perintah lokal SHALL memindai semua halaman hasil dari folder video langsung di bawah `Audit` pada root HOMEKU yang dikonfigurasi. Pemindaian SHALL membaca Drive saja, melaporkan cakupan jika pemindaian gagal, dan berhenti setelah menyelesaikan atau membatalkan satu batch.

#### Scenario: Pemindaian menghasilkan daftar paket
- **WHEN** pengguna memanggil perintah dan folder HOMEKU dapat diakses
- **THEN** perintah menampilkan paket ZIP dengan nama kanonis dari folder video yang berada di jalur hasil audit
- **AND** laporan, JPEG, shortcut, item di sampah, dan item di luar jalur hasil tersebut tidak ditawarkan untuk ingest

#### Scenario: Pemindaian tanpa ingest atau dibatalkan
- **WHEN** pengguna hanya meminta daftar, membatalkan pemilihan, atau tidak menyetujui paket apa pun
- **THEN** perintah berhenti dan pustaka serta video kanonis tidak berubah

#### Scenario: Folder tujuan ambigu atau daftar belum lengkap
- **WHEN** root atau subfolder `Audit` tidak dapat dipastikan, atau daftar hasil tidak berhasil dipindai sampai tuntas
- **THEN** perintah melaporkan kendala dan tidak memulai persetujuan batch dari daftar yang belum lengkap

### Requirement: Status paket dan urutan revisi

Perintah SHALL membandingkan paket dengan registri aktif dan riwayat ingest. Perintah SHALL menampilkan paket baru atau revisi layak dipilih, melewati paket yang sudah tercatat, dan menandai paket yang konflik atau membutuhkan revisi pendahulu.

#### Scenario: Sebagian paket sudah pernah di-ingest
- **WHEN** terdapat 20 paket dengan 12 ZIP yang cocok dengan registri aktif atau riwayat ingest
- **THEN** ringkasan melaporkan 12 paket sudah masuk dan menampilkan 8 sisanya sebagai paket yang perlu ditinjau atau ditangani
- **AND** paket yang sudah pernah di-ingest tidak ditawarkan lagi

#### Scenario: Revisi aktif dan revisi berikutnya sama-sama ada di Drive
- **WHEN** `r0001` sudah aktif dan ZIP `r0002` tersedia
- **THEN** perintah menawarkan `r0002` sebagai revisi berikutnya dan memberi status sudah masuk untuk `r0001` yang cocok

#### Scenario: ZIP memakai nomor revisi aktif dengan isi berbeda
- **WHEN** isi audit suatu ZIP berbeda dari snapshot aktif dengan ID dan nomor revisi yang sama
- **THEN** perintah melaporkan konflik dan tidak memasukkannya ke batch yang dapat disetujui

#### Scenario: Revisi melompati pendahulu
- **WHEN** paket memerlukan satu atau beberapa revisi pendahulu yang belum aktif
- **THEN** perintah menyebutkan revisi yang harus ikut disetujui dan berhasil di-ingest lebih dahulu, atau menandainya tertunda jika pendahulu tidak tersedia

### Requirement: Persetujuan atas snapshot ZIP

Perintah SHALL meminta persetujuan eksplisit dalam pemanggilan yang sama untuk satu atau beberapa paket. Persetujuan SHALL mengikat ID file, lokasi, nama kanonis, dan SHA-256 ZIP dari daftar. Perintah SHALL memeriksa ikatan itu dan SHA-256 byte ZIP sebelum meneruskannya ke ingest.

#### Scenario: Pengguna menyetujui sebagian paket
- **WHEN** pengguna memilih enam dari delapan paket dan menyetujui pilihan itu
- **THEN** hanya enam paket yang diproses dan dua paket lainnya tetap tersedia untuk pemanggilan berikutnya

#### Scenario: Paket ditimpa pada ID Drive yang sama
- **WHEN** ZIP diganti setelah daftar ditampilkan dengan isi yang berbeda meskipun nama dan ID Drive sama
- **THEN** perintah melewati paket itu, melaporkan bahwa snapshot berubah, dan memerlukan persetujuan baru untuk byte terbaru

### Requirement: Verifikasi sumber MP4 kanonis

Untuk setiap ZIP terpilih, perintah SHALL memakai MP4 yang cocok di `video/<id>.mp4` atau mengambil MP4 asli dari `HOMEKU/Video` jika salinan lokal belum tersedia. Perintah SHALL memverifikasi hash terhadap manifest sebelum memasang sumber lokal baru dan menyerahkan ZIP ke ingest.

#### Scenario: MP4 kanonis sudah cocok
- **WHEN** MP4 kanonis lokal tersedia dengan SHA-256 yang sesuai dengan manifest
- **THEN** perintah menggunakan salinan lokal itu tanpa mengunduh MP4 lagi

#### Scenario: Sumber hanya tersedia di Drive
- **WHEN** MP4 lokal belum tersedia dan sumber yang sesuai ditemukan di bawah `HOMEKU/Video`
- **THEN** perintah memverifikasi SHA-256 byte unduhan lalu menyimpannya di jalur kanonis yang ditetapkan kontrak paket

#### Scenario: Sumber hilang, ambigu atau berbeda
- **WHEN** sumber tidak dapat diidentifikasi, hash unduhan tidak cocok, atau MP4 kanonis yang sudah ada memiliki hash berbeda
- **THEN** perintah melaporkan alasan paket tertunda, mempertahankan MP4 lokal yang sudah ada, dan melanjutkan paket independen lain

### Requirement: Ingest yang dapat diulang dan hasil per paket

Perintah SHALL menyerahkan hanya ZIP yang disetujui dan terverifikasi kepada ingest HOMEKU. Ingest SHALL tetap menegakkan format, urutan revisi, `supersedes`, dan validasi yang berlaku. Hasil batch SHALL menunjukkan status dan alasan tiap paket yang diproses atau ditunda.

#### Scenario: Batch menghasilkan keberhasilan dan kegagalan
- **WHEN** satu paket lolos dan paket independen lain gagal validasi
- **THEN** paket yang lolos menjadi referensi aktif dan paket yang gagal tetap dilaporkan beserta alasannya

#### Scenario: Pemanggilan diulang setelah ingest
- **WHEN** paket yang sama pernah berhasil diproses
- **THEN** pemindaian berikutnya melaporkannya sebagai sudah masuk tanpa membuat referensi atau riwayat sukses ganda

#### Scenario: Pendahulu gagal validasi
- **WHEN** satu paket revisi gagal di-ingest dan paket lain bergantung padanya
- **THEN** revisi yang bergantung padanya tetap tertunda, sementara paket dari ID lain tetap dapat diproses
