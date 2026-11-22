# Kosakata pencatatan

Gunakan label domain/subject/attribute yang konsisten untuk konsep yang sama. Nama gaya utama, pengaruh dan interior memakai bahasa Inggris; nilai penjelasan tetap bahasa Indonesia. Daftar berikut pedoman awal, bukan whitelist; label baru tetap boleh dicatat bila maknanya berbeda.

| Domain | Subject contoh | Attribute yang dianjurkan |
| --- | --- | --- |
| space | bathroom, kitchen, bedroom, living, exterior | layout, room-shape, combined-functions, circulation, floor-level |
| architecture | house, roof, canopy, window, doorway, ceiling | massing, shape, opening, position, structure-appearance |
| furnishing | shower, vanity, toilet, sofa, bed, coffee-table, refrigerator, range | type, shape, configuration, orientation |
| storage | cabinet, wardrobe, niche, shelf, laundry-tower | type, configuration, capacity-appearance |
| relation | subjek yang sama dengan benda terkait | position, alignment, adjacency-visible |
| material | wall, floor, countertop, facade, frame | appearance, physical-material |
| lighting | ceiling-light, task-light, niche-light, wall-light | type, placement, light-character |
| environment | site, landscape, exterior-view | visible-setting, vegetation, surface-condition |
| decoration | textile, artwork, plant, seasonal-decoration | type, pattern, placement |

Untuk hubungan, tulis jangkar dan perspektifnya, misalnya 'tower laundry di kanan shower menurut layar awal'. Jangan menulis 'di kanan' tanpa referensi yang jelas. Subject yang berulang tidak berarti objek identik lintas shot; ID fisik/adjacency hanya ditetapkan jika terlihat.

Pisahkan material appearance yang terlihat dari physical-material yang belum diketahui. Contoh 'tampak kayu cokelat' observed tidak membuktikan teak; physical-material dapat unknown. Jangan menerjemahkan state not-visible menjadi daftar barang yang tidak ada.

Label areas memakai fungsi eksplisit, misalnya bathroom; laundry bila keduanya tampak. Kabinet dalam bedroom bukan otomatis ruang walk-in closet. Jika variasi penting tidak cocok daftar ini, beri label baru yang spesifik dan pertahankan bukti/statusnya.


## DNA, alias dan notasi

Profil V2 mempertahankan seluruh aspek DNA kontrak 1.1: gaya/pengaruh, skala tampak, tingkat, massa/atap/entrance/porch/bukaan, material/palet/cahaya/lingkungan, konfigurasi/pembeda/kontinuitas. Nilai diskret ditulis per klaim dengan state/confidence/bukti. Gaya adalah interpretasi beralasan; tidak memastikan asal budaya/lokasi.

Alias eksplisit Indonesia/Inggris berada di data/taxonomy.json: area, gaya, skala, sudut, massa dan gerak. Nilai asli tidak diganti. Contoh american cattage → american cottage hanya normalisasi ejaan label eksplisit, bukan deteksi gaya dari benda. Label baru dan klaim nonpositif tetap tersedia.

Notasi kamera: Dolly-In/Out, Orbit Left/Right, Pan Left/Right, Truck Left/Right, Tilt-Up/Down, Pedestal Up/Down, Zoom-In/Out, Static atau Uncertain. Parser mengenali Tilt-Up dan Tilt Up tanpa mengubah teks literal. Label lain disimpan sebagai other beserta literalnya. Gentle/strong menjelaskan komponen, bukan otomatis tempo. Jangan memakai subtle tilt untuk drift/jitter kecil.

## Area dan kontinuitas V2

`area_ids` menunjuk area fisik; `functions` boleh lebih dari satu (bathroom + laundry tetap satu area bila satu ruang). `visible_intervals` dapat tumpang tindih; `route` hanya perjalanan yang benar-benar dilalui. Fase gerak bukan batas area, dan cut memulai shot baru. Tidak menyimpulkan koneksi denah dari urutan shot. Gunakan `style_names_language: "en"`, primary-style/interior-style serta klaim influence terpisah agar label dapat ditemukan tanpa sintesis AI.
