# Alur penggunaan home-productions 2.1.0

Diperbarui: 19 November 2026

**Status: source dan rilis privat 2.1.0 sudah diperbarui dan dibaca balik.** Tahap teknis 1–6 selesai; penerimaan gambar/batch/video menunggu uji manual pengguna. Ikuti [rencana dan hasil implementasi](implementation-plan.md) serta [README](README.md) untuk panduan uji. Versi sebelumnya tersedia di Git; tidak ada alur produksi kedua.

## 1. Tujuan dan batas

Mendukung proses kreatif dari brief, konsep rumah dan shot sampai gambar referensi individual serta prompt Reference-to-Video (R2V) Omni Flash.

Repo merupakan pustaka pengetahuan. Plugin membaca sumber secara selektif lewat URL GitHub atau konektor, tanpa menyalin pustaka ke plugin atau menganalisis ulang seluruh video. Produksi tidak mengubah anotasi sumber.

DNA meliputi desain, tata ruang, material, plafon, lampu, bukaan, furnitur, lingkungan, komposisi, cakupan/urutan area, pengungkapan ruang, gerak dan ritme. Bedakan fakta sumber dari adaptasi proyek. Confidence membatasi kepastian klaim, bukan penggunaan material dalam konsep kreatif. Tidak ada human_verified atau kewajiban review manual per referensi.

Referensi dikurasi pengguna dari video viral; kesesuaian DNA menjadi sasaran, tanpa jaminan hasil baru akan viral.

**Brief → sumber dan pilihan konsep → desain/shot disetujui → pilih mode gambar → seluruh prompt atau gambar individual → review visual → prompt R2V per shot → paket proyek → generate video dan revisi hasil.**

## 2. Memilih konsep dan merancang satu rumah

Pada proyek baru, lengkapi hanya informasi yang memengaruhi hasil. Pada kelanjutan, pertahankan pilihan, persetujuan dan delegasi yang sudah diberikan. Analisis sumber saja tidak otomatis memulai produksi penuh.

Baca pengetahuan dan anotasi yang relevan; catat sumber/shot, URL/ref/commit yang benar-benar diakses, bukti dan adaptasi. Jumlah referensi tidak dibekukan dalam instruksi.

Sesudah konsep dipilih, tetapkan satu rancangan rumah:
- Massa, atap, proporsi, material, bukaan dan hubungan area.
- Lantai, plafon serta sambungan antararea yang terhubung.
- Furnitur utama dan elemen tetap, termasuk satu lokasi kitchen.
- Armatur lampu nyata pada setiap interior, jenis/posisi sesuai fungsi dan desain.
- Lighting, lingkungan serta hal yang terlihat di luar bukaan.

Hubungan baru merupakan keputusan proyek, bukan denah sumber yang sudah terbukti. Jangan menambah balok, ornamen, ruang atau kamar yang tidak dirancang.

## 3. Merancang shot, gambar dan kamera bersama

Shot adalah satu pengambilan kamera kontinu tanpa cut. Shot menjadi unit produksi; jumlah gambar dapat berbeda dari jumlah shot atau label area.

| Pola | Referensi sasaran | Video |
| --- | --- | --- |
| Area tersendiri | Satu foto individual yang informatif | Satu continuous shot |
| Living-to-kitchen | **Satu foto utuh yang memperlihatkan living dan kitchen terhubung** | Satu continuous shot 6 detik |
| Exterior-to-living | **1 atau 2 referensi sesuai pilihan pengguna saat produksi**: satu gambar utama, atau gambar exterior dan living individual | Satu continuous shot 6 detik |

Gambar living–kitchen merupakan satu pandangan ruang yang koheren, bukan kolase, dua panel atau dua shot. **Kedua shot penghubung tidak mewajibkan dua referensi.** Living-to-kitchen memakai satu foto gabungan sebagai default. Untuk exterior-to-living, pengguna bebas memilih **1 atau 2 referensi**; keduanya sah dan dicatat pada rancangan. Jika dua, gambar exterior dan living harus menggambarkan rumah yang sama dengan hubungan spasial yang konsisten.

Untuk exterior-to-living, gambar utama tidak harus memperlihatkan seluruh interior bersamaan dengan exterior. Bila memakai exterior, seluruh rumah tetap masuk frame; interior yang belum terlihat mengikuti rancangan dan prompt. Jangan memakai dinding transparan, cutaway atau mengklaim foto sudah menunjukkan ruang tersembunyi. Kedua pola diuji sesuai geometrinya masing-masing.

Cakupan mengikuti sumber terpilih. Living-to-kitchen sudah mencakup living dan kitchen; jangan membuat shot kitchen lagi. Exterior-to-living sudah mencakup exterior dan living; jangan menambahkan living-to-kitchen yang mengulang living. Area sebelumnya boleh muncul sebagai background ketika mengungkap area baru.

Maksimal satu fungsi tidur: bedroom atau sleeping loft yang sudah mengungkap fungsi tidur. Tidak menambah bedroom lain melalui label utama/tamu. Laundry, wardrobe, dining, loft atau bathroom–laundry hanya bila didukung sumber dan rancangan. Label fungsi tidak otomatis berarti ruangan atau gambar tambahan.

Baca anotasi bersama continuity, transition_out dan observation_note. Pemisahan segmen tematik tanpa cut tidak otomatis berarti beberapa shot produksi.

### Durasi dan audio

| Shot | Durasi |
| --- | --- |
| Exterior, exterior-to-living, living-to-kitchen | 6 detik masing-masing |
| Living, kitchen, bedroom, bathroom, laundry, wardrobe dan area/fungsi terpadu lain yang disetujui | 4 detik masing-masing |

Total dijumlahkan dari shot. Jangan menyeragamkan semua klip 4 detik atau memangkas untuk mengejar durasi sumber.

Audio hanya ambient natural halus; tanpa musik, soundtrack, beat, narasi, dialog atau efek dramatis. Cut perangkaian hanya antarklip, bukan di dalam shot.

### Satu catatan tata ruang untuk gambar dan video

Dari rancangan yang sama, tentukan **posisi/arah kamera → komposisi gambar → lintasan → framing akhir**. Perkirakan tinggi, jarak, sudut dan fase sebagai rencana proyek; jangan menyebutnya pengukuran sumber.

Kitchen tetap satu pada lokasi yang sama. Bila di foto tampak di depan, jangan menuliskan seolah ada kitchen lain di kanan. Pan kanan masih mungkin sesuai, tetapi harus diperiksa terhadap posisi kamera, bidang pandang dan akhir lintasan. Jika tidak sesuai, ubah posisi kamera/komposisi gambar atau lintasan dalam batas DNA/desain, bukan memindahkan/menambah kitchen secara diam-diam.

Gambar R2V bukan frame awal/akhir wajib. Meski demikian, gambar harus mendukung lintasan yang masuk akal. Larangan duplicate kitchen tidak menggantikan rancangan geometri yang sesuai.

Pilih gerak per area dari DNA sumber yang relevan: maju/mundur, lateral, pan, orbit atau tilt bila sesuai. Tidak ada default dolly + pan untuk semua ruang. Gerak tunggal tetap sah. Gerak gabungan terpilih harus terbaca seluruh komponennya; bedakan maju sambil pan dan maju lalu pan.

Pan/orbit terpilih minimal 12°. Pan mengubah arah pandang; orbit mengubah posisi mengitari subjek. Jangan menggantinya dengan roll atau memaksa rotasi pada gerak translasi.

Sesuaikan jarak, sudut, kecepatan dan fase dengan 4/6 detik. Jangan menulis slow sambil meminta jarak panjang, sudut besar dan banyak fase. Tetapkan bukti visual dari elemen nyata: perubahan perspektif, foreground, sisi ruang yang terungkap dan hubungan area yang tetap.

## 4. Menyetujui rancangan dan memilih mode gambar

Sebelum generate, tampilkan desain, daftar shot, acuan, cakupan, durasi, komposisi/lintasan serta daftar gambar. Untuk exterior-to-living, gunakan pilihan pengguna 1 atau 2 referensi; tanyakan hanya bila pilihan belum jelas dan diperlukan untuk menetapkan daftar gambar. Jangan meminta ulang jika sudah dipilih. Tunjukkan jumlah gambar, prompt gambar, shot, prompt video dan total durasi sesuai pilihan.

Sesudah rancangan disetujui, gunakan pilihan mode yang sudah diberikan atau minta pilihan:
- **Prompt-to-image:** seluruh prompt individual, satu prompt untuk satu gambar; tidak otomatis generate atau mengaku file tersedia.
- **Generate image:** seluruh gambar individual sesuai rencana dibuat sekaligus dalam satu tahap/permintaan; bukan kolase.

Jika rencana memerlukan tujuh gambar, permintaan adalah tujuh sekaligus, tanpa berhenti meminta perintah setelah setiap gambar. Satu per satu hanya jika diminta spesifik. Jangan menyimpulkan paralel hanya dari tujuh file; catat pelaksanaan aktual. Bila alat menunjukkan batas nyata, laporkan hasil parsial tanpa diam-diam mengubah alur atau memindahkan ke API.

Pada prompt-to-image, hasil generator pilihan pengguna harus benar-benar tersedia/dapat dibuka sebelum review gambar dan paket R2V final. Dua mode memakai rancangan yang sama.

### Aturan gambar dan komposisi

Setiap prompt menyatakan posisi/arah/tinggi kamera, sudut terhadap subjek, penempatan subjek, foreground/background, kedalaman, batas yang harus terlihat serta elemen tetap. Informasi harus konkret, bukan hanya wide/full overview.

| Gambar | Ketentuan |
| --- | --- |
| Exterior | Seluruh massa rumah yang terlihat masuk frame: atap, batas kiri/kanan dan dasar, dengan ruang aman di tepi. Sudut frontal, three-quarter atau lainnya sesuai desain/sumber |
| Living–kitchen | Satu foto menunjukkan kedua area dan sambungan nyata; satu kitchen pada lokasi rancangan, orientasinya sesuai lintasan |
| Bedroom | Front three-quarter; sasaran sudut horizontal 35–45° terhadap sumbu panjang bed; bed memanjang diagonal dalam frame, menghindari tampilan frontal terpusat dan simetris |
| Setiap interior | Cakupan informatif memperlihatkan hubungan lantai, plafon, furnitur dan bukaan penting; armatur lampu terbaca dan sesuai desain |

Sudut bedroom adalah pilihan pengguna. Pilih sisi kiri/kanan yang cocok dengan rancangan; jangan memutar bed, memiringkan gambar atau mengklaim semua sumber memakai sudut tersebut. Rentang 35–45° adalah rencana arah pandang di bidang horizontal, bukan kemiringan garis bed pada piksel.

Lampu tidak harus semuanya menyala; pada siang hari armatur dapat mati. Bentuk plafon, posisi lampu dan elemen tetap tidak berubah antarview.

Full exterior adalah aturan gambar; video boleh mendekat sesuai lintasan. Full interior bukan tuntutan melihat semua sisi yang terhalang. Hindari close-up yang membuang konteks, fisheye berlebihan, cutaway, dinding transparan atau perspektif mustahil.

Gambar wajib natural seperti fotografi arsitektur, dengan skala, perspektif, tekstur, cahaya, bayangan dan pantulan wajar. Hindari tampilan plastik/CGI dan HDR berlebihan. Video tetap 9:16; rasio gambar referensi dipilih agar cakupan wajar dan sesuai masukan alat, tanpa crop paksa yang merusak informasi.

## 5. Review gambar sebagai satu rumah

Periksa piksel yang benar-benar tersedia: kesesuaian desain, naturalitas, cakupan, plafon/lampu, bukaan, furnitur, material dan hubungan ruang. Khusus bedroom periksa arah pandang serta bed diagonal; exterior periksa seluruh batas rumah; living–kitchen periksa kitchen tunggal dan geometri lintasan.

Bedakan review AI dari laporan pengguna. Jangan menandai gambar tersedia/direview hanya dari nama file atau promptnya.

Revisi bagian yang menyimpang dan tinjau dampak perubahan elemen tetap pada gambar/shot lain. Pertahankan yang sudah benar. Persetujuan visual mengikuti pengguna atau delegasi yang berlaku; tidak dipaksakan per gambar.

File individual harus dapat dibuka dan diunduh. Catat format, dimensi/hash aktual serta revisi. Paket final tidak dapat dinyatakan lengkap tanpa file asli yang masih dipakai.

## 6. Prompt Omni Flash siap salin

Satu shot menghasilkan satu prompt dan satu klip. Susun prompt dari rancangan aktif dan gambar final yang benar-benar dilihat.

| Bagian | Isi |
| --- | --- |
| OUTPUT SPECIFICATION | Durasi baku 4/6 detik, video 9:16 dan jenis tampilan home tour |
| REFERENCE IMAGE ROLE | Gambar terlampir adalah identitas visual/spasial, **bukan frame awal maupun frame akhir wajib**; tanpa nama file, path atau ID internal |
| ARCHITECTURE AND DESIGN | Struktur, material, furnitur, plafon/lampu, bukaan dan hubungan ruang yang dipertahankan |
| CAMERA START COMPOSITION | Posisi/arah kamera, subjek dan foreground/background yang sesuai tata ruang |
| CAMERA MOVEMENT | Gerak pilihan per area, lintasan, perkiraan jarak/sudut, ritme dan hubungan simultan/sekuensial |
| VISIBLE MOTION EVIDENCE | Perubahan visual yang membuktikan setiap gerak terpilih terjadi |
| ENDING COMPOSITION | Framing akhir yang sesuai posisi, lintasan dan geometri |
| VISUAL CONSISTENCY LOCK | Elemen tetap dan posisi objek yang tidak boleh berubah/berlipat, termasuk kitchen |
| CONTINUITY AND AUDIO RULES | Satu shot kontinu tanpa cut/morphing; ambient natural halus tanpa musik/narasi/dialog/efek dramatis |

Teks memakai sebutan seperti “the attached reference image” dan deskripsi visual bila perlu, bukan nama berkas. ID dan nama file tetap ada pada peta lampiran di luar badan prompt. Tidak meminta generator menyalin gambar sebagai frame pembuka/penutup atau melakukan interpolasi first–last.

Di chat, setiap shot mempunyai **satu fenced code block berisi hanya prompt final lengkap sembilan bagian**. Judul, durasi ringkas, petunjuk lampiran dan catatan berada di luar block. Tidak memasukkan placeholder, JSON atau instruksi untuk membersihkan teks. File .txt hasil ekspor memuat teks prompt yang sama tanpa pagar Markdown.

Gerak, sudut dan audio yang tertulis adalah target, bukan bukti hasil sudah sesuai. Penilaian video dilakukan setelah hasil tersedia.

## 7. Checkpoint dan penyerahan

Catatan proyek menjaga keputusan, sumber, revisi dan pemetaan gambar–shot–prompt agar dapat dilanjutkan. Penyimpanan dilakukan sebagai checkpoint internal pada keputusan/revisi penting serta penyerahan; bukan syarat setiap balasan dan bukan penambahan file otomatis ke repo GitHub.

Jika project.json gagal ditulis, pertahankan data sesi dan lanjutkan konsep. Coba nama revisi baru bila folder dapat ditulis, atau folder proyek yang terbukti dapat ditulis. Jangan menghapus file pengguna, mengubah izin/ownership atau meminta pengguna mengurus filesystem sebagai alur rutin.

Klaim tersimpan hanya setelah penulisan dan baca balik berhasil. Jika pindah folder, bawa aset yang tersedia dan perbaiki peta relatif. Jika seluruh penyimpanan gagal, berikan status/catatan teks yang jujur; jangan mengarang tautan unduhan. Paket final tetap memerlukan file asli.

Penyerahan:
- **Paket prompt gambar:** prompt lengkap sesuai rencana; sah tanpa aset pada tahap ini, belum disebut siap R2V final.
- **Paket R2V final:** gambar asli yang direview, prompt per shot, peta lampiran, durasi, panduan, sumber dan catatan keputusan/revisi.

ZIP opsional tidak menggantikan unduhan gambar individual. Pengguna melampirkan referensi sesuai peta pada mode R2V, bukan kontrol first–last. Jangan menebak tombol, versi aplikasi atau parameter API.

Kelanjutan sesi mempertahankan mode, sumber, keputusan dan delegasi yang berlaku. Data schema 2.0 dipakai melalui konversi pada salinan/revisi, tanpa otomatis mengklaim gambar/review lama sesuai ketentuan baru.

## 8. Generate video, evaluasi dan keputusan

Pengguna generate video di Omni Flash, merangkai klip dan mempublikasikan hasil. Setelah media tersedia, nilai geometri, struktur, desain, framing, gerak, ritme serta audio sesuai akses yang nyata. Perbaiki bagian terdampak; pemeriksaan yang belum dilakukan tetap dicatat belum diuji.

Tiga titik keputusan tetap: konsep, desain/shot dan paket visual. Pilihan mode tidak menjadi persetujuan tambahan setiap gambar. Delegasi pengguna tetap berlaku.

| Susunan shot | Shot | Gambar utama | Prompt video | Total |
| --- | --- | --- | --- | --- |
| Exterior + living + kitchen + bedroom + bathroom | 5 | 5 | 5 | 22 detik |
| Exterior + living-to-kitchen + bedroom + bathroom | 4 | 4 | 4 | 20 detik |
| Exterior-to-living + kitchen + bedroom + bathroom | 4 | 4 atau 5, sesuai pilihan 1/2 referensi penghubung | 4 | 18 detik |
| Exterior + living-to-kitchen + bedroom + laundry + bathroom | 5 | 5 | 5 | 24 detik |

Area opsional tetap harus didukung sumber; tujuh gambar bukan jumlah wajib. Living-to-kitchen memakai satu gambar gabungan sebagai default; exterior-to-living mengikuti pilihan pengguna 1 atau 2 referensi. Konsistensi video masing-masing tetap dinilai dari uji nyata.

Dasar perbaikan: laporan pengguna mengenai dua referensi living–kitchen yang kurang konsisten, konflik gambar dengan lintasan, bedroom frontal dan kegagalan penyimpanan; ditambah ketentuan exterior utuh, plafon/lampu, peran referensi, variasi kamera dan format salin.

Rujukan pengetahuan: [inti](../../knowledge/ai-knowledge.md), [akses](../../knowledge/access-contract.md), [kontinuitas](../../knowledge/continuity-dna.md), [sinematografi](../../knowledge/cinematography-dna.md), [pola korpus](../../knowledge/corpus-patterns.md). Perubahan preferensi plugin tidak mengubah fakta pada pustaka tersebut.
