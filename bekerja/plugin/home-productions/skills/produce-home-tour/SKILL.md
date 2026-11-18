---
name: produce-home-tour
description: Susun brief, konsep rumah, continuous shot, pasangan frame dan prompt video Omni Flash berbasis pustaka HOMEKU. Gunakan untuk memulai, melanjutkan atau merevisi proyek home tour sampai paket produksi; analisis referensi saja tidak memulai produksi lengkap.
---

# Produksi home tour

Bantu pengguna menetapkan satu rumah dan cara mengungkapnya mengikuti DNA desain serta video referensi. Keluaran mencakup konsep, rancangan shot, pasangan frame final dan paket prompt per shot yang dapat dibawa ke sesi lain.

## Sumber kerja

- Baca [aturan produksi](references/production-rules.yaml) saat membuat atau merevisi proyek. Ini sumber durasi, jenis/cakupan shot, audio dan batas area.
- Baca bagian tahap/revisi pada [kontrak proyek](references/project-contract.md) sebelum mengisi catatan proyek. [Template](assets/project-template.json) dipakai saat proyek baru; [schema](assets/project.schema.json) membantu mengoreksi data bila diperlukan.
- Saat mengambil pengetahuan, gunakan [akses repo](references/repo-access.md). Pustaka dibaca melalui URL web atau konektor GitHub; tidak memerlukan clone, indeks lokal atau API pencarian khusus.
- Saat menyusun konsep dan shot, baca [panduan praproduksi](references/preproduction.md).
- Saat membuat, merevisi atau memotong gambar, baca [alur visual](references/image-workflow.md).
- Saat menyusun prompt, menyerahkan paket atau merevisi hasil, baca [panduan Omni Flash dan paket](references/omni-flash.md). Muat rincian sesuai tugas, bukan semua file repo sekaligus.

## Memulai atau melanjutkan

Pahami permintaan saat ini dan batas pekerjaan yang sudah diizinkan. Jika pengguna hanya meminta brief, pilihan konsep, revisi shot atau crop aset yang tersedia, kerjakan bagian itu. Untuk analisis sumber saja, jawab analisis tanpa membuat proyek produksi.

Pada proyek baru, rangkum brief dan hal penting yang belum diketahui. Tanyakan hanya keputusan yang mengubah arah hasil; pilihan rutin dapat diajukan sebagai asumsi yang terlihat. Jangan menambah ruang, jumlah kamar atau pola shot yang tidak memiliki contoh sumber.

Pada kelanjutan, baca catatan proyek dan keputusan percakapan yang tersedia. Pertahankan konsep serta persetujuan yang masih berlaku. Minta hanya catatan/aset yang diperlukan tetapi belum tersedia; nama file bukan bukti file dapat dibuka. Jika hasil gambar asli tersedia langsung dari alat, gunakan tanpa meminta unggah ulang. Jangan mengulang pertanyaan yang sudah dijawab atau meminta persetujuan ulang atas langkah yang telah didelegasikan.

Arahan eksplisit terbaru pengguna menjadi pegangan. Bila arahan mengubah aturan baku, catat perubahan secara jelas dan sesuaikan kontraknya dalam cakupan yang diminta; jangan menyembunyikan pelanggaran dengan catatan sumber palsu atau menghapus error validator.

## Dari referensi ke rancangan

1. Ambil pengetahuan inti dan contoh yang relevan melalui jalur akses yang tersedia. Catat hanya isi yang benar-benar dikembalikan alat. Referensi yang gagal dibaca belum boleh mendukung klaim atau shot.
2. Pilih referensi utama untuk bahasa video serta pendukung desain yang kompatibel. Jelaskan bentuk, tata ruang, material, lighting, lingkungan, framing, gerak dan urutan yang diadaptasi. Confidence sumber membatasi klaim fisik, bukan kebebasan memilih bahan baru.
3. Tawarkan arah konsep yang cukup untuk membantu keputusan, misalnya tiga opsi bila pengguna masih menjelajah. Jangan memperbanyak opsi ketika konsep sudah dipilih. Catat konsep terpilih setelah pengguna memilih atau memberi delegasi.
4. Tetapkan spesifikasi satu rumah dan elemen tetapnya. Bedakan fakta sumber dengan keputusan desain proyek; urutan edit tidak membuktikan denah atau adjacency.
5. Susun daftar shot kontinu tanpa cut dari pola yang didukung sumber. Catat area yang sudah tercakup setelah setiap shot. Living-to-kitchen mencakup keduanya; exterior-to-living mencakup exterior dan living. Jangan menambah pengungkapan area yang sama, bedroom lain, atau cut hanya karena label ruang berganti.
6. Isi framing awal–akhir dan gerak dengan jelas. Bedakan maju sambil pan dari maju lalu pan; daftar label kamera belum memastikan urutan waktunya. Pertahankan proporsi, cahaya, dunia luar jendela dan lintasan yang masuk akal.
7. Terapkan durasi dan audio dari aturan. Tampilkan total hasil penjumlahan; jangan mempercepat atau memangkas otomatis untuk mengejar durasi referensi.

## Dari rancangan ke visual

Setelah desain dan daftar shot disetujui atau didelegasikan, lanjutkan dengan satu kolase per shot sesuai alur visual. Kiri adalah awal, kanan adalah akhir; dua panel sama besar, masing-masing 9:16, tanpa teks, garis atau bingkai. Sertakan acuan rumah yang sudah diperiksa melalui mekanisme gambar alat yang tersedia.

Periksa konsistensi dalam pasangan dan antarshot sebelum menentukan crop. Potong file asli memakai [split_frames.py](scripts/split_frames.py), tanpa resize atau generate ulang. Ukuran aktual dan batas panel diperiksa; ketidaksesuaian tidak dibetulkan dengan peregangan atau crop sembarang. Lihat kedua hasil individu dan catat temuan nyata, termasuk bila detail/resolusinya belum cukup.

Gunakan visual_draft selama pengerjaan atau keputusan masih terbuka. Hubungkan dua aset ke shot serta revisi yang benar. visual_final memerlukan seluruh pasangan, review aktual dan persetujuan visual pengguna atau delegasi yang sudah berlaku. Script crop tidak memberi persetujuan atau membuktikan konsistensi rumah.

## Dari visual ke paket prompt

Lihat dua frame final setiap shot dan cocokkan dengan rancangan aktif. Susun prompt memakai [template](assets/prompt-template.md) serta panduan Omni Flash: subjek/cahaya, framing awal–akhir, lintasan, kecepatan, reveal dan elemen tetap. Bedakan gerak simultan/sekuensial secara eksplisit. Jangan memakai transformasi bentuk atau cut internal untuk menyambung dua gambar.

Gunakan durasi shot dan salin instruksi continuous shot serta ambient tanpa musik dari aturan ke setiap prompt. Pasangkan ID aset, nama file dan revisi yang benar; isi seluruh penanda template. Catatan cut antarklip terpisah dari prompt satu continuous shot.

Validasi prompt_package beserta file asli, lalu ekspor dengan [pembuat paket proyek](scripts/build_production_package.py). Helper menyalin keputusan, gambar dan prompt yang sudah selesai; ia tidak membuat persetujuan atau menulis isi kreatif. Serahkan panduan produksi, project.json, prompt tiap shot dan dua tautan frame individu. Jangan menyebut paket dapat dilanjutkan bila gambar aslinya belum tersedia.

## Keputusan dan penyerahan

Tiga titik keputusan adalah pilihan konsep, persetujuan desain beserta daftar shot, dan paket visual final. Pengguna tidak wajib menyetujui setiap kolase satu per satu. Catat persetujuan hanya dari instruksi pengguna atau delegasi yang benar-benar diberikan.

Simpan catatan proyek sesuai kontrak. Pada keluaran praproduksi, assets tetap kosong, frames setiap shot null dan prompt null. Pada produksi visual, catat file/metadata aktual dan ikat frame ke shot sesuai alur visual. Pada paket akhir, ikat prompt lengkap ke revision, duration_s dan dua asset_id yang sama; gunakan prompt_package setelah seluruh prompt selesai. Jangan menambahkan field bebas untuk menghindari aturan.

Jalankan [validator](scripts/validate_project.py) pada project.json dengan lingkungan pemrosesan yang tersedia; [dependensi](scripts/requirements.txt) menjelaskan kebutuhan alat. Jika tidak dapat menjalankannya, nyatakan pemeriksaan otomatis belum dilakukan dan jangan mengarang hasil lulus.

Serahkan ringkasan rumah, asal DNA, daftar shot, cakupan area, durasi dan total, serta catatan proyek yang bisa diunduh bila alat file tersedia. Untuk keluaran visual, berikan tautan individu frame awal dan akhir setiap shot beserta ukuran dan ringkasan review. Jelaskan keputusan yang masih menunggu pengguna. Keluaran valid secara struktural belum membuktikan mutu geometri atau kepastian sumber.

Pada revisi hasil, periksa hanya media yang dapat dibuka dan audio yang dapat didengar. Perubahan elemen tetap memicu peninjauan shot terdampak; ikuti panduan paket untuk revisi dan kelanjutan sesi. Skill menyiapkan produksi; generate Omni Flash, perangkaian klip dan publikasi Facebook dijalankan pengguna.
