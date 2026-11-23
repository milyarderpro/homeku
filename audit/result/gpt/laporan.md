## **Evaluasi waktu pengerjaan audit HOMEKU&#x20;**`edh058`

**Kesimpulan sementara dari timestamp dan riwayat eksekusi: bagian yang paling banyak menyita waktu adalah penyusunan&#x20;**`audit.json`**, pencocokan bukti, dan pemeriksaan kandidat.** Analisis kamera menjadi pekerjaan berat berikutnya, terutama karena seluruh enam shot diperiksa lagi pada 10 FPS.

Saya menemukan jejak file dari **23 November 2026, pukul 13.30–14.11 WIB**, tetapi tidak ada profil waktu yang secara otomatis mencatat durasi aktif setiap tahap. Karena itu, selang waktu antartimestamp tidak boleh dianggap seluruhnya sebagai waktu komputasi.

### **Rekonstruksi berdasarkan file nyata**

| Waktu WIB   | Aktivitas yang teridentifikasi                                |
| ----------- | ------------------------------------------------------------- |
| 13.30–13.31 | Sumber MP4, bootstrap, deteksi cut, timeline                  |
| 13.33–13.35 | Baseline 6 FPS, termasuk pengambilan ulang keenam shot        |
| 13.37–13.38 | Pendalaman 10 FPS keenam shot                                 |
| 13.40–13.48 | Perbandingan shot, frame native midpoint, dan grid pengukuran |
| 13.48–13.57 | Jeda sebelum tersimpannya skrip penyusun audit                |
| 13.57–13.59 | `audit.json`, draft kandidat, dan review                      |
| 13.59–14.08 | Jeda sebelum pembaruan artefak kandidat dan audit-info        |
| 14.09–14.11 | Pemeriksaan ZIP yang dibuka ulang dan paket final             |

Dua selang terbesar yang tampak pada jejak file adalah **13.48.52–13.57.06** (8 menit 14 detik) dan **13.59.12–14.08.39** (9 menit 27 detik). Keduanya bukan pengukuran durasi aktif; saya tidak bisa menentukan berapa banyak waktu digunakan untuk berpikir, menulis, memvalidasi, atau menunggu eksekusi.

## **1. Ekstraksi dan pemeriksaan frame**

Pemeriksaan mencakup 597 frame sumber, lima hard cut, dan enam shot.

| Tahap                                 | Jumlah frame yang tercatat dilihat |
| ------------------------------------- | ---------------------------------- |
| Baseline 6 FPS                        | 126                                |
| Pendalaman 10 FPS                     | 205                                |
| Native midpoint                       | 30                                 |
| Total peninjauan (termasuk duplikasi) | 361                                |
| Frame native unik                     | 299                                |

**Ada pekerjaan yang diulang.** Sampling baseline pertama menghasilkan beberapa batas frame yang tidak tepat. Contohnya, shot 01 berhenti pada F157, padahal frame terakhir shot itu F158; shot 04 mulai F347, padahal seharusnya F346.

Saya kemudian mengambil ulang baseline enam shot dengan batas PTS yang diperbaiki. Upaya menggunakan ulang direktori sampling lama ditolak oleh helper, sehingga diperlukan direktori baru `baseline-v2-shot-*`.

Ekstraksi frame sendiri berlangsung relatif singkat menurut timestamp. Pekerjaan yang lebih panjang adalah melihat kolase dan memeriksa kecukupan cakupan.

## **2. Analisis kamera dan pengukuran piksel**

Ini merupakan **bagian analitis paling berat** sebelum penulisan data.

Pekerjaan yang tercatat mencakup pemeriksaan oklusi, paralaks, pembesaran objek, translasi, kemungkinan rotasi, dan tempo. Saya juga menjalankan pencocokan fitur OpenCV SIFT dengan estimasi transformasi RANSAC.

Hasil pencocokan otomatis tidak selalu kuat: shot 01 hanya mempunyai 5 inlier dan shot 03 sebanyak 7. Karena itu saya tidak menjadikannya satu-satunya dasar estimasi gerak.

Nilai yang akhirnya ditulis ke `audit.json` menggunakan estimasi lebar jangkar pada frame native:

| Shot | Jangkar        | Awal → Akhir | Hasil      |
| ---- | -------------- | ------------ | ---------- |
| 01   | Pintu depan    | 62 → 180 px  | \~2,9× IN  |
| 02   | Lampu dinding  | 45 → 35 px   | \~1,3× OUT |
| 03   | Kompor         | 210 → 420 px | \~2,0× IN  |
| 04   | Jendela kamar  | 216 → 145 px | \~1,5× OUT |
| 05   | Jendela closet | 138 → 225 px | \~1,6× IN  |
| 06   | Tutup toilet   | 214 → 128 px | \~1,7× OUT |

Angka tersebut dicatat sebagai **pengukuran manual perkiraan pada piksel sumber**, bukan hasil kalibrasi kamera 3D. Riwayat menunjukkan pembuatan enam grid pembanding, tetapi tidak menyimpan koordinat setiap garis ukur atau durasi pengukuran masing-masing.

## **3. Penulisan&#x20;**`audit.json`**&#x20;dan pencocokan bukti**

Ini kemungkinan **penyumbang waktu terbesar secara keseluruhan**, bersama pemeriksaan hasil kandidat.

Skrip `build_audit.py` berukuran sekitar 50 KB menghasilkan:

- 6 shot dan 6 fase kamera.
- 68 fakta desain atomik.
- 18 klaim profil.
- 18 pemeriksaan kamera (depth, translation, rotation).
- 18 catatan peninjauan frame.
- Hubungan evidence, coverage, facet_roles, serta estimasi skala.

Skrip penyusun tercatat pukul **13.57.06**, sesudah grid pembanding terakhir pukul **13.48.52**. Selang sekitar 8 menit tersebut konsisten dengan pekerjaan penyusunan data, tetapi bukan bukti bahwa seluruh selang digunakan untuk mengetik JSON.

Kebutuhan mengaitkan setiap fakta dengan ID evidence dan shot, sekaligus menjaga konsistensi notasi kamera dan rasio piksel, membuat tahap ini lebih kompleks daripada sekadar membuat ringkasan visual.

## **4. Error dan pengulangan yang benar-benar tercatat**

| Kejadian                                             | Jumlah kegagalan yang terlihat | Tindakan                                          |
| ---------------------------------------------------- | ------------------------------ | ------------------------------------------------- |
| MP4 pertama tidak dapat dibaca FFprobe               | 1                              | Menggunakan unggahan baru                         |
| Sampling menolak direktori output yang sudah dipakai | 6                              | Menggunakan enam direktori baseline-v2 baru       |
| `frame_times()` menerima string, bukan `Path`        | 1                              | Mengganti argumen menjadi `Path`                  |
| Perintah `audit.py validate` tidak tersedia          | 1                              | Menggunakan perintah `review` yang didukung       |
| Kegagalan validasi schema `audit.json`               | **Tidak tercatat**             | Validasi yang terlihat menghasilkan `AUDIT VALID` |
| Kegagalan review kandidat resmi                      | **Tidak tercatat**             | Review berhasil                                   |

Penting dibedakan: **sembilan kegagalan teknis di tabel bukan sembilan kegagalan validasi audit**. Enam di antaranya adalah penolakan pemakaian ulang direktori sampling.

Tidak ada bukti bahwa saya berkali-kali gagal memvalidasi struktur JSON lalu memperbaiki error schema satu per satu. Karena itu saya tidak akan mengklaim adanya sejumlah putaran perbaikan schema.

## **5. Pembuatan kolase, laporan, dan ZIP**

Jejak eksekusi menunjukkan satu proses `draft-v2` yang berhasil, menghasilkan delapan JPEG dan `analysis.md`, dilanjutkan review resmi dengan snapshot hash yang sama.

Setelah persetujuan Anda, dilakukan satu ekspor final `export-v2`. ZIP dibuka kembali, isi 11 file dicocokkan secara byte, dan review paket hasil ekstraksi berhasil.

Timestamp:

- **13.59.12:** receipt review kandidat.
- **14.09.49:** hasil ekstraksi ulang ZIP.
- **14.09.55:** receipt review ZIP.
- **14.11.05:** timestamp ZIP final.

Ada pembaruan timestamp pada sejumlah file kandidat sekitar 14.08, tetapi riwayat tidak cukup untuk membuktikan bahwa seluruh kolase atau laporan dirender ulang. Saya tidak menghitungnya sebagai pengulangan renderer.

## **Kesimpulan**

Menurut jejak yang tersedia, urutan beban kerja yang paling masuk akal adalah **penulisan dan pencocokan bukti (3), analisis kamera (2), pemeriksaan frame (1), lalu pembuatan laporan dan ZIP (5)**. Perbaikan error (4) menambah pekerjaan, khususnya sampling ulang, tetapi tidak terbukti sebagai penyebab dominan.

Penyebab waktu tambahan yang paling jelas dan dapat dicegah adalah **pengulangan baseline karena batas frame dan penggunaan direktori output yang sama**. Namun, saya tidak mempunyai log durasi aktif yang cukup untuk menghitung berapa menit yang bisa dihemat.

Pemeriksaan ini hanya membaca riwayat dan artefak. **Audit yang disetujui serta ZIP di Google Drive tidak diubah.**