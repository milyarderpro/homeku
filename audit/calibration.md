# Contoh notasi dan bahan kalibrasi

Contoh berikut menunjukkan sintaks, bukan label yang harus disalin ke setiap video:

```text
Orbit Right (~15°–20°) →
Accelerating Dolly-In (~2×) toward teak entrance door.
```

```text
Dolly-In (~1.3×) +
Orbit Left + strong Pan Right (~35°).
```

```text
Dolly-In (~2×) +
gentle Pan Right (~15°).
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

## Pilot edh001: audit diterima; kalibrasi lintas pilot masih terbuka

[Laporan edh001](pilots/edh001/analysis.md) berasal dari video asli, bukan anotasi arsip. Durasi stream 18.4 s dengan cut pada 4.733333333, 8.3, 11.566666667 dan 15 s. Snapshot audit ulang memisahkan orbit kanan awal eksterior dari pendekatan yang meningkat, membedakan arc OUT pada living/bedroom, pan kiri kitchen dan pan kanan bathroom.

Laporan itu belum menjadi ground truth seluruh video. Pengguna telah menerima koreksi gerakan shot 02 berikut, setelah pemeriksaan ulang seluruh 107 frame asli pada indeks 142–248 (4.733333333–8.266666667 s; akhir interval shot 8.3 s):

```text
Dolly-Out (~2×) + Orbit Left + Pan Right.
```

Penerimaan awal ini khusus gerakan shot 02. Pada 22 November 2026, koreksi tersebut sudah diterapkan ke draf audit ulang format 1.1. Seluruh durasi diaudit ulang dengan 10 FPS dan pendalaman native; 461 frame unik diperiksa, termasuk seluruh shot 02/04. Setelah meninjau hasil audit ulang, pengguna menyetujui keseluruhan snapshot dan meminta ekspor final. Ekspor telah dilakukan dengan MD SHA-256 2d04d6bbd7fd35ee813ea7298322d593f195322f864dc2ca23142af57c4a260f; riwayat dan hash paket ada pada docs/edh001-re-audit.md. Persetujuan isi tidak menjadikan estimasi visual sebagai pengukuran pose fisik. Jangan menyalin gerak/angka ini ke sumber lain. Setelah koreksi pengguna dan enam pilot lintas chat selesai, bekukan contoh dengan versi/hash yang sesuai.

## Kalibrasi V2 — belum dibekukan

Riwayat penerimaan di atas hanya berlaku untuk edh001 r0001/format 1.1. Tahap 2 mengaudit ulang sumber secara nyata, mengisi audit.json 2.0, merender MD/kolase 2.1.2 dan meminta persetujuan snapshot lengkap yang baru sebelum r0002. Log lama tidak dihitung sebagai pemeriksaan V2 baru. Enam pilot pengguna belum dijalankan; kesamaan struktur fixture tidak membuktikan ketepatan visual atau ketersediaan tool pada akun ChatGPT/Gemini tertentu.

Kalibrasi memisahkan kesalahan tafsir kamera/desain, instruksi, render/media dan ingest. Catat koreksi nyata beserta versi/ID/rujukannya; jangan menyalin angka kalibrasi sebagai default sumber lain. Label gaya teknis Inggris, estimasi luas wajib, area/rute/fase dan kelengkapan detail merupakan bagian review isi V2.

### Pemeriksaan V2 edh001 pada 22 November 2026

Audit baru telah memeriksa 455 frame unik dari 552: baseline 10 FPS seluruh shot; native seluruh shot 01 (142 frame), 02 (107), 04 (103), serta ekor shot 03 (53 frame). Log dipisahkan dari r0001 dan tersimpan pada manifest snapshot r0002 yang diterima. Kelima cut dan rumusan kamera r0001 tetap didukung setelah pemeriksaan baru. Shift gaya utama ke Contemporary Modern merupakan penamaan teknis Inggris; tambahan Warm Contemporary dan pengaruh Scandinavian Contemporary tetap interpretasi dengan status/confidence/bukti pada JSON.

[Laporan review](pilots/edh001-v2-review.md) telah disetujui pengguna sebagai keseluruhan snapshot V2. Kandidat dipertahankan di audit/pilots/v2-candidates/edh001; [ZIP r0002](pilots/packages/edh001-r0002.zip) diekspor tanpa render ulang lalu di-ingest. [Referensi aktif](../references/edh001/analysis.md) kini r0002/2.0. Ini bukti audit lokal di Codex, bukan run pada antarmuka ChatGPT atau Gemini. Tidak ada continuous take lintas beberapa area fisik dalam edh001; dukungan multi area baru terbukti secara teknis pada fixture sampai pilot nyata tersedia.

Penerimaan V2 pada chat 22 November 2026: pengguna menyatakan “ya saya setuju” setelah laporan lengkap, storyboard dan kelima kolase ditampilkan. Snapshot `71e949c51a3ca82f0a8d22c26ad98c82c6283d8c40413b8b0a24ef99e178ca45`; ZIP `c290e7f81642498330cdb4b0b4b2ecaf2238c5074b83761bf31b08040e74c26f`. Byte sumber JSON/MD/manifest/media tidak berubah pada ekspor/ingest. Ini penerimaan edh001 saja; enam pilot pengguna tetap belum dijalankan dan kalibrasi lintas provider belum dibekukan.
