# Proposal

## Why

Profil Desain HOMEKU sudah mencatat gaya dan skala, tetapi tipe rumah belum bisa dicari. Susunan ruang tersimpan di audit, pencahayaan bercampur dengan lingkungan di laporan, dan palet saat ini berupa teks. Menetapkan Profil Desain sekarang memungkinkan pustaka dirilis dengan satu tampilan baku saat `edh001` masih menjadi satu-satunya referensi aktif.

## What Changes

- Tambahkan satu tipe rumah per audit dan filter `--house-type`. Mulai dari delapan contoh tipe, dengan label baru seperti `Tower House` tetap bisa dipakai dan dicari.
- Tampilkan susunan ruang utama dan material yang sudah tercatat. Tampilkan pencahayaan, atmosfer, dan lingkungan sebagai tiga baris singkat.
- Tambahkan tabel palet warna HEX di Profil Desain. Detail Shot cukup menjelaskan penerapan warna dan cahaya tiap area.
- Perbarui kit agar audit baru menghasilkan Profil Desain baku dalam format paket 3.0. Kandidat yang lulus review teknis langsung dapat dibungkus menjadi ZIP tanpa MP4.
- Siapkan `edh001-r0002.zip` sebagai revisi profil yang ditautkan ke snapshot `r0001`. Setelah pengguna memilih ZIP, ingest dan verifikasi hasilnya sebelum rilis.
- Pertahankan validasi snapshot 3.0 yang sudah dibuat. Paket pilot dan riwayat dapat diperiksa dengan template yang tercatat di manifest.

## Capabilities

### New Capabilities

- `design-profile` — Pencatatan profil desain, tampilan manusia, pencarian tipe rumah, dan penerapan standar pada referensi aktif.

### Modified Capabilities

Tidak ada spesifikasi utama yang sudah terdaftar. Delta ini menambahkan perilaku Profil Desain di atas kontrak 3.0 yang berjalan.

## Impact

- Schema dan template audit, validasi bukti, aset dan renderer laporan, generator proyeksi, taksonomi, pembaca, dan CLI.
- Panduan audit, prompt, kontrak laporan dan pembaca, contoh sintetis, dan ZIP kit.
- Referensi aktif `edh001` melalui revisi ZIP yang dipilih pengguna. Katalog dan indeks diperbarui oleh generator setelah ingest.
