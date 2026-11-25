# Tujuh pilot HOMEKU 3.0

Kit 3.0 telah lulus uji teknis dengan fixture. Tabel berikut mencatat tujuh video dan fokus pilotnya. Status referensi aktif mengikuti `data/registry.json`.

| Video sumber | Fokus pilot | Riwayat |
| --- | --- | --- |
| [edh001](../../video/edh001.mp4) | Alur lengkap dari awal, arah kamera, dan framing tiap shot | Data audit lama dibersihkan atas permintaan pengguna. Mulai dari r0001 dengan `supersedes: null`. |
| [edh058](../../video/edh058.mp4) | Alur dasar, wardrobe, kombinasi kamera dan tempo | Hasil ChatGPT dan Gemini terdahulu tersedia sebagai pembanding. [Catatan riwayat](edh058-comparison.md) |
| [edh013](../../video/edh013.mp4) | Bentuk organik, platform bathroom, dan durasi stream | Gunakan MP4 asli dengan kit 3.0. |
| [edh033](../../video/edh033.mp4) | Open plan, sleeping loft, dan fungsi area yang bertumpang tindih | Gunakan MP4 asli dengan kit 3.0. |
| [edh049](../../video/edh049.mp4) | Perspektif bangunan dan kitchen lengkung, serta pembedaan pan dan orbit | Gunakan MP4 asli dengan kit 3.0. |
| [edh056](../../video/edh056.mp4) | Lintasan exterior–interior, cut dan pergantian area | Gunakan MP4 asli dengan kit 3.0. |
| [dreamshome01](../../video/dreamshome01.mp4) | Pembanding arah, ritme, dan perkembangan komposisi | Gunakan MP4 asli dengan kit 3.0. |

## Pembanding rilis kamera

Enam paket pilot baru telah diperiksa secara teknis. Gunakan [pembanding kamera](camera-release-check.md) untuk uji terarah di GPT dan Gemini, termasuk kasus awal yang tertutup transisi.

## Menjalankan satu pilot

1. Buka satu chat per video. Lampirkan MP4 asli dan [kit final HOMEKU 3.0](../homeku-audit-kit.zip). Gunakan [prompt mulai](../prompts/01-audit.md).
2. Periksa kamera dan penjelasan pada kandidat yang ditampilkan. Tinjau laporan lengkap, Overview, Storyboard, serta seluruh kolase. Jika ada koreksi, gunakan [prompt koreksi](../prompts/02-correct.md).
3. Unduh ZIP yang Anda pilih dari balasan yang menampilkan laporan dan media. Jika ada koreksi, gunakan tautan ZIP dari hasil terbaru.
4. Taruh ZIP di `incoming/` dan pastikan MP4 asli tersedia di `video/<id>.mp4`. Jalankan ingest. Berikut contoh untuk edh001.

~~~sh
python tools/library.py ingest incoming/edh001-r0001.zip
~~~

Pertahankan hasil pembanding terdahulu di `audit/result/` sebagai riwayat. Mulai setiap pilot 3.0 dari MP4 asli dan catat kandidat, persetujuan keseluruhan, ekspor, dan ingest sebagai status terpisah. Pilih ChatGPT atau Gemini per video sesuai kebutuhan.

[Verifikasi tooling](../../docs/implementation-verification-single-version.md) · [Panduan audit](../README.md)
