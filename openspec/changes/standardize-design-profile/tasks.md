# Tasks

## 1. Sumber profil dan validasi

- [x] 1.1 Tambahkan bentuk klaim `design.house_type` dan entri `design.palette` di `schemas/audit.schema.json`. Validasi tipe label terbuka, status `unknown`, HEX, jumlah warna, dan palet tunggal di `tools/homeku/models.py` serta jalur preflight yang relevan. Uji di `tests/test_schemas.py`, `tests/test_models.py`, dan `tests/test_audit_preflight.py` dengan `Tower House`, tipe belum pasti, HEX salah, serta palet ganda.
- [x] 1.2 Hubungkan tipe dan bukti setiap warna ke `tools/homeku/derivations.py` dan validasi viewed yang sudah ada. Uji bahwa bukti yang valid masuk frame map, indeks di luar sumber ditolak, dan warna dari frame yang belum dideklarasikan viewed gagal validasi.
- [x] 1.3 Perbarui `audit/template-audit.json`, panduan `audit/json-guide.md`, dan kontrak sumber di `audit/contracts/package.md`. Pastikan `prepare` menyediakan field profil, placeholder belum dapat diekspor, dan paket awal 3.0 masih lulus validasi schema.

## 2. Template laporan dan kompatibilitas snapshot

- [x] 2.1 Tambahkan `tools/assets/templates/analysis-profile.md` dan render Profil Desain baku di `tools/homeku/reporting.py` serta `tools/homeku/report_validation.py`. Uji posisi tabel palet, pengurutan baris, escaping Markdown, enam bagian utama, dan struktur Detail Shot. Cocokkan dokumentasi `audit/contracts/report.md` dengan tampilan.
- [x] 2.2 Hubungkan pemilihan template dan fingerprint pada `tools/homeku/render_assets.py`, `exporter.py`, dan `validation.py`. Uji bahwa draft memakai template baku, fingerprint yang tidak dikenal atau tidak cocok ditolak, dan laporan 3.0 awal masih dirender byte-identik dari data aslinya.
- [x] 2.3 Validasi folder `references/edh001` revisi 1 dan ZIP pilot 3.0 yang tersedia dengan template awal. Bandingkan hash sebelum dan sesudah pemeriksaan serta pertahankan contoh golden untuk menutup regresi kompatibilitas.

## 3. Pencarian dan pembacaan AI

- [x] 3.1 Tambahkan alias tipe rumah di `data/taxonomy.json` dan facet `house-type` di `tools/homeku/generation.py`. Daftarkan aset template profil sebagai input fingerprint generator. Uji label asli, alias `vila`, label baru tanpa entri taksonomi, dan pointer yang dapat diresolusikan.
- [x] 3.2 Tambahkan `--house-type` di `tools/library.py` dan filter terkait di `tools/homeku/reader.py`. Uji opsi itu bersama gaya, skala, area, dan `--observed-only`. Pastikan hasil tetap terbatas pada referensi aktif.
- [x] 3.3 Verifikasi `read --part identity` mengembalikan tipe, susunan ruang, pencahayaan, atmosfer, palet, dan bukti dari proyeksi. Uji bahwa struktur palet lengkap bisa dibaca melalui identitas tanpa menyalinnya ke indeks pencarian. Dokumentasikan perintah dan sumber data di `README.md`, `audit/contracts/reader.md`, dan `audit/concept-workflow.md`.

## 4. Kit dan alur audit

- [x] 4.1 Selaraskan `audit/visual-audit.md`, `audit/authoring.md`, `audit/README.md`, `audit/vocabulary.md`, dan prompt mulai serta koreksi. Sertakan delapan tipe awal, contoh label baru, penilaian dengan `uncertain`, dan cara memilih warna. Perbarui contoh sintetis normal dan multi-area. Periksa bahwa contoh menunjukkan pencahayaan dan atmosfer secara terpisah.
- [x] 4.2 Daftarkan aset baru di `tools/build_audit_kit.py` dan buat ulang `audit/homeku-audit-kit.zip`. Uji bootstrap offline di workspace kosong serta alur prepare, check-input, draft, review, dan ekspor tanpa MP4. Pastikan prompt memberikan tautan ZIP langsung setelah review teknis.
- [x] 4.3 Bangun ulang keluaran pustaka melalui generator dan jalankan cek sebelum menyiapkan revisi produksi. Pastikan `edh001-r0001` masih aktif dan proses build tidak mengubah isi referensi yang diterima.

## 5. Revisi edh001 dan kesiapan rilis

- [x] 5.1 Salin `edh001-r0001` ke workspace, periksa frame sumber yang relevan, lalu isi tipe rumah, atmosfer, dan palet HEX. Gunakan data susunan ruang, material, pencahayaan, dan lingkungan yang tersedia. Cocokkan perubahan dengan rencana profil dan pastikan shot, cut, kamera, tempo, serta pilihan panel sama dengan revisi induk.
- [x] 5.2 Buat `edh001-r0002.zip` dengan `supersedes` dari registry aktif. Luluskan validasi terhadap `video/edh001.mp4`, lalu tampilkan laporan, media, dan tautan ZIP setelah review teknis. Cocokkan inventaris ZIP dan hash snapshot. Pastikan registry masih menunjuk `r0001` saat ZIP ditawarkan.
- [x] 5.3 Setelah pengguna memilih ZIP `r0002`, ingest paket tersebut dan periksa registry, laporan, hasil pencarian tipe rumah, proyeksi identitas, serta bukti palet. Pastikan `edh001` tetap satu entri aktif dan menunjuk revisi 2.
- [x] 5.4 Jalankan `python -m unittest discover -s tests -t . -v`, `python tools/library.py check`, dan `python tools/build_audit_kit.py --check`. Nyatakan siap rilis ketika pemeriksaan lulus dan seluruh referensi aktif memakai Profil Desain baku. Bukti pemeriksaan paket awal dan paket baru dilaporkan terpisah.
