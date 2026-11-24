# Spec Delta

## Purpose

Menyediakan pustaka yang dapat berkembang menjadi ratusan referensi, dengan ingest final yang konsisten serta pencarian dan pembacaan AI berdasarkan fakta eksplisit sumber.

## ADDED Requirements

### Requirement: Only registered references participate in discovery
Discovery, generator dan knowledge SHALL memakai hanya referensi aktif dalam data/registry.json. Arsip, pilot/result, kandidat, cache dan fixture MUST NOT menjadi sumber implisit; fixture SHALL ditolak untuk ingest produksi.

#### Scenario: Archive and candidate data exist
- **WHEN** repo berisi arsip lama, hasil edh058 dan kandidat baru yang belum di-ingest
- **THEN** build hanya menerbitkan ID dalam registry
- **AND** pustaka kosong tetap menghasilkan nol referensi serta nol shot

### Requirement: Final ZIP ingest is explicit and revision aware
Ingest SHALL menerima ZIP final yang valid dengan MP4 kanonis terpisah/hash cocok. Referensi baru SHALL mulai revision 1/supersedes null; revisi berikutnya SHALL cocok dengan sumber aktif yang diganti. Ingest MUST NOT meminta review isi tambahan atau mengubah fakta sumber.

#### Scenario: New edh001 audit arrives after reset
- **WHEN** ZIP final edh001 r0001 format aktif dimasukkan dan ingest dijalankan
- **THEN** paket dapat menjadi referensi baru dengan supersedes null
- **AND** hasil kamera/persetujuan lama tidak dipakai sebagai audit baru

#### Scenario: Conflicting revision is submitted
- **WHEN** revisi atau supersedes tidak cocok dengan referensi aktif
- **THEN** ingest menolak paket tanpa mengganti referensi dan keluaran yang telah sah

### Requirement: Derived outputs are deterministic and replace stale data
Build SHALL menghasilkan catalogs, knowledge, projections, indeks dan dependencies dari sumber/tooling resmi. Replay identik SHALL unchanged; revisi/penghapusan sumber SHALL membuang keluaran usang. Build penuh dan incremental SHALL setara tanpa sintesis fakta dari prosa.

#### Scenario: A room configuration changes in a new revision
- **WHEN** revisi final mengganti fakta konfigurasi kitchen
- **THEN** halaman/index/proyeksi baru menunjuk sumber revisi tersebut
- **AND** variasi lama yang tidak lagi bersumber tidak tersisa dalam keluaran aktif

#### Scenario: Final package is replayed
- **WHEN** ZIP yang telah berhasil di-ingest diproses lagi tanpa perubahan
- **THEN** hasil menyatakan unchanged dan byte keluaran tetap sama

### Requirement: Selective search retains explicit design and camera facets
Search SHALL mendukung pemilihan berdasarkan gaya utama/pengaruh/interior, skala, area, konfigurasi, rute, gerak/qualifier dan tempo yang eksplisit. Indeks SHALL ringkas dengan pointer untuk rincian; label baru/negasi/uncertainty MUST tetap dapat dibaca tanpa inferensi prosa atau alias rekaan.

#### Scenario: User searches for a compact cottage kitchen
- **WHEN** AI mencari gaya, skala dan area yang cocok
- **THEN** hasil memuat referensi/shot relevan beserta pointer profil dan fakta desain
- **AND** pencarian tidak perlu memuat seluruh MD, log pemeriksaan atau semua gambar

#### Scenario: A new structural label appears
- **WHEN** fakta memakai label baru dengan facet_roles eksplisit
- **THEN** label asli dan provenance tetap tersedia
- **AND** generator tidak menebak pemetaan semantik dari paragraf

### Requirement: Reader exposes complete source provenance
Reader SHALL menyediakan profil, shot, area, fakta dan kamera terpilih dengan pointer yang dapat diresolusikan ke audit/manifest asal. Turunan seperti camera summary/pattern SHALL ditandai beserta input sumbernya. Confidence kosong MUST tetap tidak dinilai.

#### Scenario: AI reads a multi-area camera timeline
- **WHEN** reader diminta menampilkan satu shot multi area
- **THEN** hasil mempertahankan scope area, route, visibility, fase dan tempo yang berbeda
- **AND** setiap fakta/turunan menunjuk lokasi sumber yang benar

### Requirement: Stored media access does not require the source video
Reader SHALL dapat mengambil panel, kolase dan blok Storyboard tersimpan tanpa MP4. Permintaan native SHALL secara eksplisit memerlukan sumber. Bbox dan selection provenance SHALL menjaga perbedaan Camera Start dengan Overview akhir OUT.

#### Scenario: Source video is temporarily unavailable for reading
- **WHEN** AI meminta panel tersimpan atau kolase dari paket valid
- **THEN** reader mengambil gambar dari lokasi media/bbox terdaftar tanpa decode MP4
- **AND** permintaan native mengembalikan kebutuhan sumber secara jelas bila MP4 tidak tersedia

### Requirement: Publication preserves atomic state and canonical sources
Publikasi SHALL memakai lock, staging dan pemulihan untuk mencegah state referensi/turunan parsial. Paket gagal MUST NOT merusak paket valid lain; MP4 kanonis MUST NOT ditimpa dengan sumber berbeda secara diam-diam.

#### Scenario: Publication fails while applying a batch
- **WHEN** proses pemasangan keluaran gagal atau terputus
- **THEN** rollback/recovery memulihkan state konsisten
- **AND** importer bersamaan tidak kehilangan referensi valid

### Requirement: Capacity scales without promoting fixtures into knowledge
Pustaka SHALL mendukung sekurangnya 300 model sintetis pada pengujian terisolasi dengan pagination dan pembacaan selektif. Prinsip desain terkurasi SHALL tetap terpisah dari fakta hasil audit, tanpa mengharuskan tes produksi konsep/gambar.

#### Scenario: Capacity test builds a large isolated library
- **WHEN** pengujian membuat 300 model format aktif pada root fixture
- **THEN** indeks/pointer/pagination dan build penuh/incremental tetap konsisten
- **AND** registry produksi tidak berubah serta hasil tes tidak diklaim sebagai pilot nyata
