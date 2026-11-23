# Panduan pengisian audit.json 2.3

Gunakan template-audit.json untuk isi dan template-audit-info.json untuk metadata proses. Semua placeholder waktu/indeks/luas dan {{penanda}} harus diisi sebelum draft. Null yang sah (depth_direction ambigu, model_build tidak diketahui, atau metadata komponen yang tidak berlaku) dipertahankan sesuai bukti; jangan mengarang nilai untuk menghapus null. Setelah kit diekstrak, `template-audit.json` dan `template-audit-info.json` berada di root workspace; salin sebagai work/audit.json dan work/audit-info.json, lalu isi. Template bukan audit valid; jangan mengisinya dengan fakta contoh Willow Cottage atau nilai default ruangan.

## Siapa menulis apa

AI auditor menulis identitas/gaya, estimasi ukuran, narasi, klaim/status/bukti, interval shot/area/fase/tempo, komposisi, kamera sederhana/teknis dan pilihan panel. Helper menghitung metadata/hash/PTS, durasi tampilan, MD, layout/font, inventaris gambar dan snapshot. Ingest hanya memvalidasi serta membangun turunan.

| Bidang sumber | Cara mengisi |
| --- | --- |
| schema_version/id/revision | 2.3; ID mengikuti stem MP4; r1 untuk sumber baru, +1 dengan supersedes yang benar untuk revisi aktif |
| identity | Nama rumah deskriptif; primary_style, nama influences dan interior_style bahasa Inggris. style_names_language=en; penjelasan boleh Indonesia. Ciri, palet, suasana/lingkungan konkret. style_relations hanya family/blend/influence yang dinyatakan, bukan alias rekaan |
| size | scale/massing/vertical/footprint/proportions dan floor_area_m2 min/max positif berurutan. Estimasi luas lantai total rumah wajib diisi; basis/uncertainty hanya JSON, tampilan cukup 60–90 m² sebagai contoh format |
| profile | Seluruh aspek DNA kontrak ditulis eksplisit dengan id/aspect/value/state/confidence/evidence/area_ids/basis/uncertainty. Tambahkan interior-style dan nilai pengaruh diskret agar mudah dicari. Unknown bila belum diketahui; jangan menebak material fisik |
| areas | ID area fisik, label, functions dan visible_intervals waktu video. Bathroom + laundry dapat satu area/two functions; dua bathroom fisik mempunyai ID berbeda. Interval boleh overlap antararea dan berulang untuk area yang muncul kembali |
| shots | Satu take sampai cut nyata. start_s/end_s menutup durasi stream video tanpa gap/overlap. transition/continuity berdasarkan sumber; jangan membuat cut dari pergantian area |
| shots.route/area_relations | Rute kamera yang benar-benar dimasuki, penghubung/fokus dan interval. Area terlihat tidak sama dengan dilalui; route boleh kosong untuk pandangan beberapa area dari satu posisi. Hubungan memakai status/bukti |
| shots.design | architecture/furnishings/environment berupa paragraf konkret; area_ids mengikat tiap uraian. Semua area penting harus tercakup. Jangan mengisi inventaris generik atau memastikan yang tertutup |
| shots.facts | Klaim atomik id/domain/subject/attribute/value dengan area_ids, state/confidence/evidence/basis/uncertainty. Konfigurasi, orientasi, bukaan dan penyimpanan lebih berguna daripada warna saja. Label baru dan negasi tetap disimpan |
| composition | camera_position/direction/view_angle/height/tilt, foreground/depth/reveal, start/end_composition, motion_compatibility, focus/lighting. Posisi awal bukan otomatis frame overview akhir OUT |
| camera_summary/phases | Summary sama dengan urutan components fase. + simultan, → berurutan; phase-01 dst. mencakup shot tanpa gap/overlap. Komponen raw/parsed harus sama; gunakan helper component bila perlu. Simpan anchor, focus/area_ids, tempo, speed_change, basis/evidence/confidence/uncertainty |
| camera_simple/rhythm | Narasi Indonesia lengkap tetapi singkat untuk semua arah, kebersamaan/urutan, target dan ritme. Ditulis auditor; renderer tidak menerjemahkan notasi |
| tempo_profile | Interval tempo aktual sepanjang shot, misalnya moderate lalu fast. Perubahan tempo tidak otomatis fase kamera baru; ~2× adalah perubahan skala, bukan kecepatan |
| journey_dna | Wajib untuk multi area: lintasan, penghubung, peralihan fokus/reveal dan ritme. Normal boleh kosong bila tidak menambah penjelasan |
| panels/overviews | ID unik global, shot/area_ids, frame_index/PTS tepat dari inspect, role/label/reason. Normal tiga panel start/middle/end; tengah native terdekat titik tengah. Multi dinamis, awal/akhir dan momen penting. Overview tiap area biasanya awal IN/akhir OUT, boleh bukan panel kolase, tersusun dalam media/overview.jpg, satu baris. Isi composition_summary wajib pada setiap pilihan overview |
| uncertainty/review_summary/composition_notes/camera_notes | Pertahankan batas pengamatan serta penjelasan terkait, jangan menyelipkan status draf/final ke narasi manusia |
| relations/limitations | Hubungan antarshot dan batas keseluruhan yang benar-benar didukung; urutan edit bukan bukti denah atau satu rumah fisik |

## Overview dan arah fase

`shots[].overviews[].composition_summary` adalah satu paragraf biasa tanpa `>` atau Enter. Setelah melihat frame terpilih, jelaskan posisi kamera, arah pandang, sudut, ketinggian/kemiringan, cakupan wide, penempatan elemen, kedalaman dan pencahayaan. Ringkas dan konkret, bukan inventaris furnitur berulang. Judul Shot/Area/waktu dan blockquote ditambahkan renderer. Ini menjelaskan frame overview terpilih; `shots[].composition` selalu menjelaskan **awal shot sumber**, sehingga overview akhir OUT dapat berbeda.

`shots[].phases[].depth_direction` wajib: IN (maju), OUT (mundur), NO IN/OUT (tidak ada maju/mundur), atau null bila belum jelas. Gunakan bukti temporal dan komponen translasi yang eksplisit. Pan/orbit/zoom atau skala saja tidak menentukan klasifikasi. Fase Dolly-In eksplisit tidak boleh diberi OUT/NO IN/OUT; fase berlawanan arah harus dipisah. Bila ambigu, perdalam native dan catat batasnya; null bukan NO IN/OUT.

Helper menurunkan Camera Pattern dari fase: arah sama berurutan digabung, arah berubah dipertahankan, fase netral tidak menambah arah bila sudah ada IN/OUT. Orbit netral lalu Dolly-In menghasilkan IN. Fase ambigu membuat pola shot null (tampilan —). Antarshot memakai ` – `; pola campuran diberi kurung, misalnya IN – (OUT → IN) – NO IN/OUT. Jangan menambahkan camera_pattern manual ke audit.json.

Camera summary, components fase dan notasi raw ditulis satu paragraf; tidak ada Enter setelah → atau +. ~× adalah perubahan skala, bukan kecepatan. Native PTS tetap presisi penuh; tampilan memakai dua desimal.

## Status dan bukti

State: observed, uncertain, not-visible, not-present, unknown. Confidence: high, medium, low, unknown. Not-visible berarti tidak terlihat dalam bukti, bukan tidak ada. Selain unknown, klaim memerlukan bukti; uncertainty dan negasi tidak dihilangkan demi katalog.

Evidence menunjuk ID pilihan panel/overview, atau `frame:shot-01:42` untuk frame native yang tidak masuk kolase. ID bukti harus benar dan dalam shot/scope yang sesuai. Satu fase lintas area boleh memakai gabungan beberapa panel; tidak harus semua area terlihat dalam satu foto. Simpan bukti temporal sumber, bukan hanya tiga gambar final. Jangan memakai path frame kerja sementara.

## Metadata proses

Audit-info berisi method, limitations cakupan, ai provider/model/model_build yang diketahui, reviewed_ranges dan frame_reviews. created_at opsional dihitung helper saat draft. Model/build tidak diketahui tidak dikarang; model_build null. Gunakan sampling.json sebagai template record; isi viewed_frame_indices hanya setelah frame benar-benar dilihat. Baseline 6 FPS seluruh shot wajib selesai; pendalaman10FPS/native ditambah sebagai record baru. Ekstraksi otomatis tidak boleh dianggap pemeriksaan otomatis.

Simpan sumber audit JSON, MP4 dan metadata kerja di luar kandidat. Koreksi JSON/log lalu draft dan review ulang. MD/media/manifest adalah hasil; jangan merawat fakta manual kedua atau memodifikasi hasil sesudah persetujuan. Receipt review mengikat seluruh kandidat, bukan hanya MD.

## Render dan pemeriksaan final

Sumber/paket2.3 → report2.2.2/media2.2.0. Helper menghasilkan laporan enam bagian: Profil desain, Ukuran & proporsi, Shot Timeline, Overview, Storyboard, Shot Details. Timeline lima kolom memakai Camera Movement teknis; Tempo tetap di detail. A/B/C dan subjudul multi area bold; Overview dan kategori desain A memakai blockquote. Kamera regular satu paragraf. Nama gaya utama dan luas bold, tanpa catatan dasar/kepastian pada MD.

Inventaris tepat N+2 JPEG: media/shot-NN.jpg per take kontinu, media/overview.jpg satu baris, media/storyboard.jpg seluruh kolase vertikal. Kolase normal tiga panel, multi area dinamis dan kronologis. Semua foto native mempertahankan konteks/rasio; hanya camera: bold pada baris kamera, caption regular. Tidak ada JPEG overview lepas per shot atau motion/.

Default quality91, scale1, columns4. Bila batas media dilampaui, pilih --quality (60–98), --scale, --overview-scale, --storyboard-scale (0,1], --columns (1–6) secara eksplisit, lalu draft/review ulang lengkap. Jangan mengecilkan font/membuang panel/membagi file diam-diam. Tampilkan Overview, Storyboard, seluruh kolase dan MD sebelum pengguna menyetujui snapshot terakhir. Export memakai receipt di luar kandidat dan tidak merender ulang.


## Pengisian sumber 2.3

Aturan wajib: [protocol.md](protocol.md). Gunakan template JSON terbaru; jangan mengonversi hasil lama tanpa revisi eksplisit.

- identity.influences: gabungan value klaim profile style-influence observed/uncertain, urutan sama, pemisah "; "; unknown bila belum diketahui. Setiap klaim hanya satu nama English. primary_style dan interior_style cocok klaim primary-style/interior-style.
- size.scale: tiny/small/medium/large/unknown. Nilai unknown harus berstatus unknown pada profil; rentang floor_area_m2 min/max tetap wajib.
- shots[].design[].fact_coverage: objek architecture/furnishings/environment. Setiap kategori mempunyai state, fact_ids, basis. mapped memakai ID fakta shot yang mencakup area desain. not-visible/unknown tidak memakai fact_ids dan basis menjelaskan batas yang nyata.
- shots[].phases[].motion_observations: tepat satu objek per component_index (indeks mulai0 menurut components_parsed). evidence memakai ID pilihan atau frame:shot-NN:index yang benar-benar viewed, juga terdaftar di evidence fase. basis menjelaskan perspektif/paralaks/oklusi/jangkar. estimate_basis wajib untuk angka ~×/~°. alternatives berisi penjelasan bila low/unknown/Uncertain; selain itu boleh null.
- Tiap gerakan memerlukan ≥2 frame berbeda dalam fase atau batas satu interval native, setidaknya satu berada dalam fase. Jika tidak cukup, periksa ulang atau pertahankan ambigu; jangan mengarang gerakan/angka/bukti.
- phase.tempo sama dengan label tempo_profile yang overlap bila seragam; variable jika berubah. unknown tidak diubah menjadi moderate. Periksa penjelasan manusia secara visual.
- Paragraf yang ditampilkan MD harus polos satu paragraf; tidak berisi heading/tabel/code fence/HTML. Semantik MD dan label tidak ditulis manual.
- review/export membutuhkan --source /path/<id>.mp4 ketika sumber tidak ada di repo workspace. Jangan gunakan --include-source: paket2.3 tanpa video. Sebelum ingest lokal, MP4 asli harus ada di video/<id>.mp4 dan sesuai hash.

## Tambahan sumber2.3

- phases[].camera_checks: depth, translation, rotation; tiap objek {evidence:[ID1,ID2], basis:"pengamatan khusus sumbu"}. Minimal dua frame fisik berbeda pada fase/toleransi batas satu native, juga masuk evidence fase dan viewed. Tidak menyalin verdict; source simpulan tetap depth_direction/components_parsed.
- motion_observations[].scale_measurement: null bila tidak ada ~×; jika ada angka wajib {anchor,dimension:"width" atau "height",start_evidence,end_evidence,start_px,end_px}. Piksel resolusi sumber, objek/bagian sama terlihat utuh, evidence berurutan dari observasi. IN=akhir/awal; OUT=awal/akhir; >1. Tulis ~2.0× atau ~1.8–2.2× sesuai hasil, bukan angka presisi berlebihan atau faktor kecepatan.
- Pan/Orbit dan Dolly/Zoom: estimate_basis wajib baik saat angka ada maupun belum terpisahkan; jelaskan kendala khusus jika tidak ada angka. Jangan menggandakan rasio total pada Dolly+Zoom simultan yang tidak terpisahkan. Gerakan lain tidak dipaksa angka tidak relevan.
- facts[].facet_roles: peran filter struktur eksplisit seperti opening, roof, massing, layout, configuration, circulation; label baru boleh slug. Kosong [] untuk fakta nonstruktural. attribute/value asli dan state/negasi tetap disimpan.
- Baseline2.3=6FPS; sumber≤6FPS atau shot<1detik seluruh native. Sampling lebih rendah hanya tambahan. Log pendalaman10FPS/native menyebut pertanyaan visual; alasan tidak kosong.
- Semua shot moderate/constant sah. Jangan menyatakan accelerating dari perspektif saja atau memaksa variasi label.
- Kompatibilitas: sumber2.2 tetap10FPS/native/report2.2.1; data baru tidak disisipkan ke sumber lama. Baca kontrak package-v2-3.md setelah pengamatan; metode inti di visual-audit.md.
