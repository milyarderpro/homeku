# Folder MP4 sumber Homeku

Sebelum meminta ChatGPT menganalisis sebuah video, unggah **MP4 yang sama** ke **branch `main`**, langsung di dalam folder `video/`, misalnya:

```text
video/dreamsHouse002.mp4
```

- Jangan hanya mengunggah MP4 ke chat atau branch uji `actions-jpg-test`: workflow produksi hanya membaca `main/video/`.
- Simpan satu MP4 dengan **nama yang sama persis** (termasuk huruf besar/kecil) seperti `video.filename` di YAML. Runner saat ini hanya menerima `video/<nama>.mp4`, bukan subfolder `video/xxx/file.mp4`.
- ChatGPT akan mencari video berdasarkan nama, lalu membandingkan **Git blob SHA-1** dengan file upload chat bila byte lokal tersedia. Nama yang sama saja tidak menjamin isi video sama; jika belum bisa dibandingkan, sumber perlu dikonfirmasi.
- **Upload video tidak memicu proses penyimpanan analisis.** Hanya update `main/requests/save.json` setelah pesan tersendiri persis `save now` yang memicu GitHub Actions.
- MP4 tidak dihapus oleh Actions setelah hasil disimpan. Perhatikan ukuran dan riwayat Git jika menyimpan banyak video berukuran besar.

Lihat [workflow v1.2](../rules/workflow-analysis.md) dan [panduan Actions](../docs/github-actions-save.md).
