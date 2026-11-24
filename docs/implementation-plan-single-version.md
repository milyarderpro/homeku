# Plan implementasi — HOMEKU satu versi dan audit ringkas

Tanggal: 24 November 2026. Status: **rencana; belum diimplementasikan**.

## 1. Hasil yang dituju

HOMEKU memakai satu format aktif, satu implementasi renderer, satu schema per jenis dokumen, dan satu alur audit hingga ingest. Hapus dukungan versi lama dari runtime dan kit, bukan sekadar menyembunyikannya. audit.json menjadi sumber final yang lebih ringkas; analysis.md tetap lengkap dan mengikuti tampilan yang sudah disepakati.

Prioritas: ketepatan pengamatan, kelengkapan pengetahuan desain, kemudahan pengisian di ChatGPT/Gemini, kemudian efisiensi tooling. Tidak ada pengurangan detail untuk mengejar batas ukuran atau jumlah fakta.

**Urutan pekerjaan:** kontrak → sumber ringkas → fungsi bersama → authoring/validasi → render/media → generator/reader → helper → kit/dokumentasi → hapus legacy → verifikasi → pilot.

## 2. Temuan eksplorasi

| Temuan nyata | Dampak | Perbaikan |
| --- | --- | --- |
| Template audit saat ini 424 baris untuk satu shot; profile 17 objek/189 baris; satu fase sekitar 57 baris | Banyak penulisan berulang dan placeholder wajib | Hilangkan duplikasi dan hasil turunan dari sumber final |
| Enam modul media, enam modul reporting, sembilan template laporan, 48 berkas kontrak di docs/contracts | Percabangan versi berlapis dan bundle membesar | Satu implementasi, template dan kumpulan kontrak aktif |
| media.py mengekspor helper dari media_v2_1_2; media terbaru dan incremental masih mengimpor modul lama | Menghapus file berdasarkan nama akan merusak runtime terbaru | Pindahkan fungsi yang masih digunakan sebelum penghapusan |
| camera_notation.py masih memanggil parser dalam markdown.py | Parser kamera terbaru bergantung pada parser MD legacy | Parser kamera mandiri |
| reporting.py mengambil helper dari reporting_v2_legacy; validation/exporter masih mendukung MD sumber | Runtime tetap memiliki dua model sumber | Hanya audit.json sebagai sumber isi |
| Schema, fingerprint generator, tes dan Actions menunjuk docs/contracts serta docs/template-analysis-v2.md | Pembersihan docs dapat merusak build/kit/CI | Pindahkan aset wajib ke schemas/, tools/assets/ dan audit/ |
| authoring.md masih memuat kewajiban angka yang bertentangan dengan aturan opsional | AI mendapat instruksi berbeda | Satu kebijakan kamera yang sama di panduan, schema dan validator |
| motion-hints mengembalikan interval tanpa ringkasan makro | AI harus merangkum banyak angka sendiri | Ringkasan agregat yang benar, helper tetap opsional |
| Registry kosong dan incoming tidak berisi ZIP | Tidak ada referensi aktif yang perlu dimigrasi | Pergantian format bersih, tanpa converter atau adapter lama |

Ukuran contoh sintetis saat eksplorasi: normal 18.023 byte/7 fakta; multi area 23.977 byte/12 fakta. Ini baseline teknis, bukan ukuran audit rumah nyata atau target kuota fakta.

## 3. Batas pekerjaan dan aturan tetap

- Target satu identitas format **3.0** untuk audit, paket, report, media dan reader. Ini penanda perubahan struktur yang tidak kompatibel; bukan tambahan cabang di samping 2.5. Nama file/modul tanpa suffix versi. Fingerprint kode/aset tetap diperlukan untuk integritas dan cache.
- Format 1.x–2.5 tidak didukung setelah cutover. Paket/session lama ditolak dengan pesan jelas untuk memakai kit terbaru dan audit ulang; tidak dikonversi diam-diam. Tidak ada compatibility flag, alias CLI lama, atau salinan runtime lama dalam archive.
- video/ dan archive/oldrepo/ tetap utuh. Hasil audit/result/ lama dipertahankan sebagai bahan pembanding di luar discovery sampai pengguna membersihkannya sendiri; tidak dikemas dalam kit atau dijadikan sumber baru.
- Pengguna akan memilih penghapusan dokumen historis setelah implementasi. Pekerjaan ini memindahkan kebutuhan aktif keluar dari docs, bukan menghapus seluruh docs sekarang.
- Satu take sampai cut nyata tetap satu shot; perubahan area bukan cut. Multi area, visibilitas overlap, area yang muncul kembali dan kamera yang melihat beberapa area tanpa memasuki semuanya tetap didukung.
- Baseline 6 FPS + batas native; sumber ≤6 FPS atau shot <1 detik diperiksa seluruh native. Pendalaman 10 FPS/native terarah, tanpa menurunkan baseline.
- Penentuan gerak mengikuti depth → translation → rotation; bedakan Pan/Orbit/Truck melalui perubahan perspektif, paralaks, oklusi dan jangkar. Goyangan/tilt tipis insidental tidak otomatis menjadi komponen Tilt.
- Notasi kamera mengikuti eksperimen pengguna: + simultan, → berurutan; Straight/Diagonal/Pure, intensitas dan easing dipertahankan. Angka opsional per komponen, tunggal atau rentang; asumsi visual wajar sah. Tidak memaksa angka, rentang, pengukuran piksel atau penurunan confidence saat angka tidak ditulis.
- ~× adalah rasio perubahan skala gambar, bukan tempo. Semua shot moderate sah. Arah, kronologi dan tempo sumber tidak diganti dengan default produksi.
- Gaya utama/pengaruh/interior berbahasa Inggris, penjelasan Indonesia. Estimasi luas lantai wajib min–max; MD cukup menampilkan **60–90 m²**, tanpa tambahan dasar perkiraan atau label kepastian.
- ZIP final hanya audit.json, analysis.md, manifest.json dan media terdaftar. Tanpa video, sheet, cache, session, log kerja atau receipt.
- Pengguna memeriksa keseluruhan hasil di chat. Export memakai byte snapshot yang sama; tidak render ulang. Ingest tidak meminta review isi baru.
- Tidak ada sintesis AI di generator, API AI tambahan, plugin produksi baru, atau pengujian manfaat melalui pembuatan konsep/gambar dalam pekerjaan ini.

## 4. Susunan repo tujuan

~~~text
README.md
AGENTS.md
schemas/
  audit.schema.json
  audit-info.schema.json
  manifest.schema.json
  reference-reader.schema.json
  search-index.schema.json
audit/
  README.md
  visual-audit.md
  authoring.md
  json-guide.md
  camera-cases.md
  vocabulary.md
  concept-workflow.md
  contracts/
    package.md
    report.md
    reader.md
  prompts/{01-audit,02-correct,03-export}.md
  template-audit.json
  template-audit-info.json
  examples/{normal,multi}/audit.json
  pilots/README.md
  homeku-audit-kit.zip
tools/
  audit.py
  library.py
  build_audit_kit.py
  homeku/
    __init__.py
    models.py
    derivations.py
    render_assets.py
    camera_notation.py
    camera_pattern.py
    media.py
    reporting.py
    ...modul fungsi aktif lainnya
  assets/
    templates/analysis.md
    layouts/media.json
    fonts/...
docs/
  implementation-plan-single-version.md
  implementation-verification-single-version.md
  ...catatan historis pilihan pengguna
~~~

Tidak ada kode, kit, tes atau Actions yang memerlukan isi docs/. Schema dibaca lokal/offline. Bila schema memakai referensi bersama, gunakan $defs lokal atau resource yang masuk inventaris eksplisit; tidak mengunduh schema.

Tiga kontrak di audit/contracts merupakan dokumentasi aktif. analysis.md tetap laporan manusia; schemas/audit.schema.json menjelaskan sumber terstruktur AI. Plan/verifikasi dalam docs bukan input generator.

## 5. Bentuk sumber audit yang lebih ringkas

Kelompok sumber final: schema_version, id, revision, design, areas, shots; relations dan notes hanya bila diperlukan. Nama field tetap jelas, tidak disingkat menjadi kode satu huruf. Definisi rinci dibekukan pada tahap 1 sebelum tooling diubah.

### 5.1 Profil desain ditulis sekali

- design.name: nama desain.
- design.styles: primary, influences dan interior; pengaruh/gaya interior diskret berupa daftar bila lebih dari satu. Tidak mengulangnya dalam profile.
- design.size: scale, levels, footprint, proportions dan floor_area_m2 {min,max}.
- design.features: klaim fleksibel untuk massing, roof, entrance, porch, openings, material hierarchy, palette, lighting, environment, spatial configuration, distinctive features dan continuity.
- Tidak ada kewajiban membuat 17 objek DNA placeholder. Aspek yang diperiksa tetapi tidak diketahui bisa dinyatakan unknown/not-visible. Aspek yang tidak diisi berarti tidak dinilai, bukan tidak ada.
- MD mengambil nama gaya, ukuran, warna/material dan ciri khas dari field yang sama. Generator tidak membuat interpretasi gaya atau hubungan DNA baru.

Pemetaan wajib sebelum implementasi: primary-style/style-influence/interior-style → styles; apparent-scale/levels-visible → size; aspek DNA lainnya → features berlabel eksplisit. Massing/roof/palette tidak boleh disalin lagi sebagai fakta profil kedua.

### 5.2 Fakta dan narasi desain

Setiap blok shot.design mengikat area_ids dan memiliki architecture, furnishings, environment. Masing-masing kategori memuat text untuk laporan manusia serta facts untuk pengetahuan terstruktur.

- Fakta memuat subject, attribute, value, state, evidence dan facet_roles struktural yang relevan. Kategori dan scope area diketahui dari tempat fakta berada; override area harus eksplisit bila diperlukan.
- State tetap eksplisit: observed, uncertain, not-visible, not-present, unknown. Tidak ada default observed/high. Confidence boleh tidak diisi bila tidak dinilai; reader tidak mengarang confidence pengganti.
- Evidence spesifik fakta tetap ada. Bukti satu kategori tidak otomatis membuktikan seluruh fakta di dalamnya.
- ID klaim yang hanya dipakai untuk pemetaan lama tidak wajib ditulis manual; pointer sumber dan identitas turunan dibuat mekanis. ID area tetap eksplisit karena membedakan ruang fisik.
- Hapus fact_coverage dan daftar fact_ids paralel: hubungan kategori–fakta ditentukan lokasi sumber. Kategori tanpa pengamatan tetap menyatakan batasnya secara singkat bila perlu.
- Ketercakupan struktural bisa dihitung; kelengkapan makna paragraf tetap diperiksa auditor di chat. Tidak mengklaim validator bisa memahami seluruh isi narasi.
- Narasi dan fakta mempunyai fungsi berbeda dan keduanya tetap diperlukan. Tidak ada ekstraksi fakta dari prosa oleh generator, kuota jumlah fakta, atau penghapusan detail furnitur/konfigurasi untuk menghemat byte.
- Field note opsional menyimpan batas/asumsi yang relevan; tidak mewajibkan basis + uncertainty berulang pada setiap klaim.

### 5.3 Kamera: satu notasi dan pengamatan per fase

shot.camera memuat description untuk manusia, phases dan tempo. Setiap fase menyimpan interval, notation, depth_direction, fokus/scope, bukti temporal bersama dan observations ringkas untuk depth/translation/rotation.

- Hapus components_parsed, raw per komponen dan camera_summary dari audit final. Parser bekerja dari notation; ringkasan shot dihitung dari urutan fase.
- Gabungkan camera_checks, motion_observations serta basis berulang menjadi observations per fase. Ketiga pemeriksaan sumbu tetap wajib dan spesifik pada interval, termasuk Pan-only/Static.
- Bukti per komponen hanya ditambahkan sebagai override bila berbeda atau perlu menjelaskan ambiguitas. Bukti bersama tidak disalin tiga kali.
- Estimasi angka tetap di notation; asumsi khusus/alternatif hanya diberi catatan saat menambah informasi. Tidak ada kewajiban scale_measurement; pengukuran piksel/helper detail adalah catatan kerja, bukan objek wajib audit final.
- Depth_direction tetap keputusan auditor: IN/OUT/NO IN/OUT/null ambigu. Parser memeriksa konflik dengan Dolly eksplisit; tidak menebak arah dari zoom atau skala global.
- Tempo memiliki satu sumber: label + description untuk tempo seragam; segments bertimestamp + description bila berubah. Pada bentuk segments, label keseluruhan dan tempo per fase dihitung dari overlap, bukan ditulis ulang.
- Batas perubahan tempo boleh berbeda dari batas fase gerak. Tidak memecah fase gerak hanya untuk menghilangkan perbedaan tempo.
- Easing per komponen tidak disamakan secara otomatis dengan tempo keseluruhan. Pertahankan pengamatan perubahan kecepatan yang memang tidak terwakili notasi.
- journey/alur visual hanya bila diperlukan untuk menjelaskan perjalanan multi area; tidak mewajibkan pengulangan paragraf kamera.

### 5.4 Timeline, framing dan media

- Pertahankan start_s/end_s shot dan fase dengan PTS presisi; durasi/tampilan dua desimal dihitung. Area visibility, rute kamera dan hubungan ruang tetap eksplisit, bukan disimpulkan dari urutan shot.
- Camera Start tetap memuat posisi, arah pandang, angle, tinggi/kemiringan; framing awal/akhir, foreground/depth/reveal, fokus dan lighting tetap tersedia sesuai pengamatan.
- Pilihan panels/overviews menyimpan frame_index, scope area dan informasi visual yang diperlukan. Hapus shot_id berulang, timestamp dan ID buatan manual yang bisa diturunkan dari posisi di shot.
- Normal tiga panel: Start, Middle, End; midpoint dipilih dari PTS native terdekat. Multi area dinamis, dengan awal/akhir dan momen penting. Label khusus multi hanya bila berguna.
- Overview memiliki composition_summary tersendiri karena menjelaskan frame terpilih, bukan otomatis awal shot. Tidak dihapus sebagai duplikasi Camera Start.
- Timestamp/ID panel dan metadata teknis dipusatkan dalam manifest, dihitung dari MP4. Bukti frame native di luar kolase tetap didukung.
- Manifest menyediakan pemetaan frame→PTS yang diperlukan untuk selections/evidence, tanpa seluruh daftar frame video. Reader/render laporan dari paket final dapat bekerja tanpa MP4; ingest/verifikasi sumber tetap menggunakan MP4 kanonis.
- Gambar tetap N+2: shot-NN.jpg, overview.jpg satu baris, storyboard.jpg kolase vertikal. Font, warna, hierarki, caption Start · 8.30s di bawah panel dan waktu lebih kecil mengikuti tampilan yang sudah disetujui.

### 5.5 Ringkasan penghapusan/pemindahan field

| Sekarang | Tujuan |
| --- | --- |
| identity + size + profile berulang | design terstruktur; setiap nilai profil hanya satu sumber |
| style_names_language=en per audit | Aturan tetap kontrak, tanpa field berulang |
| components_parsed/raw/summary | Hasil parser/derivations, tidak ditulis ulang ke audit |
| tempo fase + tempo_profile + rhythm yang bertumpuk | Satu objek tempo, label/overlap mekanis |
| fact_coverage/fact_ids | Kategori fakta melekat pada blok desain |
| checks/observations/evidence berulang | Pengamatan tiga sumbu + bukti bersama per fase |
| scale_measurement/bukti pengukuran rutin | Workspace opsional; isi audit tetap hasil pengamatan |
| selection.shot_id/timestamp/id standar | Metadata terpusat di manifest |
| review_summary/status proses/catatan ganda | Workspace atau notes relevan tunggal |
| basis/uncertainty/alternatives/null kosong wajib | Note opsional; state/negasi/bukti tetap eksplisit |

## 6. Tanggung jawab setiap keluaran

| Berkas | Isi |
| --- | --- |
| audit.json | Seluruh keputusan isi dan pilihan visual auditor; satu sumber final ringkas |
| analysis.md | Enam bagian laporan manusia, selalu hasil renderer/template |
| manifest.json | Provenance sumber, metode/pemeriksaan frame, pemetaan PTS/selection, media/bbox/hash, render fingerprint dan revisi |
| data/projections/<id>.json | Representasi AI hasil generator dengan pointer sumber, derivasi yang berguna dan inventaris media; tidak diedit |
| data/search-index.json | Facet/filter ringkas untuk memilih referensi/shot; bukan salinan seluruh audit |
| catalogs/ dan knowledge/ | Keluaran deterministik dari sumber eksplisit |
| workspace/session/cache/log/receipt | Proses kerja dan pengukuran; bukan fakta pustaka atau isi ZIP |

Tidak ada audit ringkas khusus authoring yang kemudian diwajibkan mengembang menjadi audit panjang. Derivations menghasilkan nilai yang diperlukan saat render/read/build, tanpa menulis format lama atau salinan sumber lengkap yang kedua.

## 7. Rencana perubahan file

### A. Tambah

| File | Tujuan |
| --- | --- |
| schemas/audit.schema.json | Struktur ringkas tunggal dan field wajib/opsional |
| schemas/audit-info.schema.json | Input provenance/metode, tanpa menduplikasi isi audit |
| schemas/manifest.schema.json | Metadata paket tunggal dan pemetaan frame/media |
| schemas/reference-reader.schema.json, schemas/search-index.schema.json | Kontrak AI dengan pointer ke sumber baru |
| tools/homeku/derivations.py | Parser summary/pattern, ID, scope dan tempo overlap mekanis bersama; tanpa sintesis |
| tools/homeku/render_assets.py | Font/path/helper teks/angka yang masih dipakai, mandiri dari legacy |
| audit/contracts/package.md, report.md, reader.md | Tiga kontrak aktif yang tidak bergantung docs |
| audit/concept-workflow.md | Alur discovery → pemilihan DNA → konsep → Camera Start/Overview → prompt, dipindahkan dari dokumen aktif lama |
| tests/test_repository_integrity.py | Impor/aset/schema/kit tanpa legacy atau ketergantungan docs |
| docs/implementation-verification-single-version.md | Hasil nyata, ukuran/waktu, checks dan batas verifikasi setelah implementasi |

Modul baru hanya untuk fungsi yang dipakai lintas komponen; hindari fragmentasi file untuk helper kecil satu pemakai.

### B. Ubah atau satukan

| File/kelompok | Perubahan |
| --- | --- |
| tools/homeku/__init__.py | Satu identitas format; hilangkan daftar format didukung dan nomor report/media/reader terpisah |
| models.py, audit_quality.py, preflight.py | Validasi schema ringkas, scope/bukti/negasi, tiga sumbu, tempo dan input sebelum render |
| camera_notation.py, camera_pattern.py | Parser mandiri; tidak mengimpor markdown; notasi lengkap dan derivasi pointer baru |
| media.py | Serap implementasi media terbaru dan akses crop; hilangkan dispatch versi |
| reporting.py, report_validation.py | Serap renderer terbaru; enam bagian/template wajib dari sumber baru |
| authoring.py, audit_session.py | Prepare/complete sumber ringkas; edit bertahap per shot; viewed eksplisit; tidak memperluas ke format lama |
| exporter.py, validation.py | Hanya paket JSON tunggal; review seluruh snapshot, allowlist file dan export byte sama |
| video.py, video_cache.py, audit_performance.py, media_incremental.py | Cabut impor versi lama, pertahankan batching/resume/quota, cache key baru dan byte-parity |
| motion_analysis.py | Tambah ringkasan makro, coverage/gap tracking, keluaran ringkas default |
| generation.py, reader.py, engine.py | Model/pointer/facet baru, registry hanya format aktif, cache fingerprint baru, build kosong dan revisi |
| common.py, storage.py | Telaah dan pertahankan fungsi umum/lock/rollback yang masih benar; jangan rewrite tanpa kebutuhan |
| tools/audit.py | Satu CLI: inspect, prepare, sample, mark-viewed, complete, check-input, draft, review, export, motion-hints |
| tools/library.py | Pertahankan operasi ingest/build/check/search/read/panel/shot-image; sesuaikan reader/versi tunggal |
| tools/build_audit_kit.py | Inventaris runtime/aset/schema aktif yang eksplisit, tanpa legacy atau hasil pilot |
| tools/benchmark_audit.py | Ukur JSON/kit dan tahap alat secara setara, cold/warm, tanpa audit visual atau ingest produksi |
| tools/make_test_packages.py, tests/fixtures/factory.py, tests/fixtures/README.md | Factory tunggal, MP4 fixture terpisah; hapus parameter pembuat berbagai versi |
| tests/*.py | Port skenario relevan ke sumber tunggal; satukan tes berdasarkan fungsi, bukan kronologi versi |
| audit/template-audit.json, template-audit-info.json | Skeleton minimal bermakna; tanpa 17 placeholder profil atau field turunan |
| audit/examples/normal/audit.json, multi/audit.json | Contoh lengkap sintetis struktur final, bukan data rumah nyata |
| audit/README.md, visual-audit.md, authoring.md, json-guide.md, camera-cases.md, vocabulary.md | Spasi normal, satu aturan aktif, perintah konsisten, tanpa riwayat versi |
| audit/prompts/01-audit.md, 02-correct.md, 03-export.md | Prompt pendek sesuai tahap; tidak mengulang seluruh kontrak |
| README.md, AGENTS.md, references/README.md | Entry point satu versi dan tautan aktif di luar docs |
| audit/pilots/README.md | Tujuh pilot/status nyata, edh001 dari r0001, kit baru untuk run baru |
| sources/design-principles.json, data/taxonomy.json | Pertahankan kurasi; pindahkan pointer capability/alur dari docs; tanpa menebak alias baru |
| .github/workflows/library-ci.yml, library-ingest.yml | Trigger schemas/tools/assets; core + helper opsional; tanpa path wajib docs |
| tools/homeku/actions.py, tools/publish_actions.py, tests/test_actions.py | Telaah publikasi/concurrency/root terisolasi dan penyalinan aset baru |
| requirements.txt, requirements-audit-motion.txt | Telaah dependensi yang benar-benar dipakai; OpenCV/NumPy tetap opsional |

Perintah draft/export baru hanya menerima audit JSON/kandidat; hapus --renderer-version, --contract-version, --include-source, extras legacy dan alias draft-v2/export-v2.

### C. Hapus setelah pemakai dipindahkan

- tools/homeku/versions.py dan markdown.py; konstanta umum yang masih berguna dipindahkan, parser MD sumber dihapus.
- Seluruh tools/homeku/media_v*.py: enam modul saat eksplorasi.
- Seluruh tools/homeku/reporting_v*.py: enam modul, termasuk reporting_v2_legacy.py.
- Seluruh template analysis-*.md lama setelah tools/assets/templates/analysis.md siap; layout media-*.json setelah tools/assets/layouts/media.json siap.
- Seluruh docs/contracts/ setelah schema/kontrak aktif selesai dipindahkan dan semua pemakai diperbarui. Tidak mempertahankan converter atau schema historis dalam kit.
- audit/template-analysis.md sebagai template authoring MD legacy.
- sources/fact-facets.json setelah semua fakta baru memakai facet_roles eksplisit dan tidak ada fallback generator.
- tests/test_v2_1_compatibility.py; isi tes fungsi penting dipindahkan dahulu. File test_v2_* lainnya diganti nama menjadi test_models.py, test_media.py, test_reader.py, test_reporting.py setelah konsolidasi.
- Fixture ZIP lama yang menyertakan video dan golden laporan versi lama. Golden tampilan terbaru normal/multi dipertahankan isinya sebagai acuan lalu disimpan dengan nama netral.
- audit/protocol.md, rubric.md, providers.md, calibration.md setelah isi aktif yang masih diperlukan digabung ke panduan utama. Pembahasan hasil pilot tetap pada audit/pilots dan tidak dibundel sebagai jawaban audit baru.

Tidak menghapus file hanya karena nama mengandung versi sebelum impor, CLI, tes, build kit dan referensi asetnya sudah dipindahkan.

### D. Bangun ulang, jangan edit fakta turunan manual

audit/homeku-audit-kit.zip; catalogs/; knowledge/; data/projections/; data/search-index.json; data/dependencies.json; data/build.json.

Registry/ingest saat ini kosong. Pastikan tetap kosong selama penggantian tooling. Perubahan header teknis format/envelope dilakukan eksplisit bila schema baru memerlukannya; tidak mengarang referensi/persetujuan baru.

## 8. Urutan implementasi dan syarat selesai

| Tahap | Pekerjaan berurutan | Syarat selesai |
| --- | --- | --- |
| 1 | Bekukan kontrak ringkas, pemetaan semua field lama yang masih berguna, contoh normal/multi, serta daftar field sumber/turunan/workspace | Tidak ada kebutuhan MD/AI yang kehilangan sumber; setiap field hanya satu pemilik |
| 2 | Buat schemas/, kontrak aktif dan template/layout bernama netral; ukur baseline ukuran dan simpan acuan tampilan terbaru | Schema offline valid; target bentuk JSON jelas; belum menghapus aset lama |
| 3 | Mandirikan parser kamera dan helper render; buat derivations murni | Tidak ada parser terbaru yang memanggil parser MD; helper bebas import cycle |
| 4 | Port models/quality/preflight dan authoring/session ke audit ringkas | Prepare → isi → mark-viewed → complete → check-input berjalan; invalid gagal sebelum render |
| 5 | Port media/report/export/validation ke sumber tunggal | Normal/multi MD enam bagian dan N+2 JPEG; crop/bbox benar; snapshot/export sama byte |
| 6 | Port generator/reader/registry/ingest ke pointer/facet baru | Semua fakta/status/scope dapat dibaca; search selektif; empty/revision/replay/full rebuild benar |
| 7 | Tambah ringkasan motion-hints dan ukur efisiensi | Agregasi benar, data hilang tidak ditutup angka palsu, helper tanpa OpenCV tetap fallback |
| 8 | Satukan CLI/panduan/prompt/kit dan ubah CI; alihkan seluruh dependensi docs | Kit mandiri bekerja dari folder baru tanpa repo; sumber aturan konsisten |
| 9 | Hapus modul/aset/schema/cabang/fixture legacy dan rapikan tes | Tidak ada impor, fallback, alias atau bundle versi lama; format lama ditolak jelas |
| 10 | Jalankan verifikasi lengkap, benchmark setara, build ulang dan dokumentasikan hasil | Checks akhir lulus; satu format aktif; dokumen historis bisa dihapus tanpa merusak runtime |
| 11 | Jalankan pilot baru dengan kit final yang sama | Status hasil/approval/export/ingest dicatat nyata; implementasi tidak mengklaim pilot selesai |

Tahap 1–10 dilakukan end-to-end saat implementasi diminta, tanpa berhenti pada penambahan schema saja. Transisi internal sementara tidak boleh tersisa dalam hasil akhir. Jangan menambahkan kompatibilitas demi mempertahankan tes lama; port skenarionya.

## 9. Efisiensi authoring dan helper

### Authoring

- Prepare mengikat sumber/cut, menyiapkan baseline sekali dan skeleton yang ringkas. Tidak membuat fakta, keputusan gaya atau persetujuan.
- Sediakan pengisian/update satu shot melalui helper resmi; pembaruan atomik pada audit.json yang sama. File patch opsional hanya workspace sementara, bukan format sumber kedua atau isi ZIP.
- Complete hanya menyelaraskan metadata mekanis/normalisasi eksplisit; tidak menambahkan kembali parsed/summary/coverage ke audit final. Perubahan ditampilkan.
- State/confidence/arah/tempo/fakta tidak dihitung dari prosa dan tidak diisi default demi lolos validator.
- Draft memakai konteks preflight yang sudah sah untuk menghindari pengulangan probe/hash/decode dalam pemanggilan yang sama. Cache lintas pemanggilan tetap divalidasi sumber/runtime/config.
- Perubahan kamera atau narasi tidak otomatis mengekstrak semua frame ulang; render hanya keluaran terdampak dengan hasil yang sama seperti render penuh.
- Progres singkat per tahap bila UI mendukung; tidak ada jeda konfirmasi internal atau janji durasi provider.

### Motion-hints

- Tetap opsional, tanpa verdict Dolly/Pan/Orbit, tanpa menandai viewed atau mengisi audit otomatis.
- Default output: ringkasan dan interval bermasalah; rincian interval tersedia dengan opsi --details.
- Tambah cakupan interval valid, durasi tercakup, tren awal–tengah–akhir, perubahan skala 2D dan selisih zona gambar yang valid.
- Skala kumulatif dihitung dengan komposisi yang benar. Translasi kumulatif tidak boleh sekadar menjumlah dx/dy ketika ada scale/rotation; simpan/komposisikan transform dan ukur pada titik acuan yang jelas.
- Interval gagal memutus rantai: laporkan per rentang kontinu atau null untuk total yang tidak dapat dihitung. Jangan mengalikan/menjumlah hanya interval sukses lalu menamakannya seluruh shot.
- Zona atas/bawah tetap zona gambar, bukan label dekat/jauh. Gerak 2D bukan pengukuran pose kamera fisik.
- Pertahankan batas frame/resolusi, quota, caching berhash, bounded retry dan fallback tanpa OpenCV/NumPy. Statistik/cache/log tidak masuk ZIP, indeks atau knowledge.

## 10. Verifikasi yang diperlukan

### Integritas isi dan format

1. Contoh normal/multi mencakup gaya, ukuran/luas, massa/atap/bukaan, material, lingkungan, arsitektur/furnitur, relasi area, framing dan kamera. Buat matriks kemampuan/field, bukan sekadar membandingkan jumlah key.
2. State/negasi/unknown dan confidence yang memang dinilai dipertahankan. Tidak ada asumsi observed/high, material fisik, denah, atau arah gerak dari narasi.
3. Uji semua contoh notasi eksperimen, angka tunggal/rentang/tanpa angka, easing berbeda, koma desimal dan x/×; pertahankan qualifiers/toward/raw melalui pointer turunan.
4. Uji Pan-only/Static, OUT+Orbit+Pan, perubahan arah, tempo seragam dan berubah tanpa pergantian fase, bukti di luar scope, pilihan belum viewed dan frame palsu.
5. Uji visibilitas overlap/reentry, area terlihat tetapi tidak dilalui, dua ruang berlabel sama, satu area dua fungsi dan multi area dinamis.
6. MD harus tepat enam bagian, A/B/C, seluruh narasi, gambar dan camera summary yang sama dengan fase sumber. Template tidak boleh dilonggarkan untuk mengatasi input salah.
7. Preview normal/multi diperiksa secara visual: hierarchy font/caption/waktu, Overview satu baris dan Storyboard vertikal; crop panel/blok tanpa MP4 benar.

### Runtime, paket dan generator

8. Uji cut/PTS presisi, sumber VFR/low-FPS/shot pendek, stream video yang benar, baseline 6 FPS dan pendalaman terarah.
9. Uji ekstraksi batch 32/resume/partial cache/bounded retry, error permission, file rusak, source berubah, memory/quota dan cache fingerprint baru.
10. Uji preflight invalid tanpa JPEG, koreksi parsial vs render penuh byte-identik, review mengikat seluruh snapshot, perubahan pascareview ditolak, export tidak render ulang.
11. Uji ZIP allowlist tanpa video dalam bentuk ekstensi/casing apa pun, traversal/symlink/duplicate/path collision, hash sumber/media dan fixture ditolak root produksi.
12. Uji ingest pertama/revisi/supersedes/duplicate/replay, lock/concurrency/rollback/recovery dan publikasi Git lokal. MP4 sumber tidak diduplikasi/ditimpa keliru.
13. Uji reader/pointer/provenance semua kategori dan fase, panel/shot-image tanpa MP4, taxonomy/label baru/facet_roles eksplisit serta pemisahan prinsip kurasi dari fakta sumber.
14. Uji root kosong dan 300 model sintetis format tunggal; pagination, indeks selektif, stale-output removal dan hasil full/incremental sama. Tidak membuat 300 referensi aktif.
15. Uji kit dari folder kosong tanpa checkout, tanpa docs, tanpa runtime di sys.path host dan tanpa jaringan bootstrap. Seluruh impor transitif/aset/template/schema tersedia.
16. Uji salinan repo dengan docs dihilangkan: build/check/kit/fixture workflow tetap berjalan. Lakukan hanya pada root sementara, bukan menghapus docs pengguna.
17. Pastikan runtime/kit tidak mengandung modul lama, cabang versi, import cycle atau path wajib docs. Format/session lama ditolak, bukan diterima oleh fallback.
18. Uji helper nyata dengan OpenCV/NumPy, termasuk komposisi/gap/rotasi/skala dan fallback tanpa dependensi. Catat skip atau lingkungan yang belum diuji secara jujur.

### Ukuran dan waktu

Bandingkan fixture dengan informasi yang setara: JSON pretty/compact bytes, jumlah field berulang, resource/byte kit, prepare cold/resume, complete/check-input, draft cold/warm/koreksi dan helper off/on. Simpan hasil ringkas di verifikasi.

Targetnya sumber/kit lebih sederhana dan tidak ada pekerjaan lama yang tidak diperlukan. Jangan menjanjikan persentase pemangkasan atau menit audit chat sebelum diukur. Ukuran kecil tidak boleh dicapai dengan minify saja, mengurangi fakta, atau memindahkan seluruh beban yang sama ke manifest.

Checks akhir:

~~~sh
python -m unittest discover -s tests -t . -v
python tools/library.py build
python tools/library.py check
python tools/build_audit_kit.py
python tools/build_audit_kit.py --check
git diff --check
~~~

Jalankan suite lengkap setelah integrasi; pengembangan memakai tes terarah. Setelah checks lulus, jangan mengulang benchmark mahal tanpa perubahan atau masalah baru yang relevan.

## 11. Dokumen aktif dan pembersihan docs berikutnya

Setelah implementasi, entry point hanya README.md → audit/README.md atau references/README.md. Panduan isi, authoring, JSON dan kontrak aktif berada di audit/; schema di schemas/; template/layout/font di tools/assets/.

- Pindahkan isi alur konsep/capability yang masih relevan ke audit/concept-workflow.md; ubah pointer sources/design-principles.json.
- Hapus ketergantungan fingerprint/CI/tes/kit pada docs/template-analysis-v2.md dan docs/contracts/.
- Satu template renderer resmi di tools/assets/templates/analysis.md. Contoh baru normal/multi harus mengikuti template ini.
- Jangan menautkan plan/verifikasi lama sebagai instruksi operasional aktif. Tidak perlu menyalin seluruh riwayat keputusan ke panduan baru.
- Pada laporan akhir implementasi, berikan daftar dokumen aktif dan dokumen historis yang dapat dipertimbangkan pengguna untuk dihapus. Jangan menghapus pilihan dokumen pengguna otomatis.
- Plan ini dan laporan verifikasi boleh dihapus setelah tidak diperlukan; tidak memengaruhi operasi pustaka.

## 12. Pilot dan definisi selesai

Tujuh pilot: edh001, edh058, edh013, edh033, edh049, edh056, dreamshome01. edh001 telah direset; audit baru mulai r0001 dengan supersedes null. Hasil edh058 lama hanya pembanding, tidak dikonversi menjadi hasil 3.0.

Sesudah tooling selesai, gunakan MP4 asli dan kit baru pada chat baru. Pengguna menilai desain, framing, kamera/tempo, MD dan media sebelum ekspor final. Kit diubah lagi hanya bila temuan pilot menunjukkan kekurangan sistem; jangan menambal ZIP tanpa memperbaiki penyebabnya.

**Implementasi dinyatakan selesai bila:** satu format/CLI aktif; tidak ada dependensi legacy atau docs; audit final benar-benar ringkas; MD/media tetap lengkap; knowledge/pencarian tidak kehilangan fakta/scope/status; kit portable dan checks lulus; hasil benchmark dan batas verifikasi tercatat. Pustaka tetap kosong sampai ZIP hasil audit baru disetujui dan di-ingest.

**Pilot dinyatakan selesai terpisah:** hanya sesudah audit nyata, tinjauan pengguna, ekspor dan ingest yang benar-benar terjadi. Tidak ada klaim kualitas kamera atau percepatan provider dari fixture teknis.
