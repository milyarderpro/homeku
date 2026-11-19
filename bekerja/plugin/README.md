# home-productions — ruang pengembangan plugin

Diperbarui: 19 November 2026

**Source dan rilis privat aktif: 2.1.0; schema 2.1/rules 2.1.0.** Tahap 1–6 sudah diimplementasikan dan diperiksa: 70 tes lulus, seluruh source rilis cocok dengan pembacaan balik. Tahap 7: panduan uji manual siap, penerimaan gambar/batch/video pengguna belum selesai.

## Mulai membaca

1. [Rencana dan hasil implementasi](implementation-plan.md) — keputusan, tujuh tahap, bukti teknis/rilis dan matriks penerimaan.
2. [Alur penggunaan](production-workflow.md) — produksi 2.1.0 dari konsep hingga prompt/paket R2V.
3. [Skill source 2.1.0](home-productions/skills/produce-home-tour/SKILL.md) — instruksi yang sudah diperbarui pada plugin yang sama.
4. [Kontrak proyek 2.1](home-productions/skills/produce-home-tour/references/project-contract.md) — komposisi, tata ruang, pilihan referensi, checkpoint dan migrasi.

Satu alur, satu rencana aktif dan satu plugin dipertahankan. Git/rilis menyimpan versi lama; tidak ada folder versi terpisah atau menu kolase/interpolasi.

## Perbaikan yang diterapkan

- Living-to-kitchen memakai satu foto utuh kedua area sebagai default. Exterior-to-living fleksibel **1 atau 2 referensi sesuai pilihan pengguna**. Masing-masing tetap satu shot 6 detik; kamera dan gambar mengikuti tata ruang yang sama.
- Bedroom front three-quarter 35–45° terhadap sumbu panjang bed; bed tampak memanjang diagonal.
- Gambar exterior memuat seluruh rumah; setiap interior mempunyai plafon dan armatur lampu yang masuk akal.
- Gerak mengikuti DNA per area dan ritme 4/6 detik; tidak selalu dolly + pan.
- R2V memakai gambar sebagai identitas visual/spasial, bukan frame awal/akhir wajib. Prompt tidak menyebut nama file atau ID internal.
- Satu prompt lengkap sembilan bagian per code block, siap disalin.
- Gagal menyimpan proyek tidak menghentikan diskusi konsep atau menghilangkan keputusan sesi.

Tidak ada kewajiban dua referensi pada kedua shot penghubung. Exterior-to-living juga tidak dikunci menjadi satu: pengguna dapat memilih 1 atau 2 saat produksi. Jika satu, foto tidak dipaksa memperlihatkan seluruh exterior dan interior sekaligus; bagian yang baru terungkap mengikuti rancangan dan dinilai pada video.

## Pembagian folder

| Lokasi | Isi |
| --- | --- |
| README.md | Peta pengembangan, source/rilis dan panduan uji |
| production-workflow.md | Alur produksi 2.1.0 |
| implementation-plan.md | Tahap baru, status dan penerimaan |
| home-productions/ | Source plugin 2.1.0, satu skill beserta referensi/template/script |
| tooling/ | Pengemas arsip |
| tests/ | Tes kontrak, praproduksi, gambar, ekspor dan arsip |
| dist/ | Arsip rilis, diabaikan Git |
| runs/ | Proyek/gambar percobaan dan laporan lokal, diabaikan Git |

Pustaka knowledge/, references/, video/ dan requests/ root tidak diubah atau disalin ke plugin. Plugin membaca sumber lewat URL GitHub atau konektor; file produksi berada di ruang kerja/paket proyek.

## Pemeriksaan teknis

Sebanyak 70 tes lulus: kontrak 31, checkpoint 9, gambar 7, praproduksi/sumber daya 4, ekspor 13 dan arsip 6. Format skill, template brief, tautan dan schema manifest resmi juga diperiksa. Fixture review/approval/batch serta kegagalan izin bersifat sintetis/terkontrol; bukan bukti naturalitas, konsistensi video, batch paralel atau izin filesystem ChatGPT yang sesungguhnya.

Dari root repository:

~~~sh
python -m unittest discover -s bekerja/plugin/tests -v
python bekerja/plugin/home-productions/skills/produce-home-tour/scripts/validate_project.py bekerja/plugin/home-productions/skills/produce-home-tour/assets/project-template.json
~~~

[Helper checkpoint](home-productions/skills/produce-home-tour/scripts/save_project.py) menjaga file lama, memulihkan nama/folder dan mengembalikan path aktif setelah baca balik. Kegagalan tidak menghentikan diskusi konsep dari data sesi.

Proyek schema 2.0 dikonversi pada salinan lewat validator --migrate-to. Konsep/sumber/mode dan keputusan yang masih berlaku dipertahankan; komposisi serta review baru tidak dibuat otomatis. Skrip crop V1 tidak dikembalikan. Baseline 2.0.0/53 tes tersimpan dalam riwayat Git/rilis.

## Rilis privat 2.1.0

- [Buka home-productions](https://chatgpt.com/plugins/plugins_6afd5aeb32208191a60a8b85426c898f) — versi 2.1.0, tersimpan dan source dibaca balik.
- Plugin ID: plugins_6afd5aeb32208191a60a8b85426c898f.
- Release ID terakhir tercatat: pluginrel_6afe70c8ec04819189e0f70757fec57a.
- Diperbarui 19 November 2026; USER / PRIVATE.
- Arsip: dist/home-productions-2.1.0.zip.
- SHA-256 upload: 3b5d62b56db89963320e140dfd4f16f57b766638fcbc9491fd205213dcb4718d.
- Tujuh belas berkas source cocok dengan pembacaan balik; layanan menyimpan manifest kompatibilitas berkas ke-18, versi sinkron 2.1.0.

Saat update berikutnya, update plugin yang sama melalui Plugin Creator. Baca inventory/source dan current_release_id terbaru; pertahankan publisher akun, defaultPrompt, scope dan audience. Penghapusan file memerlukan delete_paths eksplisit. Jangan menghapus manifest kompatibilitas yang dibuat layanan atau menyimpan email akun di repo.

~~~sh
python bekerja/plugin/tooling/package_plugin.py --output bekerja/plugin/dist/home-productions-VERSION.zip
~~~

## Panduan uji manual 2.1.0

Buka chat baru di ChatGPT dan pilih [home-productions](https://chatgpt.com/plugins/plugins_6afd5aeb32208191a60a8b85426c898f). Mulai pengujian pada rilis 2.1.0 dengan gambar individual/R2V. Pengguna menguji produksi di ChatGPT dan Omni Flash; tes kode tidak membuktikan aktivasi/perilaku host.

Contoh permintaan:

> Mulai uji home tour vertikal berbasis HOMEKU. Gunakan exterior, living-to-kitchen, satu bedroom dan bathroom: empat shot, total 20 detik. Living-to-kitchen memakai satu foto gabungan; bedroom front three-quarter dan bed memanjang diagonal. Mode gambar prompt-to-image. Mulai dari konsep dan rancangan terlebih dahulu.

Setelah konsep dan rancangan disetujui, periksa tahap berikut.

1. **Konsep dan checkpoint.** Pilih/revisi konsep, lalu lanjutkan persetujuan rancangan. Bila penyimpanan gagal, periksa data keputusan tetap dipakai dan tidak ada klaim file tersimpan yang palsu.
2. **Prompt-to-image.** Gunakan exterior + living-to-kitchen + bedroom + bathroom: empat shot, total 20 detik. Sesudah desain disetujui, harapkan **empat prompt gambar**, termasuk satu foto living–kitchen.
3. **Generate image.** Pada mode ini, minta seluruh gambar sesuai rencana sekaligus. Jika rencana sah berisi tujuh, uji tujuh file individual dari satu permintaan tanpa kolase atau perintah per gambar. Catat pelaksanaan sebenarnya; jumlah file bukan bukti paralel.
4. **Review visual.** Periksa exterior utuh dengan margin, bedroom three-quarter/bed diagonal, plafon/lampu tiap interior, naturalitas dan kitchen tunggal yang cocok dengan lintasan.
5. **Prompt siap salin.** Satu code block per shot, sembilan bagian lengkap, tanpa nama file/ID di badan prompt. Peran referensi jelas bukan first/last wajib; petunjuk lampiran di luar block.
6. **Video R2V.** Uji living-to-kitchen dengan satu foto gabungan. Periksa kitchen tidak berganda, gerak mengikuti gambar/DNA dan terbaca dalam 6 detik. Untuk area 4 detik, periksa ritme; pan/orbit terpilih menargetkan ≥12°, tanpa memaksa rotasi pada semua shot. Dengarkan ambient bila audio tersedia.
7. **Kasus terpisah dan kelanjutan.** Uji exterior-to-living dengan 1 atau 2 referensi sesuai pilihan pengguna, pada rancangan tanpa mengulang living. Jumlah gambar/prompt gambar harus mengikuti pilihan, tanpa mengubah jumlah shot atau durasi. Bawa paket/gambar asli ke sesi baru; periksa keputusan, mode dan delegasi tetap terbaca. Catat kasus yang belum diuji.

Laporan cukup menyebut tahap, hasil yang diamati, gambar/video terkait dan kendala spesifik. Temuan digunakan untuk perbaikan terarah pada plugin yang sama; belum diuji tetap dicatat belum diuji.
