## Bagian penting

1. `video`: identitas file dan metadata teknis.
2. `architecture`: gaya arsitektur serta ciri eksterior dan interior yang diamati.
3. `visual_style`: warna, pencahayaan, lingkungan, musim yang *tampak*, suasana.
4. `video_structure`: pola urutan adegan dan tempo keseluruhan.
5. `shots`: catatan per shot (waktu, scene, framing, gerakan kamera, detail terlihat, transisi, keyframe).
6. `analysis_quality`: ketidakpastian, estimasi, dan status verifikasi.

## Aturan yang menjaga kualitas data untuk ratusan video

- Satu file YAML = satu video, satu item `shots` = satu shot.
- Gunakan ID berurutan: `VID-001`, `VID-002` dan seterusnya. Jangan mengganti ID setelah dipakai.
- Nama kategori/tag gunakan bahasa Inggris dan `snake_case`. Catatan bebas menggunakan bahasa Indonesia.
- Jangan masukkan ide kreatif, prompt, instruksi Google Flow, saran pengembangan, atau elemen yang *tidak terlihat* di video.
- Untuk data belum diketahui gunakan `null`. Untuk daftar yang kosong gunakan `[]`.
- Bedakan **observasi langsung** (contoh: pintu warna hijau) dengan **interpretasi** (contoh: American Cottage atau gerakan dolly). Simpan `confidence` dan `uncertainties`.
- Durasi dan batas shot ditulis dalam detik; gunakan nilai perkiraan bila belum diketahui frame presisinya.
- Gunakan ID shot `shot-01`, `shot-02`, `shot-03`, dan seterusnya, sesuai dengan nama gambar `shot-01.jpg`, `shot-02.jpg`, `shot-03.jpg`. Di laporan Markdown, tampilkan sebagai **Shot 01**, **Shot 02**, dan seterusnya.
- Simpan **tepat satu keyframe asli untuk setiap shot**, dalam folder `references/VID-XXX/` dan rujuk melalui `shots[].keyframe` sebagai path relatif terhadap root repository.
- Simpan `storyboard.jpg` yang menggabungkan keyframe semua shot dalam folder video yang sama; tampilkan gambar ini **langsung** pada bagian atas `references/VID-XXX/analysis.md` dengan `![Storyboard](storyboard.jpg)`.
- Setiap folder video **wajib** memiliki `analysis.yaml` (sumber data terstruktur AI) dan `analysis.md` (laporan visual untuk manusia), selain `storyboard.jpg` dan tepat satu gambar per shot. Gunakan `templates/video-analysis.yaml` serta `templates/analysis.md`.
- `analysis.yaml` tetap menjadi **satu-satunya sumber fakta**. Isi `analysis.md` harus mengikuti YAML yang sama; tidak boleh menambahkan observasi/interpretasi baru, angka, atau detail yang tidak tercatat dalam YAML. Jika YAML berubah, sinkronkan `analysis.md`.
- Pada `analysis.md`, tampilkan **gambar setiap shot secara langsung** di bawah heading masing-masing, bukan tautan ke gambar. Gunakan contoh `<img src="shot-01.jpg" alt="Shot 01" width="360">` dengan nama berurutan (`shot-02.jpg`, dst.); gambar akan terlihat di GitHub tanpa membuka file terpisah. ID di YAML mengikuti nama file tanpa ekstensi: `shot-01`, `shot-02`, dst.; file gambar memakai format `shot-NN.jpg` (dua digit, dimulai dari `shot-01.jpg`). Path HTML di Markdown relatif terhadap folder video, sedangkan `shots[].keyframe` dalam YAML relatif terhadap root repository.
- `analysis.md` mengikuti urutan: **judul dan sumber data → informasi video → storyboard gabungan → identitas arsitektur → warna/pencahayaan/atmosfer → timeline → analisis per shot dengan gambar inline → kualitas/ketidakpastian**.
- Timeline `analysis.md` wajib sesuai `shots[]` di YAML (ID, urutan, start/end, gerakan kamera, scene, dan durasi). Cantumkan catatan confidence dan batas ketidakpastian, serta status verifikasi.
- `storyboard.jpg` merupakan ringkasan seluruh shot, **bukan pengganti gambar individual**. Tidak perlu menambah gambar lain di luar kebutuhan yang telah disepakati.
- Analisis hanya berfokus pada **visual**; tidak perlu mencatat audio, musik, voiceover, atau membuat prompt dan ide konten.
- Audit jika `shot_count` tidak sesuai jumlah elemen `shots` atau urutan waktu tidak menyambung.
- Semua analisis hanya bersumber dari isi video; asal negara tempat rumah itu berdiri tidak dapat dipastikan hanya dari gaya arsitektur.