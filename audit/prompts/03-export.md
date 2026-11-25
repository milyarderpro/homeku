# Ekspor audit HOMEKU 3.0

Setelah kandidat terbaru lulus validasi, jalankan `review` untuk menghasilkan receipt, lalu langsung ekspor snapshot tersebut.

~~~sh
python tools/audit.py review work/candidate/rumah --output work/review.md
python tools/audit.py export work/candidate/rumah --receipt work/review.md.json --output work/final
~~~

Berikan tautan unduhan ZIP `<id>-rNNNN.zip` bersama laporan dan media dalam balasan yang sama. ZIP berisi audit, laporan, manifest, serta JPEG terdaftar. MP4 asli tetap sebagai sumber terpisah untuk ingest lokal.
