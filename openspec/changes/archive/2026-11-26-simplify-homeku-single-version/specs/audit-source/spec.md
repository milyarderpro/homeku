# Spec Delta

## Purpose

Menetapkan sumber audit final yang ringkas untuk manusia dan AI, tanpa kehilangan detail desain, status pengamatan, hubungan area atau kronologi shot.

## ADDED Requirements

### Requirement: One canonical compact audit source
Sistem SHALL memakai audit.json sebagai satu sumber keputusan isi audit. Field mekanis yang dapat diturunkan, termasuk parsed components, camera summary, coverage paralel dan metadata panel standar, MUST NOT diwajibkan atau ditulis kembali ke sumber final.

#### Scenario: Final source stays compact after completion
- **WHEN** auditor menyelesaikan sumber dan menjalankan complete
- **THEN** sumber tetap memakai struktur ringkas yang sama tanpa penambahan profile paralel, components_parsed, camera_summary atau fact_coverage
- **AND** renderer dan generator memperoleh turunan yang diperlukan secara deterministik

### Requirement: Design identity is recorded once
Sumber SHALL menyimpan nama, gaya utama, pengaruh gaya, gaya interior, ukuran dan karakter DNA pada satu lokasi terstruktur per nilai. Nama gaya MUST memakai istilah Inggris; uraian manusia memakai bahasa Indonesia. Sumber MUST NOT mewajibkan 17 objek profil kosong.

#### Scenario: Styles remain discrete and searchable
- **WHEN** auditor mencatat satu gaya utama dan dua pengaruh gaya
- **THEN** ketiganya tersimpan sebagai nilai terpisah yang dapat dicari
- **AND** laporan memakai nilai sumber yang sama tanpa terjemahan atau salinan klaim profil kedua

#### Scenario: An unassessed characteristic is omitted
- **WHEN** suatu karakter DNA tidak diisi
- **THEN** reader memperlakukannya sebagai tidak dinilai
- **AND** generator tidak mengubah ketiadaan field menjadi not-present atau klaim observed

### Requirement: Floor area remains a required estimate
Sumber SHALL memuat rentang perkiraan luas lantai dengan min dan max positif serta berurutan. Laporan MUST menampilkan rentang dan satuan m² tanpa tambahan dasar perkiraan atau label kepastian yang diwajibkan sistem.

#### Scenario: Floor estimate is displayed directly
- **WHEN** sumber memuat min 60 dan max 90
- **THEN** laporan menampilkan 60–90 m²
- **AND** validasi tidak mewajibkan esai dasar perkiraan atau kalibrasi dimensi

#### Scenario: Floor estimate is missing
- **WHEN** salah satu batas luas tidak diisi atau min lebih besar daripada max
- **THEN** pemeriksaan input gagal pada field luas tanpa mengarang nilai pengganti

### Requirement: Narrative and structured facts retain their distinct roles
Setiap blok desain area SHALL menyediakan uraian arsitektur, furnitur/dekorasi dan lingkungan beserta fakta terstruktur pada kategori terkait. Scope kategori/area SHALL eksplisit melalui struktur atau override. Generator MUST NOT mengekstrak fakta dari prosa atau memangkas fakta berdasarkan kuota.

#### Scenario: Kitchen facts belong to their categories
- **WHEN** auditor mencatat kabinet, peralatan dan pemandangan luar pada satu kitchen
- **THEN** narasi lengkap tampil dalam tiga kategori laporan
- **AND** fakta terkait tersedia untuk AI dengan kategori, scope dan pointer asal
- **AND** tidak diperlukan daftar fact_ids terpisah untuk mengulangi pemetaan kategori

### Requirement: Claim state and evidence are preserved
Klaim SHALL mempertahankan state eksplisit dan evidence yang sesuai scope; observed, uncertain, not-visible, not-present dan unknown MUST tetap berbeda. Confidence dan note yang diberikan auditor SHALL dipertahankan. Confidence yang tidak diisi MUST NOT diganti dengan high atau dianggap telah dinilai.

#### Scenario: Occluded object is not declared absent
- **WHEN** klaim furnitur berstatus not-visible karena tertutup
- **THEN** reader dan knowledge mempertahankan not-visible dan bukti/batasnya
- **AND** tidak memublikasikannya sebagai not-present atau fakta observed

#### Scenario: Evidence belongs to a different shot
- **WHEN** klaim menunjuk frame di luar scope shot yang diizinkan
- **THEN** validasi menolak klaim dan menunjukkan lokasi kesalahannya

### Requirement: Shots represent uninterrupted takes
Satu shot SHALL mencakup satu take kontinu sampai cut nyata. Pergantian area MUST NOT otomatis membuat shot baru. Sumber SHALL membedakan identitas area fisik, fungsi area, interval visibilitas, rute yang dilalui dan hubungan ruang yang dinyatakan.

#### Scenario: Exterior to living to kitchen without a cut
- **WHEN** satu lintasan kontinu memperlihatkan exterior, living dan kitchen tanpa cut
- **THEN** sumber memuat satu shot dengan beberapa area dan timeline kamera terkait
- **AND** rute kamera dibedakan dari area yang hanya terlihat

#### Scenario: Reentry and repeated room labels
- **WHEN** area muncul kembali atau dua ruang fisik mempunyai label bathroom yang sama
- **THEN** visibilitas berulang tetap dapat dicatat
- **AND** dua ruang fisik berbeda mempertahankan ID area berbeda

### Requirement: Framing and selected overview retain separate meanings
Sumber SHALL mempertahankan posisi/arah/angle awal kamera, framing awal/akhir, fokus, kedalaman dan pencahayaan sesuai pengamatan. Setiap Overview SHALL menjelaskan frame terpilih tersendiri, bukan mengganti Camera Start dengan posisi Overview.

#### Scenario: Dolly-out overview occurs at the end
- **WHEN** gambaran area terlengkap dipilih pada akhir shot OUT
- **THEN** Overview menjelaskan posisi akhir tersebut
- **AND** Camera Start tetap menjelaskan awal sumber
- **AND** pilihan frame tetap mempunyai provenance tanpa menyimpan seluruh frame video
