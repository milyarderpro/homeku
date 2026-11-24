# Contoh notasi dan bahan kalibrasi

Contoh berikut menunjukkan sintaks, bukan label yang harus disalin ke setiap video:

```text
Orbit Right (~15°–20°) → Accelerating Dolly-In (~2×) toward teak entrance door.
```

```text
Dolly-In (~1.3×) + Orbit Left + strong Pan Right (~35°).
```

```text
Dolly-In (~2×) + gentle Pan Right (~15°).
```

Pan/orbit tunggal, gerakan lain, fase Static dan Uncertain tetap sah. Angka/material pada contoh tidak menjadi default. Interpretasi hanya ditulis bila didukung sumber; batasnya dicatat terpisah agar ringkasan tetap ringkas.

## Kasus pembeda

| Kasus | Cara membaca |
| --- | --- |
| Dua shot dengan framing sama, satu menempuh perubahan dalam 2 s dan satu dalam 6 s | Perubahan per waktu berbeda; keduanya dapat smooth tetapi temponya berbeda |
| Ukuran objek membesar tanpa parallax yang jelas | Cukup untuk menyatakan perubahan skala; dolly fisik versus zoom belum tentu terpisah |
| Kamera mundur dan membuka seluruh area | Gambaran area biasanya di akhir; gambar awal sumber tetap lebih dekat |
| Objek bergeser ke kanan layar | Belum membuktikan Pan Right; periksa rotasi pandangan dan translasi/parallax |
| Satu lintasan melewati exterior, entry, living dan kitchen tanpa cut | Fungsi bertambah tetapi tidak otomatis menjadi empat shot |
| Enclosure shower, laundry tower dan dua bukaan berbeda | Catat hubungan serta konfigurasi ini; jangan mengganti dengan bathroom generik |

## Status kalibrasi

Data audit dan contoh hasil edh001 telah dihapus atas permintaan pengguna. Video sumber dipertahankan untuk audit baru; hasil lama tidak menjadi acuan isi audit ulang. Kalibrasi membedakan tafsir kamera/desain, instruksi, render/media dan ingest.

## Hasil edh058 dan perbaikan sumber2.2

[Catatan dua hasil nyata](pilots/edh058-comparison.md) tersedia: Gemini dan ChatGPT, sumber2.0/report2.1.2. Sudah dibahas dengan pengguna; belum disetujui/di-ingest. Lima pilot lain belum tercatat; edh001 menunggu audit ulang setelah reset. Seluruh pilot belum dinyatakan selesai.

Gunakan kasus positif/negatif berikut ketika memeriksa sumber baru:
- Skala small terpisah dari penjelasan; satu klaim per nama pengaruh gaya. Jangan menyatukan English Country Cottage dan Mediterranean Cottage sebagai satu value.
- Kaca pintu rectangular/grid tidak otomatis arch; bentuk shutter dan pendant harus diperiksa native. Footboard tidak otomatis bench. Catatan ini titik pemeriksaan, bukan isi yang disalin ke video lain.
- Smooth bukan slow. Bandingkan perubahan framing per waktu sebelum memberi tempo; jangan membuat kuota semua shot harus berbeda.
- IN/OUT dapat jelas sementara pan/orbit/truck gabungan masih ambigu. Nyatakan batas bila bukti belum memisahkan, jangan memaksakan label provider mana pun.
- Log1FPS tidak memenuhi baseline10FPS; satu frame tidak membuktikan gerak; narasi panjang bukan pengganti fakta dan pointer lengkap.
- MD selalu renderer enam bagian. ZIP2.2 tanpa source.mp4; sumber tetap lampiran terpisah.

Kasus teknis menjadi tes regresi terisolasi. Tidak ada audit ulang video atau pembekuan ground truth visual baru pada implementasi2.2.

## Metode2.3 sesudah perbandingan2.2 edh058

Catatan sebelumnya tentang dua hasil2.0 adalah riwayat. Dua hasil terbaru2.2 ada di result/gemini/ dan result/gpt/; hash/temuan/status pada pilots/edh058-comparison.md. GPT melewatkan OUT living/bathroom ketika memilih Pan-only. Semua enam moderate Gemini sesuai penilaian pengguna dan tidak dianggap cacat distribusi tempo.

Metode inti sekarang visual-audit.md: depth dahulu, tiga tes pembanding untuk gerak lateral/rotasi, baru simpulan gabungan dan serialisasi. Baseline sumber2.3=6FPS, targeted10/native; format2.2 tetap10. Rasio OUT=awal/akhir >1 dengan anchor utuh. Saran ini memperbaiki sistem, bukan mengesahkan angka/label seluruh output Gemini. Pilot2.3 belum dijalankan; tidak ada ground truth baru dari fixture.

## Estimasi visual dan efisiensi2.4

Hasil edh058 terbaru sumber2.3/report2.2.2 tersedia dan valid menurut kontraknya; hash/status diperbarui pada pilots/edh058-comparison.md. Pengguna menerima estimasi sudut berbasis asumsi wajar. Laporan waktu menunjukkan penulisan data dan pengulangan validasi sebagai beban utama Gemini, bukan pengukuran piksel semata.

Sumber2.4 mengizinkan estimasi visual ~×/~° tanpa kalibrasi; scale_measurement opsional. Bagian jelas tetap punya perkiraan angka, bagian ambigu mempunyai alasan khusus. Metadata PTS/parser/summary/log dibantu prepare/complete, viewed eksplisit. Pendalaman tetap terarah dan preflight sebelum render. Tooling/fixture/benchmark tidak menjadi run atau persetujuan audit2.4.

## Lanjutan kamera2.5 — 24 November 2026

Dua hasil edh058 sumber2.4 kini tersedia/diperiksa, MD serta8JPEG sesuai renderer; belum disetujui/di-ingest. Pemeriksaan visual tambahan hanya18frame, bukan audit seluruh baseline. Laporan waktu provider bukan benchmark terkontrol. Implementasi kamera2.5 melanjutkan plan audit-camera-implementation-plan.md; run2.5 pengguna belum dijalankan. Status historis di atas berlaku pada saat dicatat.

Tooling2.5 kini selesai:214tes lulus tanpa skip, kit4file/90resource, caption baru dan parser angka opsional. Lihat docs/audit-camera-verification.md. Run provider2.5 tetap belum dijalankan.
