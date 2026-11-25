# Design

## Context

Format 3.0 menyimpan keputusan audit di `audit.json`. Saat ini `design.features` sudah memiliki aspek susunan ruang, material, pencahayaan, lingkungan, dan palet teks. Renderer menggabungkan palet dengan material dan pencahayaan dengan lingkungan. Validator mencocokkan hash template pada manifest lalu membandingkan seluruh byte laporan dengan hasil render. Registry mencatat `edh001` pada revisi 1 dan video kanonis tersedia. Motivasi dan perilaku yang dituju dijelaskan di [proposal](proposal.md) dan [spec delta](specs/design-profile/spec.md).

Perubahan 3.0 sebelumnya telah selesai di OpenSpec dan deltanya masih ada di folder change. Ketentuan review teknis dan ekspor langsung mengikuti kontrak operasional yang sudah diperbarui di `audit/contracts/package.md`.

## Goals / Non-Goals

**Goals**

- Satu standar penulisan profil untuk kit baru dan satu bentuk Profil Desain pada seluruh referensi aktif saat rilis.
- Bukti tipe rumah, atmosfer, dan setiap warna dapat ditelusuri ke frame sumber dari pembaca AI.
- `edh001-r0002` meningkatkan profil dengan audit visual terarah dan meneruskan rantai revisi.

**Non-Goals**

- Perubahan gerakan kamera, sampling, tata letak kolase, dan pipeline produksi berada di luar cakupan ini.
- Paket pembanding `edh013` dan `edh058` dipakai sebagai contoh atau input verifikasi baca-saja. Promosi paket pilot adalah keputusan pengguna pada alur ingest tersendiri.

## Decisions

### 1. Letakkan data baru di sumber audit yang sudah ada

- `design.house_type` menyimpan klaim `value`, `state`, dan `evidence` memakai bentuk klaim profil yang sudah ada. `value` berupa satu label Inggris atau `null` untuk `unknown`. Gunakan delapan tipe awal sebagai petunjuk dan alias terkurasi. Definisikan contoh tipe menurut ciri visual, termasuk perbedaan townhouse berderet, semi-detached berpasangan, dan duplex dua unit. Ketika konteks terbatas, catat perkiraan yang wajar dan gunakan state yang sesuai.
- `design.palette` berisi entri `{value, role, hex, state, evidence}`, dengan `value` sebagai nama warna yang dapat dibaca manusia. Tulis HEX enam digit diawali pagar dan utamakan huruf kapital di kit. Role berupa label singkat, misalnya Dominan, Pendamping, atau Aksen. Bidik 4–6 warna representatif dengan batas paling banyak 6. Jika sumber hanya memperlihatkan sebagian warna, simpan yang dapat dinilai. Palet kosong sah ketika video sama sekali tidak memberi dasar penilaian.
- `design.features` memakai kembali `spatial-configuration`, `distinctive-features`, `material-hierarchy`, `lighting`, dan `environment`. Tambahkan `atmosphere` sebagai klaim singkat. Pedoman membedakan sumber serta karakter cahaya, kondisi lingkungan fisik, dan kesan visual. Ringkasan susunan ruang menggambarkan hubungan yang benar-benar terlihat.
- Schema paket menerima audit 3.0 yang sudah dibuat. Template `prepare`, prompt, dan preflight untuk draft aktif meminta kedua field baru sehingga audit baru memakai profil baku. Mode validasi paket tetap menerima snapshot awal. Palet teks `features[aspect=palette]` berlaku pada snapshot awal. Jika `design.palette` dipakai, validasi menolak palet teks paralel.
- Gunakan traversal klaim untuk tipe rumah dan setiap warna sehingga validasi bukti, `referenced_frames`, pemeriksaan viewed, manifest, dan pointer menggunakan sumber yang sama. Ringkasan palet dalam string dipertimbangkan, tetapi tidak menyediakan bukti per warna dan memerlukan parsing prosa untuk membentuk tabel.

### 2. Tambahkan template Profil Desain melalui fingerprint yang sudah ada

Simpan `tools/assets/templates/analysis.md` dengan hash awal dan tambahkan `tools/assets/templates/analysis-profile.md` untuk audit baru. Gunakan `manifest.render.template_sha256` sebagai pengenal aset lewat daftar hash yang dikenal. Draft baru menetapkan template profil baku. Validasi memeriksa kecocokan fingerprint, struktur profil audit, dan byte laporan, lalu meneruskan template yang benar ke renderer serta validator struktur laporan. Pertahankan satu format 3.0, satu renderer dengan enam bagian, dan pilihan otomatis sesuai kontrak snapshot.

Bagian Profil memuat nama, tipe, gaya utama, pengaruh, gaya interior, susunan ruang, ciri khas, material, pencahayaan, atmosfer, dan lingkungan. Tabel **Peran | Warna | HEX** muncul setelah daftar. Nilai tanpa dasar tampil singkat sesuai kontrak, dengan state teknis di JSON. Subjudul palet hanya diizinkan di dalam Profil Desain. Baris pencahayaan di Detail Shot tetap menggambarkan area dan penggunaan warna ditulis pada objek yang relevan. Opsi menimpa template yang ada akan membuat hash snapshot awal gagal dan tidak cocok untuk transisi ini.

### 3. Gunakan facet indeks untuk tipe rumah dan pembacaan identitas untuk palet

Tambahkan grup alias tipe rumah ke `data/taxonomy.json`. `profile_claims` dan generator menerbitkan facet `house-type` dengan label asli, nilai untuk pencocokan, state, dan pointer. CLI `--house-type` menggabungkan facet ini dengan filter referensi serta shot yang sudah ada. Perkiraan `uncertain` ikut secara default dan dapat disaring dengan `--observed-only`. Label baru tetap bisa dicocokkan sebagai label literal. Pembaca identitas mengambil palet, atmosfer, dan susunan ruang dari audit yang sudah diproyeksikan, beserta pointer dan frame yang dirujuk. Palet lengkap tidak diperlukan dalam indeks seleksi referensi.

### 4. Revisi profil edh001 dari bukti asli

Mulai dengan salinan audit `r0001` di workspace. Periksa frame native yang sesuai untuk menilai tipe rumah, atmosfer, dan palet. Pilih permukaan yang cukup merata pencahayaannya dan pakai estimasi HEX yang mewakili desain. Pertahankan isi shot, gerak, pembagian fase, tempo, framing dan pilihan panel. Jika bukti baru memakai frame di luar deklarasi sebelumnya, tambahkan pemeriksaan aktual dan perbarui manifest melalui alur standar. Data yang sudah tercatat untuk ruang, material, cahaya, dan lingkungan menjadi dasar profil. Simpan hanya satu sumber palet pada revisi baru.

Ambil `revision` dan `content_sha256` induk dari registry saat menyiapkan `supersedes`. Jalankan `draft` → `review` → `export` dan berikan laporan, media, serta tautan unduhan `edh001-r0002.zip`. Pengguna memilih paket yang akan masuk pustaka. Verifikasi publish setelah pilihan tersebut tercatat.

## Risks / Trade-offs

- **Template atau jalur render berubah saat memeriksa snapshot awal** → uji hash dan hasil render byte-identik untuk paket 3.0 awal. Tolak fingerprint tak dikenal dan pemasangan template yang tidak cocok dengan struktur audit.
- **Warna atau tipe diperlakukan sebagai fakta yang terlalu pasti** → uji bukti temporal yang dirujuk dan gunakan state yang tepat. Kit mengizinkan penaksiran visual dan tidak memaksa penambahan warna yang belum cukup terlihat.
- **Data profil terbit dua kali atau indeks menebak isi** → satu sumber palet terstruktur, facet hanya dari klaim eksplisit, dan uji pointer yang dapat diresolusikan.
- **Revisi gagal di tengah ingest** → gunakan publikasi transaksional pustaka. `r0001` tetap menjadi snapshot aktif sampai satu transaksi `r0002` berhasil. Bila ada koreksi setelah publikasi, terbitkan revisi lanjutan yang mengikuti rantai.

## Migration Plan

1. Tambahkan schema, template profil, renderer, pencarian, serta panduan. Bangun ulang kit dan turunan pustaka, lalu verifikasi `r0001` masih terbaca serta kedua template tervalidasi.
2. Siapkan revisi `edh001-r0002` di workspace dan uji ZIP tersebut terhadap MP4 kanonis. Tampilkan kandidat dan ZIP di chat agar pengguna dapat memilihnya.
3. Setelah ZIP dipilih, ingest secara eksplisit. Pastikan registry menunjuk `r0002`, laporan tampil sesuai template baku, dan filter tipe rumah serta pembacaan identitas memakai data revisi baru.
4. Jalankan suite tes, cek pustaka, dan cek kit. Rilis siap ketika seluruh referensi aktif memakai Profil Desain baku dan snapshot awal tetap bisa divalidasi sebagai riwayat 3.0.
