---
name: produce-home-tour
description: Susun konsep rumah, continuous shot, prompt atau batch gambar individual, dan prompt R2V Omni Flash berbasis HOMEKU. Gunakan untuk memulai, melanjutkan atau merevisi produksi sampai paket proyek; analisis sumber saja tidak memulai seluruh produksi.
---

# Produksi home tour R2V

Bangun satu rumah dan bahasa videonya dari keseluruhan DNA HOMEKU. Satu shot menghasilkan satu prompt R2V dan satu klip. Pengguna menjalankan generate video, perangkaian dan publikasi.

## Bacaan sesuai pekerjaan

- Sumber: [akses repo](references/repo-access.md). Baca selektif lewat URL web atau konektor GitHub; tidak mewajibkan clone atau salinan pustaka.
- Konsep/desain/shot: [praproduksi](references/preproduction.md) dan [aturan](references/production-rules.yaml).
- Catatan/data: [kontrak 2.1](references/project-contract.md), [template](assets/project-template.json), [schema](assets/project.schema.json) dan [validator](scripts/validate_project.py).
- Dua mode gambar, komposisi dan review: [alur gambar](references/image-workflow.md) dan [template gambar](assets/image-prompt-template.md).
- Prompt/penyerahan/revisi: [Omni Flash](references/omni-flash.md), [template R2V](assets/prompt-template.md) dan [pembuat paket](scripts/build_production_package.py).
- Saat menyimpan checkpoint: [helper penyimpanan](scripts/save_project.py); dependensi pada [requirements](scripts/requirements.txt).

## Mulai atau lanjutkan

Kerjakan bagian yang diminta. Pada kelanjutan, pertahankan konsep, desain, pilihan mode, persetujuan dan delegasi yang masih berlaku. Minta hanya informasi yang hilang dan memengaruhi hasil.

Pisahkan fakta sumber, dugaan analisis dan adaptasi proyek. Confidence rendah tidak melarang memilih bahan desain baru. Jangan mengarang kutipan, denah, ukuran atau angka gerak sumber. Tidak ada human_verified/review manual setiap referensi.

Schema 2.0 dikenali dan dikonversi pada salinan melalui migrate_project di validator. Brief/konsep/sumber/mode dan keputusan yang masih berlaku dipertahankan; data komposisi baru perlu dilengkapi, visual lama tidak otomatis memenuhi review baru. Schema 1.0 tidak otomatis menjadi gambar full area/R2V. Jangan menimpa proyek lama atau menambahkan menu kolase/interpolasi.

## Rancangan yang mengikat gambar dan kamera

Pilih sumber untuk keseluruhan bahasa video serta pendukung desain yang kompatibel. Tetapkan satu tata ruang, plafon, lampu, bukaan, furnitur/material, cahaya dan lingkungan. Kitchen mempunyai satu lokasi tetap. Isi area_specs, komposisi gambar dan camera.spatial_plan dari keputusan yang sama: posisi/arah kamera → gambar → lintasan → framing akhir.

Pilih gerak per area dari DNA sumber, bukan dolly + pan untuk semua ruang. Gerak tunggal sah; gabungan terpilih harus terbaca. Pan/orbit terpilih ≥12°, simultan berbeda dari sekuensial; jarak/sudut/fase/kecepatan sesuai 4/6 detik. Rencana geometris tidak dibuktikan oleh teks larangan objek ganda.

Satu shot kontinu tanpa cut; jangan mengungkap area berulang atau menampilkan lebih dari satu bedroom/fungsi tidur. Area opsional mengikuti sumber. Exterior dan kedua penghubung 6 detik; shot lain 4 detik.

Living-to-kitchen memakai satu foto utuh living+kitchen sebagai default. Exterior-to-living fleksibel **1 atau 2 referensi sesuai pilihan pengguna saat produksi**; jangan mengunci salah satunya. Pilihan yang sudah ada tidak ditanyakan ulang. Kedua pola tetap satu shot, bukan dua klip. Jangan menumpuk penghubung yang mengulang living.

Sebelum produksi gambar, tampilkan rancangan, jumlah/peta gambar, shot, prompt dan total durasi. Exterior + living-to-kitchen + bedroom + bathroom: empat gambar, empat shot/prompt video, 20 detik. Exterior-to-living + kitchen + bedroom + bathroom: empat atau lima gambar sesuai pilihan referensi, empat shot, 18 detik.

## Gambar, review dan prompt

Setelah desain disetujui, gunakan image_mode yang sudah dipilih:
- prompt_to_image: serahkan seluruh prompt individual tanpa otomatis generate; hasil pengguna dibaca saat benar-benar tersedia.
- generate_image: seluruh gambar individual sekaligus sesuai rencana. Tujuh berarti tujuh file dalam satu tahap/permintaan; bukan kolase atau berhenti meminta perintah tiap area. Satu per satu hanya jika diminta.

Exterior memuat seluruh rumah dengan margin; setiap interior mempunyai plafon/armatur yang logis; bedroom front three-quarter 35–45° terhadap sumbu panjang bed dan bed memanjang diagonal. Sudut bedroom adalah preferensi pengguna, bukan ukuran universal sumber.

Review piksel aktual dan bandingkan antararea sebagai satu rumah. Bedakan review AI/laporan pengguna; catat pelaksanaan batch sebenarnya. Jangan mengaku parallel dari jumlah file/permintaan saja. Kegagalan/eksekusi belum terbukti tetap draft, tanpa diam-diam mengganti alur atau beralih ke API.

Gambar final menjadi identitas visual/spasial R2V, **bukan frame awal/akhir wajib**. Badan prompt video tidak memuat nama file, path atau ID internal; peta lampiran disimpan di data/panduan luar prompt. Tulis sembilan bagian lengkap, satu prompt per fenced code block di chat. Judul, petunjuk lampiran dan catatan di luar block. .txt ekspor memakai isi yang sama tanpa pagar Markdown.

Video 9:16, satu continuous shot, ambient natural halus saja tanpa musik/narasi/dialog/efek dramatis. Cut antarklip hanya pada panduan perangkaian. Periksa prompt utuh agar instruksi kreatif tidak bertentangan dengan aturan.

## Checkpoint dan penyerahan

Tiga titik keputusan: konsep, desain/shot dan paket visual. Delegasi tetap berlaku; tidak memaksakan persetujuan per gambar.

Simpan checkpoint pada keputusan/revisi penting dan penyerahan, **bukan syarat setiap balasan**. Gunakan save_project dari helper dengan dict proyek aktif, lokasi yang dipilih di ruang kerja host, source_root aset asal dan fallback_root yang dapat diakses host. Jangan mengulang write_text langsung ke path yang gagal.

Jika saved true, gunakan **path aktual yang dikembalikan** sebagai lokasi aktif, termasuk nama revisi/folder pemulihan baru. Jika saved false, pertahankan data sesi, lanjutkan konsep dan jelaskan belum tersimpan; berikan catatan teks untuk melanjutkan bila diperlukan. Jangan mengarang tautan, meminta pengguna mengurus izin rutin, mereset persetujuan atau mengubah chmod/ownership. Helper tidak menimpa checkpoint lama dan hanya mengaku tersimpan setelah baca balik/validasi.

image_prompt_package sah tanpa aset; image_final/prompt_package memerlukan gambar asli dan review/revisi yang sesuai. Serahkan panduan, catatan, prompt dan unduhan individu gambar; ZIP opsional. Jangan mengaku file/paket final tersedia hanya dari nama atau tautan lama.

Revisi material meninjau bagian terdampak; jangan menaikkan nomor aset usang agar tampak baru. Nilai video/audio hanya bila dapat diakses; keberhasilan validator/upload tidak membuktikan geometri, naturalitas, gerak atau audio hasil.
