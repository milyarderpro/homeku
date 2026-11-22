# Kontrak paket 2.0 — fondasi V2

Format eksplisit `manifest.contract_version = "2.0"`; 1.0/1.1 tetap memakai kontrak legacy. Implementasi fondasi tersedia; workflow chat dan pilot V2 diselesaikan pada Tahap 2.

## Isi dan otoritas

```text
<id>-r0001.zip
  <id>/
    audit.json
    analysis.md
    manifest.json
    media/storyboard.jpg
    media/shot-01.jpg
    media/shot-02.jpg
    ...
    source.mp4             # Opsional sesuai ketersediaan sumber kanonis
```

`audit.json` satu sumber isi yang ditulis AI. `analysis.md` hasil renderer untuk manusia. Manifest menyimpan metadata teknis/provenance, bukan salinan fakta desain. Tidak ada analysis.json, receipt, log kerja terpisah, motion/, JPEG frame lepas atau seluruh rangkaian frame. Setiap shot tepat satu kolase; satu storyboard per referensi.

ID mengikuti stem MP4 dan kapitalisasi aslinya. Revisi 1 memakai supersedes null; revisi berikutnya tepat +1 dan menunjuk revision/content_sha256 aktif. Paket r0001 yang telah diterima tidak diedit atau ditimpa; ZIP penyerahan lama tetap disimpan. Registry versi 1 tetap dipakai, entri V2 menambahkan contract_version dan audit_sha256; entri legacy tidak dilengkapi secara rekaan.

Sumber kanonis `video/<id>.mp4` disimpan sekali. Sertakan source.mp4 hanya jika sumber kanonis belum terbukti tersedia dengan SHA-256 yang sama. Importer tidak menyimpan salinan MP4 dalam references/. Sumber disamakan dengan ffprobe: durasi stream video, dimensi tampilan, FPS rasional dan indeks stream.

## Sumber JSON dan pemeriksaan video

[audit-v2.schema.json](audit-v2.schema.json) mengatur isi sumber; [manifest-v2.schema.json](manifest-v2.schema.json) mengatur metadata. Luas lantai wajib rentang positif min < max, diisi AI dengan estimasi visual. Basis/uncertainty tetap JSON. Semua aspek DNA legacy dipertahankan; domain, atribut, label baru, negasi, hubungan dan ketidakpastian tidak dibuang.

Shot adalah satu take kontinu sampai cut sumber; area/fungsi bukan cut. `areas` adalah identitas area fisik dengan functions dan visible_intervals global. Interval area berbeda boleh bertumpang tindih; area yang sama boleh muncul kembali pada interval terpisah. `shots[].route` hanya lintasan kamera yang benar-benar dinyatakan, boleh kosong jika kamera tetap di satu posisi. Terlihat dari kamera tidak sama dengan dimasuki kamera.

Fase kamera dan profil tempo masing-masing menutup interval shot tanpa gap/overlap. Satu fase boleh melalui banyak area, satu area boleh memuat banyak fase. Komponen simultan memakai +, fase berurutan memakai →; summary dan komponen fase harus sama. `components_parsed` diperiksa terhadap raw, tidak ditafsirkan menjadi gerak produksi. Rasio ~× bukan kecepatan; tempo eksplisit tersimpan terpisah.

Baseline tetap 10 FPS sepanjang tiap shot dengan frame native awal/akhir. Pendalaman memakai semua frame native pada rentang yang perlu, tanpa memaksa 30 FPS/interpolasi. Manifest frame_reviews memakai kontrak record 1.1: pilihan dan daftar yang benar-benar dilihat, mode/rentang/reason. Validator memeriksa PTS, batas dan kelengkapan deklarasi; tidak dapat membuktikan kebenaran penglihatan auditor. Sampling yang baru diekstrak tidak otomatis dianggap sudah dilihat.

## Pilihan media dan bukti

Auditor menentukan `panels` dan `overviews` dalam audit.json. Setiap pilihan mempunyai ID unik, shot_id, area_ids, indeks native, PTS, role, label dan reason. Awal/akhir harus frame asli tepat di batas shot. Normal: tepat tiga pilihan start/middle/end, tengah memakai PTS terdekat titik tengah, tiga kolom. Multi area: jumlah dinamis minimal cukup, kronologis, tanpa frame berulang; dapat beberapa baris. Storyboard memakai seluruh overview menurut urutan sumber, tepat satu baris. Overview biasanya awal IN/akhir OUT; alasan pilihan tersimpan tanpa JPEG overview mandiri.

Manifest media berisi path/hash/dimensi dan panels sekali. Panel teknis menunjuk selection_id, shot/area, frame index/PTS, scale dan bbox `[x,y,width,height]` untuk **foto saja**, bukan caption. Tidak ada crop konteks atau pembesaran generatif; default panel mempertahankan dimensi asli. Skala turun hanya lewat konfigurasi eksplisit. Header dan caption terang/kontras berada di luar foto. JPEG quality 60–98, scale (0,1], kolom multi 1–6; default quality 91, scale 1, kolom 4. Normal tetap tiga kolom, storyboard tetap satu baris. Batas 60 juta piksel dan dimensi JPEG 65.000 diperiksa sebelum alokasi.

Fakta/fase/profil/hubungan merujuk ID pilihan, bukan path frame sementara. Bukti tambahan yang tidak masuk kolase memakai `frame:shot-01:42`, menunjuk indeks native dalam shot; timestamp dilampirkan validator ke proyeksi. Inventaris bukti proyeksi menyimpan metadata bersama; pembaca bisa mengambil panel tanpa caption atau frame native ke folder sementara. Gambar terpilih bukan pengganti audit 10 FPS/native.

## Penyajian 2.1.2 dan istilah

Nama gaya utama, pengaruh gaya dan gaya interior ditulis menggunakan istilah bahasa Inggris; penjelasan tetap bahasa Indonesia. Auditor menyatakan identity.style_names_language = "en". Field ini wajib pada renderer 2.1.x; paket lama yang telah diterima tidak diubah. Schema memeriksa deklarasi, sedangkan nama/tafsir gaya ditulis dan diperiksa auditor. Generator tidak menerjemahkan, menebak atau mengganti nama gaya dari deskripsi bentuk rumah.

- Header kolase cukup **SHOT 03 · Kitchen** diikuti `8.30–11.57s · 3.27s` pada baris yang sama bila muat. Tidak ada daftar waktu Start/Middle/End dalam header.
- Di bawah tiap foto normal: **Start** · 8.30s, **Middle** · 9.93s, **End** · 11.53s. Label bold; timestamp regular sekitar 75% ukuran label, pada baseline yang sama. Nama area cukup pada judul.
- Multi area memakai nomor/label momen dengan timestamp kecil di bawah foto, misalnya **02 · Entrance reveal** · 6.80s. Caption panjang boleh membungkus tanpa menimpa foto. Satu shot tetap satu pengambilan.
- Header storyboard: **ID — Primary style — 18.40s — 5 shot**. Gunakan identity.primary_style, bukan nama kreatif rumah atau tafsir baru generator.
- Caption storyboard: **03 · Kitchen**, diikuti `Overview · 8.30s` dengan font waktu lebih kecil daripada nama area. Beberapa area dalam satu shot mempertahankan nomor shot sama.
- Font bold asli digunakan untuk judul/nama area/label; seluruh judul serta label area diperkecil sekitar 15% dari 2.1.0, termasuk storyboard. Ukuran tetap mempertimbangkan lebar kanvas. Caption rata kiri, ruang caption sejajar dan teks panjang membungkus di luar foto. Storyboard tetap satu baris.
- Dua desimal hanya tampilan: audit JSON, manifest PTS/frame index, bukti serta pointer tidak dibulatkan atau dimutasi. Versi terdahulu mempertahankan format lamanya.

## Snapshot dan versi renderer

Draft membuat kandidat lengkap; review menampilkan MD/media dan menghasilkan receipt di **luar** kandidat. Receipt bukan persetujuan otomatis. Setelah pengguna menyetujui keseluruhan kandidat di chat, export menerima digest snapshot dan membungkus byte yang sama. Tidak membuat ulang JPEG, MD, created_at atau manifest. Setiap perubahan file, termasuk salinan MP4 opsional, membatalkan digest. Hash sumber kanonis selalu terikat manifest. Hash isi revisi mengecualikan salinan source.mp4 opsional supaya identitas revisi tidak bergantung penempatan sumber.

Renderer/report dan media profile terbaru `2.1.2`; pasangan `2.0.0`, `2.1.0`, dan `2.1.1` tetap didukung. Hash template beku serta font regular tercatat pada manifest, ditambah bold_font_sha256 untuk 2.1.x. Report dan media harus memakai pasangan versi yang sama. Aset versi diterima tidak boleh ditimpa; renderer/template/font baru memakai registrasi versi/aset baru. Pemeriksaan MD memakai renderer versi paket. Berkas template penulisan berikutnya tidak mengubah salinan template beku yang sudah dipakai paket.

ZIP dibuka ulang, divalidasi lalu dibandingkan digest. Ekstraksi mempertahankan aturan anti traversal, symlink, duplikat, executable dan batas ZIP legacy: 2.000 file, 95 MiB/file, 256 MiB total, teks 2 MiB/file. File/media yang diizinkan diputuskan kembali oleh kontrak versi; keberadaan audit.json saja bukan deteksi V2.

Pengguna mengoreksi sebelum download ZIP. Ingest lokal `python tools/library.py ingest` melakukan validasi teknis dan memperbarui turunan; tidak ada review isi kedua atau watcher otomatis.
