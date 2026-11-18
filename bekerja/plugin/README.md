# home-productions — ruang pengembangan plugin

Status pada 18 November 2026: **V2 sudah diimplementasikan dan rilis privat 2.0.0 berhasil diperbarui**. Tahap 1–6 selesai; tahap 7 menunggu uji manual pengguna di ChatGPT/Omni Flash. Kelulusan teknis tidak membuktikan kualitas gambar/video atau batch simultan.

## Mulai membaca

1. [Alur penggunaan V2](production-workflow.md) — dua mode gambar individual, R2V dan aturan produksi.
2. [Rencana dan hasil implementasi](implementation-plan.md) — tujuh tahap, penerimaan, hasil teknis dan identitas rilis.
3. [Skill aktif](home-productions/skills/produce-home-tour/SKILL.md) — instruksi yang sudah tersimpan pada rilis V2.
4. [Kontrak proyek V2](home-productions/skills/produce-home-tour/references/project-contract.md) — schema 2.0, aset area, status batch dan revisi.

Satu alur, satu rencana dan satu plugin dipertahankan. Rilis/Git menyimpan versi lama; tidak ada menu kolase/interpolasi sebagai alur produksi V2.

## Pembagian folder

| Lokasi | Isi |
| --- | --- |
| README.md | Peta pengembangan, rilis dan panduan uji manual |
| production-workflow.md | Alur V2 |
| implementation-plan.md | Tahap, hasil dan matriks penerimaan |
| home-productions/ | Paket skill V2, aturan, template, validator dan ekspor |
| tooling/ | Pengemas arsip plugin |
| tests/ | 53 tes V2: kontrak, sumber, gambar, ekspor dan arsip |
| dist/ | Arsip rilis, diabaikan Git |
| runs/ | Proyek/gambar percobaan dan laporan lokal, diabaikan Git |

Pustaka knowledge/, references/ dan video/ root tidak diubah atau disalin. Plugin mengakses sumber melalui URL web atau konektor GitHub.

## Implementasi tersedia

[Aturan](home-productions/skills/produce-home-tour/references/production-rules.yaml), [template proyek](home-productions/skills/produce-home-tour/assets/project-template.json) dan [schema](home-productions/skills/produce-home-tour/assets/project.schema.json) sudah memakai V2.

[Alur gambar](home-productions/skills/produce-home-tour/references/image-workflow.md) mengatur prompt-to-image atau generate seluruh gambar individual. [Template gambar](home-productions/skills/produce-home-tour/assets/image-prompt-template.md) mempertahankan desain rumah/plafon pada setiap area.

[Panduan Omni Flash](home-productions/skills/produce-home-tour/references/omni-flash.md) dan [template R2V](home-productions/skills/produce-home-tour/assets/prompt-template.md) memakai sembilan bagian. [Ekspor](home-productions/skills/produce-home-tour/scripts/build_production_package.py) menyerahkan paket prompt gambar atau paket R2V lengkap dengan file asli.

Dari root repository:

~~~sh
python -m unittest discover -s bekerja/plugin/tests -v
python bekerja/plugin/home-productions/skills/produce-home-tour/scripts/validate_project.py bekerja/plugin/home-productions/skills/produce-home-tour/assets/project-template.json
~~~

53 tes lulus pada implementasi V2. Fixture batch/review/approval merupakan data sintetis, bukan bukti tujuh gambar dibuat serentak atau hasil video sudah konsisten. Tes crop V1 dan komponen crop yang tidak digunakan sudah dihapus.

## Rilis privat 2.0.0

- [Buka home-productions 2.0.0](https://chatgpt.com/plugins/plugins_6afd5aeb32208191a60a8b85426c898f)
- Plugin ID tetap: plugins_6afd5aeb32208191a60a8b85426c898f
- Release ID: pluginrel_6afd8f59eab0819199eed6bf3b189717
- Diperbarui 18 November 2026; USER, PRIVATE.
- Arsip: dist/home-productions-2.0.0.zip.
- SHA-256 upload: 1f0a90d3f156055f04ae4f52a2bc9fa123b3a230c636c4c36b3ff7a1f1d10677.
- Enam belas berkas upload dibaca balik; layanan menyimpan manifest kompatibilitas sebagai berkas ke-17. Script crop lama terverifikasi terhapus.
- Publisher akun, defaultPrompt dan scope/audience dipertahankan. Tidak menyalin email akun ke repo.

Untuk update berikutnya, gunakan plugin ID yang sama dan baca inventory/current_release_id terbaru. delete_paths diperlukan untuk file lama yang benar-benar dihapus; menghilangkan file dari ZIP saja tidak menghapusnya dari rilis.

~~~sh
python bekerja/plugin/tooling/package_plugin.py --output bekerja/plugin/dist/home-productions-VERSION.zip
~~~

## Uji manual V2

Buka percakapan baru di ChatGPT dan pilih plugin dari tautan rilis. Pastikan instruksi yang digunakan adalah V2/gambar individual/R2V, bukan konteks lama yang masih meminta kolase. Pemilihan/aktivasi pada host pengguna belum diverifikasi oleh tes kode.

### 1. Prompt-to-image

Contoh permintaan awal:

> Mulai proyek uji home tour vertikal berdasarkan pustaka HOMEKU. Gunakan pola exterior, living-to-kitchen, satu bedroom dan bathroom: empat shot, total 20 detik. Mode gambar saya prompt-to-image. Mulai dengan pilihan konsep dan rancangan terlebih dahulu.

Setelah memilih konsep serta menyetujui desain/shot, minta seluruh prompt gambar. Harapan: lima prompt area individual, tanpa otomatis generate, tanpa kolase dan tanpa klaim gambar sudah tersedia.

### 2. Generate seluruh gambar individual

Gunakan mode generate image pada rancangan yang disetujui. Jumlah file mengikuti image_plan: contoh di atas lima gambar; jika rancangan lain yang didukung sumber berisi tujuh, minta tujuh sekaligus.

> Gunakan mode generate image. Buat seluruh gambar area individual sekaligus sesuai rancangan yang sudah disetujui. Jangan membuat kolase atau berhenti meminta perintah setelah setiap gambar. Catat pelaksanaan sebenarnya.

Catat jumlah file, apakah seluruh tahap selesai dari satu permintaan, proses simultan yang benar-benar diamati, kendala serta kebutuhan revisi. Jangan menyimpulkan parallel hanya dari jumlah file. Uji satu per satu hanya jika memang itu yang diminta pengguna.

Periksa cakupan luas, naturalitas, plafon, bukaan, material, furnitur dan hubungan area. Beri persetujuan visual setelah meninjau hasil; delegasi yang sudah diberikan tetap berlaku.

### 3. R2V satu dan dua referensi

Setelah paket gambar disetujui, minta prompt sembilan bagian dan paket proyek. Periksa peta referensi:
- Area tersendiri: satu gambar area untuk satu shot.
- Living-to-kitchen: gambar living dan kitchen untuk satu shot 6 detik.
- Exterior-to-living: gambar exterior dan living untuk satu shot 6 detik, pada rancangan terpisah yang tidak mengulang living.

Generate video secara manual di Omni Flash dengan R2V, bukan kontrol interpolasi first/last. Periksa plafon/struktur tetap, seluruh komponen gerak terlihat, pan/orbit yang dipilih mempunyai target minimal 12°, ritme sesuai 4/6 detik, tanpa cut/morphing dan tanpa musik. Audio hanya dinilai bila dapat didengar.

### 4. Kelanjutan dan laporan hasil

Bawa project.json, panduan dan gambar asli ke sesi baru; periksa mode/keputusan/peta referensi tetap dapat dilanjutkan. Uji perubahan satu elemen desain dan tinjau area/shot terdampak.

Laporkan bagian yang berhasil, temuan spesifik dan tahap yang terhenti. Perbaikan dilakukan pada plugin yang sama, kemudian bagian terdampak diuji ulang. Penerimaan V2 belum ditandai selesai sampai hasil manual kasus wajib tersedia.
