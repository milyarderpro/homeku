# Verifikasi Phase 1

Tanggal: 21 November 2026. Implementasi dan verifikasi dilakukan lokal; workflow hosted belum dijalankan atau dipush dari sesi implementasi ini.

## Hasil

- 23 pengujian integrasi lulus melalui `python -m unittest discover -s tests -t . -v`.
- Kapasitas: 300 referensi sintetis, 600 shot; ingest, registry, indeks, paginasi dan rebuild penuh konsisten.
- Batch memproses seluruh ZIP; paket gagal tidak memblokir paket valid atau mengganti referensi aktif.
- Replay identik tidak mengubah keluaran; revisi mengganti variasi lama dan membersihkan hasil usang. Konflik revisi/supersedes dan duplikasi sumber ditolak.
- Sumber yang sudah ada dapat dipakai tanpa MP4 dalam ZIP. Revisi pertama tidak menimpa sumber kanonis yang berbeda. Dua revisi dalam satu batch dapat memakai sumber staging.
- Hash, metadata stream, timestamp, cakupan, inventory media, urutan storyboard dan identitas MD/manifest diperiksa.
- ZIP traversal, path bentrok, symlink, executable dan media motion tidak diterima. Paket fixture ditolak dari root produksi.
- Tiga contoh notasi kamera pengguna dipertahankan, termasuk →, +, rentang sudut, rasio, karakter dan tempo fast. Unknown/negasi/label area baru tetap terbaca.
- Dua importer lokal bersamaan mempertahankan kedua unggahan. Kegagalan persiapan/publikasi dan interupsi proses diuji tanpa merusak state sebelumnya.
- Remote Git bare sementara mensimulasikan push berdekatan: publisher kehilangan push pertama, mengulang dari snapshot baru, lalu menerbitkan kedua ZIP. Remote GitHub pengguna tidak diubah.
- Kedua YAML workflow dapat diparse; tautan navigasi, dokumentasi, pilot dan halaman awal valid.
- Registry aktif tetap 0 referensi/0 shot. Arsip, MP4 sumber dan masterprompt produksi tidak diubah.

## Batas yang belum diuji

Fixture membuktikan kontrak dan otomasi teknis, bukan kebenaran audit visual atau kreativitas produksi. Alur chat Gemini/ChatGPT, kalibrasi tempo, kenyamanan penyerahan ZIP dan tujuh audit nyata tetap Phase 2.

Aktivasi hosted memerlukan file implementasi dipush ke branch default, GitHub Actions aktif dan izin publikasi bot sesuai aturan branch. Satu run nyata diperlukan untuk membuktikan konfigurasi akun/repo. Tidak ada persetujuan isi tambahan pada workflow ingest.
