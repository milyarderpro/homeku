# Audit Session Workflow

## Purpose

Membantu auditor memastikan kit siap, melihat pekerjaan yang tersisa, dan mengonfirmasi batas shot dari video sumber.

## ADDED Requirements

### Requirement: Pemeriksaan kesiapan audit

Kit SHALL memeriksa kesiapan Python, dependensi inti termasuk OpenCV dan NumPy, keterbacaan MP4, ekstraksi satu frame, serta akses tulis workspace.

#### Scenario: OpenCV atau NumPy tidak tersedia
- **WHEN** OpenCV atau NumPy tidak bisa dimuat
- **THEN** kit melaporkan audit belum siap dan menunjukkan dependensi yang perlu dipasang

#### Scenario: Pemeriksaan inti gagal
- **WHEN** MP4 gagal dibuka, frame gagal diekstrak, atau workspace tidak dapat ditulis
- **THEN** kit melaporkan pemeriksaan yang gagal beserta tindakan berikutnya dan membiarkan catatan audit kerja utuh

### Requirement: Status pekerjaan pada sesi yang dilanjutkan

Kit SHALL menampilkan frame baseline yang belum dilihat menurut seluruh pass pada shot, serta ID pass dan indeks yang deklarasinya belum lengkap per pass. Kit SHALL menampilkan status checkpoint kamera dan kecocokan receipt terhadap kandidat. Jika receipt mencantumkan sesi, status SHALL memeriksa kecocokan sesi tersebut.

#### Scenario: Sesi dengan koreksi kamera dan receipt lama
- **WHEN** auditor membuka status sesi setelah kamera satu shot berubah dan snapshot kandidat berbeda dari receipt
- **THEN** kit menunjukkan shot yang perlu diperiksa ulang dan receipt yang usang
- **AND** pemeriksaan status membiarkan deklarasi `viewed` dan checkpoint tersimpan sesuai bukti yang sudah ada

#### Scenario: Frame baseline sudah dilihat lewat pass native
- **WHEN** pass native sudah mencatat frame baseline sebagai dilihat, sementara deklarasi pada pass baseline masih belum lengkap
- **THEN** status menunjukkan frame baseline tersebut sudah dilihat dan tetap menampilkan ID pass baseline beserta indeks yang perlu dideklarasikan pada pass itu

#### Scenario: Receipt mengikat sesi lain
- **WHEN** hash kandidat cocok dengan receipt yang terikat sesi lain
- **THEN** status menyatakan receipt usang dan menunjukkan perbedaan sesi

#### Scenario: Kandidat atau receipt belum tersedia
- **WHEN** auditor melihat status sesi sebelum kandidat atau receipt tersedia
- **THEN** kit menyebut artefak yang belum tersedia tanpa melaporkan bahwa review telah lulus

### Requirement: Pratinjau dugaan cut

Kit SHALL menyediakan mode opsional pada `inspect` untuk melihat dugaan cut beserta frame native sebelum dan sesudahnya, indeks, dan PTS sumber. Daftar cut yang diberikan ke `prepare` SHALL berasal dari konfirmasi auditor.

#### Scenario: Dugaan cut ditemukan
- **WHEN** mode pratinjau menemukan perubahan visual mendadak
- **THEN** kit menampilkan pasangan frame yang bisa diperiksa, termasuk indeks frame pertama sesudah dugaan cut
- **AND** auditor dapat memakai indeks tersebut jika tayangan memang berganti take

#### Scenario: Perubahan area dalam satu take
- **WHEN** pratinjau menandai perubahan gambar saat kamera melewati pintu dalam satu take
- **THEN** auditor dapat mengabaikan dugaan cut dan melanjutkan dengan satu shot kontinu
