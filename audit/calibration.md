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
