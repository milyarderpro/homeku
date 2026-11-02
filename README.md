# Homeku — Library Analisis Video Rumah

Repository ini menyimpan **hasil analisis visual video desain rumah** dalam format YAML yang konsisten, agar mudah dibaca, ditelusuri, dan dibandingkan oleh manusia maupun AI.

**Cakupan saat ini:** hanya analisis visual. Belum mencakup audio, ide konten, prompt generasi, atau pembuatan video baru.

## Struktur folder

```text
homeku/
├── references/
│   └── VID-001/
│       ├── analysis.yaml       # hasil analisis terstruktur
│       ├── S1.jpg              # 1 keyframe asli untuk shot S1
│       ├── S2.jpg              # 1 keyframe asli untuk shot S2
│       ├── S3.jpg
│       ├── S4.jpg
│       ├── S5.jpg
│       └── storyboard.jpg      # gabungan keyframe untuk dibaca manusia
├── rules/
│   └── analysis.md             # standar pengamatan dan pencatatan
└── templates/
    └── video-analysis.yaml     # template baku untuk setiap video
```

Folder `references/VID-002/`, `VID-003/` dan seterusnya menggunakan struktur yang sama, dengan jumlah file `S1.jpg`, `S2.jpg`, dan lain-lain mengikuti jumlah shot video.

## Peran tiap file

- **`analysis.yaml`** adalah sumber data utama; satu file berisi seluruh metadata video, ciri arsitektur, gaya visual, struktur video, rincian setiap shot, dan catatan kualitas analisis.
- **`S1.jpg`, `S2.jpg`, ...** adalah **tepat satu gambar keyframe asli per shot**. Setiap `shots[].keyframe` di YAML menunjuk ke file tersebut dengan path relatif terhadap root repository, misalnya `references/VID-001/S1.jpg`.
- **`storyboard.jpg`** adalah gabungan gambar dari semua shot, untuk memudahkan peninjauan visual. Nantinya gambar ini dapat ditampilkan dalam **`references/VID-001/analysis.md`**, bila format dokumentasi manusia tersebut sudah disepakati. File `analysis.md` per-video belum dibuat pada tahap ini.
- **`templates/video-analysis.yaml`** menjadi format yang diikuti seluruh hasil analisis.
- **`rules/analysis.md`** menjelaskan prinsip analisis agar konsisten pada banyak video.

## Konvensi penamaan dan pengisian

1. ID video: `VID-001`, `VID-002`, `VID-003`, dan seterusnya.
2. ID shot: `S1`, `S2`, `S3`, dan seterusnya, tanpa nol di depan.
3. Satu video = satu folder di `references/` = satu `analysis.yaml`.
4. Satu shot = satu entri `shots[]` = satu keyframe `S<n>.jpg`.
5. Gunakan `snake_case` untuk label teknis; catatan bebas boleh berbahasa Indonesia.
6. Isi hanya hal yang diamati dari video. Jika tidak diketahui, gunakan `null`; jika data bersifat perkiraan, cantumkan pada `analysis_quality` / `confidence`.
7. Pastikan `video.shot_count` sesuai jumlah entri `shots`, waktunya berurutan, dan setiap path gambar memang ada.

Untuk mulai menganalisis video lain, salin `templates/video-analysis.yaml`, lalu isi dan simpan sebagai `references/VID-002/analysis.yaml`, beserta keyframe per shot dan storyboard gabungan.

Detail aturan terdapat di [rules/analysis.md](rules/analysis.md). Contoh hasil lengkap tersedia di [references/VID-001/analysis.yaml](references/VID-001/analysis.yaml).
