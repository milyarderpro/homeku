# Ekspor audit HOMEKU 3.1

Lanjutkan fase 4 di `audit/authoring.md`. Jika audit kerja berubah, jalankan ulang pemeriksaan dan buat kandidat dari versi terbaru. Setelah kandidat lulus, jalankan `review` lalu langsung ekspor dengan receipt yang dihasilkan.

~~~sh
python tools/audit.py review work/candidate/rumah --output work/review.md
python tools/audit.py export work/candidate/rumah --receipt work/review.md.json --output work/final
~~~

Berikan laporan, media, dan tautan unduhan ZIP `<id>-rNNNN.zip` dalam balasan yang sama. MP4 asli dipakai terpisah untuk ingest.
