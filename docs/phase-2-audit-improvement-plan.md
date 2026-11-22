# Rencana Penyempurnaan Pustaka dan Audit HOMEKU — Phase 2

Dibuat: 21 November 2026

Diperbarui: 22 November 2026

Status: langkah 1–3 telah diimplementasikan pada 22 November 2026: format MD 1.1/profil DNA, kontrak pembaca JSON, standar audit adaptif, prinsip terkurasi, parser/generator/alias dan pemeriksaan teknis. Langkah 4 dan bagian edh001 pada langkah 5 sudah selesai: audit 1.1 disetujui pengguna dan diekspor final; kit telah diperbarui. Ingest paket final edh001 telah selesai secara lokal; enam pilot/kalibrasi berikutnya masih menunggu pelaksanaan. Hasil verifikasi dicatat pada [verifikasi improvement](phase-2-improvement-verification.md).

**Rencana V2 berikutnya:** [plan improvement V2](improvement-v2-plan.md) menjadi acuan perubahan yang belum diterapkan: audit.json sebagai sumber, MD manusia mengikuti [template baku](template-analysis-v2.md), detail desain lengkap, shot multi area, satu kolase per shot dengan panel dinamis dan storyboard satu baris. Untuk implementasi V2, ketentuan baru tersebut mengungguli bagian yang berbeda pada plan ini; uraian format/media 1.1 di sini tetap menjelaskan implementasi yang sedang berlaku.

## 1. Tujuan dan batas pekerjaan

Hasil analisis video menjadi pengetahuan desain dan kamera yang lengkap, mudah dibaca manusia, serta mudah ditemukan dan dipahami AI. Informasinya mendukung pengembangan konsep sesuai brief dan DNA referensi, kontinuitas satu rumah, serta komposisi gambar awal yang cocok dengan gerakan sumber.

Rencana ini menyempurnakan Phase 2 pada [rencana utama](implementation-plan.md).

**Aturan prioritas:** pada bagian format laporan, profil DNA/pengetahuan, akses AI, audit kamera, tinjauan pengguna dan batas pengujian, ketentuan plan improvement ini memperbarui ketentuan lama; ketentuan lain pada plan utama tetap berlaku. Status pelaksanaan pada awal dokumen membedakan tooling yang sudah tersedia dari audit/pilot yang belum selesai.

Fokus pelaksanaan adalah memperbaiki format, pengetahuan, tooling dan workflow audit, lalu menyelesaikan tujuh pilot. Tidak ditambahkan tahap pengujian manfaat pustaka, perbandingan hasil kreatif antarrepo, percobaan membuat konsep atau generate gambar. Pengembangan plugin produksi tetap terpisah.

Sudah ada satu draf audit edh001 yang sedang dikoreksi pengguna. Status belum disetujui atau belum masuk registry tidak menghapus keberadaan draf tersebut. Draf dapat ditelaah untuk perbaikan format dan isi, tetapi tidak menjadi referensi aktif sebelum penyerahan ZIP final.

## 2. Sumber isi dan jalur pembaca

| Komponen | Fungsi dan ketentuan |
| --- | --- |
| `references/<id>/analysis.md` | Satu sumber isi audit; lengkap dan nyaman dibaca manusia |
| `references/<id>/manifest.json` | Metadata teknis, provenance sumber dan inventaris media; bukan salinan fakta desain/kamera |
| `data/projections/<id>.json` | Representasi lengkap referensi untuk AI, dihasilkan otomatis dari MD dan metadata terkait |
| `data/search-index.json` | Indeks ringan untuk menemukan referensi dan shot tanpa memuat seluruh laporan |
| `catalogs/` dan `knowledge/` | Katalog, variasi dan pengetahuan dengan pointer sumber; keluaran generator |
| Media per shot | Bukti visual yang ditautkan dari MD, JSON, katalog dan knowledge |

Alur normal AI: **permintaan pengguna → indeks JSON → JSON referensi/shot terpilih → gambar terkait dan knowledge yang relevan**. AI tidak diwajibkan membaca MD untuk memperoleh isi audit yang sudah tersedia lengkap dalam JSON. MD tetap dapat dibuka sebagai sumber.

JSON tidak ditulis atau dikoreksi terpisah. Perubahan sumber membangun ulang proyeksi, indeks, katalog dan knowledge. Tidak ada `analysis.json` yang diedit manual atau satu JSON besar yang wajib dimuat seluruhnya. Generator tidak menjalankan sintesis AI atau menebak fakta dari prosa.

## 3. Analysis.md yang mudah dibaca manusia

Gunakan keterbacaan laporan lama sebagai dasar penyajian, lalu tambahkan kedalaman informasi baru.

| Bagian | Isi yang ditampilkan |
| --- | --- |
| Identitas dan DNA | Gaya, pengaruh, skala tampak, bentuk bangunan, ciri pembeda dan ringkasan karakter |
| Palet dan suasana | Material tampak, warna, pencahayaan, lingkungan dan mood sebagai interpretasi bila sesuai |
| Storyboard dan timeline | Gambaran seluruh area, urutan shot, waktu dan ringkasan kamera |
| Detail setiap shot | Gambar area; uraian arsitektur, furnitur, susunan, fungsi, dekorasi, cahaya dan lingkungan |
| Komposisi dan kamera | Posisi/arah pandang, gambaran awal–akhir, gerakan, fase, besaran perkiraan dan ritme |
| Hubungan dan batas | Kesamaan/perbedaan antarshot, bukti yang tersedia dan informasi yang belum pasti |
| Data terstruktur | Tabel lengkap untuk parser dalam bagian yang dapat dilipat; tidak mendominasi tampilan utama |

Penjelasan menggunakan bahasa Indonesia natural; notasi gerakan memakai bahasa Inggris. Seluruh informasi penting tetap tersedia dalam MD. Bentuk bagian terstruktur, heading dan parser disesuaikan bersama melalui kontrak berversi; format baru tidak dianggap sudah didukung parser lama.

Narasi, ringkasan dan data terstruktur harus konsisten. Informasi yang dibutuhkan pencarian/generator dicatat eksplisit, tidak hanya tersembunyi di paragraf. Jangan membuat klaim tambahan saat meringkas.

## 4. Profil DNA dan kedalaman desain

Tetapkan profil referensi yang konsisten, dengan sumber bukti serta batas interpretasi:

- Gaya utama, pengaruh gaya dan dasar penilaiannya.
- Skala tampak, proporsi, jumlah tingkat yang terlihat, massa dan bentuk bangunan.
- Bentuk atap, entrance, porch, pola serta keluarga bukaan.
- Hierarki material tampak, palet dan lapisan pencahayaan.
- Lingkungan dan pemandangan di luar jendela.
- Konfigurasi ruang/fungsi yang terlihat, elemen khas dan ciri pembeda.
- Hubungan serta pengulangan elemen antarshot yang memang didukung sumber.

Setiap shot mencatat bentuk, posisi relatif, orientasi, kombinasi fungsi, furnitur/perangkat, penyimpanan, bukaan, dekorasi, sirkulasi yang terlihat dan hubungan antarelemen. Pembeda desain tidak berhenti pada gaya atau warna. Tidak ada kuota furnitur generik.

Bedakan pengamatan, interpretasi, prinsip desain umum dan keputusan konsep baru. Material tampak tidak memastikan material fisik; skala tampak tidak memastikan luas; urutan edit tidak memastikan denah. DNA referensi merupakan hasil pembacaan sumber, sedangkan DNA yang dikunci untuk rumah baru merupakan keputusan proyek.

## 5. JSON dan pencarian untuk AI

Perluas proyeksi yang sudah dihasilkan tooling menjadi antarmuka pembaca dengan kontrak JSON stabil dan berversi.

| Keluaran | Isi yang wajib tersedia |
| --- | --- |
| JSON per referensi | Identitas/revisi, profil DNA, ringkasan, cakupan audit, timeline, seluruh shot, uraian desain, fakta, komposisi, kamera/fase, hubungan antarshot dan keterbatasan |
| Bukti dan provenance | Pointer MD/shot/fakta, tautan media dan perannya, timestamp, identitas/hash sumber serta status/confidence yang terkait |
| Indeks ringan | Gaya/pengaruh, skala, massa/atap/bukaan, konfigurasi dan pembeda, fungsi ruang, komposisi, gerakan serta tempo; pointer ke JSON dan bukti |
| Kosakata | Alias Indonesia/Inggris dan normalisasi label yang jelas; label asli dan istilah baru tetap tersimpan |

Pertahankan seluruh informasi penting, termasuk narasi yang tidak tepat direduksi menjadi tag. Pengetahuan yang belum diketahui, negasi, alternatif dan ketidakpastian tidak dihilangkan. Kontrak pembaca dipisahkan secara jelas dari metadata cache internal.

AI dapat memilih sebagian referensi/shot yang relevan tanpa membaca ratusan MD atau seluruh JSON koleksi. Pastikan rebuild memperbarui dan menghapus turunan usang secara konsisten. Penambahan field dan alias tidak menetapkan fakta yang tidak ditulis dalam sumber.

## 6. Pengetahuan desain dan kemampuan lama yang dipertahankan

Telaah kemampuan pustaka lama: profil DNA, pencarian gaya/skala, orisinalitas, kompatibilitas, proporsi, variasi ruang dan kontinuitas. Tetapkan padanannya pada sumber, format atau tooling baru.

Susun prinsip pendukung untuk membantu AI:

- Mengembangkan variasi massa, atap, bukaan, konfigurasi, furnitur dan lanskap sambil menjaga hubungan dengan DNA.
- Menjaga kesesuaian interior dengan skala dan bentuk rumah baru.
- Memahami hierarki material, cahaya dan lingkungan yang koheren.
- Memahami unsur yang dipertahankan antararea dan unsur yang dapat bervariasi.
- Menghubungkan komposisi gambar awal dengan posisi, arah pandang, target serta fase pertama gerakan kamera.

Prinsip umum ditulis sebagai sumber terkurasi di luar folder keluaran generator; dibedakan dari fakta audit. Generator menerbitkan pengetahuan tersebut dan perbandingan fakta ke tampilan manusia serta data JSON yang sesuai, tanpa menyintesis prinsip baru saat ingest.

Arsip dibaca hanya untuk penelaahan ini. Anotasi lama tidak otomatis menjadi fakta aktif; contoh berbasis video dalam keluaran aktif harus terikat pada referensi yang telah masuk melalui ZIP final. Tidak ada penggabungan arsip ke discovery atau generator. Penyusunan panduan pengetahuan tidak menambah workflow atau plugin produksi.

## 7. Proses audit dan aturan kamera

Audit dilaksanakan dalam pemeriksaan terpisah:

| Pemeriksaan | Yang wajib diperiksa |
| --- | --- |
| Struktur video | Seluruh durasi, batas shot dan transisi |
| Desain | Seluruh aspek desain dan pembeda pada Bagian 4 |
| Komposisi | Posisi awal, arah pandang, framing, foreground, kedalaman, target, gambaran awal/akhir dan pemilihan overview |
| Gerakan | Sampling awal 10 FPS sepanjang setiap shot, lalu pendalaman pada FPS asli untuk menilai arah, paralaks, oklusi, perspektif, skala, fase dan ritme |
| Pemeriksaan silang | Kesesuaian gambar, narasi, profil DNA, fakta, ringkasan kamera dan tabel fase |

**Metode audit adaptif:**

| Tahap | Cakupan |
| --- | --- |
| Awal — 10 FPS | Sampel mencakup seluruh durasi setiap shot; sekitar 40 frame untuk shot 4 detik bila FPS sumber memadai |
| Pendalaman rentang | Periksa seluruh frame asli pada bagian meragukan, misalnya interval 0,5–1 detik; perluas sesuai perubahan yang diamati |
| Pendalaman seluruh shot | Periksa seluruh frame shot jika rentang terbatas belum cukup atau koreksi memerlukan pemeriksaan menyeluruh |

Pendalaman diperlukan ketika pan/orbit/truck belum dapat dibedakan; awal/akhir fase, perubahan arah atau laju belum jelas; gerak cepat, blur atau oklusi mengaburkan perubahan; atau penjelasan tidak cocok dengan bukti/koreksi pengguna. Tambahan frame dinilai dengan tes kamera, bukan dianggap otomatis memperbaiki interpretasi.

FPS asli mengikuti sumber: 24 FPS berarti seluruh frame 24 FPS, 30 FPS berarti 30 FPS, dan 60 FPS berarti 60 FPS. Gunakan frame asli tanpa interpolasi; bila sumber kurang dari 10 FPS, gunakan seluruh frame yang tersedia. Frame awal dan akhir shot diambil tepat dari sumber, terpisah dari sampling 10 FPS.

Catat FPS sampling, rentang dan jumlah frame yang benar-benar dilihat, alasan/interval pendalaman pada FPS asli serta batas interpretasi. Ekstraksi saja bukan pemeriksaan. Sebut metode sebagai audit adaptif 10 FPS dengan pendalaman yang benar-benar dijalankan; jangan mengklaim frame-by-frame penuh untuk shot yang hanya disampling. Jika pendalaman yang diperlukan belum dijalankan atau alat tidak memadai, bagian terkait belum dinyatakan selesai.

Frame pemeriksaan dipakai sementara; paket final tetap menyimpan media pilihan, tanpa rangkaian seluruh frame atau `motion/`.

Aturan kamera:

- Terapkan tiga tes pembeda pan/orbit/truck dari [masterprompt audit](../bekerja/masterprompt/audit-video.md): oklusi, paralaks, serta perubahan perspektif dan pembingkaian. Nilai bersama gerak maju/mundur dan kemungkinan deformasi.
- Gunakan `omniflash-v2.md` khusus sebagai acuan notasi kamera; `audit-video.md` menjadi acuan rubrik pemeriksaan kamera. Bagian produksi pada kedua masterprompt tidak menambah lingkup pekerjaan ini.
- Bedakan arah kamera dari pergeseran objek di layar; gunakan `+` untuk simultan dan `→` untuk berurutan.
- Wajib menilai besaran gerak dan mengusahakan estimasi `~×`/`~°` berdasarkan jangkar visual. Jika belum dapat diperkirakan, jelaskan batasnya; jangan mengarang angka atau menyalin contoh.
- Bedakan rasio perubahan skala, tempo, kelancaran dan percepatan. Pertahankan fase serta kronologi sumber.
- Overview adalah satu frame asli dengan cakupan area terbaik: biasanya awal untuk IN dan akhir untuk OUT. Storyboard menggabungkan seluruh overview. Overview akhir OUT tidak otomatis menjadi frame awal sumber.
- Jelaskan komposisi yang mendukung gerakan pertama. Jangan mengganti sumber dengan default frontal, reverse atau durasi produksi 4/6 detik.

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

Koreksi gerakan shot 02 edh001 yang sudah disetujui pengguna:

```text
Dolly-Out (~2×) + Orbit Left + Pan Right.
```

Persetujuan awal ini khusus gerakan shot 02; setelah audit ulang, pengguna juga menyetujui keseluruhan snapshot. Koreksi sudah diterapkan pada draf 1.1 setelah audit ulang seluruh durasi; lihat [catatan audit ulang](edh001-re-audit.md). Snapshot terbaru sudah disetujui dan diekspor final dengan hash MD terkunci.

## 8. Tinjauan pengguna, koreksi dan ekspor

Tampilkan kartu setiap shot di chat: gambar area, deskripsi singkat, pembeda, posisi/arah pandang, gerakan lengkap, ritme dan hal penting yang belum pasti. Pengguna tidak diwajibkan membaca seluruh tabel teknis. MD lengkap tetap tersedia dan mudah dibaca.

**Upload MP4 + kit → AI mengaudit dan memeriksa hasil → tampil kartu → pengguna mengoreksi → perbarui laporan dan kartu → pengguna menyatakan sesuai → unduh satu ZIP final → ingest dan build otomatis.**

Kartu dan MD berasal dari snapshot yang sama. Koreksi memperbarui seluruh bagian terdampak beserta media/provenance yang relevan. Persetujuan satu aspek tidak dicatat sebagai persetujuan seluruh audit. Ekspor mempertahankan isi yang disepakati dan memvalidasi paket nyata.

Pengguna tetap mengunduh satu ZIP, tanpa menata JSON atau keluaran lain. Repo menghasilkan JSON, katalog dan knowledge secara otomatis; tidak ada review isi tambahan setelah ingest. Validasi teknis bukan bukti kebenaran pengamatan visual.

## 9. File dan komponen yang terdampak

| Kelompok | Perubahan |
| --- | --- |
| `docs/implementation-plan.md` | Selaraskan tujuan, keputusan format, akses AI dan kriteria selesai |
| `docs/contracts/` | Kontrak MD yang terbaca manusia, profil DNA, JSON pembaca, indeks, provenance dan penyesuaian versi |
| `audit/template-analysis.md` | Susunan manusia, profil DNA, data terstruktur dan panduan pengisian arah/fase kamera tanpa tilt tipis |
| `audit/protocol.md`, `rubric.md`, `vocabulary.md`, `calibration.md` | Audit adaptif, aturan arah/fase, penyaringan tilt tipis, istilah/alias dan contoh yang benar-benar diterima |
| `audit/prompts/*` | Terapkan aturan arah/fase dan penyaringan tilt pada audit/koreksi; kartu tinjauan serta ekspor konsisten; keluarkan uji konsep/gambar dari workflow dan kit aktif |
| Sumber prinsip desain terkurasi | Tambahkan pengetahuan pendukung di luar folder keluaran generator |
| `tools/homeku/` dan helper audit | Parser, validasi, JSON lengkap, indeks, katalog/knowledge, default sampling 10 FPS, pendalaman FPS asli, media dan konsistensi snapshot |
| `data/taxonomy.json` | Perluas alias yang eksplisit sesuai kontrak; pertahankan label asli |
| `tests/` | Pemeriksaan teknis MD–JSON, field/status/bukti, alias, revisi/regenerasi serta pemilihan frame dan pencatatan cakupan audit adaptif |
| Panduan dan `audit/homeku-audit-kit.zip` | Selaraskan akses manusia/AI dan bangun ulang kit |
| Pilot edh001 | Audit ulang, terapkan koreksi, lalu bangun ulang laporan/paket untuk tinjauan pengguna |

Keluaran `catalogs/`, `knowledge/`, proyeksi dan indeks diperbarui melalui generator saat implementasi; tidak dirawat manual. Penyimpanan video tetap satu salinan kanonis dan media final mengikuti kontrak yang telah disepakati.

## 10. Urutan pelaksanaan dan kriteria selesai

1. **Terimplementasi:** susunan MD 1.1, profil DNA, kontrak JSON dan jalur pencarian; pemetaan kemampuan lama.
2. **Terimplementasi:** standar audit, template, prompt dan sumber prinsip desain.
3. **Terimplementasi:** parser, validasi, generator, alias dan pemeriksaan teknis.
4. **Selesai untuk edh001:** seluruh durasi diaudit ulang, koreksi shot 02 diterapkan, laporan 1.1 dan kartu dari snapshot yang sama telah disetujui pengguna.
5. **Ekspor selesai:** paket edh001 final dihasilkan dengan hash MD terkunci; kit terbaru tersedia untuk enam pilot berikutnya di ChatGPT/Gemini. Ingest lokal sudah dijalankan: edh001 aktif, JSON/katalog/knowledge diperbarui otomatis.
6. Selesaikan kalibrasi serta pembenahan kontrak dari tujuh pilot sebelum membekukan versi.

Enam pilot berikutnya: edh058, edh013, edh033, edh049, edh056 dan dreamshome01. Dilaksanakan pengguna di ChatGPT/Gemini; penyiapan kit tidak dihitung sebagai audit selesai.

Kriteria selesai:

- MD mudah dipahami dan memuat seluruh hasil audit; kartu tidak menyembunyikan informasi penting.
- Profil DNA, desain, komposisi, kamera, bukti dan batas pengamatan tercatat lengkap serta eksplisit. Audit mencakup seluruh durasi pada sampling 10 FPS, frame awal/akhir asli yang tepat dan pendalaman sesuai kebutuhan; metode serta rentang nyata tercatat tanpa klaim pemeriksaan seluruh frame yang tidak dilakukan. Arah/fase mengikuti bukti dan drift/jitter vertikal kecil tidak dilabeli sebagai tilt utama.
- JSON mempertahankan isi penting MD dan metadata terkait; AI mempunyai jalur indeks dan data referensi yang mandiri dari pembacaan MD.
- Katalog/knowledge mengikuti sumber dan alias yang konsisten, dengan status serta pointer yang terjaga.
- Chat, MD dan ZIP berasal dari snapshot yang disepakati; seluruh turunan repo diperbarui otomatis.
- Tujuh pilot selesai sesuai pembagian tugas, tanpa review isi baru setelah ingest atau penyimpanan seluruh frame.
- Pemeriksaan teknis yang relevan lulus:

```sh
python -m unittest discover -s tests -t . -v
python tools/library.py check
python tools/build_audit_kit.py --check
```

Tidak ada kriteria tambahan berupa benchmark manfaat pustaka, perbandingan kualitas konsep antarrepo atau percobaan generate gambar. Pemeriksaan teknis di atas memastikan format, pelestarian isi dan otomasi; tidak diklaim membuktikan kualitas hasil generatif.
