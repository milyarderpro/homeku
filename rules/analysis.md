# Aturan Analisis Visual Homeku

> Dokumen ini menjelaskan **isi dan standar mutu analisis**. Untuk alur menerima video, menampilkan hasil, meminta revisi, dan menyimpan hanya setelah `save now`, ikuti [workflow-analysis.md](workflow-analysis.md). Jangan melakukan penulisan GitHub pada tahap analisis/review. Penyimpanan berlangsung **berurutan, satu video hingga selesai**. ChatGPT hanya boleh membaca GitHub selama analisis/review; perintah penyimpanan dan proses GitHub Actions dijelaskan dalam dokumen workflow.

## Bagian penting

1. `video`: identitas file dan metadata teknis.
2. `architecture`: gaya arsitektur, karakteristik eksterior/interior, serta **estimasi ukuran dan proporsi bangunan** melalui `building_scale`.
3. `visual_style`: warna, pencahayaan, lingkungan, musim yang *tampak*, suasana.
4. `video_structure`: pola urutan adegan dan tempo keseluruhan.
5. `shots`: catatan per shot (waktu, scene, framing, gerakan kamera, detail terlihat, transisi, keyframe).
6. `analysis_quality`: ketidakpastian, estimasi, dan status verifikasi.

## Estimasi visual ukuran bangunan (schema 2.1)

- `architecture.building_scale` wajib ada dalam setiap YAML: `perceived_size`, `building_form`, `vertical_scale`, `footprint`, `estimated_floor_area_m2.min`, `estimated_floor_area_m2.max`, dan `confidence`.
- `perceived_size` gunakan kategori `tiny`, `small`, `medium`, `large`, atau `estate` berdasarkan kesan visual; tidak ada ambang luas baku untuk kategori ini.
- `building_form` mencatat bentuk massa bangunan yang tampak (misalnya `narrow_elongated` atau `l_shaped`), `vertical_scale` tingkat/loft yang tampak atau diperkirakan, `footprint` kesan tapak `compact`, `moderate`, atau `expansive`.
- Luas lantai dalam m² adalah **rentang perkiraan visual** (`min`–`max`), bukan pengukuran atau klaim angka pasti; pilih rentang masuk akal berdasarkan petunjuk proporsi yang terlihat. Pastikan `min <= max`. Jika tidak mungkin diperkirakan secara wajar, keduanya `null`.
- `confidence` wajib mencatat `low`, `medium`, atau `high`; turunkan confidence untuk estimasi luas tanpa referensi skala yang kuat.
- Tidak perlu melakukan pemeriksaan konsistensi ukuran eksterior dan interior. Analisis tetap bersifat deskriptif terhadap video yang ada, bukan audit kelayakan arsitektur.
- Informasi ukuran pada `analysis.md` harus sama dengan `analysis.yaml`, diletakkan setelah **Identitas Desain** dan sebelum **Warna, Pencahayaan, dan Atmosfer**. Jika rentang luas `null`, tampilkan **Tidak diketahui** pada laporan Markdown.

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
- Setiap folder video **wajib** memiliki `analysis.yaml` (sumber data terstruktur AI) dan `analysis.md` (laporan visual untuk manusia), selain `storyboard.jpg` dan tepat satu gambar per shot. Gunakan `templates/video-analysis.yaml` sebagai schema data dan `templates/analysis.md` sebagai **acuan struktur**. Dalam workflow v1.2, Markdown final dibuat oleh `scripts/save_analysis_action.py` dari data YAML; template Markdown **tidak dieksekusi** sebagai mesin template. Jika susunan laporan perlu diubah, sinkronkan acuan template **dan generator Python**.
- `analysis.yaml` tetap menjadi **satu-satunya sumber fakta**. Isi `analysis.md` harus mengikuti YAML yang sama; tidak boleh menambahkan observasi/interpretasi baru, angka, atau detail yang tidak tercatat dalam YAML. Jika YAML berubah, sinkronkan `analysis.md`.
- Pada `analysis.md`, tampilkan **gambar setiap shot secara langsung** di bawah heading masing-masing, bukan tautan ke gambar. Gunakan contoh `<img src="shot-01.jpg" alt="Shot 01" width="360">` dengan nama berurutan (`shot-02.jpg`, dst.); gambar akan terlihat di GitHub tanpa membuka file terpisah. ID di YAML mengikuti nama file tanpa ekstensi: `shot-01`, `shot-02`, dst.; file gambar memakai format `shot-NN.jpg` (dua digit, dimulai dari `shot-01.jpg`). Path HTML di Markdown relatif terhadap folder video, sedangkan `shots[].keyframe` dalam YAML relatif terhadap root repository.
- `analysis.md` mengikuti urutan: **judul dan sumber data → informasi video → storyboard gabungan → identitas arsitektur → ukuran & proporsi bangunan → warna/pencahayaan/atmosfer → timeline → analisis per shot dengan gambar inline → kualitas/ketidakpastian**.
- Timeline `analysis.md` wajib sesuai `shots[]` di YAML (ID, urutan, start/end, gerakan kamera, scene, dan durasi). Cantumkan catatan confidence dan batas ketidakpastian, serta status verifikasi.
- `storyboard.jpg` merupakan ringkasan seluruh shot, **bukan pengganti gambar individual**. Tidak perlu menambah gambar lain di luar kebutuhan yang telah disepakati.
- Tampilan storyboard v1.2 mengikuti **referensi editorial yang disepakati**: judul besar memakai nama video, subtitle durasi/jumlah shot/gaya utama, frame portrait seragam dengan margin konsisten, dan tiga baris caption di bawah tiap frame (nomor + scene, rentang waktu, gerakan kamera). **1–5 shot:** satu baris, jumlah kolom sama dengan jumlah shot. **6+ shot:** tiga kolom, jumlah baris otomatis. Gambar asli shot tidak di-crop/distorsi; generator menambahkan padding bila rasio frame berbeda. Scene dan camera berasal dari YAML, bukan teks buatan.
- Analisis hanya berfokus pada **visual**; tidak perlu mencatat audio, musik, voiceover, atau membuat prompt dan ide konten.
- Audit jika `shot_count` tidak sesuai jumlah elemen `shots` atau urutan waktu tidak menyambung.
- Semua analisis hanya bersumber dari isi video; asal negara tempat rumah itu berdiri tidak dapat dipastikan hanya dari gaya arsitektur.