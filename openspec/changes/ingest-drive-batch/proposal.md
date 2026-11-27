# Proposal

## Why

Hasil audit bertambah di Google Drive, sementara setiap paket masih harus diunduh dan diserahkan ke ingest secara manual. Pengguna ingin memutuskan satu kali untuk satu batch hasil final, lalu membiarkan komputer menyelesaikan unduhan dan ingest saat perintah dipanggil.

## What Changes

- Tambahkan satu perintah Python lokal yang memindai `HOMEKU/Audit/<nama-video>/` ketika dipanggil. Perintah menampilkan ringkasan riwayat, paket baru, revisi berikutnya, dan konflik.
- Berikan satu langkah persetujuan untuk memilih satu atau beberapa paket. Ikat pilihan ke ID file Drive dan SHA-256 ZIP yang ditampilkan agar koreksi yang menimpa file memerlukan persetujuan baru.
- Unduh ZIP terpilih dan MP4 asli bila salinan lokal belum tersedia. Cocokkan hash sumber dan teruskan hanya ZIP yang sudah diverifikasi ke ingest HOMEKU.
- Tampilkan hasil tiap paket dan akhiri perintah setelah batch selesai. Pemanggilan berikutnya memindai kondisi terbaru dan melewati paket yang sudah tercatat.

## Capabilities

### New Capabilities

- `drive-batch-ingest` — Pemindaian sesuai permintaan, persetujuan batch, dan ingest lokal paket audit yang dipilih dari Google Drive.

### Modified Capabilities

## Impact

Perubahan mencakup perintah lokal, pembaca Drive berakses baca, pengujian alur batch, dan panduan pengguna. Proses memakai format 3.1, verifikasi MP4 kanonis, aturan revisi, dan ingest yang sudah berlaku. Penyerahan dari ChatGPT dan pilihan pengguna untuk menerbitkan referensi tetap mengikuti alur yang berlaku.
