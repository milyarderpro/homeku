# Design

## Context

`prepare` mengikat MP4, cut, indeks frame, dan catatan sampling ke `session.json`. `motion-hints` sudah memakai optical flow untuk statistik gambar 2D. `update-shot` menggabungkan objek kerja dan mengganti array yang dipasok. `review` saat ini menyalin laporan dengan tautan ke media kandidat, membuat inventaris fakta, dan menerbitkan receipt. `performance.jsonl` mencakup sebagian operasi runtime, sedangkan benchmark fixture mengukur perintah lokal. Lihat [proposal](proposal.md) untuk motivasi perubahan.

## Goals / Non-Goals

Batas desain berada pada CLI dan workspace audit, panduan penyerahan, serta verifikasi rilis kit. Isi yang dipakai ingest mengikuti kontrak paket 3.1. `audit.json` menjadi sumber isi audit, dan receipt di luar kandidat mengikat file snapshot yang ditinjau.

## Decisions

### Gunakan sesi yang sama untuk pencatatan dan pemulihan

Tambahkan event fase mulai dan selesai ke `performance.jsonl` di workspace. Penanda eksplisit mencakup kegiatan di luar CLI seperti memeriksa frame atau menulis narasi. Penanda fase pemetaan dapat dimulai sebelum `prepare` di workspace yang sama. Durasi antarpenanda berasal dari waktu berlalu, sementara durasi satu percobaan perintah diukur dengan jam monotonik di proses itu.

Pasangkan event awal dan terminal lewat ID percobaan, dengan hasil berhasil atau gagal, ruang lingkup shot jika ada, serta hash kandidat saat diketahui. Hitung percobaan dari log dan sajikan ringkasan yang mengenali baris lama serta percobaan terputus. Bedakan `check-input` dari preflight internal dalam `draft` agar satu pemanggilan tidak dihitung dua kali untuk operasi yang sama. Log `ok: false` sebagai hasil gagal, meski fungsi mengembalikan respons normal. Jalur CLI dalam panduan memberi `review` dan `export` konteks workspace yang sama melalui `--session`. Ekspor memeriksa metadata sesi dan ikatan receipt yang tersedia sebelum mencatat percobaan. Kegagalan kandidat atau receipt tercatat setelah workspace sesi ditetapkan. Jalur tanpa opsi sesi tetap tersedia untuk ekspor offline.

Tambahkan pemeriksaan kesiapan ringan yang memeriksa Python, Pillow, jsonschema, FFmpeg, ffprobe, OpenCV, dan NumPy dan menguji satu frame sumber serta akses tulis. Gunakan kembali verifikasi sesi, himpunan selected/viewed, dan digesti checkpoint kamera untuk status lanjutan. Status menampilkan frame baseline yang belum dilihat di semua pass shot dan, secara terpisah, ID pass serta indeks yang deklarasinya belum lengkap. Status membandingkan kandidat dengan hash receipt, mengecek identitas sesi bila dicantumkan di receipt, dan menyebut artefak yang belum tersedia. Simpan deklarasi visual melalui perintah yang sudah berwenang mencatatnya.

### Pisahkan usulan cut dari konfirmasi batas native

Pertahankan keluaran dasar `inspect` dan tambahkan mode opsional yang menyaring perubahan gambar mendadak dengan satu pembacaan video berurutan. Gunakan perbedaan gambar untuk memberi kandidat dan ambil frame pembanding melalui jalur ekstraksi kanonis. Batasi jumlah kandidat dan ukuran pratinjau agar ringkasan dapat diperiksa di chat. Gunakan indeks tampilan dan PTS dari stream kanonis, termasuk untuk video dengan jarak PTS yang berbeda. Auditor mengonfirmasi cut dan meneruskan daftar indeks ke `prepare`, termasuk daftar kosong untuk satu take.

### Tambahkan pengukuran lokal pada jalur OpenCV yang ada

Gunakan `motion-hints` untuk memilih interval yang perlu ditinjau. Untuk pengukuran lokal, terima dua ujung jangkar pada frame awal dan lacak kedua titik melalui frame berurutan dalam interval shot. Gunakan kembali prinsip validasi tracking maju-mundur. Jika OpenCV bekerja pada gambar yang diperkecil, petakan titik kembali ke koordinat native sebelum mengukur. Sajikan titik usulan dan hasil pada keluaran workspace yang dapat diperiksa lewat chat. Format ini cocok dengan OpenCV headless.

Hitung jarak dan rasio dari dua pasang titik yang dikonfirmasi. Terima pasangan titik manual dengan format yang sama, termasuk saat blur atau oklusi. OpenCV dan NumPy wajib tersedia sebelum audit dimulai. Ukuran jangkar menggambarkan proyeksi 2D. Auditor membandingkan perspektif, oklusi, dan pergeseran relatif dekat/jauh sebelum menetapkan komponen kamera, estimasi, dan batas fase. Bukti yang dirujuk mengikuti aturan `viewed` yang ada.

Sebelum menyimpan notasi, auditor menilai komponen, arah, lintasan, intensitas, skala atau sudut, serta profil laju sesuai relevansi. Auditor mengupayakan besaran tiap komponen secara independen dan memilih angka tunggal atau rentang dengan pembulatan wajar bila didukung frame. Bila pendalaman visual belum memungkinkan estimasi yang wajar, auditor mencatat alasan spesifik di `observations`. Statistik OpenCV dan kelulusan validasi teknis mendukung proses ini. Simpulan gerak berasal dari pemeriksaan visual.

### Terapkan perubahan terarah ke sumber kerja

Perluas jalur authoring yang terikat ke sesi. Gunakan target fase yang menyebut shot dan entri, serta target fakta yang menyebut shot, blok desain, kategori, dan entri. Tampilkan target yang diubah dalam hasil operasi. Gunakan kembali validasi struktur dan bukti yang relevan dengan perubahan, perbolehkan kerangka yang masih dikerjakan, dan simpan perubahan secara atomik. Untuk penyuntingan dengan indeks entri atau blok desain, cocokkan hash audit kerja dengan byte yang dibaca auditor saat memilih indeks. Periksa cakupan fase dan bukti override terhadap visibilitas yang tersedia pada checkpoint kamera. Jika koreksi notasi menggeser komponen yang dirujuk override, minta array override yang sesuai sebelum menyimpan. Gunakan checkpoint per shot untuk pemeriksaan ulang. Pertahankan `update-shot` sebagai jalur patch yang sudah tersedia.

### Turunkan lembar dan riwayat dari snapshot kandidat

Bangun lembar Markdown dari kandidat yang lulus validasi, dengan tautan ke laporan dan JPEG dari snapshot yang sama. Tampilkan pemeriksaan teknis yang dijalankan dan kotak centang visual yang bisa dikerjakan auditor. Simpan data pembanding minimal di luar kandidat, terikat ke sesi dan hash snapshot. Bandingkan notasi, frame dan cakupan bukti, asosiasi komponen override, pilihan dan cakupan panel, serta hash media dengan snapshot berbeda yang terakhir direview dalam sesi. Laporkan cakupan pembanding yang tersedia bila riwayat lama belum memuat seluruh bidang. Review dengan sesi memvalidasi metadata dan PTS native serta mencocokkan deklarasi bukti kandidat dengan sesi tersebut sebelum menerbitkan receipt. Simpan salinan snapshot dan tautan laporan serta media di workspace agar hasil lama tetap terbuka setelah `draft` mengganti kandidat. Saat nama ZIP kanonis sudah dipakai oleh snapshot berbeda, simpan ZIP baru pada jalur sesuai hash snapshot.

### Letakkan transfer Google Drive pada alur chat

Panduan mulai menerima tautan root HOMEKU dan nama MP4, lalu mengambil byte kit dari root dan video asli dari subfolder Video. CLI memproses file di workspace chat dan ekspor menghasilkan ZIP yang ditampilkan bersama laporan serta media. Setelah pengguna memilih ZIP, ChatGPT memakai aksi unggah Drive ke subfolder Hasil Audit bila tersedia. Gunakan nama kanonis dan verifikasi file tujuan dengan membaca ulang byte serta mencocokkan SHA-256. Bila nama sudah dipakai, pakai tautan lama jika hash cocok dan laporkan konflik jika berbeda. Simpan tautan unduhan chat sebagai jalur penyerahan saat unggah atau verifikasi belum tersedia.

## Risks / Trade-offs

- **Perubahan tajam di dalam satu take** → Tampilkan frame sebelum dan sesudah dugaan cut agar keputusan dapat diperiksa pada sumber.
- **Tracking bergeser atau jangkar berubah rupa** → Tampilkan posisi titik dan status kecocokan. Pasangan manual tetap tersedia, dan auditor menilai perspektif sebelum menyimpulkan gerak.
- **Sesi terputus atau penanda fase terlewat** → Sajikan fase atau percobaan yang belum selesai secara eksplisit. Gunakan pasangan lengkap untuk komparasi durasi.
- **Kandidat yang sama direview berkali-kali** → Pilih snapshot pembanding yang sesuai dengan sesi, dan tangani review ulang hash yang sama sebagai snapshot yang sama.
- **Kemampuan Drive bervariasi menurut sesi ChatGPT** → Uji unggah dan baca kembali pada workspace target. Catat hasil jalur otomatis dan unduhan chat secara terpisah.

## Migration Plan

Instrumentasikan log lebih dulu, lalu tambahkan bantuan sesi, kamera, pengisian, dan review. Pengambilan baseline sebelum optimasi dilewati sesuai arahan pengguna. Catat waktu dan percobaan yang benar-benar diukur, dan bandingkan hanya bila tersedia baseline. Catat terpisah pilot ChatGPT untuk build terdahulu, hasil transfer ZIP yang dipilih, serta 167 tes lokal pada build terbaru. Uji coba ChatGPT dengan kit terbaru diperlukan untuk menilai dampak panduan yang disempurnakan terhadap kelengkapan notasi. Untuk rollback distribusi tooling, gunakan kit sebelumnya yang sudah diverifikasi pada audit baru.
