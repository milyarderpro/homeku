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

## Pilot edh001: audit diterima; kalibrasi lintas pilot masih terbuka

[Laporan edh001](pilots/edh001/analysis.md) berasal dari video asli, bukan anotasi arsip. Durasi stream 18.4 s dengan cut pada 4.733333333, 8.3, 11.566666667 dan 15 s. Snapshot audit ulang memisahkan orbit kanan awal eksterior dari pendekatan yang meningkat, membedakan arc OUT pada living/bedroom, pan kiri kitchen dan pan kanan bathroom.

Laporan itu belum menjadi ground truth seluruh video. Pengguna telah menerima koreksi gerakan shot 02 berikut, setelah pemeriksaan ulang seluruh 107 frame asli pada indeks 142–248 (4.733333333–8.266666667 s; akhir interval shot 8.3 s):

```text
Dolly-Out (~2×) + Orbit Left + Pan Right.
```

Penerimaan awal ini khusus gerakan shot 02. Pada 22 November 2026, koreksi tersebut sudah diterapkan ke draf audit ulang format 1.1. Seluruh durasi diaudit ulang dengan 10 FPS dan pendalaman native; 461 frame unik diperiksa, termasuk seluruh shot 02/04. Setelah meninjau hasil audit ulang, pengguna menyetujui keseluruhan snapshot dan meminta ekspor final. Ekspor telah dilakukan dengan MD SHA-256 2d04d6bbd7fd35ee813ea7298322d593f195322f864dc2ca23142af57c4a260f; riwayat dan hash paket ada pada docs/edh001-re-audit.md. Persetujuan isi tidak menjadikan estimasi visual sebagai pengukuran pose fisik. Jangan menyalin gerak/angka ini ke sumber lain. Setelah koreksi pengguna dan enam pilot lintas chat selesai, bekukan contoh dengan versi/hash yang sesuai.

## Kalibrasi V2 — belum dibekukan

Riwayat penerimaan pada bagian r0001 di atas berlaku untuk format1.1. Pada implementasi V2 sebelumnya, audit baru menghasilkan audit.json2.0 dan MD/kolase2.1.2 yang kemudian diterima sebagai r0002 (catatan di bawah). Log r0001 tidak dihitung sebagai pemeriksaan V2 baru. Pada catatan historis ini enam pilot belum dijalankan; status terbaru ada di bagian hasil edh058 di bawah. kesamaan struktur fixture tidak membuktikan ketepatan visual atau ketersediaan tool pada akun ChatGPT/Gemini tertentu.

Kalibrasi memisahkan kesalahan tafsir kamera/desain, instruksi, render/media dan ingest. Catat koreksi nyata beserta versi/ID/rujukannya; jangan menyalin angka kalibrasi sebagai default sumber lain. Label gaya teknis Inggris, estimasi luas wajib, area/rute/fase dan kelengkapan detail merupakan bagian review isi V2.

### Pemeriksaan V2 edh001 pada 22 November 2026

Audit baru telah memeriksa 455 frame unik dari 552: baseline 10 FPS seluruh shot; native seluruh shot 01 (142 frame), 02 (107), 04 (103), serta ekor shot 03 (53 frame). Log dipisahkan dari r0001 dan tersimpan pada manifest snapshot r0002 yang diterima. Kelima cut dan rumusan kamera r0001 tetap didukung setelah pemeriksaan baru. Shift gaya utama ke Contemporary Modern merupakan penamaan teknis Inggris; tambahan Warm Contemporary dan pengaruh Scandinavian Contemporary tetap interpretasi dengan status/confidence/bukti pada JSON.

[Laporan review](pilots/edh001-v2-review.md) telah disetujui pengguna sebagai keseluruhan snapshot V2. Kandidat dipertahankan di audit/pilots/v2-candidates/edh001; [ZIP r0002](pilots/packages/edh001-r0002.zip) diekspor tanpa render ulang lalu di-ingest. R0002/2.0 aktif pada saat penerimaan tersebut; versi aktif berikutnya dicatat pada bagian Overview/Storyboard di bawah. Ini bukti audit lokal di Codex, bukan run pada antarmuka ChatGPT atau Gemini. Tidak ada continuous take lintas beberapa area fisik dalam edh001; dukungan multi area baru terbukti secara teknis pada fixture sampai pilot nyata tersedia.

Penerimaan V2 pada chat 22 November 2026: pengguna menyatakan “ya saya setuju” setelah laporan lengkap, storyboard dan kelima kolase ditampilkan. Snapshot `71e949c51a3ca82f0a8d22c26ad98c82c6283d8c40413b8b0a24ef99e178ca45`; ZIP `c290e7f81642498330cdb4b0b4b2ecaf2238c5074b83761bf31b08040e74c26f`. Byte sumber JSON/MD/manifest/media tidak berubah pada ekspor/ingest. Ini penerimaan edh001 saja; pada saat penerimaan tersebut enam pilot belum dijalankan dan kalibrasi lintas provider belum dibekukan.

### Workflow Overview / Storyboard2.1

Kit berikutnya menggunakan audit2.1 dan report/media2.2.0: paragraf Overview per frame, depth_direction per fase, pola turunan, Overview satu baris dan Storyboard kolase vertikal. Notasi seluruhnya satu paragraf. Penambahan data ke edh001 dilakukan sebagai kandidat revisi eksplisit yang mempertahankan fakta/gerak/tempo diterima, bukan konversi referensi aktif diam-diam. Pemeriksaan Overview tambahan dicatat terpisah dari log audit r0002; tidak mengklaim audit penuh ulang. Penerimaan r0002 tidak dianggap persetujuan r0003.

Pada 23 November 2026, kandidat edh001 r0003/2.1 dirender dengan report/media2.2.0 dan7JPEG. Lima frame Overview native (0,248,249,449,450) benar-benar dibuka kembali untuk paragraf komposisi. Rekaman r0002 dipertahankan; gabungan tetap455frame unik, bukan460. Fakta/gerak/tempo/pilihan frame diterima tetap sama; Enter pada summary shot01 diratakan menjadi satu paragraf. Pengguna kemudian menyetujui keseluruhan r0003 dengan “ya saya setuju”. Snapshot `e1572245a3cc3e88cac25409816694de5f021d2da83fbb248d5331baaee5501f` diekspor tanpa render ulang lalu di-ingest sebagai referensi aktif. ZIP r0003 berukuran 8,635,907 byte dengan SHA-256 `87fa54a8db2169e757ef5d1325fa52bb819cc71ff90d77090774a31320775db1`; replay unchanged dan check berhasil. Tidak ada audit penuh video atau run enam pilot baru pada pekerjaan ini.


## Hasil edh058 dan perbaikan sumber2.2

[Catatan dua hasil nyata](pilots/edh058-comparison.md) tersedia: Gemini dan ChatGPT, sumber2.0/report2.1.2. Sudah dibahas dengan pengguna; belum disetujui/di-ingest. Lima pilot lain belum tercatat. Ini memperbarui status historis enam pilot di atas, bukan menyatakan seluruh pilot selesai.

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
