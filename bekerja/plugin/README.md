# home-productions — ruang pengembangan plugin

Nama paket: **home-productions**. Status: tahap 1 selesai berdasarkan probe workspace dan uji manual pengguna di ChatGPT web. Tahap 2–7 belum dimulai; paket plugin belum dibangun atau dipasang.

Folder ini mengumpulkan seluruh pekerjaan pengembangan plugin. Pustaka sumber tetap berada di knowledge/, references/ dan video/ pada root repository.

## Mulai membaca

1. [Alur penggunaan](production-workflow.md) — perilaku dan keluaran yang sudah disepakati pengguna.
2. [Rencana implementasi](implementation-plan.md) — arsitektur, urutan pekerjaan, struktur target dan kriteria selesai.

Revisi aturan produksi pada alur penggunaan terlebih dahulu, lalu sesuaikan rencana dan implementasinya. Hindari membuat salinan rencana untuk setiap revisi.

## Pembagian folder

| Lokasi | Isi |
| --- | --- |
| README.md | Peta ruang kerja ini |
| production-workflow.md | Kesepakatan pengalaman pengguna |
| implementation-plan.md | Rencana pembangunan dan status tahap |
| home-productions/ | Akan dibuat saat implementasi: paket plugin yang dapat didistribusikan |
| tooling/ | Probe tahap 1 sudah tersedia; alat pembungkus paket ditambahkan saat diperlukan |
| tests/ | Akan dibuat saat diperlukan untuk pemeriksaan komponen produksi |
| dist/ | Hasil paket rilis; tidak masuk Git |
| runs/ | Berkas proyek/gambar percobaan lokal; tidak masuk Git |

Saat ini tersedia dokumen perencanaan dan [probe tahap 1](tooling/probe_stage1.py). Aset serta laporan pilot berada di runs/ yang diabaikan Git. Hasil dan batas verifikasi dicatat dalam rencana implementasi; struktur paket lainnya dibuat saat tahapnya dikerjakan.

## Batas pengembangan

- Semua kode, skill, aset plugin, pengujian dan paket produksi baru ditempatkan di bawah bekerja/plugin/.
- Data referensi tetap menjadi sumber pengetahuan; plugin membacanya melalui URL web atau konektor GitHub.
- Paket yang dipasang harus mandiri: sumber pengetahuan dirujuk melalui URL, tanpa ketergantungan pada path lokal repo ini.
- Satu shot kontinu tanpa cut adalah unit produksi: satu kolase → dua gambar individu → satu prompt → satu klip.
- Jenis serta cakupan area mengikuti contoh referensi; bedroom yang ditampilkan maksimal satu. Tidak menambahkan variasi ruang secara bebas.
- Durasi, cakupan area tanpa pengulangan, dan audio mengikuti alur penggunaan yang disepakati.
- Generate video dan publikasi Facebook tetap dilakukan pengguna dalam cakupan awal.
- Dokumen dan kode pengembangan tidak menjadi bacaan kreatif wajib AI.

Manifest paket direncanakan memakai Agent Plugins 1.0 dan dipasang secara privat melalui [Plugin Creator](https://developers.openai.com/plugins/build/plugins). Dukungan alat generate gambar, pemrosesan file dan unduhan harus dibuktikan di lingkungan sasaran sebelum kemampuan penuh dinyatakan siap.
