# Brief, satu rumah, shot dan daftar gambar

Baca [aturan produksi](production-rules.yaml) dan [kontrak](project-contract.md). Gunakan [akses repo](repo-access.md) untuk mengambil sumber. Runtime memakai URL web atau konektor GitHub, bukan salinan pustaka dalam plugin.

## Konsep dan desain

Ringkas brief, suasana, skala, lingkungan serta area yang diinginkan. Tidak perlu formulir panjang atau opsi baru ketika keputusan sudah tersedia. Pilih acuan utama untuk struktur video dan pendukung desain yang kompatibel; catat bagian sumber dan adaptasinya.

Isi design.architecture, layout, ceiling, materials, lighting, environment, connections dan anchors. Jelaskan hubungan yang menentukan pandangan kamera. Plafon mencakup bentuk/tingkat, sambungan, susunan lampu dan balok bila memang dirancang. Jangan menambahkan balok, pintu atau furnitur hanya untuk dijadikan penanda.

Connections menjelaskan hubungan ruang/bukaan pada rumah baru. Denah tidak disimpulkan hanya dari urutan shot. Kiri/kanan mengikuti pandangan kamera; elemen tetap berada pada posisi rumah yang sama. Perbedaan plafon antararea boleh mengikuti desain, tanpa berubah tak sengaja pada area yang sama.

## Shot dan kebutuhan gambar

Satu shot kontinu tanpa cut. Pilih jenis/cakupan yang didukung sumber, tandai fungsi yang sudah diungkap, lalu lanjutkan ke fungsi baru. Bedroom/sleeping loft tetap satu kelompok fungsi tidur. Jangan menambah dining/loft/laundry/wardrobe di luar pola referensi.

Daftar untuk pengguna memuat shot, cakupan, acuan, durasi, posisi/arah awal–akhir, gerak, bukti gerak dan daftar gambar. Hitung total sesudah cakupan ditetapkan. Jangan menyamaratakan menjadi 4 detik atau memangkas otomatis.

Buat image_plan berisi satu gambar aktif per area tujuan. reference_image_ids pada shot dan shot_ids pada gambar harus saling cocok. area_ids menyatakan fungsi yang memang ingin dijelaskan gambar; background insidental tidak otomatis menjadi tujuan baru.

Living-to-kitchen memerlukan primary_area living dan kitchen dalam dua gambar berbeda. Exterior-to-living memerlukan exterior dan living. Dua file identik tidak menggantikan dua pandangan area. Untuk fungsi terpadu, area_ids pada gambar dapat memuat beberapa fungsi sesuai rancangan; kebutuhan referensinya dipetakan eksplisit. Jangan menambah shot karena jumlah referensi lebih dari satu.

Contoh:
- Lima area terpisah: lima shot, lima gambar, 22 detik.
- Exterior + living-to-kitchen + bedroom + bathroom: empat shot, lima gambar, 20 detik.
- Exterior-to-living + kitchen + bedroom + bathroom: empat shot, lima gambar, 18 detik.
- Tambahan laundry pada contoh 20 detik: lima shot, enam gambar, 24 detik.

## Rencana kamera yang dapat diterapkan

camera.components menguraikan translation, pan, orbit atau tilt yang benar-benar dipilih, dengan description, start_s, duration_s, distance_m dan angle_deg. Angka merupakan perkiraan produksi, bukan hasil pengukuran sumber. Untuk translation, jarak positif diperlukan; pan/orbit minimal 12 derajat. Tilt tidak otomatis mewarisi batas pan.

single berarti satu komponen sepanjang durasi shot. simultaneous berarti dua atau lebih komponen berlangsung sepanjang durasi yang sama. sequential berarti dua atau lebih fase berurutan yang tersambung, totalnya tepat durasi shot. Catat timing_note dan visible_motion_evidence.

Bedakan posisi bergerak mengitari fokus (orbit), rotasi arah pandang (pan), dan pembesaran perspektif karena kamera mendekat. Jangan mengganti gerak kamera dengan memutar objek/rumah, zoom digital atau roll yang tidak diminta.

Untuk 4 detik, pilih lintasan pendek/komponen yang masuk akal; jangan menggabungkan jarak panjang, banyak fase dan kata slow tanpa alokasi waktu. Jika perlu mengubah rancangan yang sudah disetujui, jelaskan dampaknya. Tidak menambah/menghapus jenis gerak secara diam-diam.

Bukti gerak dipilih dari elemen yang ada: foreground membesar saat kamera maju, perspektif berubah saat orbit, sisi ruang/kitchen terungkap saat pan. Label gerak sumber belum membuktikan simultan/sekuensial; nyatakan pilihan waktu sebagai adaptasi bila sumber belum memastikan.

## Keputusan dan tahap

Sebelum konsep dipilih, stage brief; sesudah dipilih/didelegasikan, concept; saat desain, shot, kamera dan image_plan lengkap, shot_plan. prompt gambar boleh belum lengkap dan aset belum ada pada perencanaan.

Sesudah desain disetujui, pilih image_mode sekali lalu lanjutkan [dua mode gambar](image-workflow.md). Catat approval concept/shot_plan sesuai keputusan/delegasi aktual. Jangan memalsukan persetujuan, bukti sumber atau gambar demi meluluskan validator.
