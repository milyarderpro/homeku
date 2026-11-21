# Rencana Implementasi Pustaka HOMEKU

Tanggal: 21 November 2026  
Status: rencana implementasi; belum mengaktifkan pipeline.
Pelaksanaan dibagi menjadi dua phase: fondasi dan otomasi, kemudian workflow audit dan pilot.

## 1. Tujuan dan batas pekerjaan

Bangun pustaka yang tumbuh dari 57 referensi awal menjadi ratusan video. AI kreatif dapat menemukan variasi desain, memahami komposisi dan mengadaptasi gerakan kamera berdasarkan bukti referensi. Laporan Markdown harus lengkap dan nyaman dibaca manusia maupun AI.

Audit dan koreksi isi dilakukan di chat Gemini/GPT. Pengguna meninjau analisis, terutama kamera, tempo dan detail yang kurang, lalu mengunduh ZIP final. Upload ZIP ke repo menjadi penyerahan versi final; pengguna tidak diminta review isi lagi setelah ingest.

Plugin produksi baru berada di luar lingkup. `archive/oldrepo/` menjadi arsip, dikecualikan dari discovery, pencarian, build dan hitungan aktif. Anotasi lama tidak otomatis menjadi pengetahuan baru. Video asli di `video/` tetap dapat digunakan; jumlah file video tidak sama dengan jumlah referensi aktif.

## 2. Keputusan arsitektur

| Keputusan | Ketentuan |
| --- | --- |
| Satuan penyerahan | Satu ZIP per video per revisi; pengguna tidak mengurus file turunan satu per satu |
| Sumber isi | `references/<id>/analysis.md`; metadata teknis dan daftar media berada dalam manifest |
| Data pencarian | Dihasilkan dari bagian terstruktur dalam MD; tidak ada `analysis.json` yang diedit terpisah |
| Status final | Upload merupakan penerimaan versi audit; keberhasilan validasi teknis bukan verifikasi kebenaran visual |
| Pembaruan otomatis | Referensi, indeks, katalog, perbandingan dan ringkasan knowledge berbasis sumber |
| Pemeriksaan isi | Selesai di chat sebelum ZIP; repo tidak menjalankan audit video ulang atau mengganti interpretasi |
| Model operasi | Generator deterministik; tanpa API AI berbayar, database atau layanan pencarian wajib |
| Kamera | Ringkasan Inggris dengan notasi urutan/simultan yang selaras dengan masterprompt; isi tetap mengikuti video sumber |
| Pembaca | Cukup mengakses Markdown dan media; tidak perlu menjalankan tooling repo |

## 3. Struktur target

```text
README.md
docs/                   # Rencana, kontrak dan panduan pemeliharaan
audit/                  # Prompt Gemini/GPT, template MD, rubrik, contoh ZIP
incoming/               # ZIP yang diunggah pengguna
video/                  # Video asli; satu salinan kanonis per sumber
references/<id>/         # analysis.md, manifest.json, media/
catalogs/                # Indeks, variasi ruang, arsitektur, komposisi, kamera
knowledge/               # Ringkasan dan perbandingan berbasis sumber
data/                   # Registry, proyeksi terstruktur dan rekam ingest
tools/                  # Importer, parser, validator dan generator
tests/                  # Fixture serta pengujian kontrak dan alur
.github/workflows/      # Ingest dan CI
archive/oldrepo/         # Arsip pustaka sebelumnya
```

README menyediakan tiga jalur: mengaudit/menambahkan video, mencari referensi, dan memahami knowledge. Dokumen produksi di `bekerja/` tetap terpisah dari jalur pustaka; masterprompt v2 hanya menjadi acuan format ringkasan kamera pada Bagian 6. Perbarui `video/README.md` yang masih menjelaskan workflow lama saat workflow baru tersedia.

## 4. Kontrak ZIP versi 1

Nama: `<id>-r0001.zip`. Isi satu folder `<id>/`:

```text
<id>/
  analysis.md
  manifest.json
  source.mp4             # Jika sumber belum tersedia di video/
  media/
    storyboard.jpg
    shot-01/
      area-overview.jpg
      start.jpg
      middle.jpg
      end.jpg
      reveal-01.jpg       # Jika ada bagian area yang belum terwakili
      detail-01.jpg       # Jika diperlukan
    shot-02/
      area-overview.jpg
      start.jpg
      middle.jpg
      end.jpg
    ...
```

- ID stabil mengikuti stem nama video, memakai karakter aman dan diperiksa terhadap tabrakan kapitalisasi. Tidak memakai counter global.
- Manifest mencatat versi kontrak, ID/revisi, identitas sumber, hash yang benar-benar dihitung, daftar media beserta shot/timestamp, metode audit, cakupan pemeriksaan, tanggal dan identitas AI yang diketahui. Frame/crop memiliki timestamp sumber; storyboard mencatat daftar gambar penyusunnya. Model build boleh `null`.
- Sumber harus tersedia sebagai MP4 dalam ZIP atau melalui path `video/` dengan hash yang cocok. Importer menempatkan sumber baru pada `video/`; tidak menyimpan salinan MP4 kedua dalam referensi.
- Isi audit hanya berada dalam MD. Manifest tidak menduplikasi fakta desain/kamera; field yang diperlukan lintas file harus diperiksa konsistensinya.
- Media berupa frame/crop dari video asli serta storyboard yang disusun dari frame pilihan. Setiap media memiliki asal yang tercatat; gambar hasil generasi tidak menjadi bukti sumber.
- Paket menyimpan bukti pilihan sesuai ketentuan media di bawah. Tidak menyimpan folder `motion/`, rangkaian seluruh frame atau klip per shot. Video asli tetap satu salinan kanonis di `video/`.
- ZIP dibangun dari keseluruhan revisi terakhir yang diterima pengguna, termasuk pembaruan MD, media dan manifest. Tidak boleh mencampur hasil revisi lama.
- Prompt audit membuat seluruh paket; pengguna cukup mengunduh dan mengunggah ZIP.

### Media per referensi

| File | Ketentuan |
| --- | --- |
| `media/shot-XX/area-overview.jpg` | Wajib per shot: satu frame asli yang paling jelas dan luas memperlihatkan area; biasanya di awal untuk IN dan di akhir untuk OUT. Pemilihan mengikuti gerak serta cakupan nyata sesuai Bagian 6. Pertahankan rasio sumber; tidak harus landscape dan tidak dibuat menjadi panorama atau gabungan frame |
| `media/storyboard.jpg` | Wajib per referensi: gabungan seluruh `area-overview.jpg` sesuai urutan shot, disusun ke bawah dengan label nomor shot, nama area dan timestamp. Setiap gambar tetap proporsional dan terbaca |
| `media/shot-XX/start.jpg`, `middle.jpg`, `end.jpg` | Wajib per shot: frame awal, tengah dan akhir yang mewakili perkembangan komposisi. Frame awal/akhir berada di dalam shot terkait |
| `media/shot-XX/reveal-*.jpg` | Opsional: frame tambahan untuk bagian area yang belum terwakili gambar wajib |
| `media/shot-XX/detail-*.jpg` | Opsional: frame/crop untuk detail penting; crop mencatat timestamp dan area asalnya |

`analysis.md` menampilkan storyboard, gambar gambaran area per shot dan tautan bukti terkait. Jumlah gambar tambahan mengikuti informasi yang perlu ditampilkan, bukan kuota tetap. Resolusi frame individual tetap memadai untuk detail; storyboard menjadi jalur tinjauan cepat.

Bukti pilihan membantu pembaca memahami hasil audit, tetapi tidak menggantikan video untuk memastikan ulang seluruh gerakan dan ritme. Penjelasan kamera lengkap disimpan dalam MD. Jika diperlukan verifikasi visual ulang, gunakan sumber kanonis di `video/`; ini tidak menambah kewajiban review setelah ingest.

## 5. Kontrak laporan Markdown

Gunakan bahasa Indonesia natural dengan istilah teknis konsisten. Tetapkan versi format, heading/anchor stabil, metadata minimal dan tabel yang dapat diparse. Fakta untuk katalog ditulis sekali pada bagian yang ditentukan; narasi memperjelas tanpa menambah klaim. Parser tidak menebak struktur dari prosa bebas.

| Bagian wajib | Kedalaman informasi |
| --- | --- |
| Identitas dan cakupan | Sumber, metadata aktual, metode dan rentang yang diperiksa; hal yang belum diketahui |
| Karakter referensi | Massa, identitas desain, komposisi dan ciri pembeda |
| Storyboard dan timeline | Shot/segmen, fungsi area, batas waktu, transisi serta kontinuitas yang diamati |
| Desain per shot | Bentuk/proporsi visual, plafon, bukaan, finishing, furnitur, penyimpanan, dekorasi, cahaya dan lingkungan |
| Konfigurasi dan hubungan | Kombinasi fungsi, posisi relatif, orientasi, pembatas, sirkulasi yang terlihat, titik perhatian |
| Perkembangan komposisi | Awal, perubahan sepanjang shot, akhir, foreground/background, oklusi dan informasi yang terungkap |
| Sudut pandang dan gambaran area | Timestamp dan alasan pemilihan `area-overview.jpg`, perannya pada awal/tengah/akhir lintasan, posisi kamera relatif terhadap area/subjek, arah pandang, ketinggian visual, sudut frontal/serong/samping serta hubungan komposisi dengan gerakan |
| Gerakan dan ritme | Ringkasan Inggris, bukti, interpretasi, fase/interval, arah, estimasi, tempo, perubahan kecepatan dan confidence |
| Hubungan antarshot | Elemen konsisten/berbeda; adjacency yang didukung dan yang belum diketahui |
| Ketidakpastian dan bukti | Batas klaim, timestamp, tautan media dan lokasi temuan terkait |

Lengkap berarti seluruh informasi yang terlihat dicatat; tidak ada jumlah objek minimum. Material tampak, musim, ukuran dan lokasi tidak dipastikan tanpa dukungan. Kiri/kanan layar dibedakan dari orientasi rumah. Segmen fungsi tidak otomatis dianggap cut atau shot baru.

MD dapat dibaca mandiri, memakai gambar inline dan tautan relatif. Ringkasan berada di atas, rincian per shot di bawah; tidak memotong detail demi batas panjang profil. Ringkasan katalog tidak menjadi laporan kedua yang diedit manual.

## 6. Protokol audit dan kamera

1. Identifikasi sumber dan metadata; catat mekanisme pemeriksaan yang benar-benar tersedia di chat.
2. Tinjau perkembangan seluruh durasi, tentukan batas shot/segmen dan transisi.
3. Saat audit, periksa perkembangan gambar berinterval konsisten, lalu rapatkan pemeriksaan pada perubahan gerak, oklusi, transisi dan detail meragukan. Untuk ZIP final, pilih media sesuai Bagian 4; seluruh frame pemeriksaan tidak perlu disimpan. Pertahankan frame resolusi asli untuk detail.
4. Audit desain, konfigurasi, komposisi serta gerak dalam lintasan pemeriksaan terpisah.
5. Tampilkan hasil lengkap di chat; terapkan koreksi pengguna ke seluruh paket sebelum ekspor.

Pisahkan:

- perubahan gambar yang diamati dan interpretasi dolly/pan/tracking/orbit/zoom;
- tempo lambat/sedang/cepat dari kelancaran gerak;
- fase simultan/berurutan, percepatan/perlambatan, dan ritme pengungkapan;
- gerakan kamera, gerakan objek, deformasi generatif dan transisi edit.

Setiap fase memiliki rentang waktu, subjek/jangkar, bukti perubahan, interpretasi dan ketidakpastian. Jangan memaksakan semua shot memiliki In/Out, pan atau orbit. Jangan mengarang sudut fisik, jarak atau kecepatan dunia nyata dari label visual.

Rubrik tempo dikalibrasi melalui pilot pada durasi dan perubahan visual, bukan kata `smooth`. Ukuran pergeseran gambar bila tersedia tetap merupakan petunjuk, bukan pengukuran kamera fisik. Sampling, playback dan pemeriksaan setiap frame dicatat berbeda; status frame-by-frame penuh hanya untuk rentang yang benar-benar diperiksa seluruhnya.

Tidak ada janji Gemini dan GPT menghasilkan jawaban identik. Konsistensi ditopang template, rubrik, contoh kalibrasi, bukti dan koreksi di chat.

### Gambaran area dan posisi kamera

`area-overview.jpg` menjadi referensi desain sekaligus sudut pandang kamera untuk pembuatan gambar baru. Pilih satu frame yang paling lengkap dan jelas memperlihatkan area dengan aturan awal berikut:

| Gerakan sumber | Posisi frame gambaran area yang biasanya sesuai |
| --- | --- |
| IN, misalnya Dolly-In | Awal shot, sebelum kamera mendekati subjek dan cakupan menyempit |
| OUT, misalnya Dolly-Out | Akhir shot, setelah kamera menjauh dan lebih banyak area terlihat |
| Pan, orbit, tracking atau gabungan fase | Pilih berdasarkan cakupan nyata dan keterbacaan area; catat fase serta alasan pemilihannya |

Aturan IN/OUT merupakan panduan pemilihan, bukan pengganti pemeriksaan video. Jika oklusi, belokan atau gabungan gerak membuat frame lain lebih mewakili area, gunakan frame tersebut dan jelaskan alasannya.

Pada setiap shot, MD mencatat timestamp gambaran area, posisinya dalam lintasan sumber, serta posisi dan arah pandang kamera relatif terhadap subjek/ruang. Jelaskan sudut frontal, serong atau samping yang benar-benar terlihat, foreground, kedalaman, target gerak dan bagian yang terungkap sepanjang lintasan. Estimasi ketinggian atau kemiringan diberi ketidakpastian; koordinat, jarak dan lensa fisik yang tidak diketahui tidak dikarang.

Saat AI memakai pustaka untuk menyusun konsep dan prompt gambar, adaptasi posisi, arah pandang, framing dan hubungan kedalaman yang mendukung gerakan yang direncanakan. Hindari default frontal untuk semua ruang; sudut mengikuti bukti dan kebutuhan lintasan. Peran frame harus jelas: gambaran area pada akhir Dolly-Out adalah referensi sudut pandang akhir sumber, sedangkan komposisi awal sumber ditunjukkan oleh `start.jpg`. Pemilihan gambar awal produksi mempertimbangkan peran tersebut dan arah gerakan yang dituju.

### Format ringkasan gerakan kamera

Gunakan gaya ringkasan pada [Master Prompt Omni Flash v2, Bagian 5.2](../bekerja/masterprompt/omniflash-v2.md). Istilah gerakan ditulis dalam bahasa Inggris, penjelasan audit dalam bahasa Indonesia. Setiap shot mempunyai satu ringkasan singkat yang tetap terbaca bersama bukti, urutan fase dan tempo.

Berurutan:

```text
Orbit Right (~15°–20°) →
Accelerating Dolly-In (~2×) toward teak entrance door.
```

Simultan:

```text
Dolly-In (~1.3×) +
Orbit Left + strong Pan Right (~35°).
```

```text
Dolly-In (~2×) +
gentle Pan Right (~15°).
```

| Unsur | Arti dan aturan |
| --- | --- |
| `→` | Urutan fase dalam satu shot; tidak menyatakan cut. Setiap fase mempunyai interval waktu |
| `+` | Komponen berjalan bersamaan pada interval yang dijelaskan; bukan urutan gerak |
| `Left/Right` | Arah gerak/rotasi kamera sesuai jenis geraknya; dibedakan dari pergeseran objek di layar |
| `~15°–20°`, `~35°` | Estimasi sudut visual dengan dasar dan ketidakpastian; tidak wajib diisi jika tidak dapat diperkirakan |
| `~1.3×`, `~2×` | Estimasi pendekatan/perubahan skala terhadap jangkar yang disebut; bukan ukuran jarak fisik atau faktor percepatan |
| `Accelerating` | Percepatan yang terlihat sepanjang interval, dicatat terpisah dari rasio pendekatan |
| `strong/gentle` | Karakter komponen terkait; tidak otomatis menentukan tempo seluruh shot |
| `toward ...` | Target nyata yang dituju atau menjadi fokus akhir |

Contoh di atas menetapkan format, bukan gerakan, angka atau material wajib untuk referensi. Pan/orbit tunggal maupun kombinasi lain tetap sah. Ringkasan tidak boleh menambah komponen hanya untuk menyerupai contoh.

Catat gerakan menurut urutan video sumber yang diaudit. Jangan membalik arah untuk reverse, menerapkan durasi produksi 4/6 detik atau mengganti tempo sumber dengan default masterprompt. Jika bukti hanya mendukung interpretasi terbatas, pertahankan ketidakpastiannya pada penjelasan. Ringkasan, tabel fase dan bukti harus konsisten.

Parser menyimpan komponen, hubungan urutan/simultan, interval, arah, karakter, estimasi dan jangkar sebagai proyeksi dari MD. Laporan serta katalog mempertahankan notasi `→`, `+`, `~`, `°` dan `×`; normalisasi tidak menghilangkan maknanya.

## 7. Ingest otomatis dan revisi

`Upload/push ZIP → validasi → staging → ekstraksi → proyeksi data → build katalog/knowledge → pemeriksaan → publikasi atomik.`

- Workflow mengenali seluruh ZIP baru pada event, bukan memilih file terbaru saja. Sediakan pemicu manual untuk retry paket yang sama.
- Periksa versi kontrak, ID, inventaris file, struktur MD, waktu/media, hash, tautan, sumber dan konsistensi field.
- Ekstraksi membatasi path dan ukuran; tolak traversal, symlink, file eksekusi dan nama bentrok. Isi ZIP tidak dijalankan sebagai kode.
- Bangun keluaran pada staging. Paket gagal tidak mengubah referensi aktif maupun halaman turunannya.
- Gunakan fingerprint paket sebagai identitas ingest: replay identik tidak membuat referensi/commit baru.
- Revisi baru menyebut versi/hash yang digantikan. Konflik isi pada ID/revisi yang sama ditolak; tidak menimpa diam-diam.
- Serialkan publikasi dan bangun ulang terhadap registry terbaru agar unggahan berdekatan tidak menghilangkan hasil. Commit bot tidak memicu loop.
- Catat hasil `imported`, `unchanged` atau `failed` beserta path/error teknis yang spesifik. Tidak membuat antrean review isi atau meminta approval tambahan.
- Revisi sumber memperbarui semua dependennya. Bukti yang tidak lagi cocok tidak dipertahankan sebagai bukti aktif.
- Tetapkan retensi ZIP dan media sebelum ingest massal; jangan menghapus unggahan diam-diam. Ukur pertumbuhan penyimpanan dan hindari duplikasi video.

## 8. Katalog dan knowledge otomatis

Katalog dibangun dari semua referensi aktif dalam registry, tanpa angka atau daftar ID yang dibekukan. Gunakan kategori dan alias berversi; label baru tetap tersimpan dan dapat ditemukan walau belum memiliki kategori. Negasi, alternatif dan nilai kosong tidak diubah menjadi fakta positif.

| Keluaran | Isi |
| --- | --- |
| Katalog ruang | Geometri, kombinasi fungsi, konfigurasi furnitur, penyimpanan, bukaan dan pembeda |
| Arsitektur/lingkungan | Massa, atap, skala visual, tampilan material, cahaya dan lanskap |
| Komposisi | Posisi/arah pandang kamera relatif terhadap area, sudut frontal/serong/samping, kedalaman, oklusi, subjek, pola reveal serta tautan gambaran area dan perannya dalam lintasan |
| Kamera | Gerakan/fase/tempo yang tercatat, bukti dan ketidakpastian |
| Knowledge | Ringkasan, matriks perbandingan, variasi, hitungan dan pengecualian dari audit final |

Knowledge diperbarui deterministik menggunakan template dan data eksplisit, tanpa sintesis AI bebas pada ingest. Semua klaim memiliki pointer ke referensi, shot, bagian laporan dan bukti terkait. Satu contoh tidak menjadi pola universal; label tidak tercatat tidak membuktikan objek tidak ada.

Konflik dipertahankan sebagai perbedaan, tidak dirata-ratakan. Frekuensi menyebut denominator dan unit hitung; video berbeda belum tentu rumah independen. Duplikat sumber diperiksa ketika byte tersedia. Knowledge tidak mengarang penyebab virality, material pasti, denah terukur atau konfigurasi baru.

Prinsip umum yang kelak ditulis terpisah diberi jenis klaim yang jelas dan tidak ditulis ulang setiap ingest. Penalaran kreatif proyek dilakukan AI pembaca dengan menelusuri sumber.

## 9. Skalabilitas dan pengalaman pembaca

- Navigasi: README → kategori/tema → contoh pembeda → shot/bukti; tidak mewajibkan seluruh repo dibaca.
- Indeks ringan memuat ringkasan dan tautan; detail dipisah per referensi dan kategori. Pecah halaman kategori yang terlalu besar berdasarkan batas yang diuji.
- Kamera dan ruang memiliki pencarian sendiri; pilihan contoh tidak hanya mengulang referensi terpopuler atau urutan pertama.
- Pertahankan seluruh variasi; sorot perbedaan konfigurasi, bentuk, bukaan dan fokus, bukan perubahan warna saja.
- Gunakan fingerprint dan peta dependensi untuk pembaruan terarah. Rebuild penuh tetap tersedia untuk memeriksa kesetaraan.
- Pertahankan ID dan anchor yang stabil; perubahan versi kontrak memiliki migrasi eksplisit. Tidak ada schema churn per video.
- Uji pertumbuhan dengan fixture ratusan referensi; data sintetis hanya untuk tes kapasitas dan tidak masuk pustaka aktif.

## 10. Dua phase implementasi

### Phase 1 — Fondasi repo dan otomasi pustaka

| Pekerjaan | Keluaran |
| --- | --- |
| Struktur dan navigasi | README, jalur pembaca, pemisahan arsip dan sumber aktif |
| Kontrak teknis awal | Format ZIP/MD/manifest/media, identitas, notasi kamera, revisi dan retensi |
| Importer dan validasi | Parser, staging, hash sumber, registry, replay, penanganan konflik dan kegagalan |
| Katalog dan knowledge | Generator deterministik, sumber klaim, alias dan peta dependensi |
| Workflow dan pengujian | Ingest GitHub, fixture valid/gagal, pengujian revisi serta simulasi ratusan referensi |

**Syarat selesai:** paket contoh sesuai kontrak memperbarui seluruh keluaran tanpa publikasi parsial atau review isi ulang. Data sintetis tetap di fixture dan tidak menjadi referensi aktif. Pengujian teknis belum membuktikan kenyamanan workflow chat atau ketepatan audit video.

Kontrak awal diperlukan agar parser dan generator dapat dibangun. Kontrak belum dibekukan; pengalaman pilot pada Phase 2 dapat memperbaikinya melalui perubahan berversi dan pembaruan fixture/generator yang sesuai. Prompt audit lengkap dan panduan penggunaan chat dikerjakan pada Phase 2.

### Phase 2 — Workflow audit Gemini/ChatGPT dan tujuh pilot

| Pekerjaan | Keluaran |
| --- | --- |
| Perangkat audit | Prompt lintas AI, template laporan, rubrik desain/komposisi/kamera/tempo dan contoh kalibrasi |
| Review dan ekspor di chat | Hasil lengkap ditampilkan, koreksi pengguna diterapkan, satu ZIP final dari versi terbaru |
| Audit tujuh pilot | Paket nyata dari chat yang akan dipakai pengguna; penggunaan Gemini dan GPT diuji tanpa mewajibkan setiap video diaudit dua kali |
| Uji alur lengkap | Upload ZIP, ingest, laporan/media, katalog dan knowledge; format tidak perlu diperbaiki manual setelah download |
| Penyempurnaan standar | Perbaikan kontrak/tooling dari hasil pilot, penetapan versi stabil dan panduan penambahan berikutnya |

**Pembagian tugas:** asisten implementasi membangun tooling, prompt/template dan menguji paket serta keluaran repo. Gemini/ChatGPT pada chat audit memeriksa video dan membuat ZIP. Pengguna memeriksa serta meminta koreksi isi di chat sebelum download. Audit di chat ini juga dapat dilakukan bila diminta, tetapi workflow harus diuji pada lingkungan chat yang akan digunakan sehari-hari.

**Syarat selesai:** ketujuh ZIP final dapat diproses tanpa menata file atau review isi ulang di repo; rincian desain, notasi/fase/tempo kamera dan sumber bukti tetap terbaca dalam keluaran. Kontrak stabil setelah pengalaman penggunaan tersebut.

### Daftar tujuh video pilot

ID paket baru mengikuti stem file sumber. Nama kanonis video tambahan adalah `dreamshome01.mp4` dan `edh001.mp4`; ID `VID-XXX` dalam arsip lama tidak menjadi ID paket baru.

| Urutan | Video sumber | Fokus validasi |
| --- | --- | --- |
| 1 | [edh058.mp4](../video/edh058.mp4) | Laporan dasar: area terpisah, timeline, detail desain, wardrobe dan media |
| 2 | [edh013.mp4](../video/edh013.mp4) | Bentuk organik, bukaan bundar, bathroom dengan platform bertingkat dan konfigurasi khas |
| 3 | [edh033.mp4](../video/edh033.mp4) | Open-plan, sleeping loft, bathroom–laundry dan beberapa fungsi dalam satu shot |
| 4 | [edh049.mp4](../video/edh049.mp4) | Bangunan/kitchen melengkung, perubahan perspektif, cakupan ruang dan pembedaan gerakan |
| 5 | [edh056.mp4](../video/edh056.mp4) | Kontinuitas exterior–interior, fase gerak, batas cut dan segmen fungsi |
| 6 | [dreamshome01.mp4](../video/dreamshome01.mp4) | Pembanding deskripsi arah, ritme dan perkembangan komposisi antarruang |
| 7 | [edh001.mp4](../video/edh001.mp4) | Pembanding kelengkapan area dan konfigurasi bathroom–laundry |

Mulai dari `edh058` untuk menguji satu alur lengkap, lalu terapkan pada enam video lainnya. Daftar ini menetapkan bahan pilot, bukan hasil audit baru. Gerak, tempo, kontinuitas dan batas shot diperiksa ulang dari video asli.

Setelah standar stabil, ketujuh paket menjadi referensi aktif pertama. Pengisian sisa koleksi awal dan penambahan hingga ratusan video merupakan operasi berkelanjutan setelah Phase 2, memakai workflow yang sama. Semua referensi lama memerlukan audit baru untuk masuk pustaka baru; tujuh pilot termasuk koleksi awal tersebut.

## 11. Verifikasi dan kriteria penerimaan

- Alur nyata: pengguna download satu ZIP, upload/push, lalu referensi dan halaman turunannya tersedia tanpa menata file atau review isi ulang.
- Parser/kontrak: uji field hilang, format rusak, shot gabungan, nilai unknown, negasi, timestamp dan media tidak cocok.
- Media: setiap shot memiliki satu frame `area-overview.jpg` dan frame awal/tengah/akhir; storyboard tersusun dari seluruh gambaran area tersebut dalam urutan yang benar. Periksa label, rasio, keterbacaan dan asal frame pada pilot; tidak ada folder `motion/` atau rangkaian seluruh frame dalam paket.
- Sudut pandang: pilot menguji gambaran area IN di awal dan OUT di akhir, termasuk pengecualian yang beralasan. MD menyimpan posisi/arah pandang kamera serta peran frame agar AI dapat menentukan komposisi gambar yang cocok dengan lintasan, termasuk sudut serong/samping yang didukung sumber.
- Ingest: uji paket gagal, replay, duplikasi sumber, revisi, konflik, retry dan dua unggahan berdekatan; tidak ada publikasi parsial.
- Penelusuran: setiap pernyataan turunan dapat ditelusuri ke audit; tautan lokal/gambar valid; ringkasan tidak memperkuat ketidakpastian menjadi kepastian.
- Kreativitas pustaka: katalog dapat menemukan beberapa konfigurasi bathroom dan ruang lain yang berbeda secara susunan, geometri dan fungsi, bukan warna saja.
- Kamera: pilot menyimpan bukti fase, tempo dan perkembangan komposisi; tidak memberi label slow hanya karena gerak halus. Uji round-trip notasi urutan/simultan, rentang sudut, rasio dan karakter; proyeksi tidak menukar arah atau menyisipkan gerakan.
- Generator: input sama menghasilkan keluaran sama; revisi menghapus proyeksi usang; build terarah setara build penuh.
- Batas pengujian: validasi kode tidak membuktikan fakta visual atau keberhasilan video generatif. Catat evaluasi penggunaan AI yang benar-benar dijalankan, terpisah dari tes format.
- Integritas: arsip tidak berubah dan tidak ikut discovery; seluruh hitungan berasal dari registry aktif; data tes tidak menjadi sumber.

## 12. Langkah berikutnya

Mulai Phase 1 dengan struktur dan kontrak teknis awal, kemudian satu fixture ZIP valid serta satu fixture gagal. Implementasikan parser/importer, generator dan workflow sampai alur otomatis lolos pengujian. Lanjutkan Phase 2 untuk menyusun perangkat audit lengkap, menjalankan tujuh pilot di chat Gemini/ChatGPT, lalu menetapkan standar berdasarkan paket nyata.

Implementasi saat ini berfokus pada pustaka. Masterprompt hanya menjadi acuan format ringkasan kamera; perubahan plugin dan instruksi produksi berada di luar pekerjaan ini.
