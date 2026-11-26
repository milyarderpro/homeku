# Tasks

## 1. Keputusan kamera dan pembanding pilot

- [x] 1.1 Susun ulang `audit/visual-audit.md` dan contoh pembeda di `audit/camera-cases.md`. Verifikasi urutan keputusan dari batas fase, jangkar dekat/jauh dan orientasi bidang, hingga estimasi tiap komponen dan profil laju. Cek bahwa baseline 6 FPS, native untuk sumber ≤6 FPS atau shot <1 detik, serta pendalaman terarah tetap tercantum.
- [x] 1.2 Selaraskan satu pemeriksaan akhir di `audit/authoring.md` dan prompt mulai/koreksi. Periksa bahwa auditor membandingkan notasi, observations, dan frame untuk fase yang terlewat, Orbit/Pan, dan arah yang salah. Jalankan `tests.test_camera_parser` serta `tests.test_audit_authoring` untuk memastikan notasi dan alur audit yang ada tetap bekerja.
- [x] 1.3 Buat pembanding rilis di `audit/pilots/camera-release-check.md` dan tautkan dari `audit/pilots/README.md`. Sertakan cara menilai `dreamshome01` Shot 01–05, pertanyaan spesifik `edh033` Shot 02 dan `edh056` Shot 01, format catatan perbandingan, serta prompt uji kamera yang dapat dipakai di kedua provider. Verifikasi dengan ZIP dan waktu sumber, lalu pastikan hasil acuan bernama berada di luar inventaris kit.

## 2. Acuan frame awal produksi

- [x] 2.1 Tambahkan `composition.production_start` opsional pada `schemas/audit.schema.json` dan `schemas/reference-reader.schema.json`. Hubungkan indeks ke `tools/homeku/derivations.py`, serta validasi scope frame dan viewed melalui `models.py`, `audit_quality.py`, dan `package_manifest.py` sesuai jalur preflight dan review. Uji pilihan yang valid, frame Start yang sama, indeks di luar shot atau di luar video, frame belum viewed, serta audit 3.0 tanpa field.
- [x] 2.2 Tambahkan bagian bersyarat `Production Start` di `tools/homeku/reporting.py` dan pointer sumber di `tools/homeku/generation.py`. Gunakan jalur reader `panel <id> F<indeks> --native` dari frame map. Uji laporan yang memakai PTS dari manifest, proyeksi dengan pointer yang dapat diikuti, ekstraksi frame dari MP4 cocok, dan laporan lama yang tetap identik. Pastikan scope frame dinilai juga saat review tanpa MP4.
- [x] 2.3 Perbarui `audit/json-guide.md`, `audit/authoring.md`, `audit/concept-workflow.md`, serta kontrak report, reader, dan package untuk menerangkan acuan opsional, fallback Start biasa, dan kasus reverse. Verifikasi dengan fixture yang menjalankan draft → review → export, termasuk pemeriksaan bahwa Start native, Overview, daftar JPEG, dan allowlist ZIP tetap sesuai; lihat satu contoh laporan yang menampilkan frame dan framing acuan.

## 3. Panduan penyerahan dan distribusi

- [x] 3.1 Perbarui `incoming/README.md` dan `video/README.md` agar mengarah ke kontrak 3.0, mendeskripsikan inventaris ZIP dan MP4 terpisah, serta mencatat ingest lokal, revisi, dan trigger GitHub default branch. Cek tautan lokal dan cocokkan instruksi dengan CLI dan workflow yang ada.
- [x] 3.2 Bangun ulang `audit/homeku-audit-kit.zip` dan keluaran pustaka dengan generator. Jalankan bootstrap dari folder kosong, periksa bahwa schema dan panduan yang diperbarui tersedia, dan cek bahwa pembanding `audit/pilots/` tidak masuk kit.

## 4. Verifikasi integrasi

- [x] 4.1 Verifikasi `dreamshome01` pada ruang kerja terisolasi. Cocokkan perbedaan Start native F184 dan pilihan produksi F194 dengan MP4. Uji bahwa foto awal produksi bisa diekstrak untuk prompt sementara kolase dan batas sumber tetap memakai indeks semula. Tinjau pembanding kamera Shot 01–05 serta interval terarah `edh033` Shot 02 dan `edh056` Shot 01. Catat keputusan yang didukung frame dan ketidakpastian yang tersisa di pembanding rilis.
- [x] 4.2 Validasi enam ZIP pilot asli dan referensi aktif tanpa ingest. Cocokkan hash ZIP sebelum dan sesudah. Jalankan `python -m unittest discover -s tests -t . -v`, `python tools/library.py check`, `python tools/build_audit_kit.py --check`, dan `git diff --check`. Laporkan status serta tautan ke kit dan pembanding.

## Workflow follow-up

- Sebelum menyatakan siap rilis, pakai kit yang dibangun ulang pada sesi baru GPT dan Gemini untuk bagian kamera `dreamshome01`. Bandingkan hasil dengan rubrik setelah kedua sesi selesai. Periksa fase Shot 01 dan 03, komponen simultan Shot 02, hasil Shot 04–05, serta pilihan frame produksi pada transisi. Catat perbedaan arah, skala, dan waktu analisis. Gunakan cek terarah `edh033` dan `edh056` sebagai pembanding tambahan.
