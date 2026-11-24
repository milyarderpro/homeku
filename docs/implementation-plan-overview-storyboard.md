# Plan implementasi — Overview, Storyboard dan laporan HOMEKU

> Status setelah reset 24 November 2026: data audit edh001 telah dihapus atas permintaan pengguna. Catatan edh001 di dokumen ini bersifat historis, bukan referensi aktif atau persetujuan audit baru.

Tanggal: 23 November 2026.

Status: **Tahap 1 dan Tahap 2 implementasi Overview/Storyboard selesai. edh001 r0003/2.1 telah disetujui, diekspor dan di-ingest. Enam pilot pengguna tetap belum dinyatakan selesai.** [Hasil verifikasi dan daftar file aktual](overview-storyboard-verification.md).

Acuan utama: [PRD yang disetujui](prd-overview-storyboard-cloning.md), [template](template-analysis-v2.md), [contoh normal](contoh-analysis-shot-normal.md), dan [contoh multi area](contoh-analysis-shot-multi-area.md). Plan ini merinci pembaruan setelah fondasi V2; pembagian tahap di sini bukan perubahan status tahap pada plan lama.

## 1. Hasil akhir dan batas pekerjaan

**Satu audit.json → laporan manusia enam bagian + Overview + kolase setiap shot + Storyboard → ZIP final → ingest → JSON pembaca, katalog dan knowledge.**

Laporan mengikuti seluruh keputusan terbaru: judul A/B/C bold, detail multi area dikelompokkan per area, blockquote pada Overview dan tiga kategori desain bagian A, bagian B berbentuk poin, bagian C menyimpan penjelasan sederhana/Tempo/Camera. Kamera teknis tetap English dan satu paragraf; informasi rumah tidak dikurangi.

AI dapat membaca JSON serta mengambil foto overview/panel/blok dari media pustaka tanpa membuka MP4. Camera Start tetap awal shot sumber; Overview dapat berada di akhir OUT. Arah, fase dan tempo sumber tidak berubah karena workflow produksi IN lalu reverse.

Pengerjaan dibagi dua tahap berurutan:

1. **Tahap 1 — Pustaka, data, renderer dan pembaca AI.**
2. **Tahap 2 — Workflow GPT/Gemini, kit dan penerapan melalui kandidat edh001 r0003.**

Tidak membuat plugin produksi, benchmark manfaat konsep, percobaan generate gambar/video atau audit ulang penuh otomatis. Referensi aktif hanya registry; archive/oldrepo/ bukan input. Paket pada audit/result/ tidak diperiksa atau di-ingest hanya karena ada di folder tersebut. Perubahan referensi melalui revisi ZIP eksplisit, bukan penyuntingan references/ secara langsung.

## 2. Temuan eksplorasi repo

Baseline berikut dicatat sebelum implementasi. Status akhir: r0003 aktif; lihat hasil verifikasi bagian8.

| Bagian | Kondisi awal | Perubahan yang dibutuhkan |
| --- | --- | --- |
| Sumber aktif | Registry berisi edh001 r0002, kontrak 2.0, lima shot | Pertahankan sampai r0003 lengkap disetujui dan di-ingest |
| Template/contoh | Sudah menampilkan rancangan enam bagian dan blockquote | Jadikan acuan renderer baru; template aktif kit masih versi beku 2.1.2 |
| reporting.py | Memerlukan lima heading dan tiga grup tanpa bold eksplisit; timeline enam kolom | Jalur renderer baru untuk enam bagian, timeline lima kolom, label/bold/blockquote terbaru |
| media.py | 2.1.2; satu kolase/shot dan storyboard overview satu baris | Tambah Overview terpisah dan Storyboard vertikal lengkap, termasuk kamera |
| validation.py | Ekstraksi ZIP belum mengizinkan media/overview.jpg; validasi manifest mengharuskan N+1 media | Izinkan inventaris baru secara versioned: N+2 media; pertahankan validasi paket lama |
| models.py | Memakai schema 2.0; overviews belum mempunyai composition_summary | Tambah dispatch sumber baru, paragraf Overview dan klasifikasi arah yang eksplisit |
| Bukti dan crop | evidence_inventory menyimpan satu lokasi per ID; crop_panel menolak ID yang muncul di lebih dari satu media | Pisahkan identitas bukti dari lokasi penampilannya, dengan pilihan lokasi deterministik |
| Reader/generator | Banyak pemeriksaan langsung == 2.0; indeks overview menunjuk kolase shot | Dukung beberapa versi sumber, pola kamera dan rujukan overview yang tepat |
| Ekspor/registry | Manifest, review/export, penyimpanan hash dan cache masih mengasumsikan 2.0 | Dispatch konsisten dari draft sampai ingest; snapshot lama tetap utuh |
| Kit | Empat file input; runtime/schema/template diinventarisasi eksplisit, panduan dipin ke 2.1.2 | Tambah seluruh dependensi versi baru dan ganti panduan hanya ketika runtime siap |
| Pengujian/CI | Ada tes legacy, renderer lama, snapshot, keamanan ZIP, multi area dan kapasitas 300 model | Pertahankan regresi tersebut dan tambah kasus format baru; CI sudah menjalankan tiga pemeriksaan wajib |

Poin di atas berasal dari pembacaan repo. Penyusunan plan ini bukan klaim menjalankan audit video atau seluruh suite pengujian lagi.

## 3. Keputusan teknis untuk implementasi

### 3.1 Versi dan kompatibilitas

Nomor berikut telah diterapkan pada tooling Tahap 1; referensi aktif edh001 tetap memakai versi paket asal:

| Komponen | Baseline | Diterapkan |
| --- | --- | --- |
| Sumber audit / kontrak paket | 2.0 | **2.1** |
| Laporan / media / template beku | 2.1.2 | **2.2.0**, pasangan sama |
| Proyeksi pembaca / indeks | 2.0 | **2.1**, mendukung sumber 1.0, 1.1, 2.0 dan 2.1 |
| Generator | 3 | **4** |
| Struktur registry | 1 | **Tetap 1**, memperluas nilai contract_version |

Schema sumber/manifest/reader/index baru dibuat terpisah. Paket lama divalidasi menurut versi asal, tidak dilengkapi field baru secara otomatis. Keluaran generator dapat dibangun ulang; audit/MD/media paket diterima tidak ditulis ulang.

Bekukan algoritme laporan lama dan media 2.1.2 sebelum menambah dispatcher. Modul media 2.0.0/2.1.0/2.1.1, template analysis-2.0.0 sampai 2.1.2 serta font yang telah diterima tidak ditimpa. Tes membandingkan hasil renderer dan byte paket lama, bukan sekadar mengganti angka versi pada assertion.

### 3.2 Sumber paragraf dan Camera Pattern

- Tambah **shots[].overviews[].composition_summary**, wajib terisi pada sumber 2.1. Simpan paragraf biasa di JSON; renderer menambahkan markup blockquote, bukan auditor memasukkan tanda `>` ke isi sumber.
- Tambah **shots[].phases[].depth_direction** sebagai klasifikasi auditor: `IN`, `OUT`, `NO IN/OUT`, atau `null` bila belum dapat ditentukan. Nilai null mempertahankan uncertainty/bukti dan tidak diganti NO IN/OUT.
- Fase yang sudah ada menjadi acuan interval/evidence. Jika arah berubah dalam satu fase, auditor memperbaiki pemisahan fase; helper tidak menebak atau memotong fase sendiri.
- Fungsi bersama menurunkan pola per shot dari urutan fase: pertahankan pergantian IN/OUT, gabungkan arah berurutan yang sama, dan jangan menambahkan fase netral ke ringkasan bila shot mempunyai gerak maju/mundur yang jelas. Fase netral tetap tersedia pada timeline lengkap. Seluruh fase netral menghasilkan NO IN/OUT.
- Fase ambigu tidak dihapus demi menghasilkan pola pasti. Pola shot yang belum dapat ditentukan tetap null pada JSON dan memakai `—` pada posisi shot di laporan/gambar, tanpa mengubah status sumber. Paket lama tanpa klasifikasi juga tidak ditebak dari narasi.
- Pola video menyusun tepat satu entri per shot: `IN – (OUT → IN) – NO IN/OUT`. Label gambar memakai hasil fungsi yang sama; kamera lengkap tetap dari camera_summary, fase dan tempo_profile.
- Validator menolak klasifikasi yang jelas berlawanan dengan komponen translasi eksplisit; kasus orbit/pan/zoom tidak ditentukan hanya dari nama atau perubahan ukuran objek. Tidak menambahkan aturan arah di luar protokol audit yang disepakati.

Pola turunan tidak ditulis sebagai salinan manual kedua dalam audit.json. ~× tetap perubahan skala; tempo tetap disimpan terpisah. Komposisi Overview tidak menggantikan shots[].composition untuk Camera Start.

### 3.3 Media, lokasi bukti dan konfigurasi

Inventaris 2.1: **N kolase shot + overview.jpg + storyboard.jpg**. Overview satu baris; Storyboard vertikal berisi seluruh blok kolase; kolase normal tiga panel dan multi area dinamis. Tidak menambah motion/, frame JPEG lepas, klip atau seluruh frame audit.

Identitas selection tetap berasal dari audit.json. Manifest mencatat placement berbasis selection_id beserta bbox foto/skala; blok storyboard mempunyai shot_id, bbox seluruh blok dan hubungan ke kolase asal. Metadata frame/PTS/area tidak menjadi fakta baru pada setiap placement.

Reader 2.1 memakai satu entri bukti per selection_id dengan metadata sumber sekali dan daftar **locations**. Satu panel dapat tampil pada kolase dan storyboard tanpa mengganti ID atau membuat crop gagal. Lokasi utama dipilih dari foto yang tersedia dengan resolusi tertinggi; bila sama, urutan pilihan tetap kolase shot → Overview → Storyboard. Tie-break berikutnya memakai path/koordinat yang stabil. Bukti native yang tidak disimpan sebagai panel tetap memakai MP4 bila diminta secara khusus.

Konfigurasi baru mempertahankan `panel_scale` untuk kolase shot, menambahkan **overview_scale** dan **storyboard_scale** yang eksplisit, masing-masing default 1 dan rentang (0,1]. Storyboard scale berlaku pada blok kolase lengkap; bbox foto/blok dihitung kembali. Tidak ada pembesaran melebihi sumber. Semua nilai efektif masuk manifest dan snapshot.

JPEG quality default 91 (60–98), kolom multi default 4 (1–6). Batas tetap: 60 juta piksel/gambar, sisi maksimal 65.000 px, 95 MiB/file, 256 MiB ZIP dan total ekstraksi, 2.000 file, 2 MiB/file teks. Dimensi diperiksa sebelum alokasi, byte setelah encoding. Jika melampaui batas, kandidat gagal dengan pesan spesifik; perubahan skala/quality/kolom dibuat secara eksplisit sebelum tinjauan final. Tidak menambah halaman/file atau mengurangi shot diam-diam.

Ukuran font/jarak mengambil preview terakhir yang disetujui sebagai baseline tetap, bukan menerapkan pengurangan 12% setiap render. Padding bawah mengikuti teks terakhir; acuan 30 px dan jarak antarblok 60 px mengikuti proporsi kanvas contoh. Hanya `camera:` bold pada baris kamera; isi regular, ukuran sama dengan label start. Waktu/durasi kanan atas mempertahankan ukuran yang telah disetujui.

## 4. Urutan Tahap 1 — Pustaka dan renderer

### 1.1 Catat baseline dan bekukan jalur lama

- [x] Catat hash registry, seluruh file edh001 r0002, ZIP riwayat, template/font dan hasil renderer lama pada workspace verifikasi di luar sumber aktif.
- [x] Bekukan implementasi media 2.1.2 dan renderer laporan lama ke modul terpisah; dispatcher tetap menghasilkan hasil lama yang sama.
- [x] Sediakan fixture sumber/renderer versi eksplisit. Factory lama tetap bisa menghasilkan 2.0 untuk tes regresi.

**Selesai jika:** tidak ada perubahan byte audit/MD/media yang diterima, dan hasil jalur lama tetap sama. Jangan mengganti default baru sebelum jalur lengkap siap.

### 1.2 Tulis kontrak dan schema versi baru

- [x] Buat schema audit/manifest/reader/search-index 2.1 dan dokumen kontrak pendamping; masukkan keputusan §3.
- [x] Definisikan composition_summary, depth_direction, locations, blok Storyboard, batas media, versi dan konfigurasi skala secara eksplisit.
- [x] Pastikan schema membedakan 2.0 dan 2.1; paket tanpa field baru tidak dianggap 2.1 secara diam-diam. Resolusi schema pada kit harus lokal tanpa akses jaringan.
- [x] Perbarui pemetaan field dan tautan navigasi kontrak. Kontrak lama tetap menjelaskan format asalnya.

**Selesai jika:** contoh sumber/manifest 2.1 valid; versi/field/placement tidak cocok ditolak; schema lama tetap menerima paket lama.

### 1.3 Implementasikan model dan pola kamera bersama

- [x] Tambahkan dispatch schema berdasarkan versi audit dan manifest, lalu perluas adapter JSON tanpa mengubah legacy MD parser.
- [x] Validasi paragraf overview, pilihan frame/area/reason, klasifikasi fase dan kesesuaian kamera. Seluruh aturan shot/fungsi/visibility/route/tempo yang ada tetap berlaku.
- [x] Tambahkan modul camera_pattern.py untuk pola shot/video serta label, dengan provenance ke fase sumber. Tidak melakukan sintesis AI.
- [x] Pertahankan semua narasi, atribut/label baru, negasi, uncertainty dan evidence ID; multi area tetap satu take.

**Selesai jika:** pola tunggal, campuran, netral dan ambigu konsisten; fase netral awal + Dolly-In tetap IN; perubahan arah tidak mengubah jumlah shot.

### 1.4 Implementasikan media 2.2.0

- [x] Bangun kolase shot dengan header, caption, kamera satu paragraf dan tinggi otomatis sesuai contoh terakhir. Multi area memilih momen dari data auditor, bukan mengambil lima frame seragam.
- [x] Bangun overview.jpg dari pilihan frame asli, termasuk pilihan yang tidak masuk kolase; normal satu overview area, multi mencakup setiap area penting tanpa membuat shot baru.
- [x] Susun Storyboard dari seluruh blok kolase yang sama, secara vertikal. Jangan membuat layout kedua yang berbeda; catat transform/bbox setiap blok dan foto.
- [x] Preflight semua dimensi/alokasi, tangani teks panjang/kolom terakhir, catat hash/byte aktual. Batasi cache frame/bitmap selama render agar tidak menampung seluruh rangkaian audit.
- [x] Tambah akses crop lokasi bukti yang berulang dan crop blok Storyboard; pertahankan perilaku versi lama.

**Selesai jika:** semua media sesuai inventaris N+2, foto/caption tidak bertumpuk, baris kamera tidak terpotong, margin bawah rapat dan seluruh bbox benar.

### 1.5 Implementasikan laporan manusia 2.2.0

- [x] Buat renderer baru dan template beku analysis-2.2.0.md dari template rancangan terakhir; daftar heading/grup harus mendukung enam bagian dan bold eksplisit.
- [x] Tampilkan Profil desain, Ukuran & proporsi, Shot Timeline, Overview, Storyboard, Shot Details dengan label yang disepakati.
- [x] Tampilkan Overview sebagai judul bold di luar blockquote dan satu paragraf regular di dalamnya.
- [x] Kelompok A memakai blockquote per Arsitektur/Furnitur & dekorasi/Lingkungan; multi dikelompokkan per area. B tetap poin; C narasi/Tempo/Camera, dengan Movement Timeline bila diperlukan.
- [x] Waktu tampilan dua desimal; luas tetap rentang wajib tanpa catatan tambahan. Nama gaya tidak diterjemahkan; isi sumber tidak diringkas otomatis untuk menghapus pengulangan.
- [x] Hilangkan label proses/placeholder dari laporan final, tampilkan kolase pada setiap shot dan pertahankan anchor stabil.

**Selesai jika:** laporan baru sesuai template/contoh, setiap narasi sumber tetap tersedia dan renderer lama tidak berubah.

### 1.6 Integrasikan reader, indeks dan generator

- [x] Perbarui seluruh percabangan sumber == 2.0 menjadi pemeriksaan keluarga/versi yang benar pada models, reader, generation dan engine; hindari perubahan massal tanpa memeriksa perilaku setiap cabang.
- [x] Terbitkan proyeksi/indeks 2.1 serta generator 4. Identity tetap ringan; shot/area berisi paragraf Overview, desain terkait, gerak/tempo, lokasi media dan provenance.
- [x] Pembacaan satu area tetap membawa seluruh route/fase kamera shot. Indeks hanya membawa pola/rujukan ringkas, bukan salinan paragraf/media.
- [x] Perbaiki indeks yang saat ini menyebut kolase shot sebagai overview; gunakan pilihan overview yang benar dan tautan gambar gabungan/blok terkait.
- [x] Panel default memilih lokasi foto terbaik secara deterministik tanpa MP4. Tambah CLI terencana `shot-image <id> <shot-id> --output ...` untuk kolase; `--from-storyboard` mengambil blok lengkap melalui metadata. Ekstraksi tetap ke lokasi sementara di luar repo.
- [x] Perbarui seluruh pemakai inventory/proof_path/media_link dan JSON Pointer untuk bentuk locations; jangan hanya memperbaiki endpoint panel.

**Selesai jika:** koleksi campuran tetap terbaca, semua pointer valid dan foto/blok tersimpan dapat diambil saat MP4 tidak tersedia pada root tes terisolasi. `--native` tetap jalur eksplisit ke MP4.

### 1.7 Integrasikan draft, validasi, review, ekspor dan ingest

- [x] Izinkan overview.jpg pada ekstraksi ZIP yang aman, lalu batasi inventaris sesuai versi manifest. Paket lama tetap N+1 dan paket baru N+2; tidak melonggarkan aturan traversal/symlink/file asing.
- [x] Perluas default/opsi versi dan konfigurasi CLI/helper agar draft 2.1 memakai report/media 2.2.0. Default renderer mengikuti versi sumber: draft 2.0 dari kit lama tetap memakai 2.1.2. Tambah opsi overview/storyboard scale; revisi 2.0 tetap dapat divalidasi/review/export menurut versi asal.
- [x] Validasi seluruh manifest, expected_media, hash, bbox/transform dan analysis.md hasil renderer yang cocok; dokumen hasil tidak boleh diedit manual.
- [x] Perluas registry/audit_sha256, review/export dan cache validation yang masih mengunci 2.0. Registry version tetap 1.
- [x] Pertahankan receipt di luar kandidat, digest seluruh snapshot, export tanpa re-encoding/created_at baru, supersedes tepat dan replay ingest unchanged.
- [x] Perubahan kandidat/config membatalkan receipt lama. Kegagalan satu paket tidak menghalangi paket valid lain; atomic publication/recovery tetap dipakai.

**Selesai jika:** roundtrip ZIP baru, revisi, rollback teknis dan ingest campuran berjalan tanpa review isi tambahan sesudah ingest.

### 1.8 Preview nyata dan verifikasi Tahap 1

- [x] Buat preview layout dengan frame edh001 yang sudah tersedia, tanpa mengganti referensi aktif atau menyatakan audit penuh baru. Preview terpisah dari kandidat final r0003.
- [x] Periksa normal dan fixture multi area, arah campuran/netral/ambigu, notasi panjang, banyak shot, skala berbeda dan batas ukuran. Fixture tidak menjadi knowledge aktif.
- [x] Bandingkan tata letak dengan contoh yang disetujui: font, bold camera saja, waktu kanan atas, caption bawah, margin dinamis, Overview satu baris dan Storyboard vertikal.
- [x] Sinkronkan inventaris RUNTIME kit dengan modul/schema/template baru dan bangun ulang ZIP agar pemeriksaan integritas kit tidak tertinggal oleh perubahan kode. Pada tahap ini panduan/template input tetap menjalankan alur 2.0 yang kompatibel; aktivasi workflow manusia 2.1 dilakukan pada 2.1–2.2. Uji teknis sumber baru memakai fixture eksplisit.
- [x] Catat dimensi/byte setiap media dan ZIP, hasil pemeriksaan dan hash perlindungan paket lama. Jalankan tes terkait selama pengerjaan; suite lengkap dan tiga pemeriksaan wajib pada akhir tahap, setelah kit tersinkron.

**Selesai jika:** preview aktual rapi dan pemeriksaan §7 lolos. Perubahan desain tampilan yang diperlukan dikembalikan ke PRD/contoh sebelum versi baru dibekukan.

## 5. Urutan Tahap 2 — Workflow chat dan penerapan

### 2.1 Selaraskan instruksi audit dan panduan

- [x] Perbarui template-audit.json dengan versi/field baru, serta json-guide/protocol/rubric dan tiga prompt audit/koreksi/ekspor.
- [x] Tegaskan baseline 10 FPS + awal/akhir native dan pendalaman native aktual; pan/orbit memakai paralaks/oklusi/perspektif, jitter kecil bukan tilt. Log viewed hanya untuk frame yang benar-benar dilihat.
- [x] Instruksikan paragraf Overview per frame, Camera Start sumber, depth_direction, detail area lengkap dan notasi/tempo asli. Jangan menyalin fakta contoh atau default slow.
- [x] Koreksi melalui JSON/config → render kandidat lengkap → tampilkan Overview, Storyboard, seluruh kolase dan MD → persetujuan keseluruhan → export snapshot yang sama.
- [x] Perbarui panduan cloning dan konsep baru sesuai DNA; pembalikan seluruh gerak produksi dijelaskan terpisah, tanpa mengubah bekerja/ atau membuat plugin.

**Selesai jika:** prompt, schema, template, perintah helper dan isi laporan menunjuk versi/aturan yang sama.

### 2.2 Bangun kit dan uji workspace kosong

- [x] Tambah semua modul/schema/template/layout baru beserta dispatcher dan dependensi legacy yang dibutuhkan ke RUNTIME; GUIDES menunjuk template beku baru yang benar-benar didukung.
- [x] Pertahankan empat file input kit dan bootstrap lokal berinventaris/hash; source MP4 tetap lampiran terpisah. Jangan memasukkan video/paket hasil audit/fixture ke kit.
- [x] Bangun ulang audit/homeku-audit-kit.zip dan uji pada workspace kosong: bootstrap → inspect/sample fixture → isi JSON sintetis → draft → review → export → validasi/ingest pada root terisolasi.
- [x] Verifikasi ZIP deterministik, tidak mengambil kode/schema dari jaringan, dependensi lengkap dan bootstrap tidak menimpa file pengguna yang berbeda.

**Selesai jika:** pipeline teknis portabel lolos. Tes sintetis bukan klaim audit nyata di GPT/Gemini atau penyelesaian pilot pengguna.

### 2.3 Siapkan kandidat edh001 r0003

- [x] Salin sumber diterima ke workspace kandidat baru; verifikasi source hash dan supersedes memakai registry terkini, bukan nilai rekaan atau revisi tetap bila keadaan berubah.
- [x] Tulis composition_summary dari frame overview terpilih dan lengkapi klasifikasi arah berdasarkan bukti yang ada. Pertahankan fakta, nama gaya, gerak/tempo, pilihan frame serta log r0002; perubahan lain hanya jika koreksi pengguna memerlukannya.
- [x] Catat pemeriksaan tambahan yang benar-benar dilakukan. Render ulang media tidak berarti seluruh frame video diperiksa ulang.
- [x] Buat laporan enam bagian, Overview, Storyboard dan lima kolase. Tampilkan kandidat lengkap dan hasil pemeriksaan byte/layout di chat; references/edh001 tetap r0002.

**Selesai jika:** r0003 lengkap dan reviewable. Belum berarti disetujui atau aktif.

### 2.4 Persetujuan, ekspor dan ingest revisi

**Status selesai:** pengguna menerima keseluruhan kandidat r0003 dengan “ya saya setuju”, tanpa koreksi tambahan. Snapshot yang sama diekspor, ZIP dibuka/validasi ulang dan di-ingest secara eksplisit. Registry aktif r0003; replay unchanged dan rebuild/check lolos. Riwayat ZIP lama dipertahankan; penutupan 2.5 tercatat pada dokumen verifikasi.

- [x] Terapkan koreksi pengguna pada sumber/config, render ulang dan tampilkan kandidat terbaru. Persetujuan satu gerak/tampilan tidak dianggap persetujuan seluruh audit.
- [x] Setelah pengguna menyetujui keseluruhan kandidat terbaru, ekspor snapshot yang sama, buka ulang ZIP dan validasi digest/manifest/MD/media.
- [x] Tempatkan ZIP final pada jalur penyerahan/riwayat, lalu ingest eksplisit paket tersebut setelah diminta/diizinkan; jangan memindai dan mengimpor ZIP lain yang belum menjadi penyerahan.
- [x] Generator memperbarui katalog, knowledge, proyeksi, indeks dan metadata build. Pastikan replay paket sama unchanged dan paket lama tetap tersimpan.

**Selesai jika:** registry menunjuk revisi baru dan semua keluaran sesuai. Tidak ada review isi kedua setelah ingest. Commit/push bukan bagian otomatis langkah ini.

### 2.5 Tutup status dan lanjutkan pilot pengguna

- [x] Simpan verifikasi implementasi baru: versi, perintah/hasil nyata, preview/dimensi/byte, batas yang belum teruji, snapshot yang disetujui dan hasil ingest jika sudah dilakukan.
- [x] Selaraskan README, AGENTS, panduan referensi/operasi, field map serta status PRD/plan V2. Bedakan tooling siap, kandidat tersedia, audit disetujui dan referensi aktif.
- [x] Arahkan enam pilot berikutnya memakai kit baru sesuai daftar audit/pilots/README.md. Catat provider/model/status hanya berdasarkan run nyata; keberadaan ZIP bukan bukti audit selesai atau diterima.

**Selesai jika:** dokumentasi tidak mencampur format lama dengan kemampuan baru; pilot yang belum dibuktikan tetap belum dinyatakan selesai.

## 6. Daftar file baru, diubah dan keluaran otomatis

Nama file baru di bawah adalah target plan. Membuat plan ini tidak membuat seluruh file implementasinya.

### 6.1 File baru

| File target | Tujuan | Urutan |
| --- | --- | --- |
| docs/implementation-plan-overview-storyboard.md | Plan ini | Persiapan |
| docs/contracts/audit-v2-1.schema.json | Sumber audit 2.1 dan field baru | 1.2 |
| docs/contracts/manifest-v2-1.schema.json | Inventaris N+2, konfigurasi dan blok media | 1.2 |
| docs/contracts/reference-reader-v2-1.schema.json | Proyeksi multi versi, pola, locations/provenance | 1.2 |
| docs/contracts/search-index-v2-1.schema.json | Indeks 2.1 yang tetap ringkas | 1.2 |
| docs/contracts/package-v2-1.md | Aturan paket dan kompatibilitas baru | 1.2 |
| docs/contracts/analysis-v2-2.md | Kontrak laporan/media 2.2.0 | 1.2 |
| docs/contracts/ai-reader-v2-1.md | Jalur baca/crop tanpa MP4 dan pola kamera | 1.2 |
| tools/homeku/reporting_v2_legacy.py | Salinan perilaku renderer lama sebelum dispatcher baru | 1.1 |
| tools/homeku/media_v2_1_2.py | Algoritme media 2.1.2 yang dibekukan | 1.1 |
| tools/homeku/camera_pattern.py | Turunan arah shot/video bersama | 1.3 |
| tools/homeku/media_v2_2.py | Layout/render Overview, kolase dan Storyboard baru | 1.4 |
| tools/homeku/reporting_v2_2.py | Laporan manusia enam bagian | 1.5 |
| tools/assets/templates/analysis-2.2.0.md | Template beku renderer baru | 1.5 |
| tools/assets/layouts/media-2.2.0.json | Parameter font/jarak versi baru, ikut fingerprint/kit | 1.4 |
| tests/test_camera_pattern.py | Kasus pola dan konsistensi dengan fase | 1.3 |
| tests/test_v2_1_compatibility.py | Campuran sumber/renderer, bukti berulang dan pipeline revisi | 1.6–1.8 |
| docs/overview-storyboard-verification.md | Hasil nyata implementasi dan preview, ditulis setelah dijalankan | 1.8/2.5 |

### 6.2 File yang diubah

| File | Perubahan | Urutan |
| --- | --- | --- |
| tools/homeku/__init__.py | Daftar versi didukung dan default baru saat integrasi siap | 1.2–1.7 |
| tools/homeku/models.py | Dispatch schema/model, field Overview/arah dan inventory locations | 1.3/1.6 |
| tools/homeku/media.py | Dispatcher versi, expected_media dan pemilihan crop yang benar | 1.4 |
| tools/homeku/reporting.py | Dispatcher/config/hash/renderer baru, jalur lama tetap sama | 1.5 |
| tools/homeku/validation.py | Allowlist ZIP, dispatch kontrak, inventaris/bbox/hash/laporan baru | 1.2/1.7 |
| tools/homeku/exporter.py | Draft/config, review/export multi versi dan snapshot lengkap | 1.7 |
| tools/homeku/engine.py | Registry/ingest mendukung 2.1 dan audit_sha256 | 1.6–1.7 |
| tools/homeku/generation.py | Proyeksi/indeks/pola/provenance, link media, fingerprint/cache | 1.6 |
| tools/homeku/reader.py | Locations, baca sebagian dan ekstraksi tanpa MP4 | 1.6 |
| tools/library.py | CLI shot-image dan akses blok Storyboard | 1.6 |
| tools/audit.py | Versi draft/review/export dan opsi skala media gabungan | 1.7 |
| tests/fixtures/factory.py | Factory versi eksplisit serta kasus 2.1 terisolasi | 1.1–1.8 |
| tests/fixtures/README.md | Dokumentasi fixture baru tanpa klaim audit nyata | 1.8 |
| tests/test_v2_models.py | Field/versi, scope dan invalidasi yang relevan | 1.3 |
| tests/test_v2_media.py | Overview/Storyboard, crop, font/batas dan layout versi lama | 1.4 |
| tests/test_v2_reporting.py | Enam bagian, bold/blockquote serta isi lengkap | 1.5 |
| tests/test_v2_reader.py | Reader/generator/snapshot/revisi/kapasitas | 1.6–1.8 |
| tests/test_audit.py | Sinkronisasi inventaris runtime lalu kit/prompt dan pipeline portable baru | 1.8/2.1–2.2 |
| tests/test_library.py, tests/test_actions.py | Regresi ingest/publikasi campuran bila asumsi output berubah | 1.7–1.8 |
| audit/template-audit.json | Sumber 2.1 dengan placeholder yang jelas | 2.1 |
| audit/json-guide.md | Pengisian Overview/arah dan pemisahan sumber/hasil | 2.1 |
| audit/protocol.md, audit/rubric.md | Cakupan/kelengkapan baru, metode audit tetap | 2.1 |
| audit/vocabulary.md | Label Camera Pattern dan istilah tampilan | 2.1 |
| audit/prompts/01-audit.md | Audit dan kandidat baru lengkap | 2.1 |
| audit/prompts/02-correct.md | Dampak koreksi pada JSON/Overview/pola/media | 2.1 |
| audit/prompts/03-export.md | Ekspor snapshot baru tanpa render ulang | 2.1 |
| audit/README.md, audit/providers.md | Perintah/isi kit dan petunjuk lingkungan aktual | 2.1–2.2 |
| tools/build_audit_kit.py | Sinkronisasi RUNTIME teknis, lalu GUIDES/template input dan versi workflow baru | 1.8/2.2 |
| docs/contracts/package-v2.md, docs/contracts/analysis-v2.md, docs/contracts/ai-reader-v2.md | Tambah navigasi/batas versi ke kontrak baru, tetap dokumentasi versi lama | 1.2/2.5 |
| docs/v2-field-map.md | Mapping field baru dan label manusia/AI | 1.2/2.5 |
| docs/template-analysis-v2.md | Acuan terbaru; hanya penyesuaian konsistensi yang diperlukan | 1.5 |
| docs/contoh-analysis-shot-normal.md, docs/contoh-analysis-shot-multi-area.md | Acuan yang sudah disetujui; koreksi hanya jika implementasi memerlukan penyelarasan | 1.5/1.8 |
| docs/prd-overview-storyboard-cloning.md | Catat keputusan versi/field/config dan status nyata | 1.2/2.5 |
| README.md, AGENTS.md, references/README.md, docs/operations.md | Jalur baca, media, versi dan penambahan ZIP | 2.5 |
| docs/alur-konsep-desain-v2.md, docs/capability-map.md | Inspirasi DNA/cloning dari JSON dan media baru | 2.1/2.5 |
| docs/improvement-v2-plan.md, docs/implementation-plan.md | Tautan kelanjutan/status baru tanpa menulis ulang riwayat | 2.5 |
| audit/pilots/README.md, audit/calibration.md | Kit/status dan hasil koreksi yang benar-benar terjadi | 2.5 |

### 6.3 Keluaran otomatis dan kandidat revisi

| File/folder | Cara pembaruan |
| --- | --- |
| audit/homeku-audit-kit.zip | Hasil tools/build_audit_kit.py; sinkron teknis di 1.8, lalu workflow baru lengkap di 2.2 |
| catalogs/, knowledge/, data/projections/, data/search-index.json, data/dependencies.json, data/build.json | Hasil generator/build/ingest; tidak diedit manual |
| data/registry.json, data/ingest.json | Hasil ingest paket final eksplisit, bukan perubahan plan/tooling saja |
| Workspace kandidat edh001 r0003 | audit.json ditulis dari revisi diterima; MD/manifest/tujuh JPEG dihasilkan helper; receipt di luar folder |
| audit/pilots/packages/edh001-r0003.zip dan incoming/edh001-r0003.zip | Hasil ekspor snapshot yang disetujui; nomor direkonsiliasi dengan registry saat pelaksanaan |
| references/edh001/* | Diganti oleh ingest revisi final, bukan edit langsung |

### 6.4 Tetap dipertahankan

- Semua file aktif edh001 r0002 sampai ingest revisi yang disetujui; ZIP r0001/r0002 dan riwayat tinjauan tidak ditimpa.
- Schema audit/manifest/reader/index lama, template beku lama, algoritme renderer versi lama dan font/lisensinya.
- Parser legacy tools/homeku/markdown.py, logika penyimpanan tools/homeku/storage.py, sampling/frame-native tools/homeku/video.py dan requirements.txt tidak memerlukan perubahan perilaku untuk PRD ini. Jika dependensi baru diperlukan, alasannya harus dicatat terlebih dahulu.
- .github/workflows/library-ci.yml dan library-ingest.yml sudah mencakup jalur tools/tests/schema/audit/data yang relevan; perubahan YAML tidak direncanakan kecuali tes menunjukkan kebutuhan spesifik. Tools publikasi Git tetap dipakai.
- bekerja/, archive/oldrepo/, video kanonis serta ZIP lain milik pengguna tidak diubah oleh implementasi tampilan.

## 7. Verifikasi dan keterlacakan ke PRD

| Persyaratan PRD | Bukti yang harus tersedia | Langkah |
| --- | --- | --- |
| Enam bagian, label/bold/blockquote terbaru | Render normal/multi, paragraf sumber utuh dan tidak ada placeholder/proses | 1.5/1.8 |
| Overview tepat, termasuk akhir OUT | Selection ID/PTS/area/paragraf sesuai gambar; Camera Start tetap awal sumber | 1.3–1.5/2.3 |
| Satu continuous shot multi area | Desain per area, rute/relasi, fase dan jumlah shot tidak terpecah | 1.3/1.5/1.6 |
| Camera Pattern tunggal/campuran/netral | Fungsi bersama, slot shot/pola/label sama; ambigu tidak menjadi NO IN/OUT | 1.3/1.6 |
| Kolase dan Storyboard rapi | Preview foto nyata, bold camera saja, waktu kanan atas, caption dan margin benar | 1.4/1.8 |
| Media aman dan tidak membengkak diam-diam | Preflight dimensi, byte aktual, skala eksplisit, konfigurasi/bbox/hash cocok | 1.4/1.7 |
| AI membaca ringan tanpa MP4 untuk media tersimpan | Identity/shot/area, crop foto/blok dengan sumber video disembunyikan pada root tes | 1.6 |
| Ratusan referensi | Regresi 300 model, pagination dan payload sebagian; tidak memuat media/narasi penuh di indeks | 1.6/1.8 |
| Paket lama dan satu sumber fakta | Regresi lintas versi, pointer/status/negasi/atribut baru utuh, r0002 byte-asli | 1.1–1.8 |
| Kit lengkap dan snapshot sama | Workspace kosong, roundtrip, perubahan JSON/MD/JPEG/config membatalkan receipt | 2.2/2.4 |
| Ingest tanpa review ulang | Supersedes tepat, replay unchanged dan turunan dibangun generator | 1.7/2.4 |
| Cloning/DNA dan reverse sesuai sumber | Panduan memakai Overview/JSON/media, produksi terpisah dari fakta audit | 2.1/2.5 |

Perintah penutup implementasi, sesuai instruksi repo:

```sh
python -m unittest discover -s tests -t . -v
python tools/build_audit_kit.py
python tools/library.py build
python tools/library.py check
python tools/build_audit_kit.py --check
git diff --check
```

Selama implementasi, jalankan tes terarah sesuai perubahan. Setelah suite lengkap dan pemeriksaan wajib lolos, ulangi hanya bila ada perubahan baru atau masalah yang belum terselesaikan. Tes menguji format/alur, bukan membuktikan kebenaran audit visual atau manfaat generatif pustaka.

## 8. Kriteria selesai dan titik berhenti

**Tahap 1 selesai:** kontrak/model/renderer/media/reader/ingest baru terintegrasi, preview nyata dan regresi lolos, kit tersinkron secara teknis dengan alur lama yang kompatibel, sumber aktif lama tetap utuh. Workflow pengguna 2.1 baru dinyatakan siap setelah Tahap 2 tooling selesai.

**Tahap 2 tooling selesai:** workflow dan kit baru lengkap serta lolos pipeline portabel. Ini terpisah dari penerimaan audit.

**Penerapan edh001 selesai:** kandidat lengkap disetujui pengguna, ZIP snapshot identik diekspor dan di-ingest secara eksplisit, turunan konsisten. Jika persetujuan belum diberikan, status berhenti pada kandidat siap ditinjau; tidak membuat persetujuan atau receipt rekaan.

**Enam pilot selesai:** hanya setelah run nyata dan penyerahan final masing-masing. Tidak menjadi syarat untuk menyatakan tooling baru siap, dan tidak dinyatakan selesai oleh plan ini.
