# Video sumber HOMEKU

Simpan MP4 asli sebagai `video/<id>.mp4`. ID audit mengikuti stem nama file, termasuk kapitalisasi. Manifest mengikat MP4 kanonis dengan SHA-256 dan metadata stream aktual.

Simpan ZIP final secara terpisah di [incoming](../incoming/README.md). Paket 3.0 memuat `audit.json`, `analysis.md`, `manifest.json`, dan JPEG terdaftar. Penambahan referensi aktif dilakukan melalui ingest setelah ZIP dan MP4 tersedia. [Kontrak paket](../audit/contracts/package.md)

Pemeriksaan native seperti `panel --native` membaca MP4 kanonis. Arsip video dapat tersedia di folder ini sebelum audit selesai dan diterima ke pustaka.
