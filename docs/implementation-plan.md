# Rencana Implementasi Pustaka HOMEKU

Dibuat: 21 November 2026

Diperbarui: 22 November 2026

Status: Phase 1 terimplementasi; perangkat Phase 2 tersedia. Pilot edh001 sudah diaudit ulang, disetujui, diekspor dan di-ingest sebagai referensi aktif lokal; enam pilot lain menunggu pelaksanaan pengguna di ChatGPT/Gemini. Kontrak belum dibekukan. Aktivasi hosted menunggu push/run GitHub.
Pelaksanaan dibagi menjadi dua phase: fondasi dan otomasi, kemudian workflow audit dan pilot. Penyempurnaan langkah 1–3 tersedia: MD 1.1 dengan profil DNA, JSON pembaca/indeks, prinsip terkurasi dan audit adaptif pada tooling. Audit ulang edh001 telah disetujui pengguna dan diekspor final dalam format 1.1; ingest edh001 selesai, sedangkan enam pilot lain masih menunggu pelaksanaan.

**Hubungan dokumen:** [plan improvement Phase 2](phase-2-audit-improvement-plan.md) merinci dan memperbarui bagian format laporan, profil DNA/pengetahuan, akses AI, audit kamera, tinjauan pengguna dan batas pengujian. Jika ada perbedaan pada bagian tersebut, ketentuan plan improvement berlaku; ketentuan lain pada plan utama tetap berlaku. Status implementasi terbaru dan batas pengujian dicatat pada [verifikasi improvement](phase-2-improvement-verification.md).

## 1. Tujuan dan batas pekerjaan

Bangun pustaka yang tumbuh dari 57 referensi awal menjadi ratusan video. AI kreatif dapat menemukan variasi desain, memahami komposisi dan mengadaptasi gerakan kamera berdasarkan bukti referensi. Laporan Markdown harus lengkap dan nyaman dibaca manusia. Jalur utama AI adalah indeks JSON, JSON referensi/shot terpilih, media dan knowledge terkait; seluruh isi audit penting harus tersedia tanpa mewajibkan pembacaan MD.

Audit dan koreksi isi dilakukan di chat Gemini/GPT. Pengguna meninjau kartu dan gambar setiap shot, terutama kamera, tempo dan detail yang kurang, lalu mengunduh ZIP final. MD lengkap tetap tersedia dan mudah dibaca; pengguna tidak diwajibkan membaca seluruh tabel teknis. Persetujuan satu aspek tidak dianggap persetujuan seluruh audit. Upload ZIP ke repo menjadi penyerahan versi final; pengguna tidak diminta review isi lagi setelah ingest.

Plugin produksi baru berada di luar lingkup. `archive/oldrepo/` menjadi arsip, dikecualikan dari discovery, pencarian, build dan hitungan aktif. Anotasi lama tidak otomatis menjadi pengetahuan baru. Video asli di `video/` tetap dapat digunakan; jumlah file video tidak sama dengan jumlah referensi aktif. Kemampuan pengetahuan lama ditelaah untuk dipertahankan melalui profil DNA, alias, serta prinsip desain terkurasi; arsip tidak menjadi input generator. Tidak ditambahkan tahap pengujian manfaat pustaka, perbandingan hasil kreatif antarrepo, percobaan membuat konsep atau generate gambar.

## 2. Keputusan arsitektur

| Keputusan | Ketentuan |
| --- | --- |
| Satuan penyerahan | Satu ZIP per video per revisi; pengguna tidak mengurus file turunan satu per satu |
| Sumber isi | `references/<id>/analysis.md`; metadata teknis dan daftar media berada dalam manifest |
| Data AI dan pencarian | JSON per referensi serta indeks dihasilkan otomatis dari MD dan metadata terkait; tidak ada `analysis.json` yang diedit terpisah |
| Status final | Upload merupakan penerimaan versi audit; keberhasilan validasi teknis bukan verifikasi kebenaran visual |
| Pembaruan otomatis | Referensi, indeks, katalog, perbandingan dan ringkasan knowledge berbasis sumber |
| Pemeriksaan isi | Selesai di chat sebelum ZIP; repo tidak menjalankan audit video ulang atau mengganti interpretasi |
| Model operasi | Generator deterministik; tanpa API AI berbayar, database atau layanan pencarian wajib |
| Kamera | Notasi dari `omniflash-v2.md`; rubrik pemeriksaan dari `audit-video.md`; isi tetap mengikuti video sumber |
| Pembaca | Manusia membaca MD dan media; AI memakai indeks JSON lalu JSON referensi terpilih, media dan knowledge; pembaca tidak perlu menjalankan tooling repo |

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
sources/                 # Prinsip umum terkurasi; input generator, bukan fakta video
data/                   # Registry, JSON referensi, indeks pencarian dan rekam ingest
tools/                  # Importer, parser, validator dan generator
tests/                  # Fixture serta pengujian kontrak dan alur
.github/workflows/      # Ingest dan CI
archive/oldrepo/         # Arsip pustaka sebelumnya
```

README menyediakan tiga jalur: mengaudit/menambahkan video, mencari referensi, dan memahami knowledge. Dokumen produksi di `bekerja/` tetap terpisah dari jalur pustaka. `omniflash-v2.md` menjadi acuan notasi kamera; rubrik pada `audit-video.md` menjadi acuan pemeriksaan kamera pada Bagian 6. Default produksi keduanya tidak diterapkan pada sumber. Perbarui `video/README.md` yang masih menjelaskan workflow lama saat workflow baru tersedia.

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
- Sumber isi audit yang dikoreksi berada dalam MD. Manifest tidak menduplikasi fakta desain/kamera; field yang diperlukan lintas file diperiksa konsistensinya. JSON untuk AI dibangun otomatis oleh repo dan tidak menambah file yang harus ditata pengguna dalam ZIP.
- Media berupa frame/crop dari video asli serta storyboard yang disusun dari frame pilihan. Setiap media memiliki asal yang tercatat; gambar hasil generasi tidak menjadi bukti sumber.
- Paket menyimpan bukti pilihan sesuai ketentuan media di bawah. Tidak menyimpan folder `motion/`, rangkaian seluruh frame atau klip per shot. Video asli tetap satu salinan kanonis di `video/`.
- ZIP dibangun dari keseluruhan revisi terakhir yang diterima pengguna, termasuk pembaruan MD, media dan manifest. Tidak boleh mencampur hasil revisi lama.
- Prompt audit membuat seluruh paket; pengguna cukup mengunduh dan mengunggah ZIP.

### Media per referensi

| File | Ketentuan |
| --- | --- |
| `media/shot-XX/area-overview.jpg` | Wajib per shot: satu frame asli yang paling jelas dan luas memperlihatkan area; biasanya di awal untuk IN dan di akhir untuk OUT. Pemilihan mengikuti gerak serta cakupan nyata sesuai Bagian 6. Pertahankan rasio sumber; tidak harus landscape dan tidak dibuat menjadi panorama atau gabungan frame |
| `media/storyboard.jpg` | Wajib per referensi: gabungan seluruh `area-overview.jpg` sesuai urutan shot, disusun ke bawah dengan label nomor shot, nama area dan timestamp. Setiap gambar tetap proporsional dan terbaca |
| `media/shot-XX/start.jpg`, `middle.jpg`, `end.jpg` | Wajib per shot: frame awal, tengah dan akhir yang mewakili perkembangan komposisi. Frame awal/akhir diambil tepat dari frame asli pertama/terakhir di dalam shot terkait, terpisah dari kisi sampling 10 FPS |
| `media/shot-XX/reveal-*.jpg` | Opsional: frame tambahan untuk bagian area yang belum terwakili gambar wajib |
| `media/shot-XX/detail-*.jpg` | Opsional: frame/crop untuk detail penting; crop mencatat timestamp dan area asalnya |

`analysis.md` menampilkan storyboard, gambar gambaran area per shot dan tautan bukti terkait. Jumlah gambar tambahan mengikuti informasi yang perlu ditampilkan, bukan kuota tetap. Resolusi frame individual tetap memadai untuk detail; storyboard menjadi jalur tinjauan cepat.

Bukti pilihan membantu pembaca memahami hasil audit, tetapi tidak menggantikan video untuk memastikan ulang seluruh gerakan dan ritme. Penjelasan kamera lengkap disimpan dalam MD. Jika diperlukan verifikasi visual ulang, gunakan sumber kanonis di `video/`; ini tidak menambah kewajiban review setelah ingest.

## 5. Kontrak laporan Markdown

Gunakan bahasa Indonesia natural dengan istilah teknis konsisten. Tetapkan versi format, heading/anchor stabil, metadata minimal dan tabel yang dapat diparse. Fakta untuk katalog ditulis sekali pada bagian yang ditentukan; narasi memperjelas tanpa menambah klaim. Parser tidak menebak struktur dari prosa bebas.

| Bagian wajib | Kedalaman informasi |
| --- | --- |
| Identitas dan cakupan | Sumber, metadata aktual, metode dan rentang yang diperiksa; hal yang belum diketahui |
| Profil DNA referensi | Gaya/pengaruh beserta dasar interpretasi, skala tampak, massa, atap, bukaan, hierarki material, palet/cahaya, lingkungan, konfigurasi khas dan pembeda dengan bukti/batasnya |
| Storyboard dan timeline | Shot/segmen, fungsi area, batas waktu, transisi serta kontinuitas yang diamati |
| Desain per shot | Bentuk/proporsi visual, plafon, bukaan, finishing, furnitur, penyimpanan, dekorasi, cahaya dan lingkungan |
| Konfigurasi dan hubungan | Kombinasi fungsi, posisi relatif, orientasi, pembatas, sirkulasi yang terlihat, titik perhatian |
| Perkembangan komposisi | Awal, perubahan sepanjang shot, akhir, foreground/background, oklusi dan informasi yang terungkap |
| Sudut pandang dan gambaran area | Timestamp dan alasan pemilihan `area-overview.jpg`, perannya pada awal/tengah/akhir lintasan, posisi kamera relatif terhadap area/subjek, arah pandang, ketinggian visual, sudut frontal/serong/samping serta hubungan komposisi dengan gerakan |
| Gerakan dan ritme | Ringkasan Inggris, bukti, interpretasi, fase/interval, arah, estimasi, tempo, perubahan kecepatan dan confidence |
| Hubungan antarshot | Elemen konsisten/berbeda; adjacency yang didukung dan yang belum diketahui |
| Ketidakpastian dan bukti | Batas klaim, timestamp, tautan media dan lokasi temuan terkait |

Lengkap berarti seluruh informasi yang terlihat dicatat; tidak ada jumlah objek minimum. Material tampak, musim, ukuran dan lokasi tidak dipastikan tanpa dukungan. Kiri/kanan layar dibedakan dari orientasi rumah. Segmen fungsi tidak otomatis dianggap cut atau shot baru.

MD dapat dibaca mandiri, memakai gambar inline dan tautan relatif. Gunakan keterbacaan laporan lama sebagai dasar: identitas/DNA, palet, storyboard/timeline dan rincian shot. Ringkasan berada di atas; tabel teknis lengkap ditempatkan pada bagian yang dapat dilipat. Tidak memotong detail demi batas panjang profil. Ringkasan, narasi dan data terstruktur harus konsisten.

Parser, heading dan kontrak disesuaikan bersama melalui versi yang jelas. JSON per referensi di `data/projections/<id>.json` mempertahankan profil DNA, ringkasan/narasi, cakupan, seluruh shot/fakta/komposisi/fase kamera, hubungan, keterbatasan dan pointer media/sumber. Tetapkan kontrak pembaca JSON yang stabil, terpisah dari metadata cache internal. Ringkasan katalog dan JSON tidak menjadi laporan kedua yang diedit manual.

## 6. Protokol audit dan kamera

1. Identifikasi sumber dan metadata; catat mekanisme pemeriksaan yang benar-benar tersedia di chat.
2. Tinjau perkembangan seluruh durasi, tentukan batas shot/segmen dan transisi.
3. Gunakan audit adaptif: mulai dengan sampling 10 FPS yang mencakup seluruh durasi setiap shot (atau seluruh frame asli bila FPS sumber lebih rendah); periksa seluruh frame asli pada rentang meragukan, lalu seluruh shot bila diperlukan. Pendalaman mengikuti FPS asli sumber, bukan selalu 30 FPS. Ambil frame awal dan akhir shot yang tepat dari sumber secara terpisah dari kisi sampling. Untuk ZIP final, pilih media sesuai Bagian 4; rangkaian seluruh frame tidak disimpan. Pertahankan frame resolusi asli untuk detail.
4. Audit desain, konfigurasi, komposisi serta gerak dalam lintasan pemeriksaan terpisah.
5. Tampilkan kartu setiap shot di chat: gambar area, deskripsi/pembeda, posisi/arah pandang, kamera, ritme dan hal penting yang belum pasti. Sediakan MD lengkap yang mudah dibaca. Terapkan koreksi ke laporan/kartu dan seluruh paket dari snapshot yang sama sebelum ekspor; tidak mewajibkan pengguna membaca seluruh tabel teknis.

Pisahkan:

- perubahan gambar yang diamati dan interpretasi dolly/pan/tracking/orbit/zoom;
- tempo lambat/sedang/cepat dari kelancaran gerak;
- fase simultan/berurutan, percepatan/perlambatan, dan ritme pengungkapan;
- gerakan kamera, gerakan objek, deformasi generatif dan transisi edit.

Setiap fase memiliki rentang waktu, subjek/jangkar, bukti perubahan, interpretasi dan ketidakpastian. Jangan memaksakan semua shot memiliki In/Out, pan atau orbit. Jangan mengarang sudut fisik, jarak atau kecepatan dunia nyata dari label visual.

Rubrik tempo dikalibrasi melalui pilot pada durasi dan perubahan visual, bukan kata `smooth`. Ukuran pergeseran gambar bila tersedia tetap merupakan petunjuk, bukan pengukuran kamera fisik. Catat FPS sampling, rentang serta jumlah frame yang benar-benar dilihat, alasan pendalaman, interval yang diperiksa pada FPS asli dan batas interpretasi; ekstraksi saja bukan pemeriksaan. Gunakan label audit adaptif 10 FPS dengan cakupan pendalaman yang nyata. Jangan mengklaim frame-by-frame penuh jika hanya sebagian frame diperiksa. Pendalaman wajib dilakukan saat pan/orbit/truck sulit dibedakan, batas fase/arah atau laju meragukan, gerak cepat/blur/oklusi mengaburkan perubahan, atau bukti tidak cocok dengan penjelasan/koreksi pengguna. Jika pendalaman yang diperlukan belum dijalankan atau alat tidak memadai, bagian terkait belum dinyatakan selesai. Terapkan tiga tes dari `audit-video.md`: oklusi, paralaks, serta perubahan perspektif/pembingkaian, dengan memperhitungkan gerak maju/mundur dan kemungkinan deformasi.

Tidak ada janji Gemini dan GPT menghasilkan jawaban identik. Konsistensi ditopang template, rubrik, contoh kalibrasi, bukti dan koreksi di chat.

### Aturan penentuan arah, fase dan penyaringan tilt

Adopsi bagian **Aturan Penentuan Arah & Fase** dari [masterprompt audit](../bekerja/masterprompt/audit-video.md) sebagai aturan operasional dalam rubrik, prompt audit/koreksi dan panduan pengisian kamera. Pertahankan batas bukti berikut:

| Aspek | Ketentuan audit |
| --- | --- |
| Pan murni | Pada adegan statis, sapuan gambar ke kiri mendukung Pan Right; sapuan ke kanan mendukung Pan Left. Pastikan petunjuk rotasi pandangan dan bedakan dari gerakan objek |
| Arah orbit/truck | Gunakan foreground dan background yang dapat dilacak. Pergeseran foreground relatif lebih ke kanan mendukung perpindahan kamera ke kiri; relatif lebih ke kiri mendukung perpindahan ke kanan. Periksa bersama oklusi, perubahan sisi/perspektif dan pembingkaian subjek |
| Orbit atau truck | Perubahan sudut mengelilingi jangkar dengan subjek tetap terbingkai mendukung orbit; pergeseran lateral dibaca bersama orientasi kamera untuk menilai truck. Gerakan gabungan boleh dicatat; jangan memaksakan pemisahan yang tidak didukung |
| IN/OUT | Catat Dolly-In/Out bila bukti mendukung, beserta jangkar dan estimasi perubahan skalanya. Pan/orbit/static tidak dipaksa mempunyai komponen maju/mundur |
| Simultan dan berurutan | Catat awal/akhir setiap komponen. `+` berlaku pada interval komponen yang berjalan bersamaan; `→` untuk perubahan fase. Jika komponen mulai/berhenti pada waktu berbeda, pecah fase dan jelaskan waktunya relatif terhadap awal shot serta timestamp sumber |
| Penyaringan tilt tipis | Jangan menambahkan `subtle tilt-up` atau `subtle tilt-down` untuk drift, jitter, goyangan vertikal kecil atau koreksi framing sesaat. Bila relevan, catat sebagai karakter ketidakstabilan, bukan komponen utama kamera |
| Tilt yang layak dicatat | Catat Tilt-Up/Down bila arah pandang vertikal berubah jelas dan berkelanjutan, dengan target/pengungkapan bagian atas atau bawah yang mendukung. Bedakan rotasi tersebut dari perpindahan ketinggian kamera |

Untuk arah lateral, `Δparallax = fg_dx − bg_dx` adalah petunjuk pendukung. Nilai mentah tidak menjadi penentu tunggal arah fisik: dolly, pan, posisi jangkar, perspektif dan deformasi dapat memengaruhinya. Jika bukti tidak cukup, perdalam pada FPS asli dan pertahankan ketidakpastian.

Jangan memastikan penyebab goyangan atau ketiadaan gimbal hanya dari gambar. Aturan penyaringan tilt menjaga agar gerakan utama tidak tercampur dengan ketidakstabilan kecil; aturan ini tidak menghapus tilt yang jelas dari sumber.

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
| `~15°–20°`, `~35°` | Wajib menilai besaran dan mengusahakan estimasi sudut dengan dasar visual; jika belum dapat diperkirakan, jelaskan batasnya tanpa mengarang angka |
| `~1.3×`, `~2×` | Wajib menilai dan mengusahakan estimasi pendekatan/perubahan skala terhadap jangkar; jelaskan bila belum dapat diperkirakan. Bukan ukuran jarak fisik atau faktor percepatan |
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
- Bangun keluaran pada staging. Paket gagal tidak mengubah referensi aktif maupun halaman turunannya. CLI memakai lock dan journal pemulihan; publikasi remote berupa satu commit. Batas pembacaan filesystem lokal dijelaskan dalam panduan operasi.
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
| DNA/arsitektur/lingkungan | Gaya/pengaruh, massa, atap, skala visual, bukaan, tampilan material, palet, cahaya dan lanskap beserta dasar interpretasi |
| Komposisi | Posisi/arah pandang kamera relatif terhadap area, sudut frontal/serong/samping, kedalaman, oklusi, subjek, pola reveal serta tautan gambaran area dan perannya dalam lintasan |
| Kamera | Gerakan/fase/tempo yang tercatat, bukti dan ketidakpastian |
| Knowledge | Ringkasan, matriks perbandingan, variasi, hitungan dan pengecualian dari audit final |

Knowledge diperbarui deterministik menggunakan template dan data eksplisit, tanpa sintesis AI bebas pada ingest. Klaim berbasis referensi memiliki pointer ke referensi, shot, bagian laporan dan bukti terkait. Prinsip umum memiliki identitas sumber serta jenis klaim tersendiri dan tidak disamarkan sebagai pengamatan video. Satu contoh tidak menjadi pola universal; label tidak tercatat tidak membuktikan objek tidak ada.

Konflik dipertahankan sebagai perbedaan, tidak dirata-ratakan. Frekuensi menyebut denominator dan unit hitung; video berbeda belum tentu rumah independen. Duplikat sumber diperiksa ketika byte tersedia. Knowledge tidak mengarang penyebab virality, material pasti, denah terukur atau konfigurasi baru.

Prinsip orisinalitas, kompatibilitas, proporsi, variasi ruang dan kontinuitas ditulis sebagai sumber terkurasi di luar folder keluaran generator, dengan jenis klaim yang jelas. Telaah kemampuan lama tanpa memasukkan arsip ke input aktif; contoh video harus terikat referensi aktif dari ZIP final. Generator menerbitkan prinsip dan perbandingan fakta ke tampilan manusia serta JSON yang sesuai, tanpa menyintesis prinsip baru saat ingest. Penalaran kreatif dan lock DNA proyek tetap dilakukan AI pembaca; keputusan rumah baru dibedakan dari fakta referensi.

## 9. Skalabilitas dan pengalaman pembaca

- Navigasi manusia: README → kategori/tema → contoh pembeda → MD/shot/bukti. Navigasi utama AI: `data/search-index.json` → `data/projections/<id>.json` terpilih → media/knowledge; tidak mewajibkan pembacaan seluruh repo atau MD.
- Indeks ringan memuat gaya/pengaruh, skala, bentuk/atap/bukaan, konfigurasi/pembeda, fungsi ruang, komposisi, kamera/tempo dan pointer JSON/bukti. Normalisasi memakai alias Indonesia/Inggris tanpa menghapus label asli atau menebak fakta. Detail dipisah per referensi/shot dan kategori; pecah halaman kategori yang terlalu besar berdasarkan batas teknis yang diuji.
- Kamera dan ruang memiliki pencarian sendiri; pilihan contoh tidak hanya mengulang referensi terpopuler atau urutan pertama.
- Pertahankan seluruh variasi; sorot perbedaan konfigurasi, bentuk, bukaan dan fokus, bukan perubahan warna saja.
- Gunakan fingerprint dan peta dependensi untuk pembaruan terarah. Rebuild penuh tetap tersedia untuk memeriksa kesetaraan.
- Pertahankan ID dan anchor yang stabil; perubahan versi kontrak memiliki migrasi eksplisit. Tidak ada schema churn per video.
- Uji pertumbuhan dengan fixture ratusan referensi; data sintetis hanya untuk tes kapasitas dan tidak masuk pustaka aktif.

## 10. Dua phase implementasi

### Phase 1 — Fondasi repo dan otomasi pustaka

**Status:** implementasi lokal selesai. [Kontrak teknis](contracts/package-v1.md), [operasi](operations.md) dan [hasil verifikasi](phase-1-verification.md) tersedia; 23 pengujian lulus, termasuk 300 referensi/600 shot sintetis dan konflik push pada remote Git lokal.

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

**Status:** protokol, rubrik, kosakata, prompt audit/koreksi/ekspor, kit portabel dan helper tersedia. [Status pilot](../audit/pilots/README.md) membedakan draf edh001 dari enam audit yang belum dijalankan. [Verifikasi perangkat awal](phase-2-verification.md) mencatat hasil sebelum improvement; [verifikasi improvement](phase-2-improvement-verification.md) mencatat pemeriksaan terbaru. Kelulusan teknis tidak dianggap persetujuan isi atau penyelesaian seluruh pilot.

| Pekerjaan | Keluaran |
| --- | --- |
| Perangkat audit | Prompt lintas AI, MD manusia dengan profil DNA, kontrak JSON pembaca, audit adaptif 10 FPS dengan pendalaman pada FPS asli dan contoh kalibrasi |
| Review dan ekspor di chat | Kartu/gambar setiap shot ditampilkan; MD lengkap tersedia; koreksi diterapkan dan satu ZIP final berasal dari snapshot yang disepakati |
| Audit tujuh pilot | Paket nyata dari chat yang akan dipakai pengguna; penggunaan Gemini dan GPT diuji tanpa mewajibkan setiap video diaudit dua kali |
| Uji alur teknis | Upload ZIP, ingest, laporan/media, kesetaraan MD–JSON, indeks, katalog dan knowledge; format tidak perlu diperbaiki manual setelah download |
| Penyempurnaan standar | Perbaikan kontrak/tooling dari hasil pilot, penetapan versi stabil dan panduan penambahan berikutnya |

**Pembagian tugas terbaru:** asisten membangun perangkat audit dan mengaudit edh001 terlebih dahulu di chat implementasi ini. Pengguna mengaudit enam pilot lain di ChatGPT/Gemini sehari-hari. Pengguna memeriksa serta meminta koreksi isi di chat sebelum download; hasil final masuk melalui ZIP tanpa review isi baru di repo.

**Syarat selesai:** ketujuh ZIP final dapat diproses tanpa menata file atau review isi ulang di repo. MD mudah dibaca; profil DNA, rincian desain, komposisi, notasi/fase/tempo kamera dan bukti tetap lengkap dalam JSON serta keluaran terkait. Kontrak stabil setelah pengalaman pilot tersebut; tidak ditambah benchmark manfaat, percobaan konsep atau generate gambar.

### Daftar tujuh video pilot

ID paket baru mengikuti stem file sumber. Nama kanonis video tambahan adalah `dreamshome01.mp4` dan `edh001.mp4`; ID `VID-XXX` dalam arsip lama tidak menjadi ID paket baru.

| Urutan | Video sumber | Fokus validasi |
| --- | --- | --- |
| 1 | [edh001.mp4](../video/edh001.mp4) | Pilot pertama di chat ini: kelengkapan area, fase/tempo dan konfigurasi bathroom–laundry |
| 2 | [edh058.mp4](../video/edh058.mp4) | Laporan dasar: area terpisah, timeline, detail desain, wardrobe dan media |
| 3 | [edh013.mp4](../video/edh013.mp4) | Bentuk organik, bukaan bundar, bathroom dengan platform bertingkat dan konfigurasi khas |
| 4 | [edh033.mp4](../video/edh033.mp4) | Open-plan, sleeping loft, bathroom–laundry dan beberapa fungsi dalam satu shot |
| 5 | [edh049.mp4](../video/edh049.mp4) | Bangunan/kitchen melengkung, perubahan perspektif, cakupan ruang dan pembedaan gerakan |
| 6 | [edh056.mp4](../video/edh056.mp4) | Kontinuitas exterior–interior, fase gerak, batas cut dan segmen fungsi |
| 7 | [dreamshome01.mp4](../video/dreamshome01.mp4) | Pembanding deskripsi arah, ritme dan perkembangan komposisi antarruang |

Pelaksanaan dimulai dari edh001 di chat ini sesuai instruksi pengguna terbaru. Enam sumber lain dijalankan pengguna di ChatGPT/Gemini; edh058 disarankan sebagai awal uji chat harian. Daftar tujuh sumber tetap sama; hasil dan persetujuan dicatat hanya setelah pemeriksaan yang benar-benar dilakukan.

Setelah standar stabil, ketujuh paket menjadi referensi aktif pertama. Pengisian sisa koleksi awal dan penambahan hingga ratusan video merupakan operasi berkelanjutan setelah Phase 2, memakai workflow yang sama. Semua referensi lama memerlukan audit baru untuk masuk pustaka baru; tujuh pilot termasuk koleksi awal tersebut.

## 11. Verifikasi dan kriteria penerimaan

- Alur nyata: pengguna download satu ZIP, upload/push, lalu referensi dan halaman turunannya tersedia tanpa menata file atau review isi ulang.
- Parser/kontrak: uji field hilang, format rusak, shot gabungan, nilai unknown, negasi, timestamp dan media tidak cocok.
- Media: setiap shot memiliki satu frame `area-overview.jpg` dan frame awal/tengah/akhir; storyboard tersusun dari seluruh gambaran area tersebut dalam urutan yang benar. Periksa label, rasio, keterbacaan dan asal frame pada pilot; tidak ada folder `motion/` atau rangkaian seluruh frame dalam paket.
- Sudut pandang: pilot menguji gambaran area IN di awal dan OUT di akhir, termasuk pengecualian yang beralasan. MD menyimpan posisi/arah pandang kamera serta peran frame agar AI dapat menentukan komposisi gambar yang cocok dengan lintasan, termasuk sudut serong/samping yang didukung sumber.
- Ingest: uji paket gagal, replay, duplikasi sumber, revisi, konflik, retry dan dua unggahan berdekatan; tidak ada publikasi parsial.
- Penelusuran: setiap pernyataan turunan dapat ditelusuri ke audit; tautan lokal/gambar valid; ringkasan tidak memperkuat ketidakpastian menjadi kepastian.
- Kelengkapan indeks/katalog: field gaya, skala, bentuk, konfigurasi, geometri, fungsi, komposisi dan kamera yang dicatat diteruskan beserta alias serta pointer sumber; tidak dibatasi pada warna. Pemeriksaannya berupa pelestarian data, konsistensi pengelompokan dan tautan, bukan percobaan membuat konsep.
- Kamera: pilot memakai sampling 10 FPS sepanjang setiap shot, frame awal/akhir asli yang tepat dan pendalaman pada FPS asli sesuai kebutuhan. Catat cakupan nyata, alasan/interval pendalaman, bukti fase/tempo dan perkembangan komposisi; tidak memberi label slow hanya karena gerak halus atau mengklaim seluruh frame sudah dilihat. Arah/fase mengikuti aturan operasional dan drift/jitter vertikal kecil tidak dilabeli sebagai tilt utama. Uji round-trip notasi urutan/simultan, rentang sudut, rasio dan karakter; proyeksi tidak menukar arah atau menyisipkan gerakan.
- Generator: input sama menghasilkan keluaran sama; revisi menghapus proyeksi usang; build terarah setara build penuh.
- MD–JSON: periksa kelengkapan profil DNA, uraian/fakta, komposisi/kamera, hubungan, status/confidence, keterbatasan dan bukti. Revisi sumber memperbarui indeks/knowledge serta menghapus turunan usang; kontrak JSON pembaca stabil dan berversi.
- Tinjauan: kartu, MD dan ZIP berasal dari snapshot yang sama; persetujuan satu aspek tidak dianggap persetujuan seluruh audit.
- Batas pengujian: pemeriksaan mencakup format, pelestarian isi, indeks/tautan, regenerasi dan alur teknis. Validasi kode tidak membuktikan fakta visual atau keberhasilan generatif. Tidak ada tahap pengujian manfaat pustaka, perbandingan kualitas konsep antarrepo, percobaan membuat konsep atau generate gambar.
- Integritas: arsip tidak berubah dan tidak ikut discovery; seluruh hitungan berasal dari registry aktif; data tes tidak menjadi sumber.

## 12. Langkah berikutnya

Langkah 1–3 dan audit ulang edh001 telah dilaksanakan; lihat [catatan audit ulang](edh001-re-audit.md). Kartu dan MD terbaru sudah disetujui pengguna; ZIP final telah diekspor dari snapshot terkunci, diserahkan melalui incoming/ dan di-ingest menjadi 1 referensi/5 shot aktif lokal. Kit sudah diperbarui; enam audit berikutnya tetap dilaksanakan pengguna di ChatGPT/Gemini.

Setelah paket final diterima, periksa ingest, kelengkapan data/alias, kesetaraan MD–JSON, tautan sumber dan pembaruan katalog/knowledge. Selesaikan pembenahan dari tujuh pilot sebelum membekukan kontrak; tidak ada percobaan konsep/gambar tambahan. Setelah implementasi dipush, buktikan konfigurasi hosted melalui Library checks dan Library ingest.

Implementasi berfokus pada pustaka. `omniflash-v2.md` menjadi acuan notasi kamera dan `audit-video.md` menjadi acuan rubrik pemeriksaan kamera. Default reverse, durasi dan tempo produksi tidak mengganti kronologi sumber; perubahan plugin serta instruksi produksi berada di luar pekerjaan ini.
