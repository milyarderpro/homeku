# Tasks

## 1. Standar nama area dan caption

- [x] 1.1 Perbarui `audit/vocabulary.md`, `audit/json-guide.md`, `audit/visual-audit.md`, `audit/authoring.md`, `audit/prompts/01-audit.md`, dan `audit/prompts/02-correct.md`. Tetapkan label area dan momen dalam bahasa Inggris dengan Title Case, pemakaian `&` dan `/`, fungsi ruang eksplisit, istilah teknis Inggris, dan narasi Indonesia. Periksa contoh aturan pada audit normal dan multi-area.
- [x] 1.2 Perbarui `data/taxonomy.json` dengan padanan yang setara melalui normalisasi yang sudah ada. Uji di `tests/test_generation.py` atau `tests/test_reader.py` bahwa `Living Room`, `Dining Area`, `Kitchen`, dan `ruang makan` menemukan area open-plan saat fungsi itu tercatat. Pastikan fungsi `Bathroom` dan `Laundry` tetap bisa dicari dan label sumber tetap utuh.
- [x] 1.3 Periksa pemakaian label bersama di `tools/homeku/render_assets.py`, `tools/homeku/reporting.py`, dan `tools/homeku/media.py`. Reuse jalur judul dan caption dari audit. Perbarui `audit/contracts/report.md` bila kontrak tampilan perlu dicatat. Uji judul multi-area, label frame wide terpilih, label momen spesifik, dan fallback `Moment N` di `tests/test_reporting.py` dan `tests/test_media.py`.

## 2. Pilihan layout dan geometri media

- [x] 2.1 Tambahkan `tools/assets/layouts/media-aligned.json`. Hubungkan pemilihan layout berdasarkan `manifest.render.layout_sha256` di `tools/homeku/render_assets.py`, `tools/homeku/exporter.py`, dan `tools/homeku/validation.py`. Uji bahwa kedua hash layout diterima dengan template laporan yang sesuai dan hash asing ditolak di `tests/test_render_assets.py` serta `tests/test_package.py`. Catat pemilihan fingerprint di `audit/contracts/package.md`.
- [x] 2.2 Implementasikan geometri layout baru di `tools/homeku/media.py` dengan lebar blok acuan tiga panel, perataan kiri, pembagian baris seimbang, dan foto berproporsi asli. Setel default lima kolom pada jalur draft di `tools/audit.py` dan konfigurasi render terkait. Uji shot normal tiga panel, multi-area lima panel sebaris, enam panel 3+3, tujuh panel 4+3, dan batas `--columns` eksplisit. Sertakan kasus layout asal empat kolom.
- [x] 2.3 Ratakan judul, foto, dan `Camera:` antarshot. Tempatkan waktu shot di kanan dan waktu panel lebih kecil di bawah foto. Uji judul atau caption panjang, keselarasan blok, dan lebar Overview satu baris di `tests/test_media.py`. Catat susunan dan opsi kolom di `audit/README.md`.
- [x] 2.4 Gunakan hasil perencanaan geometri yang sama untuk render, validasi, koordinat panel, dan cache. Periksa `tools/homeku/media_incremental.py`, `tools/homeku/validation.py`, dan `tools/homeku/reader.py`. Uji crop `panel` dan `shot-image --from-storyboard` melalui JPEG dan bbox pada skala 1 dan pecahan. Verifikasi indeks, waktu, batas piksel dan JPEG, serta perubahan kunci cache saat layout atau caption berubah.

## 3. Kit audit dan kompatibilitas pustaka

- [x] 3.1 Daftarkan kedua aset layout di `tools/build_audit_kit.py` dan masukkan keduanya ke fingerprint generator di `tools/homeku/generation.py`. Bangun ulang kit dan keluaran pustaka dengan `python tools/build_audit_kit.py` serta `python tools/library.py build`. Ekstrak kit ke workspace kosong dan verifikasi bootstrap memulihkan kedua layout bersama panduan yang diperbarui.
- [x] 3.2 Validasi referensi aktif melalui `python tools/library.py check` dan kedua ZIP pilot asli melalui `python tools/library.py validate` dengan MP4 kanonis tersedia. Pastikan paket layout awal tetap lolos dengan geometri asal dan hash ZIP sumber tetap sama setelah validasi.

## 4. Preview pilot dan verifikasi integrasi

- [x] 4.1 Render preview dari salinan `docs/runpilot/pilot/edh033-r0002.zip` dan MP4 kanonis. Buka Storyboard, Overview, kolase, dan laporan. Periksa judul `Exterior`, `Open-Plan Living / Sleeping Loft`, `Bathroom & Laundry`, dan `Exterior`. Periksa frame tengah sebelum memberi nama momen dan pastikan indeks serta isi audit di luar label tetap sama.
- [x] 4.2 Render preview dari salinan `docs/runpilot/pilot/edh056-r0001.zip` dan MP4 kanonis. Periksa bahwa lima frame Shot 01 `0, 70, 190, 220, 379` tampil dalam satu baris dengan caption `Start`, `Facade Reveal`, `Doorway`, `Living & Kitchen`, dan `End`. Ukur perataan terhadap tiga shot berikutnya dan lihat keterbacaan pada Storyboard. Simpan kedua preview di workspace di luar jalur ingest dan cocokkan hash sumber sebelum dan sesudah.
- [x] 4.3 Jalankan `python -m unittest discover -s tests -t . -v`, `python tools/library.py check`, `python tools/build_audit_kit.py --check`, dan `git diff --check`. Laporkan hasil pemeriksaan serta tautan kedua preview dan kit audit yang siap dipakai.
