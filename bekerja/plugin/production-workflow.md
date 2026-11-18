# Alur penggunaan home-productions V2

Versi alur: 2.0

Diperbarui: 18 November 2026

Status: **alur V2 sudah diimplementasikan dan tersedia pada rilis privat 2.0.0 untuk uji manual**. Penerimaan gambar, batch, gerak dan video/audio menunggu hasil pengguna; keberhasilan teknis tidak menggantikan uji tersebut.

Acuan pembangunan: [rencana implementasi V2](implementation-plan.md). [Peta pengembangan dan rilis](README.md). Satu alur dan satu rencana aktif dipertahankan; versi sebelumnya tersedia melalui riwayat Git.

## 1. Tujuan dan sumber pengetahuan

Membantu pengguna dari brief dan konsep desain rumah sampai gambar referensi individual serta prompt Reference-to-Video (R2V) Omni Flash.

Repository tetap menjadi pustaka pengetahuan yang dibaca melalui URL web atau konektor GitHub. Skill/plugin menjalankan workflow. Tidak menyalin pustaka ke plugin, mengubah anotasi sumber atau menganalisis ulang seluruh video untuk perubahan V2.

DNA yang dipelajari mencakup bentuk, tata ruang, material, plafon, bukaan, furnitur, lighting, lingkungan, komposisi, cakupan/urutan area, pengungkapan ruang, gerak kamera dan ritme. Pilihan baru dibedakan dari fakta sumber; urutan edit tidak membuktikan denah. Confidence membatasi kepastian klaim sumber, bukan kebebasan memilih bahan desain baru. Tidak ada human_verified atau kewajiban review manual setiap referensi.

Pengguna mengkurasi referensi berdasarkan performa viral. Kesesuaian DNA menjadi sasaran produksi; performa viral setiap hasil baru tidak dijamin.

**Brief → referensi dan konsep → desain/shot disetujui → pengguna memilih mode gambar → seluruh prompt atau gambar individual → review gambar → prompt R2V per shot → paket proyek → generate dan revisi hasil.**

## 2. Shot, gambar dan cakupan

Shot adalah satu tampilan kamera kontinu tanpa cut. Adegan tidak menjadi unit penghitungan produksi.

Gambar V2 menetapkan identitas visual suatu area, bukan frame awal atau akhir wajib. Komposisi awal–akhir video tetap direncanakan dalam teks, tanpa mewajibkan generator menyalin piksel referensi pada kedua ujung klip. Tidak ada kolase atau crop panel dalam alur utama.

| Pola | Gambar individual | Video |
| --- | --- | --- |
| Area tersendiri | Satu gambar area tersebut | Satu continuous shot |
| Living-to-kitchen | Satu gambar living dan satu gambar kitchen | Satu continuous shot 6 detik dengan dua referensi R2V |
| Exterior-to-living | Satu gambar exterior dan satu gambar living | Satu continuous shot 6 detik dengan dua referensi R2V |

Kedua gambar pada shot penghubung menggambarkan area berbeda dalam rumah yang sama. Keduanya bukan alternatif desain, kolase atau dua shot.

Jenis/jumlah area serta pola gabungan mengikuti referensi terpilih. Bedroom yang ditampilkan maksimal satu; sleeping loft yang sudah mencakup fungsi tidur tidak diikuti bedroom lain. Tidak menambah ruang atau kamar dengan mengganti namanya.

Setelah living-to-kitchen, living dan kitchen sudah tercakup. Setelah exterior-to-living, exterior dan living sudah tercakup. Jangan menumpuk kedua pola tersebut sehingga living terungkap ulang. Area lama boleh terlihat sebagai background ketika mengungkap fungsi baru; itu bukan alasan membuat shot tambahan.

Laundry, wardrobe/closet, dining, sleeping loft atau bathroom–laundry hanya digunakan sesuai pola sumber. Untuk fungsi terpadu, kebutuhan gambar dipetakan secara eksplisit dalam rancangan; banyaknya label fungsi tidak otomatis menambah ruang fisik, gambar atau shot. Dua gambar pada living-to-kitchen dan exterior-to-living tetap wajib.

Baca ID anotasi bersama continuity, transition_out dan observation_note. Segmen tematik yang tersambung tanpa cut tidak otomatis menjadi shot produksi terpisah.

### Durasi dan audio

| Jenis shot | Durasi |
| --- | --- |
| Exterior | 6 detik |
| Exterior-to-living | 6 detik |
| Living-to-kitchen | 6 detik |
| Living, kitchen, bedroom, bathroom, laundry, wardrobe dan area lainnya | 4 detik |
| Fungsi terpadu lain, misalnya bathroom–laundry | 4 detik |

Jumlah gambar bukan penentu durasi. Total merupakan penjumlahan seluruh shot. Jangan menyamaratakan durasi, mempercepat atau memangkas otomatis untuk mengejar panjang video referensi.

Semua prompt/klip memakai ambient natural yang halus. Tanpa musik, soundtrack, beat, narasi, dialog atau efek dramatis. Musik sumber tidak diterapkan pada produksi. Cut antarklip dicatat di panduan perangkaian, terpisah dari gerak kontinu dalam klip.

## 3. Menetapkan satu rumah dan rancangan

Plugin membaca pengetahuan inti, tema, direktori dan sumber yang relevan secara selektif. Catat URL/ref/commit, referensi, shot/segmen, bukti yang benar-benar dibaca, serta adaptasi. Tidak membekukan jumlah referensi dalam instruksi plugin.

Tawarkan konsep bila pengguna masih memilih; pertahankan keputusan yang sudah diberikan. Rancangan terpilih menetapkan:

- Bentuk/massa, proporsi, atap, bukaan dan hubungan ruang.
- Plafon: bentuk, tingkat, sambungan antararea, balok bila ada, serta susunan lampu.
- Material, warna, tekstur, lantai dan furnitur utama.
- Lighting, lingkungan dan dunia di luar jendela.
- Elemen tetap yang harus konsisten antararea serta sepanjang video.

Rincian tersebut mengikuti desain yang disetujui, bukan alasan menambahkan ornamen atau geometri yang tidak dirancang. Hubungan baru dinyatakan sebagai keputusan proyek, bukan denah sumber yang telah terbukti.

Daftar shot mencatat cakupan, acuan, posisi/komposisi awal–akhir, lintasan, jenis gerak, hubungan simultan/sekuensial, perkiraan jarak/sudut, ritme, bukti visual gerak dan durasi. Perkiraan adalah rencana produksi, bukan ukuran fisik referensi yang sudah terverifikasi.

Rancangan juga memuat daftar gambar individual dan pemetaannya ke shot. Jumlah gambar, prompt gambar, shot, prompt video dan total durasi ditampilkan sebelum produksi gambar.

## 4. Dua mode gambar setelah rancangan disetujui

Pengguna memilih satu mode. Pilihan dapat diberikan bersama persetujuan desain; jangan meminta ulang jika sudah jelas.

| Mode | Keluaran |
| --- | --- |
| Prompt-to-image | Seluruh prompt gambar area; satu prompt untuk satu gambar individual |
| Generate image | Seluruh gambar area individual dibuat dalam satu tahap sesuai jumlah yang direncanakan |

Pada prompt-to-image, AI menyerahkan prompt gambar tanpa otomatis menjalankan generator. Gambar hasil generator yang dipilih pengguna kemudian dibawa kembali atau dibaca lewat akses yang benar-benar tersedia sebelum review visual dan prompt video final. Jangan mengklaim gambar sudah dihasilkan/dilihat hanya karena promptnya lengkap.

Pada generate image, bila rencana berisi tujuh gambar, AI diminta membuat **tujuh gambar individual sekaligus**, tanpa berhenti setelah satu gambar atau meminta perintah lanjutan per area. Generate satu per satu hanya bila diminta spesifik oleh pengguna. Jangan mengganti batch dengan satu kolase/contact sheet.

Pemenuhan batch dan proses yang benar-benar bersamaan diuji pada ChatGPT pengguna. Jangan menyatakan batas kemampuan dari keterbatasan alat pengembang. Jika alat menunjukkan batas nyata, laporkan apa yang berhasil/terhenti; jangan mengklaim batch lengkap, mengubah menjadi alur satu per satu, atau beralih ke API berbayar tanpa arahan pengguna.

Kedua mode memakai spesifikasi rumah dan kebutuhan area yang sama. Satu prompt memuat area tujuan, desain tetap, plafon, komposisi luas, lighting, lingkungan, naturalitas serta hal yang harus dipertahankan. Batch tidak berarti setiap gambar boleh mendesain rumahnya sendiri.

### Cakupan penuh dan naturalitas

Gambar harus memperlihatkan area secara luas dan informatif: hubungan furnitur, plafon, lantai serta bukaan yang diperlukan untuk merencanakan gerak. Full area tidak berarti seluruh sisi ruangan yang terhalang terlihat sekaligus.

Hindari close-up yang memotong informasi utama, fisheye berlebihan, dinding transparan, tampilan dollhouse dan perspektif mustahil. Rasio video tetap 9:16. Gambar R2V berfungsi sebagai referensi; rasio/komposisinya dipilih untuk memperlihatkan area secara wajar dan sesuai masukan yang diterima alat, tanpa memaksa crop 9:16 yang merusak informasi.

Hasil wajib mengikuti desain yang disetujui dan terlihat natural seperti fotografi arsitektur: skala, garis bangunan, tekstur, pencahayaan, bayangan dan pantulan masuk akal. Hindari tampilan plastik/CGI, HDR berlebihan atau perubahan struktur. Penilaian dilakukan pada hasil nyata, bukan hanya kata photorealistic dalam prompt.

## 5. Review paket gambar

Periksa setiap gambar dan seluruh gambar sebagai satu rumah, terutama plafon, bukaan, lantai, furnitur tetap, cahaya dan lingkungan. Untuk dua area yang tersambung, bukaan/batas ruang dan orientasinya harus saling sesuai.

Living dan kitchen tetap dua file individual, walaupun sebagian area lain terlihat sebagai konteks pada gambar masing-masing. Referensi diberi peran yang jelas; jangan menyerahkan dua file identik yang hanya diganti nama sebagai dua gambar area.

Revisi gambar yang menyimpang sebelum menyatakannya final. Pertahankan yang sudah benar. Perubahan elemen tetap memicu peninjauan area/shot terdampak serta revisi keputusan; jangan sekadar mengganti nomor versi aset lama.

AI dapat melakukan review dari piksel yang benar-benar dilihat; laporan pengguna dibedakan asalnya. Persetujuan paket visual mengikuti keputusan pengguna atau delegasi yang sudah berlaku. Tidak ada kewajiban persetujuan setiap gambar satu per satu.

File individual harus dapat dibuka dan diserahkan melalui unduhan. Simpan dimensi/format aktual, hash, peran area dan revisinya. Nama file atau tautan lama bukan pengganti file asli.

## 6. Prompt R2V sembilan bagian

Satu shot menghasilkan satu prompt dan satu klip. Prompt disusun setelah melihat gambar referensi final serta rancangan aktif.

| Bagian | Isi |
| --- | --- |
| OUTPUT SPECIFICATION | Durasi 6/4 detik, video 9:16, home tour dan identitas shot |
| REFERENCE IMAGE ROLE | Peran tiap gambar sebagai identitas area; bukan kewajiban first/last frame |
| ARCHITECTURE AND DESIGN | Material, furnitur, plafon, bukaan dan hubungan ruang yang dipertahankan |
| CAMERA START COMPOSITION | Posisi/arah kamera, subjek dan foreground/background |
| CAMERA MOVEMENT | Lintasan, perkiraan jarak/sudut, kecepatan dan simultan atau berurutan |
| VISIBLE MOTION EVIDENCE | Perubahan visual yang menunjukkan gerak benar-benar terjadi |
| ENDING COMPOSITION | Framing akhir yang masuk akal terhadap lintasan |
| VISUAL CONSISTENCY LOCK | Struktur dan objek tetap yang tidak boleh berubah |
| CONTINUITY AND AUDIO RULES | Satu shot kontinu, tanpa cut/morphing, ambient natural halus tanpa musik/narasi/dialog |

Untuk living-to-kitchen, gambar living dan kitchen menjadi dua acuan area terhubung pada satu rumah. Untuk exterior-to-living, gambar exterior dan living memiliki peran yang sama sesuai areanya. Jelaskan sambungan ruang; jangan meminta dissolve, perpindahan mendadak atau pergantian rumah.

### Gerak yang terlihat dan sesuai durasi

Gerak gabungan harus terlihat seluruh komponennya. Pan dan orbit yang memang dipilih dalam rancangan mempunyai target minimal **12 derajat**. Bedakan rotasi arah pandang saat pan dari perpindahan posisi mengitari subjek saat orbit; jangan menggantinya dengan memutar gambar/roll.

Jangan menambahkan pan/orbit pada setiap shot jika pola sumber dan rancangan hanya meminta gerak translasi. Maju sambil pan berarti bersamaan; maju lalu pan mempunyai fase berurutan.

Sesuaikan perkiraan jarak, sudut dan alokasi waktu terhadap 4 atau 6 detik. Jangan menulis slow sambil meminta lintasan panjang dan banyak fase dalam waktu pendek. Bila terlalu padat, kurangi jarak/kompleksitas dalam batas rancangan; perubahan keputusan yang material dikembalikan ke review desain.

Bukti gerak dipilih dari elemen yang memang ada: foreground membesar saat mendekat, perubahan perspektif yang wajar, sisi ruang yang terungkap atau kitchen yang terlihat bertahap. Pan tidak boleh dianggap telah terjadi hanya karena prompt mencantumkan angka sudut.

Sudut/jarak merupakan target instruksi. JSON dan teks prompt tidak membuktikan hasil video mematuhinya; keberhasilan dinilai dari media yang benar-benar terlihat.

## 7. Penyerahan, generate dan revisi

Paket prompt-to-image dapat diserahkan tanpa gambar pada tahap tersebut, dengan status yang jelas. Paket R2V final memerlukan gambar asli yang tersedia dan sudah direview.

Paket proyek memuat brief, konsep, desain tetap, sumber, shot/durasi, pilihan mode, prompt gambar, aset area, pemetaan gambar–shot, prompt R2V, petunjuk penggunaan dan keputusan/revisi. Pertahankan file individual; ZIP opsional tidak menggantikan tautan setiap gambar.

Pengguna memasang satu atau dua referensi sesuai peta shot pada mode R2V, lalu memakai prompt dan durasi shot tersebut. Jangan memasangnya sebagai kontrol first–last frame. Fungsi terpadu lain mengikuti pemetaan gambar yang sudah disetujui. Jangan menebak nama tombol, parameter API, batas input atau versi aplikasi.

Generate video, perangkaian klip dan publikasi Facebook tetap dijalankan pengguna. Setelah hasil tersedia, nilai desain, plafon, konsistensi, gerak, framing, ritme dan audio sesuai media yang dapat diakses. Pemeriksaan yang belum dilakukan tetap dinyatakan belum dilakukan.

Kelanjutan sesi membutuhkan catatan dan file asli yang masih dipakai. Pertahankan keputusan yang berlaku; minta hanya data yang hilang. Hasil produksi tidak otomatis mengubah pengetahuan sumber.

## 8. Keputusan pengguna dan contoh

Tiga titik keputusan tetap: pilihan konsep, persetujuan desain/shot, dan persetujuan paket gambar final. Pilihan mode gambar merupakan pilihan alur setelah desain, bukan persetujuan tambahan setiap area. Delegasi dan jawaban sebelumnya tetap berlaku.

| Susunan shot | Shot | Gambar individual | Prompt video | Total |
| --- | --- | --- | --- | --- |
| Exterior + living + kitchen + bedroom + bathroom | 5 | 5 | 5 | 22 detik |
| Exterior + living-to-kitchen + bedroom + bathroom | 4 | 5 | 4 | 20 detik |
| Exterior-to-living + kitchen + bedroom + bathroom | 4 | 5 | 4 | 18 detik |
| Exterior + living-to-kitchen + bedroom + laundry + bathroom | 5 | 6 | 5 | 24 detik |

Jumlah gambar pada contoh mengikuti area yang disebutkan, bukan dua kali jumlah shot. Area opsional tetap harus didukung sumber.

Contoh permintaan:

> Gunakan mode prompt-to-image. Berikan seluruh prompt individual untuk area dalam rancangan; satu prompt untuk satu gambar.

> Gunakan mode generate image. Buat seluruh tujuh gambar area individual sekaligus sesuai rancangan. Jangan membuat kolase atau berhenti meminta perintah setelah setiap gambar.

> Paket gambar ini sudah saya setujui. Susun prompt R2V sembilan bagian per shot, petakan referensinya dan sesuaikan gerak dengan durasi 6/4 detik.

## 9. Dasar perubahan

Pengguna melaporkan kolase awal–akhir sering tidak konsisten, terutama plafon, dan video interpolasi masih mengubah susunan. Percobaan R2V satu gambar dinilai lebih baik dan konsisten oleh pengguna. Itu menjadi dasar V2, bukan klaim bahwa semua video R2V selalu konsisten.

Batch tujuh gambar, R2V dua referensi pada dua jenis shot penghubung, serta keberhasilan gerak minimal 12 derajat tetap menjadi sasaran uji manual V2.

Rujukan: [pengetahuan inti](../../knowledge/ai-knowledge.md), [akses pustaka](../../knowledge/access-contract.md), [kontinuitas](../../knowledge/continuity-dna.md), [sinematografi](../../knowledge/cinematography-dna.md), [pola korpus](../../knowledge/corpus-patterns.md).

Revisi 2.0 mengganti kolase/crop dan interpolasi first–last dengan dua mode gambar individual serta R2V. Riwayat alur sebelumnya tersedia di Git.
