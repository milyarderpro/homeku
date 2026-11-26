# Spec Delta

## Purpose

Menjaga pengamatan gerakan kamera yang konsisten dan dapat dipakai untuk adopsi DNA sumber, dengan bukti temporal yang cukup serta pekerjaan audit yang terarah.

## ADDED Requirements

### Requirement: Directed native sampling
Audit SHALL memakai baseline 6 FPS dan frame native batas setiap shot, tanpa interpolasi. Sumber ≤6 FPS dan shot <1 detik SHALL diperiksa seluruh native. Pendalaman SHALL memakai 10 FPS/native untuk pertanyaan visual dan interval yang dinyatakan, bukan otomatis mengulang seluruh video.

#### Scenario: Short shot uses native frames
- **WHEN** shot berlangsung 0,8 detik pada sumber 30 FPS
- **THEN** baseline mencakup seluruh frame native shot
- **AND** tidak ada frame hasil interpolasi atau frame melintasi cut

#### Scenario: Ambiguous rotation needs deepening
- **WHEN** baseline belum membedakan Pan dari Orbit pada satu interval
- **THEN** auditor dapat menambah pemeriksaan 10 FPS/native dengan alasan khusus interval tersebut
- **AND** baseline shot lainnya tidak diekstrak ulang tanpa kebutuhan

### Requirement: Three-axis observations precede conclusions
Setiap fase SHALL mencatat pengamatan depth, translation dan rotation sebelum simpulan notasi, termasuk Pan-only dan Static. Pengamatan SHALL bertumpu pada perspektif/paralaks/oklusi/jangkar temporal. Goyangan atau tilt tipis insidental MUST NOT otomatis dilabeli Tilt disengaja.

#### Scenario: Screen shift does not alone prove a pan
- **WHEN** objek bergeser di layar tetapi perubahan sudut dan paralaks belum dipisahkan
- **THEN** pemeriksaan menuntut pengamatan ketiga sumbu dan bukti temporal yang sesuai
- **AND** ambiguitas yang tersisa dicatat, bukan diisi label Pan otomatis

#### Scenario: Shared evidence avoids repeated objects
- **WHEN** tiga pengamatan sumbu memakai frame temporal yang sama
- **THEN** fase dapat menyimpan evidence bersama sekali
- **AND** pengamatan masing-masing sumbu tetap spesifik, dengan override bukti bila diperlukan

### Requirement: Flexible camera notation
Notasi SHALL mempertahankan komponen utama/sekunder, + simultan, → urutan fase, intensitas, orientasi, target dan easing. Angka ~×/~° SHALL opsional per komponen; angka tunggal dan rentang sama-sama sah. Ketiadaan angka MUST NOT memaksa alasan khusus atau penurunan confidence.

#### Scenario: Mixed numeric and nonnumeric components
- **WHEN** auditor menulis Dolly-Out (~1.6×) + Orbit Left + Subtle Pan Right (Ease-Out)
- **THEN** notasi diterima dengan seluruh komponen dan qualifier dipertahankan
- **AND** Orbit Left tidak diwajibkan mempunyai derajat

#### Scenario: Sequential movement with a degree range
- **WHEN** auditor menulis Straight Dolly-In → Dolly-In + Strong Pan Right (~25°–30°)
- **THEN** sumber mencatat fase berurutan dan komponen simultan yang sesuai
- **AND** ringkasan turunan mempertahankan urutan serta rentang sudut

#### Scenario: Source uses decimal comma and x
- **WHEN** auditor menulis Dolly-Out (~1,6x)
- **THEN** sumber kerja dapat dinormalisasi menjadi Dolly-Out (~1.6×) tanpa mengubah nilai
- **AND** ekspor kandidat yang telah direview tidak melakukan normalisasi ulang

### Requirement: Visual estimates do not require calibration
Perkiraan skala/sudut SHALL menerima asumsi visual wajar tanpa kewajiban pengukuran piksel atau kalibrasi kamera. ~× SHALL berarti perubahan skala gambar IN=akhir/awal dan OUT=awal/akhir, bukan faktor tempo. Ketidakpastian gerakan yang nyata SHALL dipertahankan.

#### Scenario: Estimated angle without pixel measurements
- **WHEN** auditor memperkirakan Pan Right (~25°) dari perubahan pandangan
- **THEN** estimasi dapat diterima tanpa scale_measurement atau data pose fisik
- **AND** sistem tidak menyatakan estimasi sebagai pengukuran fisik terkalibrasi

### Requirement: Tempo is independent from movement phase boundaries
Tempo SHALL mempunyai satu sumber, berupa label seragam atau segmen perubahan yang menutup shot. Label/tempo fase turunan SHALL mengikuti overlap waktu. Intensitas komponen dan easing MUST NOT otomatis mengganti tempo shot; seluruh shot berlabel moderate SHALL tetap sah.

#### Scenario: Tempo changes within one movement phase
- **WHEN** Dolly-In berlangsung terus sementara tempo berubah moderate menjadi fast
- **THEN** sumber dapat mempertahankan satu fase gerak dan beberapa segmen tempo
- **AND** pembacaan timeline menyampaikan perubahan tempo tanpa menuntut fase gerak palsu

#### Scenario: All shots have the same tempo
- **WHEN** semua shot dinilai moderate berdasarkan pengamatan
- **THEN** validasi menerima distribusi tersebut tanpa memaksa variasi label

### Requirement: Source depth and chronology remain explicit
Depth_direction SHALL diputuskan auditor sebagai IN, OUT, NO IN/OUT atau null ambigu. Konflik dengan Dolly eksplisit SHALL ditolak. Pola kamera SHALL diturunkan dari arah fase; zoom atau perubahan skala saja MUST NOT menjadi bukti translasi, dan default produksi MUST NOT mengubah sumber.

#### Scenario: Zoom does not imply camera translation
- **WHEN** fase Zoom-In tidak memperlihatkan maju kamera yang dapat dipastikan
- **THEN** sistem tidak mengisi IN berdasarkan zoom semata
- **AND** mempertahankan klasifikasi netral atau ambigu auditor beserta batasnya

### Requirement: Optional motion hints summarize valid tracking honestly
Helper SHALL memberikan ringkasan perubahan 2D, cakupan valid dan tren awal–tengah–akhir tanpa verdict gerakan atau perubahan audit/viewed. Agregat total MUST mencerminkan komposisi transform pada rentang valid; kegagalan tracking MUST NOT disembunyikan. Tanpa dependensi opsional, audit visual SHALL tetap dapat dilanjutkan.

#### Scenario: Tracking fails in the middle
- **WHEN** satu interval di tengah shot gagal tracking
- **THEN** ringkasan melaporkan gap dan rentang valid terpisah atau total yang tidak tersedia
- **AND** tidak menyajikan gabungan interval sukses sebagai hasil seluruh shot

#### Scenario: Optional dependencies are unavailable
- **WHEN** helper tidak dapat memuat dependensi tracking
- **THEN** helper mengembalikan status unavailable yang jelas
- **AND** workflow tidak mewajibkan instalasi jaringan atau menghentikan audit visual
