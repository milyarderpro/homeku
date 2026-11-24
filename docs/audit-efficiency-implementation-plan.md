# Plan implementasi audit efisien dengan hasil tetap lengkap

> Status setelah reset 24 November 2026: data audit edh001 telah dihapus atas permintaan pengguna. Catatan edh001 di dokumen ini bersifat historis, bukan referensi aktif atau persetujuan audit baru.

Status: **tooling tahap1–7 dan pengujian/benchmark tahap8 selesai23November2026; pilot2.4 provider siap dijalankan pengguna, belum dijalankan**. Disusun 23 November 2026 sesudah evaluasi pilot edh058 sumber2.3 dan persetujuan pengguna atas estimasi visual berbasis asumsi yang wajar. Melanjutkan audit-method-6fps-implementation-plan.md; temuan run2.3 memperbarui status pilot, bukan mengubah kontrak lama.

## 1. Tujuan dan batas pekerjaan

Mengurangi waktu pengisian data teknis, kesalahan yang berulang, sampling ulang dan render sia-sia. Pengamatan desain/kamera tetap lengkap; AI memperoleh pengetahuan yang sama kayanya dari pustaka.

- audit.json tetap satu sumber isi audit; analysis.md hanya laporan manusia hasil renderer, manifest metadata teknis.
- Nama gaya English, uraian Indonesia; identitas, estimasi ukuran/luas, arsitektur, furnitur/properti, lingkungan, komposisi, Camera Start, gerakan/fase/tempo serta DNA perjalanan tetap lengkap.
- analysis.md wajib mengikuti enam bagian dan struktur A/B/C yang disetujui. Tidak menambahkan tabel pembuktian, asumsi, performa atau log ke MD.
- Media tetap kolase per take kontinu, Overview wide seluruh area satu baris, Storyboard vertikal; normal3panel, multi area dinamis. Layout/font/caption tidak didesain ulang.
- Baseline6FPS tetap. Sumber≤6FPS dan shot<1detik native; pendalaman10FPS/native sesuai pertanyaan.
- ZIP final satu paket tanpa MP4, frame kerja, cache, telemetry atau receipt. Pengguna meninjau di chat sebelum download; ingest tanpa review isi kedua.
- Tidak mengurangi detail, membuat frame viewed palsu, mengarang fakta atau menghentikan audit yang belum cukup demi mengejar waktu.
- Produksi/plugin/masterprompt bekerja/, arsip dan referensi aktif tidak menjadi objek perubahan isi.

## 2. Temuan dasar yang benar-benar tersedia

Kedua paket terbaru lulus validasi sumber2.3/report2.2.2, MD identik renderer dan semua8JPEG identik ketika dibuat ulang pada pemeriksaan terakhir. Pemeriksaan visual tambahan hanya12frame awal/akhir, bukan audit ulang seluruh video.

| Hasil di audit/result/<provider>/edh058-r0001.zip | SHA-256 | Frame unik tercatat viewed | Fakta |
| --- | --- | --- | --- |
| gemini | 51962d120cc63600d0e5ba99403021c66c6ed85aac82221ab4e67c5e0c2e1556 | 145 | 47 |
| gpt | 20a80cbc48335ca035b693c30aabd7c3b75f341c47b913a2dd42f20a93cb1229 | 299 | 68 |

- Laporan Gemini: penulisan/pembacaan panduan sekitar8menit26detik;8kegagalan validasi sebelum percobaan ke9 lulus; baseline diulang3kali. Analisis kamera/piksel sekitar1menit40detik. Durasi berasal dari laporan provider; log eksekusi mentah belum tersedia.
- Laporan GPT dan manifest: baseline6FPS lalu10FPS seluruh6shot, ditambah native midpoint;299frame unik. SIFT/RANSAC dilaporkan sebagai pekerjaan tambahan, bukan kewajiban kit.
- Penyebab berulang: waktu PTS dibulatkan manual, midpoint salah, metadata komponen ditulis ulang, relasi area/shot tertukar, mode native salah, selected/viewed tidak sesuai.
- Kode draft memang membuat JPEG sebelum memvalidasi audit-info/manifest lengkap. Validator schema hanya mengembalikan kesalahan pertama.
- Pengukuran lokal terakhir: render8JPEG sekitar18detik,24pemanggilan ekstraksi untuk18frame unik. Ini biaya lokal, bukan durasi render di akun provider.
- GPT menghilangkan sudut pada4komponen Pan dengan alasan umum yang sama. Pengguna menghendaki estimasi visual tetap tersedia dan menerima asumsi yang wajar.

Prioritas mengikuti temuan ini: otomatisasi pengisian dan pemeriksaan sebelum render terlebih dahulu; optimasi decode menyusul. Bukan menurunkan FPS lagi atau menghapus kekayaan desain.

## 3. Keputusan kontrak dan kompatibilitas

| Komponen | Sekarang | Target implementasi |
| --- | --- | --- |
| Sumber/paket |2.3|2.4|
| Laporan/template |2.2.2|2.2.3; tampilan sama|
| Media/layout/font |2.2.0|Tetap2.2.0|
| Reader/index |2.3|2.4; indeks tetap ringkas|
| Generator |6|7|
| Sampling |6FPS adaptif|Tetap6FPS adaptif|
| Pengukuran piksel |Wajib jika ada ~×|Opsional; estimasi visual sah|

Versi2.4 diperlukan agar pelonggaran pengukuran tidak mengubah validitas sumber2.3 diam-diam. Sumber2.3 tetap aturan pengukuran asal,2.2 tetap10FPS, format sebelumnya tetap kontraknya. Renderer lama/template/font terdaftar tidak ditimpa;2.2.3 menambah penerimaan sumber2.4 tanpa redesain.

Paket diterima hanya berubah melalui ZIP revisi eksplisit. edh001 r0003/2.1 tetap aktif. Dua hasil2.3 di audit/result/ adalah hasil pilot yang tersedia; penyerahannya untuk evaluasi bukan instruksi ingest. Riwayat2.0/2.2 pada dokumen dipertahankan dengan hash/status pada waktunya; file yang telah diganti tidak diklaim masih byte-identik.

## 4. Urutan implementasi

### Tahap 1 — Selaraskan aturan estimasi dan beban kerja

Ubah panduan inti sebelum kode/default baru diberlakukan.

- Pan/Orbit yang jelas ditulis dengan perkiraan ~°; Dolly/Zoom yang jelas diusahakan dan ditampilkan dengan ~×. Rentang visual diterima, misalnya Dolly-In (~1.8–2.2×) + Pan Right (~15–20°).
- Ketiadaan focal length, kalibrasi atau derajat3D unik bukan alasan tunggal untuk menghilangkan estimasi. Asumsi lensa/perspektif boleh dipakai sebagai dasar pendekatan, tanpa kewajiban mencari sumber eksternal.
- Bila rekaman memang tidak memungkinkan estimasi yang berguna, jelaskan kendala khusus komponen tersebut; jangan menyalin alasan umum ke semua shot. Ketidakpastian tidak menghapus gerak yang jelas.
- scale_measurement boleh null walau ada ~× pada sumber2.4. estimate_basis tetap satu kalimat ringkas mengenai jangkar/pengamatan/asumsi; tidak perlu esai pembuktian.
- Bila pengukuran diisi, tetap periksa evidence/dimensi/nilai/urutan/rasio. IN=akhir/awal, OUT=awal/akhir; ~× bukan tempo atau jarak fisik. Asumsi tidak menjadi klaim pengukuran nyata.
- camera_checks tetap memeriksa depth/translation/rotation dengan bukti, tetapi basis cukup singkat per sumbu. Komponen/fase/tempo mengikuti sumber; semua moderate sah.
- Pertahankan matriks Pan/Orbit/Truck, oklusi/paralaks/perspektif dan aturan jitter bukan Tilt. SIFT/RANSAC/pose estimation bukan langkah rutin.
- Samakan penulisan baru dengan contoh pengguna: estimasi dalam tanda kurung, + simultan dan → berurutan, satu paragraf. Pemeriksaan format tidak menebak arah atau besaran.

Selesai: aturan estimasi jelas dan tidak mendorong penghilangan angka demi menunggu kalibrasi, tanpa memaksakan angka pada bagian yang memang tidak terbaca.

### Tahap 2 — Tambahkan kontrak2.4 dan integrasi versi

- Schema2.4 memakai field yang sudah ada; jangan menambah field pembuktian kamera baru. Perbedaan inti: scale_measurement opsional/null untuk pendekatan visual.
- Pertahankan fact_coverage, facet_roles, evidence, status/negasi dan pointer sumber. Tidak membuat jumlah fakta minimal atau kuota tempo.
- Data turunan mekanis tetap dapat disimpan di audit.json final, tetapi helper yang mengisinya dari keputusan auditor.
- Tambahkan renderer/template2.2.3, reader/index2.4 dan dispatch generator7. Cabang reader lama dipertahankan beserta field turunan shot dan provenance.
- MD tetap enam bagian; tidak menampilkan basis estimasi, checks atau telemetry baru. Luas lantai tetap angka rentang wajib.
- Larangan video, batas paket, supersedes, sumber kanonis dan snapshot berlaku seperti2.3. Export tetap byte-identik.
- Generator tetap deterministik; tidak melengkapi narasi/fakta/arah/tempo memakai AI.

Selesai: pasangan versi benar, estimasi visual2.4 diterima,2.3 tetap mengharuskan pengukuran menurut kontraknya.

### Tahap 3 — Otomatiskan persiapan dan pelengkapan teknis

Tambahkan helper authoring yang bekerja pada audit.json di workspace. Nama CLI berikut merupakan antarmuka target implementasi, belum perintah yang tersedia saat plan ditulis.

| Perintah target | Tugas |
| --- | --- |
| prepare | Menerima sumber dan daftar cut frame-index yang telah diperiksa AI; menyiapkan session, kerangka audit.json, batas PTS, calon panel dan sampling awal |
| complete | Mengisi ulang hanya field mekanis yang diizinkan, setelah keputusan audit ditulis; menampilkan perubahan yang dilakukan |
| mark-viewed | Mencatat deklarasi pemeriksaan eksplisit untuk pass/frame yang benar-benar sudah dilihat |
| check-input | Memeriksa sumber audit dan audit-info tanpa membuat JPEG; diagnostik terkelompok |

Ketentuan:
- Deteksi cut boleh memberi kandidat, tetapi AI memastikan cut nyata terlebih dahulu. Pergantian area tidak otomatis cut.
- Gunakan frame-index/native PTS sebagai dasar. Batas detik, frame awal/akhir dan midpoint dihitung helper yang sama dengan validator; jangan meminta AI mengetik ulang9desimal atau memilih tie-break sendiri.
- prepare dapat mengambil baseline seluruh shot dalam satu batch. Sertakan calon midpoint yang belum tercakup sebagai pemeriksaan pendukung satu frame, bukan otomatis5frame native di tiap tengah shot.
- Metadata komponen dihitung parser dari satu notasi fase; camera_summary dihitung dari urutan fase. AI tidak mengisi keduanya secara manual. Helper tidak menciptakan komponen, sudut, fase atau tempo.
- selected_frame_indices/mode/sampling_fps diambil dari hasil sampling asli. viewed_frame_indices tetap kosong sampai deklarasi AI; ekstraksi/cache hit tidak dianggap melihat.
- Jika midpoint tambahan dimasukkan, buat record native pendukung dengan interval PTS yang tepat; jangan menyisipkan indeks ke baseline sehingga tidak cocok aturan selected_indices.
- Kerangka berisi placeholder yang jelas; bukan fakta/default gaya/ruangan atau kandidat yang sudah valid. Overview wide, label area, rute, fakta, narasi dan estimasi dipilih auditor setelah melihat.
- cut list/session/patch sementara hanya alat kerja. Finalisasi menghasilkan satu audit.json; tidak ada analysis.json atau sumber isi kedua yang dirawat paralel.
- complete hanya boleh memperbarui whitelist turunan mekanis. Konflik ID/evidence/ruang dilaporkan, bukan diperbaiki dengan menebak.
- prepare ulang tidak menimpa narasi/pilihan yang sudah diisi. Refresh turunan memakai operasi eksplisit dengan perubahan tercatat; input diterima/references/ tidak pernah diedit helper.

Selesai: AI tidak perlu menulis skrip50KB hanya untuk membangun struktur/metadata; keputusan pengamatan tetap diisi AI pada sumber yang sama.

### Tahap 4 — Pemeriksaan input wajib sebelum render

- check-input memeriksa schema audit dan audit-info, ID sumber/revisi, source/PTS, timeline, panel/midpoint, parsed notation, relasi, coverage, estimasi, log/viewed dan kecocokan renderer.
- Bentuk diagnostik stabil: path, kelompok, pesan, tindakan perbaikan. Kumpulkan kesalahan independen sekaligus; batasi keluaran agar terbaca. Bila struktur rusak, lewati pemeriksaan turunannya yang tidak aman.
- Prioritas error seperti relations.from area-vs-shot, mode native yang salah, batas waktu dan indeks frame harus ditemukan tanpa decode media final.
- Rekomendasi perbaikan boleh menunjukkan enum/nilai teknis dari helper; tidak menulis klaim visual agar lolos.
- draft-v2 selalu menjalankan pemeriksaan ini secara internal sebelum build_media. CLI terpisah tersedia untuk pemeriksaan dini, bukan kewajiban menjalankan pemeriksaan mahal dua kali.
- Pemeriksaan setelah render tetap memvalidasi artefak/hash/inventory/ukuran/MD; preflight tidak menggantikannya. Aturan log/metadata dipakai bersama agar preflight dan validator final tidak berbeda.
- Kandidat lama tetap utuh jika preflight/render gagal. Tidak ada render, overwrite kandidat atau ZIP ketika input tidak valid.
- Snapshot tidak berubah karena telemetry/cache. Perubahan isi memerlukan draft/review baru; receipt lama tidak berlaku.

Selesai: delapan contoh kesalahan Gemini dapat didiagnosis tanpa mengulang render; struktur invalid tidak menyebabkan traceback turunan atau koreksi fakta otomatis.

### Tahap 5 — Sampling dan ekstraksi yang dapat digunakan kembali

- Session mengikat hash MP4, stream, native PTS, timeline/cuts, FPS dan parameter ekstraksi. Hilangkan pembulatan manual pada sample untuk shot yang sudah terdaftar di session.
- Baseline6FPS hanya satu putaran per timeline yang sama; ambil tambahan frame untuk perubahan seleksi atau pendalaman.
- Pendalaman menyebut pertanyaan dan rentang yang relevan. Seluruh shot/native tetap boleh jika benar-benar perlu; jangan memakai alasan umum yang sama untuk rutin mengulang semua shot.
- Gunakan ulang sampling yang cocok melalui opsi resume/session eksplisit. Aturan output lama yang menolak folder berisi tetap aman; jangan menimpa direktori berbeda secara paksa.
- Frame yang sudah diperiksa tetap diketahui melalui log sumber/pass-nya; frame baru saja yang perlu diperiksa tambahan. Cache tanpa catatan viewed yang cocok tidak membuktikan pemeriksaan.
- Tambahkan ekstraksi beberapa indeks sekaligus untuk mengurangi proses FFmpeg dan decode berulang. Metadata/PTS dipakai ulang dalam operasi yang sama.
- Cache berada di workspace sementara, terikat source hash/stream/indeks/parameter/versi extractor dan hasil hash. Sumber berubah, cache rusak atau parameter berubah harus menginvalidasi cache.
- Cache dapat dibangun ulang dan dibatasi ukurannya; tidak menjadi ketergantungan ingest, tidak disimpan ke registry/pustaka/ZIP.
- Implementasi media/font/layout yang sudah diterima tetap immutable. Optimasi masuk lapisan ekstraksi/cache dan orkestrasi, dengan pembandingan byte media.
- Batch baru hanya dipakai untuk renderer terdaftar jika menghasilkan byte JPEG yang sama. Jika tidak identik, pertahankan jalur ekstraksi asal dan optimalkan reuse frame asal; jangan mengganti encoder atau media version diam-diam.

Selesai: baseline identik tidak diekstrak ulang;24permintaan media edh058 dapat memakai18frame unik yang sama; tidak perlu audit tambahan hanya karena midpoint wajib.

### Tahap 6 — Render hanya bagian yang berubah dan log performa

- Pisahkan dependency render per kolase/Overview/Storyboard/MD. Cache memakai seluruh input yang relevan: seleksi/frame, urutan, judul/gaya/area, notasi, timing, konfigurasi, versi template/font/layout/implementasi.
- Perubahan fakta/basis yang tidak memengaruhi media dapat memakai JPEG lama. Notasi/judul yang berubah harus memperbarui media terkait; perubahan kolase memperbarui Storyboard.
- Cache hit tidak melewati validasi final. Jika ragu atas dependensi, render ulang; byte kandidat lengkap tetap dikunci review terbaru.
- Cache dan log hanya state kerja di luar kandidat. Ekspor tidak merender ulang walau cache hilang; hanya memvalidasi/mengemas snapshot disetujui.
- Catat otomatis waktu mulai/akhir, durasi helper, hit/miss cache, jumlah decode/frame unik, kegagalan dan retry pada work/performance.jsonl.
- Catat perpindahan tahap untuk memperkirakan waktu alur, tetapi bedakan durasi alat, selang waktu percakapan dan jeda persetujuan. Jangan menganggap semua jarak timestamp sebagai waktu komputasi/analisis.
- Instruksi meminta progres singkat setelah sampling, simpulan visual, preflight dan kandidat siap, sesuai kemampuan UI provider. Tidak menambah permintaan konfirmasi antarputaran internal.
- Jumlah log/field kerja tidak berkembang menjadi tabel baru dalam analysis.md atau persyaratan source baru yang harus diketik AI.

Selesai: koreksi metadata tidak membuat ulang8JPEG, log menjelaskan operasi yang diulang, dan review/export tetap mengikat snapshot utuh.

### Tahap 7 — Ringkaskan workflow ChatGPT/Gemini dan perbarui kit

Alur target: sumber + kit → prepare dengan cut terkonfirmasi → lihat frame/desain/kamera → isi audit dan deklarasikan viewed → complete/check-input → draft/review → koreksi → satu persetujuan keseluruhan → export.

- README tetap pintu masuk singkat. Metode visual satu dokumen; petunjuk authoring menjelaskan perintah baru dengan contoh langsung yang telah diuji.
- Utamakan estimasi visual yang berguna. Tidak mengarahkan AI mengejar pose3D, mencari bukti eksternal atau menghapus sudut karena lensa tidak terkalibrasi.
- Template/contoh normal dan multi area memakai contoh sintetis lengkap di resource kit; label jelas fixture, bukan isi yang disalin ke audit nyata.
- Jelaskan relasi shot vs area, parser komponen, logging native, midpoint dan penanganan error tanpa meminta AI mencari fungsi internal/import yang belum pasti.
- Pastikan semua perintah yang disarankan benar-benar ada dan portable. Tidak lagi menyarankan perintah audit.py validate yang tidak tersedia.
- Pertahankan4file input luar kit bila memungkinkan; runtime/panduan/contoh baru dibundel sebagai resource lokal berhash.
- Prompt koreksi memakai pekerjaan yang sudah selesai dan helper refresh yang sesuai; tidak mengulang seluruh pengamatan tanpa alasan.
- Prompt ekspor hanya sesudah persetujuan keseluruhan nyata. Kit/contoh/provider report tidak menjadi bukti persetujuan pengguna.
- Ratusan referensi tetap melalui registry/generator; helper authoring/cache tidak menjadi jalur discovery tambahan.

Selesai: pipeline contoh dapat dijalankan di workspace kosong dengan perintah resmi, tanpa script builder khusus per video dan tanpa unduhan jaringan/tool analisis baru yang wajib.

### Tahap 8 — Regresi teknis, performa dan pilot nyata

Pengujian:
1. Sumber2.4 visual ~×/~° diterima tanpa pengukuran; pengukuran opsional yang diisi tetap diperiksa. Sumber2.3 tetap menolak hilangnya pengukuran yang diwajibkan kontraknya.
2. Notasi Pan/Orbit/Dolly sesuai format baru; ketidakpastian spesifik tetap sah. Tidak menilai kebenaran sudut visual hanya dari teks.
3. prepare/complete menghasilkan PTS/midpoint/parser/summary sama dengan validator, termasuk30/60FPS, sumber≤6, VFR, cut boundary dan shot pendek.
4. Ekstraksi/cache/session tidak otomatis mengisi viewed. Record tambahan midpoint dan pendalaman tidak merusak coverage.
5. Kelompok error independen ditampilkan sebelum media; spy memastikan nol pemanggilan render untuk audit-info/input salah. Jangan mengandalkan timing tes yang mudah fluktuatif.
6. Ulang baseline memakai cache yang sesuai; perubahan source/cut/stream/parameter menginvalidasi; korupsi/cache parsial/symlink ditolak atau dibangun ulang dengan aman.
7. Batch/cache menghasilkan byte media yang sama dengan jalur asal. Golden MD normal/multi tetap6bagian tanpa tabel proses; layout/font/renderer lama tidak berubah.
8. Dependency render benar untuk perubahan fakta, basis, notasi, gaya/judul/area, panel, scale dan layout. Cache tidak membuat hasil lama terbawa ke snapshot baru.
9. Export byte-identik, receipt usang ditolak, ingest/replay/mixed legacy tetap benar; cache/log tidak masuk ZIP.
10. Reader2.4 mempertahankan semua sumber lama, status/negasi/label baru/facet/pointer;300model tetap ringkas tanpa log/cache/pengukuran lengkap di indeks.
11. Kit portable menjalankan alur2.4 pada contoh normal/multi, resume/koreksi dan ekspor; semua contoh hanya root fixture terisolasi.

Jalankan checks wajib:
- python -m unittest discover -s tests -t . -v
- python tools/library.py build
- python tools/library.py check
- python tools/build_audit_kit.py --check
- git diff --check

Benchmark lokal terpisah:
- Gunakan sumber/cuts yang sama; ukur prepare, check-input invalid/valid, draft cold, draft warm, koreksi metadata dan koreksi kamera.
- Catat durasi nyata, decode/FFmpeg calls, cache hit dan kesamaan output; jangan mengklaim peningkatan waktu AI dari benchmark helper.
- Target mekanis: nol render input invalid, nol decode ulang pada cache hit yang valid, nol perhitungan PTS/parser manual, dan render ulang hanya dependensi yang berubah.
- Angka18detik render lokal/sekitar24menit menuju kandidat Gemini2.3 menjadi konteks awal, bukan SLA lintas komputer/provider.

Pilot:
- Pengguna menjalankan ulang edh058 pada chat baru ChatGPT/Gemini sesuai pembagian yang disepakati, menggunakan kit baru dan hash MP4 yang sama.
- Simpan hasil di audit/result/<provider>/v2.4/run-NN/ dengan nama ZIP kanonis; hasil2.3 tidak ditimpa. Provider/model, hash kit/sumber/paket dan status nyata dicatat.
- Bandingkan waktu sampai kandidat siap terpisah dari waktu persetujuan/ekspor. Sasaran awal pengurangan sekitar30% dari alur2.3 yang sebanding; ini target evaluasi, bukan batas waktu yang boleh mengorbankan audit.
- Data lama berupa laporan provider, bukan benchmark terkontrol. Jika model/lingkungan berubah, jelaskan batas perbandingan; jangan mengarang menit yang dihemat.
- Tinjau seluruh arah/fase/tempo/estimasi, Camera Start/Overview, detail rumah, keterwakilan fakta, MD dan media. Semua moderate boleh; lebih sedikit frame/fakta tidak otomatis lebih baik.
- Bila lebih cepat tetapi detail hilang atau sudut kembali dihapus tanpa alasan khusus, perbaikan belum memenuhi tujuan. Bila tetap lambat, gunakan log untuk menemukan penyebab sebelum menambah aturan baru.
- Setelah alur memadai, lanjutkan lima pilot lain. Tooling siap, run nyata, koreksi, persetujuan, ekspor dan ingest selalu dicatat terpisah.
- Tidak menambahkan pengujian manfaat melalui produksi konsep/gambar/video ke pekerjaan ini.

## 5. Peta perubahan file

Path relatif terhadap root HOMEKU. Baris “ubah” berarti jalur yang harus ditelaah; jika dispatch terpusat sudah cukup, dokumentasikan alasan tanpa mengedit file sia-sia.

| Tindakan | File | Perubahan |
| --- | --- | --- |
| Ubah | audit/visual-audit.md, protocol.md, rubric.md, vocabulary.md | Estimasi visual sah, piksel opsional, pendalaman terarah; metode kamera/desain dipertahankan |
| Ubah | audit/README.md, json-guide.md, providers.md, prompts/01-audit.md, 02-correct.md, 03-export.md | Workflow helper baru, progres, koreksi efisien dan persetujuan tunggal |
| Ubah | audit/template-audit.json, template-audit-info.json | Default2.4, contoh field baru hanya jika diperlukan; log tidak menandai viewed otomatis |
| Tambah | audit/authoring.md | Panduan perintah resmi dan penanganan error; tidak mengulang matriks visual |
| Tambah | audit/examples/normal/audit.json, audit/examples/multi/audit.json | Contoh sintetis lengkap, selaras fixture/golden dan jelas bukan referensi aktif |
| Tambah | docs/contracts/audit-v2-4.schema.json, manifest-v2-4.schema.json, package-v2-4.md | Kontrak estimasi visual, kompatibilitas dan paket baru |
| Tambah | docs/contracts/reference-reader-v2-4.schema.json, search-index-v2-4.schema.json, ai-reader-v2-4.md | Cabang sumber baru/provenance, indeks tetap ringan |
| Tambah | docs/contracts/analysis-v2-2-3.md, tools/assets/templates/analysis-2.2.3.md, tools/homeku/reporting_v2_2_3.py | Penerimaan2.4, struktur tampilan sama; versi lama immutable |
| Ubah | tools/homeku/versions.py, __init__.py, models.py, audit_quality.py | Dispatch2.4, reader2.4/generator7, estimasi visual dan validasi berversi |
| Tambah | tools/homeku/authoring.py | prepare/complete, turunan mekanis, calon panel dan deklarasi viewed |
| Tambah | tools/homeku/preflight.py | Pemeriksaan input tanpa render, diagnostik terkelompok dan aturan bersama |
| Tambah | tools/homeku/audit_session.py | Identitas session, pass, cache/resume dan invalidasi sumber/timeline |
| Tambah | tools/homeku/video_cache.py | Cache frame/PTS dan lapisan ekstraksi batch, tetap menjaga byte |
| Tambah | tools/homeku/audit_performance.py | Timer/log kerja di luar kandidat, tanpa efek pada isi/snapshot |
| Ubah | tools/audit.py, tools/homeku/exporter.py, validation.py | CLI resmi, preflight wajib sebelum render, session/cache dan orkestrasi draft |
| Ubah | tools/homeku/video.py | Ekstraksi batch/context cache; semantik PTS/nearest lama dipertahankan |
| Ubah | tools/homeku/media.py | Integrasi provider/cache di dispatcher tanpa menimpa implementasi media terdaftar |
| Ubah | tools/homeku/reporting.py, report_validation.py | Dispatch laporan baru dan struktur MD berversi |
| Ubah | tools/homeku/generation.py, reader.py, engine.py | Sumber baru dan reader/provenance, fingerprint, ingest/build; tidak menebak fakta |
| Ubah | tools/build_audit_kit.py | Bundle helper/panduan/contoh baru, inventory/hash dan pintu masuk singkat |
| Hasil builder | audit/homeku-audit-kit.zip | Regenerasi resmi, bukan edit ZIP manual |
| Ubah/tambah | tests/fixtures/factory.py, tests/fixtures/README.md, tests/fixtures/reports/*-2.2.3.md | Fixture sumber2.4, contoh normal/multi, golden MD |
| Tambah | tests/test_audit_authoring.py, test_audit_preflight.py, test_audit_cache.py, test_audit_efficiency.py | Regresi otomasi, error awal, cache, dependensi, log dan portable workflow |
| Ubah bila diperlukan | tests/test_audit_method.py, test_audit_quality.py, test_audit.py, test_improvement.py, test_v2_1_compatibility.py, test_v2_reader.py, test_v2_reporting.py | Default baru dengan assertion kompatibilitas lama tetap |
| Tambah | tools/benchmark_audit.py | Benchmark lokal terisolasi cold/warm/koreksi, tanpa ingest atau AI |
| Ubah | audit/calibration.md, pilots/README.md, pilots/edh058-comparison.md | Hasil2.3 nyata, hash terbaru/historis, run2.4 belum berjalan |
| Selaraskan | docs/audit-method-6fps-implementation-plan.md, docs/audit-method-verification.md | Catatan lanjutan pilot2.3; hasil pengujian historis tidak ditulis ulang |
| Ubah | README.md, AGENTS.md, docs/operations.md, docs/v2-field-map.md | Default baru setelah implementasi dan batas tanggung jawab helper |
| Tetap/telaah | docs/template-analysis-v2.md, sources/fact-facets.json | Struktur enam bagian dan mapping tidak diubah kecuali ada kebutuhan nyata yang tercatat |
| Tambah sesudah verifikasi | docs/audit-efficiency-verification.md | Checks/benchmark nyata, hash kit dan status pilot terpisah |
| Hasil generator | catalogs/, knowledge/, data/projections/, data/search-index.json, data/dependencies.json, data/build.json | Hanya build; bukan edit fakta manual |

Tidak menimpa media_v2_2.py, renderer/template lama, font/layout diterima, ZIP hasil provider, bekerja/, video/, references/, registry atau ledger. Publikasi referensi hanya melalui ingest final terpisah yang diinstruksikan pengguna. Workflow CI sudah memantau tools/tests/contracts/audit/sources; ubah hanya jika pemeriksaan menunjukkan kebutuhan nyata.

## 6. Kriteria selesai dan pengaman

**Tooling selesai** ketika kontrak2.4 dan estimasi visual diterima, helper menghilangkan pengisian mekanis berulang, seluruh error input ditemukan sebelum render, cache aman/byte-identik, laporan tetap sesuai template, reader/build kompatibel, kit portable lengkap dan semua checks lulus.

**Efisiensi terbukti** ketika benchmark mencatat berkurangnya operasi berulang dan pilot provider menunjukkan alur lebih ringan tanpa kehilangan detail/estimasi. Tidak menjanjikan semua video selesai dalam jumlah menit yang sama.

**Pilot selesai** hanya sesudah audit benar-benar dijalankan, seluruh hasil dikoreksi dan disetujui pengguna, lalu diekspor sesuai snapshot. Menyelesaikan kode tidak menjadi persetujuan kandidat atau instruksi ingest.

Implementasikan1→8 secara berurutan. Tahap persiapan/perubahan kontrak tidak mengganti default aktif sebelum jalur baru terintegrasi dan diverifikasi; regenerasi kit/build dilakukan setelah integrasi. Jika optimasi mengubah byte aset lama, gagal invalidasi cache atau mengurangi isi, pertahankan jalur asal dan selesaikan masalah sebelum publikasi tooling baru.

Pada penyusunan awal dokumen ini hanya plan. Tooling/kit/turunan kini sudah diterapkan; sumber referensi aktif, ZIP hasil pilot dan persetujuannya tetap utuh. Hasil nyata pada [verifikasi efisiensi](audit-efficiency-verification.md).

## Catatan penjabaran implementasi

Lapisan tools/homeku/media_incremental.py ditambahkan sebagai executor subset byte-kompatibel; media_v2_2.py yang terdaftar tetap immutable. Frame sampling dapat diambil batch; media final tetap memakai extractor kanonis sekali/frame unik dan cache, sehingga optimasi tidak mengubah JPEG. CLI sample --session --frames menerima pilihan tambahan panel/Overview tanpa pembulatan waktu manual. Output CLI pass diringkas menjadi ID/count/sheet; log lengkap tetap di session workspace. Ini pelengkapan mekanisme dalam cakupan tahap3–6, bukan penambahan field audit.


## Status akhir implementasi

| Tahap | Status nyata |
| --- | --- |
|1|Aturan estimasi visual dan panduan inti selaras; piksel opsional pada2.4 |
|2|Kontrak2.4/report2.2.3/reader2.4/generator7 terintegrasi, format lama tetap |
|3|prepare/complete/mark-viewed serta session/PTS/parser/midpoint tersedia |
|4|check-input/preflight wajib sebelum render, diagnostik terkelompok |
|5|Sampling batch, pilihan native tambahan, resume dan cache sumber tervalidasi |
|6|Cache media per dependensi, byte-identik, log render/review/export |
|7|Kit4file/78resource, panduan authoring/contoh dan prompt terbaru |
|8 teknis|190tes, build/check/kit-check/diff-check lulus; benchmark lokal tercatat |
|8 provider|Run2.4 ChatGPT/Gemini belum dilaksanakan; tidak ada persetujuan/ekspor/ingest baru |

engine.py sudah memakai JSON_CONTRACTS terpusat sehingga tidak perlu edit tambahan. report_validation.py sudah memakai DEFAULT_REPORT sehingga dapat memilih2.2.3 tanpa mengubah checker. Template authoring MD, sources/fact-facets.json dan workflow CI tetap karena tidak memerlukan perubahan. Media terdaftar/font/layout/renderer lama tidak ditimpa. Rincian benchmark dan pengaman berada di docs/audit-efficiency-verification.md.

## Lanjutan kamera2.5 — 24 November 2026

Dua hasil edh058 sumber2.4 kini tersedia/diperiksa, MD serta8JPEG sesuai renderer; belum disetujui/di-ingest. Pemeriksaan visual tambahan hanya18frame, bukan audit seluruh baseline. Laporan waktu provider bukan benchmark terkontrol. Implementasi kamera2.5 melanjutkan plan audit-camera-implementation-plan.md; run2.5 pengguna belum dijalankan. Status historis di atas berlaku pada saat dicatat.
