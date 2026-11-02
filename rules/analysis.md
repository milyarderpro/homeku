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
- Simpan minimal 1 keyframe asli per shot, dengan path relatif terhadap folder library.
- Audit jika `shot_count` tidak sesuai jumlah elemen `shots` atau urutan waktu tidak menyambung.
- Semua analisis hanya bersumber dari isi video; asal negara tempat rumah itu berdiri tidak dapat dipastikan hanya dari gaya arsitektur.