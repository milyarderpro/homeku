# Panduan pengisian audit.json V2

Gunakan template-audit.json untuk isi dan template-audit-info.json untuk metadata proses. Semua null numerik dan {{penanda}} pada template harus diganti sebelum draft final. Setelah kit diekstrak, `template-audit.json` dan `template-audit-info.json` berada di root workspace; salin sebagai work/audit.json dan work/audit-info.json, lalu isi. Template bukan audit valid; jangan mengisinya dengan fakta contoh Willow Cottage atau nilai default ruangan.

## Siapa menulis apa

AI auditor menulis identitas/gaya, estimasi ukuran, narasi, klaim/status/bukti, interval shot/area/fase/tempo, komposisi, kamera sederhana/teknis dan pilihan panel. Helper menghitung metadata/hash/PTS, durasi tampilan, MD, layout/font, inventaris gambar dan snapshot. Ingest hanya memvalidasi serta membangun turunan.

| Bidang sumber | Cara mengisi |
| --- | --- |
| schema_version/id/revision | 2.0; ID mengikuti stem MP4; r1 untuk sumber baru, +1 dengan supersedes yang benar untuk revisi aktif |
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
| panels/overviews | ID unik global, shot/area_ids, frame_index/PTS tepat dari inspect, role/label/reason. Normal tiga panel start/middle/end; tengah native terdekat titik tengah. Multi dinamis, awal/akhir dan momen penting. Overview tiap area biasanya awal IN/akhir OUT, boleh bukan panel kolase, tidak menjadi file terpisah |
| uncertainty/review_summary/composition_notes/camera_notes | Pertahankan batas pengamatan serta penjelasan terkait, jangan menyelipkan status draf/final ke narasi manusia |
| relations/limitations | Hubungan antarshot dan batas keseluruhan yang benar-benar didukung; urutan edit bukan bukti denah atau satu rumah fisik |

## Status dan bukti

State: observed, uncertain, not-visible, not-present, unknown. Confidence: high, medium, low, unknown. Not-visible berarti tidak terlihat dalam bukti, bukan tidak ada. Selain unknown, klaim memerlukan bukti; uncertainty dan negasi tidak dihilangkan demi katalog.

Evidence menunjuk ID pilihan panel/overview, atau `frame:shot-01:42` untuk frame native yang tidak masuk kolase. ID bukti harus benar dan dalam shot/scope yang sesuai. Satu fase lintas area boleh memakai gabungan beberapa panel; tidak harus semua area terlihat dalam satu foto. Simpan bukti temporal sumber, bukan hanya tiga gambar final. Jangan memakai path frame kerja sementara.

## Metadata proses

Audit-info berisi method, limitations cakupan, ai provider/model/model_build yang diketahui, reviewed_ranges dan frame_reviews. created_at opsional dihitung helper saat draft. Model/build tidak diketahui tidak dikarang; model_build null. Gunakan sampling.json sebagai template record; isi viewed_frame_indices hanya setelah frame benar-benar dilihat. Baseline 10 FPS seluruh shot wajib selesai; pendalaman native ditambah sebagai record baru. Ekstraksi otomatis tidak boleh dianggap pemeriksaan otomatis.

Simpan sumber audit JSON, MP4 dan metadata kerja di luar kandidat. Koreksi JSON/log lalu draft dan review ulang. MD/media/manifest adalah hasil; jangan merawat fakta manual kedua atau memodifikasi hasil sesudah persetujuan. Receipt review mengikat seluruh kandidat, bukan hanya MD.
