# Ekspor audit HOMEKU 3.0

Jalankan prompt ini sesudah saya menyetujui keseluruhan laporan dan media pada kandidat terbaru di chat. Gunakan receipt dari review snapshot tersebut.

~~~sh
python tools/audit.py export work/candidate/rumah --receipt work/review.md.json --output work/final
~~~

Berikan satu ZIP final `<id>-rNNNN.zip` dengan byte kandidat yang sudah ditinjau. ZIP berisi audit, laporan, manifest, serta JPEG terdaftar. MP4 asli tetap sebagai sumber terpisah untuk ingest lokal.
