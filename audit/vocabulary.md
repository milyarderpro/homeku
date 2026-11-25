# Kosakata pencatatan

Aturan kamera di [visual-audit.md](visual-audit.md), contoh di [camera-cases.md](camera-cases.md). Tulis estimasi untuk setiap komponen yang besarannya dapat diperkirakan secara wajar. Label intensitas menjelaskan komponen gerak.

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


## Tipe rumah

Pilih tipe yang paling mewakili bangunan dari massa, tapak, akses, dan susunan ruang yang terlihat.

| Tipe awal | Petunjuk visual |
| --- | --- |
| Detached House | Rumah berdiri sendiri tanpa ciri tipe yang lebih spesifik. |
| Villa | Hunian yang ditata untuk privasi dan pemakaian ruang luar seperti teras, taman, atau area santai. |
| Cottage | Hunian kompak dengan karakter rumah pedesaan atau peristirahatan kecil. |
| Cabin | Hunian kecil dan sederhana yang dekat dengan lingkungan alam. |
| Bungalow | Rumah rendah dengan ruang utama pada satu lantai dan massa cenderung melebar. |
| Townhouse | Rumah dalam deretan yang memiliki akses masing-masing dan berbagi dinding sisi. |
| Semi-Detached House | Satu dari sepasang rumah yang berbagi satu dinding. |
| Duplex | Satu bangunan dengan dua unit hunian terpisah. |

Daftar ini terbuka. Gunakan label yang lebih mewakili sumber seperti `Tower House` jika bentuk menara mendominasi. Catat pilihan yang masuk akal sebagai `uncertain` saat cirinya mendukung lebih dari satu tipe. Jika video terlalu terbatas untuk memperkirakan tipe apa pun, gunakan `unknown`.

## DNA, alias dan notasi

Profil desain mencakup gaya/pengaruh, skala tampak, tingkat, massa/atap/entrance/porch/bukaan, material/palet/cahaya/lingkungan, konfigurasi/pembeda/kontinuitas. Nilai diskret ditulis per klaim dengan state/confidence/bukti. Gaya adalah interpretasi beralasan; tidak memastikan asal budaya/lokasi.

Alias eksplisit Indonesia/Inggris berada di data/taxonomy.json: area, gaya, skala, sudut, massa dan gerak. Nilai asli tidak diganti. Contoh american cattage → american cottage hanya normalisasi ejaan label eksplisit, bukan deteksi gaya dari benda. Label baru dan klaim nonpositif tetap tersedia.

Notasi kamera: Dolly-In/Out, Orbit Left/Right, Pan Left/Right, Truck Left/Right, Tilt-Up/Down, Pedestal Up/Down, Zoom-In/Out, Static atau Uncertain. Parser mengenali Tilt-Up dan Tilt Up tanpa mengubah teks literal. Label lain disimpan sebagai other beserta literalnya. Gentle/strong menjelaskan komponen, bukan otomatis tempo. Jangan memakai subtle tilt untuk drift/jitter kecil.

## Area, caption, dan kontinuitas

- Pakai nama area pendek berbahasa Inggris dengan Title Case, misalnya `Exterior`, `Living Room`, atau `Sleeping Loft`. Pakai `&` bila dua fungsi memakai ruang yang sama, seperti `Bathroom & Laundry`. Renderer memakai ` / ` saat menggabungkan area fisik terpisah, seperti `Open-Plan Living / Sleeping Loft`.
- Tulis setiap fungsi yang terlihat di `areas[].functions`. `Open-Plan Living` dapat mencatat `Living Room`, `Dining Area`, dan `Kitchen` bila semuanya tampak. Kabinet di kamar tidur saja belum mendukung fungsi `Walk-In Closet`.
- Pakai label teknis Inggris untuk nilai yang dipakai dalam filter, seperti `oblique` atau `walk-in shower`. Narasi dan uraian bukti memakai bahasa Indonesia. Gunakan label baru bila maknanya berbeda.
- Untuk panel antara pada shot multi-area, beri caption Inggris singkat dengan Title Case bila momennya jelas, misalnya `Facade Reveal` atau `Doorway`. Panel biasa memakai `Start`, `Middle`, dan `End`.

`area_ids` menunjuk area fisik; `functions` boleh lebih dari satu (bathroom + laundry tetap satu area bila satu ruang). `visible_intervals` dapat tumpang tindih; `route` hanya perjalanan yang benar-benar dilalui. Fase gerak bukan batas area, dan cut memulai shot baru. Tidak menyimpulkan koneksi denah dari urutan shot. Tulis nama gaya Inggris sebagai klaim terpisah pada design.styles.

## Camera Pattern dan tampilan

Depth_direction fase: IN, OUT, NO IN/OUT atau null ambigu. Pola per shot/video hasil helper, bukan field manual audit. Arah berubah dalam satu shot memakai →; antarshot memakai – dan pola campuran dikurung. Misalnya IN – (OUT → IN) – NO IN/OUT. Pan/orbit/zoom sendiri tidak menentukan kedalaman; ~× bukan tempo.

Overview adalah gabungan frame wide terpilih satu baris; Storyboard adalah seluruh kolase shot vertikal. Camera Start adalah awal sumber, composition_summary adalah paragraf pada frame Overview. Gunakan istilah Profil desain, Ukuran & proporsi, Shot Timeline, Overview, Storyboard, Shot Details, Framing & Lighting, Camera Movement, Tempo, Alur visual, Movement Timeline. Notasi English satu paragraf; nama area/gaya teknis English, uraian Indonesia.

Gunakan tiny, small, medium, atau large sebagai label skala bila dapat ditentukan. Nilai yang belum dapat diketahui dapat dicatat dengan state unknown. Gunakan facet_roles untuk menyebut peran pencarian yang memang dicatat, seperti layout, configuration, opening, atau circulation.
