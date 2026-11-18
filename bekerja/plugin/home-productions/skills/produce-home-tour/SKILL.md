---
name: produce-home-tour
description: Susun brief, konsep rumah, continuous shot, prompt atau batch gambar area individual, dan prompt R2V Omni Flash. Gunakan untuk memulai, melanjutkan atau merevisi produksi home tour berbasis HOMEKU sampai paket proyek; analisis sumber saja tidak memulai seluruh produksi.
---

# Produksi home tour R2V

Bangun satu rumah dan bahasa videonya dari DNA referensi HOMEKU. Gambar individual menetapkan identitas area; satu shot menghasilkan satu prompt R2V dan satu klip, termasuk shot penghubung dengan dua gambar area. Generate video, perangkaian dan publikasi dilakukan pengguna.

## Bacaan sesuai tugas

- Baca [aturan](references/production-rules.yaml) dan [kontrak proyek](references/project-contract.md) saat menyiapkan/merevisi catatan. Gunakan [template proyek](assets/project-template.json); [schema](assets/project.schema.json) dan [validator](scripts/validate_project.py) memeriksa data.
- Untuk sumber, baca [akses repo](references/repo-access.md). Gunakan URL web atau konektor GitHub secara selektif; jangan mewajibkan clone atau memuat seluruh pustaka.
- Untuk konsep, rumah, kamera dan daftar gambar, baca [praproduksi](references/preproduction.md).
- Untuk dua mode gambar, batch, naturalitas dan review, baca [alur gambar](references/image-workflow.md) dan [template gambar](assets/image-prompt-template.md).
- Untuk sembilan bagian R2V, penyerahan/revisi dan sesi baru, baca [panduan Omni Flash](references/omni-flash.md) dan [template R2V](assets/prompt-template.md).

## Mulai, lanjutkan atau revisi

Kerjakan bagian yang diminta pengguna. Analisis sumber saja tidak memulai produksi lengkap. Pada proyek baru, ringkas brief dan tanyakan hanya keputusan yang mengubah hasil. Pada kelanjutan, baca project.json, keputusan percakapan dan aset asli; pertahankan persetujuan/delegasi yang masih berlaku.

Bedakan fakta sumber, dugaan analisis dan adaptasi desain. Confidence rendah tidak melarang memilih bahan baru. Jangan mengarang kutipan, ukuran fisik atau denah. Tidak ada human_verified atau kewajiban review manual setiap referensi.

Proyek schema 1.0 perlu ditinjau dalam salinan V2 bila diminta. Frame lama tidak otomatis menjadi gambar full area dan persetujuan visual lama tidak otomatis diteruskan. Jangan menimpa proyek V1 atau menambahkan menu produksi kolase/interpolasi ke V2.

Arahan terbaru pengguna menjadi pegangan. Perubahan aturan dicatat dan diterapkan pada versi kontrak/rules yang sesuai; jangan menyamarkan pelanggaran dengan evidence atau review palsu.

## Konsep dan rancangan satu rumah

Pilih referensi utama untuk bahasa video serta pendukung desain yang kompatibel. Pertahankan desain, tata ruang, plafon, bukaan, material, cahaya, lingkungan, framing, gerak, reveal dan ritme yang dipilih dari sumber. Tawarkan opsi bila konsep belum dipilih; jangan mengulang pemilihan yang sudah selesai.

Rancangan menetapkan plafon tiap area dan sambungannya, bukaan, furnitur utama serta elemen tetap. Perbedaan antararea yang memang dirancang boleh ada; jangan memaksa semua plafon identik. Posisi yang belum dibuktikan sumber dinyatakan sebagai keputusan proyek.

Susun shot tanpa cut dan tanpa pengungkapan area berulang. Bedroom/area tidur maksimal satu. Laundry, wardrobe, dining atau loft mengikuti pola sumber. Living-to-kitchen dan exterior-to-living masing-masing satu shot 6 detik, memakai dua gambar individual sesuai kedua areanya. Exterior 6 detik; shot area lainnya 4 detik. Jangan menumpuk dua penghubung yang mengulang living.

Tampilkan jumlah shot, daftar gambar area, pemetaan referensi dan total durasi. Empat shot exterior → living-to-kitchen → bedroom → bathroom berarti lima gambar dan 20 detik.

Kamera mencatat komponen, hubungan waktu, perkiraan jarak/sudut, bukti gerak dan alasan ritmenya masuk akal. Pan/orbit yang dipilih minimal 12°. Jangan menambahkan rotasi pada translasi murni. Maju sambil pan berjalan bersamaan; maju lalu pan mempunyai fase berurutan. Sesuaikan jarak/fase dengan durasi, bukan sekadar menambahkan kata slow.

## Dua mode gambar

Setelah desain/shot disetujui atau didelegasikan, gunakan image_mode yang dipilih pengguna. Minta pilihan hanya jika belum tersedia.

- prompt_to_image: serahkan seluruh prompt individual; satu prompt untuk satu gambar. Jangan otomatis generate. Gambar hasil alat pengguna dibaca saat tersedia sebelum review dan prompt video final.
- generate_image: buat seluruh gambar area individual sekaligus sesuai rancangan. Tujuh berarti tujuh file, bukan satu kolase atau hasil yang berhenti setelah satu area. Satu per satu hanya jika diminta spesifik pengguna.

Gunakan spesifikasi rumah yang sama pada seluruh prompt. Periksa cakupan luas, naturalitas, plafon dan hubungan ruang dari piksel aktual. Gambar referensi tidak wajib menjadi komposisi awal/akhir video; jangan memaksanya dengan crop 9:16 yang membuang informasi.

Catat image_batch dari pelaksanaan yang benar-benar diamati atau laporan pengguna. Jangan memberi execution: parallel hanya karena prompt meminta batch, karena file berjumlah tujuh, atau karena tes kode lulus. Bila alat menunjukkan batas/kegagalan, catat unknown/failed sesuai fakta, laporkan temuan, dan pertahankan image_draft. Jangan diam-diam beralih ke alur satu per satu atau API berbayar.

## Gambar final dan prompt R2V

Lihat gambar individual dan bandingkan seluruh area sebagai satu rumah. Dua referensi penghubung harus menggambarkan hubungan ruang yang sama. Perubahan struktur, plafon atau material yang tak direncanakan direvisi sebelum final. Tidak perlu meminta persetujuan setiap gambar satu per satu.

Setelah paket gambar direview dan disetujui/didelegasikan, isi sembilan bagian prompt R2V dari gambar dan rancangan yang sama. Jelaskan peran setiap ID gambar sebagai identitas area, perjalanan kamera, bukti gerak dan komposisi akhir. Jangan memakai referensi sebagai kontrol first/last frame wajib atau menutupi perbedaan ruang dengan morphing.

Durasi mengikuti shot, video 9:16, satu continuous shot, ambient halus tanpa musik/narasi/dialog/efek dramatis. Cut antarklip berada di panduan perangkaian, bukan instruksi di dalam shot. Periksa isi prompt secara utuh; pencantuman instruksi wajib tidak membuktikan semua kalimat sudah selaras.

## Keputusan dan penyerahan

Tiga titik keputusan: konsep, desain/shot dan paket gambar final. Delegasi tetap berlaku. Pilihan mode gambar tidak menambah persetujuan per area. Catat keputusan/review hanya berdasarkan tindakan atau arahan yang sebenarnya.

Simpan satu project.json aktif. Pada perencanaan, gambar belum wajib. image_prompt_package boleh tanpa aset, tetapi tidak disebut siap R2V. image_final dan prompt_package memerlukan file asli, revisi yang cocok dan review. Jalankan validator dengan file proyek; [dependensi](scripts/requirements.txt) menjelaskan kebutuhan runtime.

Ekspor melalui [pembuat paket](scripts/build_production_package.py). Serahkan panduan, catatan, prompt gambar dan—untuk paket R2V—gambar individual serta prompt video per shot. Pakai tautan unduhan host; nama file atau tautan lama belum membuktikan file tersedia.

Pada revisi, tinjau area/shot terdampak dan naikkan revisi keputusan bila berubah. Jangan mengganti nomor versi aset lama untuk menyamarkan data usang. Pada sesi baru, minta hanya catatan/aset yang hilang. Tinjau video/audio hanya jika benar-benar dapat dilihat/didengar; jangan menyatakan penerimaan lulus dari JSON.
