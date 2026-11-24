# Plan Improvement V2 — MD untuk Manusia, JSON sebagai Sumber Audit

> Status setelah reset 24 November 2026: data audit edh001 telah dihapus atas permintaan pengguna. Catatan edh001 di dokumen ini bersifat historis, bukan referensi aktif atau persetujuan audit baru.

**Kelanjutan Overview/Storyboard (23 November 2026):** format2.1/report2.2.0 dan reader2.1 tersedia; workflow/kit terbaru telah diselaraskan. edh001 r0003 telah disetujui, diekspor dan di-ingest; implementasi Overview/Storyboard selesai. Enam pilot pengguna tetap belum dinyatakan selesai. Lihat [plan berurutan](implementation-plan-overview-storyboard.md) dan [hasil/status terbaru](overview-storyboard-verification.md). Uraian versi sebelumnya di bawah dipertahankan sebagai riwayat.

Tanggal: 22 November 2026.

Status: **Tahap 1 (1.1–1.12) dan Tahap 2 langkah 2.1–2.10 telah selesai**; lihat [verifikasi fondasi](v2-stage-1-verification.md) dan [hasil Tahap 2](v2-stage-2-verification.md). Workflow/kit V2 siap; audit ulang edh001 telah disetujui pengguna lalu di-ingest sebagai r0002/2.0. Enam pilot pengguna (2.11) belum dijalankan dan kalibrasi lintas pilot (2.12) masih terbuka, sehingga keseluruhan Tahap 2 belum selesai. Template dan dua contoh laporan yang disetujui tetap menjadi acuan renderer 2.1.2; versi terdahulu didukung. [Verifikasi tampilan](v2-stage-1-media-verification.md) mencatat penyempurnaan sebelumnya. ZIP r0001 dipertahankan sebagai riwayat; perubahan referensi dilakukan melalui revisi eksplisit.

## 1. Tujuan dan keputusan utama

`analysis.md` menjadi laporan yang mudah dipahami manusia: terstruktur, lengkap untuk mengenali desain, ukuran, isi area dan kamera. Ringkas berarti menghindari pengulangan, bukan membatasi detail rumah menjadi satu paragraf. Seluruh data audit disimpan pada `audit.json`, yang menjadi sumber untuk otomasi dan pengetahuan AI.

Plan ini memperbarui ketentuan sumber isi, format laporan dan paket pada [plan utama](implementation-plan.md) serta [plan improvement sebelumnya](phase-2-audit-improvement-plan.md). Aturan sumber, tampilan dan media diganti untuk format V2 sesuai plan ini; audit adaptif, revisi ZIP, pemisahan arsip dan produksi tetap berlaku. Ketentuan legacy tentang frame terpisah dan storyboard vertikal tidak diterapkan pada paket V2. Kontrak dan AGENTS.md diselaraskan saat implementasi, bukan dianggap sudah berubah hanya karena plan ini dibuat.

Saat ini edh001 revisi 2 sudah aktif lokal dengan format 2.0 berbasis audit.json setelah persetujuan isi dan ingest ZIP revisi eksplisit. Enam pilot lain belum selesai. Perubahan V2 tidak mengubah isi atau hash paket aktif secara diam-diam. [Alur konsep V2](alur-konsep-desain-v2.md) menjelaskan penggunaan data oleh AI; ketentuan pembacaan dan pemilihan referensi pada Bagian 6 mendukung alur tersebut.

**Acuan penyajian yang sudah disetujui:** [template baku](template-analysis-v2.md), [contoh shot normal](contoh-analysis-shot-normal.md) dan [contoh shot multi area](contoh-analysis-shot-multi-area.md). Template menjadi acuan struktur renderer; kedua contoh memperlihatkan tingkat kelengkapan dan bahasa yang diharapkan. Isi contoh adalah simulasi, bukan referensi aktif atau bukti audit pilot.

**Cara membaca plan:** Bagian 2–6 menetapkan hasil dan aturan; Bagian 7 memetakan file yang diubah/ditambahkan; Bagian 8 mengatur audit ulang edh001; Bagian 9 merinci urutan Tahap 1 (1.1–1.12) dan Tahap 2 (2.1–2.12), pemeriksaan serta kriteria selesai masing-masing. File baru pada peta adalah target implementasi, bukan klaim sudah tersedia.

## 2. Pembagian file dan alur data

```text
references/<id>/
  audit.json           # Satu sumber seluruh isi audit
  analysis.md          # Laporan manusia, dihasilkan dari audit.json
  manifest.json        # Metadata sumber, audit teknis, media dan provenance
  media/
    storyboard.jpg     # Overview seluruh area, satu baris
    shot-01.jpg        # Satu kolase per shot
    shot-02.jpg        # Tiga panel atau panel dinamis sesuai jenis shot
    ...
```

| Komponen | Fungsi V2 |
| --- | --- |
| audit.json | Identitas gaya, ukuran/proporsi, narasi desain per kategori/area, fakta, komposisi, shot/area/rute, kamera teknis dan bahasa sederhana, profil tempo, hubungan, bukti dan ketidakpastian |
| analysis.md | Tampilan manusia; tidak menjadi sumber ekstraksi fakta atau pengetahuan |
| manifest.json | Identitas/hash/metadata video, cakupan pemeriksaan nyata dan inventaris media; tidak menduplikasi fakta desain |
| data/projections/<id>.json | JSON pembaca AI yang lengkap, dibangun dari audit.json dan manifest; terpisah dari metadata cache |
| Indeks, catalogs/ dan knowledge/ | Turunan deterministik dari sumber yang sama, termasuk prinsip umum terkurasi yang sudah tersedia |

Alur V2: **AI mengaudit → mengisi audit.json → helper membuat MD dan kartu → pengguna mengoreksi → sumber diperbarui dan tampilan dibuat ulang → pengguna menyetujui → satu ZIP final → incoming/ → ingest.**

AI menulis narasi desain yang lengkap, penjelasan kamera sederhana serta pilihan frame/panel saat audit dan menyimpannya dalam audit.json bersama fakta terstruktur. Renderer hanya menata data, gambar serta narasi sesuai template; generator tidak menjalankan AI, menerjemahkan gerak dengan tebakan atau mengekstrak fakta dari prosa. JSON sumber dan JSON proyeksi mempunyai peran berbeda dan tidak dikoreksi terpisah.

## 3. Format baku analysis.md

Gunakan [template baku V2](template-analysis-v2.md). Judul laporan **ID — nama desain rumah**, lalu lima bagian bernomor dalam urutan tetap: **1. Identitas desain; 2. Ukuran dan proporsi bangunan; 3. Struktur dan timeline video; 4. Storyboard; 5. Detail shot.** Tidak menyalin pengantar template, komentar petunjuk atau penanda kosong ke laporan final.

### A. Identitas desain

- **Nama desain rumah:** judul deskriptif yang mudah diingat; dibedakan dari nama resmi jika sumber menyediakannya.
- **Gaya utama:** nama gaya yang spesifik dan paling mewakili referensi.
- **Pengaruh gaya:** pengaruh pendukung yang sesuai, beserta alasan singkat; tidak wajib mengisi banyak label.
- **Gaya interior:** karakter interior keseluruhan; perbedaan penting tiap area dicatat pada shot terkait.
- **Ciri pengenal:** dua atau tiga ciri yang membantu manusia memahami nama gayanya.
- **Palet utama:** warna dan tampilan material dominan.
- **Suasana dan lingkungan:** karakter cahaya serta lingkungan yang terlihat.

Nama gaya wajib tampil tersendiri. Nama gaya utama, pengaruh gaya serta gaya interior memakai istilah bahasa Inggris; penjelasan tetap bahasa Indonesia. Renderer 2.1.x memerlukan deklarasi identity.style_names_language=en tanpa menerjemahkan atau menebak nama gaya. Organic Modern Cottage dan American Cottage pada pembahasan/contoh bukan label wajib atau penetapan baru untuk edh001. Label asli dipertahankan; alasan penamaan gaya disimpan dalam JSON.

### B. Ukuran dan proporsi bangunan

| Aspek | Isi |
| --- | --- |
| Ukuran rumah | Label kesan ukuran, misalnya tiny/small/medium/large |
| Bentuk bangunan | Bentuk dan susunan massa yang terlihat |
| Skala vertikal | Tingkat yang terlihat serta bentuk bagian atas bangunan |
| Tapak bangunan | Kesan bentuk/cakupan tapak dari sumber |
| Proporsi utama | Hubungan lebar, tinggi atau panjang yang menonjol |
| Perkiraan luas lantai | Wajib rentang angka m² |

**Ketentuan wajib luas lantai:** AI harus menghasilkan rentang estimasi visual; field tidak boleh kosong, null, unknown atau dijawab “belum dapat diperkirakan”. AI memakai gabungan massa eksterior, tingkat dan proporsi ruang/furnitur. Petunjuk yang terbatas ditangani melalui rentang yang sesuai, bukan melewati estimasi. Luas berarti perkiraan total lantai rumah yang direpresentasikan, bukan luas lahan atau penjumlahan luas setiap shot.

Tampilan MD cukup:

| Aspek | Estimasi visual |
| --- | --- |
| Perkiraan luas lantai | **60–90 m²** |

Angka tersebut hanya contoh format. Jangan menambahkan “estimasi kasar”, “kepastian rendah”, dasar perkiraan atau paragraf pembenaran luas pada MD. Penanda estimasi, dasar/asumsi dan ketidakpastian disimpan dalam JSON. Validasi memeriksa rentang angka positif dan berurutan, bukan mengklaim luas tersebut telah diukur.

### C. Struktur dan timeline video

Awali dengan durasi total, jumlah shot dan cut/kontinuitas secara singkat. Tabel utama memakai gerakan bahasa manusia agar mudah dipindai:

| Shot | Waktu (detik) | Durasi | Area/Scene | Gerakan singkat | Ritme |
| --- | --- | --- | --- | --- | --- |
| Nomor shot | Rentang waktu sumber | Dihitung dari rentang | Area atau urutan area | Ringkasan bahasa sederhana | Tempo/perubahannya |

Satu baris untuk satu shot, bukan satu area. Notasi teknis lengkap ditempatkan pada detail shot. Waktu/durasi berasal dari sumber, tanpa default produksi 4/6 detik; pembulatan tampilan tidak menghilangkan presisi JSON. Ringkasan, kartu, detail dan proyeksi harus sejalan dengan data kamera yang sama meskipun bentuk penyajiannya berbeda.

### D. Media: satu kolase per shot dan storyboard satu baris

Paket final menyimpan **satu JPEG kolase untuk setiap shot dan satu storyboard per referensi**. Detail shot menampilkan `media/shot-NN.jpg`, bukan gambar overview tunggal. Tidak menyimpan start/middle/end, overview, reveal atau detail sebagai JPEG tambahan. Frame sumber dipakai sementara untuk merakit gambar; sumber video kanonis tetap disimpan satu kali. Ini mengubah penyimpanan media V2, bukan mengurangi cakupan audit.

| Jenis | Pemilihan dan susunan panel |
| --- | --- |
| Satu shot satu area | Tepat **3 panel: awal → tengah → akhir**, disusun 3 kolom dalam satu baris |
| Satu shot multi area | **Jumlah dinamis**: awal, akhir dan momen penting yang cukup menjelaskan area, penghubung/reveal serta perubahan sudut/fokus; tidak wajib 5 panel |
| Storyboard | Overview seluruh area penting dalam **satu baris**, mengikuti urutan shot/kemunculan area; nomor shot yang sama dipertahankan jika beberapa overview berasal dari satu shot multi area |

**Prinsip panel dinamis:** pilih jumlah paling sedikit yang tetap menjelaskan seluruh perjalanan penting. Satu panel boleh mewakili beberapa area atau fungsi sekaligus. Jangan menambah panel untuk setiap fase jika gambarnya tidak memberi informasi baru; jangan membagi durasi menjadi lima bagian sama rata. Awal/akhir tetap terwakili. Jumlah panel tidak dibatasi angka tetap yang menghilangkan area/penghubung penting. Pemilihan momen dilakukan auditor dan dicatat eksplisit, bukan ditebak generator dari narasi.

Panel kolase mengikuti waktu sumber dari kiri ke kanan; bila satu baris terlalu panjang untuk dibaca, multi area boleh memakai dua baris atau tata letak lanjutan sesuai jumlah/rasio panel. Urutan baca dan nomor panel harus jelas. Storyboard tetap satu baris. Pemilihan tata letak mempertimbangkan keterbacaan, dimensi dan batas ukuran paket, tanpa memperkecil setiap panel sampai detail hilang.

**Overview tetap ada sebagai pilihan frame, bukan file mandiri.** Pilih frame asli dengan cakupan area paling jelas, biasanya awal IN/akhir OUT, dengan alasan bila berbeda. Storyboard berisi satu gambaran representatif per area penting; satu frame yang jelas mencakup dua area tidak harus disalin dua kali. Jika multi area membutuhkan beberapa gambaran, beri label seperti Shot 01 · Exterior, Shot 01 · Living dan Shot 01 · Kitchen. Panel storyboard bukan shot baru. Overview boleh sama dengan panel kolase atau diambil dari frame sumber lain; asalnya tetap tercatat meskipun JPEG frame terpisah tidak disimpan.

**Tampilan baku:** renderer 2.1.2 mempertahankan ukuran judul/nama area 15% lebih kecil dari 2.1.0, termasuk storyboard. Header kolase cukup judul beserta rentang waktu dan durasi pada satu baris bila muat. Di bawah tiap foto, label Start/Middle/End atau nomor/momen multi area ditulis bold, diikuti timestamp regular yang lebih kecil (sekitar 75% ukuran label), sejajar pada baseline yang sama. Tidak ada daftar timestamp semua panel dalam header. Header storyboard tetap ID — Primary style — durasi x.xxs — jumlah shot; tiap area memiliki nama bold lalu Overview · x.xxs dengan font waktu lebih kecil. Caption panjang membungkus di luar foto. Dua desimal hanya tampilan; presisi/pointer JSON tetap. Versi sebelumnya beserta template/fontnya dipertahankan. Gaya acuan lama hanya untuk tata letak, bukan sumber label gerak.

**Resolusi dan ukuran:** pertahankan rasio serta detail frame asli, tanpa crop yang membuang konteks atau pembesaran generatif. Resolusi kolase mengikuti ukuran panel dan tata letak, bukan memperbesar sumber secara semu. Kompresi JPEG dapat dikonfigurasi untuk menyeimbangkan detail dan ukuran. Ukur jumlah byte media/ZIP sebelum–sesudah pada pilot; jumlah file lebih sedikit tidak dianggap jaminan penghematan. Seluruh frame audit dan potongan panel sementara tetap di workspace kerja, bukan paket/Git.

### E. Detail shot: tiga kelompok tetap

Kartu berada di bawah bagian **5. Detail shot**, memakai judul **Shot NN — area/urutan area · durasi**. Tampilkan kolase shot dan keterangan singkat urutan panel sebelum kelompok A/B/C. Awal/tengah/akhir atau momen perjalanan terbaca pada label panel; referensikan panel awal saat overview storyboard berasal dari akhir OUT. Pisahkan antarkartu dengan garis horizontal.

| Kelompok | Susunan wajib |
| --- | --- |
| **A. Desain area** | **Arsitektur**, **Furnitur dan properti**, **Lingkungan**; setiap kategori berupa paragraf konkret dan lengkap |
| **B. Komposisi dan cahaya** | Tabel dua kolom: fokus utama, posisi/arah kamera awal, framing awal → akhir dan pencahayaan; multi area menambahkan area terlihat, rute dan hubungan antararea |
| **C. Gerakan kamera** | Bahasa sederhana → ritme → DNA perjalanan bila berlaku → timeline gerakan bila berlaku → notasi teknis lengkap |

**Arsitektur** menjelaskan bentuk/susunan ruang, dinding, plafon, lantai, bukaan, kabinet, material tampak dan penempatan lampu. **Furnitur dan properti** menjelaskan bentuk, posisi, susunan serta hubungan furnitur/peralatan/dekorasi/penyimpanan/tanaman yang terlihat. **Lingkungan** menjelaskan pemandangan melalui bukaan, taman, vegetasi, bangunan sekitar, cuaca dan hubungan dengan luar. Tidak memaksa objek atau lingkungan yang tidak terlihat. Bidang pencahayaan menjelaskan sumber, arah dan karakter cahaya; hindari mengulang inventaris lampu.

Pada shot normal, paragraf menjelaskan area terkait. Pada multi area, gunakan penanda **Nama area.** pada paragraf dalam setiap kategori, mengikuti urutan kemunculan. Ini tetap satu laporan shot, bukan subshot 01A/01B atau laporan kamera per ruang. Panjang mengikuti kekayaan desain, tidak dibatasi satu paragraf untuk seluruh isi shot.

**Bahasa kamera sederhana** wajib singkat tetapi lengkap: perpindahan kamera, perubahan arah pandang, target, urutan atau kebersamaan dan perubahan penting. Melangkah melingkar ke kiri dibedakan dari memutar pandangan ke kanan. Penjelasan dibuat AI saat audit; renderer tidak menafsirkan notasi menjadi prosa baru. Ritme menjelaskan tempo awal, akhir dan perubahan penting. Notasi Inggris mempertahankan `+`, `→`, estimasi `~×/~°` serta kronologi sumber; rasio skala bukan kelipatan kecepatan.

**Timeline gerakan** wajib pada multi area atau shot beberapa fase; shot normal satu fase boleh tidak menampilkannya. Kolom: **Waktu (detik) | Area dan fokus | Gerakan Kamera | Ritme**. Interval mengacu ke awal video, mengikuti perubahan komponen kamera dan mencakup shot secara berurutan; pergantian area atau tempo saja tidak memaksa fase baru. DNA perjalanan wajib untuk multi area, menjelaskan pola lintasan, peralihan fokus/reveal dan ritmenya; pada normal hanya ditampilkan bila menambah informasi penting.

### F. Definisi satu shot dan dukungan multi area

Satu shot adalah satu pengambilan berkelanjutan sampai batas cut/transisi pengambilan yang diamati. Exterior → living → kitchen tanpa cut tetap **Shot 01**. Sebaliknya, tiga cut pada area sama tetap beberapa shot. Pergantian label area, perubahan fokus, belokan atau fase gerak tidak membuat shot baru.

**Area berbeda dari fungsi:** satu bathroom yang juga memuat laundry dapat tetap satu area dengan dua fungsi. Label kitchen/living yang terlihat bersamaan juga tidak otomatis membuktikan kamera berpindah ruang. Gunakan identitas area yang stabil, daftar fungsi, kemunculan visual dan rute yang dibedakan. Dua living yang berbeda tidak digabung hanya karena label fungsinya sama; tipe perjalanan ditentukan dari pengamatan.

Untuk multi area, audit mencatat:

- **Area terlihat:** area dan waktu kemunculannya; beberapa area dapat tampil bersamaan, hilang lalu muncul kembali.
- **Rute kamera:** lokasi yang benar-benar dilalui; kitchen dapat terlihat dari living tanpa kamera memasuki kitchen. Waktu terlihat dan waktu kamera masuk dibedakan, tanpa mengarang waktu yang tidak didukung.
- **Desain per area:** narasi/fakta tetap terkait area yang tepat di dalam shot; informasi bersama dapat berlaku pada beberapa area.
- **Penghubung dan orientasi:** pintu, koridor, bukaan/open plan serta elemen penanda kesinambungan yang terlihat.
- **Satu perjalanan kamera:** fase, jangkar, target, posisi/framing dan tempo sepanjang shot; satu fase boleh melewati beberapa area dan satu area boleh muncul pada beberapa fase.

Baseline 10 FPS mencakup seluruh shot, termasuk penghubung dan pergantian fokus; pendalaman native dilakukan pada rentang meragukan. Bukti tiap area/fase merujuk waktu dan media yang sesuai. Metode ini tidak mewajibkan penyimpanan seluruh frame.

## 4. Aturan keterbacaan dan kelengkapan

- Gunakan bahasa Indonesia sehari-hari. Nama gaya dan notasi kamera dapat memakai istilah Inggris yang relevan.
- Tidak ada tabel fakta teknis, hash, jumlah frame, ID klaim, log pemeriksaan atau penjelasan parser dalam laporan manusia.
- Tidak ada pengulangan panjang antara identitas, ringkasan dan detail. Jangan menambahkan bagian ringkasan yang hanya mengulang seluruh identitas desain.
- Tidak menetapkan batas keras 400–650 kata yang menghapus informasi wajib. Ringkas dicapai melalui paragraf pendek, bidang yang jelas dan penghapusan pengulangan.
- JSON tetap menyimpan kedalaman audit: arsitektur, susunan/fungsi, furnitur, penyimpanan, dekorasi, material tampak, cahaya, lingkungan, hubungan, bukti serta batas pengamatan. Tidak ada kuota furnitur generik.
- Status pengamatan/tafsir/negasi dan label baru tetap terjaga di JSON. MD menampilkan catatan penting sesuai kebutuhan pembaca, bukan semua rincian pembuktian.
- Buat pemetaan bidang lama → JSON V2 agar profil, fakta, narasi penting, hubungan, kamera dan bukti tidak hilang saat migrasi. Identitas klaim dan pointer sumber tetap dapat dilacak.
- Narasi desain per kategori/area, bahasa kamera sederhana dan data terstruktur diperiksa silang oleh AI saat audit/koreksi sebelum ekspor. Nilai bersama seperti waktu, gaya dan notasi kamera diambil dari field yang sama saat render; validator memeriksa konsistensi teknis, bukan mengklaim memahami seluruh makna prosa.
- Renderer mempertahankan heading, urutan, tabel dan aturan bagian opsional pada template; laporan final tidak memuat komentar petunjuk, penanda kosong atau baris yang tidak berlaku. Template dan renderer dijaga selaras, tanpa dua susunan yang dirawat terpisah.

## 5. Kontrak JSON, paket dan snapshot final

Tetapkan kontrak paket/sumber **2.0 provisional** serta kontrak pembaca AI dan indeks **2.0** untuk perubahan antarmuka ini. Pembaca tetap mempunyai jalur eksplisit untuk paket 1.0/1.1; versi tidak ditebak dari keberadaan file atau bentuk narasi. Nomor versi registry/taksonomi diputuskan sesuai perubahan strukturnya sendiri, bukan otomatis disamakan dengan nomor paket.

| Data sumber | Penambahan/penyesuaian |
| --- | --- |
| Identitas desain | Nama desain, gaya utama/pengaruh/interior, hubungan keluarga gaya, ciri pengenal, palet dan lingkungan; label asli dipertahankan |
| Ukuran/proporsi | Label ukuran, bentuk, skala vertikal, tapak, proporsi dan rentang luas lantai wajib; rincian estimasi tetap dalam JSON |
| Shot/area | Identitas shot dan kontinuitas, daftar area beridentitas stabil dalam shot, narasi arsitektur/furnitur-properti/lingkungan, konfigurasi yang dapat dicari, fokus, posisi/framing, cahaya serta fakta/bukti terkait area atau lingkup bersama |
| Perjalanan | Kemunculan area yang dapat bertumpang tindih/berulang, rute/lokasi yang dilalui jika diketahui, penghubung dan penanda orientasi, waktu peralihan serta DNA perjalanan; tidak memecah shot per area |
| Kamera | Ringkasan literal, ringkasan manusia, penjelasan lengkap sederhana, fase/timestamp, estimasi, jangkar/target dan rujukan area, profil tempo/perubahan laju, dasar dan ketidakpastian |
| Hubungan/batas | Hubungan antararea dalam shot dan antarshot, serta informasi tidak terlihat/tidak hadir/belum diketahui |
| Provenance | Pointer JSON sumber, identitas klaim, media/panel, indeks frame dan PTS sumber, status serta metadata sumber terkait |

Schema membedakan interval shot, fase kamera dan kemunculan area. Referensi area/fase/media harus valid dan berada dalam shot yang tepat. Interval fase berurutan tanpa gap/overlap; interval kemunculan area boleh bertumpang tindih atau berulang. Rute tidak disimpulkan dari daftar area terlihat. Timestamp yang tidak diketahui tetap berstatus sesuai pengamatan; metadata bukan klaim lokasi/ukuran fisik yang terukur. Nama field final ditetapkan dalam schema saat implementasi.

**Satu sumber pilihan panel:** audit.json menyimpan identitas panel, frame/PTS pilihan, area, peran, caption serta alasan pemilihan yang ditulis auditor. Manifest menyimpan hasil teknis aktual: file/hash/dimensi, penempatan foto dan rujukan ke pilihan panel tersebut. Metadata yang diulang untuk pemeriksaan konsistensi harus dihasilkan otomatis, bukan menjadi isi kedua yang diedit terpisah.

**Kontrak media komposit:** manifest menginventarisasi satu file per kolase/storyboard beserta hash, dimensi dan urutan panel. Setiap panel beridentitas stabil dan mencatat shot/area terkait, peran/keterangan, indeks frame/PTS sumber serta batas bagian foto dalam koordinat gambar kolase. Simpan hubungan ke sumber video, rasio/skala penempatan dan alasan pilihan overview/momen penting; tidak merujuk path frame sementara yang tidak dikirim. Header dan caption bukan bagian bukti visual foto.

Fakta/fase merujuk panel dan waktu sumber yang tepat, bukan menganggap kolase sebagai satu timestamp. Tooling dapat mengambil bagian foto panel atau mengekstrak ulang frame dari video bila perlu, tanpa menyimpan salinan panel permanen. Pointer bukti lama dipetakan ke panel/frame sumber atau riwayat revisi secara eksplisit saat migrasi; tidak membuat tautan JPEG yang sudah tidak ada. Untuk detail yang tidak terwakili panel, pertahankan pointer waktu/frame video; jangan mengklaim detail terlihat pada panel yang tidak menampilkannya.

Paket baru memuat audit.json, analysis.md, manifest.json dan media; source.mp4 hanya bila sumber kanonis belum tersedia. Batas ukuran/dimensi, daftar file yang diizinkan, hash isi, registry dan fingerprint disesuaikan untuk audit.json serta format kolase/storyboard. Validator V2 memeriksa jumlah berkas satu per shot ditambah satu storyboard, urutan/rujukan panel, timestamp dalam shot, batas foto dalam gambar, rasio dan ketentuan tiga panel normal; multi area tidak ditolak hanya karena jumlah panel bukan lima. Tidak ada analysis.json lain yang ditulis sebagai sumber kedua.

**Registry dan cache:** entri V2 mencatat versi sumber dan hash audit.json, selain hash laporan/manifest/paket/sumber. Entri legacy tetap dapat dibaca tanpa diberi fakta V2 rekaan. Model bersama mempertahankan seluruh isi/status/provenance legacy; field baru yang tidak tersedia tidak otomatis dilengkapi oleh build. Fingerprint memasukkan schema, template/versi renderer dan aset font/pengaturan yang memengaruhi keluaran.

MD dan kartu dibuat dari JSON yang sama di workspace chat sebelum pengguna meninjau. Persetujuan mengunci snapshot JSON dan MD beserta media/metadata relevan; pemeriksaan hash MD saja tidak cukup karena MD tidak menampilkan seluruh data. Pengguna tetap meninjau laporan/kartu, tanpa diwajibkan memeriksa JSON teknis.

Koreksi memperbarui audit.json, kemudian helper merender ulang kandidat lengkap. Setelah pengguna meninjau dan menyatakan sesuai, **export membungkus kandidat yang sama**, bukan menyusun ulang JPEG, mengubah created_at atau mengganti metadata. Digest snapshot mengikat JSON, MD, manifest dan seluruh media; sumber video terikat melalui hash manifest. Setiap perubahan isi kandidat membatalkan digest dan memerlukan tampilan terbaru sebelum persetujuan akhir. Receipt/digest tinjauan dikelola di workspace proses, di luar payload yang dihash, agar tidak membuat hash merujuk dirinya sendiri; tidak menambah file kerja ke ZIP referensi.

Ekspor memvalidasi kandidat dan ZIP yang dibuka ulang, lalu membandingkan snapshot lengkap. Ingest memeriksa kesetaraan MD dengan renderer JSON yang sesuai versi; ketidakcocokan menjadi kegagalan teknis, bukan alasan menulis ulang isi audit atau meminta review baru setelah ingest.

**Versi tampilan:** catat versi renderer/template serta profil media/font pada metadata teknis. Pertahankan pembaca/renderer untuk versi yang sudah diterima; perubahan template berikutnya tidak mengubah laporan lama atau membuatnya gagal hanya karena renderer terbaru berbeda. Pembaruan gaya laporan aktif masuk melalui revisi ZIP. Gunakan font berlisensi yang dibundel beserta lisensinya, pengaturan gambar eksplisit dan pemisahan foto/caption; tidak bergantung pada font sistem yang kebetulan tersedia. Validasi ingest tidak wajib meng-encode ulang JPEG yang sudah disetujui.

Status draf/final dan riwayat persetujuan dikelola sebagai provenance proses, agar narasi laporan tidak membawa kalimat status draf yang sudah kedaluwarsa.

## 6. Penguatan kualitas AI dan pembacaan ringan

### A. Pembacaan bertahap

Alur pembaca: **indeks ringkas → identitas referensi terpilih → detail shot yang diperlukan → bukti/media bila dibutuhkan**. JSON lengkap tetap tersedia; AI tidak diwajibkan memuat semua isinya untuk setiap tahap.

- Indeks memuat ID/revisi, label pencarian, ciri pembeda singkat dan pointer. Hindari seluruh narasi, daftar fakta lengkap, log frame atau metadata media berulang dalam indeks.
- Sediakan pembacaan bagian referensi/shot melalui tooling yang sama, dengan pembatasan hasil dan penambahan kandidat bertahap. Ringkasan tampilan ini dihasilkan dari sumber, bukan file fakta yang ditulis terpisah.
- Simpan metadata media dan panel sekali dalam inventaris; fakta/fase merujuk ID panel/path stabil. Reader tetap dapat menelusuri timestamp, hash dan asal bukti tanpa menyalin objek metadata penuh pada setiap klaim.
- Cakupan frame/hash teknis tersedia untuk validasi dan penelusuran; tidak wajib dikirim pada permintaan konsep/desain biasa. AI dapat meminta panel/area yang relevan, tanpa harus membaca seluruh kolase atau storyboard lebar dalam satu tampilan.
- Pertahankan cache proyeksi dan penerbitan keluaran yang berubah. Gunakan file JSON dan helper repo yang ada; tidak menambah database, embedding wajib atau layanan AI saat ingest.

### B. Pemilihan referensi yang bervariasi

Bedakan syarat wajib brief dari preferensi. Mulai dari beberapa referensi yang sesuai gaya, bentuk dan ukuran, kemudian perluas bila bukti atau variasinya belum cukup. Satu acuan utama dapat menjaga identitas arsitektur, dengan referensi pelengkap untuk konfigurasi area atau kamera yang kompatibel.

Ciri pembeda shot harus tersedia sebagai label/nilai eksplisit yang dapat dicari dan ditautkan ke fakta: geometri ruang, susunan fungsi, orientasi furnitur, penyimpanan dan bukaan. Pemilihan variasi mempertimbangkan konfigurasi tersebut, bukan hanya warna atau kemiripan nama gaya. Pertahankan nilai asli/status dan jangan mengisi fakta dari label saja.

Indeks membedakan video yang mempunyai beberapa shot area terpisah dari **satu shot berkelanjutan multi area**. Simpan label area, kontinuitas, urutan/rute eksplisit dan pointer perjalanan yang ringkas agar permintaan “satu shot living → kitchen” dapat menemukan bukti yang tepat; jangan menggabungkan shot terpisah menjadi perjalanan yang diklaim kontinu. Detail interval/narasi tetap dibaca setelah kandidat dipilih.

Jika kecocokan hanya sebagian atau sumber kurang, nyatakan bagian yang digunakan serta adaptasinya. Jangan mengarang referensi atau menafsirkan unknown/not-visible sebagai kecocokan positif. Perkiraan luas wajib tetap tersedia; kesesuaian ukuran dinilai bersama bentuk/proporsi dan kebutuhan brief.

### C. Profil tempo yang dapat dicari

Catat perkembangan tempo secara eksplisit saat audit: awal, akhir dan perubahan penting di antaranya bila ada. Indeks mengumpulkan label tempo yang benar-benar tercatat. Contoh sedang → cepat tetap ditemukan melalui moderate maupun fast, bukan hanya variable.

Variable menandai adanya perubahan, bukan menggantikan informasi kecepatannya. Ringkasan notasi, rasio skala, profil tempo dan percepatan tetap berbeda. Generator tidak menebak fast dari narasi atau kata Accelerating. Perubahan tempo tidak mewajibkan pemecahan fase komponen kamera yang sebenarnya berlangsung kontinu; MD cukup menampilkan ritme singkat dari data yang sama.

### D. Hubungan nama gaya

Alias hanya menyamakan ejaan/terjemahan yang bermakna setara. Keluarga gaya, gabungan gaya dan pengaruh dicatat sebagai hubungan eksplisit yang berbeda. Organic Modern Cottage dapat mempunyai hubungan keluarga Organic Modern dan Cottage bila dicatat oleh auditor; hubungan itu tidak menjadikan semua Organic Modern sebagai cottage.

Penetapan hubungan dilakukan saat audit, bukan disimpulkan generator dari judul/narasi. Bedakan gaya arsitektur utama, pengaruh dan gaya interior; judul kreatif rumah tidak otomatis menjadi label gaya. Pencarian mempertahankan status/tafsir dan istilah asli.

### E. Ringkasan DNA untuk penggunaan proyek

Setelah pengguna memilih konsep, alur AI membawa ringkasan keputusan proyek: bentuk/ukuran rencana, bukaan, material/palet, lingkungan/cahaya, keputusan area dan rujukan kamera. Setiap shot berikutnya memakai ringkasan tersebut dan membaca ulang referensi hanya sesuai kebutuhan, bukan memuat seluruh pustaka berulang.

Untuk konsep satu shot multi area, konteks proyek juga membawa susunan area, penghubung/jalur yang dapat dilalui, awal lintasan, perkembangan fokus dan ritme. AI membaca satu perjalanan sumber secara utuh ketika mengadopsi kontinuitasnya, sambil membedakan fakta sumber dari adaptasi konsep baru.

Ringkasan ini adalah konteks proyek produksi, bukan fakta audit atau referensi aktif baru. Plan V2 menyediakan kontrak/panduan penggunaan datanya; implementasi plugin atau pengelola proyek produksi tetap terpisah. Keenam penguatan ini tidak menambah bidang atau uraian teknis pada tampilan MD Bagian 3.

## 7. Peta perubahan file

Peta berikut mencakup fondasi Tahap 1 yang sudah tersedia dan file workflow/pilot Tahap 2 yang masih direncanakan. Status aktual dicatat pada verifikasi Tahap 1; keberadaan tooling tidak berarti audit/pilot selesai. Nama/versi legacy dipertahankan untuk kompatibilitas dan riwayat.

### A. Tooling yang diubah

| File | Perubahan yang harus dikerjakan |
| --- | --- |
| `tools/homeku/validation.py` | Dispatch versi/schema, izin file ZIP V2, validasi audit.json/MD hasil render, interval dan relasi area/fase, panel/media serta frame_reviews; pertahankan validasi legacy |
| `tools/homeku/exporter.py` | Susun kandidat V2 dari JSON, koordinasikan media/manifest/render; export hanya mengemas kandidat yang dikunci dan memeriksa roundtrip snapshot lengkap |
| `tools/homeku/markdown.py` | Pertahankan parser MD 1.0/1.1 sebagai jalur legacy; alihkan kartu V2 ke reporting, tanpa parsing fakta V2 dari MD manusia |
| `tools/homeku/generation.py` | Pakai model bersama, proyeksi/indeks 2.0, bukti panel dan pointer sumber JSON, hitungan area/shot yang tepat, alias/keluarga gaya serta fingerprint/cache baru |
| `tools/homeku/engine.py` | Registry dengan versi sumber/hash audit.json, ingest campuran legacy/V2, revisi/supersedes dan check/build tanpa konversi diam-diam |
| `tools/homeku/common.py` | Utilitas snapshot/digest dan pemeriksaan bersama; payload yang dihash tidak menyimpan digest dirinya sendiri |
| `tools/homeku/__init__.py` | Deklarasi kontrak/renderer/generator dan daftar versi yang didukung |
| `tools/audit.py` | Draft/render/review berbasis audit.json dan perintah export kandidat dengan digest snapshot; legacy tetap lewat jalur eksplisit |
| `tools/library.py` | Pertahankan ingest/build/check/recover; tambahkan pencarian serta pembacaan identitas/shot/area/panel dengan batas hasil |
| `tools/build_audit_kit.py` | Inventaris runtime/schema/template/font yang benar, bundel deterministik, panduan perintah baru dan pemeriksaan kit mandiri |
| `data/taxonomy.json` | Alias setara, hubungan keluarga/gabungan/pengaruh yang dibedakan dan label baru; perbarui pembaca agar hubungan tidak diperlakukan sebagai daftar alias |
| `.github/workflows/library-ci.yml`, `.github/workflows/library-ingest.yml` | Perbarui pemicu untuk template/aset terkait, uji legacy/V2 dan pemeriksaan kit; alur publikasi tetap diserialkan |

`tools/homeku/storage.py`, `tools/homeku/actions.py` dan `tools/publish_actions.py` dipertahankan bila antarmukanya tidak berubah. Verifikasi transaksi, recovery dan publikasi Git lewat regresi; tidak merombaknya hanya karena format audit berganti. Dependensi awal tetap FFmpeg, Pillow dan jsonschema; ubah requirements.txt hanya jika implementasi memang membutuhkan tambahan.

### B. Modul dan aset baru

| Target file | Tanggung jawab |
| --- | --- |
| `tools/homeku/models.py` | Membaca sumber berdasarkan versi, membentuk model bersama dan mempertahankan isi/status/bukti asli; tidak memperkaya legacy lewat tebakan |
| `tools/homeku/reporting.py` | Merender MD/kartu sesuai template, heading/anchor stabil serta aturan opsional; tidak membuat narasi AI baru |
| `tools/homeku/media.py`, `media_v2_0.py` | Kolase tiga panel/dinamis, storyboard satu baris, label/tata letak, inventaris penempatan panel dan pengambilan bagian foto |
| `tools/homeku/reader.py` | Indeks/pencarian dan pembacaan bagian identitas/shot/area/panel beserta konteks kontinuitas, dengan hasil terbatas |
| `tools/homeku/video.py` | PTS, pemilihan indeks dan ekstraksi frame bersama; pindahkan helper yang diperlukan tanpa mengubah aturan audit 10 FPS/native |
| `tools/assets/fonts/<font>.ttf`, `tools/assets/fonts/LICENSE.txt` | Font distribusi yang dipilih saat implementasi dan lisensi sebenarnya; profil/hash font masuk inventaris renderer dan kit |

Model sumber JSON menyimpan fakta; reporting menata; media merakit gambar; reader memilih bagian data. Pemisahan tanggung jawab tidak menambah file fakta manual atau layanan wajib baru. Anchor shot/identitas yang digunakan katalog harus eksplisit dan stabil meskipun judul manusia berubah.

### C. Kontrak dan template baru

| Target file | Isi |
| --- | --- |
| `docs/contracts/audit-v2.schema.json` | Sumber audit: identitas/luas wajib, kategori narasi, fakta/status, area/fungsi/kemunculan/rute, kamera/tempo, pilihan panel dan rujukan bukti |
| `docs/contracts/manifest-v2.schema.json` | Metadata teknis/provenance, inventaris komposit, frame_reviews, versi tampilan dan rujukan pilihan panel |
| `docs/contracts/reference-reader-v2.schema.json` | Proyeksi lengkap 2.0 dengan sumber JSON, bukti bersama dan payload bagian yang dapat ditelusuri |
| `docs/contracts/search-index-v2.schema.json` | Indeks ringkas 2.0 untuk gaya/konfigurasi/ukuran, shot/area/perjalanan dan seluruh tempo eksplisit |
| `docs/contracts/package-v2.md`, `analysis-v2.md`, `ai-reader-v2.md` | Kontrak ZIP/snapshot/revisi, laporan manusia baku dan pembacaan AI bertahap, termasuk bentuk hasil CLI |
| `docs/v2-field-map.md` | Pemetaan lengkap bidang lama ke V2, transformasi mekanis, bidang yang memerlukan pemeriksaan video dan pemetaan bukti/anchor |
| `audit/template-audit.json` | Kerangka sumber audit untuk AI; penanda kerja dilengkapi sebelum validasi/ekspor, bukan referensi aktif |

Kontrak/schema V1 tetap melayani legacy. `docs/template-analysis-v2.md` menjadi satu acuan susunan MD V2; kedua contoh dipertahankan sebagai ilustrasi tingkat kelengkapan. `audit/template-analysis.md` dipertahankan sebagai template legacy dan diberi penunjuk versi, bukan dijadikan template V2 kedua yang dirawat terpisah. Kit membawa acuan V2 yang sama dengan renderer repo.

### D. Panduan dan workflow audit yang diubah

| File/kelompok | Penyesuaian |
| --- | --- |
| `AGENTS.md`, `README.md` | Sumber JSON V2, fungsi MD, versi legacy, media panel dan cara memakai pustaka |
| `references/README.md`, `incoming/README.md`, `video/README.md` | Cara membaca panel/overview, satu ZIP, ingest lokal eksplisit, revisi dan video kanonis |
| `docs/operations.md`, `docs/capability-map.md`, kedua plan lama, `docs/alur-konsep-desain-v2.md` | Operasi/cache/versi/retensi dan jalur AI sesuai V2; riwayat implementasi lama dibedakan |
| `docs/template-analysis-v2.md`, kedua contoh MD | Acuan format; perubahan berikutnya harus tercatat versi tampilan dan tidak mengubah paket aktif |
| `audit/README.md`, `protocol.md`, `rubric.md`, `vocabulary.md` | Pengisian JSON/desain lengkap, shot vs area/fungsi, kamera sederhana/teknis, pemilihan panel dan audit adaptif |
| `audit/providers.md`, `audit/calibration.md` | Cara memakai kit baru dan batas pembuktian nyata; hapus ketergantungan instruksi pada jumlah file kit lama |
| `audit/prompts/01-audit.md`, `02-correct.md`, `03-export.md` | Audit/koreksi satu sumber JSON, render kandidat lengkap, persetujuan digest kandidat dan ekspor tanpa membuat ulang snapshot |
| `audit/pilots/README.md`, `docs/edh001-re-audit.md` | Catat audit ulang V2 dan status pilot hanya sesudah dijalankan; riwayat 1.1 tetap tersedia |

### E. Pengujian dan keluaran generator

| File/kelompok | Pekerjaan |
| --- | --- |
| `tests/fixtures/factory.py`, `tests/fixtures/README.md` | Fixture V2 terisolasi untuk normal/multi area; fixture legacy tetap dapat dipakai |
| `tests/test_library.py`, `test_audit.py`, `test_improvement.py`, `test_actions.py` | Regresi ingest/revisi/cache, audit native, pelestarian fakta dan publikasi; perbarui asumsi hash MD/jumlah file/media yang khusus legacy |
| Baru: `tests/test_v2_models.py`, `test_v2_reporting.py`, `test_v2_media.py`, `test_v2_reader.py` | Kontrak/model, render/snapshot, komposit/panel dan pencarian/pembacaan sebagian |
| Baru: `docs/v2-stage-1-verification.md` | Catatan hasil pemeriksaan aktual dan batas penyerahan Tahap 1; dibuat saat verifikasi dijalankan, tidak diisi dengan hasil perkiraan |
| Baru: `docs/v2-stage-2-verification.md` | Catatan kesiapan workflow/kit, audit ulang edh001, pelaksanaan enam pilot dan cakupan kalibrasi nyata; dibuat sesuai pelaksanaan, tanpa klaim run yang belum terjadi |
| `tools/make_test_packages.py`, `tests/fixtures/*.zip` | Bila fixture tersimpan ditambah, buat melalui factory; tidak mengimpor ke pustaka aktif atau mengganti legacy tanpa alasan |
| `audit/homeku-audit-kit.zip` | Bangun ulang dari builder setelah runtime/panduan siap; bukan diedit langsung |
| `catalogs/`, `knowledge/`, `data/projections/`, indeks/dependencies/build/registry/ingest | Keluaran tooling sesuai sumber/ingest yang sah; tidak dirawat sebagai salinan fakta manual |

Pada saat rencana awal dibuat, builder dan tes mengunci sembilan file kit. V2 harus menetapkan inventaris bundel portabel yang lengkap; runtime/schema/font tidak boleh dihilangkan demi mempertahankan angka sembilan. Tetap satu ZIP input tanpa video/audio dan satu ZIP hasil per referensi. Susunan bundel diuji dari workspace kosong; penerapan pada chat nyata dicatat pada tahap workflow/pilot.

Cache dan CI harus mengenali perubahan template, schema, profil renderer dan aset. Katalog/knowledge mempertahankan lingkup area dan pointer tanpa menggandakan hitungan shot karena fase/kemunculan. Prinsip terkurasi tetap bersumber dari `sources/design-principles.json`; perubahan isinya hanya bila diperlukan dan tidak diisi lewat sintesis saat ingest. Arsip tidak menjadi input generator atau kumpulan contoh aktif.

## 8. Audit ulang dan migrasi edh001, lalu enam pilot

Pertahankan pembacaan legacy 1.0/1.1 lewat jalur eksplisit selama transisi. Parser MD lama hanya melayani paket legacy; paket V2 membaca audit.json. Build tidak diam-diam mengonversi atau mengganti sumber referensi aktif.

edh001 menjadi uji audit nyata pertama untuk format baru: **periksa ulang seluruh lima shot sesuai standar V2**, bukan hanya mengubah format file. Gunakan baseline 10 FPS dan pendalaman native pada arah/fase/tempo, oklusi atau detail yang meragukan. Catat pemeriksaan baru yang benar-benar dijalankan; log audit 1.1 tidak otomatis dianggap log pemeriksaan ulang V2.

Audit ulang melengkapi identitas/gaya, proporsi dan luas wajib, tiga kategori detail desain, posisi/framing/cahaya, kamera sederhana yang sejalan dengan notasi/ritme serta pilihan panel/overview. Gerakan yang sudah disetujui menjadi acuan pemeriksaan, dengan alasan berbukti bila hasilnya perlu diperbaiki. Pindahkan fakta/status lama tanpa kehilangan bukti; perubahan atau koreksi ditelusuri melalui pemetaan bidang dan riwayat, bukan dihapus diam-diam.

Siapkan **ZIP revisi 2**, menyebut supersedes revisi 1 dan hash aktif yang benar. Konversi mekanis membantu memindahkan data, tetapi tidak mengarang gaya interior, luas, detail shot atau klaim pemeriksaan. Pelaksanaan audit V2 dibuktikan melalui log pemeriksaan aktual, bukan penyusunan rencana.

edh001 tetap lima shot sesuai cut sumber; migrasi tidak mengubahnya menjadi satu shot multi area. Paket V2 menargetkan lima kolase tiga panel dan satu storyboard horizontal, dengan label informatif. Bandingkan ukuran file aktual dan petakan bukti/overview ke panel atau timestamp sumber; paket r0001 tetap menyimpan bukti lama. Kedua contoh Willow Cottage adalah simulasi penyajian dan tidak dimasukkan ke registry atau dipakai untuk mengklaim audit multi area sudah dijalankan.

Tampilkan MD, kolase dan storyboard V2 untuk edh001 di chat, terapkan koreksi, kunci kandidat lengkap lalu ekspor kandidat tersebut setelah pengguna menyatakan sesuai. Ingest memperbarui referensi dan semua turunan tanpa review isi kedua. ZIP revisi 1 tetap sebagai bukti penyerahan.

Gunakan kit V2 untuk enam pilot berikutnya: edh058, edh013, edh033, edh049, edh056 dan dreamshome01. Audit dijalankan pengguna di ChatGPT/Gemini. Penyiapan kit tidak dihitung sebagai audit pilot selesai.

## 9. Urutan pekerjaan dan kriteria selesai

Pelaksanaan V2 dibagi dua tahap agar fondasi selesai sebelum workflow audit final diperbarui:

| Tahap | Urutan | Hasil yang harus tersedia |
| --- | --- | --- |
| **1. Struktur data, laporan dan pustaka** | Kontrak/pemetaan → model → renderer/media → validator/ingest → reader/turunan | JSON/MD/media V2 konsisten, snapshot utuh, legacy/revisi dan akses AI bertahap lolos pemeriksaan teknis |
| **2. Workflow analisis ChatGPT/Gemini dan pilot** | Prompt/panduan/helper/kit → audit ulang edh001 r0002 → enam pilot | Kit mandiri, audit nyata seluruh shot edh001, persetujuan/ekspor kandidat utuh dan kalibrasi pilot |

### A. Urutan lengkap Tahap 1

**Tujuan:** fondasi repo dapat menerima paket V2, membuat laporan/media baku, mempertahankan legacy serta menyediakan pengetahuan AI yang ringan. Tahap ini memakai fixture terisolasi dan referensi aktif yang sudah ada; audit ulang edh001, prompt audit final dan pelaksanaan pilot tetap Tahap 2.

Kerjakan menurut urutan 1.1–1.12. Hasil langkah sebelumnya menjadi input langkah berikutnya; tes tiap kemampuan ditambahkan bersama implementasinya, bukan ditunda seluruhnya sampai akhir. Schema dan CLI pada langkah awal ditetapkan sebagai antarmuka target; perilakunya baru dinyatakan tersedia setelah implementasi dan pemeriksaan terkait lulus.

| Langkah | Pekerjaan dan file utama | Hasil serta pemeriksaan sebelum lanjut |
| --- | --- | --- |
| **1.1 — Tetapkan kontrak dan pemetaan** | Buat `docs/contracts/audit-v2.schema.json`, `manifest-v2.schema.json`, `reference-reader-v2.schema.json`, `search-index-v2.schema.json`, `package-v2.md`, `analysis-v2.md`, `ai-reader-v2.md` dan `docs/v2-field-map.md`. Tetapkan versi sumber/reader, renderer, registry/taksonomi serta bentuk respons CLI. | Semua bidang lama terpetakan; identitas/luas, kategori narasi, fungsi/area/rute/fase, pilihan panel dan snapshot mempunyai sumber/tanggung jawab jelas. Kontrak legacy tetap tersedia; tidak ada schema yang hanya menerima dokumen contoh tetapi membuang bidang audit lain. |
| **1.2 — Siapkan baseline dan fixture V2** | Catat kondisi awal pustaka/kit/tes. Perluas `tests/fixtures/factory.py`, panduannya dan kerangka `tests/test_v2_*.py`. Buat sumber sintetis serta audit JSON/metadata yang sesuai untuk tes terisolasi. | Tersedia kasus normal, perjalanan multi area, area terlihat bersamaan, satu area banyak fungsi, kemunculan berulang serta input tidak valid. Semua berstatus fixture; tidak masuk registry produksi. Hash/revisi edh001 r0001 dicatat sebagai batas yang harus dipertahankan. |
| **1.3 — Bangun pembaca model dan helper video** | Tambahkan `tools/homeku/models.py`, `video.py`; sesuaikan utilitas/versi pada `common.py`, `__init__.py` serta pemanggil legacy. Pertahankan `markdown.py` untuk 1.0/1.1. | Dispatch versi eksplisit dan model bersama mempertahankan isi/status/negasi/bukti legacy. PTS, indeks dan ekstraksi sesuai sumber; baseline 10 FPS/native tidak berubah. Tidak ada pelengkapan gaya/luas legacy otomatis, parsing MD untuk sumber V2 atau ketergantungan impor melingkar baru. |
| **1.4 — Implementasikan media dan font** | Tambahkan `tools/homeku/media.py` dan font berlisensi dalam `tools/assets/fonts/`. Baca pilihan frame dari audit.json, ekstrak sementara, buat kolase serta inventaris teknis manifest. | Normal tiga panel/kolom; multi area dinamis dan kronologis dengan tata letak terbaca; storyboard seluruh area satu baris. Caption di luar foto, rasio/detail terjaga, koordinat panel dapat dipakai mengambil foto tanpa caption. Tidak ada JPEG frame tambahan dalam paket. Ukur dimensi/byte, tanpa menjanjikan penghematan tertentu. |
| **1.5 — Implementasikan laporan dan kartu** | Tambahkan `tools/homeku/reporting.py`, gunakan `docs/template-analysis-v2.md`, media/inventaris langkah 1.4 dan narasi sumber. Tetapkan anchor serta versi template/renderer. | MD mempunyai lima bagian dan kartu A/B/C; desain lengkap, tabel komposisi, kamera sederhana/ritme/teknis serta bagian opsional benar. Tidak ada placeholder/petunjuk template atau fakta baru dari renderer. Nilai waktu/notasi sama dengan sumber; luas tampil hanya angka m². |
| **1.6 — Implementasikan validasi paket V2** | Sesuaikan `tools/homeku/validation.py` dengan model, video dan reporting. Pilih schema sesuai versi setelah pemeriksaan ZIP aman; jangan menganggap audit.json atau pola nama file sebagai pengganti versi kontrak. | Paket valid diterima; identitas/file ekstra, hash, waktu, fase, area/fungsi, pilihan panel, batas foto/rasio, frame_reviews dan MD tidak cocok ditolak dengan alasan jelas. Legacy tetap valid menurut kontraknya sendiri. Pemeriksaan teknis tidak dianggap bukti kebenaran visual atau persetujuan manusia. |
| **1.7 — Implementasikan kandidat dan ekspor terkunci** | Sesuaikan inti `tools/homeku/exporter.py` dan utilitas digest; sediakan antarmuka kandidat/review/export di `tools/audit.py` sejauh diperlukan untuk menguji alur V2. | Draft membentuk kandidat lengkap. Review menghasilkan digest seluruh JSON/MD/manifest/media; export mengemas byte kandidat yang sama tanpa mengubah JPEG/created_at/metadata. Mengubah satu file membatalkan digest. ZIP yang dibuka ulang identik dalam isi, dan file receipt kerja tidak ikut paket. |
| **1.8 — Sesuaikan generator dan taksonomi** | Ubah `tools/homeku/generation.py`, `data/taxonomy.json` dan validasi proyeksi/indeks. Terapkan inventaris bukti bersama, hubungan gaya terpisah dari alias, scope area serta profil tempo eksplisit. | Fixture legacy/V2 menghasilkan proyeksi lengkap dan indeks 2.0 tanpa pengulangan metadata/narasi besar. Pointer sumber JSON/MD/panel valid; katalog dan knowledge menjaga status/negasi serta denominator. Satu shot tidak dihitung berkali-kali karena area, fungsi atau fase. |
| **1.9 — Implementasikan pembacaan AI bertahap** | Tambahkan `tools/homeku/reader.py`; perluas `tools/library.py` untuk pencarian serta pembacaan identitas, shot, area dan panel dengan batas hasil. | Gaya/ukuran/konfigurasi/tempo dapat ditemukan; satu perjalanan multi area dibedakan dari beberapa cut terpisah. Pembaca mengambil bagian yang diperlukan beserta pointer/konteks kontinuitas, tanpa semua log/hash/narasi pustaka. Foto panel dapat diambil sementara atau frame diekstrak dari sumber, tanpa salinan permanen. |
| **1.10 — Integrasikan ingest, registry dan cache** | Sesuaikan `tools/homeku/engine.py`, hubungan generator/model dan fingerprint. Catat versi/hash audit.json pada entri V2, tetap membaca entri legacy; pertahankan storage/actions bila antarmukanya tetap. | Ingest ZIP V2 terisolasi memperbarui referensi dan seluruh turunan; replay, konflik revisi, supersedes, koleksi campuran dan penghapusan turunan usang benar. Build penuh/setara inkremental, cache rusak pulih melalui rebuild, transaksi/recovery aman dan perubahan template/font menginvalidasi cache yang terkait. |
| **1.11 — Selaraskan operasi, CI dan kompatibilitas kit** | Perbarui `AGENTS.md`, README/panduan operasi/pembaca dan workflow CI/ingest sesuai kemampuan yang benar-benar tersedia. Perbarui builder/inventaris teknis kit bila modul/schema/aset bersama berubah. | Aturan aktif membedakan sumber V2 dari legacy; petunjuk lokal menyebut perintah ingest. CI memantau template/aset. Kit legacy masih dapat dijalankan dan --check tidak rusak karena dependensi baru tidak terbawa. Jangan menyebut workflow audit V2/pilot siap hanya karena bundel teknis sudah diperbarui. |
| **1.12 — Verifikasi integrasi dan serahkan fondasi** | Jalankan pemeriksaan wajib, tes kontrak/render/media/reader, alur ZIP dan transaksi, serta fixture ratusan referensi. Bangun turunan melalui generator jika implementasi mengubah format keluarannya. Catat hasil pada `docs/v2-stage-1-verification.md` saat pekerjaan benar-benar dijalankan. | Semua pemeriksaan lulus atau kegagalannya diselesaikan; sumber/hash/revisi/media aktif edh001 r0001 tetap utuh. Laporan verifikasi mencantumkan hasil aktual, batas pembuktian dan pekerjaan Tahap 2. Tidak ada fixture aktif, klaim audit baru atau ekspor edh001 r0002 pada Tahap 1. |

**Batas antarmuka dan transisi**

- Langkah 1.7 menyediakan API/CLI teknis untuk menguji kandidat dan ekspor; penyusunan prompt, panduan analisis serta pengalaman review ChatGPT/Gemini V2 dilakukan pada Tahap 2.
- Kit saat ini bergantung pada runtime bersama dan CI memeriksa kesegarannya. Karena itu, penyesuaian dependensi/inventaris serta regenerasi bundel yang diperlukan agar jalur lama tetap berjalan masuk langkah 1.11. Mengganti seluruh panduan/prompt kit menjadi workflow V2 tetap Tahap 2. Jumlah sembilan file tidak boleh menyebabkan modul/schema/font hilang.
- Uji end-to-end V2 pada tahap ini berarti **sumber sintetis → audit JSON fixture → media/MD → kandidat terkunci → ZIP → ingest terisolasi → reader/knowledge**. Ini bukan audit video nyata atau pengujian manfaat kreatif.
- Pustaka produksi hanya dibangun ulang bila format keluaran generator berubah; seluruh fakta tetap berasal dari sumber aktif yang sama. `references/edh001/`, media/hash/revisi sumber serta ZIP r0001 tidak dikonversi atau ditimpa. Perubahan keluaran generator tidak dihitung sebagai audit/revisi isi baru.
- Jangan menjalankan ingest fixture pada root produksi. Jangan menggunakan arsip sebagai sumber build. Jangan menambah database, embedding wajib, watcher atau layanan AI untuk menyelesaikan Tahap 1.

**Tahap 1 selesai bila:** kontrak dan pemetaan data tersedia; normal/multi area dapat diproses sesuai template; kandidat/ekspor tidak berubah setelah dikunci; reader dan turunan mempertahankan isi/status/bukti; jalur legacy, kit yang sedang berlaku serta transaksi tetap berjalan; seluruh pemeriksaan wajib dan regresi V2 lulus. Kemampuan ini dibuktikan melalui tes terisolasi dan check pustaka aktif, bukan jumlah file yang telah dibuat.

### B. Urutan lengkap Tahap 2

**Status pelaksanaan 22 November 2026:** 2.1–2.10 selesai: workflow/kit diuji, kelima shot edh001 diaudit ulang, seluruh kandidat disetujui pengguna, lalu r0002 diekspor tanpa perubahan dan di-ingest. Enam run pengguna pada 2.11 belum dijalankan dan kalibrasi 2.12 masih terbuka. Rincian/bukti aktual: [verifikasi Tahap 2](v2-stage-2-verification.md).

**Tujuan:** workflow ChatGPT/Gemini memakai fondasi V2 untuk mengaudit sumber, menampilkan laporan/kolase yang mudah dikoreksi dan menyerahkan satu ZIP final. edh001 diaudit ulang di chat ini; enam pilot berikutnya dijalankan pengguna di ChatGPT/Gemini. Tahap 2 baru dimulai setelah kriteria penyerahan Tahap 1 terpenuhi.

Kerjakan menurut urutan 2.1–2.12. Bedakan **workflow/kit siap dipakai** dari **audit pilot selesai**. Runtime yang sudah tersedia dan tes sintetis tidak menggantikan pemeriksaan video, koreksi serta persetujuan isi di chat.

| Langkah | Pekerjaan dan file utama | Hasil serta pemeriksaan sebelum lanjut |
| --- | --- | --- |
| **2.1 — Terima fondasi Tahap 1** | Baca `docs/v2-stage-1-verification.md`; cocokkan kontrak/schema, renderer/template/font, CLI, reader dan versi kit yang akan dipakai. Periksa status aktif edh001 dan supersedes r0001. | Hasil Tahap 1 benar-benar lulus, ketergantungan kit tersedia dan batas yang masih terbuka tercatat. Jangan memulai audit V2 dengan perangkat setengah terintegrasi atau menganggap data r0001 telah menjadi V2. |
| **2.2 — Siapkan template JSON dan panduan pengisian** | Buat `audit/template-audit.json`; sesuaikan `audit/README.md` dan panduan penggunaan template dengan schema sumber, `docs/template-analysis-v2.md` serta dua contoh yang disetujui. | AI mempunyai satu sumber pengisian untuk identitas/luas, desain per kategori/area, fakta/status/bukti, komposisi, kamera sederhana/teknis/tempo, perjalanan dan pilihan panel. Jelaskan data yang ditulis AI versus metadata yang dihitung helper; template kerja tidak boleh lolos sebagai audit final yang masih berisi penanda. |
| **2.3 — Selaraskan protokol, rubrik dan kosakata** | Perbarui `audit/protocol.md`, `rubric.md`, `vocabulary.md` dan bagian metodologi `calibration.md`. | Urutan audit mencakup metadata/cut → baseline 10 FPS seluruh shot → pendalaman native → desain/komposisi/kamera → pemilihan panel → pemeriksaan silang. Pan/orbit/truck/zoom, arah, tempo dan jitter/tilt mengikuti bukti; gaya/luas/detail diisi sesuai ketentuan. Fungsi, area terlihat, rute dan fase tidak disamakan. |
| **2.4 — Tulis ulang tiga prompt workflow** | Perbarui `audit/prompts/01-audit.md`, `02-correct.md`, `03-export.md`. | Prompt audit mengisi JSON dan meminta helper membuat kandidat. Koreksi memperbarui sumber/log pemeriksaan yang benar-benar dilakukan, lalu merender ulang seluruh bagian terdampak. Ekspor hanya setelah persetujuan keseluruhan snapshot; persetujuan satu gerak bukan persetujuan seluruh audit. Tidak ada fakta manual yang disalin terpisah ke MD. |
| **2.5 — Selesaikan pengalaman review dan helper chat** | Selesaikan antarmuka pada `tools/audit.py`, `reporting.py`, `exporter.py` dan panduan perintah sesuai kontrak yang sudah tersedia. Gunakan versi tampilan yang sama dengan repo. | AI dapat menjalankan inspect/sample/draft/review/export dari workspace chat. Tampilkan storyboard, kolase dan laporan yang nyaman dibaca, dengan kamera sederhana serta teknis yang sejalan. Digest/receipt dihitung helper di luar isi laporan manusia; pengguna tidak diminta membaca JSON atau memeriksa hash secara manual. |
| **2.6 — Bangun kit audit V2 lengkap** | Sesuaikan `tools/build_audit_kit.py`, `audit/providers.md` dan README/inventaris kit; regenerasi `audit/homeku-audit-kit.zip` dari sumber. | Satu ZIP input membawa runtime, schema, template/font/lisensi dan panduan yang cocok; MP4 tetap dilampirkan terpisah. Jumlah file mengikuti inventaris yang diperlukan, bukan angka sembilan lama. Tidak memerlukan repo penuh, akses arsip, API AI atau layanan baru untuk menyusun paket. |
| **2.7 — Uji kit dari workspace kosong** | Jalankan tes portabel pada fixture terisolasi, termasuk alur koreksi, render, snapshot, ekspor dan validasi ZIP yang dibuka ulang. Perbarui `tests/test_audit.py`/tes V2 bila perilaku berubah. | Modul/schema/font lengkap; paket final hanya berisi isi kontrak; export tidak mengubah kandidat yang ditinjau. Frame log benar menurut fixture, bagian opsional/label terbaca dan rujukan panel valid. Petunjuk input/lingkungan chat diverifikasi saat implementasi, bukan diasumsikan dari nama model. Ini bukti portabilitas teknis, belum bukti pilot ChatGPT/Gemini selesai. |
| **2.8 — Audit ulang seluruh edh001** | Periksa `video/edh001.mp4` sesuai Bagian 8; gunakan data r0001 dan pemetaan lama sebagai bahan penelusuran, bukan pengganti melihat sumber. Susun audit.json V2, metadata pemeriksaan aktual dan kandidat di workspace kerja. | Kelima shot benar-benar diperiksa pada baseline/pendalaman yang diperlukan; gaya/luas/desain/komposisi/kamera lengkap. Pertahankan lima shot dan batas cut sumber; telusuri alasan perubahan hasil yang sudah disetujui. Buat lima kolase tiga panel serta storyboard satu baris; catat jumlah byte aktual. Tidak menimpa referensi aktif atau menganggap log lama sebagai pemeriksaan baru. |
| **2.9 — Tinjau dan koreksi edh001 di chat** | Tampilkan MD, storyboard dan seluruh kolase kandidat kepada pengguna. Terapkan koreksi pada audit.json/bukti/pilihan panel serta log bila ada pemeriksaan baru; bangun ulang kandidat dan tampilkan bagian terdampak beserta konteks. | Pengguna dapat memeriksa desain, gambar, awal lintasan, gerak dan ritme tanpa membaca rincian teknis JSON. Narasi dan data diperiksa silang AI sebelum ditampilkan. Kunci digest kandidat lengkap hanya setelah versi terbaru dinyatakan sesuai; koreksi setelahnya membatalkan digest lama. |
| **2.10 — Ekspor dan ingest edh001 revisi 2** | Bungkus kandidat yang disetujui menjadi `edh001-r0002.zip` dengan supersedes r0001 yang benar. Validasi roundtrip; setelah penyerahan final, masukkan ke incoming/ dan jalankan ingest/check. Perbarui catatan edh001 sesuai kejadian nyata. | JSON/MD/manifest/media dalam ZIP cocok dengan kandidat; video hanya disertakan jika sumber kanonis belum tersedia dengan hash sama. Registry menjadi revisi 2 dan turunan terbarui tanpa review isi kedua; r0001 tetap tersimpan. Periksa pointer/reader, replay dan tidak adanya fakta turunan usang secara teknis, bukan mengaudit ulang isi setelah ingest. |
| **2.11 — Jalankan enam pilot di ChatGPT/Gemini** | Pengguna menjalankan edh058, edh013, edh033, edh049, edh056 dan dreamshome01, satu chat per sumber, memakai kit V2 terbaru. Catat pelaksanaan pada `audit/pilots/README.md` dan kalibrasi. | Setiap pilot mengikuti audit → review/koreksi di chat → persetujuan → satu ZIP → ingest lokal. Kedua lingkungan terwakili; tidak wajib menjalankan setiap video dua kali. Nama provider/model yang dicatat adalah yang benar-benar digunakan, build yang tidak diketahui tidak dikarang. ZIP valid diperiksa teknis, tanpa mengulang review isi pengguna di repo. |
| **2.12 — Selesaikan kalibrasi dan dokumentasi hasil** | Rangkum temuan nyata pada `audit/calibration.md`, panduan terkait dan `docs/v2-stage-2-verification.md`; perbaiki akar masalah pada sumber/tooling lalu jalankan pemeriksaan yang relevan dan bangun ulang kit jika berubah. | Bedakan kesalahan interpretasi, instruksi, render/media dan ingest. Paket yang sudah diterima tidak diedit diam-diam; koreksi isi memakai revisi eksplisit. Catat status setiap pilot, versi kit/snapshot dan cakupan yang telah/belum terbukti. Bekukan kontrak sesuai cakupan kalibrasi yang selesai, tanpa menjadikan fixture sebagai bukti visual. |

**Pembagian pelaksanaan**

- Langkah 2.1–2.7: asisten menyiapkan workflow dan menguji perangkat; pengguna belum perlu menjalankan enam pilot dengan kit yang belum siap.
- Langkah 2.8–2.10: asisten mengaudit edh001 di chat ini, pengguna meninjau/koreksi dan menyetujui sebelum ZIP final. Perintah ekspor/ingest mengikuti penyerahan yang sudah diotorisasi; penulisan plan ini tidak dihitung sebagai persetujuan isi audit V2 yang belum dibuat.
- Langkah 2.11: pengguna menjalankan enam audit pada chat pilihannya. Mulai dari edh058 untuk alur standar, lalu lanjutkan daftar pilot; pembagian provider pada daftar pilot adalah usulan sampai run nyata dicatat. Asisten dapat menyiapkan perangkat dan menangani masalah repo tanpa mengaku menjalankan chat pengguna.
- Langkah 2.12: selesaikan berdasarkan hasil yang benar-benar tersedia. Selama paket/run pengguna belum tersedia, status pilot tetap belum selesai; jangan menutup keseluruhan Tahap 2 hanya karena kit dan edh001 selesai.

**Batas kalibrasi dan perubahan**

- Pilihan panel dinamis dibuat saat audit, memakai jumlah paling sedikit yang tetap menjelaskan perjalanan. Tidak mengubah shot agar sesuai jumlah gambar; sumber tanpa cut tetap satu shot.
- Jika tujuh pilot belum menyediakan contoh perjalanan multi area yang nyata, catat batas kalibrasi visual tersebut. Tes fixture tetap membuktikan struktur/tooling saja; jangan mengarang kontinuitas atau mengklaim semua variasi kamera sudah terkalibrasi. Penambahan sumber di luar tujuh pilot tidak otomatis menjadi kewajiban baru pada plan ini.
- Temuan yang membutuhkan perubahan kontrak/renderer harus diberi versi dan diuji; regenerasi kit tidak mengubah JSON/MD/JPEG paket yang sudah disetujui. Perubahan isi referensi mengikuti revisi dan tinjauan sebelum ZIP seperti biasa.
- Pengecekan reader/knowledge setelah ingest hanya memeriksa hasil pemrosesan dan pointer; tidak menambah review isi kedua atau pengujian manfaat melalui konsep/gambar baru.

**Tahap 2 selesai bila:** workflow/kit V2 portabel sudah diuji; seluruh lima shot edh001 diaudit ulang, disetujui dan masuk sebagai r0002; enam pilot selesai sesuai pembagian pengguna dengan kedua lingkungan terwakili; hasil ZIP/ingest dan kalibrasi tercatat beserta batasnya. Semua koreksi masuk melalui sumber/tooling atau revisi yang sah, dan pemeriksaan relevan lulus. Status kesiapan kit, pelaksanaan audit, penerimaan isi dan ingest dibedakan secara jelas.

Tidak ada implementasi plugin produksi, percobaan konsep/gambar atau benchmark manfaat dalam kedua tahap. Pengguna tetap mengoreksi isi sebelum download ZIP, menjalankan ingest lokal setelah menaruh ZIP di incoming/, dan tidak diminta review isi kedua setelah ingest.

### C. Kriteria selesai keseluruhan V2

- **Laporan manusia:** lima bagian bernomor, kartu A/B/C konsisten, desain lengkap dalam tiga kategori, tabel komposisi, kamera sederhana/ritme/notasi teknis serta timeline gerakan sesuai aturan. Tidak ada petunjuk template atau placeholder pada hasil final.
- **Identitas dan ukuran:** nama gaya jelas; rentang luas lantai selalu terisi dan tampil hanya sebagai angka m², tanpa tambahan yang tidak diminta.
- **Normal dan multi area:** satu pengambilan tetap satu shot; detail/fakta terikat ke area yang tepat; kemunculan area, rute dan fase dibedakan; waktu/media valid. Simultanitas, urutan, tempo dan notasi tidak berubah antarhasil tampilan.
- **Media:** satu kolase per shot; normal tepat tiga panel; multi area dinamis sesuai perjalanan tanpa panel berulang yang tidak menambah informasi. Storyboard overview seluruh area satu baris; label informatif, rasio/detail dan asal panel terjaga. Tidak ada JPEG frame terpisah atau rangkaian frame penuh dalam paket V2.
- **Data dan operasi:** seluruh isi/status/bukti lama terpelihara dalam JSON; persetujuan mengikat kandidat lengkap dan export tidak membangun ulang media/metadata. Versi renderer, hash sumber JSON dan seluruh pointer tercatat; ZIP valid memperbarui turunan tanpa review isi kedua.
- **Akses AI:** bagian identitas/shot/area dapat dibaca tanpa semua data, dengan konteks kontinuitas saat dibutuhkan. Indeks membedakan perjalanan satu shot dari area pada shot terpisah, tidak menyalin narasi/log lengkap, serta mendukung pencarian konfigurasi, tempo dan hubungan gaya.
- **Skala dan migrasi:** ratusan referensi, cache, revisi, legacy dan pemisahan arsip tetap terjaga; paket lama tetap terbaca dan edh001 r0001 tidak diganti diam-diam. Audit ulang lima shot V2 dan enam pilot dicatat sesuai pelaksanaan nyata, terpisah dari pengujian teknis.
- **Portabilitas:** template/font/inventaris runtime tersedia di kit, perubahan aset memicu cache/CI yang relevan, dan renderer versi lama tetap dapat memeriksa paket yang sudah diterima.

### D. Pemeriksaan setelah implementasi tooling

Perintah berikut telah lulus pada akhir Tahap 1; hasil aktual dan batas pembuktian terdapat pada [verifikasi](v2-stage-1-verification.md). Jalankan kembali setelah perubahan tooling yang relevan.

```sh
python -m unittest discover -s tests -t . -v
python tools/library.py check
python tools/build_audit_kit.py --check
```

Regresi yang diperlukan:

- Render JSON → MD mengikuti template; bagian opsional normal/multi area, seluruh detail desain dan kamera sederhana terpelihara; nilai teknis/waktu konsisten, luas wajib tanpa catatan tambahan dan hasil final tanpa placeholder.
- Satu shot satu area, satu shot melewati beberapa area, beberapa area terlihat bersamaan tanpa dilewati semuanya, area muncul kembali, serta beberapa shot pada area sama. Uji satu fase melewati banyak area dan beberapa fase pada satu area; jangan memaksa batas area menjadi fase/cut.
- Interval kemunculan boleh bertumpang tindih, interval fase tidak; pointer area/fase/media tepat, penghubung dan kronologi terjaga. Pencarian perjalanan tidak salah menganggap cut terpisah sebagai kontinuitas; hitungan shot tidak bertambah karena fase/area.
- Pelestarian bidang lama/status/negasi, konfigurasi pembeda, gaya/interior dan alias/keluarga gaya, profil tempo termasuk perubahan di tengah, fokus/framing/cahaya, inventaris bukti bersama dan legacy/revisi tanpa turunan usang.
- Kolase normal tiga panel, multi area dengan berbagai jumlah panel, susunan beberapa baris yang tetap kronologis, storyboard satu baris dengan beberapa area bernomor shot sama, overview yang berbeda dari panel kolase, serta caption yang tidak menutupi foto.
- Bounds/rasio dan timestamp/frame panel, pointer bukti tanpa path sementara, ekstraksi panel tanpa caption, jumlah file media, batas piksel/ukuran serta ukuran byte aktual sebelum–sesudah; pengujian tidak menjanjikan penghematan tertentu.
- Snapshot JSON+MD/manifest/media; perubahan salah satu file membatalkan digest. Export tidak mengubah created_at, JPEG atau metadata; perubahan template baru tidak menggagalkan paket yang memakai versi renderer lama yang masih didukung.
- Bedakan satu area banyak fungsi, beberapa area terlihat tanpa dilalui dan perjalanan antararea; fakta serta pilihan panel tidak mempunyai dua sumber yang dikoreksi terpisah.
- Hash sumber audit.json, registry/cache campuran legacy/V2, anchor stabil, fingerprint template/font dan inventaris kit; pembacaan legacy tidak menambahkan nilai gaya/luas V2 rekaan.
- Roundtrip ZIP dan kit mandiri dari workspace kosong; penolakan MD tidak cocok, modul/schema/aset hilang dan ketergantungan font sistem yang tidak dinyatakan.
- Fixture ratusan referensi: hasil pencarian/pembacaan sebagian, batas hasil, ukuran payload dan tidak terikutnya narasi/log/metadata berulang di indeks.

Ini pengujian teknis struktur, akses dan pelestarian data, bukan benchmark konsep atau generate gambar. Validasi teknis bukan klaim kebenaran estimasi visual atau bukti audit video yang belum dijalankan.

Metode audit tetap 10 FPS dengan pendalaman native sesuai kebutuhan, tanpa seluruh frame/motion dalam paket. Tidak ditambahkan plugin produksi, watcher lokal, benchmark manfaat pustaka, percobaan konsep atau generate gambar. Pengguna tetap cukup mengunduh satu ZIP, menaruhnya di incoming/ dan menjalankan ingest lokal. Fondasi Tahap 1 tidak mengubah isi referensi aktif; keseluruhan V2 belum selesai sampai workflow dan pilot Tahap 2 benar-benar dijalankan.
