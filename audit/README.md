# Audit HOMEKU2.4 di ChatGPT/Gemini

Lampirkan **MP4 asli + homeku-audit-kit.zip**, satu video per chat, lalu gunakan [prompt mulai](prompts/01-audit.md). AI menjalankan helper di chat; pengguna meninjau isi dan mengunduh satu ZIP final.

1. Bootstrap memulihkan runtime/panduan lokal berhash. Baca [metode visual](visual-audit.md) dan [authoring](authoring.md).
2. Inspect dan pastikan cut nyata; prepare membuat kerangka, PTS dan baseline6FPS. Sumber≤6FPS/shot<1s native. Pendalaman10FPS/native untuk pertanyaan tertentu.
3. AI melihat frame, mengisi desain/kamera/fakta dan menyatakan viewed eksplisit. complete menghitung metadata, tanpa menebak isi.
4. check-input/draft memeriksa data sebelum render. Kandidat berisi analysis.md enam bagian, Overview satu baris, Storyboard vertikal dan kolase per shot.
5. Koreksi memakai sumber kerja/helper/cache. Seluruh snapshot terbaru ditinjau; satu persetujuan keseluruhan sebelum export.
6. Unduh ZIP <id>-rNNNN.zip **tanpa video**; taruh incoming/ lokal dan jalankan python tools/library.py ingest. MP4 asli tersedia terpisah di video/<id>.mp4 dengan hash sama.

Estimasi visual kamera sah: Dolly-In (~2×) + Pan Right (~15–20°). Tidak perlu kalibrasi/sumber eksternal; piksel opsional. Nama gaya English, penjelasan Indonesia, luas lantai rentang wajib dan detail desain lengkap. Semua moderate boleh. Camera Start awal sumber berbeda dari Overview akhir OUT.

[Authoring](authoring.md) berisi perintah prepare/mark-viewed/complete/check-input/draft/review/export yang diuji. [Panduan JSON](json-guide.md) dibaca sesuai field yang diperlukan; tidak perlu memuat semua kontrak sekaligus sebelum mengamati. Contoh normal/multi di examples/ hanya sintetik, bukan isi referensi.

Sumber2.4 → report2.2.3/media2.2.0/reader2.4; layout/font/caption tetap. Format2.3 tetap pengukuran wajib untuk ~×,2.2 tetap10FPS; sumber diterima tidak dikonversi. JSON satu sumber final, MD hanya renderer. Cache/session/performance/receipt di luar kandidat dan ZIP.

[Provider](providers.md), [koreksi](prompts/02-correct.md), [ekspor](prompts/03-export.md), [kontrak](../docs/contracts/package-v2-4.md), [pilot](pilots/README.md). Kelulusan tooling bukan persetujuan isi atau penyelesaian pilot nyata.
