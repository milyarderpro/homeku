# Homeku — Library Analisis Video Rumah

Repository ini menyimpan **hasil analisis visual video desain rumah** dalam format YAML yang konsisten, agar mudah dibaca, ditelusuri, dan dibandingkan oleh manusia maupun AI.

**Cakupan saat ini:** hanya analisis visual. Belum mencakup audio, ide konten, prompt generasi, atau pembuatan video baru.

## Struktur folder

```text
homeku/
├── references/
│   └── VID-001/
│       ├── analysis.yaml       # data analisis terstruktur (sumber utama)
│       ├── analysis.md         # laporan visual untuk dibaca di GitHub
│       ├── shot-01.jpg              # 1 keyframe asli untuk shot S1
│       ├── shot-02.jpg              # 1 keyframe asli untuk shot S2
│       ├── shot-03.jpg
│       ├── shot-04.jpg
│       ├── shot-05.jpg
│       └── storyboard.jpg      # gabungan keyframe untuk dibaca manusia
├── rules/
│   └── analysis.md             # standar pengamatan dan pencatatan
└── templates/
    ├── video-analysis.yaml     # template baku data terstruktur
    └── analysis.md             # template baku laporan visual
```

Folder `references/VID-002/`, `VID-003/` dan seterusnya menggunakan struktur yang sama, dengan jumlah file `shot-01.jpg`, `shot-02.jpg`, dan lain-lain mengikuti jumlah shot video.

## Peran tiap file

- **`analysis.yaml`** adalah sumber data utama; satu file berisi seluruh metadata video, ciri arsitektur, gaya visual, struktur video, rincian setiap shot, dan catatan kualitas analisis.
- **`shot-01.jpg`, `shot-02.jpg`, ...** adalah **tepat satu gambar keyframe asli per shot**. Setiap `shots[].keyframe` di YAML menunjuk ke file tersebut dengan path relatif terhadap root repository, misalnya `references/VID-001/shot-01.jpg`.
- **`analysis.md`** adalah laporan untuk manusia, **berdasarkan `analysis.yaml`**, dengan storyboard di bagian atas dan **setiap gambar shot ditampilkan langsung** (inline), bukan tautan gambar saja. Lihat [contoh VID-001](references/VID-001/analysis.md).
- **`storyboard.jpg`** adalah gabungan gambar semua shot, langsung ditampilkan di bagian atas laporan Markdown. Gambar per shot tetap disimpan dan ditampilkan di setiap uraian shot.
- **`templates/video-analysis.yaml`** menjadi format data analisis baku.
- **`templates/analysis.md`** menjadi format laporan GitHub untuk semua video.
- **`rules/analysis.md`** menjelaskan prinsip analisis, sinkronisasi dua format, dan aturan penayangan gambar.

## Konvensi penamaan dan pengisian

1. ID video: `VID-001`, `VID-002`, `VID-003`, dan seterusnya.
2. ID shot: `S1`, `S2`, `S3`, dan seterusnya, tanpa nol di depan. Nama gambar: `shot-01.jpg`, `shot-02.jpg`, dst. (dua digit).
3. Satu video = satu folder di `references/` = **`analysis.yaml` + `analysis.md` + `storyboard.jpg` + gambar setiap shot**.
4. Satu shot = satu entri `shots[]` = satu keyframe `shot-NN.jpg` **yang ditampilkan langsung pada bagian shot di `analysis.md`**.
5. Gunakan `snake_case` untuk label teknis; catatan bebas boleh berbahasa Indonesia.
6. Isi hanya hal yang diamati dari video. Jika tidak diketahui, gunakan `null`; jika data bersifat perkiraan, cantumkan pada `analysis_quality` / `confidence`.
7. Pastikan `video.shot_count` sesuai jumlah entri `shots`, waktunya berurutan, dan setiap path gambar memang ada.

Untuk menganalisis video berikutnya, isi [template YAML](templates/video-analysis.yaml) ke `references/VID-002/analysis.yaml` terlebih dahulu. Simpan satu gambar untuk setiap shot (`shot-01.jpg`, `shot-02.jpg`, dst.) dan `storyboard.jpg` ke folder yang sama. Kemudian susun `references/VID-002/analysis.md` memakai [template Markdown](templates/analysis.md), **menyalin data dari YAML tanpa mengarang informasi baru**. Gambar storyboard dan seluruh gambar shot wajib tampil secara langsung di Markdown GitHub.

Jika isi YAML berubah, perbarui Markdown agar informasi tetap identik; YAML adalah sumber kebenaran utama. Tidak ada analisis audio atau prompt generatif pada tahap ini.

**Dokumen acuan:** [Aturan analisis](rules/analysis.md) · [Contoh data YAML](references/VID-001/analysis.yaml) · [Contoh laporan visual Markdown](references/VID-001/analysis.md).
