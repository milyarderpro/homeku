# Proposal

## Why

Keenam ZIP pilot lulus validasi teknis. Pemeriksaan ulang `dreamshome01` menunjukkan bahwa dua perubahan fase terlewat, Orbit belum tercatat pada ruang tamu, dan frame awal ruang tamu masih tertutup transisi sehingga sulit dipakai sebagai acuan produksi.

## What Changes

- Tata ulang audit kamera agar auditor menentukan fase, membandingkan lintasan dan arah pandang, lalu menaksir besaran serta laju. Gunakan baseline 6 FPS dan pendalaman terarah jika bukti masih ambigu.
- Cocokkan hasil pengamatan dalam `observations` dengan `notation` sebelum review dan ekspor. Gunakan kasus eksterior, ruang tamu, dan dapur `dreamshome01` untuk menguji keputusan fase dan komponen.
- Tambahkan opsi mencatat frame awal produksi dari MP4 kanonis ketika frame native pertama tertutup transisi. Sertakan deskripsi framing singkat dan pertahankan batas shot serta panel native untuk audit sumber.
- Selaraskan panduan lokal dan GitHub dengan ZIP 3.0 serta MP4 kanonis terpisah.
- Verifikasi hasil dengan pemeriksaan terarah pada `dreamshome01`, `edh033`, dan `edh056`. Bandingkan hasil bagian kamera `dreamshome01` di GPT dan Gemini sebelum menyatakan siap rilis.

## Capabilities

### New Capabilities

- `camera-audit` — Menentukan batas fase dan membedakan lintasan kamera dari arah pandang dengan bukti temporal.
- `production-start-frame` — Menunjuk frame awal yang layak untuk produksi ketika awal shot sumber masih tertutup transisi.

### Modified Capabilities

## Impact

- Panduan visual, authoring, contoh kamera, prompt kit, dan alur konsep.
- Schema sumber dan reader, validasi waktu serta viewed, frame map, provenance, laporan, dan ekstraksi native.
- Panduan penyerahan ZIP, kit mandiri, pemeriksaan kompatibilitas paket 3.0, dan verifikasi pilot terarah.
