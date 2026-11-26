# Spec Delta

## Purpose

Mendukung adopsi gerakan sumber dengan pemeriksaan visual yang menangkap kapan lintasan kamera dan arah pandang berubah.

## ADDED Requirements

### Requirement: Audit isolates movement changes before notation

Auditor SHALL menentukan kapan komponen mulai, berhenti, atau berubah sebelum menyusun notasi dan arah fase. Auditor SHALL memilih frame pembanding berurutan dari baseline 6 FPS dan mempertahankan cakupan native pada shot pendek atau sumber ber-FPS rendah. Pendalaman SHALL dibatasi pada pertanyaan dan interval yang belum terjawab.

#### Scenario: Exterior orbit gives way to approach

- **WHEN** awal shot memperlihatkan perubahan sisi teras selama lintasan melingkar dan bagian berikutnya memperlihatkan pendekatan dominan menuju tangga
- **THEN** ringkasan mempertahankan fase Orbit lalu Dolly-In secara berurutan
- **AND** kemunculan pendekatan hanya dicatat pada interval yang didukung frame

#### Scenario: Pan starts after a straight kitchen approach

- **WHEN** kamera mula-mula mendekati wastafel dengan arah relatif stabil lalu menyapu ke kompor sambil tetap mendekat
- **THEN** ringkasan mempertahankan `Straight Dolly-In → Dolly-In + Pan Right` serta intensitas atau sudut yang layak ditaksir

### Requirement: Audit compares competing lateral interpretations

Auditor SHALL membandingkan jangkar dekat, jangkar jauh, dan orientasi bidang ketika membedakan Pan, Orbit, dan Truck. Auditor SHALL mempertimbangkan perubahan skala akibat Dolly dan mencatat komponen simultan yang didukung. Pergeseran layar saja MUST NOT menentukan arah badan kamera.

#### Scenario: Living room has orbit and compensating pan

- **WHEN** kamera mundur, perapian bergeser ke kanan, dan orientasi meja berubah dengan paralaks yang mendukung lintasan badan ke kanan
- **THEN** notasi mempertahankan `Dolly-Out + Orbit Right + Pan Left` dalam fase yang sama

#### Scenario: Perspective changes are inconclusive

- **WHEN** skala atau sapuan terlihat tetapi perbandingan bidang dan jangkar belum membedakan Orbit dari Truck
- **THEN** auditor mencatat gerak yang didukung dan ketidakpastian yang relevan pada pengamatan fase

### Requirement: Audited notation agrees with temporal observations

Auditor SHALL mencocokkan jenis, arah, fase, dan qualifier notasi dengan frame serta pengamatan. Estimasi SHALL ditulis jika wajar untuk komponen yang bersangkutan. Laju SHALL dinilai dari interval PTS setara dan mempertimbangkan perspektif. Pemeriksaan semantik SHALL terjadi sebelum review dan ekspor melalui panduan audit yang ada.

#### Scenario: Dolly makes a fixed object scale nonlinearly

- **WHEN** jangkar membesar makin cepat tetapi bukti belum memisahkan efek perspektif dari laju kamera
- **THEN** estimasi skala dapat dipertahankan dan qualifier percepatan hanya dicatat bila didukung
- **AND** tempo shot tetap berasal dari penilaian tempo terpisah

#### Scenario: Several components have different estimation quality

- **WHEN** skala Dolly dapat ditaksir dan putaran Orbit serta Pan yang mengimbanginya belum dapat diukur secara wajar
- **THEN** notasi mencantumkan skala Dolly dan mempertahankan arah Orbit serta Pan tanpa angka yang ditebak
