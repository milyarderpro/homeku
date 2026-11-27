# Ekspor audit HOMEKU 3.1

Lanjutkan fase 4 di `audit/authoring.md`. Jika audit kerja berubah, jalankan ulang pemeriksaan dan buat kandidat dari versi terbaru. Setelah kandidat lulus, jalankan `review` lalu langsung ekspor dengan receipt yang dihasilkan.

~~~sh
python tools/audit.py review work/candidate/rumah --output work/review.md --session work/audit/session.json
python tools/audit.py export work/candidate/rumah --receipt work/review.md.json --output work/final --session work/audit/session.json
~~~

Berikan laporan, Overview, Storyboard, kolase, dan tautan unduhan ZIP `<id>-rNNNN.zip` dalam balasan yang sama. Ambil tautan laporan dan gambar dari checklist yang dikembalikan `review`, dan jalur ZIP dari field `package` keluaran `export`. Gunakan checklist untuk membantu pengguna menemukan perubahan. MP4 asli dipakai terpisah untuk ingest.

## Simpan ZIP pilihan ke Google Drive

Di root `HOMEKU` yang ditentukan pengguna, gunakan subfolder `Hasil Audit` sebagai tujuan. Setelah pengguna memilih ZIP di chat, unggah file ekspor tersebut dengan nama aslinya jika aksi unggah tersedia. Periksa tujuan dan nama file sebelum mengunggah. Ambil kembali byte ZIP dari Drive dan cocokkan SHA-256 dengan `package_sha256` dari `export`. Berikan tautan Drive hasil pembacaan kembali dan pertahankan unduhan di chat.

Jika sudah ada file bernama sama, pakai tautannya bila SHA-256 cocok. Laporkan konflik bila SHA-256 berbeda atau tujuan tidak bisa dipastikan. Jika aksi unggah atau pembacaan ulang tidak tersedia, laporkan langkah yang belum selesai dan sediakan unduhan ZIP di chat agar pengguna dapat menyimpannya ke Drive. Pemilihan atau transfer paket tidak menjalankan ingest.
