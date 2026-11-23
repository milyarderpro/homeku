# Metode inti audit visual HOMEKU

Baca panduan ini sebelum mengisi JSON. Pengamatan dilakukan per take kontinu, bukan per ruangan. Lihat perjalanan utuh lalu frame terpilih berurutan. Catatan kerja bersifat sementara; hanya audit.json menjadi sumber final.

## Urutan keputusan per fase

1. **Kedalaman dahulu.** Bandingkan ukuran objek yang sama, lapisan dekat/jauh, oklusi dan ruang yang terbuka. Tentukan apakah kamera mendekat, menjauh, netral atau ambigu. Sebelum memilih Pan-only/NO IN/OUT, periksa kemungkinan Dolly dan Zoom.
2. **Translasi.** Periksa perpindahan lateral/vertikal dengan foreground dan background. Apakah kusen bergeser terhadap dinding jauh? Apakah sisi benda berubah? Bedakan gerak badan kamera dari gerak pandang.
3. **Rotasi.** Periksa arah pandang terhadap jangkar; gabungkan Pan/Tilt yang nyata dengan translasi yang juga terlihat. Jangan memilih hanya komponen paling menonjol.
4. **Fase.** + berarti simultan; → berarti komponen mulai/berhenti/berubah. Area baru atau tempo berubah saja tidak membuat cut/fase baru.
5. **Besaran dan tempo.** Ukur skala, usahakan sudut, lalu nilai tempo pada interval waktu setara. Tulis bahasa sederhana dan notasi teknis dari keputusan yang sama.

## Matriks pembeda Pan / Orbit / Truck

| Tafsir | Oklusi foreground | Selisih paralaks | Perspektif/posisi jangkar utama |
| --- | --- | --- | --- |
| Pan | Biasanya menyapu scene tanpa perubahan lapisan besar akibat translasi | Pergeseran layar bisa berbeda karena proyeksi; bukan bukti translasi tunggal | Pandangan berputar; sisi objek tidak berubah seperti lintasan mengelilinginya |
| Orbit | Foreground dapat membuka/menutupi latar saat mengelilingi jangkar | Lapisan dekat/jauh bergeser berbeda | Sisi/sudut jangkar berubah sepanjang lintasan, sering tetap terbingkai |
| Truck | Foreground melewati/membuka latar akibat geser badan kamera | Lapisan dekat bergeser lebih besar daripada lapisan jauh | Translasi lateral; orientasi pandang relatif dipertahankan atau dikompensasi Pan |

Gunakan ketiga tes bersama. Satu delta layar bukan rekonstruksi pose3D. Distorsi lensa, zoom, objek bergerak dan deformasi generatif dapat mengacaukan petunjuk. Pan Right pada scene statis umumnya menyapu gambar ke kiri, tetapi arah satu objek saja tidak menentukan arah kamera. Orbit Left menyatakan badan kamera melingkar ke kiri mengelilingi jangkar; Pan Right menyatakan arah pandang berputar ke kanan. Keduanya bisa terjadi bersamaan.

**Contoh oklusi:** kusen dekat bergeser sehingga sakelar/nightstand di belakang mulai terlihat, sementara sisi objek utama berubah. Periksa translasi/orbit, jangan menyebutnya Pan hanya karena elemen menyapu layar. Bila kamera juga mundur dan pandangan mengompensasi ke kanan, hasil dapat berupa Dolly-Out + Orbit Left + Pan Right. Arah tetap ditentukan dari bukti sumber, bukan menyalin contoh.

**Kasus kalibrasi edh058:** living room dan bathroom memperlihatkan jangkar mengecil dan cakupan dekat/lantai melebar. Pan-only melewatkan OUT. Periksa pasangan frame awal–akhir dan lapisan ruang sebelum menetapkan NO IN/OUT; contoh ini bukan daftar jawaban untuk video lain.

## Kedalaman, vertikal dan ketidakpastian

Skala membesar saja dapat berasal dari Dolly-In, Zoom-In atau crop digital. Dolly membutuhkan dukungan kedalaman/oklusi/perspektif. Pan/Static/Zoom dapat benar-benar tidak memiliki translasi kedalaman. NO IN/OUT adalah simpulan netral; null adalah belum dapat ditentukan. Jangan memaksakan Dolly.

Tilt memerlukan rotasi vertikal jelas dan berkelanjutan. Drift/jitter tipis bukan Tilt; bedakan dari pedestal/gerak naik turun badan kamera. Jangan menyimpulkan penggunaan gimbal dari video saja.

## Pengamatan adaptif

Sumber2.3: baseline6FPS setiap shot ditambah batas native pertama/terakhir. Sumber≤6FPS seluruh native; shot<1detik native. Tidak ada interpolasi. Perdalam bagian yang belum jelas pada10FPS atau langsung native, lalu perluas jika pertanyaan belum terjawab. Alasan menyebut pertanyaan visual dan interval, bukan otomatis rentang tengah. Sumber2.2 tetap10FPS/native sesuai kontrak asal.

Ekstraksi bukan pemeriksaan. Hanya frame yang benar-benar dilihat dicatat viewed. Semua evidence, panel dan Overview harus termasuk viewed. Simpan frame kerja di workspace sementara, bukan ZIP.

## Estimasi dan tempo

~× adalah besaran perubahan skala gambar: IN=ukuran akhir/awal; OUT=ukuran awal/akhir. Gunakan objek/bagian yang sama, dimensi width/height yang sama, terlihat utuh pada kedua frame native. Catat piksel dalam koordinat resolusi sumber (bukan ukuran thumbnail), anchor serta evidence awal/akhir. Hindari objek terpotong; pilih anchor lain. Angka tampil satu desimal atau rentang yang mencakup hasil ukur. Ini bukan faktor kecepatan/jarak fisik.

Pan/Orbit: usahakan ~° melalui orientasi/jangkar. Bila tidak dapat dipisahkan dari gerak lain, estimate_basis menjelaskan kendala khusus; jangan memberi presisi palsu. Dolly+Zoom yang tidak terpisahkan tidak boleh diberi rasio total yang sama pada keduanya. Pertahankan batas atribusi dan komponen yang jelas.

Semua shot boleh moderate. Smooth bukan slow; tidak ada kuota tempo. Bandingkan perpindahan/reveal pada interval waktu setara dan konteks lintasan. Pertumbuhan skala saat mendekati objek tidak sendirian membuktikan percepatan fisik. Confidence mengikuti kecukupan bukti, bukan jumlah frame atau kelengkapan formulir.

## Detail desain yang diamati

Eksterior: (1) gaya dan massa, (2) ukuran/proporsi, (3) atap, (4) fasad/bukaan, (5) akses/teras, (6) material/cahaya tampak, (7) tapak/lingkungan.
Interior: (1) bentuk/volume/bukaan, (2) layout dan hubungan terlihat, (3) furnitur beserta bentuk/orientasi, (4) penyimpanan/properti pembeda, (5) tampilan material/lapisan cahaya, (6) lingkungan melalui bukaan.

Catat detail yang benar-benar terlihat, termasuk konfigurasi bathroom/kitchen yang berbeda. Hindari daftar furnitur generik. Pisahkan terlihat, uncertain, not-visible, not-present dan unknown. Urutan edit tidak membuktikan denah/adjacency. Nama gaya English; uraian Indonesia. Luas lantai wajib estimasi rentang. Ketentuan produksi reverse/4–6detik/lima shot tidak berlaku di audit pustaka.
