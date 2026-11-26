# Spec Delta

## Purpose

Mendistribusikan satu runtime audit HOMEKU yang bersih, mandiri dan mudah diikuti, tanpa dependensi versi lama maupun dokumen historis yang dapat dihapus pengguna.

## ADDED Requirements

### Requirement: Only one active format is supported
Runtime, schema, paket, report, media dan reader SHALL memakai identitas format 3.0 tunggal. Format/session lama SHALL ditolak dengan petunjuk audit ulang. Runtime/kit MUST NOT menyertakan parser, renderer, adapter atau opsi pemilihan versi lama.

#### Scenario: A legacy package is submitted
- **WHEN** paket 2.5 atau sumber MD legacy diminta divalidasi/di-ingest
- **THEN** sistem menolak dengan pesan format tidak didukung dan petunjuk memakai kit terbaru
- **AND** tidak mengonversi, merender atau mengubah paket tersebut

#### Scenario: CLI exposes the final audit workflow
- **WHEN** pengguna/AI membuka bantuan CLI
- **THEN** perintah audit memakai draft/review/export untuk format aktif
- **AND** tidak tersedia draft-v2/export-v2, --renderer-version, --contract-version atau --include-source sebagai compatibility alias

### Requirement: Operational assets are independent of planning documents
Schema, template/layout/font, kontrak dan panduan aktif SHALL tersedia di lokasi operasional khusus. Build, check, kit, tes workflow dan Actions MUST NOT memerlukan docs/ atau openspec/ sebagai input runtime, fingerprint atau sumber fakta.

#### Scenario: Historical docs are removed from a temporary copy
- **WHEN** salinan repo pengujian tidak menyertakan docs/ dan openspec/
- **THEN** build/check, pembentukan kit dan workflow fixture tetap berjalan
- **AND** entry point aktif serta provenance kurasi tidak menunjuk file wajib yang hilang

### Requirement: Portable audit kit restores only the active runtime
Kit SHALL menyediakan runtime, schema, aset dan panduan aktif yang lengkap secara transitif dan berhash. Bootstrap SHALL bekerja offline pada workspace kosong tanpa checkout atau runtime host. Kit MUST NOT menyertakan sumber video, hasil pilot atau runtime legacy.

#### Scenario: Kit runs in a fresh chat workspace
- **WHEN** kit diekstrak dan dipulihkan pada folder kosong dengan dependensi inti tersedia
- **THEN** workflow fixture aktif dapat mencapai draft/review/export tanpa mengakses repo asal atau jaringan bootstrap
- **AND** inventaris tidak berisi hasil edh001/edh058 atau modul versi lama

### Requirement: Active instructions are coherent and readable
Panduan/prompts/CLI/schema SHALL menyampaikan kebijakan aktif yang sama, dengan spasi normal dan pembagian tahap yang jelas. Instruksi angka wajib dari versi lama MUST NOT tersisa pada panduan aktif. Contoh sintetis MUST tetap dibedakan dari audit nyata.

#### Scenario: Auditor follows the authoring guide
- **WHEN** AI membaca authoring dan panduan kamera dalam kit yang sama
- **THEN** keduanya menerima angka kamera opsional, baseline 6 FPS dan review snapshot penuh
- **AND** tidak ada aturan kompatibilitas lama yang harus dipilih auditor

### Requirement: Cache and optional tooling remain bounded
Ekstraksi/cache/helper SHALL mempunyai batas sumber daya, fingerprint sumber/runtime/config dan pemulihan terbatas. Resume/cache MUST NOT melewati validasi atau deklarasi viewed. OpenCV/NumPy SHALL opsional; workflow inti MUST NOT memerlukan AI API tambahan.

#### Scenario: A matching session resumes
- **WHEN** prepare dilanjutkan pada sumber/cut yang sama dengan cache valid
- **THEN** pekerjaan mekanis yang tersedia dipakai ulang tanpa menimpa observasi
- **AND** frame belum dilihat tidak dinyatakan viewed

#### Scenario: Source or runtime changes
- **WHEN** cache/session tidak cocok dengan sumber atau runtime aktif
- **THEN** cache usang tidak dipakai sebagai data sah
- **AND** session lama ditolak atau pekerjaan mekanis yang diperlukan dibangun ulang sesuai aturan sumber

### Requirement: Cleanliness and efficiency are verified with equivalent content
Verifikasi SHALL mencakup dependensi bersih, schema/kit offline, pipeline normal/multi, helper opsional dan ukuran/waktu fixture setara. Pengurangan ukuran MUST NOT berasal dari penghilangan fakta atau pemindahan seluruh duplikasi ke manifest. Hasil benchmark MUST dibedakan dari durasi audit provider.

#### Scenario: Implementation verification is reported
- **WHEN** perubahan tooling dinyatakan selesai
- **THEN** laporan mencatat checks, ukuran JSON/kit, waktu tahap cold/warm serta batas lingkungan yang diuji
- **AND** tidak mengklaim pilot nyata selesai atau durasi chat tertentu dari benchmark fixture

### Requirement: User-controlled data and historical cleanup are preserved
Cutover SHALL mempertahankan MP4, arsip dan hasil pilot yang belum diminta dihapus. Pengguna SHALL tetap memilih pembersihan dokumen historis setelah implementasi. Riwayat tersebut MUST NOT dipakai untuk mengisi audit baru atau menjadi dependensi aktif.

#### Scenario: Runtime is consolidated while the library is empty
- **WHEN** dukungan lama dihapus dari tooling
- **THEN** sumber video dan hasil pembanding tetap utuh
- **AND** registry tetap kosong sampai ZIP audit baru yang final di-ingest
- **AND** laporan akhir menjelaskan lokasi panduan aktif yang perlu dipertahankan
