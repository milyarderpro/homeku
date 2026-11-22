# Menyerahkan ZIP final

Untuk lokal: letakkan ZIP final di folder ini, lalu jalankan `python tools/library.py ingest`. Menyalin ZIP saja tidak menjalankan proses.

Untuk GitHub: upload satu file `<id>-r0001.zip` langsung di folder ini pada branch utama. ZIP berisi satu folder `<id>/` dengan laporan, manifest dan seluruh media. [Kontrak V2](../docs/contracts/package-v2.md) dan [kontrak legacy](../docs/contracts/package-v1.md) menentukan isi sesuai versi. V2 menambahkan audit.json, MD hasil render serta kolase; paket lama tetap valid.

Audit/koreksi dilakukan sebelum download ZIP dari chat. Setelah upload, workflow **Library ingest** memproses seluruh ZIP yang tersedia, termasuk unggahan berdekatan. Tidak perlu mengirim perintah save now atau mengedit requests/save.json.

Hasil ada di [katalog](../catalogs/README.md). Status teknis ada di `data/ingest.json` dan artifact **homeku-ingest-report** pada Actions. ZIP gagal tidak mengganti referensi aktif; setelah diperbaiki, upload paket koreksi dan simpan perubahan. Paket dengan ID/revisi yang sudah aktif hanya dapat diubah melalui revisi berikutnya.

ZIP disimpan sebagai bukti penyerahan. Tidak ada penghapusan otomatis; kebijakan [retensi](../docs/operations.md) berlaku.
