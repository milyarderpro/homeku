# Gambar individual: dua mode, komposisi dan review

Gunakan setelah rancangan disetujui/didelegasikan. Baca [kontrak](project-contract.md), [aturan](production-rules.yaml) dan [template gambar](../assets/image-prompt-template.md).

## Pilihan mode dan batch

prompt_to_image menyerahkan seluruh prompt, satu prompt lengkap per image_id. Jangan otomatis generate. Gunakan image_prompt_package; file belum wajib, belum disebut siap R2V final. Buka hasil alat pilihan pengguna saat benar-benar tersedia, tanpa meminta unggah ulang jika akses sudah ada.

generate_image membuat seluruh gambar individual sesuai rencana **sekaligus dalam satu tahap/permintaan**. Tujuh berarti tujuh file, bukan kolase/contact sheet atau berhenti meminta perintah tiap area. Satu per satu hanya bila pengguna meminta, dicatat di image_batch.user_instruction.

Gunakan kemampuan generate/edit yang tersedia pada host. Lampirkan piksel lewat mekanisme alat, bukan hanya nama file. Jangan memindahkan produksi ke API/layanan berbayar atau menyatakan batas ChatGPT dari kegagalan alat pengembang. Jika ada batas nyata, laporkan hasil parsial; jangan mengubah permintaan diam-diam.

Semua tugas gambar memakai desain yang sama. Aset yang sudah tersedia boleh membantu konsistensi jika benar-benar dilampirkan, tetapi jangan mewajibkan membuat gambar tambahan sebelum batch.

## Satu pandangan yang mendukung shot

Gunakan design.area_specs, connections dan anchors untuk menyusun composition: posisi/arah/tinggi kamera, sudut terhadap subjek, penempatan subjek, foreground/background, visible_bounds, layout_note serta shot_alignment. Kamera video memakai tata ruang yang sama. Jangan menyerahkan hanya kata wide/full overview.

| Jenis gambar | Komposisi wajib |
| --- | --- |
| Exterior | Seluruh massa rumah yang terlihat: atap, batas kiri/kanan, dasar; ada ruang aman di tepi. Sudut frontal, three-quarter atau lainnya sesuai desain/sumber |
| Living–kitchen | Satu foto koheren kedua area dan sambungan, kitchen tunggal pada lokasi tetap; orientasi mendukung lintasan |
| Bedroom | Front three-quarter, sasaran 35–45° terhadap sumbu panjang bed secara horizontal; bed memanjang diagonal, hindari frontal terpusat/simetris |
| Interior lainnya | Ruang terbaca luas: lantai, plafon, bukaan/furnitur utama dan armatur lampu yang sesuai fungsi/desain |

Untuk bedroom, pilih sisi kamera yang sesuai layout; jangan memutar bed atau memakai roll. Sudut tersebut target proyek, bukan pengukuran otomatis dari piksel atau ukuran semua referensi.

Setiap interior punya lampu nyata yang terbaca; jenis dan posisinya mengikuti rancangan. Lampu boleh mati pada cahaya siang. Plafon, lampu, bukaan dan furnitur tetap tidak berubah antarview. Jangan menambah dekorasi/struktur yang belum dirancang.

Living-to-kitchen default satu foto gabungan, bukan dua foto yang ditempel. Exterior-to-living mengikuti pilihan pengguna 1/2 referensi. Jika satu, tidak perlu memaksakan seluruh living terlihat pada foto exterior. Jika dua, exterior/living individual harus menunjukkan rumah dan sambungan yang sama. Jangan menambah referensi kedua sebagai syarat tersembunyi.

Full exterior merupakan syarat gambar, bukan semua frame video. Full interior adalah cakupan informatif, bukan melihat seluruh sisi yang tertutup. Hindari close-up yang membuang konteks, fisheye ekstrem, dinding transparan, dollhouse/cutaway atau perspektif mustahil.

Gambar adalah identitas visual/spasial R2V, bukan frame awal/akhir wajib. Video 9:16; rasio gambar dipilih agar cakupan wajar dan sesuai alat, tanpa crop/resize paksa yang membuang informasi. Simpan dimensi/format aktual, tanpa mengarang resolusi minimum atau mengklaim upscaling menambah detail. PNG/JPEG/WEBP statis didukung kontrak; PNG dapat dipilih bila tersedia.

Naturalitas dilihat dari perspektif, skala, garis, tekstur, cahaya, bayangan dan pantulan yang masuk akal. Hindari plastik/CGI/HDR berlebihan. Kata photorealistic bukan bukti gambar sudah natural.

## Review sebelum final

Periksa setiap gambar serta seluruh set sebagai satu rumah:
- Desain/material, plafon/lampu, bukaan, lantai, furnitur tetap, cahaya dan lingkungan.
- Exterior utuh dengan margin; bedroom benar-benar three-quarter dan bed diagonal.
- Kitchen tunggal, hubungan ruang dan arah pandang sesuai posisi kamera/lintasan/akhir.
- Jika dua referensi exterior-to-living dipilih, sambungan masuk/living dan geometri saling sesuai.
- Cakupan cukup dan perspektif natural tanpa memaksa bagian yang tersembunyi terlihat.

Review didasarkan pada piksel yang dilihat atau laporan pengguna, dengan review_origin ai_visual/user_report dan note yang menjelaskan cakupan. Data komposisi, hash atau kalimat larangan tidak membuktikan visual benar.

Revisi bagian yang menyimpang sebelum image_final. Perubahan elemen tetap meninjau gambar/shot terdampak. Jangan menyalin nomor revisi baru ke isi aset lama agar tampak mutakhir. Persetujuan paket visual mengikuti pengguna/delegasi, bukan wajib per gambar.

## Status dan penyerahan

image_batch.execution berisi not_started/parallel/sequential/external/unknown. Catat bukti pelaksanaan pada note; jumlah file/permintaan/tes tidak membuktikan parallel. Jika tidak teramati, unknown; jika alat memproses berurutan, catat sequential dan laporkan ketidaksesuaian. all_at_once pada generate_image tetap draft sampai pemenuhan permintaan tercatat berdasarkan pelaksanaan/laporan, bukan disimpulkan.

prompt_to_image mencatat external saat file dibawa dari generator pengguna. one_by_one hanya atas instruksi pengguna. Kegagalan/parsial tidak diberi status seluruh batch selesai.

Satu aset reference per image_id, dengan ID unik, path relatif, revisi, hash, dimensi dan format sebenarnya. File identik tidak menyamar sebagai dua gambar. planned/prompt_ready/failed belum mengaku punya aset; failed menyimpan error. available berarti file ada; reviewed memerlukan catatan review aktual.

Gunakan [checkpoint](../scripts/save_project.py) untuk menyimpan dict aktif; bila gagal, lanjutkan dari data sesi tanpa mengaku file tersedia. Jalankan [validator](../scripts/validate_project.py) terhadap file yang benar-benar berhasil disimpan.

Serahkan unduhan setiap gambar, ukuran aktual, ringkasan review dan catatan proyek. ZIP opsional tidak menggantikan gambar individual. Sesudah paket final, lanjutkan [R2V](omni-flash.md); tidak ada kolase/crop panel/interpolasi dalam alur utama.
