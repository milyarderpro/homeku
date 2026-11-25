# Design

## Context

`tools/homeku/render_assets.py` mengambil judul dari `areas[].label`. `tools/homeku/media.py` memakai label yang sama untuk Overview dan memakai label momen dari selection. Kolase multi-area saat ini mengambil batas `columns` dari manifest. Storyboard memakai lebar blok terbesar lalu memusatkan blok lain. `verify_renderer` saat ini hanya mengenali satu hash layout.

Pemeriksaan baca-saja atas `docs/runpilot/pilot/edh033-r0002.zip` menunjukkan empat label area campuran dan shot interior yang mereferensikan dua area fisik. `docs/runpilot/pilot/edh056-r0001.zip` mencatat panel Shot 01 pada frame 0, 70, 190, 220, dan 379. Lebar kolasenya 3.030 px dengan pengaturan empat kolom. Tiga blok lain selebar 2.280 px dimulai pada x=375. Kedua ZIP memakai layout 3.0 awal. MP4 kanonis tersedia untuk keduanya. Lihat [proposal](proposal.md) dan [spesifikasi](specs/audit-media-presentation/spec.md).

## Goals / Non-Goals

**Goals**

- Penamaan dibuat sekali di audit dan diteruskan ke semua tampilan yang menyebut area atau panel.
- Jumlah panel mengikuti pilihan auditor. Ukuran blok dan perataan Storyboard tetap konsisten pada susunan panel yang berbeda.
- Validator, cache, dan crop menggunakan geometri yang sama dengan JPEG hasil render.

**Non-Goals**

- Perubahan shot, isi baris notasi kamera, geometri frame sumber, Overview wide, dan teks naratif Indonesia berada di luar perubahan visual ini.
- Pembuatan preview bersifat terisolasi. Promosi pilot atau revisi referensi aktif mengikuti alur ZIP tersendiri.

## Decisions

### 1. Terapkan aturan penamaan saat pengisian audit

Gunakan `areas[].label` untuk satu nama area fisik berbahasa Inggris dengan Title Case. Simpan fungsi yang terlihat satu per entri di `areas[].functions`. Renderer meneruskan label itu. Saat satu shot memuat beberapa ID, renderer menyusun label mengikuti urutan ID dengan ` / `. `&` digunakan di dalam satu label seperti `Bathroom & Laundry`. Contoh `Open-Plan Living` mencatat fungsi living, dining, dan kitchen meski judulnya singkat.

Untuk panel multi-area, pakai label momen dari audit sebagai caption. Panduan meminta caption spesifik jika momen visual bisa dinamai, misalnya `Facade Reveal` atau `Doorway`. Pertahankan fallback `Moment N` untuk input lama. Label `Start`, `Middle`, dan `End` diturunkan seperti sekarang sesuai jenis shot. Standar Inggris juga mencakup fungsi dan nilai teknis yang dipakai filter, seperti `oblique` atau `walk-in shower`.

Perbarui panduan kosakata, petunjuk JSON, prompt mulai dan koreksi, serta checklist. Pertahankan istilah yang sudah disimpan pada snapshot awal. Tambahkan alias hanya saat maknanya ekuivalen, misalnya `Dining Area`, `dining room`, dan `ruang makan` untuk fungsi dining. Gunakan mekanisme casefold dan alias yang sudah ada. Penamaan baru tetap terbuka untuk area berbeda. Hindari perubahan jumlah area atau pengisian fakta dari judul/sinonim.

### 2. Pakai lebar blok tiga panel sebagai acuan untuk semua shot

Hitung lebar blok dari tiga sel panel nominal dan margin yang sudah dipakai oleh shot biasa. Gunakan lebar ini untuk setiap kolase shot. Susun panel dari kiri dengan margin dan jarak tetap. Untuk multi-area, cari jumlah baris minimum sesuai batas kolom dan bagi jumlah panel sedekat mungkin. Gunakan ukuran foto yang sama untuk seluruh panel dalam satu shot, dihitung dari baris terpadat. Perkecil foto secara proporsional saat diperlukan dan hindari memperbesar foto di atas skala panel yang dipilih. Baris lebih pendek dimulai pada margin kiri yang sama.

Default baru memberi kapasitas lima panel per baris. Karena itu 5 membentuk satu baris, 6 membentuk 3+3, dan 7 membentuk 4+3. Pilihan eksplisit `--columns` tetap menentukan batas maksimum pada multi-area. Simpan nilai efektif di `render.columns` dalam rentang 1–6 yang sudah diterima schema. Layout asal menafsirkan konfigurasi persis seperti saat snapshot dibuat.

Pisahkan ukuran foto dari ukuran judul shot. Pertahankan hierarki label tebal dan waktu lebih kecil di bawah foto. Pemenggalan judul panjang dan caption tetap menghormati ruang yang tersedia. Taruh waktu di kanan, termasuk saat perlu baris kedua. Gunakan `Camera:` pada layout baru. Storyboard menyusun kolase jadi dengan margin kiri bersama. Overview tetap memakai rumus lebar satu baris untuk frame wide terpilih. Terapkan pemeriksaan batas piksel, sisi, dan ukuran JPEG yang sudah ada.

### 3. Pilih layout dari fingerprint yang sudah tersimpan

Pertahankan byte `tools/assets/layouts/media.json` serta perilaku layout awal. Tambahkan aset `tools/assets/layouts/media-aligned.json` dengan fingerprint tersendiri. Pilih layout baru pada draft dan resolve `manifest.render.layout_sha256` lewat daftar kecil aset yang diketahui pada validasi. Verifikasi hash layout secara terpisah dari template laporan sehingga template dan layout lama tetap dapat dikombinasikan sesuai snapshot asal.

Pertahankan satu jalur renderer dan pisahkan keputusan geometri lama serta baru pada bagian yang memerlukannya. Satu perencanaan geometri memasok render, validasi, cache, dan koordinat bbox. Daftarkan kedua aset pada pembuat kit dan fingerprint generator. Cache yang sudah mencakup konfigurasi dan geometri akan memakai kunci baru ketika layout atau caption berubah. Pembaca crop tetap berjalan dari JPEG tersimpan dan bbox manifest.

### 4. Buat dua preview dari salinan paket asli

- Untuk `edh033-r0002.zip`, gunakan `Exterior`, `Open-Plan Living / Sleeping Loft`, `Bathroom & Laundry`, dan `Exterior` sebagai judul yang diperiksa. Tinjau frame panel tengah sebelum memilih caption yang konkret. Cek hasil di Storyboard, Overview, kolase, dan laporan.
- Untuk `edh056-r0001.zip`, pertahankan lima indeks asli Shot 01. Gunakan `Start`, `Facade Reveal`, `Doorway`, `Living & Kitchen`, dan `End`. Ukur satu baris dan perataan dengan ketiga shot biasa.
- Gunakan paket pilot dan Frame/PTS yang tercatat sebagai dasar, serta MP4 kanonis untuk render ulang. Simpan preview di workspace di luar jalur ingest dan tandai sebagai preview. Bandingkan hash kedua ZIP asli sebelum dan sesudah.

## Risks / Trade-offs

- **Naik jumlah panel membuat caption rapat** → gunakan pemenggalan sesuai lebar sel dan verifikasi keterbacaan preview pada lebar tampilan yang sama.
- **Pergantian fingerprint dapat merusak validasi paket yang sudah ada** → verifikasi kedua layout dengan geometri lama dan baru, serta tolak fingerprint yang tidak dikenal.
- **Alias yang terlalu luas mengubah hasil pencarian** → kurasi hanya padanan setara dan uji fungsi open-plan satu per satu.
- **Koordinat berubah setelah skala Storyboard** → uji crop panel dan blok dengan skala 1 dan pecahan serta pembacaan metadata tanpa video.

## Migration Plan

1. Tambahkan aturan penamaan, alias, layout baru, dan jalur kompatibilitas untuk validasi.
2. Bangun dua preview dari snapshot pilot dan verifikasi media serta tampilan. Build ulang ZIP kit dan turunan pustaka melalui generator.
3. Sebelum rilis, validasi referensi aktif serta ZIP pilot asal, cek keterbacaan preview, dan jalankan suite tes, cek pustaka, serta cek kit. Paket pilot tetap dikelola melalui keputusan ingest/revisi terpisah.
