# Audit HOMEKU2.5 di ChatGPT/Gemini

Lampirkan **MP4 asli + homeku-audit-kit.zip**, satu video per chat, lalu gunakan [prompt mulai](prompts/01-audit.md). AI menjalankan helper di chat; pengguna meninjau isi dan mengunduh satu ZIP final.

1. Bootstrap memulihkan runtime/panduan lokal berhash. Baca [metode visual](visual-audit.md) dan [authoring](authoring.md).
2. Inspect dan pastikan cut nyata; prepare membuat kerangka, PTS dan baseline6FPS. Sumber≤6FPS/shot<1s native. Pendalaman10FPS/native untuk pertanyaan tertentu.
3. AI melihat frame, mengisi desain/kamera/fakta dan menyatakan viewed eksplisit. complete menghitung metadata, tanpa menebak isi.
4. check-input/draft memeriksa data sebelum render. Kandidat berisi analysis.md enam bagian, Overview satu baris, Storyboard vertikal dan kolase per shot.
5. Koreksi memakai sumber kerja/helper/cache. Seluruh snapshot terbaru ditinjau; satu persetujuan keseluruhan sebelum export.
6. Unduh ZIP <id>-rNNNN.zip **tanpa video**; taruh incoming/ lokal dan jalankan python tools/library.py ingest. MP4 asli tersedia terpisah di video/<id>.mp4 dengan hash sama.

Estimasi visual kamera sah: Dolly-In (~2×) + Pan Right (~15–20°). Tidak perlu kalibrasi/sumber eksternal; piksel opsional. Nama gaya English, penjelasan Indonesia, luas lantai rentang wajib dan detail desain lengkap. Semua moderate boleh. Camera Start awal sumber berbeda dari Overview akhir OUT.

[Authoring](authoring.md) berisi perintah prepare/mark-viewed/complete/check-input/draft/review/export yang diuji. [Panduan JSON](json-guide.md) dibaca sesuai field yang diperlukan; tidak perlu memuat semua kontrak sekaligus sebelum mengamati. Contoh normal/multi di examples/ hanya sintetik, bukan isi referensi.

Sumber2.5 → report2.2.4/media2.2.1/reader2.5; caption Start/Middle/End tebal dan waktu lebih kecil. Format2.4 tetap angka pada gerak jelas/report2.2.3/media2.2.0;2.3 tetap pengukuran wajib untuk ~×,2.2 tetap10FPS; sumber diterima tidak dikonversi. JSON satu sumber final, MD hanya renderer. Cache/session/performance/receipt di luar kandidat dan ZIP.

[Provider](providers.md), [koreksi](prompts/02-correct.md), [ekspor](prompts/03-export.md), [kontrak](../docs/contracts/package-v2-5.md), [pilot](pilots/README.md). Kelulusan tooling bukan persetujuan isi atau penyelesaian pilot nyata.

## Kamera fleksibel dan helper opsional2.5

Angka opsional per komponen, tanpa mengubah confidence. Angka tunggal default, rentang boleh; estimate_basis boleh null tanpa angka. Contoh: Dolly-Out (~1.6×) + Orbit Left + Subtle Pan Right (Ease-Out). Lihat camera-cases.md.

Jika interval gabungan belum jelas: python tools/audit.py motion-hints work/audit/session.json --shot-id shot-02. Helper memakai cache, maksimal32frame default/640px batas, tanpa verdict dan tidak mengisi viewed. OpenCV/NumPy opsional; bila tidak tersedia lanjutkan visual. Jangan memasang paket jaringan rutin di chat. Semua output helper/inventory kerja di luar ZIP.

Untuk melanjutkan session2.4 gunakan prepare --contract-version 2.4 --resume; sumber/session harus versi sama. Review2.5 memberi ringkasan fakta kerja terpisah; AI mencocokkan narasi/fakta sebelum persetujuan, tanpa review ulang sesudah ingest.
