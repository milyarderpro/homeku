# Audit HOMEKU 3.0 di ChatGPT atau Gemini

Lampirkan MP4 asli dan `homeku-audit-kit.zip`, satu video per chat. Gunakan [prompt mulai](prompts/01-audit.md).

Gunakan workspace yang dapat menjalankan Python dan FFmpeg, membuka frame hasil ekstraksi, serta menyediakan file ZIP. Catat provider dan model yang diketahui. Jika operasi gagal, sebutkan langkah dan error yang terjadi agar audit dapat dilanjutkan dari workspace yang sesuai.

1. Ekstrak kit dan jalankan `python homeku_runtime.py --output .`. Baca [metode visual](visual-audit.md) dan [authoring](authoring.md).
2. Tentukan cut nyata, lalu jalankan prepare untuk baseline 6 FPS beserta batas native. Gunakan seluruh native untuk sumber ≤6 FPS atau shot <1 detik. Periksa lebih rapat hanya pada bagian yang masih menyisakan pertanyaan.
3. Lihat frame lalu isi desain, komposisi, kamera, tempo, dan bukti di [audit.json](json-guide.md). Nilai besaran setiap komponen gerak dan cantumkan estimasi yang wajar dari petunjuk visual. Deklarasikan viewed setelah gambar diperiksa.
4. Ikuti [checklist isi](authoring.md#periksa-isi-sebelum-memperlihatkan-kandidat), lalu jalankan `complete`, `check-input`, dan `draft`. Setelah kandidat lulus validasi, jalankan `review` dan langsung ekspor dengan receipt terbaru. Tampilkan laporan enam bagian, Overview, Storyboard, semua kolase, dan tautan ZIP tanpa MP4 dalam balasan yang sama.
5. Jika ada koreksi, perbarui audit kerja, ulangi draft dan review, lalu ekspor dan berikan tautan ZIP terbaru.
6. Periksa hasil di chat dan unduh ZIP yang Anda pilih. Taruh di `incoming/`, simpan MP4 kanonis di `video/<id>.mp4`, dan jalankan `python tools/library.py ingest`.

[Prompt koreksi](prompts/02-correct.md) · [Prompt ekspor](prompts/03-export.md) · [Kontrak paket](contracts/package.md)
