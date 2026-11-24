# PRD — Overview, Storyboard dan Alur Cloning HOMEKU

> Status setelah reset 24 November 2026: data audit edh001 telah dihapus atas permintaan pengguna. Catatan edh001 di dokumen ini bersifat historis, bukan referensi aktif atau persetujuan audit baru.

Diperbarui: 23 November 2026.

Status: **Tahap 1 dan Tahap 2 implementasi selesai; edh001 r0003 disetujui, diekspor dan aktif melalui ingest. Enam pilot pengguna tetap belum dinyatakan selesai.**

Dokumen ini melanjutkan [plan V2](improvement-v2-plan.md). Referensi aktif edh001 r0003, kontrak 2.1, renderer/media 2.2.0. Kontrak sumber/paket 2.1, renderer/media 2.2.0 dan reader/index 2.1 tersedia pada tooling baru. Workflow/prompt/template input dan kit telah diselaraskan ke 2.1. Pengguna menyetujui keseluruhan r0003; ZIP snapshot identik diekspor dan di-ingest. Riwayat r0001/r0002 tetap utuh.

## 1. Tujuan dan ruang lingkup

Pengguna dan AI dapat memahami desain serta seluruh perjalanan kamera melalui media pustaka, lalu membuat gambar wide dengan posisi kamera yang sesuai untuk produksi home tour.

**Lihat Overview dan Storyboard → pahami desain serta posisi kamera → buat gambar wide yang mirip → siapkan prompt gerakan kamera → susun video.**

Pembacaan untuk inspirasi atau cloning tidak mewajibkan membuka MP4. MP4 tetap sumber kanonis untuk audit dan koreksi bukti bila diperlukan. AI dapat memperbesar gambar atau mengambil foto/blok shot dari media gabungan, kemudian membaca JSON untuk detail dan penyalinan gerakan kamera secara tepat.

Cakupan implementasi adalah pustaka, media, laporan manusia, data/pembaca AI dan workflow audit GPT/Gemini. Dokumen bekerja/ tetap jalur produksi terpisah; omniflash-v2.md hanya acuan notasi, tanpa mengganti arah, tempo atau kronologi sumber. Pembuatan plugin produksi tidak termasuk cakupan ini.

## 2. Keputusan tampilan yang sudah disepakati

Acuan tampilan: [template](template-analysis-v2.md), [contoh normal](contoh-analysis-shot-normal.md), dan [contoh multi area](contoh-analysis-shot-multi-area.md). Provenance aset contoh tersedia [terpisah](example/prd-overview-storyboard/README.md); gambar contoh bukan bukti audit video.

- Laporan mempunyai enam bagian: **Profil desain, Ukuran & proporsi, Shot Timeline, Overview, Storyboard, Shot Details**.
- Nama gaya, nama area dan istilah teknis memakai bahasa Inggris; uraian tetap bahasa Indonesia. Nama gaya sumber yang diterima tidak diterjemahkan otomatis.
- Judul A/B/C dan subjudul area multi area menggunakan **bold eksplisit**, dengan tingkat heading konsisten. Label isi bold pada ukuran teks biasa; paragraf dan notasi kamera regular.
- Gaya utama dan rentang luas lantai ditebalkan. Luas lantai wajib rentang angka, misalnya **60–90 m²**, tanpa catatan dasar/kepastian pada laporan manusia.
- Shot Timeline mempunyai lima kolom dan Camera Pattern di atasnya. Kolom Gerakan singkat/Ritme tidak ditampilkan; tempo tetap tersedia pada detail shot dan JSON.
- Overview menggabungkan frame wide dalam satu baris. Di bawahnya, setiap pilihan mempunyai judul singkat **Shot NN · Area · x.xxs**, kemudian satu paragraf regular dalam blockquote (`> `), tanpa label “Komposisi overview”. Judul bold berada di luar blockquote.
- Storyboard menyusun seluruh kolase shot ke bawah, termasuk header, panel, caption dan camera. Setiap shot juga mempunyai gambar kolase sendiri pada Shot Details.
- Satu continuous take tetap satu shot walaupun melalui beberapa area. Normal memakai tiga panel; multi area dinamis mengikuti momen penting.
- Notasi kamera satu paragraf tanpa Enter manual setelah `→` atau `+`; baris membungkus mengikuti lebar tampilan.
- Pada gambar, label **camera:** saja yang bold; IN/OUT dan notasi sesudahnya regular. Ukurannya sama dengan label start. Font memakai ukuran preview terakhir yang disetujui: sekitar 12% lebih kecil dari preview sebelumnya, kecuali waktu/durasi kanan atas yang tetap. Pengurangan tidak diulang setiap render.
- Tinggi kanvas mengikuti teks terakhir. Padding bawah contoh 30 px dan jarak antarblok storyboard 60 px menjadi acuan pada ukuran kanvas contoh; penyesuaian skala mempertahankan proporsinya.

## 3. Susunan analysis.md

### Enam bagian laporan

| Bagian | Isi |
| --- | --- |
| **1. Profil desain** | Nama desain, gaya utama, pengaruh gaya, gaya interior, ciri khas, warna & material, suasana dan lingkungan |
| **2. Ukuran & proporsi** | Tabel ukuran, bentuk bangunan, lantai & bentuk atap, tapak, proporsi dan perkiraan luas lantai wajib |
| **3. Shot Timeline** | Ringkasan durasi/cut atau kontinuitas, Camera Pattern dan tabel urutan shot |
| **4. Overview** | Gambar gabungan wide satu baris, judul dan satu paragraf per frame terpilih |
| **5. Storyboard** | Satu gambar gabungan seluruh blok kolase shot secara vertikal |
| **6. Shot Details** | Kolase dan rincian desain, Framing & Lighting, serta Camera Movement per take kontinu |

Gunakan label **Nama desain, Ciri khas, Warna & material, Lantai & bentuk atap, Camera Pattern, Camera Movement, Tempo, Alur visual, Movement Timeline** sesuai template. Tabel digunakan untuk ukuran, Shot Timeline dan Movement Timeline; rincian Framing & Lighting memakai poin berlabel pendek.

### Shot Timeline

Contoh pola lima shot: **Camera Pattern:** IN – OUT – IN – OUT – IN.

Tabel tepat lima kolom: **Shot, Time (s), Duration, Area/Scene, Camera Movement**. Contoh berikut memformat data edh001 r0002 yang sudah diterima, tanpa audit atau revisi baru:

| Shot | Time (s) | Duration | Area/Scene | Camera Movement |
| --- | --- | --- | --- | --- |
| 01 | 0.00–4.73 | 4.73s | Exterior | Orbit Right (~15°–20°) → Accelerating Dolly-In (~2×) toward entrance door. |
| 02 | 4.73–8.30 | 3.57s | Living Room | Dolly-Out (~2×) + Orbit Left + Pan Right. |
| 03 | 8.30–11.57 | 3.27s | Kitchen | Accelerating Dolly-In (~2×) + Pan Left (~25°–30°) toward refrigerator and coffee niche. |
| 04 | 11.57–15.00 | 3.43s | Bedroom | Dolly-Out (~1.3×) + Orbit Left + strong Pan Right (~30°–35°). |
| 05 | 15.00–18.40 | 3.40s | Bathroom & Laundry | Dolly-In (~2×) + gentle Pan Right (~10°–15°). |

Waktu tampilan menggunakan dua desimal; nilai waktu/PTS/frame asli dalam JSON tetap utuh. Perkiraan ~×/~°, target, simultan `+`, urutan `→` dan tanda baca kamera tidak diubah. Rasio ~× tidak dianggap sebagai tempo.

### Overview

Single area memakai satu overview yang paling lengkap menjelaskan area. Multi area memakai overview untuk setiap area penting dalam take yang sama; nomor shot tetap sama. Area yang hanya tampak sekilas tidak otomatis menjadi area fisik atau shot baru. Pemilihan tambahan hanya untuk kebutuhan visual yang jelas, dengan alasan tersimpan pada JSON.

Frame terpilih biasanya awal IN atau akhir OUT. Jika frame lain lebih lengkap, auditor dapat memilihnya dan mencatat alasan serta bagian lintasan yang diwakilinya. Overview di tengah shot tidak dianggap otomatis cocok untuk menjalankan seluruh gerak sumber dari awal.

Setiap paragraf menjelaskan **frame overview yang dipilih**: posisi kamera, arah pandang, sudut, ketinggian/kemiringan, cakupan wide, penempatan elemen, kedalaman dan pencahayaan. Satu paragraf ringkas dalam blockquote (`> `), tanpa mengulang seluruh inventaris furnitur. Judul bold menampilkan shot, area dan timestamp di luar blockquote; tidak memakai label “Komposisi overview”.

**Camera Start** pada Shot Details selalu menjelaskan awal shot sumber. Overview akhir OUT menjelaskan posisi akhir yang lebih wide. Keduanya disimpan dan ditampilkan sesuai perannya.

### Shot Details dan hierarki bold

Setiap kartu dimulai dengan judul **Shot NN · Area/urutan area**, baris **Time:** rentang sumber · **Duration:** durasi, lalu kolase. Shot multi area menambahkan **Shot Type:** Continuous shot · Multi area · No cut. Anchor `profil-dna` dan `shot-NN` tetap stabil.

- **A. Desain area:** Arsitektur, Furnitur & dekorasi, Lingkungan. Single area langsung memakai ketiga label tersebut. Multi area dikelompokkan **per area** sesuai urutan kemunculan: Exterior beserta tiga uraian, kemudian Living, lalu Kitchen; tetap dalam satu kartu shot.
- **B. Framing & Lighting:** Fokus, Camera Start, Framing, Lighting. Multi area menambahkan Area, Rute kamera dan Hubungan antararea: Penghubung area, Peralihan, Orientasi ruang. Area terlihat berbeda dari area yang benar-benar dimasuki kamera.
- **C. Camera Movement:** paragraf gerakan bahasa sederhana, **Tempo:**, lalu **Camera:** dengan notasi lengkap. Multi area menambahkan **Alur visual:**; shot beberapa fase/perpindahan area mempunyai **Movement Timeline** dengan kolom Time (s), Area & fokus, Camera Movement, Tempo.

A/B/C memakai heading tingkat 4 dengan bold eksplisit; nama area multi memakai tingkat 5 dengan bold eksplisit. Label kategori dan label singkat memakai bold ukuran teks biasa. Paragraf Arsitektur, Furnitur & dekorasi, dan Lingkungan pada bagian A memakai blockquote (`> `), dengan label kategori bold di luar blockquote dan isi paragraf regular. Aturan ini berlaku pada setiap area dalam shot multi area. Bagian B tetap poin berlabel dan bagian C tetap paragraf/label biasa. Isi notasi kamera regular. Pisahkan antarkartu shot dengan garis horizontal.

Paragraf gerakan menjelaskan lintasan, arah pandang, target dan reveal; Tempo menjelaskan perkembangan kecepatan. Hindari pengulangan kalimat tanpa menghilangkan detail. Data bersama, seperti waktu dan notasi, ditampilkan dari field sumber yang sama.

## 4. Media, keterbacaan dan batas ukuran

### Inventaris dan pemilihan panel

Paket versi baru mencakup **media/overview.jpg, media/storyboard.jpg dan media/shot-NN.jpg per shot**. Tidak menambah motion/, JPEG frame lepas atau seluruh frame audit.

- **Overview:** frame asli yang dipilih auditor; seluruh pilihan tersusun satu baris menurut urutan sumber. Nomor shot, area dan waktu dapat dikenali. Header gabungan memuat ID referensi — Primary style — durasi — jumlah shot.
- **Kolase normal:** tiga kolom Start, Middle, End. Start/End mengikuti batas native shot; Middle memakai frame native terdekat titik tengah.
- **Kolase multi area:** jumlah panel dinamis dan kronologis, mencakup awal/akhir serta reveal, perpindahan atau perubahan gerak penting. Tidak dipaksa lima panel; susunan dapat beberapa baris agar terbaca.
- **Storyboard:** seluruh blok kolase disusun vertikal sesuai urutan shot, dengan identitas video sekali di atas. Tinggi setiap blok mengikuti isi, termasuk notasi yang membungkus.

Semua foto mempertahankan rasio serta konteks sumber. Tidak ada crop konteks atau pembesaran generatif. Foto overview/blok/panel dapat diambil dari media melalui metadata bbox, tanpa membuka MP4. Perbesaran tampilan tidak menambah detail asli.

### Header dan caption kolase

```text
SHOT 01 · Exterior                         0.00–4.73s · 4.73s

[Foto Start]             [Foto Middle]             [Foto End]

shot-01 start 0.00s       shot-01 middle 2.37s      shot-01 end 4.70s
camera: (IN) Orbit Right (~15°–20°) → Accelerating Dolly-In (~2×) toward entrance door.
```

Header hanya judul, rentang dan durasi; tidak memuat daftar waktu seluruh panel. Caption berada di bawah foto, font regular. Multi area memakai nama momen yang spesifik, bukan semua disebut middle. Hanya `camera:` pada baris kamera yang bold; seluruh notasi regular dan satu paragraf. Teks panjang membungkus di luar foto; ruang bawah mengikuti teks terakhir.

### Batas dan penanganan gambar panjang

Batas awal rancangan mempertahankan batas teknis yang berlaku: **60 juta piksel per gambar, sisi JPEG maksimal 65.000 px, 95 MiB per file, 256 MiB ZIP maupun total hasil ekstraksi**. Batas lainnya tetap 2.000 file dan 2 MiB per file teks. Batas ini bukan target ukuran; byte media/ZIP tetap diukur pada preview nyata.

- Default awal JPEG quality **91**, panel scale **1**; rentang konfigurasi quality **60–98**, scale **(0, 1]**, dan kolom multi **1–6**. Angka ini melanjutkan konfigurasi yang ada, bukan aturan yang sudah diterapkan untuk layout baru.
- Perhitungan dimensi, jumlah piksel dan perkiraan alokasi dilakukan sebelum merender; ukuran byte aktual diperiksa setelah encoding dan sebelum ekspor.
- Overview satu baris dan storyboard vertikal tetap satu file masing-masing selama memenuhi batas dan terbaca. Kolase tiap shot selalu tersedia sebagai akses detail, dengan inventaris yang menunjuk foto beresolusi paling baik yang tersedia.
- Jika layout melampaui batas, hentikan kandidat dengan penjelasan media yang bermasalah. Penyesuaian skala/kolom/quality dilakukan secara eksplisit di workspace chat sebelum pengguna memeriksa kandidat final. Jangan otomatis mengecilkan font, membuang shot/panel atau menghasilkan berkas terpotong.
- Jika pengecilan media gabungan dipilih, per-shot dapat dipertahankan lebih detail melalui konfigurasi yang tercatat; seluruh koordinat/skala/provenance harus mengikuti hasil aktual. Pilihan konfigurasi per jenis media dirinci dalam kontrak implementasi.
- Bila satu file gabungan tetap tidak memadai, kasus tersebut kembali dibahas sebelum ZIP final; tidak diam-diam menambah halaman/file atau mengubah kesepakatan satu gambar.

Preview memeriksa normal, multi area, notasi panjang dan banyak shot. Ukur keterbacaan pada lebar baca biasa serta ukuran asli, ruang kosong, dimensi dan byte. Tidak menganggap jumlah file lebih sedikit pasti menghemat penyimpanan.

## 5. Data sumber dan pembacaan AI

**audit.json tetap satu sumber isi**, analysis.md hasil renderer, manifest metadata teknis/provenance. Tidak membuat analysis.json yang diedit terpisah. Generator tidak menebak fakta dari narasi atau melakukan sintesis AI.

Tambahan yang diperlukan:

- **shots[].overviews[].composition_summary:** satu paragraf yang ditulis auditor setelah melihat frame terpilih. ID/frame/PTS/area/reason tetap tersedia. Paragraf yang sama ditampilkan verbatim pada laporan dan JSON pembaca; tidak dipecah menjadi delapan salinan field baru.
- Klasifikasi arah sumber yang tercatat dan terhubung ke shot/fase terkait. Representasi field minimal serta aturan konsistensinya ditetapkan pada kontrak baru. Pola tingkat shot/video merupakan hasil deterministik dari sumber tersebut, bukan ringkasan manual kedua.
- Manifest menginventarisasi overview, kolase dan storyboard beserta hash, dimensi, urutan, bbox foto/blok, skala dan pointer pilihan asli. Foto dan caption memiliki batas terpisah.

**Camera Start** tetap berasal dari shots[].composition; tidak digantikan composition_summary overview. Desain setiap area, route, fase, tempo, relasi, ketidakpastian, negasi, label baru dan pointer sumber tetap dipertahankan.

### Camera Pattern

| Kasus | Label per shot |
| --- | --- |
| Hanya maju | IN |
| Hanya mundur | OUT |
| Berubah arah | IN → OUT, OUT → IN, atau urutan aktual lainnya |
| Tanpa maju/mundur | NO IN/OUT; Orbit/Pan/Tilt/gerak lain tetap pada Camera Movement |

Urutan antarshot memakai ` – `. Pola campuran dalam satu shot dikelompokkan dengan kurung, misalnya **IN – (OUT → IN) – NO IN/OUT** berarti tiga shot, bukan empat. Label pada gambar menggunakan klasifikasi shot yang sama: `(IN)`, `(OUT)`, `(IN → OUT)`, atau `(NO IN/OUT)`.

Pola merangkum maju/mundur; orbit atau pan awal yang diikuti Dolly-In tidak otomatis menambah arah baru, sehingga shot pertama edh001 tetap IN. Fase netral dan jeda tetap tersedia pada Movement Timeline; perubahan arah maju/mundur yang nyata tidak dihapus dari pola. NO IN/OUT bukan pengganti data yang belum diketahui.

Auditor menetapkan klasifikasi melalui bukti/gerak terstruktur yang jelas; generator tidak menebak dari prosa, zoom, perubahan ukuran objek atau ketidakstabilan kamera. Kasus ambigu dan paket lama mempertahankan status aslinya tanpa dipaksa berlabel baru. Pola tidak menggantikan rincian kamera, fase atau tempo.

Generator menerbitkan pola sesuai urutan shot pada laporan, proyeksi dan indeks ringkas. Indeks tidak membawa seluruh paragraf/desain/media. Filter pola CLI dapat dirinci saat implementasi tanpa menjadi syarat penggunaan dasar.

### Dua alur penggunaan

**Cloning referensi:** pilih ID aktif → lihat Overview/Storyboard → baca paragraf posisi kamera serta detail yang diperlukan → tirukan desain, susunan objek dan framing → siapkan gambar wide serta prompt kamera sesuai referensi. Tidak menambahkan variasi kreatif tanpa permintaan pengguna.

**Konsep baru sesuai DNA:** cari referensi relevan → baca visual/detail terpilih → kembangkan konfigurasi sesuai brief → kunci identitas rumah → pilih komposisi wide serta gerak yang cocok. Sumber inspirasi dan keputusan desain baru tetap dibedakan.

Reader identitas tetap ringan. Reader shot/area mengembalikan overview beserta paragrafnya, desain relevan, kamera, fase/tempo dan rujukan media. Pembacaan satu area pada multi area tetap mempertahankan perjalanan kamera seluruh shot. Foto/blok diekstrak ke workspace sementara; MP4 tidak diperlukan untuk mengambil foto yang sudah tersimpan dalam media.

### Workflow produksi: IN dan reverse OUT

- **Sumber IN:** overview wide biasanya dari awal, menjadi gambar awal produksi IN.
- **Sumber OUT:** overview wide biasanya dari akhir, menjadi gambar awal produksi IN; hasil video di-reverse menjadi OUT.
- Pembalikan berlaku pada **seluruh perjalanan**, termasuk rotasi, urutan fase dan perkembangan tempo. Mengganti kata Out menjadi In saja tidak cukup.
- Camera Pattern dan Camera Movement selalu mencatat sumber asli. Adaptasi prompt produksi dijelaskan terpisah dan tidak mengubah audit.
- Overview tengah shot, gerak campuran dan multi area memerlukan penyesuaian lintasan sesuai bagian yang terlihat. Overview area akhir tidak otomatis menggambarkan semua area sebelumnya; hubungan ruang tidak dikarang dari cut.

## 6. Workflow audit GPT/Gemini

1. Auditor menerima MP4 dan kit yang mendukung versi baru. Metode tetap baseline **10 FPS** sepanjang shot, frame native awal/akhir, serta pendalaman seluruh frame native pada rentang yang membutuhkan; bukan memaksa video lain menjadi 30 FPS.
2. Tetapkan batas take kontinu, area fisik yang terlihat/dilalui, desain, hubungan ruang, gerak/fase dan tempo. Jangan mengubah arah/tempo sumber menjadi default produksi. Log hanya mencatat frame yang benar-benar diperiksa.
3. Pilih panel serta overview dari frame asli, tulis paragraf overview dan Camera Start sesuai frame masing-masing. Lengkapi seluruh data yang dibutuhkan template/pembaca dalam audit.json.
4. Helper merender satu kandidat lengkap: JSON, analysis.md, manifest dan semua media. Nilai bersama memakai field yang sama; validator memeriksa struktur, interval, label, inventaris dan hubungan teknis. AI memeriksa kesesuaian makna desain, kamera dan gambar sebelum kandidat ditampilkan.
5. Pengguna memeriksa laporan/media di chat. Koreksi memperbarui sumber JSON atau konfigurasi layout, lalu merender ulang seluruh keluaran terkait; bukan menyunting MD/JPEG secara terpisah.
6. Setelah kandidat lengkap disetujui, ekspor **byte snapshot yang sama** menjadi satu ZIP. Receipt tetap di luar ZIP. Tidak merender ulang saat ekspor.
7. Pengguna memindahkan ZIP ke incoming/ lalu menjalankan ingest. Sistem memvalidasi teknis dan memperbarui katalog/knowledge/proyeksi/indeks; tidak ada review isi ulang setelah ingest atau pembaruan otomatis hanya karena ZIP ditempel.

Prompt audit, panduan JSON, template kit dan helper harus mendukung field serta layout yang sama. Menyalin template rancangan ke kit aktif saja tidak dianggap implementasi selesai.

## 7. Perubahan file dan urutan implementasi

### Peta file

- **Kontrak:** docs/contracts/analysis-v2.md, package-v2.md, ai-reader-v2.md serta schema audit/manifest/reader/search-index yang relevan; tambahkan versi eksplisit untuk field dan media baru.
- **Template/contoh:** template-analysis-v2.md dan kedua contoh sebagai acuan rancangan; docs/v2-field-map.md serta template beku versi baru di tools/assets/templates/ mengikuti hasil implementasi.
- **Media/laporan:** tools/homeku/media.py, reporting.py dan dispatch modul versi baru: Overview, kolase, Storyboard, Camera Pattern, hierarki bold, crop serta batas ukuran.
- **Model/validasi/ekspor:** tools/homeku/models.py, validation.py, exporter.py, tools/audit.py untuk inventaris/field baru dan snapshot/ekspor.
- **Reader/generator:** tools/homeku/reader.py, generation.py, engine.py bila diperlukan: baca overview dan perjalanan kamera, provenance, pola ringkas, invalidasi cache dan pembacaan parsial.
- **Workflow/kit:** audit/template-audit.json, json-guide.md, README.md, protocol/rubric, tiga prompt serta tools/build_audit_kit.py; kit dibangun ulang dari sumber yang sesuai renderer baru.
- **Panduan/status:** docs/alur-konsep-desain-v2.md, README.md, references/README.md, docs/operations.md, status plan V2 dan AGENTS.md diselaraskan saat kontrak baru diterapkan.
- **Regresi:** tests/test_v2_media.py, test_v2_reporting.py, test_v2_models.py, test_v2_reader.py, test_audit.py serta fixture terisolasi.

catalogs/, knowledge/, data/projections/, indeks, dependencies dan build tetap keluaran generator. Referensi aktif tidak diubah langsung; archive/oldrepo/ bukan input discovery.

### Urutan kerja

1. Tetapkan pasangan versi sumber/paket, reader/index dan renderer/media baru beserta representasi arah serta konfigurasi media. Rancangan sumber, tampilan, kit dan kompatibilitas harus konsisten sebelum coding terkait dimulai.
2. Perbarui kontrak/schema/pemetaan field, lalu implementasikan model/validasi dan dukungan versi. Paket lama tetap dapat dibaca; renderer/template/font versi yang telah diterima tetap beku.
3. Implementasikan layout serta laporan mengikuti template/contoh terakhir. Buat preview dengan frame edh001 yang sudah tersedia, ditambah fixture multi area/gerak campuran/notasi panjang/banyak shot. Ini pemeriksaan layout, bukan klaim audit ulang penuh.
4. Integrasikan reader, generator, snapshot/ekspor, prompt audit dan kit portabel; jalankan verifikasi teknis yang relevan.
5. Siapkan kandidat edh001 **r0003**: tulis paragraf overview dari frame terpilih dan lengkapi klasifikasi arah yang dibutuhkan. Pertahankan fakta, gerak dan log r0002; pemeriksaan tambahan hanya dicatat jika benar-benar dilakukan. Tidak otomatis mengaudit ulang seluruh video.
6. Tampilkan kandidat lengkap untuk koreksi/persetujuan di chat, lalu ekspor byte yang sama dan ingest revisi eksplisit yang supersede r0002. Riwayat r0001/r0002 dipertahankan.
7. Selaraskan status dan gunakan kit versi baru untuk enam pilot berikutnya yang dijalankan pengguna. PRD ini tidak menyatakan pilot tersebut selesai.

## 8. Kriteria penerimaan

- Keenam bagian, label, hierarki bold A/B/C, subjudul area dan tabel sesuai template/contoh yang disetujui. Paragraf desain tetap lengkap dan memakai blockquote per kategori pada bagian A; label kategori berada di luarnya. Bagian B/C tidak diubah menjadi blockquote; tidak ada label proses dalam laporan hasil.
- Setiap overview mempunyai judul bold di luar blockquote dan paragraf regular di dalamnya, sesuai frame/area/timestamp; Camera Start tetap posisi awal sumber, termasuk ketika overview berada di akhir OUT.
- Multi area tetap satu shot dengan desain dikelompokkan per area, rute/relasi terlihat dan timeline kamera yang utuh.
- Camera Pattern konsisten pada laporan/gambar/proyeksi/indeks; IN/OUT campuran tidak menambah shot; NO IN/OUT tidak dipakai untuk data yang belum diketahui.
- Notasi kamera satu paragraf, tidak berubah arah, angka, fase, target atau tempo karena renderer maupun workflow reverse produksi.
- Overview satu baris; Storyboard seluruh blok vertikal; kolase per-shot hadir pada Shot Details. Caption dan camera terbaca, tidak bertumpuk, tidak menimpa foto dan tidak menyisakan ruang bawah berlebih.
- Bbox/foto/blok sesuai media yang dihasilkan; AI dapat mengambil gambar yang tersimpan tanpa MP4. Pointer, pilihan native dan provenance tetap konsisten.
- Dimensi/piksel diperiksa sebelum alokasi; byte diperiksa sesudah encoding. Media panjang tidak diam-diam diperkecil/dipotong atau kehilangan shot. Konfigurasi yang dipilih tercatat dan ditampilkan sebelum ZIP final.
- JSON satu sumber; tidak ada ekstraksi fakta dari MD, salinan manual pada keluaran generator atau ketidakpastian/negasi yang hilang.
- Workflow GPT/Gemini menghasilkan paket versi baru yang lengkap. Koreksi merender ulang kandidat; persetujuan mengikat seluruh snapshot; ekspor mempertahankan byte dan ingest tidak menambah review isi.
- Paket lama tetap valid/readable, ZIP edh001 r0002 dipertahankan utuh; referensi aktif berubah hanya melalui revisi yang disetujui, dan replay ingest tidak mengubah hasil. Fixture tidak menjadi referensi aktif dan kit bisa dipakai dari workspace kosong.

Pemeriksaan wajib setelah perubahan tooling:

```sh
python -m unittest discover -s tests -t . -v
python tools/library.py check
python tools/build_audit_kit.py --check
```

Pemeriksaan teknis serta preview layout tidak dianggap sebagai pengujian manfaat konsep AI, audit penuh video atau penyelesaian pilot yang belum dijalankan.

## 9. Status keputusan dan langkah berikutnya

**Sudah dirumuskan dalam PRD:** susunan laporan terbaru, istilah/bold, aturan overview, Camera Pattern tunggal/campuran/netral, batas teknis awal media, penanganan gambar panjang dan workflow audit hingga ingest.

**Rincian implementasi:** [plan implementasi berurutan](implementation-plan-overview-storyboard.md) merinci target versi, field klasifikasi arah, konfigurasi skala per jenis media, daftar file baru/diubah dan verifikasinya. Rincian tersebut diterapkan melalui kontrak baru dan tidak mengubah sistem aktif hanya karena dokumennya ditulis.

**Sudah diverifikasi pada Tahap 1:** preview foto nyata, layout normal/multi area, notasi panjang, batas ukuran, snapshot/kompatibilitas serta pembaca tanpa MP4 untuk foto tersimpan. [Hasil, ukuran media dan daftar file](overview-storyboard-verification.md). Konfigurasi/font mengikuti baseline contoh yang disetujui; batas teknis tidak diubah.

**Tahap 2 selesai:** panduan/prompt/template kit2.1 aktif dan pipeline teknis portable telah diuji. edh001 r0003 aktif dengan lima paragraf Overview dan enam klasifikasi arah fase; fakta/gerak/tempo sumber diterima tetap sama. Camera Start laporan diselaraskan ke posisi/arah/sudut sesuai template; tinggi/kemiringan tetap pada JSON dan paragraf Overview.

**Penerapan langkah 2.4–2.5 selesai:** pengguna menyetujui snapshot lengkap dengan “ya saya setuju”; ekspor/validasi roundtrip mempertahankan byte yang sama, ingest eksplisit mengaktifkan r0003, replay unchanged dan status dokumentasi diperbarui. Enam pilot pengguna berikutnya memakai kit terbaru; pelaksanaan/kalibrasi mereka belum dinyatakan selesai. Runtime/paket lama tetap didukung.
