# Brief, satu tata ruang dan shot

Baca [aturan](production-rules.yaml), [kontrak](project-contract.md) dan [akses sumber](repo-access.md). Gunakan anotasi tersimpan secara selektif melalui web/konektor. Tidak menyalin pustaka atau menganalisis ulang seluruh video.

## Konsep dan rumah yang sama

Ringkas brief, skala, suasana, lingkungan dan area yang dibutuhkan. Pilih acuan utama untuk bahasa video dan pendukung desain yang kompatibel; catat bukti serta adaptasi. Jangan mengulang pemilihan yang sudah selesai.

design menetapkan bentuk, atap, material, tata ruang, plafon, lampu, bukaan, furnitur, cahaya dan lingkungan. connections/anchors menjaga sambungan serta elemen tetap. area_specs menetapkan satu posisi/plafon/armatur untuk setiap area yang akan dicakup video, termasuk area yang belum terlihat pada foto.

Kitchen merupakan satu zona di satu lokasi; bukan satu di depan dan satu lagi di kanan. Kiri/kanan pada frame bergantung pada posisi/arah kamera, bukan perubahan lokasi ruang. Denah baru adalah keputusan proyek; urutan shot tidak membuktikan denah sumber.

Setiap interior mempunyai armatur yang logis untuk fungsi/desainnya. Nyatakan jenis/posisi serta cahaya siang/nyala yang dirancang. Tidak wajib semua lampu menyala. Plafon boleh berbeda antararea bila memang dirancang, tetapi plafon/lampu pada area yang sama tidak berubah antarview. Jangan menambahkan balok/ornamen/pintu hanya untuk membuat penanda.

## Pilih cakupan dan referensi

Satu shot kontinu tanpa cut. Area yang sudah diungkap tidak diulang; background konteks tidak otomatis menjadi area baru. Maksimal satu bedroom/fungsi tidur, termasuk loft. Laundry/wardrobe/dining/loft/fungsi terpadu hanya dari pola sumber yang relevan.

image_plan adalah daftar pandangan individual, bukan kuota satu gambar untuk setiap label fungsi. Peta reference_image_ids dan shot_ids harus sama.
- Living-to-kitchen: default satu foto utuh memperlihatkan kedua area terhubung. Tidak perlu gambar kitchen khusus atau shot kitchen sesudahnya.
- Exterior-to-living: pengguna memilih **1 atau 2 referensi**. Pilihan dicatat di reference_choice; jangan mewajibkan dua atau memaksakan satu.
- Jika satu pada exterior-to-living, pilih referensi utama sesuai lintasan, umumnya exterior/pintu masuk. Interior tidak wajib terlihat penuh pada foto yang sama; bagian tersembunyi tetap mempunyai rancangan.
- Jika dua, gunakan exterior dan living individual dari rumah yang sama; review hubungan pintu, lantai, plafon dan orientasi. Jangan menyamarkan file identik sebagai dua pandangan.
- Fungsi terpadu lain mengikuti pemetaan yang disetujui; banyaknya label fungsi tidak otomatis menambah ruang/gambar/shot.

Tanyakan pilihan exterior-to-living hanya jika diperlukan dan belum ada; pertahankan jawaban/delegasi. Pilihan jumlah bukan mode video baru. R2V tetap metode video; dua mode gambar hanya mengatur cara memperoleh gambar.

| Pola | Shot | Gambar | Durasi |
| --- | --- | --- | --- |
| Exterior + living + kitchen + bedroom + bathroom | 5 | 5 | 22 detik |
| Exterior + living-to-kitchen + bedroom + bathroom | 4 | 4 | 20 detik |
| Exterior-to-living + kitchen + bedroom + bathroom | 4 | 4 atau 5, sesuai pilihan 1/2 referensi | 18 detik |
| Tambahan laundry pada pola 20 detik, bila didukung sumber | 5 | 5 | 24 detik |

## Posisi kamera → gambar → lintasan → akhir

Tetapkan posisi, arah pandang, tinggi dan komposisi berdasarkan tata ruang. Isi composition pada gambar dan camera.spatial_plan pada shot; keduanya merujuk keputusan yang sama. framing.start/end menjelaskan hasil pandangan, bukan kewajiban memakai referensi sebagai endpoint.

Contoh masalah: gambar memperlihatkan kitchen di depan, sementara teks gerak menganggap kitchen baru berada di kanan. Periksa posisi/arah kamera dan bidang pandangnya dahulu; pan kanan tidak otomatis salah. Jika lintasan tidak mendukung akhir yang diinginkan, ubah komposisi/posisi kamera atau rute yang kompatibel dengan DNA/desain. Jangan memindahkan/menambah kitchen atau hanya mengandalkan kalimat no duplicate kitchen.

Gambar R2V tidak harus sama dengan frame awal/akhir. Namun jangan meminta lintasan yang bertentangan dengan hubungan ruang yang terlihat. Untuk area tersembunyi pada satu referensi exterior-to-living, jelaskan sambungan dan desain interior secara jujur; foto tidak membuktikan detail yang belum terlihat.

### Bedroom sesuai preferensi

Pilih acuan bedroom yang mendukung front three-quarter dan bed memanjang diagonal. Sasaran sudut 35–45° di bidang horizontal terhadap sumbu panjang bed, bukan sudut kemiringan piksel/roll. Pilih sisi kamera kiri/kanan yang cocok dengan rancangan; pindahkan posisi/arah kamera, bukan memutar bed.

Rentang tersebut adalah preferensi produksi pengguna. Anotasi edh058/shot-04 mendukung keluarga front three-quarter; edh056/shot-04 hampir frontal. Jangan menyatakan semua referensi memakai 35–45° atau memaksakan framing frontal hanya karena satu sumber utama frontal. Bedakan adaptasi pandangan dari fakta sumber.

## Gerak mengikuti sumber dan durasi

Pilih gerak per area: dolly maju/mundur, tracking lateral, pan, orbit atau tilt bila sesuai sumber dan geometri. Tidak selalu dolly + pan; gerak tunggal sah. Catat acuan gerak serta adaptasinya.

components mencatat kind translation/pan/orbit/tilt, description, start_s, duration_s, distance_m dan angle_deg. Translasi memakai jarak positif; pan/orbit terpilih ≥12°, tilt tidak otomatis mewarisi batas itu. Angka adalah perkiraan proyek, bukan pengukuran sumber.

single satu komponen sepanjang shot. simultaneous dua atau lebih sepanjang waktu yang sama. sequential fase tersambung tanpa overlap/jeda tak tercatat, total tepat durasi. Label gerak gabungan sumber belum membuktikan hubungan waktunya.

Exterior dan kedua penghubung 6 detik; area/fungsi terpadu lain 4 detik. Sesuaikan jarak, sudut, kompleksitas dan ritme: jangan meminta slow untuk jalur panjang/banyak fase dalam 4 detik. Perubahan material pada rancangan yang sudah disetujui kembali ke review, tanpa diam-diam menghilangkan komponen sumber.

visible_motion_evidence menyebut perubahan pada elemen yang ada: perspektif/foreground saat maju, sisi ruang saat pan, atau parallax saat orbit. Setiap komponen gabungan harus mempunyai bukti yang dapat dinilai. Pan bukan orbit, zoom digital atau roll; rumah/furnitur tidak diputar untuk meniru kamera.

## Menyerahkan rancangan

Tampilkan desain, acuan, area, shot/durasi, gambar/peta lampiran, komposisi/lintasan dan jumlah total sebelum generate. Jangan menambah area untuk memenuhi angka tujuh gambar atau durasi video sumber.

Stage concept setelah konsep dipilih; shot_plan saat rancangan lengkap. Sesudah persetujuan/delegasi desain, gunakan pilihan image_mode yang berlaku lalu lanjutkan [gambar](image-workflow.md). Catatan/persetujuan hanya dari keputusan nyata. Checkpoint internal tidak menjadi penghalang pembahasan jika gagal disimpan.
