# Design

## Context

Lihat proposal.md untuk alasan perubahan dan specs/ untuk perilaku wajib. Eksplorasi ulang mengonfirmasi registry serta ledger ingest kosong, tidak ada main spec OpenSpec, dan runtime masih mendukung 1.0–2.5. Perubahan sengaja memutus kontrak kompatibilitas yang sekarang tercantum dalam AGENTS.md/dokumen lama sesuai keputusan pengguna.

Ketergantungan nyata: media.py dan media terbaru memakai media_v2_1_2; media_incremental memakai media_v2_2; reporting.py memakai reporting_v2_legacy; camera_notation memakai markdown.component. Generator/schema/CI masih membaca docs/contracts dan docs/template-analysis-v2.md. Kit memuat 90 resource sebelum perubahan. Template sumber 424 baris, dengan 17 objek profile sekitar 189 baris.

Baseline contoh sintetis: normal 18.023 byte/7 fakta; multi 23.977 byte/12 fakta. Angka ini untuk pembandingan teknis setara, bukan batas informasi, ground truth atau prediksi durasi provider.

## Goals / Non-Goals

**Goals:**
- Satu graph dependensi aktif yang mandiri, dengan satu pemilik untuk setiap keputusan isi.
- Sumber ringkas yang langsung final; turunan dibentuk sesuai kebutuhan renderer/reader.
- Jalur baca media/AI tanpa MP4 dipisahkan dari verifikasi sumber yang memang memerlukan MP4.
- Penghapusan docs/ dan dokumen OpenSpec pada salinan uji tidak merusak operasi.
- Mempertahankan jaminan snapshot, deterministic build, bounded cache dan publikasi konsisten.

**Non-Goals:**
- Converter, adapter, alias CLI atau runtime historis yang tetap didistribusikan.
- Penulisan ulang seluruh tooling yang masih benar; common/storage dipertahankan kecuali ada kebutuhan spesifik.
- Menghapus MP4, arsip, hasil pilot atau seluruh dokumen historis pengguna.
- Menjalankan audit pilot baru sebagai bagian dari implementasi tooling, menambah AI API/plugin, atau menguji manfaat melalui produksi konsep/gambar.

## Decisions

### 1. Satu identitas format dan nama file netral

Gunakan FORMAT_VERSION = "3.0" pada satu lokasi konstanta, dipakai audit, manifest, report/media metadata dan reader/index. Fingerprint isi kode/template/layout/font menangani invalidasi cache dan snapshot, bukan pilihan versi renderer yang berbeda. Revisi referensi tetap r0001/r0002; itu revisi konten, bukan dukungan schema ganda. Header envelope registry/ledger tidak menjadi pilihan format audit.

Schema di schemas/: audit.schema.json, audit-info.schema.json, manifest.schema.json, reference-reader.schema.json, search-index.schema.json. Kontrak aktif di audit/contracts/{package,report,reader}.md. Template/layout di tools/assets/{templates/analysis.md,layouts/media.json}. Font/lisensinya tetap aset yang sama.

Paket/session di luar 3.0 gagal sebelum proses isi/render; tidak membutuhkan salinan schema lama untuk menyampaikan kesalahan. Unknown version juga gagal. CLI audit akhir: inspect, prepare, sample, mark-viewed, complete, check-input, draft, review, export, motion-hints serta update-shot. Hapus parameter pemilihan versi dan jalur input MD/extras/include-source. CLI library tetap menyediakan operasi yang ada.

Alternatif mempertahankan kompatibilitas lokal dan hanya membuat kit slim ditolak: permintaan pengguna adalah membersihkan repo dan kit sekaligus, dan tidak ada referensi aktif yang perlu dibaca format lama.

### 2. Sumber ringkas dengan profil terstruktur sekali

Struktur top-level final: schema_version, id, revision, design, areas, shots; relations/notes opsional. Pilih nama field yang jelas; pengurangan berasal dari struktur, bukan minify atau akronim.

| Sumber baru | Pemilik informasi |
| --- | --- |
| design.name | Nama rumah/desain |
| design.styles.primary | Satu klaim gaya utama |
| design.styles.influences dan interior | Daftar klaim gaya diskret; kosong berarti belum ada klaim tercatat, bukan bukti tidak ada pengaruh |
| design.styles.relations bila ada | Relasi gaya family/blend/influence eksplisit; tidak diinferensikan dari nama |
| design.size | scale, levels, footprint, proportions serta floor_area_m2 {min,max} |
| design.features | Daftar klaim fleksibel dengan aspect: massing, roof, entrance, porch, openings, material-hierarchy, palette, lighting, environment, spatial-configuration, distinctive-features, continuity |
| areas | ID fisik, label, functions dan visible_intervals |
| shots[].design[] | Scope area dan kategori architecture/furnishings/environment |
| shots[].composition | Camera Start, framing awal/akhir, fokus, lighting, foreground/depth/reveal dan kompatibilitas gerak yang diamati |
| shots[].camera | description, phases, tempo; journey opsional untuk alur lintas area |
| shots[].panels/overviews | Pilihan frame/area; composition_summary Overview |
| relations/notes | Hubungan antarshot dan batas relevan yang benar-benar dinyatakan |

Scale/levels/footprint/proportions serta styles/features memakai klaim terstruktur: value, state, evidence; confidence/note hanya bila diisi. floor_area_m2 merupakan estimasi min/max wajib khusus; tidak mewajibkan basis/uncertainty tambahan. Tidak ada default observed/high. Field nonwajib yang tidak diisi berarti tidak dinilai.

Primary/interior style yang belum teridentifikasi dinyatakan unknown secara eksplisit bila diperlukan untuk laporan, bukan nama gaya rekaan. Label gaya English merupakan aturan kontrak; style_names_language berulang dihapus. Report memakai claim.value yang sama. Pemetaan dari 17 aspek lama adalah pemetaan kemampuan saat pengembangan, bukan converter audit produksi.

Setiap kategori shot.design memuat text dan facts. Fakta memuat subject, attribute, value, state, evidence; facet_roles eksplisit untuk filter struktural, confidence/note opsional. Domain/kategori dan area scope diturunkan dari kontainer; override area_ids hanya jika lebih spesifik dan tervalidasi sebagai subset. Tidak menyalin evidence kategori sebagai bukti seluruh fakta. Scope multi area bersama berarti auditor memang menyatakannya bersama.

Hapus profile paralel, fact_coverage, daftar fact_ids, basis/uncertainty kosong dan ID fakta yang hanya diperlukan pemetaan lama. Identitas klaim generator berasal dari pointer sumber di snapshot terkait, tidak diklaim stabil antar revisi. Klaim/relasi yang membutuhkan rujukan memakai pointer eksplisit yang divalidasi.

Narasi manusia dan fakta atomik tetap dua representasi untuk fungsi berbeda. Generator tidak memahami prosa; kesetaraan makna diperiksa auditor sebelum ekspor. Tidak ada kuota fakta atau kewajiban 17 placeholder unknown.

Alternatif menyimpan narasi saja ditolak karena kehilangan discovery terstruktur. Alternatif membungkus semua field dengan metadata lengkap wajib ditolak karena mengembalikan beban authoring yang sama.

### 3. Evidence native dan scope yang sederhana

Gunakan evidence berupa indeks frame native global sumber, misalnya [142,195,248], bukan ID panel buatan manual. Referensi tidak ambigu karena satu audit terikat satu sumber. Validator mengikat indeks ke shot/fase/area dan record viewed; frame di luar scope gagal. Klaim unknown dapat tanpa evidence, tanpa dianggap bukti negatif.

Shot/fase/visibility/route tetap memakai start_s/end_s PTS presisi dan interval half-open. Helper mengisi batas shot dari cut terkonfirmasi; auditor menetapkan batas fase/area yang benar dari PTS sumber. Angka tampilan dua desimal tidak dipakai sebagai batas validasi.

Panels/overviews menyimpan frame_index dan scope; role Start/Middle/End normal diturunkan dari posisi panel. Multi area mempunyai label momen opsional yang jelas, serta awal/akhir wajib. ID selection diturunkan dari pointer shot/kelompok/posisi; perubahan urutan memerlukan snapshot baru. Overview menyimpan composition_summary karena menggambarkan frame terpilih yang bisa berbeda dari Camera Start.

Manifest mempunyai frame map untuk union indeks yang dirujuk audit/pilihan bukti, dengan PTS asli; tidak memuat seluruh frame video. Media metadata menunjuk selection ID dan bbox, bukan menyalin seluruh selection/fakta berulang. Baseline/viewed provenance tetap teknis dalam manifest, sementara path cache/session/performance tidak masuk paket.

Alternatif menyimpan ID, shot_id, frame_index dan timestamp di setiap selection audit ditolak karena duplikasi mekanis. Evidence tanpa scope/PTS juga ditolak karena melemahkan pembacaan dan verifikasi.

### 4. Satu notasi fase dan satu sumber tempo

shot.camera.phases berisi interval, notation, depth_direction, area_ids bila berbeda dari scope shot, focus, evidence bersama, observations {depth,translation,rotation}, confidence/note opsional. Observations berupa pengamatan singkat spesifik sumbu, bukan verdict berulang.

Component-specific overrides hanya bila bukti/ambiguitas berbeda, menggunakan indeks komponen hasil parse notation. Ketiganya bukan salinan wajib motion_observations. Estimasi tetap dalam notation; pengukuran/helper numerik detail tinggal workspace. Bukti gerak memerlukan setidaknya dua frame temporal berbeda dalam fase/toleransi batas satu native yang terdokumentasi; satu frame tidak membuktikan gerak.

Parser mandiri mempertahankan raw, gerak, arah, qualifier, estimate dan toward sebagai output turunan. Fase input tidak memakai → di dalam notation; summary menggabungkan fase dengan →. Depth_direction tetap auditor, diperiksa terhadap Dolly eksplisit. Angka tunggal/rentang/tanpa angka diterima, asumsi visual sah, tanpa kewajiban alasan ketiadaan angka atau confidence downgrade.

camera.tempo memakai salah satu bentuk: {label,description} untuk seragam atau {segments:[{start_s,end_s,label,description}],description} untuk berubah. Segmen menutup shot tanpa gap/overlap; label fase/shot turunan dihitung dari overlap. Tidak ada phase.tempo, rhythm dan tempo_profile paralel. Tempo perubahan boleh memotong fase; easing komponen tetap berbeda dari tempo keseluruhan. speed_change pengamatan disimpan hanya jika memang menambah informasi yang tidak terwakili qualifier.

Alternatif memperluas JSON ringkas kembali ke struktur 2.5 ditolak. Alternatif menyatukan batas tempo dengan batas fase ditolak karena menghasilkan fase palsu.

### 5. Derivasi murni dan graph modul tanpa legacy

~~~text
common + konstanta + schemas
    → camera_notation / camera_pattern / render_assets
    → models + audit_quality + derivations
    → authoring/preflight + media/reporting
    → exporter/validation
    → engine/generation/reader + CLI
~~~

Panah menunjukkan dependensi konseptual; pisahkan utility agar tidak membuat import cycle media↔cache atau validation↔generation. derivations.py menghasilkan summary, parsed components, ID/scope/tempo overlap dan mapping profil/facet hanya saat dibutuhkan. Ia tidak membuat model expanded lengkap kedua atau menulis kembali data turunan ke audit.

media.py menjadi implementasi media tunggal berdasarkan perilaku media terbaru, termasuk crop panel. reporting.py menjadi renderer MD tunggal; helper font/path/wrap/angka dipindahkan ke render_assets.py. Ekstraktor kanonis dan batch cache tetap dipakai. media_incremental memakai fungsi aktif dan wajib byte-identik dengan render penuh pada konfigurasi sama.

Schema validation tersedia offline dan tidak mengimpor generator. Preflight mengembalikan konteks probe/hash/PTS yang dipakai draft dalam pemanggilan sama; cache lintas pemanggilan tetap terikat sumber/runtime/config. Complete hanya normalisasi eksplisit dan metadata yang memang menjadi sumber, bukan mematerialisasi field terhapus.

Alternatif sekadar rename modul lama atau membuat facade di atas semua modul versi lama ditolak: hasil akhir harus hanya satu implementasi.

### 6. Authoring bertahap dan snapshot utuh

Prepare membuat satu skeleton audit ringkas dan workspace terikat source/cuts, baseline 6 FPS/native boundaries serta midpoint normal. mark-viewed tetap deklarasi eksplisit sesudah pemeriksaan. Add-pass tidak menandai gambar dilihat.

update-shot menerima session, shot-id dan patch JSON melalui file terstruktur; menggabungkan hanya field yang diizinkan dalam satu shot lalu menulis audit.json atomik. Metadata waktu/ID sumber yang dikunci helper dan field turunan tidak boleh disisipkan oleh patch. Perubahan area global dilakukan eksplisit pada sumber, tidak disimpulkan patch. Patch hanya alat kerja sementara, bukan format sumber kedua.

Complete lalu check-input/draft menyediakan error field terarah tanpa JPEG untuk input invalid. Draft membuat kandidat pada staging dan mengganti hanya kandidat terkelola setelah valid. Report/template, seluruh media dan manifest termasuk snapshot. Receipt terpisah tidak mengandung persetujuan tersirat; pengguna menilai isi di chat. Export memvalidasi snapshot dan membungkus byte sama tanpa probe/decode/render ulang yang tidak diperlukan.

ZIP allowlist ketat: folder ID berisi audit.json, analysis.md, manifest.json, media/shot-NN.jpg, media/overview.jpg, media/storyboard.jpg. Semua video dan file lain ditolak, juga path bersarang/casing/symlink. Ingest tetap memverifikasi MP4 kanonis/hash, validitas provenance dan revisi; tidak meminta review isi baru.

Alternatif membuat builder khusus per video atau banyak file authoring permanen ditolak karena menambah beban dan sumber konflik.

### 7. Report/media tetap lengkap, bukan desain ulang tampilan

Template analysis.md mempertahankan enam bagian dan A/B/C. Profil/ukuran membaca field sumber tunggal; Timeline summary/pattern mekanis; detail area memakai text lengkap, kamera Indonesia dari camera.description dan teknis dari fase. Narasi tidak disintesis ulang. Ketiadaan confidence tidak menambah disclaimer baru di MD.

Layout media.json menyalin perilaku tata letak terbaru yang disetujui: judul/area tebal, ukuran judul terkendali, waktu shot di header tanpa baris Start/Middle/End tambahan, caption bawah label tebal dan waktu lebih kecil. Overview satu baris; Storyboard kolase vertikal dengan identitas ID–gaya–durasi–jumlah shot. Normal tiga panel, multi dinamis; overflow dipreflight dengan scale/kolom eksplisit, bukan crop/pemangkasan detail diam-diam.

Simpan golden terbaru normal/multi dengan nama netral sebelum menghapus golden lama; bandingkan isi/render pada fixture yang ekuivalen dan lakukan inspeksi visual preview. Ini mempertahankan tampilan, bukan dukungan renderer lama.

### 8. Generator dan reader langsung memakai sumber baru

Generator menelusuri styles/size/features dan facts nested, menghasilkan facet eksplisit dari field/aspect/facet_roles, bukan narasi. sources/fact-facets.json tidak diperlukan untuk format baru. Relasi gaya/area dipertahankan hanya jika dinyatakan; label baru tidak diberi alias otomatis.

Proyeksi AI merupakan hasil generator dengan sumber ringkas, turunan terpilih dan provenance JSON Pointer ke audit/manifest. Indeks menyimpan facet/ringkasan/locator untuk discovery; pemeriksaan tiga sumbu, log dan flow detail tidak disalin ke indeks. Mapping/pointer diuji untuk setiap kelompok field dan setiap revisi.

Read/search/panel/shot-image memvalidasi snapshot/proyeksi/aset tersimpan tanpa probe MP4; --native tetap membutuhkan MP4 eksplisit. Build/check/ingest memerlukan MP4 untuk verifikasi sumber. Prinsip kurasi tidak dicampur dengan fakta video.

Pertahankan lock/staging/rollback/recovery, batching revisi, replay unchanged dan output stale removal, termasuk saat registry kosong. Capacity fixture 300 model hanya di root terisolasi, bukan referensi aktif.

Alternatif mempertahankan model/proyeksi legacy sebagai perantara ditolak karena memelihara bentuk panjang kedua dan pointer palsu ke field yang telah dihapus.

### 9. Statistik helper ringkas dengan komposisi yang benar

motion-hints default mengembalikan summary, coverage/gap dan interval bermasalah; --details menambahkan interval lengkap. Simpan matriks transform interval di cache kerja, komposisikan pada koordinat konsisten untuk mengukur cumulative scale dan displacement titik acuan. Jangan menjumlah dx/dy ketika scale/rotation ikut berubah.

Tracking gagal memutus rantai. Laporkan per rentang kontinu; total seluruh shot null bila tidak terbukti. Tren awal–tengah–akhir mengikuti PTS, bukan jumlah interval, dengan gap tetap tampak. Statistik zona atas/bawah diberi label zona gambar, bukan kedalaman fisik. Cache key mencakup source/PTS/indices/width/backend/runtime.

Pertahankan default 32 frame helper, width 320/batas 640, bounded tracking/cache dan fallback unavailable tanpa OpenCV/NumPy. Detail helper tidak mengubah viewed/audit atau masuk ZIP/knowledge. Tidak ada verdict otomatis.

Alternatif menjumlah interval 2D mentah atau menjadikan helper wajib ditolak karena menyesatkan dan menambah beban audit.

### 10. Kit dan dokumentasi tidak bergantung docs/OpenSpec

Kit tetap empat file input dan memulihkan inventaris aktif eksplisit, termasuk import transitif/schema/font/lisensi/template/layout/panduan yang diperlukan; tanpa wildcard historis. Bootstrap offline berhash. Contoh normal/multi dinyatakan sintetis; hasil pilot/ground-truth tidak disisipkan.

Panduan aktif: audit/README, visual-audit, authoring, json-guide, camera-cases, vocabulary, prompts dan contracts. Gabungkan isi aktif protocol/rubric/providers/calibration lalu hapus file yang berulang. Pindahkan alur konsep/capability ke audit/concept-workflow.md dan arahkan provenance prinsip ke sana; dokumen ini tidak perlu membebani kit audit jika tidak digunakan auditor.

README/AGENTS/references entry point tidak lagi menjadikan plan historis sebagai instruksi. Fingerprint/runtime/CI membaca schemas/, tools/assets/, sources dan taxonomy; bukan docs/ atau openspec/. OpenSpec tetap rumah perencanaan, bukan dependency paket produksi.

Alternatif memindahkan plan panjang ke panduan runtime ditolak: aturan aktif harus pendek, bertahap dan konsisten.

### 11. Peta perubahan file

| Tindakan | File/kelompok | Tujuan |
| --- | --- | --- |
| Tambah | schemas/{audit,audit-info,manifest,reference-reader,search-index}.schema.json | Satu kontrak offline per dokumen |
| Tambah | tools/homeku/{derivations,render_assets}.py | Utility aktif yang dipakai bersama |
| Tambah | audit/contracts/{package,report,reader}.md; audit/concept-workflow.md | Kontrak/alur aktif di luar docs |
| Tambah | tests/test_repository_integrity.py | Import/schema/kit tanpa legacy atau planning docs |
| Tambah saat implementasi | docs/implementation-verification-single-version.md | Catatan hasil nyata, bukan input runtime |
| Ubah | tools/homeku/__init__.py, models.py, audit_quality.py, preflight.py | Konstanta, schema/scope/status dan quality checks baru |
| Satukan | media.py, reporting.py, report_validation.py | Renderer/report/media aktif tunggal |
| Ubah | camera_notation.py, camera_pattern.py | Parser mandiri, notasi fleksibel, pointer baru |
| Ubah | authoring.py, audit_session.py, exporter.py, validation.py | Sumber ringkas, update-shot, snapshot dan ZIP |
| Ubah | video.py, video_cache.py, media_incremental.py, audit_performance.py | Cabut import lama, cache/parity/retry/telemetri |
| Ubah | motion_analysis.py | Ringkasan transform/coverage tanpa verdict |
| Ubah | generation.py, reader.py, engine.py | Pointer/facet baru, empty/revision/replay/provenance |
| Telaah, ubah seperlunya | common.py, storage.py, actions.py, tools/publish_actions.py | Pertahankan primitives dan publikasi Git yang benar |
| Ubah | tools/audit.py, library.py, build_audit_kit.py, benchmark_audit.py, make_test_packages.py | CLI tunggal, kit, benchmark dan fixture |
| Ubah | audit/template-audit.json, template-audit-info.json, examples/{normal,multi}/audit.json | Template minimal dan contoh lengkap |
| Ubah | audit panduan/prompts, README.md, AGENTS.md, references/README.md, audit/pilots/README.md | Aturan konsisten dan status nyata |
| Ubah | sources/design-principles.json, data/taxonomy.json bila perlu | Pointer aktif; tidak menebak fakta/alias |
| Ubah | tests/fixtures/factory.py, README.md, tests/*.py | Factory aktif tunggal dan port skenario penting |
| Ubah | .github/workflows/{library-ci,library-ingest}.yml | Path schema/aset baru; helper opsional tetap diuji |
| Telaah | requirements.txt, requirements-audit-motion.txt | Dependensi inti/opsional yang dipakai |
| Ganti nama aset | tools/assets/templates/analysis.md, layouts/media.json | Isi tampilan terbaru, path netral |
| Bangun ulang | audit/homeku-audit-kit.zip; catalogs/; knowledge/; data/{projections,search-index.json,dependencies.json,build.json} | Hanya melalui generator resmi |

Hapus setelah semua pemakai dipindahkan: versions.py, markdown.py, media_v*.py, reporting_v*.py, template/layout versi lama, docs/contracts/, audit/template-analysis.md dan sources/fact-facets.json. Hapus test_v2_1_compatibility setelah memindahkan skenario produk yang masih penting. Rename/konsolidasikan test_v2_models/media/reader/reporting ke nama fungsi netral. Hapus golden lama dan fixture ZIP legacy yang memuat video; factory format aktif menghasilkan MP4 fixture terpisah. Tidak menyimpan versi lama di archive kode.

## Risks / Trade-offs

- [Ringkas menjadi kehilangan pengetahuan] → Matrikkan seluruh kemampuan/field yang dipertahankan, uji fakta/negasi/scope dan golden laporan; tidak menetapkan kuota fakta.
- [Pengamatan kamera berubah menjadi boilerplate] → Tiga observasi tetap spesifik fase dengan bukti viewed; kesalahan isi dikoreksi pada sistem/panduan dan pilot, bukan ditutup validator struktural.
- [Duplikasi berpindah seluruhnya ke manifest] → Manifest hanya metadata/provenance teknis; ukur total audit + manifest + kit pada informasi setara.
- [Penghapusan legacy memutus import tersembunyi] → Pindahkan helper dahulu, cek graph/import cycle dan jalankan workflow kit tanpa checkout/docs.
- [Evidence pointer berubah setelah reorder] → Pointer selalu terikat revisi/snapshot; regenerasi seluruh turunan dan receipt saat sumber berubah.
- [Agregasi flow menyesatkan] → Komposisi transform pada satu koordinat, rangkaian valid terpisah, total null saat gap; tidak menghasilkan pose fisik/verdict.
- [Tidak ada kompatibilitas lama] → Pengguna memilih audit ulang selama pilot; pesan penolakan jelas, tidak mengubah paket lama.
- [Benchmark dianggap jaminan durasi chat] → Catat waktu alat/fixture dan versi lingkungan; run provider/approval/export/ingest tetap status berbeda.

## Migration Plan

1. Pastikan registry dan incoming masih kosong sebelum cutover; bila state berubah, jangan menghapus/mengonversi referensi baru secara diam-diam.
2. Catat baseline struktur/ukuran dan hash data yang dipertahankan; simpan acuan tampilan terbaru. Buat schema/utility baru lalu port pemakai berurutan.
3. Selesaikan model/authoring, report/media, pipeline paket, generator/reader dan helper sebelum menyingkirkan dependensi yang masih dipakai.
4. Alihkan CLI, panduan, kit, fixture dan CI. Hapus semua modul/cabang/aset legacy dari hasil akhir.
5. Jalankan matriks tes perilaku, kit standalone, salinan tanpa docs/OpenSpec, helper inti/opsional, root kosong, revisi dan kapasitas. Build ulang hanya keluaran generator.
6. Publikasikan catatan verifikasi dan daftar panduan aktif; dokumen historis tetap pilihan pengguna. Jangan memasukkan fixture/pilot lama ke registry.
7. Serahkan kit final untuk tujuh pilot: edh001, edh058, edh013, edh033, edh049, edh056, dreamshome01. edh001 baru r0001/supersedes null; run lama tidak dimigrasi. Audit nyata memerlukan permintaan/run terpisah.

Rollback pengembangan memakai state Git sebelumnya sebagai satu kesatuan tooling/aset/keluaran, bukan menambah runtime lama ke versi akhir. Jangan push/release tanpa instruksi pengguna. Setelah referensi 3.0 diterima, rollback tidak boleh mengubah/menghapusnya; simpan snapshot paketnya dan pulihkan tooling yang cocok secara eksplisit.

## Acceptance and verification

Syarat selesai mengikuti kelima specs. Jalankan tes terarah selama porting, lalu suite lengkap sesudah integrasi. Verifikasi golden normal/multi dan preview visual; bukti pointer/media offline; rejection format lama; keamanan ZIP/hash; batch/resume/cache parity; lock/rollback/concurrency/Git lokal; 300 fixture serta hasil full/incremental sama.

Ukur JSON pretty/compact, metadata berulang, total paket dan kit/resource; prepare cold/resume, complete/preflight, draft cold/warm/koreksi, helper off/on. Pakai informasi fixture setara dan versi lingkungan tercatat; tidak memalsukan input provider menjadi audit baru atau menjanjikan persentase/menit sebelum pengukuran.

~~~sh
python -m unittest discover -s tests -t . -v
python tools/library.py build
python tools/library.py check
python tools/build_audit_kit.py
python tools/build_audit_kit.py --check
git diff --check
~~~

Panduan pilot siap tidak sama dengan pilot selesai. Tidak ada open question material yang ditunda untuk mengubah scope/spec; detail internal yang tidak mengubah kontrak dapat dipilih selama apply.
