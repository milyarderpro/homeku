# Aturan Analisis Visual Homeku

> Dokumen ini menjelaskan **isi dan standar mutu analisis**. Untuk alur menerima video, menampilkan hasil, meminta revisi, dan menyimpan hanya setelah `save now`, ikuti [workflow-analysis.md](workflow-analysis.md). Jangan melakukan penulisan GitHub pada tahap analisis/review. Penyimpanan berlangsung **berurutan, satu video hingga selesai**. ChatGPT hanya boleh membaca GitHub selama analisis/review; perintah penyimpanan dan proses GitHub Actions dijelaskan dalam dokumen workflow.

## Bagian penting

1. `video`: identitas file dan metadata teknis.
2. `architecture`: gaya arsitektur, karakteristik eksterior/interior, serta **estimasi ukuran dan proporsi bangunan** melalui `building_scale`.
3. `visual_style`: warna, pencahayaan, lingkungan, musim yang *tampak*, suasana.
4. `video_structure`: pola urutan adegan dan tempo keseluruhan.
5. `shots`: catatan per shot (waktu, scene, framing, gerakan kamera, detail terlihat, transisi, keyframe).
6. `analysis_quality`: ketidakpastian, estimasi, dan status verifikasi.

## Standar v1.3 — Detailed Exterior & Environment Analysis

- **Amati sepanjang shot**, termasuk awal, tengah, dan akhir gerakan kamera. Keyframe adalah bukti representatif, **bukan** satu-satunya frame untuk menemukan fakta. Data harus spesifik, lengkap menurut hal yang terlihat, tanpa jumlah item minimum yang dipaksakan.
- **Eksterior/arsitektur:** bentuk massa rumah, atap dan kemiringan, fasad, material dan finishing yang tampak, warna, kusen/jendela, pintu, teras, tangga, pagar, chimney dan hubungan spasial objek. Catat posisi relatif, bentuk, ukuran visual, warna, dan material ketika cukup jelas.
- **Lingkungan/lanskap:** ukuran dan posisi pohon, warna/kerapatan dedaunan, jenis vegetasi secara visual, rumput, bunga, taman, hamparan sawah/ladang jika dapat dikenali, sungai/danau, bukit/pegunungan, jalur masuk, pagar, tetangga/bangunan lain, tanah/batu/salju, kabut, awan, dan langit. Catat **depan/samping/belakang/kiri/kanan/jauh** dari rumah jika didukung framing.
- Tulis label Inggris **spesifik** yang bisa ditelusuri ke video, misalnya `large_tree_with_yellow_leaves_left_of_house`, `green_rice_field_beside_house`, `distant_mountain_silhouette_behind_roofline`. Hindari label generik `tree` jika atribut penting terlihat jelas.
- **Ketidakpastian:** jika bentuk lahan hanya tampak seperti lahan pertanian, pilih `green_agricultural_field` alih-alih memastikan itu sawah. Dedaunan kuning tidak otomatis membuktikan musim gugur atau negara tertentu. Jangan menambah fakta berdasarkan preferensi estetika atau asumsi rumah ideal.

## Standar v1.3 — Detailed Interior & Spatial Analysis

- **Geometri ruangan:** bentuk dan proporsi visual, plafon, balok terekspos, bukaan, tangga, perapian, area masuk dan hubungan antar-ruangan.
- **Finishing:** warna, pola, tekstur, dan material yang *terlihat* pada dinding, lantai, plafon, countertop, backsplash, kabinet dan panel. Jika bahan persis tidak terbukti, gunakan deskripsi penampakan (`light_wood_appearance_flooring`), bukan menyatakan kayu tertentu sebagai fakta.
- **Furnitur/properti:** jenis, bentuk, ukuran relatif, warna, upholstery/material yang tampak, jumlah jika jelas, arah hadap, penempatan dan hubungan antarbenda. Contoh: `cream_fabric_sofa_facing_stone_fireplace` lebih baik daripada `sofa`.
- **Dekorasi/pencahayaan:** karpet, bantal, lampu, vas, buku, tanaman, lukisan, gorden, tekstil, cahaya alami/buatan dan sumbernya jika terlihat. Cahaya dan atmosfer yang sudah disimpan pada field lain harus tetap konsisten.
- **Fokus ruangan:** living room (area duduk, meja, TV/fireplace), kitchen/dining (kabinet, island, sink, appliances, meja makan), bedroom (tempat tidur, bedding, headboard, bedside), bathroom (shower, bathtub, toilet, vanity, tile), laundry/utility (mesin, rak, penyimpanan). **Ini panduan observasi, bukan daftar objek wajib ada.**
- Pemandangan **melalui jendela** tetap bisa dicatat pada `visible_details.environment` saat interior shot; hindari mengarang area luar yang tidak tampak.
- Catat unsur pada kategori **yang sudah ada**, bukan field YAML baru: `shots[].visible_details.architectural` untuk struktur, finishing dan bukaan; `furniture_and_props` untuk objek; `environment` untuk konteks lingkungan luar atau pemandangan yang terlihat. Gunakan `[]` bila tidak ada detail yang terlihat.

## Dual representation: fakta YAML dan narasi manusia

- Analisis **baru**: item `visible_details` memakai English `snake_case`, sebaiknya memuat atribut + posisi/relasi jika terlihat. Nama field, `schema_version: "2.1"` dan data arsip **tidak berubah**.
- **ChatGPT** membuat narasi bahasa Indonesia natural untuk tiga kategori per shot **berdasarkan item YAML**, sebelum review dan sebelum pesan `save now`. Narasi boleh menyatukan beberapa item menjadi kalimat mengalir, tetapi **tidak boleh menambah, menghilangkan, mengubah atau mempertajam fakta** di luar bukti YAML.
- Lakukan review dua arah YAML ↔ narasi: objek, material, jumlah, warna, posisi, dan ketidakpastian harus sejalan. Jika satu detail tidak bisa ditulis dengan aman, revisi YAML/narasi dalam chat, **jangan mengarang** untuk memenuhi paragraf.
- `analysis.yaml` adalah satu-satunya sumber fakta; narasi tidak ditambahkan ke YAML, melainkan hanya payload penyajian dalam `requests/save.json`. GitHub Actions **tidak menjalankan AI** atau penerjemahan.
- Untuk kategori kosong, narasi `null` dan Markdown menampilkan **Tidak ada detail yang tercatat.** Evaluasi kelengkapan berdasarkan apa yang tampak; jangan paksakan jumlah item.
- Penyimpanan dan request hanya mengikuti [workflow-analysis.md](workflow-analysis.md), termasuk pemeriksaan exact `save now` dan sequential save.

## Estimasi visual ukuran bangunan (schema 2.1)

- `architecture.building_scale` wajib ada dalam setiap YAML: `perceived_size`, `building_form`, `vertical_scale`, `footprint`, `estimated_floor_area_m2.min`, `estimated_floor_area_m2.max`, dan `confidence`.
- `perceived_size` gunakan kategori `tiny`, `small`, `medium`, `large`, atau `estate` berdasarkan kesan visual; tidak ada ambang luas baku untuk kategori ini.
- `building_form` mencatat bentuk massa bangunan yang tampak (misalnya `narrow_elongated` atau `l_shaped`), `vertical_scale` tingkat/loft yang tampak atau diperkirakan, `footprint` kesan tapak `compact`, `moderate`, atau `expansive`.
- Luas lantai dalam m² adalah **rentang perkiraan visual** (`min`–`max`), bukan pengukuran atau klaim angka pasti; pilih rentang masuk akal berdasarkan petunjuk proporsi yang terlihat. Pastikan `min <= max`. Jika tidak mungkin diperkirakan secara wajar, keduanya `null`.
- `confidence` wajib mencatat `low`, `medium`, atau `high`; turunkan confidence untuk estimasi luas tanpa referensi skala yang kuat.
- Tidak perlu melakukan pemeriksaan konsistensi ukuran eksterior dan interior. Analisis tetap bersifat deskriptif terhadap video yang ada, bukan audit kelayakan arsitektur.
- Informasi ukuran pada `analysis.md` harus sama dengan `analysis.yaml`, diletakkan setelah **Identitas Desain** dan sebelum **Warna, Pencahayaan, dan Atmosfer**. Jika rentang luas `null`, tampilkan **Tidak diketahui** pada laporan Markdown.

## Asosiasi Wilayah Gaya Arsitektur (schema 2.1)

- `architecture.common_regions` wajib dicantumkan pada **analisis baru**, sebagai daftar kawasan luas yang lazim diasosiasikan dengan karakter gaya desain rumah yang terlihat, **bukan** lokasi asli bangunan, asal negara, atau peringkat prevalensi.
- Nilai yang diizinkan: `north_america`, `south_america`, `europe`, `asia`, `africa`, `oceania`. Boleh memilih lebih dari satu tanpa duplikat, gunakan English `snake_case`.
- Gunakan `[]` jika tidak ada asosiasi kawasan yang cukup masuk akal. Jangan mengisi hanya karena lanskap, musim, cuaca, atau gaya dekorasi tampak mirip wilayah tertentu; utamakan pengetahuan karakter arsitektur dan ungkapkan bahwa ini interpretasi.
- Pada analisis historis yang tidak memiliki field tersebut, data tetap valid. Validator memeriksa tipe, nilai dan duplikasi **jika field hadir**; kewajiban untuk draft baru ditegakkan melalui template dan review, bukan dengan menolak arsip lama.
- Dalam laporan Markdown tampilkan sebagai **Wilayah terkait gaya desain** pada Identitas Desain. Jika kosong atau tidak ada, tampilkan **Tidak diketahui**. Jangan mengklaim rumah di video benar-benar berlokasi di kawasan itu.

## Aturan yang menjaga kualitas data untuk ratusan video

- Satu file YAML = satu video, satu item `shots` = satu shot.
- Gunakan ID berurutan: `VID-001`, `VID-002` dan seterusnya. Jangan mengganti ID setelah dipakai.
- Nama kategori/tag gunakan bahasa Inggris dan `snake_case`. Catatan bebas menggunakan bahasa Indonesia.
- Jangan masukkan ide kreatif, prompt, instruksi Google Flow, saran pengembangan, atau elemen yang *tidak terlihat* di video.
- Untuk data belum diketahui gunakan `null`. Untuk daftar yang kosong gunakan `[]`.
- Bedakan **observasi langsung** (contoh: pintu warna hijau) dengan **interpretasi** (contoh: American Cottage atau gerakan dolly). Simpan `confidence` dan `uncertainties`.
- Durasi dan batas shot ditulis dalam detik; gunakan nilai perkiraan bila belum diketahui frame presisinya.
- Gunakan ID shot `shot-01`, `shot-02`, `shot-03`, dan seterusnya, sesuai dengan nama gambar `shot-01.jpg`, `shot-02.jpg`, `shot-03.jpg`. Di laporan Markdown, tampilkan sebagai **Shot 01**, **Shot 02**, dan seterusnya.
- Simpan **tepat satu keyframe JPEG yang diekstrak langsung dari frame video per shot**, dalam folder `references/VID-XXX/` dan rujuk melalui `shots[].keyframe` sebagai path relatif terhadap root repository. GitHub Actions memakai FFmpeg untuk mengekstrak frame pada timestamp yang dipilih selama analisis; JPEG hasil encode runner **tidak wajib identik byte** dengan gambar preview di chat, tetapi harus berasal dari shot dan video yang benar.
- Simpan `storyboard.jpg` yang menggabungkan keyframe semua shot dalam folder video yang sama; tampilkan gambar ini **langsung** pada bagian atas `references/VID-XXX/analysis.md` dengan `![Storyboard](storyboard.jpg)`.
- Setiap folder video **wajib** memiliki `analysis.yaml` (sumber data terstruktur AI) dan `analysis.md` (laporan visual untuk manusia), selain `storyboard.jpg` dan tepat satu gambar per shot. Gunakan `templates/video-analysis.yaml` sebagai schema data dan `templates/analysis.md` sebagai **acuan struktur**. Dalam workflow v1.3, Markdown final dibuat oleh `scripts/save_analysis_action.py` secara deterministik dari data YAML dan (untuk request baru) paragraf yang telah direview di chat; template Markdown **tidak dieksekusi** sebagai mesin template. Request historis tanpa narasi tetap dirender dengan formatter lama. Jika susunan laporan perlu diubah, sinkronkan acuan template **dan generator Python**.
- `analysis.yaml` tetap menjadi **satu-satunya sumber fakta**. Isi `analysis.md` harus mengikuti YAML yang sama; tidak boleh menambahkan observasi/interpretasi baru, angka, atau detail yang tidak tercatat dalam YAML. Jika YAML berubah, sinkronkan `analysis.md`.
- Pada `analysis.md`, tampilkan **gambar setiap shot secara langsung** di bawah heading masing-masing, bukan tautan ke gambar. Gunakan contoh `<img src="shot-01.jpg" alt="Shot 01" width="360">` dengan nama berurutan (`shot-02.jpg`, dst.); gambar akan terlihat di GitHub tanpa membuka file terpisah. ID di YAML mengikuti nama file tanpa ekstensi: `shot-01`, `shot-02`, dst.; file gambar memakai format `shot-NN.jpg` (dua digit, dimulai dari `shot-01.jpg`). Path HTML di Markdown relatif terhadap folder video, sedangkan `shots[].keyframe` dalam YAML relatif terhadap root repository.
- `analysis.md` mengikuti urutan: **judul dan sumber data → informasi video → storyboard gabungan → identitas arsitektur → ukuran & proporsi bangunan → warna/pencahayaan/atmosfer → timeline → analisis per shot dengan gambar inline → kualitas/ketidakpastian**.
- Timeline `analysis.md` wajib sesuai `shots[]` di YAML (ID, urutan, start/end, gerakan kamera, scene, dan durasi). Cantumkan catatan confidence dan batas ketidakpastian, serta status verifikasi.
- `storyboard.jpg` merupakan ringkasan seluruh shot, **bukan pengganti gambar individual**. Tidak perlu menambah gambar lain di luar kebutuhan yang telah disepakati.
- Tampilan storyboard v1.2 mengikuti **referensi editorial yang disepakati**: judul besar memakai nama video, subtitle durasi/jumlah shot/gaya utama, frame portrait seragam dengan margin konsisten, dan tiga baris caption di bawah tiap frame (nomor + scene, rentang waktu, gerakan kamera). **1–5 shot:** satu baris, jumlah kolom sama dengan jumlah shot. **6+ shot:** tiga kolom, jumlah baris otomatis. Gambar asli shot tidak di-crop/distorsi; generator menambahkan padding bila rasio frame berbeda. Scene dan camera berasal dari YAML, bukan teks buatan.
- Analisis hanya berfokus pada **visual**; tidak perlu mencatat audio, musik, voiceover, atau membuat prompt dan ide konten.
- Audit jika `shot_count` tidak sesuai jumlah elemen `shots` atau urutan waktu tidak menyambung.
- Semua analisis hanya bersumber dari isi video; asal negara tempat rumah itu berdiri tidak dapat dipastikan hanya dari gaya arsitektur.