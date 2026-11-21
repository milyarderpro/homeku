# Video sumber HOMEKU

Simpan satu MP4 kanonis per sumber sebagai `video/<id>.mp4`. ID paket mengikuti stem nama file dan mempertahankan kapitalisasinya. Manifest mengikat sumber dengan SHA-256 serta metadata stream video aktual.

Jika sumber sudah ada di sini, ZIP cukup berisi laporan, manifest dan media. Jika belum ada, chat dapat menyertakan `<id>/source.mp4` di ZIP; importer menempatkannya di sini. Tidak ada salinan MP4 kedua dalam folder referensi.

File video yang tersedia belum otomatis menjadi referensi aktif. Audit final masuk melalui [incoming/](../incoming/README.md) sesuai [kontrak paket](../docs/contracts/package-v1.md). Metadata/review lama dalam arsip tidak dipindahkan otomatis.

Alur baru tidak memakai YAML, Git blob SHA-1, requests/save.json atau perintah save now. Upload sumber juga dapat memicu retry ingest paket yang sebelumnya gagal karena sumber belum tersedia.
