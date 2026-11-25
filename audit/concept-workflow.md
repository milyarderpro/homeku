# Menggunakan pustaka untuk konsep desain dan produksi

Gunakan audit sebagai pengetahuan visual untuk mengembangkan konsep baru atau mengikuti satu referensi tertentu. Setiap proyek memiliki keputusan desain, framing, dan produksi sendiri. Data audit mempertahankan kronologi sumber.

## Pilih sumber yang relevan

Mulai dari kebutuhan pengguna. Misalnya, tiga konsep American Cottage berukuran tiny dengan dapur dan ruang keluarga yang terhubung. Pisahkan syarat dari preferensi, lalu cari beberapa referensi aktif.

~~~sh
python tools/library.py search --house-type Cottage --style "American Cottage" --scale tiny --area kitchen --limit 5
python tools/library.py read rumah --part identity
python tools/library.py read rumah --part shot --shot shot-02
python tools/library.py read rumah --part area --shot shot-02 --area kitchen-1
~~~

Indeks mencari tipe rumah, gaya, skala, konfigurasi, rute, gerak, dan tempo. Buka identitas untuk susunan ruang, palet HEX dan atmosfer, lalu buka shot terpilih untuk detail pencahayaan serta pointer sumber. Buka gambar yang membantu keputusan; gunakan [kontrak reader](contracts/reader.md) untuk mengambil panel, Overview, dan blok Storyboard. Catat keterbatasan kecocokan bila pustaka belum punya sumber yang memenuhi brief.

## Kembangkan variasi dengan DNA yang jelas

- Pilih satu acuan utama untuk siluet, proporsi, atap dan entrance. Gunakan referensi lain untuk susunan area, keluarga bukaan, material, cahaya, atau kamera yang kompatibel.
- Buat perbedaan antar konsep pada bentuk dan hubungan elemen. Bathroom dapat memakai susunan shower, vanity, penyimpanan, serta bukaan yang berbeda sesuai tapak dan sirkulasi. Gunakan warna untuk menguatkan karakter desain.
- Sebutkan hubungan DNA yang dipertahankan dan perubahan baru untuk setiap konsep. Perkiraan luas sumber membantu menilai skala. Ukuran rumah baru adalah bagian dari brief dan keputusan proyek.
- Setelah pengguna memilih satu konsep, kunci massa, ukuran, bukaan, material, lingkungan, dan elemen tetap untuk seluruh shot. Catat rujukan audit dan keputusan proyek secara eksplisit.

| Kemampuan | Data yang dibaca |
| --- | --- |
| Tipe rumah, gaya, ukuran, dan palet | design.house_type, design.styles, design.size, design.features, design.palette serta katalog DNA |
| Variasi ruang dan furnitur | Area fisik, fungsi, kategori desain, fakta dan facet konfigurasi |
| Kontinuitas rumah | Rute, visibilitas, hubungan area, bukaan dan lingkungan yang terlihat |
| Komposisi dan gerak | Camera Start, framing, fase, tempo, Overview serta panel native |
| Prinsip umum | Knowledge memuat prinsip terkurasi tentang orisinalitas, skala, kontinuitas, dan komposisi |

Catat ketidakpastian serta negasi sesuai sumber. Rujuk halaman [prinsip desain](../knowledge/principles.md) untuk hubungan DNA, orisinalitas, skala, kompatibilitas gaya, variasi ruang, kontinuitas rumah, material dan cahaya, serta kecocokan frame awal.

## Susun frame awal dan gerakan

Untuk tiap take, tentukan area pertama, posisi dan arah kamera, sudut, tinggi, kemiringan, foreground, kedalaman, cahaya dan bagian yang akan terungkap. Baca Camera Start, panel Start, fase pertama, serta tempo secara bersamaan. Overview memuat frame wide terpilih dan komposisinya. Pada OUT, Overview biasanya berada di akhir sumber. Gunakan sudut yang sesuai lintasan dan ruang.

Untuk satu take multi area, pilih rute yang benar-benar kontinu dan pelajari tiap penghubung, kemunculan area, fokus, fase, serta tempo. Siapkan satu frame awal untuk take tersebut. Gunakan gambar pendukung untuk ruang yang muncul kemudian. Pastikan jalur kamera baru dapat melewati penghubung dalam desain terkunci.

Gerakan sederhana menjelaskan perjalanan. Notasi teknis mempertahankan komponen simultan, urutan fase, besaran bila tersedia, dan tempo. Catat adaptasi yang dibutuhkan oleh geometri rumah baru di rencana produksi.

## Mengikuti satu referensi

Jika pengguna memilih meniru satu video, baca ID aktif tersebut untuk desain, posisi furnitur, pencahayaan, urutan, framing, serta kamera dan tempo. Pertahankan penghubung dan reveal pada take multi area sesuai yang terlihat.

Untuk produksi IN, Overview awal sering cocok sebagai sumber gambar awal. Jika produksi OUT memakai reverse, gunakan Overview akhir sebagai gambar awal perjalanan kebalikan. Balik lintasan, arah rotasi, urutan fase, target dan perkembangan tempo sebelum membalik hasil video. Untuk fase campuran, Overview tengah, atau area yang baru terlihat kemudian, sesuaikan bagian lintasan dengan cakupan bukti. Keputusan reverse dicatat pada proyek produksi.
