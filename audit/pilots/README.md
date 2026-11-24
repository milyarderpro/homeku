# Tujuh pilot nyata

Pustaka aktif kosong setelah reset edh001. Hasil edh058 tetap tersimpan untuk perbandingan dan belum di-ingest. Status berikut membedakan hasil nyata dari rencana pengujian.

| Video | Pelaksana/lingkungan | Status nyata | Fokus |
| --- | --- | --- | --- |
| [edh001](../../video/edh001.mp4) | Audit ulang dari awal | Data audit lama, kandidat, ZIP, cache dan riwayat ingest telah dihapus atas permintaan pengguna; belum ada audit baru | Gunakan video asli dan kit terbaru |
| [edh058](../../video/edh058.mp4) | Pengguna / ChatGPT dan Gemini | Dua hasil tersedia dan sudah dibandingkan; belum disetujui/di-ingest. [Catatan](edh058-comparison.md) | Alur dasar lengkap dan wardrobe |
| [edh013](../../video/edh013.mp4) | Pengguna / Gemini | Belum ada run terverifikasi dalam catatan ini | Bentuk organik, platform bathroom, durasi stream/container |
| [edh033](../../video/edh033.mp4) | Pengguna / ChatGPT | Belum ada run terverifikasi dalam catatan ini | Open-plan, sleeping loft dan beberapa fungsi dalam satu shot |
| [edh049](../../video/edh049.mp4) | Pengguna / Gemini | Belum ada run terverifikasi dalam catatan ini | Perspektif bangunan/kitchen lengkung dan pembedaan pan/orbit |
| [edh056](../../video/edh056.mp4) | Pengguna / ChatGPT | Belum ada run terverifikasi dalam catatan ini | Lintasan exterior–interior, cut versus segmen fungsi |
| [dreamshome01](../../video/dreamshome01.mp4) | Pengguna / Gemini | Belum ada run terverifikasi dalam catatan ini | Pembanding arah, ritme dan perkembangan komposisi |
## Memulai audit berikutnya

Gunakan [panduan audit](../README.md), MP4 sumber terpisah dan [kit terbaru](../homeku-audit-kit.zip). Default baru: sumber2.5/report2.2.4/media2.2.1, baseline6FPS dengan pendalaman10FPS/native sesuai kebutuhan. Satu chat per video; tidak wajib menggandakan seluruh video pada dua provider.

Edh001 dimulai kembali dari r0001 dengan supersedes null. Jangan menggunakan laporan, hasil kamera atau persetujuan lama sebagai audit baru. MP4 kanonis tetap di video/edh001.mp4.

Tinjau Overview, Storyboard, kolase seluruh shot dan analysis.md lengkap di chat. Setelah koreksi dan persetujuan keseluruhan snapshot, ekspor ZIP tanpa MP4. Masukkan ZIP final ke incoming/ lalu jalankan ingest; tidak ada review isi kedua.

Hasil edh058 dan pembandingnya tetap tersedia di audit/result/ serta [catatan perbandingan](edh058-comparison.md). Implementasi tooling, hasil audit, persetujuan, ekspor dan ingest adalah status terpisah.

## Reset edh001

Pada 24 November 2026, pengguna meminta seluruh data audit edh001 dibersihkan untuk memulai dari awal. Referensi aktif, r0001–r0003, kandidat, laporan review, frame/cache dan ledger ingest dihapus. Katalog/knowledge/proyeksi dibangun ulang tanpa edh001. Catatan implementasi historis bukan referensi audit aktif.
