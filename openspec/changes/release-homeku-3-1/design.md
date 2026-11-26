# Design

## Context

Worktree rilis 3.1 menjalankan empat fase dan pemeriksaan kamera per shot. Pada pilot awal `dreamshome01`, paket ChatGPT dan Gemini lolos validasi terhadap MP4 kanonis, tetapi keduanya menggabungkan Orbit dan Dolly-In sejak awal Shot 01. Pemilihan panel yang saat itu dikunci ke indeks native tertentu membawa blur transisi ke kolase. Indeks Gemini juga belum memetakan `dining-area` ke `dining`. Hasil pemeriksaan pilot terbaru tercatat pada bagian verifikasi.

`data/registry.json` mendaftarkan `edh001` revisi 2 sebagai satu-satunya referensi aktif. `incoming/edh001-r0001.zip` memakai format 3.0. `engine.py` memeriksa versi registry sebelum ingest normal, sehingga mengganti konstanta dapat membuat pustaka aktif gagal dibuka bila kode dan datanya diterbitkan terpisah.

## Goals / Non-Goals

Cakupan teknis meliputi audit dan ekspor, distribusi kit, serta penerbitan pustaka. Plugin dan workflow produksi berada di luar cakupan. Audit memakai bukti visual untuk penilaian kamera. CLI memeriksa struktur, bukti yang dirujuk, dan konsistensi hasil yang sudah diperiksa.

## Decisions

### 1. Satu prompt, empat fase

| Fase | Panduan | Hasil |
|---|---|---|
| 1. Pemetaan shot | `audit/authoring.md` | Jalankan `prepare`, periksa batas cut dan tetapkan satu shot per take kontinu. Siapkan frame baseline dan `audit.json` untuk sumber tersebut. |
| 2. Audit kamera | `audit/visual-audit.md` dan `audit/camera-cases.md` | Periksa fase, Orbit dan Pan, qualifier, besaran, dan tempo per shot. Periksa Production Start bila dipilih. Jalankan `check-camera` dan ringkas hasilnya di chat. |
| 3. Audit desain dan kurasi media | `audit/design-audit.md` dan `audit/json-guide.md` | Isi profil desain, kronologi area, detail, framing, dan rencana panel serta Overview dalam JSON yang sama. |
| 4. Validasi dan ekspor | `audit/authoring.md` dan `audit/contracts/package.md` | Jalankan `complete → check-input → draft → review → export`. Setelah lulus, berikan ZIP di chat yang sama. |

`audit/authoring.md` memandu perpindahan fase. Pindahkan aturan desain yang tersebar ke panduan desain dan tautkan bagian terkait. Prompt awal menjalankan keempat fase berurutan. Prompt koreksi dan ekspor membantu melanjutkan sesi yang sudah ada. Pengguna tetap memilih sendiri ZIP yang akan masuk pustaka.

Pakai frame baseline yang dihasilkan `prepare` pada 6 FPS dengan batas native, termasuk aturan seluruh frame native untuk shot pendek dan video dengan FPS rendah. Bandingkan frame pada interval sepadan. Gunakan 10 FPS atau native untuk menjawab pertanyaan visual tertentu. Kamera dan desain memakai cache yang sama. Referensi yang tercatat sebagai dilihat harus sudah benar-benar diperiksa.

### 2. Pemeriksaan kamera per shot

Tambahkan `check-camera` pada CLI. Gunakan kembali validasi kamera dan timeline yang relevan dari `audit_quality.py` dan `models.py`. Gunakan satu normalisasi untuk hasil kamera yang diperiksa dan hasil akhir. Relasi kamera dengan data area yang baru diisi pada fase desain diperiksa kembali pada validasi lengkap.

Simpan status pemeriksaan di `session.json` melalui `audit_session.py`. Ikat ke versi, ID referensi, fingerprint MP4, daftar shot dan batas cut. Simpan hash serialisasi kanonis untuk blok kamera setiap shot, termasuk notasi, fase, tempo dan observasi, serta untuk Production Start. Perlakukan pilihan Production Start yang kosong sebagai keadaan yang bisa diperiksa. Data kamera tetap bersumber dari `audit.json`. Verifikasi status pada `complete`, `check-input`, dan `draft` melalui CLI dan jalur runtime yang dipakai CLI. Kandidat dan ZIP mengikuti pemeriksaan receipt serta aturan paket yang sudah berlaku.

Jika perubahan disengaja, gunakan koreksi shot dan jalankan `check-camera --shot-id …` setelah memeriksa kembali bukti terkait. Perbarui status shot itu dan tampilkan shot serta bagian yang berubah bila ada ketidakcocokan. Pemeriksaan umum atas sesi yang sudah dikunci wajib mendeteksi perubahan yang belum diperiksa ulang. Perubahan sumber atau pemetaan cut memerlukan pemetaan dan pemeriksaan kamera kembali. Penulisan status sesi menggunakan operasi atomik dan verifikasi batas yang sama saat melanjutkan.

### 3. Satu kontrak aktif dan satu pasangan aset renderer

Naikkan `FORMAT_VERSION` dan kontrak versi yang mengikutinya, termasuk audit, manifest, format render manifest, reader dan indeks. Versi struktur internal yang punya semantik independen dipertahankan. Buat pesan penolakan yang jelas untuk paket, kandidat, dan sesi 3.0 melalui jalur aktif. Wajibkan `house_type` dan `palette` di kontrak yang memuat profil. Pertahankan data yang disetujui dalam profil, layout panel dinamis, Overview, Storyboard, dan aturan alamat Production Start.

Konsolidasikan isi `analysis-profile.md` dan `media-aligned.json` sebagai `analysis.md` dan `media.json` yang kanonis. Hapus aset rangkap dan cabang lama pada `render_assets.py`, `reporting.py`, dan `media.py`. Perbarui inventaris kit, fingerprint generator, fixture, contoh, kontrak dan dokumentasi operasional. Pastikan kit tetap berjalan mandiri ketika diekstrak dengan MP4 di luar repo.

Delta OpenSpec yang telah selesai masih mencatat aturan lama. `simplify-homeku-single-version` menetapkan 3.0 sebagai format tunggal, sedangkan `standardize-design-profile`, `standardize-audit-media`, dan `refine-camera-audit-for-release` memuat skenario penerimaan materi 3.0. Kontrak rilis ini menggantikan aturan kompatibilitas tersebut. Saat sinkronisasi spesifikasi berikutnya, selaraskan skenario yang bertentangan dengan keputusan rilis ini.

### 4. Pemilihan panel jernih

Di fase 3, pilih indeks native yang sudah dilihat dalam `panels[].frame_index`. Untuk shot biasa, pilih Start jernih pertama dan End jernih terakhir. Hitung midpoint sebagai `(start_s + end_s) / 2` dari batas shot sumber, lalu pilih frame native jernih dengan PTS terdekat ke titik itu di antara panel Start dan End. Hindari frame dengan blur transisi, motion blur berlebihan, atau artefak transisi. Dalami hanya interval terkait bila perlu. Jika ada Production Start, gunakan indeks itu sebagai panel Start.

Selaraskan `audit/json-guide.md`, panduan authoring dan desain, serta kontrak media. Ubah `tools/homeku/authoring.py` agar `complete` mempertahankan pilihan auditor dan menyamakan panel Start dengan Production Start pada shot biasa. Gunakan batas dan midpoint dari sesi sebagai acuan saat memilih. `models.py` dan `package_manifest.py` memeriksa cakupan shot, urutan panel, dan kesamaan Start dengan Production Start bila berlaku. Bukti viewed mengikuti kontrak paket. Validasi Production Start merujuk pada batas native shot dan PTS sumber, terpisah dari indeks panel Start. Kamera, durasi, batas native dan pilihan Overview tetap bersumber dari data masing-masing. Renderer menggunakan pilihan panel dalam sumber audit.

### 5. Pemeriksaan awal dan akhir komponen kamera

Di `audit/visual-audit.md` dan `audit/camera-cases.md`, sertakan contoh cara membandingkan beberapa frame awal dan frame di sekitar perubahan sebelum menulis gerakan simultan. Periksa perubahan skala, paralaks, dan orientasi bidang per interval. Gunakan bagian awal `dreamshome01` Shot 01 sebagai acuan regresi untuk membedakan Orbit Right, kemunculan Dolly-In yang bertumpang tindih, dan pendekatan akhir ke teras. Isi notasi mengikuti bukti pada video yang diaudit. Pendalaman tetap terbatas pada pertanyaan visual terkait.

### 6. Kosakata filter area

Gunakan satu normalisasi untuk label dan fungsi area, alias taksonomi, dan kueri area maupun rute yang memakai kosakata area. Normalisasi merapikan kapitalisasi, spasi, dan tanda hubung antar kata. Gunakan inventaris label serta fungsi dari semua hasil pilot yang tersedia untuk menambah alias yang benar-benar setara di `data/taxonomy.json`. Pertahankan makna yang berbeda dan label asli di `audit.json`, pembaca, serta laporan. Pencarian memakai fungsi yang dinyatakan dalam audit. Variasi ejaan istilah baru dapat dicocokkan melalui normalisasi. Uji benturan alias, pencarian gabungan lintas fungsi, dan kesesuaian hasil antarprovider.

### 7. Verifikasi pilot setelah perbaikan

Gunakan hasil Gemini `dreamshome01` sebagai dasar perbaikan terarah. Periksa urutan fase dan frame End jernih Shot 01, panel Start Shot 02 pada F192, serta skala Dolly-In Shot 05. Pertahankan pemeriksaan komponen simultan Shot 02 dan peralihan Pan Right Shot 03. Bila kamera dikoreksi, jalankan pemeriksaan ulang shot terkait. Buat ulang kandidat, kolase, Storyboard dan ZIP, lalu periksa bahwa perubahan panel mempertahankan batas, durasi, dan kamera yang telah diverifikasi.

Verifikasi pilot dapat memakai hasil fase 2 yang tersedia atau pemeriksaan ulang lokal dari ZIP dan MP4 kanonis. Cocokkan hasil `check-camera` dengan `audit.json`, `analysis.md`, dan media. Catat hasil lokal sebagai bukti pemeriksaan keluaran. Riwayat urutan langkah di chat provider memerlukan bukti dari sesi asal bila menjadi tujuan pengujian.

Kedua ZIP terbaru `dreamshome01` diperiksa ulang secara lokal terhadap MP4. Kedua versi mempertahankan tiga fase pada Shot 01 serta menyediakan Shot 03 di filter `kitchen` dan `dining`. Gemini menangkap dua fase pada Shot 03 dan menjadi dasar kandidat final. Kandidat koreksi memakai End F177 pada Shot 01, Production Start F192 pada Shot 02, dan estimasi Dolly-In ~2.5× pada Shot 05. Panel Middle untuk Shot 01 dan 02 memakai F92 dan F236 pada kedua ekspor koreksi. Bukti lokal menutup verifikasi pilot ini.

## Risks / Trade-offs

- **Kamera dikoreksi setelah fase 2** → Periksa ulang shot yang berubah dan buat draf dari data yang sudah divalidasi ulang. Perubahan setelah draf memakai jalur review dan ekspor dari snapshot baru.
- **Klaim validasi dianggap bukti akurasi** → Bandingkan langsung dengan frame dan nilai hasil pilot penuh sebelum rilis.
- **Keluaran pustaka terbit sebagian** → Jalankan dry run dan semua pemeriksaan dari snapshot staging lengkap. Cek kembali predecessor serta fingerprint sumber sebelum publikasi.
- **Dua implementasi kembali bertumpuk** → Gunakan helper yang ada, simpan satu status sesi, dan pertahankan satu pasangan aset. Siapkan prosedur cutover sekali pakai dengan kontrak 3.1 sebagai jalur operasi setelah rilis.

## Migration Plan

1. Bangun dan uji kit 3.1 serta prosedur cutover dalam workspace terisolasi. Uji jalur sukses, paket stale, dan rollback dengan fixture. Branch aktif tetap menyediakan snapshot yang sudah terbit sampai pengganti valid.
2. Setelah verifikasi pilot selesai, audit kembali MP4 kanonis `video/edh001.mp4`. Kandidat `edh001-r0003.zip` sudah diekspor dan divalidasi untuk tinjauan pengguna. `supersedes` mengikat `revision` dan `content_sha256` dari entri aktif di registry. Jika entri aktif berubah, periksa kembali kandidat terhadap predecessor terkini sebelum penggantian.
3. Mulai cutover setelah pengguna memilih ZIP pengganti. Dalam workspace penerbitan, verifikasi ZIP sebagai paket 3.1 terhadap sumber kanonis dan catatan predecessor yang diambil dari registry aktif. Gunakan validasi dan generator yang sama dengan ingest. Gunakan metadata predecessor untuk menjaga riwayat revisi. Perbarui paket aktif, registry, ledger, incoming, katalog, Knowledge dan indeks di staging. Keluarkan ZIP 3.0 dari jalur incoming operasional. Riwayat Git, arsip, hasil pilot lama di luar jalur aktif, dan MP4 sumber tersimpan sesuai fungsinya.
4. Jalankan pemeriksaan rilis dan terbitkan satu snapshot kode dan data melalui jalur Git dan Actions. Jika pengganti belum lengkap atau validasi gagal, hentikan publikasi dan perbaiki staging. Bila diperlukan rollback setelah publikasi, pulihkan satu snapshot kode dan data yang koheren.
