# Pemetaan data V2 dan kompatibilitas

Fondasi Tahap 1. Sumber baru: audit.json; legacy 1.0/1.1: analysis.md. Metadata teknis tetap manifest. JSON proyeksi adalah hasil build, bukan sumber manual kedua.

| Isi lama | Sumber V2 | Tampilan manusia / AI |
| --- | --- | --- |
| Identitas format/id/revision/title | schema_version/id/revision; identity.name | Judul manusia; metadata versi/revisi di JSON |
| Ringkasan, profil dan palet naratif | identity (nama/gaya utama/pengaruh/interior/ciri/palet/suasana) | Bagian 1; seluruh narasi tersedia dalam proyeksi |
| profile klaim seluruh aspek 1.1 | profile: id/aspect/value/state/confidence/evidence + area_ids/basis/uncertainty | Gaya/identitas tampil ringkas; klaim lengkap untuk AI |
| Skala/massa/tingkat eksplisit | size: scale/massing/vertical/footprint/proportions | Bagian 2; estimasi luas wajib min/max m², basis/uncertainty JSON saja |
| Cakupan/method/limitations | manifest.audit; limitations sumber audit | Metadata teknis, tidak memenuhi laporan dengan tabel proses |
| Timeline & timeline_notes | shots start_s/end_s/transition/continuity; timeline_notes | Bagian 3; durasi dihitung dari interval, bukan default produksi |
| Fungsi di timeline | areas: ID fisik/label/functions/visible_intervals; shots.area_ids | Fungsi tidak dianggap area fisik/cut baru |
| Hubungan ruang/perjalanan | shots.route (interval masuk, connector, focus); area_relations berbukti | B pada multi area; area terlihat berbeda dari dilalui |
| Desain dan konfigurasi | shots.design[].area_ids/architecture/furnishings/environment | A per shot, penanda area jika multi; narasi asli ditulis AI |
| Fakta semua domain/atribut baru | shots.facts, ditambah area_ids/basis/uncertainty | Proyeksi/katalog/knowledge; status dan negasi tidak diubah |
| Seluruh composition lama | shots.composition; peran/waktu overview pindah ke overviews.role/timestamp_s/reason; alasan dan overview_exception dipertahankan dalam reason pilihan | B menampilkan fokus, posisi/arah/sudut, framing/cahaya; detail lain tetap AI |
| composition_notes/camera_notes/review_summary | bidang sama pada shot | Tersimpan utuh pada JSON; laporan memakai kategori yang disepakati |
| camera_summary/notasi | shots.camera_summary + phases.components/components_parsed | C; + simultan, → urutan; raw/arah/estimasi diperiksa konsisten |
| Fase/tempo/percepatan/basis/bukti/confidence/uncertainty | shots.phases (semua bidang lama), area_ids/focus | Timeline bila multi/beberapa fase; dasar teknis tetap JSON |
| Gerak mudah dipahami | shots.camera_simple (narasi AI) | Tabel utama dan C dari nilai yang sama, tidak ditebak renderer |
| Perkembangan ritme | shots.rhythm + tempo_profile interval eksplisit | C dan facet semua label tempo; tempo bukan rasio ~× |
| Pola perjalanan | shots.journey_dna | C pada multi; AI mempelajari satu rute penuh |
| Ketidakpastian shot/keseluruhan | shots.uncertainty; audit limitations; basis/uncertainty klaim | Tersimpan lengkap tanpa catatan kepastian tambahan pada luas MD |
| relations antarshot | relations mempertahankan from/to/relation/description/state/confidence/evidence + id/basis/uncertainty | AI; tidak mengarang adjacency/continuity |
| Hubungan nama gaya | identity.style_relations (family/blend/influence, status/bukti/basis) | Pencarian perlu opsi hubungan; bukan alias otomatis |
| Frame awal/tengah/akhir dan overview | shots.panels dan overviews: pilihan semantic ID/frame/PTS/area/label/reason | Satu kolase/shot; storyboard satu baris, tanpa JPEG frame terpisah |
| Media/hash/provenance | manifest.source/audit/render/media, audit_sha256 | Teknis; inventory panel/bbox sekali, klaim memakai ID |
| Link MD legacy | Renderer memakai anchor stabil dan path media deterministik | Bukti V2 lewat ID pilihan atau frame:shot-NN:index; sumber via JSON Pointer |

Legacy tidak dikonversi atau dilengkapi field V2 otomatis. Model bersama mempertahankan bidang lama; reader 2.0 menandai format sumber. `size`/`identity` baru pada read legacy ditampilkan null, bukan angka/gaya rekaan. Tidak dibuat analysis.json yang diedit terpisah.

## Versi dan tanggung jawab

- Kontrak sumber/paket 2.0; renderer/report/media terbaru 2.1.2 (versi terdahulu tetap didukung); reader/index 2.0; generator 3.
- Registry tetap version 1 dengan tambahan contract_version/audit_sha256 per entri V2. Taksonomi version 3 menambahkan slot style_relations terpisah; tidak memasukkan hubungan gaya yang ditebak.
- Auditor menulis seluruh narasi, label, fakta, hubungan, interval shot/area/fase/tempo, estimasi dan pilihan panel. Helper membaca metadata sumber/PTS dan menghitung durasi/layout/hash/MD/snapshot. Ingest hanya memvalidasi serta membangun turunan.
- Koreksi sebelum persetujuan: ubah audit.json/log pemeriksaan aktual, buat kandidat ulang. Setelah persetujuan: export kandidat persis sama. Sesudah ingest: koreksi isi lewat ZIP revisi, bukan edit referensi aktif.
- Fixture sintetis hanya root terisolasi. Tahap 1 tidak mengaudit ulang edh001 atau menjalankan enam pilot pengguna.

## Penyempurnaan tampilan Tahap 1

identity.style_names_language=en menandai nama gaya utama/pengaruh/interior berbahasa Inggris; wajib untuk renderer 2.1.x. Prosa tetap bahasa Indonesia. Header storyboard mengambil identity.primary_style. Caption hanya memformat role/label/waktu sumber; Start/Middle/End tidak mengulang label bebas normal, multi memakai nama momen. Metadata baru bold_font_sha256 mengikat font bold; template dan implementasi media 2.0.0/2.1.0 dibekukan. Kontrak sumber/reader tetap 2.0 dan data diterima tidak dikonversi.

Tampilan 2.1.2 mengembalikan label dan timestamp ke bawah tiap foto; timestamp regular sekitar 75% ukuran label bold. Header kolase hanya judul/rentang/durasi. Ukuran judul tetap 15% lebih kecil daripada 2.1.0. Presisi dan pointer JSON tidak berubah.
