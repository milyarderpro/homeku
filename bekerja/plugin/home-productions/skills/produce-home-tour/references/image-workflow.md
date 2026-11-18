# Gambar area individual: prompt atau batch

Gunakan setelah desain/shot disetujui atau didelegasikan. Baca [kontrak](project-contract.md), [aturan](production-rules.yaml) dan [template prompt gambar](../assets/image-prompt-template.md).

## Pilihan mode

prompt_to_image menyerahkan seluruh prompt gambar individual. Satu image_id mempunyai satu prompt lengkap. Jangan otomatis menjalankan generator. Gunakan stage image_prompt_package untuk penyerahan ini; aset belum wajib. Hasil dari alat pilihan pengguna kemudian dibuka melalui akses nyata, tanpa meminta unggah ulang bila file sudah tersedia.

generate_image membuat seluruh gambar individual sesuai image_plan dalam satu tahap. Jika tujuh, kerjakan tujuh sekaligus. Jangan membuat kolase/contact sheet atau berhenti menunggu perintah setelah setiap gambar. Generate satu per satu hanya untuk permintaan eksplisit pengguna, dicatat pada image_batch.user_instruction.

Gunakan kemampuan generate/edit bawaan yang benar-benar tersedia. Sertakan gambar acuan melalui mekanisme alat yang sebenarnya; menyebut nama file tidak melampirkan piksel. Jangan beralih ke API atau layanan berbayar tanpa permintaan. Ketersediaan batch simultan dibuktikan pada host pengguna, bukan disimpulkan dari alat pengembang.

## Satu rumah pada seluruh gambar

Semua prompt memakai keputusan design yang sama dan mencatat area tujuan, plafon, bukaan, furnitur, material, cahaya, lingkungan serta hubungan ruang. Gambar yang sudah tersedia/diperiksa boleh menjadi acuan bersama sesuai arahan proyek; jangan mewajibkan generate gambar tambahan sebelum batch.

Komposisi memperlihatkan area secara luas/informatif: lantai, plafon, bukaan dan susunan furnitur yang dibutuhkan kamera. Jangan memaksa seluruh dinding terhalang terlihat melalui fisheye, transparansi atau dollhouse. Hindari close-up yang membuang informasi utama.

Video tetap 9:16. Gambar area bukan endpoint video wajib, sehingga rasio acuan dipilih sesuai cakupan dan alat; tidak dipotong/diregangkan demi memenuhi rasio frame V1. Simpan dimensi dan format aktual. PNG menjadi pilihan penyerahan bila tersedia; PNG/JPEG/WEBP statis dapat dicatat sesuai file sebenarnya. Jangan mengasumsikan format/input tambahan didukung aplikasi yang belum diperiksa.

Naturalitas dinilai dari gambar: perspektif, skala, tekstur, garis bangunan, pencahayaan, pantulan dan bayangan masuk akal; tidak tampak seperti CGI/plastik/HDR berlebihan. Kata photorealistic bukan hasil review.

Living-to-kitchen tetap dua gambar individual; exterior-to-living juga dua. Kedua area harus memperlihatkan hubungan ruang yang sama sesuai rancangan. Fungsi lain yang terpadu mengikuti pemetaan image_plan; tidak otomatis membuat area fisik baru.

## Status batch yang jujur

image_batch.request_mode default all_at_once. execution mencatat not_started, parallel, sequential, external atau unknown. note menjelaskan dasar pengamatan/laporan; jangan menyimpulkan parallel hanya dari jumlah file.

Jika tujuh diminta tetapi lima berhasil, catat dua gambar gagal/tertunda dan pertahankan image_draft. Jika eksekusi serentak tidak teramati, gunakan unknown dan laporkan batas pengamatan. Jika alat terbukti memproses satu per satu, catat sequential; jangan mengklaim permintaan simultan sudah dipenuhi atau mengubah permintaan tanpa arahan.

all_at_once pada mode generate_image baru dapat dinyatakan final bila pelaksanaan parallel dicatat berdasarkan bukti aktual atau laporan pengguna. one_by_one memerlukan instruksi pengguna dan pelaksanaan sequential yang sesuai. Ini pemeriksaan konsistensi catatan, bukan pengukuran concurrency otomatis.

Pada mode prompt_to_image, gambar yang dibawa dari luar dicatat sebagai external, dengan dasar perolehannya pada note. Tidak ada klaim batch internal ChatGPT pada mode ini.

## Review dan aset

Periksa setiap gambar dan seluruh set sebagai satu rumah. Bandingkan plafon/tingkat/sambungan/lampu, bukaan, lantai, furnitur tetap, material, cahaya dan lingkungan. Perbedaan antararea yang memang dirancang boleh ada; perubahan tak direncanakan direvisi.

Simpan satu aset role reference per image_id, dengan asset_id unik, revision, path relatif dari folder project.json, SHA-256, width, height dan format aktual. File asli diperlukan. Pastikan dimensi/keterbacaan cukup untuk kebutuhan; tanpa target resolusi tertentu, jangan mengarang standar minimum atau mengklaim upscaling menambah detail.

image_plan.status: planned selama perencanaan, prompt_ready ketika prompt siap, available setelah file ada, reviewed setelah review, atau failed dengan error aktual tanpa mengklaim aset. image_plan.asset_id mengikat file; jangan menyamarkan file sama sebagai dua area melalui nama berbeda.

reviewed hanya true setelah piksel dilihat atau laporan pengguna diterima; review_origin ai_visual/user_report dan review_note memuat temuan serta cakupan. image_final memerlukan seluruh gambar, persetujuan visual aktual/delegasi, dan revisi yang sama. Tidak meminta persetujuan setiap gambar satu per satu.

Bila desain berubah, tinjau area dan shot terdampak. File/review lama tidak otomatis cocok hanya dengan mengganti nomor revisi. Tidak ada human_verified atau review manual setiap referensi pustaka.

## Penyerahan

Jalankan [validator](../scripts/validate_project.py) dengan file proyek dan [dependensi](../scripts/requirements.txt) yang tersedia. Ia memeriksa file/metadata, bukan naturalitas atau plafon.

Serahkan tautan individu setiap gambar, ukuran aktual, ringkasan review dan project.json. File harus dapat dibuka sebelum disebut tersedia; keberhasilan pengguna mengunduh hanya disebut jika diamati/dilaporkan. ZIP opsional tidak menggantikan file individual.

Sesudah gambar final, lanjutkan [prompt R2V](omni-flash.md) bila diminta. Kolase, pemotongan panel dan pasangan first/last frame tidak menjadi alur produksi V2.
