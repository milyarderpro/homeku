# Plan implementasi audit kamera berbasis panduan eksperimen

> Status setelah reset 24 November 2026: data audit edh001 telah dihapus atas permintaan pengguna. Catatan edh001 di dokumen ini bersifat historis, bukan referensi aktif atau persetujuan audit baru.

Tanggal: 24 November 2026. Status: **tahap1–8 selesai; tahap9 siap diuji pengguna, run provider2.5 belum dijalankan**.

Melanjutkan [plan efisiensi](audit-efficiency-implementation-plan.md) dan evaluasi dua hasil pilot edh058 sumber 2.4. Acuan eksperimen: [panduan audit gerakan kamera](panduan_audit_gerakan_kamera_ai.md). Kesepakatan terbaru pengguna pada plan ini menggantikan kewajiban angka per komponen untuk **format baru**, tanpa mengubah kontrak atau paket lama.

## 1. Hasil yang ingin dicapai

AI mengenali gerakan utama, gerakan gabungan, urutan fase, intensitas dan perubahan laju dengan lebih baik. Notasi tetap singkat dan berguna untuk produksi; angka tidak dipaksakan pada setiap komponen. Detail rumah tetap kaya dan dapat ditemukan AI melalui fakta terstruktur.

| Dipertahankan | Diperbaiki |
| --- | --- |
| Baseline 6 FPS; pendalaman 10 FPS/native sesuai pertanyaan | Pembacaan per interval dan pemeriksaan Pan–Orbit–Truck |
| audit.json sebagai satu sumber isi audit | Parser dan validator menerima notasi eksperimen secara utuh |
| analysis.md enam bagian dengan struktur A/B/C | Keterwakilan detail narasi di fakta dan label kolase |
| Satu take kontinu = satu shot, termasuk multi area | Batch ekstraksi yang gagal pada lingkungan provider |
| Camera Start berbeda dari Overview akhir OUT | Bantuan angka ringan, tidak menjadi syarat kelengkapan |
| Persetujuan seluruh kandidat di chat sebelum ekspor | Panduan, contoh, tooling dan pembaca AI saling selaras |

Tidak mencakup produksi konsep/gambar/video, plugin, perubahan masterprompt bekerja/, audit massal seluruh koleksi atau pengujian manfaat produksi. Tidak mengubah referensi aktif, melakukan ingest, atau menerima paket baru melalui implementasi tooling.

## 2. Dasar temuan dan batas kesimpulan

Kedua ZIP terbaru yang diperiksa memakai sumber 2.4, report 2.2.3 dan media 2.2.0. Keduanya lulus validator, MD identik renderer dan seluruh delapan JPEG identik setelah render ulang dari sumber kanonis.

| Provider / lokasi saat diperiksa | SHA-256 ZIP | Shot | Fakta | Frame unik dinyatakan viewed |
| --- | --- | --- | --- | --- |
| Gemini: audit/result/gemini/edh058-r0001.zip | 62ea7f3c7e40b5f7cf6cc64a7f04b0e1328e5ed3a6960f35afecbaef93764df7 | 6 | 36 | 132 |
| GPT: audit/result/gpt/edh058-r0001.zip | bf34dab108720c30ce8703b9c79a7efa7066a4c6445e1b223b8e4620d7e36f5d | 6 | 36 | 132 |

- Pengamatan tambahan asisten: 18 frame sumber awal–tengah–akhir, bukan audit ulang seluruh baseline. Belum cukup untuk mengesahkan semua angka, fase dan gerakan.
- Laporan Gemini menyebut sekitar 11 menit 16 detik; GPT sekitar 14 menit 45 detik dari prepare sampai review, belum termasuk persiapan awal. Rentang dan cakupannya berbeda; log performa mentah tidak disertakan.
- Keduanya melaporkan kegagalan ekstraksi 132 frame sekaligus lalu memakai batch kecil. Kode lokal extract_many memang masih membentuk satu ekspresi select untuk seluruh frame yang belum tersedia.
- GPT menambahkan Pan pada exterior, closet dan bathroom yang belum cukup kuat pada pemeriksaan terbatas. Ini temuan untuk pilot, bukan daftar jawaban wajib.
- Keduanya menulis enam fakta setiap shot, padahal narasi memuat detail tambahan. Tidak disimpulkan bahwa jumlah fakta tertentu harus dipenuhi.
- Label media sekarang berasal dari engine: shot-03 start 8.37s. Ini masalah renderer, bukan kesalahan pengguna/provider.
- Sepuluh studi kasus pada dokumen eksperimen belum dijalankan ulang oleh asisten; contoh metode bukan bukti kalibrasi selesai.

## 3. Aturan kamera yang disepakati

### 3.1 Format dan angka

Kerangka baku:

~~~text
[Komponen Utama] ([Skala]) [+ / →] [Komponen Sekunder] ([Intensitas / Kurva])
~~~

Bagian dalam kurung dan komponen sekunder **opsional**. Kerangka bukan kewajiban selalu ada Dolly, angka, intensitas atau easing. Komponen utama boleh Orbit, Pan, Truck, Static atau gerakan lain yang diamati.

- + berarti simultan; → urutan fase. Satu shot dapat memuat keduanya dalam satu paragraf.
- Skala ~× dan sudut ~° boleh ada pada sebagian komponen saja. Komponen jelas tanpa angka tetap sah pada confidence medium/high.
- Ketiadaan angka tidak memerlukan alasan khusus, alternatives atau penurunan confidence. Ketidakpastian gerakan yang nyata tetap dijelaskan.
- Angka tunggal menjadi default. Rentang boleh bila berguna, bukan dipaksakan.
- Jangan mewajibkan satu desimal jika hasil yang berguna ditulis ~1.75×. Dukungan angka berhingga positif dan rentang berurutan diuji; hindari presisi yang tidak membantu.
- x menjadi × dan koma desimal menjadi titik hanya pada normalisasi sumber kerja baru, tanpa mengubah nilai. Notasi sumber diterima tidak ditulis ulang.
- Tidak mewajibkan awalan Simultaneous: atau Multi-Phase:. Bila ditulis, parser mengenalinya sebagai penjelas struktur, bukan jenis gerakan.
- estimate_basis boleh null bila tidak ada angka. Jika angka dicantumkan, satu kalimat pengamatan/asumsi cukup; tanpa kewajiban kalibrasi, bukti eksternal atau pengukuran piksel.
- scale_measurement tetap nullable. Jika diisi, pengukuran nyata dan rasio tetap diuji; statistik affine global tidak dipalsukan sebagai pengukuran lebar/tinggi objek.
- ~× tetap perubahan skala gambar: IN = akhir/awal, OUT = awal/akhir; bukan faktor kecepatan atau jarak fisik.

Semua contoh berikut harus diterima pada format baru:

~~~text
Dolly-Out (~1.6×) + Orbit Left + Pan Right.
Straight Dolly-In → Dolly-In + Strong Pan Right (~25°–30°).
Dolly-Out (~1.6×) + Orbit Left + Subtle Pan Right (Ease-Out).
Diagonal Dolly-Out (~2.5×) + Moderate Pan Right (Ease-Out).
Pure Orbit Right → Accelerating Dolly-In (~2×) toward entrance door.
Mild Dolly-Out (~1.75×) + Orbit Left + Strong Pan Right (~35°, Ease-Out).
~~~

### 3.2 Kosakata dan ritme

Pertahankan gerak dasar Dolly/Zoom, Pan, Orbit, Truck, Tilt, Pedestal, Tracking, Static dan Uncertain. Tambahkan pengenal Straight, Diagonal, Pure, Mild, Subtle, Moderate, Strong, gentle, Accelerating, Decelerating, Constant, Ease-In dan Ease-Out.

- Straight/Diagonal menjelaskan lintasan; bukan jenis ruangan atau fase baru.
- Mild/Subtle/Moderate/Strong/gentle menjelaskan intensitas komponen, bukan otomatis tempo shot.
- Pure Orbit tidak berarti Static camera. Static Distance hanya menyatakan kedalaman netral; tidak menghapus rotasi/translasi lain yang ditulis.
- Ease-In/Ease-Out berlaku pada komponen tempat label ditempelkan. Ease-Out pada Pan tidak otomatis membuat seluruh Dolly melambat.
- Label Accelerating/Decelerating harus konsisten dengan speed_change; gabungan komponen yang berbeda dapat memakai variable pada fase.
- Kenaikan skala saja tidak otomatis Accelerating. Nilai laju visual pada interval waktu setara; penilaian visual wajar tetap sah tanpa pembuktian fisik.
- Semua shot moderate boleh. Tidak ada kuota tempo, jumlah fase atau jumlah jenis gerakan.

### 3.3 Cara mengamati

Lihat perjalanan utuh lalu baseline berurutan. Tentukan depth → translation → rotation sebelum menyimpulkan setiap fase.

1. Pilih jangkar utama, benda dekat dan benda jauh yang benar-benar terlihat.
2. Bandingkan ukuran, tutup-buka lapisan, perubahan sisi benda dan orientasi bidang per interval.
3. Periksa apakah ada bagian awal berbeda, komponen mulai/berhenti atau perubahan arah; jangan merata-ratakan seluruh take.
4. Bedakan Pan dari Orbit/Truck memakai gabungan petunjuk. Oklusi saja atau satu arah geser layar bukan bukti tunggal.
5. Catat gerakan sederhana dan teknis dari keputusan yang sama. Perubahan area tidak otomatis fase/cut.
6. Abaikan jitter/drift vertikal tipis. Tilt adalah rotasi vertikal berkelanjutan yang terlihat; tidak harus ekstrem. Crane/Pedestal berbeda dari Tilt.

Baseline tetap 6 FPS serta batas native awal/akhir; sumber ≤6 FPS dan shot <1 detik seluruh native. Contact sheet 6–10 momen boleh menjadi ringkasan dari baseline yang sama, bukan pengganti atau penurunan baseline. Sampel 6–10 frame per shot tidak disamakan dengan 6 FPS. Cut memakai indeks dan PTS native sumber, tidak diasumsikan selalu 30 FPS.

## 4. Versi target dan kompatibilitas

| Komponen | Saat ini | Target |
| --- | --- | --- |
| Sumber / paket | 2.4 | 2.5 |
| Report / template | 2.2.3 | 2.2.4; struktur manusia sama |
| Media / layout | 2.2.0 | 2.2.1; perbaikan caption |
| Reader / index | 2.4 | 2.5 |
| Generator | 7 | 8 |
| Sampling | 6 FPS adaptif | Tetap |
| Font | Font terdaftar saat ini | Tetap byte yang sama |

Pelonggaran aturan serta metadata parser baru hanya untuk 2.5. Format 2.4 tetap kewajiban angka asal; 2.3 tetap pengukuran ~× asal; 2.2 tetap baseline 10 FPS. Semua cabang lama dan literal sumber tetap tersedia. Tidak mengonversi ZIP pilot atau referensi aktif diam-diam.

Renderer/template/layout/engine lama tidak ditimpa. Perbaikan byte gambar memakai implementasi dan layout baru. Cache baru terpisah berdasarkan sumber, versi engine/parser/layout dan konfigurasi. Versi target baru diaktifkan setelah integrasi dan pemeriksaan selesai.

## 5. Urutan implementasi

### Tahap 1 — Bekukan spesifikasi dan selaraskan panduan

- Jadikan bagian 3 plan ini acuan penerimaan format baru; contoh tanpa angka sama pentingnya dengan contoh berangka.
- Adaptasi panduan eksperimen ke audit/visual-audit.md dan dokumen contoh kasus di kit; dokumen eksperimen asli dipertahankan.
- Catat rumus/ambang eksperimen sebagai heuristik, bukan batas universal. Bawah/atas gambar tidak otomatis dekat/jauh; skala global tidak otomatis Dolly; selisih flow tidak otomatis Orbit.
- Pertahankan cara baca visual dan estimasi yang praktis. Tidak menambah tabel pembuktian atau disclaimer ke analysis.md.
- Selaraskan panduan JSON, vocabulary, rubric dan prompt, termasuk intensitas vs tempo serta jumlah fakta tanpa kuota.

Selesai: daftar contoh diterima/ditolak dan batas tanggung jawab AI/helper/validator jelas sebelum kode diubah.

### Tahap 2 — Tambahkan kontrak, parser dan validator 2.5

- Tambahkan schema sumber/manifest/reader/index serta pasangan report/media baru.
- Buat parser kamera berversi yang mengembalikan movement dasar, direction, qualifiers, estimates, toward dan raw. Pakai field yang sudah tersedia; tidak membuat sumber fakta kedua.
- Pertahankan parser legacy beserta keluarannya. Models, complete dan preflight memakai parser yang sama menurut versi, bukan regex terpisah.
- Pertahankan raw klausa, intensitas, lintasan, easing dan angka; label baru yang tidak dikenal tidak dihapus.
- Normalisasi mekanis hanya pada sumber kerja 2.5; jangan menebak komponen/fase/tempo/sudut atau menambah angka yang tidak ditulis auditor.
- Lepaskan kewajiban angka dan alasan ketiadaan angka pada 2.5. Basis gerakan dan evidence tetap diperlukan; confidence mengikuti pengamatan, bukan isian angka.
- Angka yang ditulis tetap diperiksa: unit relevan, berhingga positif, urutan rentang, kurung dan konsistensi pengukuran bila tersedia.
- Atasi gabungan (~35°, Ease-Out), variasi x/×, desimal koma/titik serta ~1.75× tanpa mengubah nilai.
- Parsed metadata dan camera_summary harus sama pada source → preflight → draft → reader. Fase tetap sumber urutan, bukan diturunkan AI oleh generator.

Selesai: seluruh contoh bagian 3 lulus pada 2.5; format lama mempertahankan hasil validasi/parser/golden asal.

### Tahap 3 — Perbaiki ekstraksi batch lintas lingkungan

- Pecah frame hilang menjadi batch terbatas sebelum membentuk ekspresi FFmpeg; satu panggilan extract_many dapat menjalankan beberapa batch.
- Tambahkan pemulihan bounded split pada kegagalan parser/panjang ekspresi yang relevan; jangan retry semua error tanpa membedakan sumber rusak, izin atau timeout.
- Frame yang sudah berhasil disimpan dengan hash dan dapat digunakan resume. Tidak mengulang seluruh baseline.
- Urutan indeks/PTS, jumlah JPEG dan frame sumber tetap benar; ekstraksi tidak menyatakan viewed.
- Ukur panggilan FFmpeg, frame baru/hit, durasi dan retry di log workspace. Quota, timeout, symlink dan deteksi perubahan sumber tetap berlaku.
- Jangan mengganti extractor kanonis media final. Sampling batch dan media final tetap memiliki peran berbeda.

Selesai: kasus 132 frame dan frame cache parsial berhasil tanpa patch manual, termasuk jalur kegagalan yang direproduksi pada lingkungan FFmpeg lama.

### Tahap 4 — Tambahkan bantuan analisis per interval

Antarmuka target, **belum tersedia**: motion-hints pada tools/audit.py, menerima session/shot dan rentang opsional; keluaran di workspace.

- Gunakan frame cache/PTS yang sudah tersedia, bukan mengekstrak atau melakukan random seek ulang pada setiap pasangan.
- Pilih pasangan interval dari baseline; proses pada ukuran analisis yang dibatasi. Gunakan Δt sebenarnya, terutama pada VFR.
- Helper menghasilkan perubahan skala 2D, pergeseran dan statistik flow per interval, jumlah titik/inlier serta status cukup/tidak cukup. Tidak menghasilkan verdict Dolly/Pan/Orbit, confidence atau fakta desain.
- AI memeriksa jangkar dekat/jauh dan perspektif. Zona atas/bawah hanya petunjuk lokasi; tidak dipromosikan menjadi kedalaman pasti.
- Normalisasi perpindahan terhadap ukuran gambar dan waktu. Tidak memakai >20–30 px, persentase geser, atau FOV 50°–65° sebagai ambang universal untuk semua sumber.
- Flow menjadi pendamping otomatis yang dipanggil terutama untuk pertanyaan gabungan/ambigu. Tidak wajib pada setiap shot dan tidak mensyaratkan proof numerik agar audit dapat dilanjutkan.
- Dependensi OpenCV/NumPy bersifat opsional dan dimuat hanya ketika helper dipakai. Jika tidak tersedia atau tracking gagal, laporkan keterbatasan helper lalu lanjutkan pemeriksaan visual; tanpa instalasi jaringan rutin.
- Tidak memakai SIFT, pose3D atau rekonstruksi kamera sebagai langkah standar. Tambahkan log waktu helper; batasi satu analisis tersimpan per sumber/rentang/parameter yang sama.
- Hasil statistik tetap workspace; auditor boleh mengutip pengamatan ringkas pada field existing. Tidak memasukkan tabel flow/session/cache ke ZIP atau knowledge.
- Tidak menambah detektor cut otomatis sebagai kewajiban baru. Cut nyata tetap dikonfirmasi auditor memakai sumber native.

Selesai: helper dapat membantu membaca arah/fase tanpa mengambil alih keputusan, tidak menulis audit.json atau viewed, dan tidak membuat audit bergantung pada paket opsional.

### Tahap 5 — Lengkapi fakta desain tanpa memperberat laporan

- Saat audit, AI menginventaris temuan penting pada facts[] terlebih dahulu atau bersamaan dengan narasi, lalu mencocokkan ketiganya: arsitektur, furnitur/dekorasi dan lingkungan.
- Detail pembeda yang ditemukan harus terwakili: misalnya bentuk/layout, bukaan, storage, countertop, pencahayaan, peralatan dan orientasi. Tidak ada enam fakta wajib atau jumlah minimum baru.
- Klaim dipisahkan bila atribut/statusnya berbeda; boleh menggabungkan uraian satu konfigurasi yang memang satu temuan. Hindari duplikasi demi memperbanyak fakta.
- fact_coverage memakai tautan fakta yang relevan pada area/kategori. facet_roles eksplisit, sesuai makna temuan; tidak menyamakan balok plafon dengan massing hanya untuk mengisi label.
- Perkuat pemeriksaan deterministik ID, area, evidence, duplikasi dan metadata coverage; tampilkan ringkasan singkat pada review kerja untuk membantu AI menemukan bagian yang belum tercatat.
- Kecocokan makna narasi–fakta tetap diperiksa AI saat audit/koreksi di chat. Validator tidak mengklaim dapat membuktikan kelengkapan prosa; generator tidak mengekstrak atau mengarang fakta.
- Tidak menambah JSON isi kedua atau daftar pembuktian pada MD. Setelah ingest tidak ada review isi tambahan oleh pengguna.

Selesai: fixture dan contoh memperlihatkan variasi detail nyata per area; fakta yang ditulis benar-benar terbawa ke facet/pointer/knowledge, tanpa kuota jumlah.

### Tahap 6 — Perbaiki caption pada media baru dan daftarkan laporan

- Tambahkan media 2.2.1 dan report/template 2.2.4. Jangan mengedit media_v2_2.py, layout 2.2.0 atau renderer/template lama.
- Caption panel normal: Start · 8.37s, Middle · 9.93s, End · 11.50s. Label lebih tebal, waktu lebih kecil; keduanya di bawah gambar, tanpa mengulang shot-ID.
- Header tetap SHOT 03 · Kitchen dengan rentang/durasi di samping kanan. Tidak memindahkan daftar waktu panel ke header.
- Multi area: Start/End tetap; panel antara memakai label area/reveal yang berguna dan waktu. Jumlah panel dinamis, tidak dipaksa lima.
- Overview tetap seluruh pilihan wide satu baris. Storyboard tetap seluruh kolase vertikal. Header identitas: ID referensi – gaya utama English – durasi – jumlah shot.
- Font, ukuran judul dan hierarki yang disetujui dipertahankan; hanya perubahan caption yang diperlukan. Bar hitam bawaan sumber tidak di-crop otomatis.
- Catat bbox/provenance dari layout baru; crop/read panel tetap benar. Jalur cache/subset harus byte-identik dengan render penuh **versi baru yang sama**.
- Laporan tetap enam bagian/A-B-C dan literal kamera yang sama dengan JSON. Tidak menambah tabel kerja, FOV atau log.

Selesai: preview normal dan multi area terbaca rapi, golden media/MD versi baru lulus, byte media lama tidak berubah.

### Tahap 7 — Integrasikan pembaca AI, CLI, kit dan dokumentasi

- Reader/index 2.5 dan generator 8 menerima cabang sumber baru dan semua format lama.
- Indeks tetap ringkas: gerak dasar dan qualifier eksplisit yang diperlukan, beserta pointer sumber. Jangan menyalin flow/log/checks lengkap ke indeks.
- Pencarian/read mempertahankan Straight/Diagonal/Pure, intensitas dan easing. Bila menambah filter, gunakan nilai eksplisit parser, bukan inferensi prosa; pertahankan default antarmuka lama.
- Ease-Out pada Pan tidak berubah menjadi tempo slow, dan label Moderate Pan tidak berubah menjadi tempo moderate.
- Perbarui seluruh hard-coded cabang versi pada session, cache, complete, preflight, draft/export, validation dan reporting. Session lama tidak diubah menjadi session baru diam-diam.
- Perbarui template/contoh normal/multi serta bundel studi kasus. Studi kasus sintetik untuk tes diberi label; kasus eksperimen tidak diklaim telah diaudit ulang.
- Kit tetap empat file input luar bila memungkinkan; semua resource baru berhash. Dependensi helper opsional dijelaskan tanpa membebani bootstrap normal.
- Prompt menuntun pengamatan → simpulan → serialisasi, dengan progres singkat dan panduan dibaca sesuai tahap. Koreksi memakai cache dan pekerjaan terdahulu.
- Larangan video tetap berlaku pada 2.5, termasuk varian ekstensi. ZIP hanya audit.json, analysis.md, manifest.json dan media terdaftar.
- Selaraskan status pilot: dua run 2.4 sudah tersedia/diperiksa; belum disetujui atau di-ingest. Catatan lama dipertahankan sebagai riwayat.
- Aktifkan default baru setelah integrasi, lalu bangun kit dan keluaran generator dari sumber resmi.

Selesai: workflow portable normal/multi berjalan melalui CLI resmi, reader tidak kehilangan makna notasi baru, dan kandidat lama tetap dapat diverifikasi.

### Tahap 8 — Jalankan regresi dan benchmark teknis

Pengujian wajib berfokus pada perilaku yang berisiko, bukan menyalin implementasi:

1. Matriks notasi sepuluh studi kasus serta contoh bagian 3; tanpa angka sah pada medium/high, angka tunggal/rentang sah, confidence rendah bukan syarat menghilangkan sudut.
2. Parser source/complete/preflight/reader konsisten; raw dan qualifier dipertahankan. Label baru, negasi dan uncertainty tidak hilang.
3. Ease-Out per komponen, intensitas vs tempo dan fase campuran; camera_summary/Camera Pattern tetap mengikuti fase/depth.
4. Batch 132/lebih besar, cache parsial, bounded retry, output kurang/rusak, timeout, source berubah, symlink dan quota. Jalur media lama tetap byte-identik.
5. Motion helper pada pola sintetis dengan nilai transformasi yang diketahui; Δt VFR, tracking tidak cukup, dependensi tidak tersedia, no-mutation audit/viewed dan reuse cache.
6. Tes helper nyata dengan OpenCV/NumPy dipasang di lingkungan pengujian tersendiri; tidak cukup hanya mock atau semua tes helper di-skip. Catat versi dependensi/FFmpeg yang benar-benar diuji.
7. Coverage/facet/pointer lengkap untuk contoh kaya detail; validator tidak membuat klaim kelengkapan semantik yang tidak diperiksa.
8. Media baru normal/multi/label panjang/angka rentang: glyph ×/°/→, ukuran waktu, wrap, bbox, crop, Overview/Storyboard; subset/cache vs full byte-identik.
9. Golden MD enam bagian, literal kamera dan urutan media; font/layout/renderer lama tidak berubah.
10. Preflight input invalid sebelum render; receipt usang ditolak; ekspor tanpa render ulang dan byte sama; ingest/replay hanya di root fixture.
11. Reader campuran legacy–2.5 dan skala ratusan model: indeks ringkas, filter/pointer benar, tanpa flow/cache/log dalam output.
12. Kit dipulihkan ke workspace kosong, alur normal/multi dan koreksi berjalan dengan CLI; video/receipt/cache tidak masuk ZIP final.

Perintah verifikasi:

~~~sh
python -m unittest discover -s tests -t . -v
python tools/library.py build
python tools/library.py check
python tools/build_audit_kit.py --check
git diff --check
~~~

Benchmark lokal: prepare cold/resume, ekstraksi batch yang sebelumnya gagal, helper off/on, check-input, draft cold/warm dan koreksi kamera/metadata. Catat panggilan FFmpeg, frame baru, waktu dan byte output. Jangan menjanjikan durasi audit provider dari benchmark lokal. Uji kompatibilitas FFmpeg 5.1 bila lingkungan tersedia; bila tidak, catat belum terverifikasi dan gunakan simulasi gagal parser sebagai regresi tambahan, bukan pengganti klaim uji nyata.

Selesai: checks lulus, versi yang diuji tercatat, integritas referensi/artefak lama terjaga, batas verifikasi dilaporkan.

### Tahap 9 — Ulang pilot dan catat hasil nyata

- Pengguna menjalankan edh058 di chat baru ChatGPT dan Gemini memakai kit baru dan MP4 kanonis yang sama.
- Simpan run terpisah audit/result/<provider>/v2.5/run-NN/; jangan menimpa ZIP/laporan 2.4.
- Bandingkan arah, Dolly/Pan/Orbit, fase, ritme, estimasi yang berguna, Camera Start/Overview, detail rumah, fakta terstruktur, MD serta seluruh media.
- Gerakan tanpa derajat tidak dianggap lebih buruk; angka lebih banyak dan semua label berbeda bukan ukuran mutu.
- Catat masalah ekstraksi, retry/patch manual, waktu kandidat siap, log alat dan koreksi. Pisahkan persetujuan/ekspor dari durasi audit.
- Tinjau keseluruhan di chat; ekspor hanya sesudah persetujuan nyata dan gunakan snapshot yang sama. Tidak otomatis meng-ingest hasil evaluasi.
- Lanjutkan edh013, edh033, edh049, edh056 dan dreamshome01 setelah alur memadai. edh001 tetap referensi aktif yang sudah diterima, bukan kewajiban audit ulang.
- Jika video sumber tiga eksperimen tersedia kemudian, audit ulang studi kasus dicatat sebagai verifikasi tambahan, bukan dianggap telah terjadi atau syarat baru yang menghalangi pilot.

Selesai: status tiap run, koreksi, persetujuan, ekspor dan ingest dicatat terpisah. Tooling selesai tidak berarti pilot selesai.

## 6. Peta perubahan file

Semua path relatif root repo. Baris telaah berarti edit hanya jika integrasi terpusat belum mencukupi; dokumentasikan bila tidak perlu berubah.

| Tindakan | File / kelompok | Tujuan |
| --- | --- | --- |
| Tambah | docs/contracts/package-v2-5.md, audit-v2-5.schema.json, manifest-v2-5.schema.json | Aturan kamera fleksibel, versi dan paket tanpa video |
| Tambah | docs/contracts/ai-reader-v2-5.md, reference-reader-v2-5.schema.json, search-index-v2-5.schema.json | Cabang baru, qualifier dan pointer; semua cabang lama |
| Tambah | docs/contracts/analysis-v2-2-4.md, tools/assets/templates/analysis-2.2.4.md, tools/homeku/reporting_v2_2_4.py | Renderer baru dengan enam bagian yang sama |
| Tambah | tools/homeku/camera_notation.py | Parser/normalisasi berversi, qualifier dan easing |
| Tambah | tools/homeku/motion_analysis.py | Statistik per interval, dependensi opsional, tanpa verdict otomatis |
| Tambah | requirements-audit-motion.txt | Dependensi opsional helper; versi kompatibel ditentukan lewat pengujian |
| Tambah | tools/homeku/media_v2_2_1.py, tools/assets/layouts/media-2.2.1.json | Caption sesuai kesepakatan tanpa menimpa media lama |
| Tambah | audit/camera-cases.md | Adaptasi sepuluh kasus dan jebakan; bukan kumpulan jawaban sumber baru |
| Ubah | tools/homeku/versions.py, __init__.py | Registrasi 2.5/report/media/reader baru dan generator 8 |
| Ubah/telaah | tools/homeku/markdown.py | Dispatcher parser baru tanpa mengubah perilaku parser lama |
| Ubah | tools/homeku/models.py, audit_quality.py, preflight.py | Validasi berversi, angka opsional, qualifier, easing dan coverage |
| Ubah | tools/homeku/authoring.py, audit_session.py, tools/audit.py | Default/session 2.5, complete mekanis, CLI motion-hints |
| Ubah | tools/homeku/video_cache.py, audit_performance.py | Batch kecil, bounded recovery, cache/log statistik |
| Telaah | tools/homeku/video.py, exporter.py, validation.py | Kompatibilitas sampling/PTS, format baru, no-video dan snapshot |
| Ubah | tools/homeku/media.py, media_incremental.py, reporting.py | Dispatch engine/layout baru, subset dan hash konfigurasi |
| Telaah | tools/homeku/report_validation.py | Struktur MD tetap; registrasi baru bila diperlukan |
| Ubah | tools/homeku/generation.py, reader.py, tools/library.py | Proyeksi/facet kamera eksplisit, read/filter tanpa inferensi |
| Telaah | tools/homeku/engine.py, camera_pattern.py | Versi sumber baru, pola kedalaman dan fingerprint |
| Telaah | data/taxonomy.json | Alias eksplisit istilah kamera bila perlu; label asli tetap |
| Ubah | audit/visual-audit.md, protocol.md, rubric.md, vocabulary.md | Metode per interval dan aturan angka/intensitas/tempo |
| Ubah | audit/README.md, authoring.md, json-guide.md, providers.md | Workflow ringan, helper opsional dan penanganan error |
| Ubah | audit/prompts/01-audit.md, 02-correct.md, 03-export.md | Pengamatan sebelum serialisasi, koreksi dan persetujuan snapshot |
| Ubah/telaah | audit/template-audit.json, template-audit-info.json, examples/normal/audit.json, examples/multi/audit.json | Default/contoh sumber baru; tanpa viewed/fakta otomatis |
| Ubah | tools/build_audit_kit.py | Bundel modul/kontrak/contoh baru, inventory/hash dan dependencies |
| Hasil builder | audit/homeku-audit-kit.zip | Kit baru melalui builder resmi |
| Ubah/tambah | tests/fixtures/factory.py, tests/fixtures/README.md, tests/fixtures/reports/*-2.2.4.md | Fixture terisolasi dan golden report baru |
| Tambah | tests/test_camera_notation.py, test_motion_analysis.py, test_audit_camera_workflow.py | Matriks notasi, statistik dan pipeline 2.5 |
| Ubah | tests/test_audit_cache.py, test_audit_authoring.py, test_audit_preflight.py, test_audit_efficiency.py | Batch recovery, defaults/session, angka opsional dan portabilitas |
| Ubah/telaah | tests/test_audit_method.py, test_audit_quality.py, test_v2_models.py, test_v2_media.py, test_v2_reader.py, test_v2_reporting.py, test_v2_1_compatibility.py, test_audit.py, test_library.py | Integrasi baru dan kompatibilitas lama |
| Ubah | tools/benchmark_audit.py | Benchmark batch/recovery/helper tanpa audit atau ingest produksi |
| Telaah | .github/workflows/library-ci.yml | Jalur uji helper dengan dependensi opsional, selain core suite |
| Ubah | README.md, AGENTS.md, docs/operations.md, docs/v2-field-map.md | Default baru dan aturan kerja yang konsisten |
| Ubah saat implementasi | audit/calibration.md, pilots/README.md, pilots/edh058-comparison.md | Hasil 2.4 nyata serta status 2.5 yang benar |
| Selaraskan saat implementasi | docs/audit-efficiency-implementation-plan.md, docs/audit-efficiency-verification.md | Catatan lanjutan 2.5 dan koreksi status run; hasil historis tetap |
| Tambah setelah pengujian | docs/audit-camera-verification.md | Hasil tes/benchmark, preview, hash kit dan status pilot nyata |
| Hasil generator | catalogs/, knowledge/, data/projections/, data/search-index.json, data/dependencies.json, data/build.json | Hanya lewat build, bukan edit fakta manual |

Pertahankan docs/panduan_audit_gerakan_kamera_ai.md sebagai sumber eksperimen. Jangan mengedit kontrak lama, renderer/template/layout/font terdaftar, bekerja/, video/, ZIP hasil provider, references/, registry atau ledger. sources/fact-facets.json tidak diubah tanpa kebutuhan mapping terkurasi yang nyata; generator tidak mengisi fakta dari prosa.

## 7. Kriteria selesai

| Status | Bukti yang diperlukan |
| --- | --- |
| Aturan sesuai kebutuhan | Contoh pengguna diterima; angka/derajat tidak diwajibkan per komponen; format tetap konsisten |
| Tooling selesai | Tahap 1–8 lulus, kit baru portable, tidak perlu patch manual pada kasus ekstraksi yang diuji |
| Media sesuai | Caption dan hierarki sesuai kesepakatan; media lama utuh; output baru tervalidasi |
| Pengetahuan AI terjaga | Detail pembeda menjadi fakta yang ditautkan, qualifier/pointer/status tidak hilang, indeks tetap ringkas |
| Peningkatan visual teramati | Hasil pilot nyata ditinjau, bukan disimpulkan dari jumlah frame atau tes parser |
| Referensi diterima | Persetujuan seluruh snapshot, ekspor byte sama, ingest hanya atas instruksi pengguna |

Implementasikan tahap **1 → 9** berurutan. Pada penyusunan awal dokumen ini hanya plan. Tooling/default/kit baru kini diimplementasikan; hasil provider dan referensi diterima tetap utuh. Lihat audit-camera-verification.md.

## Status implementasi nyata

| Tahap | Status |
| --- | --- |
|1|Panduan dan contoh eksperimen selaras; angka opsional |
|2|Kontrak/parser/validator2.5 terintegrasi; aturan lama tetap |
|3|Batch32, bounded retry, cache parsial/resume diuji |
|4|Helper opsional nyata diuji; tanpa API AI/verdict/viewed otomatis |
|5|Inventory fakta/coverage kerja terpisah; tanpa kuota/sintesis fakta |
|6|Media2.2.1/report2.2.4, preview normal/multi dan byte-parity lulus |
|7|Reader2.5/generator8/CLI/kit4file terintegrasi |
|8|214tes tanpa skip, build/check/kit/diff checks dan benchmark lulus |
|9|Panduan pilot siap; run nyata/koreksi/persetujuan/ekspor/ingest pengguna belum terjadi |

[Hasil verifikasi](audit-camera-verification.md). Implementasi tooling tidak menjadi persetujuan kandidat atau pengganti pilot pengguna.
