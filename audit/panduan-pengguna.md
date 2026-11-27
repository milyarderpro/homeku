# Panduan Pengguna Audit HOMEKU 3.1

Gunakan panduan ini untuk mengaudit satu video di ChatGPT, meminta koreksi, dan memilih hasil yang masuk ke pustaka HOMEKU. Setiap audit yang lulus langsung disimpan ke Google Drive. **Hasil menjadi referensi aktif setelah Anda memilih ZIP dan menjalankan ingest.**

Salin blok prompt yang sesuai, lalu ganti bagian dalam `[kurung siku]`. [Buka folder HOMEKU di Google Drive](https://drive.google.com/drive/folders/11LOGurcTdSSqbA4PDd217JNs-jzirKUA) · [Kit audit HOMEKU](https://drive.google.com/file/d/1awQO7Zy9Zw4fgZI6J2nU_63RLxjgsDv6/view)

## Audit video baru

Simpan MP4 asli di `HOMEKU/Video/`. ChatGPT mengambil `homeku-audit-kit.zip` dari root HOMEKU dan menjalankan lima fase dalam satu chat.

| Fase | Yang dilakukan auditor |
| --- | --- |
| 1. Pemetaan shot | Memastikan batas cut dan menyiapkan frame yang akan diperiksa. |
| 2. Audit kamera | Memeriksa gerakan, arah, besaran, tempo, dan Production Start jika diperlukan. |
| 3. Audit desain dan media | Menyusun laporan desain serta memilih frame untuk Overview, Storyboard, dan kolase shot. |
| 4. Validasi dan ekspor | Memeriksa audit dan media, lalu membuat ZIP final beserta SHA-256. |
| 5. Penyimpanan di Drive | Menyimpan laporan, media, dan ZIP, lalu mengunduh ulang ZIP dari Drive untuk mencocokkan SHA-256. |

Contoh isi folder hasil untuk video `dreamshome01.mp4`:

~~~text
HOMEKU/
├── homeku-audit-kit.zip
├── Video/
│   └── dreamshome01.mp4
└── Audit/
    └── dreamshome01/
        ├── dreamshome01-r0001.zip
        ├── analysis.md
        └── media/
            ├── overview.jpg
            ├── storyboard.jpg
            └── shot-01.jpg
~~~

Folder video memakai nama MP4 tanpa ekstensi. Media berisi satu kolase untuk setiap shot. Di balasan akhir, periksa laporan dan media serta status verifikasi Drive.

### Prompt audit baru

~~~text
Audit video [NAMA_VIDEO.mp4] dari folder Video di root HOMEKU berikut.
https://drive.google.com/drive/folders/11LOGurcTdSSqbA4PDd217JNs-jzirKUA

Unduh homeku-audit-kit.zip dari tautan langsung ini.
https://drive.google.com/file/d/1awQO7Zy9Zw4fgZI6J2nU_63RLxjgsDv6/view

Pulihkan runtime dan pastikan readiness lulus, lalu jalankan lima fase dalam chat ini. Setelah ekspor lulus, langsung simpan ZIP, analysis.md, dan media ke folder Audit untuk video ini. Baca kembali ZIP dari Drive dan cocokkan SHA-256. Tampilkan ringkasan shot, laporan, media, tautan unduhan ZIP, tautan folder Drive, serta status fase 5. Saya akan memilih ZIP untuk ingest setelah memeriksa hasil.
~~~

## Audit baru dengan persetujuan kamera

Gunakan dua giliran dalam chat yang sama. Pada giliran pertama, auditor memetakan shot dan menyelesaikan pemeriksaan kamera. Anda meninjau hasilnya sebelum memberi instruksi untuk melanjutkan desain, ekspor, dan penyimpanan. Jeda ini mengikuti instruksi dalam prompt.

### Prompt jalankan Fase 1 dan 2

~~~text
Audit video [NAMA_VIDEO.mp4] dari folder Video di root HOMEKU berikut.
https://drive.google.com/drive/folders/11LOGurcTdSSqbA4PDd217JNs-jzirKUA

Unduh homeku-audit-kit.zip dari tautan langsung ini.
https://drive.google.com/file/d/1awQO7Zy9Zw4fgZI6J2nU_63RLxjgsDv6/view

Pulihkan runtime, pastikan readiness lulus, lalu jalankan hanya Fase 1 dan 2. Setelah check-camera lulus, tampilkan batas tiap shot, notasi dan urutan gerakan, estimasi besaran, tempo, serta Production Start jika ada. Sertakan indeks atau waktu frame pendukung dan tunjukkan bagian yang masih meragukan.

Selesaikan pencatatan Fase 2 dan pertahankan workspace audit. Berhenti di sini dan tunggu persetujuan saya sebelum memulai Fase 3.
~~~

Jika ada temuan yang meragukan, sebutkan shot dan gerakan yang perlu diperiksa ulang sebelum Anda memberi persetujuan.

### Prompt setelah kamera disetujui

~~~text
Saya setujui hasil kamera terakhir. Lanjutkan Fase 3, 4, dan 5 di chat dan workspace yang sama. Gunakan hasil kamera yang telah disetujui. Setelah validasi dan ekspor lulus, simpan laporan, media, dan ZIP ke folder Drive video ini. Baca kembali ZIP dari Drive dan verifikasi SHA-256.
~~~

## Memilih nomor revisi

Nomor revisi mengikuti **versi yang aktif di pustaka**. Status simpan di Google Drive dan status ingest dicatat terpisah.

| Status saat meminta koreksi | Hasil berikutnya |
| --- | --- |
| `r0001` belum pernah di-ingest | Koreksi tetap memakai `r0001`. |
| `r0001` sudah aktif dan Anda meminta perubahan baru | Auditor membuat `r0002` yang terikat ke `r0001` aktif. |
| `r0002` sudah ada di Drive dan masih menunggu ingest | Gunakan ZIP `r0002` itu sebagai dasar. Koreksi tetap memakai `r0002`. |
| `r0002` sudah aktif dan Anda meminta perubahan baru | Auditor membuat `r0003` yang terikat ke `r0002` aktif. |

Pada setiap koreksi, auditor memakai folder video yang sama. Laporan, media, dan ZIP bernama sama diperbarui dengan ID Drive yang sama jika isinya berubah. File identik dilewati. Saat nomor naik, Drive mendapat ZIP dengan nama baru dan ZIP versi lama tetap tersedia. Laporan dan media terpisah menampilkan hasil terbaru yang tersimpan di folder itu.

## Audit ulang kamera di chat yang sama

Gunakan chat lama jika workspace audit masih bisa dipakai. Tulis **kamera semua shot** untuk memeriksa ulang seluruh kamera, atau sebutkan nomor shot untuk koreksi terarah. Auditor memakai MP4 dan batas shot yang sama, meninjau kembali frame yang diperlukan, lalu mengulang fase 4 dan 5. Jika Production Start berubah, auditor ikut memperbarui panel dan media yang terdampak.

### Prompt audit ulang kamera sebelum ingest di chat yang sama

~~~text
ZIP terakhir untuk video ini masih menunggu ingest. Audit ulang kamera semua shot dari MP4 asli. Periksa depth, translation, dan rotation, lalu nilai arah, besaran, tempo, dan Production Start. Pertahankan batas shot dan isi desain. Sesuaikan panel dan media jika Production Start atau keterangan kameranya berubah.

Tampilkan perubahan kamera per shot beserta bukti frame yang mendukungnya. Jika ada perubahan yang didukung bukti, validasi, ekspor dengan nomor revisi yang sama, lalu perbarui hasil di folder Drive yang sama dan verifikasi SHA-256 ZIP.
~~~

Untuk koreksi satu shot, ganti kalimat kedua dengan permintaan seperti `Audit ulang kamera Shot 05. Ukur ulang rasio Dolly-In dan periksa apakah Pan Right terlihat sebagai komponen tersendiri.` Untuk koreksi desain, sebutkan shot atau area dan detail desain yang ingin diperiksa.

## Audit ulang kamera di chat baru

Berikan nama MP4 asli, tautan ZIP yang persis ingin dikoreksi, dan status ingest. Auditor menggunakan `audit.json` dari ZIP sebagai dasar, menyiapkan workspace dengan batas cut yang sama bila workspace lama tidak tersedia, dan memeriksa frame yang diperlukan untuk audit serta validasi sesi baru.

### Prompt audit ulang kamera sebelum ingest di chat baru

~~~text
Root HOMEKU untuk MP4 dan hasil audit:
https://drive.google.com/drive/folders/11LOGurcTdSSqbA4PDd217JNs-jzirKUA

Unduh homeku-audit-kit.zip dari tautan langsung ini, lalu pastikan readiness lulus.
https://drive.google.com/file/d/1awQO7Zy9Zw4fgZI6J2nU_63RLxjgsDv6/view

MP4 asli di folder Video adalah [NAMA_VIDEO.mp4]. Paket dasar saya adalah [TAUTAN_ZIP_DASAR]. Paket ini masih menunggu ingest. Pertahankan ID audit, nomor revisi, batas shot, dan isi desain. Audit ulang kamera semua shot dari MP4 asli. Periksa gerakan, arah, besaran, tempo, serta Production Start dan sesuaikan panel atau media yang terdampak.

Tampilkan perubahan per shot. Jika ada perubahan yang didukung bukti, validasi, ekspor, dan simpan hasil ke folder Drive yang sama. Verifikasi SHA-256 ZIP setelah membacanya kembali dari Drive.
~~~

## Verifikasi kamera sebelum memperbarui ZIP

Gunakan alur ini untuk mendapat pemeriksaan kedua atas **kamera semua shot** ketika ZIP masih menunggu ingest. Mulai di chat baru agar auditor menilai frame sumber terlebih dahulu. Setelah membandingkan hasilnya dengan ZIP, auditor menunggu persetujuan Anda. Jika hasil lama terkonfirmasi, laporan verifikasi di chat sudah cukup.

### Prompt verifikasi kamera dari MP4 asli

~~~text
Verifikasi kamera semua shot pada [NAMA_VIDEO.mp4] dari folder Video di root HOMEKU berikut.
https://drive.google.com/drive/folders/11LOGurcTdSSqbA4PDd217JNs-jzirKUA

Unduh homeku-audit-kit.zip dari tautan langsung ini.
https://drive.google.com/file/d/1awQO7Zy9Zw4fgZI6J2nU_63RLxjgsDv6/view

Pastikan readiness lulus dan gunakan ZIP [TAUTAN_ZIP_DASAR] sebagai dasar. ZIP ini masih menunggu ingest. Cocokkan SHA-256 MP4 dengan manifest ZIP. Pakai batas shot dari paket untuk menyiapkan pemeriksaan dan laporkan jika ada dugaan masalah pada cut.

Nilai kamera dari frame MP4 asli sebelum membaca kesimpulan kamera di ZIP. Periksa urutan fase, depth, translation, rotation, arah, besaran, tempo, dan Production Start. Jika bukti belum jelas, periksa frame native tambahan. Untuk memeriksa estimasi ~×, ukur dimensi bagian yang sama pada dua frame dan catat indeks frame dan hasilnya dalam piksel.

Bandingkan penilaianmu dengan audit lama. Tampilkan hasil per shot, meliputi notasi lama, temuan baru, bukti frame, dan usulan koreksi. Sebutkan bagian yang masih meragukan. Pertahankan batas shot dan isi desain. Berhenti setelah laporan verifikasi dan tunggu persetujuan saya sebelum memperbarui audit atau file di Drive.
~~~

### Prompt terapkan koreksi yang disetujui

~~~text
Saya setujui koreksi kamera [SEBUTKAN SHOT ATAU TEMUAN]. Terapkan koreksi itu dan sesuaikan panel serta media yang terdampak. ZIP dasar masih menunggu ingest. Validasi dan ekspor dengan nomor revisi yang sama, lalu perbarui hasil di folder Drive yang sama. Baca kembali ZIP dari Drive dan verifikasi SHA-256.
~~~

## Koreksi setelah versi sebelumnya aktif

Ambil `revision` dan `content_sha256` dari entri ID audit yang aktif di `data/registry.json`. Auditor memakai kedua nilai itu untuk menghubungkan paket baru ke versi aktif. Contohnya, revisi aktif `1` menghasilkan `r0002`. Jika `r0002` sudah dibuat tetapi belum di-ingest, sebutkan tautan ZIP `r0002` sebagai paket dasar dan tetap berikan kedua nilai dari `r0001` aktif.

### Prompt koreksi setelah ingest di chat lama atau baru

~~~text
Root HOMEKU untuk MP4 dan hasil audit:
https://drive.google.com/drive/folders/11LOGurcTdSSqbA4PDd217JNs-jzirKUA

Unduh homeku-audit-kit.zip dari tautan langsung ini, lalu pastikan readiness lulus.
https://drive.google.com/file/d/1awQO7Zy9Zw4fgZI6J2nU_63RLxjgsDv6/view

Nama MP4 asli di folder Video adalah [NAMA_VIDEO.mp4]. Paket dasar untuk koreksi ada di [TAUTAN_ZIP_DASAR]. Revisi yang sudah aktif di registri adalah [NOMOR_REVISI_AKTIF] dengan content_sha256 [HASH_KONTEN_AKTIF].

Audit ulang [KAMERA SEMUA SHOT ATAU BAGIAN YANG INGIN DIKOREKSI] dan pertahankan bagian lain. Gunakan revisi aktif + 1 dan ikat paket ke revisi aktif dengan data registri di atas. Tampilkan perubahan, validasi, lalu simpan hasil ke folder Drive video yang sama. Baca kembali ZIP dari Drive dan verifikasi SHA-256. Saya akan memeriksa ZIP baru sebelum memilihnya untuk ingest.
~~~

## Ingest batch dari Google Drive

Perintah ini dijalankan ketika Anda siap memeriksa hasil yang akan dimasukkan ke pustaka. Untuk penggunaan pertama, aktifkan Drive API pada proyek Google Cloud yang Anda gunakan, siapkan klien OAuth bertipe Desktop app, lalu simpan JSON klien di `~/.config/homeku/google-oauth-client.json`. Jika menggunakan lokasi berbeda, berikan `--credentials /jalur/klien.json`. [Penyiapan OAuth desktop](https://developers.google.com/identity/protocols/oauth2/native-app)

Pasang dependensi lokal dan simpan ID folder HOMEKU satu kali. Perintah berikut memakai ID root HOMEKU yang digunakan dalam panduan ini.

~~~sh
python -m pip install -r requirements.txt -r requirements-drive.txt
mkdir -p ~/.config/homeku
printf '%s\n' '11LOGurcTdSSqbA4PDd217JNs-jzirKUA' > ~/.config/homeku/drive-root.id
~~~

Untuk memindai root lain, berikan ID melalui `--drive-root` atau variabel `HOMEKU_DRIVE_ROOT_ID`.

Saat perintah pertama dijalankan, selesaikan login di browser untuk memberi akses baca Drive. Token disimpan di `~/.config/homeku/drive-token.json` dengan akses lokal untuk pemilik. Gunakan `--token /jalur/token.json` untuk memilih lokasi token di luar repo.

Gunakan mode daftar untuk melihat paket yang sudah masuk, revisi baru, dan konflik. Untuk memilih paket dan menjalankan ingest, jalankan perintah tanpa `--list`.

~~~sh
python tools/ingest_drive.py --list
python tools/ingest_drive.py
~~~

Pada perintah kedua, ketik nomor yang dipisahkan koma, misalnya `1,3,4`, atau `semua` untuk memilih semua kandidat yang dapat diproses. Ketik `ya` untuk menyetujui batch. Tekan Enter tanpa pilihan untuk membatalkan. Jika revisi membutuhkan pendahulu, pilih juga semua revisi yang disebut dalam daftar.

Setelah konfirmasi, perintah mengunduh paket terpilih, mencocokkan MP4 kanonis, lalu menampilkan jumlah yang berhasil, sudah masuk, tertunda, atau gagal. Periksa alasan pada nama ZIP yang tertunda atau gagal. Setelah memperbaiki sumber atau paketnya, jalankan perintah lagi. Paket yang sudah masuk akan dilewati. Jika ZIP di Drive berubah setelah persetujuan, pindai dan setujui versi terbaru. Satu pemanggilan berakhir setelah batch selesai.

## Memasukkan ZIP yang sudah disetujui ke pustaka

1. Pastikan laporan dan media sesuai, lalu unduh ZIP yang Anda pilih.
2. Taruh ZIP dengan nama kanonis di `incoming/`. Pastikan MP4 kanonis yang sesuai tersedia di `video/<id>.mp4`.
3. Jalankan ingest dari root repo untuk **satu ZIP yang dipilih**. Contoh:

~~~sh
python tools/library.py ingest incoming/dreamshome01-r0001.zip
~~~

Jika meminta bantuan Codex, gunakan prompt ini:

~~~text
Saya memilih [NAMA_ZIP] dari [TAUTAN_ZIP_DRIVE] untuk di-ingest ke pustaka HOMEKU. Verifikasi paket terhadap MP4 kanonis, ingest hanya ZIP tersebut, lalu laporkan ID dan revisi yang menjadi aktif.
~~~

## Melanjutkan penyimpanan Drive yang terputus

Jika fase 4 sudah lulus, lanjutkan dari ZIP yang sama. Gunakan chat audit yang masih menyimpan workspace dan catatan transfer.

~~~text
Lanjutkan fase 5 dari ZIP yang sudah diekspor di chat ini. Pakai folder Drive dan catatan transfer yang sama. Verifikasi file yang sudah ada, selesaikan file yang tertunda, lalu baca kembali ZIP dan cocokkan SHA-256. Laporkan langkah yang masih tertunda jika verifikasi belum selesai.
~~~

[Alur teknis audit](authoring.md) · [Prosedur penyimpanan Drive](prompts/03-export.md) · [Kontrak paket dan revisi](contracts/package.md)
