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
- Gunakan ID shot `S1`, `S2`, `S3`, dan seterusnya (tanpa angka nol di depan), sesuai nama gambar `S1.jpg`, `S2.jpg`, dan sebagainya.
- Simpan **tepat satu keyframe asli untuk setiap shot**, dalam folder `references/VID-XXX/` dan rujuk melalui `shots[].keyframe` sebagai path relatif terhadap root repository.
- Simpan `storyboard.jpg` yang menggabungkan keyframe semua shot dalam folder video yang sama. Storyboard disiapkan untuk dokumentasi visual `analysis.md` di masa depan; file Markdown tersebut belum perlu dibuat sekarang.
- `analysis.yaml` tetap menjadi sumber data utama untuk AI. `storyboard.jpg` digunakan sebagai ringkasan visual, bukan pengganti keyframe masing-masing shot.
- Analisis hanya berfokus pada **visual**; tidak perlu mencatat audio, musik, voiceover, atau membuat prompt dan ide konten.
- Audit jika `shot_count` tidak sesuai jumlah elemen `shots` atau urutan waktu tidak menyambung.
- Semua analisis hanya bersumber dari isi video; asal negara tempat rumah itu berdiri tidak dapat dipastikan hanya dari gaya arsitektur.