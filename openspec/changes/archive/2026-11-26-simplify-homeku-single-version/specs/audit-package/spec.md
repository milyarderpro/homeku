# Spec Delta

## Purpose

Menjamin hasil audit dapat disiapkan di chat, ditinjau secara manusiawi dan diekspor menjadi paket final yang konsisten tanpa penulisan ulang fakta atau review isi kedua.

## ADDED Requirements

### Requirement: Authoring separates observations from mechanical work
Workflow SHALL menyediakan prepare, pengisian, mark-viewed, complete dan check-input pada audit.json yang sama. Prepare/complete MUST NOT mengarang fakta, arah, tempo atau penilaian. Pembaruan bertahap per shot SHALL mempertahankan isi shot lain dan menulis secara atomik.

#### Scenario: Preparing frames does not declare them viewed
- **WHEN** prepare mengekstrak baseline dan membuat skeleton
- **THEN** frame tersedia untuk diamati tetapi belum dinyatakan viewed
- **AND** skeleton tidak dianggap audit valid atau referensi aktif

#### Scenario: A single shot is corrected
- **WHEN** auditor memperbarui kamera shot-02 melalui helper resmi
- **THEN** audit.json yang sama diperbarui secara atomik
- **AND** isi pengamatan shot lain tetap utuh
- **AND** file patch kerja tidak menjadi sumber final atau isi ZIP

### Requirement: Input validation precedes final image rendering
Check-input/draft SHALL menolak struktur, scope, timeline, bukti atau coverage pemeriksaan yang tidak valid sebelum merender JPEG final. Pesan kesalahan SHALL menunjukkan field dan koreksi yang diperlukan tanpa menyuruh auditor mengarang nilai.

#### Scenario: Missing floor estimate fails before rendering
- **WHEN** draft menerima audit tanpa rentang luas yang diwajibkan
- **THEN** proses gagal pada lokasi field luas
- **AND** tidak menghasilkan JPEG final atau kandidat yang tampak selesai

### Requirement: Human report follows one complete template
Analysis.md SHALL dihasilkan renderer dengan enam bagian: Profil desain, Ukuran & proporsi, Shot Timeline, Overview, Storyboard dan Shot Details. Detail shot SHALL mempertahankan A. Desain area, B. Framing & Lighting, C. Camera Movement, termasuk gerakan sederhana dan teknis.

#### Scenario: A multi-area report is rendered
- **WHEN** satu shot mencakup living dan kitchen
- **THEN** laporan menampilkan satu blok shot dengan detail tiap area dan hubungan ruangnya
- **AND** timeline gerak/tempo, framing, lighting dan seluruh narasi sumber tetap tersedia
- **AND** laporan bukan template kosong atau MD authoring manual

### Requirement: Stored media follows the approved layout
Paket SHALL memuat satu kolase per shot, Overview wide seluruh pilihan satu baris dan Storyboard kolase seluruh shot secara vertikal. Shot normal SHALL memiliki Start/Middle/End; multi area memakai panel dinamis. Hierarki tebal dan waktu caption lebih kecil di bawah gambar SHALL dipertahankan.

#### Scenario: A normal collage retains approved captions
- **WHEN** kolase kitchen normal dirender
- **THEN** judul menyebut Shot dan area dengan hierarki yang rapi
- **AND** label panel berbentuk Start · 8.30s, Middle · waktu dan End · waktu di bawah gambar
- **AND** waktu tidak diulang sebagai baris caption tambahan di header

#### Scenario: Storyboard identity and panel provenance
- **WHEN** Overview dan Storyboard dirender
- **THEN** identitas memuat ID referensi, gaya utama, durasi dan jumlah shot
- **AND** manifest memuat posisi panel/blok yang benar untuk crop tersimpan
- **AND** jumlah JPEG paket adalah jumlah shot ditambah dua

### Requirement: Technical metadata is derived once
Manifest SHALL menyimpan provenance sumber, pemetaan frame/PTS yang dirujuk, selection/media/bbox/hash dan konfigurasi render. Metadata SHALL berasal dari sumber kanonis dan tidak menduplikasi isi keputusan audit. Pembacaan laporan/media tersimpan SHALL tidak memerlukan seluruh frame video.

#### Scenario: Native evidence is outside a stored collage
- **WHEN** fakta memakai frame native yang bukan panel kolase
- **THEN** provenance frame dan PTS tetap tersedia untuk reader
- **AND** paket tidak menyimpan seluruh frame video atau seluruh tabel PTS tanpa kebutuhan

### Requirement: Review binds the entire candidate snapshot
Review SHALL mengikat audit.json, analysis.md, manifest.json dan semua media kandidat. Receipt SHALL berada di luar kandidat dan MUST NOT dianggap persetujuan pengguna. Semua koreksi SHALL diikuti review snapshot terbaru sebelum ekspor yang disetujui.

#### Scenario: Candidate changes after review
- **WHEN** salah satu file kandidat berubah setelah receipt dibuat
- **THEN** export menolak snapshot yang tidak cocok
- **AND** meminta review kandidat terbaru, tanpa menganggap receipt sebagai persetujuan otomatis

### Requirement: Final export packages approved bytes without video
Export SHALL membungkus byte kandidat yang telah ditinjau tanpa render ulang. ZIP SHALL hanya berisi audit.json, analysis.md, manifest.json dan JPEG terdaftar di dalam folder ID. Video, cache, sheet, session, log kerja dan receipt MUST NOT masuk ZIP.

#### Scenario: Approved candidate is exported
- **WHEN** pengguna telah menyetujui keseluruhan snapshot dan export dijalankan dengan receipt yang cocok
- **THEN** byte sumber, MD, manifest dan media ZIP identik dengan kandidat
- **AND** tidak ada ekstraksi video atau render ulang selama export

#### Scenario: Video or extra work file is included
- **WHEN** kandidat/paket memuat MP4, varian ekstensi video atau file kerja di luar allowlist
- **THEN** validasi menolak paket, termasuk perbedaan casing dan path bersarang
- **AND** MP4 sumber tetap diserahkan terpisah
