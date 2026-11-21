# Menyerahkan ZIP final

Upload satu file `<id>-r0001.zip` langsung di folder ini pada branch utama. ZIP berisi satu folder `<id>/` dengan laporan, manifest dan seluruh media. [Kontrak paket](../docs/contracts/package-v1.md) menjelaskan format teknis awal.

Audit/koreksi dilakukan sebelum download ZIP dari chat. Setelah upload, workflow **Library ingest** memproses seluruh ZIP yang tersedia, termasuk unggahan berdekatan. Tidak perlu mengirim perintah save now atau mengedit requests/save.json.

Hasil ada di [katalog](../catalogs/README.md). Status teknis ada di `data/ingest.json` dan artifact **homeku-ingest-report** pada Actions. ZIP gagal tidak mengganti referensi aktif; setelah diperbaiki, upload paket koreksi dan simpan perubahan. Paket dengan ID/revisi yang sudah aktif hanya dapat diubah melalui revisi berikutnya.

ZIP disimpan sebagai bukti penyerahan. Tidak ada penghapusan otomatis; kebijakan [retensi](../docs/operations.md) berlaku.
