# Rencana implementasi perbaikan home-productions 2.1.0

Diperbarui: 19 November 2026

**Status: tahap 1–6 selesai; source dan rilis privat 2.1.0 sudah diverifikasi.** Schema proyek 2.1 dan rules 2.1.0 aktif. Tahap 7: panduan uji manual siap, penerimaan gambar/batch/video menunggu pengguna. Nomor tahap di sini adalah tahap perbaikan baru, terpisah dari implementasi V2 sebelumnya.

Dokumen ini menggantikan rencana aktif sebelumnya. [Alur sasaran](production-workflow.md) menjelaskan pengalaman pengguna sesudah perbaikan; [README](README.md) membedakan rencana, source dan rilis. Riwayat implementasi sebelumnya tersedia di Git.

## 1. Tujuan dan batas pekerjaan

Memperbaiki produksi dari konsep desain hingga gambar referensi dan prompt Reference-to-Video (R2V) Omni Flash berdasarkan hasil uji manual pengguna. Keseluruhan DNA sumber tetap dipakai: desain, hubungan ruang, plafon, pencahayaan, komposisi, pengungkapan area, urutan, gerak dan ritme.

Seluruh perubahan pengembangan berada di bekerja/plugin/. Pustaka knowledge/, references/, video/ dan requests/ tidak diubah atau disalin ke plugin. Sumber dibaca selektif melalui URL GitHub atau konektor; tidak perlu analisis ulang seluruh video. Ketidakpastian sumber membatasi klaim fakta, bukan pilihan kreatif proyek.

Pertahankan satu plugin home-productions dan satu skill produce-home-tour. Generate video, merangkai klip dan publikasi tetap dilakukan pengguna. Tidak menambah server, API produksi, database, UI khusus, mode video baru atau salinan plan/folder versi lain.

## 2. Temuan dan keputusan yang menjadi dasar

| ID | Masalah atau kebutuhan | Perbaikan yang disepakati |
| --- | --- | --- |
| P01 | Dua gambar living dan kitchen memberi hasil kurang konsisten dibanding satu gambar; pengguna juga menghapus kewajiban dua referensi exterior-to-living | Living-to-kitchen memakai **satu foto utuh living dan kitchen terhubung sebagai default**. Exterior-to-living memakai **1 atau 2 referensi sesuai pilihan pengguna saat produksi**, tanpa kewajiban salah satu jumlah. Masing-masing tetap satu shot 6 detik |
| P02 | Kitchen di depan pada gambar, tetapi lintasan meminta pengungkapan kitchen di kanan; hasil dapat menggandakan kitchen | Satu catatan tata ruang dan elemen tetap mengikat posisi kamera, komposisi gambar, lintasan dan framing akhir; kitchen tetap satu pada tempat yang sama |
| P03 | Bedroom terlalu frontal, bed terpusat dan simetris | Preferensi produksi pengguna: **front three-quarter**, arah pandang horizontal **35–45° terhadap sumbu panjang bed**, bed tampak memanjang diagonal |
| P04 | Prompt gambar hanya memakai arahan overview umum | Komposisi setiap gambar dinyatakan eksplisit dan terkait lintasan video; bukan sekadar kata wide atau full |
| P05 | Gerak tidak terlihat atau terlalu padat untuk 4/6 detik | Review komposisi, geometri, bukti gerak dan ritme; angka dalam data tidak dianggap bukti hasil video |
| P06 | PermissionError saat menyimpan project.json menghentikan proses | Penyimpanan menjadi checkpoint internal yang dapat pulih; konsep tetap dilanjutkan dari data sesi, tanpa klaim file berhasil tersimpan |
| P07 | Sisi rumah terpotong pada gambar exterior | Gambar memuat seluruh massa rumah yang terlihat: atap, batas kiri/kanan dan dasar, dengan ruang aman di tepi; sudut kamera fleksibel |
| P08 | Interior kadang tidak mempunyai lampu | Setiap area interior mempunyai armatur lampu nyata dan masuk akal sesuai desain; plafon serta posisi lampu ditetapkan dan konsisten |
| P09 | Peran gambar dan penyebutan nama file membingungkan prompt R2V | Tegaskan referensi identitas visual/spasial, **bukan frame awal maupun akhir wajib**; nama file, path dan ID gambar berada di metadata/panduan, di luar teks prompt |
| P10 | Gerak terlalu sering dolly + pan | Pilih gerak per area dari sumber yang relevan: translasi, pan, orbit atau tilt sesuai kebutuhan; gerak tunggal tetap sah |
| P11 | Prompt akhir harus mudah disalin | Setiap prompt video lengkap berada dalam satu fenced code block tersendiri; hanya isi prompt di dalamnya, penjelasan di luar |

Laporan pengguna merupakan bukti temuan pada percobaan tersebut, bukan jaminan bahwa semua R2V satu gambar akan selalu konsisten.

### Referensi untuk kedua shot penghubung

Pengguna menghapus kewajiban dua referensi pada **living-to-kitchen dan exterior-to-living**. Living-to-kitchen memakai satu foto gabungan sebagai default; tambahan referensi hanya atas permintaan pengguna.

**Exterior-to-living fleksibel: pengguna memilih 1 atau 2 referensi saat produksi.** Dengan satu referensi, pakai satu gambar utama yang sesuai lintasan. Dengan dua referensi, pakai gambar exterior dan living individual dari rumah yang sama, dengan hubungan spasial yang diperiksa. Jangan mengunci jumlah menjadi satu, mewajibkan dua, atau otomatis mengganti pilihan pengguna. Pilihan ini dicatat pada rancangan/peta lampiran, bukan menjadi mode produksi baru.

Living-to-kitchen memerlukan satu foto koheren kedua area. Pada exterior-to-living, pilih gambar utama yang mendukung lintasan, umumnya exterior dengan pintu masuk yang jelas. Jika memakai gambar exterior, ketentuan seluruh rumah terlihat tetap berlaku. Interior tidak wajib terlihat penuh pada gambar yang sama; jangan membuat dinding transparan, cutaway atau perspektif mustahil. Bagian interior yang belum terlihat ditetapkan pada rancangan dan prompt, bukan diklaim sudah dibuktikan oleh foto.

Kedua pola tetap diuji sesuai geometrinya masing-masing. Menghapus syarat dua referensi merupakan keputusan pengguna; itu bukan bukti bahwa semua hasil video satu referensi sudah konsisten.

### Membedakan sumber dan keputusan proyek

Anotasi tersimpan [edh058/shot-04](../../references/edh058/analysis.yaml) mendukung keluarga pandangan bedroom front three-quarter. Sebaliknya, [edh056/shot-04](../../references/edh056/analysis.yaml) tercatat hampir frontal. Karena itu, angka 35–45° dan bed diagonal merupakan preferensi produksi pengguna, bukan ukuran semua referensi. Pilih acuan bedroom yang kompatibel dan catat adaptasinya; jangan mengubah anotasi sumber agar tampak mendukung keputusan baru.

Pan ke kanan saat kitchen tampak di depan tidak otomatis salah. Kesesuaiannya bergantung pada posisi/arah kamera, sudut pandang, jalur dan akhir yang dituju. Perbaikan harus menyelesaikan hubungan tersebut, bukan sekadar menambahkan larangan duplicate kitchen.

## 3. Aturan produksi yang dipertahankan

| Aspek | Ketentuan |
| --- | --- |
| Unit produksi | Satu shot = satu rekaman kontinu tanpa cut; bukan penghitungan adegan |
| Durasi | Exterior, exterior-to-living dan living-to-kitchen 6 detik; area lain/fungsi terpadu yang disetujui 4 detik |
| Cakupan | Area yang sudah diungkap tidak diulang pada shot berikutnya; kemunculan sebagai background bukan pengungkapan baru |
| Bedroom | Maksimal satu fungsi tidur, termasuk sleeping loft; tidak menambah kamar lain dengan nama berbeda |
| Area opsional | Laundry, wardrobe/dining/loft atau fungsi terpadu hanya sesuai sumber dan rancangan |
| Gambar | Individual, natural dan sesuai desain; tanpa kolase, crop panel atau pasangan first/last wajib |
| Mode gambar | prompt_to_image atau generate_image, dipilih setelah rancangan disetujui atau mengikuti pilihan yang sudah ada |
| Batch | Seluruh jumlah gambar yang disetujui dikerjakan sekaligus dalam satu tahap/permintaan; satu per satu hanya atas permintaan pengguna |
| Kamera | DNA per area, gerak gabungan terlihat jika dipilih; simultan berbeda dari sekuensial |
| Rotasi | Pan/orbit yang dipilih minimal 12°; tidak memaksa rotasi pada shot translasi atau menyamakan pan dengan orbit/roll |
| Audio | Ambient natural halus saja; tanpa musik, narasi, dialog atau efek dramatis |
| Keputusan | Pilihan konsep, persetujuan desain/shot, persetujuan paket visual; delegasi berlaku tanpa persetujuan per gambar yang dipaksakan |

Jumlah gambar mengikuti kebutuhan pandangan referensi, bukan jumlah label area. Satu gambar gabungan living–kitchen adalah satu foto dari satu sudut kamera yang memperlihatkan ruang terhubung secara wajar. Bukan stitching dua gambar, dinding transparan atau sudut pandang mustahil. Gambar tidak harus menjadi titik awal/akhir video, tetapi harus mendukung lintasan yang direncanakan.

Full exterior berlaku pada **gambar acuan**, bukan kewajiban mempertahankan seluruh rumah dalam setiap frame video. Pada interior, full berarti cakupan ruang yang informatif, bukan melihat semua sisi yang terhalang. Lampu wajib ada dan terbaca; tidak semua lampu harus menyala ketika adegan memakai cahaya siang.

## 4. Kontrak data sasaran dan kompatibilitas

Target: paket/rules **2.1.0**, schema proyek **2.1**. Perbarui schema, template, rules, validator, skill dan exporter bersama agar tidak ada aturan lama yang menolak alur baru.

| Bagian | Perubahan sasaran |
| --- | --- |
| design | Catatan tata ruang bersama, hubungan area, elemen tetap, plafon dan armatur/posisi lampu; cukup untuk mengikat pandangan dan lintasan, bukan sistem denah 3D baru |
| image_plan | Satu entri per gambar/pandangan; area_ids mencatat area yang benar-benar terlihat. Lepas kewajiban file terpisah per primary_area untuk **kedua** shot penghubung. Satu referensi utama dapat mendukung shot yang cakupan videonya lebih luas daripada area yang terlihat di foto |
| Komposisi gambar | Posisi/arah/tinggi kamera yang direncanakan, sudut terhadap subjek, penempatan subjek, foreground/background, batas yang harus terlihat, elemen tetap serta hubungan dengan lintasan shot |
| Bedroom | Preferensi sudut 35–45° di bidang horizontal terhadap sumbu panjang bed; penempatan diagonal di frame. Nilai rencana bukan pengukuran otomatis dari piksel |
| shots dan camera | Peta gambar, cakupan dan gerak memakai tata ruang yang sama; awal → lintasan → akhir saling sesuai, ritme mengikuti durasi baku. Bedakan area terlihat pada gambar dan area yang akan diungkap video; area tersembunyi tidak diberi status sudah terlihat |
| assets dan review | Pertahankan file asli, revisi, dimensi/format/hash dan asal review; catat aspek visual yang benar-benar diperiksa, tanpa human_verified global |
| prompt.sections | Tetap sembilan bagian sebagai sumber tunggal; tidak mewajibkan image_id di REFERENCE IMAGE ROLE |
| reference_image_ids | Tetap tersedia di data dan peta lampiran; exterior-to-living menerima 1 atau 2 ID sesuai pilihan pengguna. Jumlah gambar, prompt gambar dan aset mengikuti pilihan tersebut, tanpa bocor ke badan prompt video |
| Checkpoint | Lokasi aktif dan hasil penyimpanan dilaporkan sesuai kenyataan; keputusan sesi tidak hilang karena gagal menulis file |

Gunakan nama field yang ringkas pada implementasi dan dokumentasikan sekali di project-contract.md. Hindari salinan struktur yang menyatakan tata ruang berbeda dalam prompt gambar dan prompt video.

Proyek schema 2.0 harus dikenali dan dapat dilanjutkan melalui konversi eksplisit pada salinan/revisi. Pertahankan brief, sumber, konsep, mode, delegasi dan keputusan yang masih berlaku. Jangan menggabungkan dua gambar lama menjadi foto baru secara otomatis atau menandai preferensi/ulasan baru sudah terpenuhi. Tinjau ulang hanya gambar dan shot terdampak. Proyek V1 tetap dikenali sebagai alur lama; tidak otomatis diklaim cocok untuk R2V.

## 5. Tujuh tahap implementasi berurutan

Tahap 1–6 di bawah sudah diimplementasikan dan diperiksa. Tahap 7 baru sampai serah-terima panduan; hasil uji manual rilis baru belum tersedia. Rincian bukti dan batas pemeriksaan ada pada bagian 10.

### Tahap 1 — Kontrak gambar, tata ruang dan aturan

**Pekerjaan**
- Selaraskan rules, schema, template proyek dan project-contract dengan kebutuhan P01–P11.
- Implementasikan satu foto gabungan sebagai default living-to-kitchen. Untuk exterior-to-living, terima **1 maupun 2 referensi sesuai pilihan pengguna**, tanpa mengunci salah satunya; satu gambar tidak wajib memperlihatkan seluruh interior.
- Tetapkan data komposisi, elemen ruang tetap, preferensi bedroom dan lampu interior.
- Hapus validasi yang mewajibkan ID gambar dalam REFERENCE IMAGE ROLE; pertahankan kecocokan ID/revisi pada metadata.
- Ganti asumsi validator bahwa gabungan area terlihat pada semua gambar harus selalu sama persis dengan cakupan video. Untuk exterior-to-living, area yang baru terungkap boleh belum terlihat pada referensi, tetapi wajib punya hubungan/elemen tetap dalam rancangan.
- Sediakan jalur konversi schema 2.0 yang tidak memalsukan review atau mengganti aset lama.

**Keluaran:** kontrak dan validator yang menerima model referensi baru.
**Selesai bila:** satu foto living–kitchen sah dan kedua pilihan 1/2 referensi exterior-to-living diterima sesuai rancangan, cakupan/tautan salah tetap ditolak, proyek perencanaan sah tanpa gambar, ketentuan durasi/audio/bedroom dan pemisahan metadata tetap terjaga. Nilai geometri diperiksa sebagai data rencana; validator tidak mengklaim menilai piksel.

### Tahap 2 — Checkpoint tahan gagal dan kelanjutan sesi

**Pekerjaan**
- Tambahkan helper penyimpanan kecil, misalnya scripts/save_project.py, untuk menyelesaikan kegagalan nyata; tidak menambah dependensi/layanan.
- Validasi data sesuai tahap dari memori sebelum menyimpan; lakukan percobaan menulis file sementara, bukan hanya os.access.
- Bila file lama tidak dapat ditimpa tetapi folder masih dapat ditulis, gunakan nama revisi baru. Bila folder tidak dapat ditulis, pilih/buat folder proyek yang benar-benar berhasil diuji.
- Gunakan penulisan aman, baca balik dan validasi sebelum mengaku tersimpan; pertahankan checkpoint terakhir yang baik.
- Jika pindah folder, bawa aset terdaftar yang dapat dibaca dan pertahankan/perbarui path relatif secara konsisten. Aset yang tidak dapat disalin tetap dilaporkan kurang.
- Bila penyimpanan gagal seluruhnya, lanjutkan pembahasan konsep dari data sesi dan berikan catatan teks untuk melanjutkan, tanpa tautan file palsu atau persetujuan yang direset.

**Keluaran:** satu checkpoint aktif yang dapat ditemukan setelah berhasil disimpan, dengan status kegagalan yang tidak memblokir diskusi.
**Selesai bila:** simulasi file/folder tak dapat ditulis dan gagal baca balik tidak merusak data terakhir atau kehilangan keputusan. Tidak menghapus file pengguna, mengubah ownership/chmod atau mengklaim paket final tanpa file asli.

Checkpoint dipakai pada keputusan/revisi penting dan penyerahan, bukan kewajiban menulis disk setiap balasan. File proyek berada di ruang kerja produksi ChatGPT atau paket unduhan, bukan otomatis ditambahkan ke repo pengetahuan. Penyebab persis PermissionError yang dilaporkan belum terbukti dari traceback saja.

### Tahap 3 — Praproduksi dan gambar yang sesuai lintasan

**Pekerjaan**
- Perbarui SKILL.md, preproduction.md, image-workflow.md dan image-prompt-template.md; pertahankan satu entrypoint dengan panduan rinci bersyarat.
- Tetapkan tata ruang dan posisi/arah kamera, lalu turunkan komposisi gambar serta lintasan dari keputusan yang sama.
- Buat satu gambar living–kitchen yang menunjukkan kedua area dan sambungannya. Kitchen tetap satu; jangan memindahkannya untuk menuruti teks pan.
- Untuk exterior-to-living, ikuti pilihan pengguna: satu gambar utama atau dua gambar exterior/living yang konsisten. Sesuaikan daftar gambar dan sambungan pintu masuk/living; jangan menambah gambar kedua secara wajib atau memaksa pengguna memakai satu saja.
- Terapkan bedroom front three-quarter 35–45° dan bed memanjang diagonal, tanpa memutar bed atau memberi efek roll demi meniru sudut.
- Exterior memuat seluruh rumah dengan tepi aman; sudut frontal, three-quarter atau lainnya dipilih sesuai desain/sumber, tanpa sudut wajib universal.
- Setiap interior memperlihatkan plafon dan lampu yang masuk akal sesuai fungsi/desain; lampu dan plafon tetap konsisten antarview.
- Kedua mode memakai rancangan yang sama. Hitung seluruh prompt/file sesuai image_plan baru; jangan diam-diam mengurangi batch atau menggantinya dengan kolase.
- Review hasil nyata sebelum image_final: naturalitas, proporsi, cakupan, elemen tetap, orientasi dan dukungan terhadap gerak.

**Keluaran:** seluruh prompt gambar atau gambar individual yang sesuai mode dan rancangan.
**Selesai secara teknis bila:** pemetaan/jumlah/revisi benar dan instruksi komposisi lengkap. Kualitas visual dan eksekusi batch nyata tetap dinilai pada tahap 7, bukan dibuktikan dari prompt.

### Tahap 4 — Prompt R2V, variasi gerak dan format salin

**Pekerjaan**
- Perbarui omni-flash.md dan prompt-template.md dengan sembilan bagian yang tetap sama.
- REFERENCE IMAGE ROLE menyatakan referensi identitas visual/spasial, bukan frame awal/akhir wajib; tanpa nama file, path atau ID internal di badan prompt.
- Pilih gerak dari sumber yang sesuai per area. Dolly maju/mundur, gerak lateral, pan, orbit atau tilt dipakai bila relevan; tidak mewajibkan dolly + pan.
- Cocokkan kamera awal, lintasan, geometri dan akhir dengan gambar yang benar-benar tersedia. Jika tidak cocok, revisi gambar atau lintasan yang sesuai DNA/desain; perubahan material kembali ke keputusan desain.
- Pastikan semua komponen gerak gabungan tampak; jelaskan simultan/sekuensial dan bukti visualnya. Pan/orbit terpilih minimal 12°.
- Sesuaikan jarak, sudut, jumlah fase dan kecepatan dengan 4/6 detik. Jangan memakai slow sebagai kata baku yang bertentangan dengan tugas gerak.
- Tampilkan **satu prompt lengkap dalam satu fenced code block per shot**. Judul shot, catatan dan peta lampiran berada di luar block; tidak ada placeholder atau JSON dalam teks siap salin.

**Keluaran:** prompt yang dapat langsung dipakai pada R2V.
**Selesai bila:** kesembilan bagian lengkap, peran gambar tegas, tidak ada ID/nama file di badan prompt, dan rancangan gerak tidak bertentangan dengan gambar. Keberhasilan gerak, kontinuitas dan audio hasil tetap menunggu video nyata.

### Tahap 5 — Ekspor, konversi dan kelanjutan proyek

**Pekerjaan**
- Selaraskan build_production_package.py dengan model gambar multi-area, checkpoint dan versi baru.
- Pertahankan dua jenis penyerahan: image_prompt_package sah tanpa aset; prompt_package memerlukan file referensi aktual yang direview dan prompt final.
- Letakkan ID/nama file dan peta lampiran pada project.json/production-guide.md, terpisah dari isi prompt.
- Simpan video-prompts/*.txt sebagai teks mentah sembilan bagian, tanpa pagar Markdown; pagar code block hanya format penyerahan di chat.
- Jalankan konversi pada salinan proyek lama dan tandai kebutuhan baru yang belum dipenuhi; jangan menimpa proyek sumber atau menaikkan status review otomatis.
- Pastikan paket dapat dibuka di folder/sesi baru, dengan gambar asli, peta shot, keputusan, mode dan delegasi yang masih berlaku.

**Keluaran:** paket yang konsisten dan dapat dilanjutkan.
**Selesai bila:** contoh 20 detik memakai empat gambar/prompt gambar dan empat prompt video; contoh 18 detik memakai empat atau lima gambar sesuai pilihan 1/2 referensi exterior-to-living; isi .txt sama dengan isi code block chat; ekspor/migrasi tidak merusak keputusan atau aset lama.

### Tahap 6 — Pemeriksaan teknis dan rilis privat

**Pekerjaan**
- Jalankan tes bermakna untuk kontrak multi-area, migrasi, checkpoint gagal, ekspor, aturan cakupan/durasi/kamera/audio dan arsip.
- Periksa format skill/manifest/metadata, tautan, struktur ZIP dan semua pemanggil aturan lama. Jangan menambah tes yang sekadar mencari kalimat instruksi.
- Selaraskan versi manifest 2.1.0, schema 2.1 dan rules 2.1.0. Pertahankan nama/plugin ID, publisher akun, nilai defaultPrompt, scope USER dan audience PRIVATE.
- Kemas hanya source plugin; docs pengembangan, tests, dist dan runs tetap di luar paket.
- Saat melaksanakan rilis yang termasuk pekerjaan ini, gunakan Plugin Creator untuk **update plugin yang sama**: baca source/inventory dan current_release_id terbaru, bandingkan perubahan, pakai expected_release_id aktual.
- Jika menghapus file lama, gunakan delete_paths berkas yang terverifikasi, bukan sekadar tidak memasukkannya ke ZIP. Pertahankan manifest kompatibilitas yang dibuat layanan.
- Baca balik versi, source terdampak dan inventaris penghapusan; catat release ID aktual dan status uji yang masih belum selesai. Jangan menyalin email akun ke repo.

**Keluaran:** rilis privat 2.1.0 yang dapat diuji langsung.
**Selesai bila:** pemeriksaan teknis dan pembacaan balik lulus. Upload berhasil tidak dinyatakan sebagai bukti kualitas hasil, aktivasi host, batch bersamaan atau gerak aktual.

### Tahap 7 — Uji manual pengguna dan perbaikan terarah

**Pekerjaan**
- Pengguna menguji rilis privat di ChatGPT dan video di Omni Flash; tidak mengganti proses ini dengan klaim keterbatasan alat pengembang.
- Prioritaskan reproduksi masalah: satu referensi living–kitchen, kitchen tidak berganda, bedroom diagonal, exterior utuh, lampu/plafon, variasi dan ritme gerak, prompt siap salin, serta kelanjutan saat save gagal.
- Uji dua mode gambar dan batch sesuai jumlah yang disetujui; jika tujuh, catat tujuh file dan pelaksanaan yang benar-benar diamati.
- Uji exterior-to-living dengan **1 atau 2 referensi sesuai pilihan pengguna**; nilai ambang pintu, hubungan ruang dan interior yang terungkap. Penerimaan kontrak kedua pilihan diuji teknis; pengguna tidak diwajibkan menguji kedua pilihan video sekaligus. Catat pilihan yang belum diuji.
- Catat hasil pada matriks di bawah, perbaiki bagian terdampak dan update plugin yang sama. Tidak perlu pengujian video ulang untuk perubahan dokumen saja.

**Keluaran:** penerimaan berdasarkan hasil aktual, beserta daftar kasus yang belum diuji.
**Selesai bila:** kasus inti yang diperbaiki diterima pengguna. Bila salah satu pola penghubung belum diuji, nyatakan batas penerimaan tersebut secara eksplisit; jangan menyatakan seluruh pola lulus.

## 6. Matriks penerimaan

Pemeriksaan kontrak/file/ekspor sudah dijalankan pada tahap 6. Seluruh pembuktian gambar natural, geometri visual, batch nyata, gerak dan audio pada rilis perbaikan **menunggu uji manual pengguna**. Temuan manual lama pada bagian 2 menjadi dasar, bukan status lulus rilis baru.

| Kasus / kebutuhan | Harapan | Bukti utama |
| --- | --- | --- |
| P01 living-to-kitchen | Satu foto utuh berisi living dan kitchen, satu shot 6 detik, tidak disusul kitchen lagi | Kontrak/paket + gambar/video pengguna |
| P02 tata ruang | Kitchen tunggal, orientasi gambar dan gerak sesuai; tidak muncul kitchen kedua | Review gambar dan video nyata |
| P03 bedroom | Three-quarter, sasaran 35–45° terhadap sumbu bed, bed memanjang diagonal; bukan frontal simetris | Data komposisi + review gambar |
| P04 komposisi | Posisi/arah kamera, subjek, kedalaman, batas penting dan dukungan lintasan jelas | Kontrak + review visual |
| P05 ritme | Gerak terpilih terbaca dalam 4/6 detik; simultan/sekuensial sesuai rencana | Data waktu + video nyata |
| P06 save gagal | Diskusi/revisi konsep berlanjut; checkpoint terakhir utuh, lokasi baru hanya diklaim setelah berhasil | Tes kegagalan terkontrol + laporan host bila terjadi |
| P07 exterior | Atap, sisi kiri/kanan dan dasar terlihat utuh dengan margin wajar | Gambar nyata; bukan tuntutan semua frame video |
| P08 lampu/plafon | Setiap interior mempunyai armatur yang terbaca, logis dan sesuai desain; antarview konsisten | Rancangan + gambar/video nyata |
| P09 peran referensi | Bukan first/last wajib; prompt tanpa nama file/ID, metadata tetap benar | Template/validator/ekspor + salin manual |
| P10 kamera | Gerak dipilih dari DNA per area, tanpa paksaan dolly + pan; pan/orbit terpilih ≥12° | Provenance + rencana + video nyata |
| P11 format chat | Satu block berisi satu prompt lengkap sembilan bagian; tidak perlu membersihkan isi | Tampilan/copy ChatGPT + kesamaan isi ekspor |
| Dua mode | Prompt-only tidak mengaku sudah ada gambar; generate menghasilkan file sesuai rencana | Kontrak + uji ChatGPT |
| Batch tujuh jika direncanakan | Tujuh gambar individual dari satu permintaan/tahap; tidak menjadi kolase atau perintah per gambar | Catatan pelaksanaan nyata; jumlah file bukan bukti paralel |
| Exterior-to-living | **1 atau 2 referensi sesuai pilihan pengguna**, satu shot 6 detik; living tidak diulang, jumlah aset sesuai pilihan | Tes kontrak kedua pilihan + uji video pilihan pengguna; hasil pilihan lain tidak otomatis lulus |
| Audio/struktur | Ambient halus tanpa musik; tidak ada cut/morphing/perubahan elemen tetap | Video dan audio yang benar-benar diakses |
| Ekspor/resume/migrasi | File asli, keputusan dan delegasi terjaga; aset/review lama tidak otomatis cocok dengan aturan baru | Tes paket + kelanjutan manual |

Validator dapat membuktikan struktur, rentang nilai rencana, pemetaan, revisi, file dan hash. Validator tidak membuktikan geometri 3D dari gambar, naturalitas, sudut kamera aktual, pan aktual, kualitas audio atau eksekusi batch paralel.

## 7. Contoh jumlah dan durasi sesudah perbaikan

| Susunan | Shot | Gambar utama | Prompt video | Total |
| --- | --- | --- | --- | --- |
| Exterior + living + kitchen + bedroom + bathroom | 5 | 5 | 5 | 22 detik |
| Exterior + living-to-kitchen + bedroom + bathroom | 4 | **4** | 4 | **20 detik** |
| Exterior-to-living + kitchen + bedroom + bathroom | 4 | **4 atau 5**, sesuai pilihan 1/2 referensi penghubung | 4 | **18 detik** |
| Exterior + living-to-kitchen + bedroom + laundry + bathroom | 5 | 5 | 5 | 24 detik |

Contoh adalah pola hitung, bukan kewajiban memakai semua area. Area opsional tetap mengikuti sumber. Tujuh gambar hanya bila rencana sah benar-benar memerlukannya, bukan kuota setiap produksi. Tidak menambah gambar kedua pada salah satu shot penghubung sebagai kewajiban terselubung.

## 8. Peta berkas dan batas perubahan

Seluruh path berikut relatif terhadap bekerja/plugin/. R = ubah saat implementasi, B = baru untuk kebutuhan nyata, P = pertahankan kecuali integrasi menuntut perubahan.

| Komponen | Tindakan / tahap |
| --- | --- |
| home-productions/plugin.json | R — versi/ringkasan saat tahap 6, identitas tetap |
| home-productions/skills/produce-home-tour/SKILL.md | R — rute, keputusan, checkpoint, gambar, format chat; tahap 2–4 |
| references/production-rules.yaml dan project-contract.md | R — kontrak/pemetaan, versi, kompatibilitas; tahap 1 |
| assets/project.schema.json dan project-template.json | R — schema 2.1 dan data pandangan/tata ruang; tahap 1 |
| scripts/validate_project.py | R — kontrak, metadata terpisah dan review sesuai tahap; tahap 1/5 |
| scripts/save_project.py | B — penyimpanan aman, fallback dan hasil nyata; tahap 2 |
| references/preproduction.md dan image-workflow.md | R — geometri, komposisi, gambar gabungan dan review; tahap 3 |
| assets/image-prompt-template.md | R — exterior utuh, bedroom diagonal, plafon/lampu, naturalitas; tahap 3 |
| references/omni-flash.md dan assets/prompt-template.md | R — R2V, variasi/ritme kamera dan format salin; tahap 4 |
| scripts/build_production_package.py | R — ekspor dan peta gambar–shot; tahap 5 |
| agents/openai.yaml | Tinjau/sesuaikan bila deskripsi berubah; tahap 3/6, kebijakan tetap |
| references/repo-access.md dan scripts/requirements.txt | P — jalur akses dan dependensi yang sudah sesuai |
| tests/ | R/B — tes perilaku nyata terdampak, termasuk checkpoint dan migrasi; tahap 1–6 |
| tooling/package_plugin.py | P — sesuaikan hanya jika inventaris baru memerlukannya |
| README.md, production-workflow.md, implementation-plan.md | R — satu set dokumen aktif, status aktual tiap tahap |

Path singkat references/, assets/, scripts/ dan agents/ dalam tabel mengacu ke home-productions/skills/produce-home-tour/. Tidak membuat folder versi baru atau mengembalikan skrip crop yang sudah dihapus.

## 9. Baseline dan pelaporan kemajuan

Baseline tersedia: source/rilis privat 2.0.0, schema 2.0/rules 2.0.0; 53 tes teknis pernah lulus sebelum temuan baru ini. Angka tersebut bukan bukti perbaikan 2.1.0 atau penerimaan manual.

- Plugin: [home-productions](https://chatgpt.com/plugins/plugins_6afd5aeb32208191a60a8b85426c898f).
- Plugin ID: plugins_6afd5aeb32208191a60a8b85426c898f.
- Release ID baseline 2.0.0: pluginrel_6afd8f59eab0819199eed6bf3b189717, hanya riwayat. Rilis aktif 2.1.0 dicatat pada bagian 10; baca current_release_id aktual sebelum update berikutnya.
- Scope/audience: USER / PRIVATE.
- Publisher akun dan defaultPrompt dipertahankan; tidak membuat plugin baru.

Setelah tiap tahap, catat berkas yang berubah, hasil pemeriksaan, status rilis dan aspek yang belum diuji pada dokumen aktif ini. Rencana baru tidak menandai tahap lama gagal seluruhnya, dan tidak menganggap temuan manual sudah selesai hanya karena instruksi telah ditulis.

## 10. Hasil implementasi — 19 November 2026

| Tahap | Hasil aktual | Status |
| --- | --- | --- |
| 1 — Kontrak | Schema 2.1/rules 2.1.0; composition, spatial_plan, area_specs/lampu dan reference_choice. Living–kitchen satu foto; exterior-to-living menerima pilihan 1/2. ID/nama file tidak boleh di badan prompt | Selesai |
| 2 — Checkpoint | save_project.py menulis file sementara, memvalidasi/baca balik dan menerbitkan tanpa menimpa file lama. Fallback nama/folder membawa aset asli; gagal tetap mengembalikan status jujur tanpa merusak dict/keputusan sesi | Selesai |
| 3 — Gambar | Instruksi dua mode/batch diperbarui; posisi kamera, komposisi dan tata ruang bersama; bedroom diagonal 35–45°, exterior utuh, plafon/lampu dan review piksel | Implementasi selesai; kualitas menunggu manual |
| 4 — R2V | Sembilan bagian, referensi bukan first/last wajib, tanpa ID/nama file; variasi gerak mengikuti sumber, geometri/ritme sesuai durasi dan code block per shot | Implementasi selesai; hasil gerak/audio menunggu manual |
| 5 — Paket/migrasi | Empat gambar/20 detik; empat atau lima/18 detik sesuai pilihan. Renderer chat dan .txt memakai isi sama. CLI --migrate-to membuat salinan dengan aset, tanpa menggabungkan foto lama atau memalsukan review baru | Selesai |
| 6 — Teknis/rilis | 70 tes lulus; format skill, schema manifest resmi, template, tautan, arsip dan source rilis dibaca balik | Selesai |
| 7 — Manual | Panduan tersedia di README; kasus P01–P11, dua mode/batch, pilihan exterior-to-living dan resume. Belum ada hasil manual 2.1.0 | Serah-terima siap; penerimaan belum selesai |

### Bukti teknis dan peninjauan terhadap plan

| Kelompok | Jumlah tes | Cakupan |
| --- | --- | --- |
| test_project_rules.py | 31 | Cakupan/durasi/sumber, satu foto gabungan, pilihan 1/2, komposisi bedroom/exterior, lokasi/lampu, metadata/prompt dan migrasi |
| test_checkpoint.py | 9 | File/folder tidak dapat ditulis, baca balik gagal, pemindahan/corrupt/missing aset, checkpoint lama utuh, CLI dari memori dan konversi salinan |
| test_images.py | 7 | Dua mode, parsial/draft/review, tujuh aset sintetis, fungsi terpadu dan pan tunggal |
| test_preproduction.py | 4 | Struktur anotasi tersimpan edh022/edh035 dan sumber daya/tautan skill; bukan analisis ulang video |
| test_production_package.py | 13 | Ekspor/portabilitas, pilihan referensi, empat gambar/20 detik, kesamaan code block/.txt, kegagalan salinan dan perlindungan paket lama |
| test_package.py | 6 | Inventaris, determinisme, byte/CRC arsip, manifest/skill dan tidak mengemas file pengembangan |

P01–P11 ditelusuri pada kontrak/instruksi/template serta tes data/ekspor yang relevan. Variasi gerak, komposisi, naturalitas, lampu, plafon dan hubungan ruang tetap memerlukan penilaian media; tidak dibuat tes kata kunci yang mengaku membuktikan perilaku model.

quick_validate menyatakan skill valid. Template brief sah pada validator. Manifest 2.1.0 divalidasi terhadap schema resmi Agent Plugins 1.0.0. Seluruh tautan lokal dalam paket diperiksa. Pustaka pengetahuan tidak berubah, tidak ada analisis ulang semua video, folder versi baru, layanan tambahan atau komponen crop yang dikembalikan.

Fixture aset/batch/review/approval dan kegagalan izin adalah sintetis/terkontrol. Tes membuktikan konsistensi data dan perilaku I/O, bukan kualitas produksi atau izin filesystem ChatGPT pengguna yang sesungguhnya.

### Rilis terverifikasi

- [home-productions 2.1.0](https://chatgpt.com/plugins/plugins_6afd5aeb32208191a60a8b85426c898f), plugin ID tetap plugins_6afd5aeb32208191a60a8b85426c898f.
- Release ID: pluginrel_6afe70c8ec04819189e0f70757fec57a.
- Arsip: dist/home-productions-2.1.0.zip; SHA-256 3b5d62b56db89963320e140dfd4f16f57b766638fcbc9491fd205213dcb4718d.
- Tujuh belas berkas source cocok dengan pembacaan balik; manifest kompatibilitas layanan menjadi berkas ke-18 dan versinya sinkron 2.1.0.
- Baseline remote dibandingkan dengan source Git sebelum update; tidak ada perubahan remote tak terduga. Update memakai expected_release_id yang dibaca segar.
- Tidak ada file lama yang perlu dihapus pada rilis ini; helper checkpoint ditambahkan. Publisher, defaultPrompt, USER/PRIVATE dipertahankan, tanpa menyalin email akun ke repo.

### Serah-terima tahap 7

Gunakan [panduan uji 2.1.0](README.md#panduan-uji-manual-210). Prioritas reproduksi: kitchen tunggal pada satu foto living–kitchen, bedroom diagonal, exterior utuh, lampu/plafon, gerak beragam sesuai ritme, prompt siap salin dan checkpoint/resume.

Exterior-to-living mengikuti pilihan pengguna 1 atau 2; pengguna tidak diwajibkan menguji kedua opsi sekaligus. Penerimaan opsi yang belum diuji tidak disimpulkan dari opsi lainnya. Aktivasi skill pada host, batch simultan nyata, kualitas gambar serta video/audio belum diverifikasi pada rilis baru.
