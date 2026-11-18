# home-productions — ruang pengembangan plugin

Nama paket: **home-productions**. Status: tahap 1–3 selesai. Skill praproduksi tersedia sampai rancangan shot; produksi gambar dan prompt akhir belum diimplementasikan. Plugin belum dipasang.

Folder ini mengumpulkan seluruh pekerjaan pengembangan plugin. Pustaka sumber tetap berada di knowledge/, references/ dan video/ pada root repository.

## Mulai membaca

1. [Alur penggunaan](production-workflow.md) — perilaku dan keluaran yang sudah disepakati pengguna.
2. [Rencana implementasi](implementation-plan.md) — arsitektur, urutan pekerjaan, struktur target dan kriteria selesai.
3. [Skill praproduksi](home-productions/skills/produce-home-tour/SKILL.md) — instruksi aktif untuk brief, sumber, konsep dan rancangan shot.

Revisi aturan produksi pada alur penggunaan terlebih dahulu, lalu sesuaikan rencana dan implementasinya. Hindari membuat salinan rencana untuk setiap revisi.

## Pembagian folder

| Lokasi | Isi |
| --- | --- |
| README.md | Peta ruang kerja ini |
| production-workflow.md | Kesepakatan pengalaman pengguna |
| implementation-plan.md | Rencana pembangunan dan status tahap |
| home-productions/ | Paket skill praproduksi, panduan akses/konsep, manifest, aturan, kontrak/template dan validator |
| tooling/ | Probe tahap 1 sudah tersedia; alat pembungkus paket ditambahkan saat diperlukan |
| tests/ | Tes aturan, kontrak, dua kasus anotasi sumber, tautan dan portabilitas; 32 tes lulus |
| dist/ | Hasil paket rilis; tidak masuk Git |
| runs/ | Berkas proyek/gambar percobaan lokal; tidak masuk Git |

Fondasi dapat dibaca melalui [kontrak proyek](home-productions/skills/produce-home-tour/references/project-contract.md), [aturan produksi](home-productions/skills/produce-home-tour/references/production-rules.yaml) dan [template proyek](home-productions/skills/produce-home-tour/assets/project-template.json). [Probe tahap 1](tooling/probe_stage1.py) tetap tersedia. Aset pilot berada di runs/ yang diabaikan Git; hasil dan batas pemeriksaan dicatat dalam rencana implementasi.

## Pemeriksaan lokal

Dari root repository, jalankan:

~~~sh
python -m unittest discover -s bekerja/plugin/tests -v
python bekerja/plugin/home-productions/skills/produce-home-tour/scripts/validate_project.py bekerja/plugin/home-productions/skills/produce-home-tour/assets/project-template.json
~~~

Skill sudah tersedia sebagai berkas paket, tetapi belum diuji sebagai plugin terpasang. Pemasangan termasuk tahap 7 setelah komponennya lengkap; hasil pemeriksaan lokal bukan pengganti uji perilaku di ChatGPT web.

## Batas pengembangan

- Semua kode, skill, aset plugin, pengujian dan paket produksi baru ditempatkan di bawah bekerja/plugin/.
- Data referensi tetap menjadi sumber pengetahuan; plugin membacanya melalui URL web atau konektor GitHub.
- Paket yang dipasang harus mandiri: sumber pengetahuan dirujuk melalui URL, tanpa ketergantungan pada path lokal repo ini.
- Satu shot kontinu tanpa cut adalah unit produksi: satu kolase → dua gambar individu → satu prompt → satu klip.
- Jenis serta cakupan area mengikuti contoh referensi; bedroom yang ditampilkan maksimal satu. Tidak menambahkan variasi ruang secara bebas.
- Durasi, cakupan area tanpa pengulangan, dan audio mengikuti alur penggunaan yang disepakati.
- Generate video dan publikasi Facebook tetap dilakukan pengguna dalam cakupan awal.
- Dokumen dan kode pengembangan tidak menjadi bacaan kreatif wajib AI.

Manifest fondasi memakai Agent Plugins 1.0. Paket lengkap direncanakan dipasang secara privat melalui [Plugin Creator](https://developers.openai.com/plugins/build/plugins). Dukungan alat generate gambar, pemrosesan file dan unduhan harus dibuktikan di lingkungan sasaran sebelum kemampuan penuh dinyatakan siap.
