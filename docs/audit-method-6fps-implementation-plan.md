# Plan implementasi metode audit visual dan baseline 6 FPS

> Status setelah reset 24 November 2026: data audit edh001 telah dihapus atas permintaan pengguna. Catatan edh001 di dokumen ini bersifat historis, bukan referensi aktif atau persetujuan audit baru.

Status: tahap1–7 selesai diterapkan dan diverifikasi pada23November2026; tahap8 siap dijalankan pengguna di ChatGPT/Gemini, belum ada run2.3. Disusun 23 November 2026 berdasarkan evaluasi pilot edh058 dan perbandingan dengan bekerja/masterprompt/audit-video.md. Melanjutkan audit-quality-implementation-plan.md; bukan penulisan ulang riwayat implementasi2.2.

## 1. Tujuan dan hasil yang diharapkan

1. AI memeriksa seluruh komponen gerak sebelum memilih notasi, sehingga Dolly tidak terlewat ketika Pan juga terlihat.
2. Baseline audit baru6FPS dengan pendalaman10FPS/native berdasarkan pertanyaan visual yang belum terjawab.
3. Estimasi kamera dan tempo konsisten, tetap mengikuti sumber.
4. JSON menyimpan hasil pengamatan yang lengkap; analysis.md tetap laporan manusia enam bagian.
5. Detail bentuk/konfigurasi desain dapat ditemukan melalui indeks tanpa menebak fakta dari narasi.
6. Kit memandu AI mengamati terlebih dahulu, kemudian mengisi data dan mengemas hasil.

Akurasi tidak dijanjikan hanya karena jumlah frame atau validator lulus. Keberhasilan metode dinilai melalui hasil pilot; keberhasilan tooling dinilai melalui tes teknis. Seluruh proses pengamatan dan koreksi tetap di chat sebelum satu persetujuan keseluruhan kandidat.

## 2. Batas perubahan dan kompatibilitas

| Komponen | Sebelum implementasi | Target yang diterapkan |
| --- | --- | --- |
| Sumber audit/paket | 2.2 | 2.3 |
| Renderer/template laporan | 2.2.1 | 2.2.2; tampilan sama |
| Media/layout/font | 2.2.0 | Tetap2.2.0 |
| Reader/index | 2.2 | 2.3 |
| Generator | 5 | 6 |
| Baseline audit baru | 10FPS | 6FPS; pendalaman10FPS/native |

Versi sumber baru diperlukan karena baseline wajib berubah dan ada data pemeriksaan baru. Renderer baru menerima sumber2.3 tanpa menimpa implementasi2.2.1 yang telah terdaftar. Template2.2.2 memakai struktur visual yang sama; bukan redesain laporan.

- Sumber2.2 tetap baseline10FPS menurut kontraknya. Format1.0/1.1/2.0/2.1 tetap aturan asal; tidak ada pelonggaran global atau konversi otomatis.
- edh001 r0003/2.1 tetap aktif sampai ada ZIP revisi eksplisit yang disetujui. Memperbarui reader bukan mengubah audit sumber.
- Paket2.3 meneruskan larangan video dalam ZIP: hanya audit.json, analysis.md, manifest.json dan N+2 JPEG. MP4 input terpisah dan tersedia di video/<id>.mp4 sebelum ingest.
- Satu take kontinu tetap satu shot walaupun multi area. Camera Start tetap awal sumber; Overview wide tidak menggantikannya.
- Nama gaya English; penjelasan Indonesia; luas lantai wajib rentang angka, tampilan tanpa tambahan catatan.
- Katalog, knowledge, proyeksi, indeks dan metadata build hanya dihasilkan generator.
- Dokumen bekerja/ dibaca sebagai acuan metode. Target produksi4/6detik, reverse, format laporan tiga bagian dan asumsi lima shot tidak masuk kontrak audit pustaka.

## 3. Urutan implementasi

### Tahap 1 — Tetapkan metode pengamatan visual inti

Tambahkan audit/visual-audit.md sebagai satu panduan pengamatan utama.

Urutan per shot: baca perjalanan utuh → periksa maju/mundur → periksa translasi lateral/vertikal yang relevan → periksa rotasi pandangan → gabungkan komponen simultan → tentukan pergantian fase → estimasi → tempo → simpulan.

Isi wajib:

- Matriks Pan/Orbit/Truck dengan tiga kolom pembanding yang sama: oklusi foreground, selisih paralaks, perubahan perspektif/posisi subjek.
- Pertahankan contoh konkret kusen membuka/menutupi elemen belakang dan penjelasan gerakan gabungan. Tambahkan kasus edh058: Pan-only melewatkan OUT pada living room/bathroom.
- Perlakukan tes sebagai petunjuk yang diperiksa bersama; tidak menganggap satu delta layar sebagai pengukuran pose3D yang pasti.
- Sebelum menyatakan Pan-only atau NO IN/OUT, wajib menyelesaikan pemeriksaan skala, kedalaman, oklusi dan kemungkinan zoom.
- Bedakan hasil tidak ada gerak kedalaman dari belum dapat ditentukan. Tidak memaksakan IN/OUT pada shot Pan/Static yang memang netral.
- Gabungan Dolly+Pan/Orbit/Truck tetap dicatat bila didukung; tidak memilih satu gerakan saja karena paling menonjol.
- Periksa fase di awal, tengah, akhir dan titik perubahan; multi area tidak otomatis menjadi fase atau shot baru.
- Tilt nyata diperiksa bila terlihat; drift/jitter vertikal kecil tidak menjadi label tilt.
- Adaptasi rubrik eksterior7parameter/interior6parameter dari masterprompt untuk detail desain, dengan status sesuai bukti dan tanpa mengarang material fisik atau hubungan antarshot.

Selesai ketika matriks, contoh pembeda dan urutan pemeriksaan eksplisit tersedia dalam satu panduan; protocol/rubric merujuknya tanpa memelihara versi logika yang berbeda.

### Tahap 2 — Tetapkan kontrak dan data minimum2.3

Simpan keputusan audit sebelum serialisasi sebagai catatan kerja sementara di workspace chat. Catatan ini bukan sumber data kedua dan tidak masuk ZIP. Isi final tetap satu audit.json.

Tambahan minimum pada JSON:

| Lokasi | Isi dan batas |
| --- | --- |
| phases[].camera_checks | depth, translation, rotation; masing-masing evidence ID dan basis singkat. translation mencakup lateral/vertikal yang relevan. Tidak menyalin verdict depth_direction atau daftar komponen sebagai fakta manual kedua. |
| motion_observations[].scale_measurement | Objek nullable: anchor, dimension width/height, start_evidence, end_evidence, start_px, end_px. Wajib untuk estimasi skala ~× yang dinyatakan; titik ukur memakai objek/bagian yang sama dan tidak terpotong. |
| motion_observations[].estimate_basis | Tetap dipakai. Menjelaskan dasar sudut atau batas estimasi; bila komponen memerlukan estimasi tetapi angka belum dapat ditentukan, alasan eksplisit wajib ada. |
| facts[].facet_roles | Daftar peran pencarian terstruktur yang relevan, dapat kosong untuk fakta yang tidak masuk filter struktur. Nama atribut dan label asli tetap disimpan. |

camera_checks menegakkan pencatatan pemeriksaan sumbu yang tidak muncul pada notasi. motion_observations tetap menyimpan bukti komponen yang dipilih; matriks tidak disalin tiga kali pada tiap komponen. Pointer bukti dipakai ulang, tanpa menambah JPEG atau metadata frame berulang.

Validator memeriksa keberadaan, referensi, interval dan konsistensi field. Validator tidak membaca makna gambar atau menganggap basis terisi sebagai bukti klasifikasi benar.

Selesai ketika schema mandiri, matriks versi, aturan ketergantungan field dan contoh JSON normal/multi disepakati dalam kontrak. Tidak ada field pemeriksaan baru yang ditambahkan ke MD manusia.

### Tahap 3 — Implementasikan sampling adaptif6FPS

- Baseline6FPS mencakup seluruh shot, selalu menyertakan frame native pertama/terakhir.
- Sumber ≤6FPS memakai seluruh frame tersedia. Tidak ada interpolasi menjadi6/10/30FPS.
- Shot <1detik diperiksa native; perubahan arah/reveal cepat atau detail ambigu langsung diperiksa lebih rapat pada rentang terkait.
- Bagian belum jelas diperiksa10FPS, lalu native bila perlu; boleh langsung native. Pendalaman tidak wajib selalu mengambil tengah shot.
- Log pendalaman menyebut pertanyaan visual dan rentang yang benar-benar diperiksa.
- Record di bawah6FPS tidak menggantikan baseline2.3; log2.2 tetap memerlukan10FPS.
- Sampling/ekstraksi tidak otomatis menjadi viewed. Frame bukti, panel dan Overview yang dipilih tetap harus tercatat diperiksa.
- Kebijakan baseline berada pada dispatch versi. Jangan mengganti semua literal10 menjadi6 dalam kode atau helper PTS generik.

Selesai ketika CLI sampling, validator dan panduan sepakat, baseline3FPS ditolak pada2.3, baseline6FPS diterima pada2.3 dan tetap ditolak sebagai pengganti10FPS pada2.2.

### Tahap 4 — Perketat keputusan, estimasi dan tempo

- Pemeriksaan camera_checks wajib untuk seluruh fase, termasuk fase Pan-only/Static/Uncertain.
- Bukti pemeriksaan dan komponen memakai frame berbeda yang relevan dengan fase dan benar-benar viewed; toleransi batas tetap dinyatakan eksplisit menurut kontrak.
- depth_direction dan components tetap sumber simpulan; Camera Pattern tetap turunan.
- Untuk ~×, gunakan besar perubahan skala yang konsisten: IN = ukuran akhir/awal; OUT = ukuran awal/akhir. Arah tetap ditentukan dari bukti kedalaman, bukan formula skala saja.
- Notasi ~× mengikuti pembulatan satu desimal atau rentang yang sesuai data ukuran. Tidak berarti faktor kecepatan, meter tempuh, atau pose kamera fisik.
- Jika Dolly dan Zoom simultan tidak dapat dipisahkan, jangan menyalin rasio perubahan skala total menjadi estimasi masing-masing. Catat batas atribusi pada estimate_basis/uncertainty.
- Pan/Orbit memakai perkiraan sudut yang diusahakan dari orientasi/jangkar. Penghilangan angka memerlukan alasan khusus; tidak cukup null tanpa penjelasan. Gerakan tanpa satuan sudut/skala tidak dipaksa mempunyai angka tidak relevan.
- Semua shot boleh moderate. Tidak ada kuota distribusi slow/moderate/fast dan tidak ada kewajiban membuat variasi tempo.
- Pertumbuhan skala akibat perspektif tidak otomatis berarti percepatan fisik. Label perubahan tempo didukung perbandingan interval waktu setara dan konteks lintasan.
- Confidence didukung pengamatan; jumlah frame atau bukti tertulis tidak otomatis membuat confidence high.

Selesai ketika konflik field yang dapat diuji ditolak, kasus tanpa gerakan kedalaman tetap sah, dan pengecualian estimasi mempertahankan batas bukti tanpa menghapus komponen gerak yang jelas.

### Tahap 5 — Integrasikan paket, laporan dan pencarian AI

- Sumber2.3 dirender melalui report2.2.2; struktur enam bagian, anchor, A/B/C, kategori desain, media dan kondisional multi area tetap sama.
- draft/review/export/ingest mengenali2.3; pairing salah ditolak. Export mempertahankan byte snapshot yang disetujui, tanpa render ulang.
- Reader2.3 mempertahankan seluruh format lama dan mengekspos camera_checks, pengukuran skala, facet_roles serta pointer asal.
- Indeks tidak menyalin catatan pemeriksaan, log frame atau seluruh narasi. Simpan facet relevan dan pointer; pembacaan rinci melalui proyeksi terpilih.
- Tambahkan sources/fact-facets.json sebagai pemetaan atribut eksplisit berversi untuk format lama. Contoh opening-shape → opening, massing-and-roof → massing+roof. Ini pemetaan terkurasi, bukan inferensi dari prosa.
- Sumber2.3 memakai facet_roles eksplisit. Sumber lama memakai pemetaan terdaftar; label sumber tidak diganti. Provenance turunan menunjukkan sumber aturan pemetaan.
- Atribut belum dipetakan tetap tersimpan dan dapat ditemukan melalui inventory/topik fakta; tampilkan daftar yang belum dipetakan pada diagnostik teknis, tanpa mengarang peran baru.
- Pertahankan state, negasi dan uncertainty dalam hasil pencarian/knowledge.

Selesai ketika kasus bentuk pintu dan massa/atap edh058 dapat masuk facet yang tepat, label baru tidak hilang, dan source accepted tetap byte-identik.

### Tahap 6 — Rapikan instruksi ChatGPT/Gemini dan kit

- README kit menjadi pintu masuk ringkas dengan urutan tahap; tidak menggabungkan13panduan menjadi satu instruksi aktif.
- Saat mulai audit: inspect metadata/cut, lalu baca visual-audit.md dan jalankan putaran pengamatan.
- Setelah simpulan visual diperiksa silang: baca panduan JSON, isi sumber final, draft dan validasi.
- Rubrik memeriksa simpulan; panduan JSON menjelaskan field; protokol menjelaskan urutan kerja. Matriks visual hanya dirawat di visual-audit.md.
- Prompt01 memulai audit; prompt02 dipakai saat koreksi; prompt03 dipakai sesudah persetujuan keseluruhan. Contoh teks persetujuan pada dokumen tidak menjadi persetujuan pengguna.
- Panduan dan kontrak yang diperlukan dipulihkan bootstrap sebagai resource lokal berinventaris/hash. Tidak ada ketergantungan unduhan jaringan atau file panduan yang hilang dari kit.
- Pertahankan empat file input luar kit bila memungkinkan; seluruh dokumen pendukung berada dalam payload bootstrap. ZIP hasil referensi tetap satu paket tanpa MP4.
- Jangan menambah konfirmasi pengguna di antara putaran pengamatan dan penulisan JSON. Persetujuan keseluruhan kandidat tetap titik yang sudah disepakati.

Selesai ketika kit pada workspace bersih bisa menjalankan seluruh alur dengan panduan sesuai tahap dan tidak membaca instruksi ekspor sebagai tugas audit awal.

### Tahap 7 — Regresi teknis dan build

Tambahkan tes bermakna:

1. Baseline6FPS, native sumber≤6FPS, batas shot, VFR, gap dan sampling di bawah minimum.
2. Kebijakan2.2 tetap10FPS; sumber lama dan snapshot diterima tidak ditulis ulang.
3. Camera checks hilang, bukti sama/salah fase/tidak viewed, serta konflik depth/components ditolak.
4. Pan-only yang benar, Static, Zoom tanpa translasi, Uncertain dan gerakan gabungan tetap sah; tidak dipaksa menjadi Dolly.
5. Pengukuran skala menggunakan referensi valid, satu dimensi dan nilai positif; rasio IN/OUT serta pembulatan/notasi konsisten. Estimasi tidak dapat ditentukan mempunyai alasan.
6. Enam shot seluruhnya moderate sah; klaim accelerating/decelerating dan tempo_profile yang bertentangan ditolak.
7. Facet bentuk pintu/massa/atap, label baru, negasi, unknown dan pointer sumber tetap benar.
8. Golden MD normal/multi tetap enam bagian dan tidak memuat tabel pemeriksaan teknis baru.
9. Paket tanpa video, snapshot ekspor identik, replay ingest dan campuran format lama/baru.
10. Bootstrap lengkap dan alur portable2.3 dari kit bersih; pengujian koleksi300model dengan indeks tetap ringkas tanpa camera_checks/log/measurement lengkap di dalamnya.

Fixture hanya root terisolasi. Contoh kesalahan visual edh058 menjadi bahan kalibrasi; tes teknis tidak dinyatakan membuktikan gambar telah dipahami.

Jalankan: python -m unittest discover -s tests -t . -v; python tools/library.py build; python tools/library.py check; python tools/build_audit_kit.py --check; git diff --check. Dokumentasikan hasil nyata pada dokumen verifikasi baru.

### Tahap 8 — Uji pilot sesudah tooling siap

- Audit ulang edh058 di chat baru menggunakan MP4 asli dan kit terbaru; kedua provider digunakan untuk pembandingan metode.
- Gunakan hasil Gemini2.2 dan koreksi pengguna sebagai pembanding kuat, bukan template gerakan/angka untuk disalin atau bukti persetujuan seluruh paket.
- Tinjau gerakan, fase, estimasi, tempo, detail desain dan laporan lengkap; koreksi di chat sebelum ZIP final.
- Semua label moderate tetap sah bila sesuai sumber. Tidak membuat perubahan tempo untuk mengejar variasi.
- Simpan setiap run di folder terpisah dengan nama ZIP kanonis; rekam provider yang benar-benar dipakai, versi, hash dan status.
- Bandingkan kualitas keputusan, keterbacaan, kecukupan bukti dan beban pemeriksaan. Jumlah frame lebih kecil bukan otomatis lebih baik.
- Setelah hasil memadai, lanjutkan lima pilot lain. Tooling selesai, run nyata, persetujuan, ekspor dan ingest dicatat terpisah.

Pelaksanaan pilot ChatGPT/Gemini mengikuti pembagian tugas yang sudah disepakati dengan pengguna. Menyiapkan kit tidak berarti menjalankan pilot atau mengesahkan referensi.

## 4. Peta file implementasi

Semua path di bawah relatif terhadap root repo HOMEKU.

| Tindakan | File | Perubahan |
| --- | --- | --- |
| Tambah | audit/visual-audit.md | Metode inti; rubrik desain, matriks tiga tes, urutan sumbu dan contoh pembeda |
| Ubah | audit/protocol.md, audit/rubric.md | Alur bertahap dan pemeriksaan akhir; merujuk satu metode inti |
| Ubah | audit/json-guide.md, audit/vocabulary.md | Field2.3, definisi rasio, facet_roles, status dan pengecualian estimasi |
| Ubah | audit/prompts/01-audit.md, 02-correct.md, 03-export.md | Urutan pengamatan → data → review → ekspor |
| Ubah | audit/README.md, audit/providers.md | Panduan pengguna, baseline6FPS dan pembacaan dokumen sesuai tahap |
| Ubah | audit/template-audit.json, audit/template-audit-info.json | Template2.3 dan kebijakan/log baru; audit-info hanya bila contoh/default memang perlu disesuaikan |
| Tambah | docs/contracts/audit-v2-3.schema.json, manifest-v2-3.schema.json, package-v2-3.md | Kontrak sumber/paket baru, data minimum, baseline dan kompatibilitas |
| Tambah | docs/contracts/reference-reader-v2-3.schema.json, search-index-v2-3.schema.json, ai-reader-v2-3.md | Reader/index baru dan provenance |
| Tambah | docs/contracts/analysis-v2-2-2.md | Kontrak laporan baru dengan struktur visual yang sama |
| Ubah | tools/homeku/versions.py, __init__.py | Matriks versi dan baseline; deklarasi reader/generator baru |
| Ubah | tools/audit.py, tools/homeku/exporter.py, validation.py | Sampling baru, dispatch dan penegakan paket/review/export |
| Ubah bila diperlukan | tools/homeku/video.py | Dukungan PTS/sampling6 tanpa mengubah interpretasi fungsi generik untuk versi lama |
| Ubah | tools/homeku/models.py, audit_quality.py | Validasi checks, pengukuran, referensi dan konsistensi |
| Tambah | tools/homeku/reporting_v2_2_2.py, tools/assets/templates/analysis-2.2.2.md | Renderer sumber2.3; template menyalin struktur yang disetujui |
| Ubah | tools/homeku/reporting.py, report_validation.py | Dispatch/pemeriksa laporan berversi, tanpa menimpa renderer lama |
| Tambah | sources/fact-facets.json | Pemetaan atribut lama ke peran facet yang eksplisit dan berversi |
| Ubah | tools/homeku/generation.py, reader.py, engine.py | Indeks, provenance, reader, ingest2.3 dan fingerprint pemetaan |
| Ubah | tools/build_audit_kit.py | Bootstrap menyertakan panduan lokal; README ringkas dan inventory lengkap |
| Hasil build | audit/homeku-audit-kit.zip | Kit terbaru dihasilkan builder, tidak dirakit manual |
| Ubah/tambah | tests/fixtures/factory.py, tests/fixtures/README.md, tests/fixtures/reports/*-2.2.2.md | Fixture2.3 serta snapshot lengkap normal/multi |
| Tambah | tests/test_audit_method.py | Regresi metode/6FPS/estimasi/facet dan portable2.3 |
| Ubah | tests/test_audit_quality.py, test_audit.py, test_v2_1_compatibility.py, test_v2_reader.py, test_v2_reporting.py, test_improvement.py | Ekspektasi kit/default terbaru; assertion kompatibilitas lama tetap dipertahankan |
| Ubah | audit/calibration.md, audit/pilots/README.md, audit/pilots/edh058-comparison.md | Bedakan hasil2.0 lama, dua hasil2.2 terbaru dan pilot2.3 yang belum berjalan; pertahankan identitas/hash historis |
| Ubah | README.md, AGENTS.md, docs/operations.md, docs/v2-field-map.md | Dokumentasi default dan tanggung jawab terkini setelah implementasi |
| Selaraskan | docs/template-analysis-v2.md | Tetap enam bagian; tidak menambah kolom proses, hanya acuan versi bila diperlukan |
| Tambah setelah verifikasi | docs/audit-method-verification.md | Hasil pengujian/build/kit dan status nyata |
| Hasil generator | catalogs/, knowledge/, data/projections/, data/search-index.json, data/dependencies.json, data/build.json | Hanya hasil yang berubah melalui build; bukan edit fakta manual |

Implementasi media2.2.0, font/layout terdaftar, dokumen produksi bekerja/, ZIP hasil pilot, video sumber dan references/<id>/ tidak ditulis ulang oleh pekerjaan tooling ini. Perubahan registry/ledger hanya melalui ingest final yang terpisah dan eksplisit.

## 5. Kriteria selesai

Tooling: kontrak/matriks konsisten, metode inti tersedia, sampling adaptif benar, validator dan renderer lulus tes, reader/facet/provenance lengkap, kit portable sinkron dan build/check lulus. Versi lama serta referensi diterima tetap utuh.

Pilot: kualitas visual benar-benar ditinjau di chat, koreksi masuk kandidat, persetujuan keseluruhan tercatat, ekspor byte identik; ingest dilakukan hanya jika pengguna menginstruksikan penyerahan final. Belum ada klaim bahwa pilot2.3 telah dijalankan atau lebih akurat sebelum pengujian nyata.

Pada penyusunan awal dokumen ini hanya plan. Implementasi kini sudah memperbarui tooling/kit/turunan, tanpa mengubah sumber referensi aktif atau persetujuannya. Hasil nyata dicatat pada [verifikasi metode](audit-method-verification.md).


## 6. Status pelaksanaan23November2026

| Tahap | Hasil nyata |
| --- | --- |
| 1 | visual-audit.md tersedia: urutan pengamatan, matriks pembanding dan contoh kalibrasi |
| 2 | Schema sumber/manifest2.3, camera_checks, scale_measurement dan facet_roles ditambahkan |
| 3 | Default sampling6FPS; shot<1s/native, low-FPS/VFR/batas dan kebijakan2.2 diuji |
| 4 | Checks seluruh fase, bukti viewed, rasio IN/OUT dan konsistensi tempo divalidasi |
| 5 | Renderer2.2.2, reader/index2.3, generator6 dan mapping facet terintegrasi |
| 6 | Kit empat file dengan61resource lokal berhash, instruksi per tahap dan prompt terbaru |
| 7 | 156tes lulus, build/check/kit-check/diff-check lulus; sumber/aset diterima tetap utuh |
| 8 | Panduan run terpisah ChatGPT/Gemini edh058 siap; pelaksanaan/koreksi/persetujuan/ekspor/ingest2.3 belum terjadi |

engine.py sudah memakai JSON_CONTRACTS terpusat sehingga tidak memerlukan edit tambahan. video.py tetap helper PTS generik; kebijakan6FPS ada di dispatch, exporter dan validator. template-audit-info.json tidak memiliki default FPS sehingga tetap; template authoring MD dan seluruh renderer/media/font diterima tidak ditimpa. Tes reader/report lama tetap berjalan tanpa mengubah kontrak sumbernya.

Rincian hasil, fingerprint kit dan batas pembuktian tersedia pada docs/audit-method-verification.md. Menyelesaikan implementasi tooling tidak menggantikan pelaksanaan pilot oleh pengguna.

## Lanjutan sesudah hasil pilot2.3 tersedia

Pada diskusi berikutnya pengguna telah memberikan dua hasil2.3 edh058 beserta laporan proses. Kedua paket lulus pemeriksaan teknis dan reproduksi JPEG; status “belum ada run2.3” pada catatan sebelumnya berlaku saat implementasi itu selesai. Hash terbaru dan status pada audit/pilots/edh058-comparison.md. Paket asli tidak dikonversi atau di-ingest oleh evaluasi ini. Perbaikan efisiensi berikutnya memakai kontrak2.4 menurut docs/audit-efficiency-implementation-plan.md; pengujian historis di dokumen ini tetap dicatat apa adanya.
