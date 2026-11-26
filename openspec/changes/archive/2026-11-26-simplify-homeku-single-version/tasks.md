# Tasks

Progres ditandai pada checklist berikut. Jalankan berurutan sesuai dependensi; detail pendekatan ada di design.md dan perilaku wajib pada lima spec. Port tes/dokumentasi bersama bagian yang diubah. Pilot nyata dan archive bukan syarat tersembunyi untuk menyelesaikan implementasi tooling.

## 1. Lindungi state dan simpan baseline

- [x] 1.1 Periksa registry, ledger dan incoming sebelum cutover; verifikasi tetap kosong dan jangan menghapus/mengonversi data baru jika state berubah.
- [x] 1.2 Catat hash MP4, arsip dan hasil pilot yang dipertahankan serta ukuran JSON/kit saat ini; verifikasi catatan membedakan baseline fixture dari audit nyata.
- [x] 1.3 Simpan acuan laporan/media terbaru normal dan multi area dengan nama netral untuk porting; verifikasi enam bagian MD, N+2 JPEG dan caption sesuai tampilan yang telah disetujui.
- [x] 1.4 Buat matriks kemampuan→field sumber/turunan/workspace pada kontrak aktif, mencakup seluruh aspek DNA lama, fakta, relasi, framing dan kamera; verifikasi tidak ada informasi produk yang hilang atau dua pemilik fakta yang sama.

## 2. Kontrak dan contoh sumber ringkas

- [x] 2.1 Tambahkan lima schema offline dalam schemas/ dan konstanta format 3.0 tunggal; verifikasi schema valid secara lokal tanpa fetch jaringan serta unknown/format lama ditolak.
- [x] 2.2 Definisikan design/styles/size/features dan fakta nested per kategori dengan state/evidence eksplisit; tambahkan tes schema untuk luas wajib, gaya diskret, nilai negatif/unknown dan confidence tidak dinilai.
- [x] 2.3 Definisikan shots/areas/routes/relations, kamera/fase/tempo serta pilihan frame tanpa field turunan berulang; verifikasi contoh multi area mendukung overlap, reentry dan area hanya terlihat.
- [x] 2.4 Ganti template-audit.json dan contoh normal/multi menjadi sumber ringkas lengkap sintetis; verifikasi tidak ada profile paralel, components_parsed, summary atau fact_coverage, tanpa memangkas isi fixture yang setara.
- [x] 2.5 Tulis audit/contracts/{package,report,reader}.md dan perbarui json-guide/template-audit-info untuk kontrak baru; verifikasi semua field wajib/opsional dan pemilik metadata dijelaskan konsisten dengan schema.

## 3. Parser dan utility tanpa legacy

- [x] 3.1 Jadikan camera_notation.py parser mandiri dan pindahkan konstanta umum yang dibutuhkan dari markdown.py; verifikasi seluruh studi kasus pengguna, angka tunggal/rentang/tanpa angka, koma desimal, x/×, qualifiers/toward dan easing pada tes parser.
- [x] 3.2 Buat render_assets.py untuk font/path/wrap/angka yang dipakai bersama; verifikasi import media/reporting yang dipindahkan tidak membutuhkan modul media/reporting lama.
- [x] 3.3 Buat derivations.py untuk summary/pattern, ID selection, scope dan tempo overlap dari sumber eksplisit; verifikasi hasil deterministik, pointer asal tersedia dan audit.json tidak ditulis ulang dengan field turunan.
- [x] 3.4 Sesuaikan camera_pattern.py dan dokumentasi camera-cases/visual-audit untuk depth eksplisit; verifikasi Zoom tidak mengisi IN, Dolly kontradiktif ditolak dan semua moderate tetap sah.

## 4. Model, authoring dan pemeriksaan awal

- [x] 4.1 Port models.py/audit_quality.py ke sumber ringkas dan evidence indeks frame; verifikasi validitas scope shot/fase/area, state/negasi, bukti temporal minimal dan override komponen dengan tes positif/negatif.
- [x] 4.2 Port audit_session.py/prepare ke format aktif, batas native dan midpoint presisi; verifikasi 6 FPS, ≤6 FPS, VFR, shot pendek, stream yang benar, cut tidak terlintasi dan frame belum otomatis viewed.
- [x] 4.3 Implementasikan update-shot berbasis patch file terstruktur pada authoring.py; verifikasi update atomik, hanya shot yang dituju berubah dan metadata terkunci/field turunan ditolak.
- [x] 4.4 Port complete/mark-viewed/resume tanpa mengembalikan struktur panjang; verifikasi observasi tidak tertimpa, source/cut/session lama ditolak dan complete tidak mengarang state/angka/tempo.
- [x] 4.5 Port preflight.py beserta schema audit-info dan error pointer; verifikasi input invalid gagal sebelum JPEG, kesalahan independen terlihat dan konteks probe/hash/PTS bisa dipakai draft tanpa pengulangan dalam satu call.
- [x] 4.6 Perbarui authoring.md serta tes authoring/preflight/quality pada tahap ini; verifikasi contoh perintah sesuai helper aktif dan tidak ada instruksi angka wajib atau viewed otomatis.

## 5. Laporan, media dan paket final

- [x] 5.1 Satukan reporting.py/report_validation.py dan tools/assets/templates/analysis.md untuk sumber baru; verifikasi golden normal/multi tepat enam bagian, A/B/C, seluruh narasi dan notasi yang sama dengan fase.
- [x] 5.2 Satukan media.py dan tools/assets/layouts/media.json, mempertahankan aset font/lisensi; verifikasi N+2 JPEG, panel normal tiga, multi dinamis, Overview satu baris dan Storyboard vertikal.
- [x] 5.3 Bentuk manifest dengan pemetaan frame→PTS terbatas, selection ID, bbox/media/hash dan provenance pemeriksaan; verifikasi native evidence di luar kolase dan crop panel/blok benar tanpa salinan seluruh frame/tabel PTS.
- [x] 5.4 Port media_incremental.py/video_cache.py ke utility aktif; verifikasi cache/subset/full byte-identik untuk konfigurasi sama, batas alokasi/quota, partial cache, batch 32 dan bounded retry/error fail-fast.
- [x] 5.5 Port exporter.py/validation.py ke draft/review/export JSON tunggal; verifikasi snapshot mencakup semua file, receipt di luar kandidat, mutasi pascareview ditolak dan export tidak merender ulang.
- [x] 5.6 Terapkan ZIP allowlist ketat tanpa video/file kerja; verifikasi ekstensi/casing/path bersarang, traversal, duplicate/symlink, hash sumber/media dan kandidat tidak terkelola ditolak.
- [x] 5.7 Perbarui kontrak report/package dan tes media/report/paket bersama porting; inspeksi preview normal/multi secara visual untuk judul, waktu header serta caption bawah label tebal dengan waktu lebih kecil.

## 6. Generator, discovery dan ingest

- [x] 6.1 Port generation.py untuk styles/size/features dan fakta nested dengan facet_roles eksplisit; verifikasi label asli/negasi/status/note dipertahankan tanpa inference prosa atau fallback fact-facets lama.
- [x] 6.2 Bentuk schema proyeksi/indeks dan provenance pointer baru; verifikasi seluruh kategori fakta, profil, fase, tempo, relasi serta turunan merujuk field audit/manifest yang dapat diresolusikan.
- [x] 6.3 Port reader.py/library.py untuk filter gaya utama/pengaruh/interior, skala, area, konfigurasi, route, gerak/qualifier dan tempo; verifikasi partial read/search tidak memuat seluruh MD/media/log.
- [x] 6.4 Pisahkan baca paket/media tersimpan dari verifikasi MP4; verifikasi read/panel/shot-image/blok Storyboard tetap berhasil tanpa MP4, sedangkan --native meminta sumber eksplisit.
- [x] 6.5 Port engine.py/registry/fingerprint ke format tunggal sambil mempertahankan storage primitives; verifikasi root kosong, revisi/supersedes, duplicate, replay unchanged dan stale-output removal.
- [x] 6.6 Port tes library/reader/Actions yang relevan dan kontrak reader pada tahap ini; verifikasi lock/concurrency/rollback/recovery, batch sebagian gagal, kanonis tidak tertimpa dan publikasi Git lokal tetap benar.

## 7. Ringkasan helper kamera dan batas pekerjaan

- [x] 7.1 Tambahkan matriks transform/ringkasan makro di motion_analysis.py; verifikasi transform sintetis skala+rotasi+translasi dikomposisikan benar dan displacement tidak sekadar penjumlahan mentah.
- [x] 7.2 Implementasikan coverage, gap dan tren PTS awal–tengah–akhir; verifikasi tracking gagal memutus rantai dan total seluruh shot null/tidak tersedia bila tidak dapat dihitung.
- [x] 7.3 Tambahkan output ringkas default dan --details serta cache key baru; verifikasi batas frame/resolusi/quota, cache reuse dan tidak ada mutasi audit/viewed atau statistik dalam ZIP/knowledge.
- [x] 7.4 Perbarui panduan helper serta tests/test_motion_analysis.py; verifikasi tes nyata dengan OpenCV/NumPy dan fallback tanpa dependensi berjalan, dengan skip/lingkungan yang tidak tersedia dicatat jujur.

## 8. CLI, panduan, kit dan CI mandiri

- [x] 8.1 Satukan tools/audit.py menjadi CLI format aktif termasuk update-shot; verifikasi --help dan workflow normal/multi tidak mempunyai jalur MD, draft-v2/export-v2 atau flag pemilihan versi/include-source.
- [x] 8.2 Satukan aturan pada README/AGENTS/references serta audit/README, visual-audit, authoring, json-guide, vocabulary dan tiga prompt; verifikasi spasi normal, angka opsional, baseline 6 FPS dan persetujuan keseluruhan konsisten.
- [x] 8.3 Pindahkan isi aktif protocol/rubric/providers/calibration ke panduan yang tepat serta alur konsep/capability ke audit/concept-workflow.md; verifikasi isi operasional/prinsip kurasi tetap tersedia dan provenance tidak memerlukan docs.
- [x] 8.4 Ubah tools/build_audit_kit.py menjadi inventaris eksplisit runtime/schema/aset/panduan aktif dengan empat file input; verifikasi bootstrap deterministik/offline tanpa hasil pilot, video atau resource legacy.
- [x] 8.5 Perbarui trigger .github/workflows/library-ci.yml/library-ingest.yml, root fixture Actions dan kebutuhan dependensi; verifikasi schemas/tools/assets memicu checks dan pengujian helper tetap opsional untuk core.
- [x] 8.6 Tambahkan tests/test_repository_integrity.py serta tes kit standalone; verifikasi workspace kosong tanpa checkout/PYTHONPATH repo dan salinan tanpa docs/openspec dapat menjalankan workflow fixture, build/check dan pembentukan kit.

## 9. Hapus legacy dan konsolidasikan fixture

- [x] 9.1 Setelah semua pemakai aktif dipindahkan, hapus versions.py, markdown.py, media_v*.py dan reporting_v*.py; verifikasi graph impor tidak memiliki referensi ke modul terhapus atau import cycle.
- [x] 9.2 Hapus schema/kontrak docs/contracts, template/layout versi lama, audit/template-analysis.md dan sources/fact-facets.json; verifikasi hanya schema/aset netral yang dibaca kode/kit/fingerprint/Actions.
- [x] 9.3 Hapus panduan duplikat yang sudah digabung dan perbarui seluruh entry point aktif; verifikasi tidak ada instruksi kompatibilitas/angka wajib lama pada runtime kit dan tidak menghapus dokumen historis pilihan pengguna.
- [x] 9.4 Konsolidasikan tests/fixtures/factory.py, make_test_packages.py dan tes menurut fungsi; hapus parameter pembuat multi-versi, compatibility-only tests, golden lama dan ZIP fixture berisi video setelah skenario produk penting diport, lalu verifikasi fixture aktif tetap terisolasi.
- [x] 9.5 Verifikasi penolakan paket/session lama dan unknown tanpa adapter; pastikan hash MP4/arsip/hasil pilot tetap sama serta tidak ada salinan runtime lama baru di archive.

## 10. Integrasi, pengukuran dan serah terima

- [x] 10.1 Jalankan workflow fixture end-to-end normal/multi dari source→prepare/viewed/complete/preflight→draft/review→export/ingest/replay; verifikasi kesetaraan byte, pointer/media, format MD dan tidak ada review isi kedua.
- [x] 10.2 Jalankan kapasitas 300 model sintetis format aktif pada root sementara; verifikasi pagination, selective read/search, full/incremental setara dan registry produksi tetap kosong.
- [x] 10.3 Perbarui benchmark_audit.py dan ukur fixture dengan informasi setara: JSON pretty/compact, total audit+manifest/paket, kit/resource, prepare cold/resume, complete/preflight, draft cold/warm/koreksi dan helper off/on; verifikasi hasil tidak bergantung pemangkasan fakta atau dianggap durasi provider.
- [x] 10.4 Jalankan python -m unittest discover -s tests -t . -v, python tools/library.py build, python tools/library.py check, python tools/build_audit_kit.py, python tools/build_audit_kit.py --check dan git diff --check; verifikasi semua checks final berhasil dan hanya keluaran generator yang diregenerasi.
- [x] 10.5 Tulis docs/implementation-verification-single-version.md dengan hasil nyata, versi lingkungan, preview/benchmark, keterbatasan dan daftar dokumen aktif/historis; verifikasi catatan ini tidak menjadi input runtime atau klaim pilot selesai.
- [x] 10.6 Perbarui audit/pilots/README.md untuk tujuh pilot dan panduan kit final; verifikasi edh001 mulai r0001/supersedes null, hasil lama tidak dikonversi dan status tooling/hasil/approval/export/ingest dibedakan.

## Workflow follow-up

- Tinjau hasil implementasi dan catatan verifikasi; pengguna kemudian dapat memilih penghapusan dokumen historis tanpa merusak panduan/aset aktif.
- Jalankan audit nyata edh001, edh058, edh013, edh033, edh049, edh056 dan dreamshome01 melalui chat baru dengan kit final bila diminta. Tinjau keseluruhan hasil sebelum ekspor dan ingest; jangan menandai pilot selesai dari fixture.
- Sinkronisasi main spec dan archive change hanya melalui workflow OpenSpec yang diminta setelah implementasi selesai; jangan mengarsipkan pada tahap proposal.
