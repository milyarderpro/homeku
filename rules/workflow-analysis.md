# Homeku — Workflow Analisis Video v1.0

> **Status:** standar operasional analisis video di ChatGPT. **Repository:** `milyarderpro/homeku`. **Branch:** `main`.
>
> **Alur:** **UPLOAD → ANALYZE → REVIEW / REVISE → `save now` → SAFE SAVE → VERIFY**.

## 1. Tujuan dan pembagian aturan

File ini mengatur **proses kerja dan izin menulis ke GitHub**, termasuk beberapa chat yang menganalisis video berbeda secara paralel.

- `rules/workflow-analysis.md` (file ini): kapan melakukan analisis, review, revisi, dan penyimpanan.
- `rules/analysis.md`: apa yang harus diamati, bagaimana melakukan estimasi, dan standar kualitas analisis visual.
- `templates/video-analysis.yaml`: struktur `analysis.yaml`, sumber data utama; gunakan `schema_version` aktif (saat ini **2.1**).
- `templates/analysis.md`: format laporan visual yang diturunkan dari YAML.

**Batasan:** hanya analisis video yang diberikan; tidak membuat ide konten, prompt produksi, atau analisis audio. Jangan mengubah skema/template hanya untuk memenuhi workflow ini.

## 2. Konteks satu chat dan keadaan analisis

Satu chat menangani **maksimal satu draft analisis aktif yang belum disimpan**. Draft mencakup metadata video, data YAML, laporan yang ditampilkan di chat, storyboard, dan gambar setiap shot.

Keadaan yang digunakan:

1. **`no_draft`** — belum ada analisis yang menunggu review.
2. **`review_pending`** — analisis selesai ditampilkan, menunggu revisi atau perintah penyimpanan.
3. **`saving`** — proses validasi dan commit GitHub sedang dijalankan.
4. **`saved`** — seluruh file sudah diverifikasi di GitHub.

Keadaan ini adalah **konsep operasional percakapan**, bukan status baru dalam skema YAML. `analysis_quality.status` dan `human_verified` tetap mengikuti makna yang ditentukan aturan analisis; mengirim `save now` **tidak otomatis** mengubah status menjadi `reviewed` atau `human_verified: true`.

Jika pengguna mengirim video baru saat draft lama masih `review_pending`, jangan menggantinya diam-diam. Mintalah pengguna memilih untuk menyimpan atau mengabaikan draft lama, atau memproses video baru di chat lain. Draft dan file sementara **tidak otomatis terbagi antarchat**; untuk menyimpan, gunakan chat yang memiliki video dan hasil analisisnya.

## 3. Tahap UPLOAD dan ANALYZE

Saat pengguna mengirim video baru:

1. Baca versi terbaru empat dokumen di bagian 1 dari GitHub sebelum mulai.
2. Periksa apakah file video dapat diakses/dibaca. Catat metadata teknis yang tersedia: nama, durasi, resolusi, FPS, rasio, dan jumlah shot.
3. Identifikasi seluruh shot beserta waktu awal/akhir. Analisis tiap shot sesuai `rules/analysis.md`: scene, framing, pergerakan kamera, pencahayaan, detail arsitektur/properti/lingkungan, dan transisi.
4. Analisis gaya rumah, warna, suasana, serta `architecture.building_scale` termasuk rentang perkiraan luas m² dan tingkat keyakinannya. Estimasi visual yang masuk akal diperbolehkan; jangan menyatakan angka perkiraan sebagai ukuran pasti dan jangan memeriksa konsistensi dimensi interior-eksterior.
5. Ekstrak **tepat satu keyframe asli per shot** dalam JPEG; siapkan `storyboard.jpg` yang menggabungkan semua shot.
6. Susun draft `analysis.yaml` berdasarkan template, dan draft `analysis.md` **dari data YAML yang sama**. Semua rujukan gambar disiapkan mengikuti nama `shot-01.jpg`, `shot-02.jpg`, dst.
7. ID akhir `VID-XXX` **belum ditetapkan** pada tahap ini; gunakan label sementara `PENDING` dalam preview atau tunjukkan bahwa ID akan diberikan saat penyimpanan.

**Larangan tegas:** pada tahap upload, analyze, review, dan revise, **jangan membuat/memperbarui/menghapus file maupun commit di GitHub**. Hanya membaca repo diperbolehkan.

Jika video tidak dapat dibaca, jelaskan keterbatasan; jangan mengarang hasil analisis seolah-olah video sudah diperiksa.

## 4. Tahap REVIEW dan REVISE (di chat)

Setelah analisis, tampilkan laporan **lengkap dan nyaman ditinjau** di chat:

- metadata teknis dan ringkasan video;
- storyboard gabungan;
- gaya arsitektur, ukuran dan proporsi, rentang luas perkiraan beserta confidence;
- warna, pencahayaan, suasana, lingkungan;
- urutan scene dan tabel timeline seluruh shot;
- detail **setiap** shot beserta gambar keyframe (jika tampilan media memungkinkan), gerakan kamera, properti, transisi, dan confidence;
- ketidakpastian, status analisis, dan catatan kualitas.

Nyatakan secara jelas: **“Belum disimpan ke GitHub. Kirim `save now` untuk menyimpan hasil analisis ini.”**

Jika pengguna meminta revisi, ubah **draft aktif yang sama**, sinkronkan YAML dan laporan visual, lalu tampilkan hasil terbaru. Tidak ada penulisan GitHub sebelum perintah yang valid.

## 5. Otorisasi `save now`

**Satu-satunya pemicu penyimpanan standar** adalah pesan pengguna tersendiri yang setelah menghapus spasi awal/akhir bernilai persis `save now` (abaikan perbedaan huruf besar/kecil).

- Penyebutan kata `save now` dalam contoh, kutipan, pertanyaan, atau pesan yang memuat teks lain **bukan izin menyimpan**.
- Perintah berlaku hanya untuk **draft terbaru di chat yang sama** dan berstatus `review_pending`. Jangan mengambil draft chat lain, video lain, atau versi lama.
- Jika tidak ada draft aktif, minta video/analisis yang perlu disimpan; jangan membuat data baru.
- Jika draft sudah `saved` dan perintah diulang, laporkan tautan hasil lama bila diketahui, **jangan membuat folder duplikat**.
- `save now` adalah persetujuan untuk **menyimpan draft yang sudah ditampilkan**, bukan verifikasi bahwa seluruh pengukuran/estimasi telah diperiksa secara manual.

## 6. SAFE PARALLEL SAVE — wajib untuk beberapa chat

**Jangan mengunci ID terlalu awal.** Semua chat berbagi branch `main` dan dapat mencoba menyimpan bersamaan.

Saat perintah valid diterima:

1. **Preflight**: pastikan draft lengkap dan seluruh byte gambar keyframe serta storyboard masih tersedia. Bila tidak, berhenti; jangan menyimpan paket parsial. Jika media hilang, minta upload ulang.
2. **Ambil HEAD terbaru** dari `main` dan daftar folder `references/VID-XXX/` pada HEAD yang sama. Tentukan **ID terkecil yang masih kosong** (umumnya nomor setelah ID terbesar) dengan format `VID-001`, `VID-002`, dst. **Jangan menimpa folder yang sudah ada.**
3. **Finalisasi ID dan seluruh path** pada `analysis.yaml`, `analysis.md`, serta nama file folder berdasarkan ID terpilih. Nama gambar: `shot-01.jpg`, `shot-02.jpg`, ...; YAML memakai path root-relative `references/VID-XXX/shot-01.jpg`; Markdown memakai src relatif `shot-01.jpg`.
4. **Validasi seluruh paket** (bagian 7). Semua byte JPEG tetap utuh. Untuk API GitHub Git Data, gambar perlu dibuat sebagai **blob binary melalui encoding base64**, bukan dikirim sebagai teks biasa.
5. Buat **satu tree Git** berisi dua dokumen dan seluruh gambar yang akan disimpan, dengan base tree dari commit HEAD terpilih; kemudian buat **satu commit** dengan parent commit HEAD yang sama. **Jangan menyimpan tiap file sebagai commit terpisah.**
6. Perbarui ref `main` menggunakan pemeriksaan HEAD yang diharapkan (**compare-and-swap / expected SHA**) dan **tanpa force**. Jangan menggunakan `force push` atau menimpa commit pihak lain.
7. Jika pembaruan ref ditolak/HEAD berubah, **jangan menggunakan commit yang sudah basi**. Ambil ulang HEAD dan daftar folder, tentukan ID yang tersedia lagi, perbarui path, susun ulang tree+commit dari HEAD baru, lalu coba lagi (maksimal **3 percobaan**).
8. Jika setelah 3 percobaan tetap konflik, atau layanan GitHub mengalami kesalahan, hentikan penyimpanan dan jelaskan kegagalannya. **Jangan menyatakan sukses.** Pertahankan draft jika masih tersedia.
9. Setelah update ref berhasil, **baca kembali repository** dan pastikan semua file ada, setiap gambar dapat dirujuk, ID dan isi YAML sesuai, serta commit terlihat di branch. Hanya setelah verifikasi ini status menjadi `saved`.

**Penting:** pembuatan object blob/tree/commit di GitHub sebelum pembaruan ref tidak membuat file terlihat di branch `main`. Namun, seluruh proses write ini **hanya boleh dimulai setelah perintah `save now`**.

## 7. Checklist validasi sebelum commit

Paket akhir `references/VID-XXX/` **wajib** berisi:

```text
references/VID-XXX/
├── analysis.yaml
├── analysis.md
├── storyboard.jpg
├── shot-01.jpg
├── shot-02.jpg
└── ... (tepat satu gambar per shot)
```

Periksa seluruh hal berikut:

- Versi skema YAML sesuai `templates/video-analysis.yaml`.
- `video.id` sesuai folder `VID-XXX`; `video.shot_count` sama dengan jumlah `shots[]`.
- ID shot berurutan `shot-01`, `shot-02`, ... dan tanpa duplikasi.
- Awal/akhir shot masuk akal, berurutan, serta mencakup durasi video dengan toleransi estimasi.
- Setiap `shots[].keyframe` mengarah ke gambar JPEG yang **benar-benar disimpan**, bukan nama path kosong.
- `storyboard.jpg` ada dan merangkum seluruh shot.
- `analysis.md` memakai storyboard inline dan gambar **setiap** shot inline (`<img src="shot-01.jpg" ...>`).
- Ringkasan, scene, timeline, ukuran bangunan, rentang luas, catatan, dan confidence di Markdown konsisten dengan YAML.
- Rentang `estimated_floor_area_m2` berisi `min <= max`, atau keduanya `null` jika tidak dapat diperkirakan.
- Label Markdown menggunakan `Shot 01`, `Shot 02`, ...; tidak menggunakan label lama `S1`, `S2`.
- Tidak ada konten audio, ide generatif, prompt, atau tambahan fakta yang tidak bersumber dari pengamatan.
- ID/folder target belum ada pada HEAD yang dipakai untuk commit.

## 8. Hasil yang harus ditampilkan setelah penyimpanan

Jika berhasil, jawab dengan ringkas:

- **Status:** Saved (terverifikasi).
- **Video ID:** `VID-XXX`.
- **Jumlah shot:** sesuai file.
- **Tautan:** `references/VID-XXX/analysis.md` dan `analysis.yaml` di GitHub.
- **Commit:** tautan commit yang sudah menjadi bagian branch `main`.

Jika gagal, tampilkan **Not saved** beserta penyebab konkret dan tindakan yang diperlukan. Jangan membuat tautan file seolah-olah sudah tersedia jika commit gagal.

## 9. Batas penerapan

Dokumen GitHub **tidak otomatis dieksekusi oleh ChatGPT**. Agar diterapkan secara konsisten pada chat baru, masukkan instruksi singkat ke **Project Instructions Homeku** agar AI membaca file ini beserta rules dan template pada awal setiap analisis. Koneksi GitHub harus menyediakan izin tulis untuk tahap `save now`.

Setiap chat tetap bekerja atas konteks video dan berkasnya sendiri; aturan ini tidak menyediakan antrean latar belakang, penyimpanan lintas chat, atau kemampuan mengakses file yang sudah tidak tersedia.

---

**Prinsip kerja:** *Analyze first. Review in chat. Save only on explicit approval. Commit atomically. Verify before declaring success.*
