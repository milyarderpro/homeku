# Kolase, konsistensi dan dua frame individu

Gunakan setelah konsep serta desain/daftar shot disetujui atau didelegasikan. Baca [kontrak proyek](project-contract.md) dan pertahankan [aturan produksi](production-rules.yaml). Produksi visual tidak mengubah cakupan, jumlah bedroom, durasi atau audio proyek.

## Menyiapkan acuan dan generate

Baca keputusan rumah, framing, lintasan dan elemen tetap dari catatan aktif. Pastikan gambar acuan benar-benar dapat dibuka. Ketika sumber gambar perlu diambil dari HOMEKU, ikuti [akses repo](repo-access.md); jangan mengklaim gambar telah dilihat hanya karena URL atau namanya diketahui.

Gunakan alat generate/edit gambar yang tersedia pada host. Sertakan gambar acuan melalui mekanisme lampiran/acuan alat yang sebenarnya; nama file dalam prompt saja tidak memasukkan piksel. Untuk kolase berikutnya, sertakan gambar proyek yang sudah diperiksa dan disetujui atau dipilih dalam delegasi pengguna, bersama spesifikasi rumah yang sama. Jangan mengandalkan ingatan model atas gambar sebelumnya atau mewajibkan paket gambar seluruh area di awal.

Satu shot menghasilkan satu kolase dua panel berdampingan:

- Kiri frame awal; kanan frame akhir. Dua panel sama besar, masing-masing vertikal 9:16; kanvas gabungan ideal 9:8.
- Batas lurus tanpa celah, garis pemisah, teks, label, border, letterbox atau hiasan.
- Spesifikasi rumah, material, bukaan, furnitur, cahaya dan lingkungan tetap sama pada kedua panel.
- Kedua pandangan sesuai framing serta lintasan shot. Pada exterior-to-living atau living-to-kitchen, awal dan akhir boleh berada pada fungsi berbeda yang terhubung sesuai rancangan.
- Ukuran diminta mengikuti kemampuan alat dan kebutuhan keluaran. Ukuran aktual harus dibaca dari file, bukan disalin dari prompt.

Susun instruksi gambar dari identitas rumah, acuan yang terlampir, kondisi cahaya/lingkungan, uraian panel awal dan akhir, serta elemen tetap. Jelaskan pergeseran sudut pandang karena kamera; jangan meminta transformasi rumah sebagai pengganti gerak.

Gunakan file kolase asli dari hasil alat. Jika file dapat diproses langsung, lanjutkan tanpa meminta pengguna mengunggah ulang. Preview saja belum membuktikan file tersedia. Jika akses file atau alat pemrosesan belum ada, laporkan bagian yang belum selesai; jangan mengganti dua frame dengan kolase utuh.

## Review visual dan revisi

Lihat kolase sebelum menentukan crop. Periksa pula hasil crop individu, dengan dua tingkat konsistensi:

| Pemeriksaan | Yang dibandingkan |
| --- | --- |
| Dalam shot | Geometri, posisi relatif pintu/jendela, furnitur, material, cahaya dan pandangan luar yang sama ketika kamera bergerak |
| Antarshot | Identitas satu rumah, keluarga bukaan, palet/material, hubungan ruang yang dirancang serta lingkungan luar jendela |
| Gerak | Frame awal–akhir memungkinkan lintasan dalam durasi shot; maju sambil pan berbeda dari maju lalu pan |
| Panel dan mutu | Urutan kiri/kanan, batas panel, garis/teks tersisa, ketajaman dan detail yang tersedia |

Jangan menolak perpindahan exterior–living hanya karena dua frame memperlihatkan area berbeda. Nilai apakah sambungan dan elemen tetap sesuai rancangan. Dua gambar tidak membuktikan semua geometri yang tidak terlihat atau menjamin gerak video nantinya.

Jika elemen berubah tanpa alasan, revisi kolase memakai acuan dan keputusan yang masih berlaku. Pertahankan bagian yang sudah benar. Perubahan keputusan rumah mengikuti revisi proyek dan peninjauan shot terdampak; jangan menimpa aset lama lalu menyebutnya versi baru. Jika percobaan masih bermasalah, laporkan temuan spesifik dan keputusan yang diperlukan sebelum mencoba lagi.

Review dilakukan AI dari gambar yang benar-benar dilihat, atau dicatat sebagai laporan pengguna. Ini bukan kewajiban review manual setiap referensi dan tidak menambahkan human_verified.

## Memotong tanpa resize

Jalankan [split_frames.py](../scripts/split_frames.py) pada lingkungan pemrosesan file yang tersedia. Dependensi memakai [requirements.txt](../scripts/requirements.txt). Script tidak mengakses jaringan, generate gambar, mendeteksi batas secara otomatis atau memberi persetujuan visual.

Dari root paket, contoh untuk kolase dengan dua panel 9:16 tepat yang sudah dilihat:

~~~sh
python skills/produce-home-tour/scripts/split_frames.py /path/to/project/collage.png --output /path/to/project/frames/r1 --shot-id shot-01
~~~

Mode standar membagi di tengah hanya jika lebar genap dan kedua bagian tepat 9:16. Jika tidak, script berhenti. Setelah memeriksa gambar, berikan kedua kotak crop secara eksplisit dengan koordinat LEFT TOP RIGHT BOTTOM; kanan/bawah eksklusif. Kotak wajib sama ukuran, 9:16, tetap di dalam kanvas dan di sisi panel yang sesuai.

Contoh khusus kolase pilot 1330 × 1182 yang batasnya sudah diperiksa; jangan memakai angka ini untuk gambar lain:

~~~sh
python skills/produce-home-tour/scripts/split_frames.py /path/to/project/collage.png --output /path/to/project/frames/r1 --shot-id shot-01 --start-box 4 7 661 1175 --end-box 669 7 1326 1175
~~~

Hasil contoh itu 657 × 1168 per frame. Kotak eksplisit boleh membuang inset kecil setelah diperiksa, tetapi jangan memotong elemen penting, mencampur panel, mempertahankan garis pemisah atau mengubah framing yang disetujui. Jika perlu membuang bagian penting, revisi sumber. Tidak ada inset otomatis, resize, peregangan atau generasi ulang dalam script.

Keluaran: shot-01-start.png, shot-01-end.png dan shot-01-split.json. Laporan berisi ukuran aktual, kotak crop, hash sumber/hasil dan pemeriksaan kesamaan piksel. File yang sudah ada tidak ditimpa; gunakan folder revisi baru untuk penggantian. Beberapa shot dapat ditulis ke folder yang sama.

Jika proyek memiliki target lebar minimum, gunakan --min-frame-width sesuai keputusan tersebut. Hasil di bawah target ditandai dalam warnings dan resolution_target_met: false; tidak di-upscale atau otomatis menjadi final. Tanpa target, nilainya null, bukan bukti resolusi produksi sudah layak. Periksa ketajaman/detail aktual; jika belum cukup, nyatakan keterbatasan dan revisi sumber. Crop tidak menambah detail.

## Catatan proyek dan penyerahan

Pertahankan stage: visual_draft selama gambar atau keputusan visual masih dikerjakan. Simpan file proyek/aset pada folder proyek host; saat mengembangkan di repository, gunakan runs/ yang diabaikan Git.

Untuk setiap frame, catat asset_id unik, shot_id, revision aktif, role, path relatif dari folder project.json, SHA-256, width dan height hasil aktual. Pasangkan ID tersebut ke shots[].frames.start/end. Path file pada laporan crop relatif terhadap folder keluaran crop; sesuaikan menjadi path relatif proyek ketika memasukkannya ke assets.

Laporan crop tidak memberi status reviewed. Setelah kedua potongan benar-benar dilihat, isi reviewed, review_origin: ai_visual atau user_report, serta review_note yang menyebut temuan dan cakupan pemeriksaan. Jika kolase dicatat sebagai aset, salin aslinya ke dalam folder proyek dan gunakan role: collage. Kotak crop/asal piksel tetap tersimpan pada laporan pendamping; kontrak proyek tidak perlu field bebas baru.

Saat seluruh pasangan lengkap, hasil review sesuai dan pengguna menyetujui paket visual atau telah mendelegasikannya, catat approvals.visual pada revisi aktif dan gunakan stage: visual_final. Persetujuan paket akhir adalah titik keputusan ketiga; tidak harus meminta persetujuan setiap kolase satu per satu. Persetujuan tidak diciptakan oleh script.

Jalankan [validator proyek](../scripts/validate_project.py) dengan project.json dan file asli di folder proyek. Periksa juga semua gambar sebagai satu rumah; validasi hash/dimensi tidak menggantikan review ini. Bila alat tidak tersedia, nyatakan pemeriksaan yang belum dilakukan.

Serahkan tautan individual frame awal dan akhir untuk setiap shot, ukuran aktual, ringkasan review serta catatan proyek. Gunakan mekanisme file unduhan host; jangan hanya menampilkan kolase atau nama file. Pastikan file dapat dibuka sebelum menyebutnya siap diunduh. Keberhasilan pengguna mengunduh baru boleh disebut jika benar-benar diamati atau dilaporkan. ZIP boleh ditambahkan, tetapi tidak menggantikan dua tautan individu.

Keluaran tahap visual adalah pasangan gambar dan catatan review. Setelah visual final, lanjutkan ke [prompt dan paket proyek](omni-flash.md) bila termasuk permintaan pengguna. Generate Omni Flash, perangkaian dan publikasi tetap dijalankan pengguna.
