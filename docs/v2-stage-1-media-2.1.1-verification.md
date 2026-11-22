# Verifikasi Tampilan Tahap 1 — 2.1.1

Tanggal: 22 November 2026. **Selesai. Tahap 2 tidak dijalankan.**

**Koreksi terbaru:** [tampilan 2.1.2](v2-stage-1-media-verification.md) mengembalikan timestamp kecil ke bawah foto sesuai contoh pengguna. Isi di bawah adalah riwayat 2.1.1, bukan format terbaru.

Menindaklanjuti [tampilan 2.1.0](v2-stage-1-media-2.1-verification.md), seluruh judul/nama area media diperkecil sekitar 15%. Pada kolase, semua waktu dipindahkan ke blok di samping judul; caption di bawah foto hanya label.

## Tampilan akhir

```text
SHOT 03 · Kitchen    8.30–11.57s · 3.27s
                    Start 8.30s · Middle 9.93s · End 11.53s
```

- Judul tetap bold; font waktu regular sekitar 75% ukuran judul.
- Rentang/durasi serta timestamp setiap panel berada di sisi kanan judul. Blok membungkus dalam kolom kanan bila panjang, termasuk untuk multi area dan tata letak satu kolom.
- Caption foto normal hanya Start/Middle/End; multi area memakai nomor/label momen. Timestamp tidak ditampilkan ulang di bawah foto.
- Header storyboard dan label nama area ikut diperkecil 15%; header tetap ID — Primary style — durasi — jumlah shot. Timestamp overview storyboard tetap bersama area masing-masing.
- Foto, pilihan frame, indeks/PTS, bukti, presisi JSON serta data audit tidak berubah. MD tetap menyertakan waktu pada urutan panel agar mudah ditelusuri.

## Versi dan pemeriksaan

Report/media terbaru 2.1.1; kontrak sumber/reader tetap 2.0. Template 2.1.1 didaftarkan terpisah. Implementasi media 2.1.0 dibekukan pada tools/homeku/media_v2_1.py; dukungan 2.0.0/2.1.0 beserta template/font tetap tersedia. Tidak ada perubahan otomatis pada paket yang telah diterima.

| Pemeriksaan aktual | Hasil |
| --- | --- |
| Tes terarah media/report | 24 tes lulus |
| `python -m unittest discover -s tests -t . -v` | **99 tes lulus**, 152,477 detik |
| `python tools/library.py check` | Lulus: 1 referensi, 5 shot |
| `python tools/build_audit_kit.py --check` | Lulus: 23 file, 818.856 byte |
| `git diff --check` | Lulus |
| Referensi/aset/workflow yang dilindungi | 38 file identik dengan baseline |
| Kandidat 2.1.0 yang dibuat sebelum perubahan | Tetap valid dan digest seluruh snapshot sama |

Tes mencakup waktu seluruh panel di sebelah judul dan sebelum foto, caption tanpa timestamp, rasio ukuran font, judul/storyboard 15% lebih kecil, teks panjang tanpa overlap foto, tata letak satu kolom, caption storyboard lebar, serta validasi/ekspor/ingest versi lama dan baru. Pengujian dilakukan pada fixture terisolasi, bukan audit video baru.

## Preview lokal

Lima kolase dan satu storyboard dibuat ulang dari pilihan frame edh001 r0001 yang sudah tersedia. Galeri berada pada `.homeku/previews/edh001-v2.1.1-layout/README.md`. Dimensi kolase 2260×1542, storyboard 3750×1588; enam JPEG berjumlah 4.901.924 byte. Jumlah file tidak dijadikan klaim penghematan ukuran.

Preview memakai label tampilan Inggris yang sama dengan preview 2.1.0, bukan penetapan gaya V2 baru. Referensi, video, registry serta ZIP edh001 r0001 tetap utuh. Prompt/protokol/provider dan pilot Tahap 2 tidak diubah. Kit hanya diperbarui pada dependensi teknis versi renderer.
