# Video sumber Homeku

Unggah video MP4 ke folder `video/` pada branch `main` **sebelum** meminta ChatGPT menganalisis video tersebut.

Contoh: `video/dreamsHouse002.mp4`.

File MP4 asli disimpan sebagai sumber untuk GitHub Actions; upload MP4 saja **tidak** menyimpan hasil analisis atau memicu workflow Save. Hanya pembaruan `requests/save.json` setelah pesan persis `save now` yang mengizinkan proses penyimpanan.
