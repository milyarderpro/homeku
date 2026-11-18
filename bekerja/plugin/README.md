# home-productions — ruang pengembangan plugin

Nama paket: **home-productions**. Status: implementasi tahap 1–5 dan pemeriksaan teknis selesai. Rilis privat **0.1.0** tersedia untuk uji manual di ChatGPT; penerimaan pengguna belum dinyatakan selesai.

Folder ini mengumpulkan seluruh pekerjaan pengembangan plugin. Pustaka sumber tetap berada di knowledge/, references/ dan video/ pada root repository.

## Mulai membaca

1. [Alur penggunaan](production-workflow.md) — perilaku dan keluaran yang sudah disepakati pengguna.
2. [Rencana implementasi](implementation-plan.md) — arsitektur, urutan pekerjaan, struktur target dan kriteria selesai.
3. [Skill produksi](home-productions/skills/produce-home-tour/SKILL.md) — instruksi aktif untuk konsep, shot, gambar, prompt dan penyerahan paket.

Revisi aturan produksi pada alur penggunaan terlebih dahulu, lalu sesuaikan rencana dan implementasinya. Hindari membuat salinan rencana untuk setiap revisi.

## Pembagian folder

| Lokasi | Isi |
| --- | --- |
| README.md | Peta ruang kerja ini |
| production-workflow.md | Kesepakatan pengalaman pengguna |
| implementation-plan.md | Rencana pembangunan dan status tahap |
| home-productions/ | Skill, panduan akses/produksi, template, pemotong frame, ekspor proyek, aturan dan validator |
| tooling/ | Probe kemampuan dan pengemas arsip rilis plugin |
| tests/ | Tes aturan, sumber, crop/piksel, paket proyek, tautan dan portabilitas serta arsip rilis; 65 tes lulus |
| dist/ | Hasil paket rilis; tidak masuk Git |
| runs/ | Berkas proyek/gambar percobaan lokal; tidak masuk Git |

Alur gambar dijelaskan pada [panduan visual](home-productions/skills/produce-home-tour/references/image-workflow.md), dengan [pemotong produksi](home-productions/skills/produce-home-tour/scripts/split_frames.py) yang menjaga piksel tanpa resize. [Panduan prompt/paket](home-productions/skills/produce-home-tour/references/omni-flash.md) melanjutkan ke prompt per shot dan [ekspor proyek](home-productions/skills/produce-home-tour/scripts/build_production_package.py) beserta aset aslinya.

Fondasi dapat dibaca melalui [kontrak proyek](home-productions/skills/produce-home-tour/references/project-contract.md), [aturan produksi](home-productions/skills/produce-home-tour/references/production-rules.yaml) dan [template proyek](home-productions/skills/produce-home-tour/assets/project-template.json). [Probe tahap 1](tooling/probe_stage1.py) tetap tersedia. Aset pilot berada di runs/ yang diabaikan Git; hasil dan batas pemeriksaan dicatat dalam rencana implementasi.

## Pemeriksaan lokal

Dari root repository, jalankan:

~~~sh
python -m unittest discover -s bekerja/plugin/tests -v
python bekerja/plugin/home-productions/skills/produce-home-tour/scripts/validate_project.py bekerja/plugin/home-productions/skills/produce-home-tour/assets/project-template.json
~~~

Rilis privat sudah disimpan dan seluruh source dibaca balik. Pemilihan/aktivasi skill serta alur di ChatGPT diuji manual oleh pengguna; hasil pemeriksaan lokal bukan pengganti uji tersebut.

## Batas pengembangan

- Semua kode, skill, aset plugin, pengujian dan paket produksi baru ditempatkan di bawah bekerja/plugin/.
- Data referensi tetap menjadi sumber pengetahuan; plugin membacanya melalui URL web atau konektor GitHub.
- Paket yang dipasang harus mandiri: sumber pengetahuan dirujuk melalui URL, tanpa ketergantungan pada path lokal repo ini.
- Satu shot kontinu tanpa cut adalah unit produksi: satu kolase → dua gambar individu → satu prompt → satu klip.
- Jenis serta cakupan area mengikuti contoh referensi; bedroom yang ditampilkan maksimal satu. Tidak menambahkan variasi ruang secara bebas.
- Durasi, cakupan area tanpa pengulangan, dan audio mengikuti alur penggunaan yang disepakati.
- Generate video dan publikasi Facebook tetap dilakukan pengguna dalam cakupan awal.
- Dokumen dan kode pengembangan tidak menjadi bacaan kreatif wajib AI.

Manifest memakai Agent Plugins 1.0. Rilis privat dibuat melalui Plugin Creator; langkah berikutnya adalah uji manual pada lingkungan pengguna. Hasil uji kemampuan tahap 1 dan pemeriksaan teknis tidak diubah menjadi klaim bahwa alur plugin terpasang sudah lulus.


## Rilis privat untuk pengujian

- [Buka home-productions 0.1.0](https://chatgpt.com/plugins/plugins_6afd5aeb32208191a60a8b85426c898f)
- Plugin ID: plugins_6afd5aeb32208191a60a8b85426c898f
- Release ID: pluginrel_6afd5aede8fc81918c13057632e8250f
- Dibuat 18 November 2026; scope USER, PRIVATE.
- Arsip: dist/home-productions-0.1.0.zip; SHA-256: 35fb8f999a92a0f6fbf309b77c939cc75ef07a876a86f816bcdb88f80444d8f7.
- Pemeriksaan: 65 tes lulus, schema resmi dan format skill valid. Source terbaca lengkap; layanan menambahkan manifest kompatibilitas dan menerapkan identitas publisher akun.

Untuk mengemas versi berikutnya, jalankan dari root repo setelah memperbarui versi dan pemeriksaannya:

~~~sh
python bekerja/plugin/tooling/package_plugin.py --output bekerja/plugin/dist/home-productions-VERSION.zip
~~~

Gunakan plugin ID yang sama untuk pembaruan melalui Plugin Creator. Ambil current_release_id terbaru sebelum update; jangan membuat plugin duplikat.

## Mulai uji manual di ChatGPT

Buka tautan rilis dan pilih plugin pada percakapan baru. Pastikan plugin dikenali sebelum melanjutkan. Uji satu proyek lengkap terlebih dahulu, dengan contoh permintaan awal:

> Mulai proyek uji home tour vertikal berdasarkan pustaka HOMEKU. Cari referensi yang mendukung exterior, living-to-kitchen, satu bedroom dan bathroom: empat shot, total 20 detik. Tawarkan arah konsep terlebih dahulu; belum perlu membuat gambar.

Sesudah memilih konsep, minta spesifikasi satu rumah dan daftar shot. Setelah desain/shot sesuai, setujui dan minta kolase, review konsistensi, crop serta dua unduhan individu per shot. Hasil yang diharapkan: empat kolase dasar dan delapan PNG 9:16, tanpa pengulangan kitchen.

Setelah meninjau paket visual dan menyetujuinya, lanjutkan ke prompt serta paket proyek. Periksa empat prompt, durasi 6/6/4/4, gerak yang sesuai, ambient tanpa musik, peta file dan ketersediaan gambar asli. Coba lanjutkan proyek dari catatan dan aset pada sesi baru.

Persetujuan diberikan berdasarkan hasil yang sudah ditinjau; tidak perlu mengulang persetujuan yang telah didelegasikan. Laporkan bagian yang berhasil, temuan spesifik dan tahap yang terhenti. Perbaikan mengikuti hasil nyata, lalu bagian terdampak diuji ulang. Variasi cakupan, kegagalan akses dan revisi tetap mengikuti skenario penerimaan dalam rencana.

Aktivasi dan alur ChatGPT belum diverifikasi oleh pengembang. Uji Omni Flash tetap dilewati sesuai arahan pengguna; video/audio hanya dinilai bila hasilnya tersedia.
