# Menyerahkan ZIP final HOMEKU 3.1

Letakkan ZIP yang sudah dipilih dari chat di folder ini. Nama paket mengikuti `<id>-rNNNN.zip`. ZIP memuat satu folder `<id>/` berisi `audit.json`, `analysis.md`, `manifest.json`, serta JPEG kolase setiap shot, Overview, dan Storyboard di `media/`. Simpan MP4 kanonis secara terpisah di `video/<id>.mp4`. [Kontrak paket](../audit/contracts/package.md) · [Panduan MP4](../video/README.md)

## Ingest lokal

Setelah MP4 dan ZIP tersedia, jalankan perintah berikut dari root repo. Gunakan `python tools/library.py ingest` untuk memindai seluruh ZIP di folder ini.

~~~sh
python tools/library.py ingest incoming/rumah-r0001.zip
~~~

## Ingest di GitHub

Workflow [Library ingest](../.github/workflows/library-ingest.yml) memindai ZIP yang tersedia pada branch default ketika dipicu oleh push pada path yang tercantum, termasuk `incoming/*.zip` dan `video/*.mp4`. Workflow juga bisa dijalankan manual pada branch default.

Referensi baru memakai r0001 dengan `supersedes` bernilai null. Untuk memperbarui referensi aktif, gunakan revisi berikutnya dan isi `supersedes` dengan revisi serta hash snapshot aktif. Hasil ingest yang berhasil masuk [katalog](../catalogs/README.md). Status teknis tercatat di `data/ingest.json` dan artifact **homeku-ingest-report** di Actions.
