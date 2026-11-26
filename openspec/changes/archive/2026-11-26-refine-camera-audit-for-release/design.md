# Design

## Context

Lihat [proposal](proposal.md) untuk temuan pilot. Saat ini panduan visual meminta pengamatan depth, translation, dan rotation, lalu validator memeriksa struktur fase, bukti temporal, serta sintaks notasi. Penilaian jenis dan arah gerak berasal dari auditor. Runtime mengunci panel pertama dan terakhir pada indeks native. Alur produksi memakai Camera Start dan panel Start dari sumber.

Daftar spec utama belum berisi kapabilitas tersinkron. Delta `camera-audit` memakai jalur yang sama dengan perubahan `simplify-homeku-single-version` dan menambahkan tiga persyaratan dengan nama baru. Baseline, struktur fase, dan fleksibilitas notasi mengikuti aturan yang sudah berlaku. Acuan produksi memiliki delta tersendiri karena dipakai oleh laporan, reader, dan alur konsep.

## Goals / Non-Goals

- Jadikan pemeriksaan fase, lintasan, dan arah pandang dapat diulang dengan frame yang tersedia.
- Beri framing awal produksi yang bisa dibaca dari laporan dan JSON tanpa mengubah panel bukti sumber.
- Pertahankan bentuk paket 3.0, layout media, dan alur review lalu ekspor. Klasifikasi gerak tetap tanggung jawab auditor. Validator menangani struktur, kronologi, viewed, dan integritas.

## Decisions

### 1. Satukan urutan analisis dan pemeriksaan akhir kamera

Susun `audit/visual-audit.md` sebagai satu urutan keputusan. Pilih sekitar 6–10 frame pembanding dari baseline 6 FPS sesuai durasi dan kerumitan. Jumlah pembanding adalah panduan memilih frame setelah baseline diperiksa. Gunakan frame ber-PTS sebelum dan sesudah dugaan batas fase. Pilih interval setara untuk menilai laju. Sumber ≤6 FPS dan shot <1 detik tetap memakai seluruh native. Ambil 10 FPS/native hanya di interval yang masih membutuhkan jawaban. `motion-hints` tetap bantuan opsional.

Untuk setiap kandidat fase, periksa kedalaman dan paralaks sebelum memilih label gerak lateral. Bandingkan objek dekat, jangkar jauh, dan perubahan orientasi satu bidang. Perhatikan bahwa Dolly atau perubahan skala bisa memunculkan pergeseran relatif. Gunakan sapuan latar untuk arah pandang dan perubahan sudut bidang serta oklusi untuk membedakan Orbit dan Truck. Saat dua tafsir masih masuk akal, tulis bukti pembeda atau batas observasinya secara singkat dalam `observations` yang sudah ada.

Tentukan komponen simultan, kemudian taksir skala, sudut, intensitas, dan kurva laju menurut bukti. Pakai angka tunggal untuk perkiraan yang berdekatan dan rentang bila membantu. Definisi ~× tetap mengikuti rasio skala gambar. Tempo dibaca tersendiri. Ringkas checklist `audit/authoring.md` dan prompt mulai/koreksi agar satu pemeriksaan silang frame, observasi, dan notasi dilakukan sebelum review. Gunakan `audit/camera-cases.md` untuk menunjukkan cara memutuskan fase dan arah. Pertanyaan yang masih ambigu masuk ke pemeriksaan visual, sementara parser tetap memeriksa sintaks yang sama.

### 2. Simpan acuan awal produksi sebagai data opsional

Tambahkan `shots[].composition.production_start` hanya saat awal native tertutup transisi dan ditemukan frame jernih yang layak. Field berisi `frame_index` dan `composition_summary` dalam bahasa Indonesia tentang posisi, arah, dan framing. Auditable time tetap berasal dari indeks dan PTS sumber. Gunakan nama `Production Start` untuk satu baris bersyarat di bagian Framing & Lighting. Laporan dari audit tanpa field ini tetap identik.

Tambahkan field pada schema audit dan reader. Masukkan indeks pada `referenced_frames` agar pipeline frame map dan validasi viewed yang sudah berjalan ikut mencakup acuan. Validasi indeks terhadap panel batas dan PTS native bila tersedia. Saat review memakai manifest tanpa MP4, validasi pilihan terhadap PTS tersimpan serta deklarasi viewed. Gunakan scope dan pointer field dalam pesan kesalahan. Ketika acuan merupakan panel yang sudah dipilih, frame map tetap menyimpan indeks sekali.

Proyeksi mewarisi field dari komposisi dan memasukkan pointer untuk framing dan frame. Reader bisa memakai jalur `panel <id> F<indeks> --native` dengan MP4 kanonis dan SHA-256 yang cocok. Laporan dan reader dapat menampilkan metadata acuan tanpa MP4. ZIP memuat media native yang sama. Bila sumber diproduksi dengan urutan terbalik, ikuti pemilihan awal reverse yang sudah ada.

Jelaskan cara memilih dan memeriksa frame di `audit/json-guide.md`, `audit/authoring.md`, dan `audit/concept-workflow.md`. Jika transisi diketahui dan belum ada frame jernih yang dapat dipakai, catat keterbatasan pada `notes` dan periksa sumber sebelum menyusun prompt. Untuk shot dengan awal jernih, gunakan Camera Start dan panel Start.

### 3. Gunakan kontrak yang sama pada dua panduan penyerahan

`incoming/README.md` dan `video/README.md` menunjuk `audit/contracts/package.md`. Jelaskan bahwa penyalinan lokal dilanjutkan dengan perintah ingest, sedangkan GitHub Actions hanya berjalan pada branch default sesuai trigger yang tercatat dan memeriksa ZIP yang tersedia. Gunakan aturan revisi 3.0, MP4 kanonis terpisah, dan inventaris ZIP yang sama seperti panduan utama. Uji tautan lokal yang diperbarui. Catat workflow apa adanya.

### 4. Ukur hasil dengan kasus pilot yang spesifik

Gunakan ZIP yang ada di `incoming/` sebagai pembanding baca-saja dan MP4 kanonis untuk memeriksa frame. Simpan rubrik serta bukti ringkas di `audit/pilots/` di luar kit. Saat uji GPT dan Gemini, mulai sesi baru dengan kit yang sama dan instruksi audit bagian kamera. Berikan hasil acuan setelah kedua hasil tersedia agar perbandingan mengukur keputusan auditor. Catat interval, komponen, arah, estimasi, dan pendalaman yang dipakai. Gunakan temuan berikut sebagai titik pembanding, dengan angka sebagai estimasi visual.

| Kasus | Pembanding |
| --- | --- |
| `dreamshome01` Shot 01 | Orbit Right di awal, kemudian Straight Dolly-In sekitar 1,6–2× menuju tangga dan teras. Nilai seberapa dini skala mulai berubah sebelum memakai Pure. |
| `dreamshome01` Shot 02 | Dolly-Out sekitar 1,75× + Orbit Right + Pan Left. F184 pada 6,13 detik sebagai Start native dan F194 pada 6,47 detik sebagai contoh frame produksi jernih. |
| `dreamshome01` Shot 03 | Straight Dolly-In, lalu Dolly-In + Strong Pan Right sekitar 25°. Wastafel relatif terpusat selama sekitar dua detik pertama shot. |
| `dreamshome01` Shot 04 | Diagonal Dolly-Out sekitar 1,75× + Gentle Pan Left. |
| `dreamshome01` Shot 05 | Dolly-In + Gentle Pan Right. Perbandingan bingkai bawah jendela F497–F600 mendukung ~2,5×. Sudut ~15° adalah estimasi visual. |
| `edh033` Shot 02 | Cek apakah pembesaran jangkar pada fase akhir mendukung Dolly-In bersama Tilt-Up. |
| `edh056` Shot 01 | Konfirmasi arah Orbit awal melalui pohon depan, fasad, dan perubahan sudut bidang. |

## Risks / Trade-offs

- **Satu aturan tanda bisa salah pada gerak gabungan** → gunakan jangkar dekat dan jauh bersama perubahan sudut bidang, lalu nilai bukti yang masih ambigu pada fase bersangkutan.
- **Acuan produksi masuk ke daftar media native** → simpan di komposisi dan frame map. Panel, Overview, dan Storyboard tetap berasal dari daftar seleksi yang ada.
- **Perubahan renderer membuat paket lama gagal validasi** → render baris tambahan hanya ketika field hadir dan uji semua format profil dan layout 3.0 yang masih dipakai.
- **Contoh pilot membocorkan jawaban saat uji ulang** → simpan rubrik dan perbandingan bernama di luar aset kit, kemudian jalankan dengan prompt yang sama di dua sesi baru.
- **ZIP di incoming terbit saat push** → kerjakan verifikasi kandidat di workspace lokal dan dokumentasikan trigger serta jalur ingest yang berlaku.

## Migration Plan

1. Perbarui panduan kamera dan persiapkan rubrik kasus. Tambahkan acuan produksi secara aditif, lalu verifikasi laporan, reader, dan paket.
2. Sinkronkan panduan penyerahan, bangun ulang kit dan keluaran pustaka melalui generator, serta jalankan pemeriksaan kompatibilitas paket yang sudah ada.
3. Verifikasi kasus terarah secara lokal. Catat perbandingan GPT dan Gemini pada konfirmasi kesiapan rilis. Revisi referensi aktif mengikuti alur ZIP eksplisit. Jika perlu kembali ke runtime sebelum dukungan field, pertahankan runtime yang bisa membaca setiap snapshot yang sudah diterima dengan acuan tersebut.
