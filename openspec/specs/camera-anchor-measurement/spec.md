# camera-anchor-measurement Specification

## Purpose

Memberi auditor bukti skala gambar dari dimensi jangkar yang sama pada frame native yang dapat diperiksa.

## Requirements

### Requirement: Pengukuran skala dari pasangan titik

Kit SHALL mengukur panjang antara dua titik yang dipilih pada masing-masing dari dua frame native kronologis dalam shot yang sama. Hasil SHALL menyertakan panjang dalam piksel, indeks frame, PTS, arah perubahan skala, dan rasio untuk estimasi `~×`. Untuk pembesaran, rasio adalah akhir dibagi awal. Untuk pengecilan, rasio adalah awal dibagi akhir.

#### Scenario: Tepi kusen membesar
- **WHEN** auditor memilih ujung tepi kusen yang sama dan panjangnya 170 px pada frame awal serta 425 px pada frame akhir
- **THEN** kit menunjukkan kedua panjang, indeks dan PTS, serta pembesaran sekitar `~2.5×`

#### Scenario: Tepi kusen mengecil
- **WHEN** panjang yang dipilih adalah 425 px pada frame awal dan 170 px pada frame akhir
- **THEN** kit melaporkan pengecilan sekitar `~2.5×`

#### Scenario: Koordinat atau frame tidak valid
- **WHEN** titik di luar frame, panjang nol, urutan frame terbalik, atau frame berasal dari shot berbeda
- **THEN** kit meminta data pengukuran yang valid

### Requirement: Pelacakan jangkar dengan konfirmasi auditor

Kit SHALL menawarkan posisi calon titik pada frame berikutnya, menyatakan bila tracking tidak memadai, dan memberi auditor cara mengonfirmasi atau memperbaiki titik. Pasangan titik manual SHALL dapat diukur saat tracking gagal.

#### Scenario: Titik terhalang atau tracking terputus
- **WHEN** salah satu titik hilang selama pelacakan
- **THEN** kit menandai hasil untuk pemeriksaan dan memungkinkan pengukuran dengan titik pada kedua frame yang ditentukan manual

#### Scenario: Pengukuran selesai
- **WHEN** alat menghasilkan pengukuran jangkar dari titik yang dikonfirmasi
- **THEN** hasil disimpan di workspace untuk dipakai auditor saat menulis observasi dan notasi
- **AND** perubahan skala ditampilkan sebagai bukti 2D, sementara keputusan Dolly atau Zoom mengikuti audit depth, translation, dan rotation
- **AND** status `viewed` hanya dicatat melalui deklarasi auditor setelah melihat frame

### Requirement: Upaya estimasi visual per komponen

Auditor SHALL menilai dan mengupayakan estimasi visual setiap komponen gerak yang teridentifikasi. Auditor SHALL memakai angka tunggal atau rentang dengan pembulatan wajar jika frame mendukungnya. Jika pendalaman visual masih belum mendukung perkiraan yang wajar, auditor SHALL mencatat alasan spesifik di `observations`.

#### Scenario: Frame mendukung perkiraan visual
- **WHEN** perbandingan frame mendukung taksiran sudut atau skala suatu komponen
- **THEN** notasi mencantumkan estimasi dengan angka tunggal atau rentang yang sesuai
- **AND** pemeriksaan teknis tetap mengikuti kontrak paket

#### Scenario: Pendalaman visual belum mendukung estimasi
- **WHEN** auditor sudah memeriksa ulang frame pada interval yang relevan dan besaran suatu komponen masih belum dapat diperkirakan secara wajar
- **THEN** notasi boleh melewatkan besaran tersebut dengan alasan spesifik pada `observations`
