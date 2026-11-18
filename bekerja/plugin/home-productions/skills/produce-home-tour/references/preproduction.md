# Menyusun brief, konsep dan daftar shot

Gunakan panduan ini untuk praproduksi baru atau revisi. Aturan mesin ada pada [production-rules.yaml](production-rules.yaml); struktur project.json ada pada [project-contract.md](project-contract.md). Jangan menyalin pustaka desain ke dalam paket skill.

## Brief dan pilihan

Rangkum arah desain, skala visual, suasana, lingkungan, area yang hendak ditampilkan dan target video. Bedakan kebutuhan yang sudah pasti dengan pertanyaan terbuka. Tidak ada kewajiban mengisi formulir panjang sebelum mulai mencari contoh.

Baca sumber yang relevan sebelum menawarkan konsep. Setiap opsi perlu menjelaskan:

- Identitas bentuk rumah, material/palet, lighting dan lingkungan.
- Hubungan fungsi ruang serta pola shot yang akan digunakan.
- Referensi utama/pendukung dan ciri yang diadaptasi.
- Perubahan kreatif yang dipilih dan hal yang belum diketahui.

Contoh jumlah opsi adalah tiga ketika pengguna masih memilih; itu bukan jumlah wajib. Jika konsep sudah dipilih atau pengguna meminta perbaikan kecil, pertahankan keputusan yang masih sesuai.

Sebelum pilihan ditetapkan, catat kebutuhan/opsi terbuka pada brief dan pertahankan stage: brief. Isi concept sebagai konsep pilihan dan naikkan stage: concept setelah pengguna memilih atau mendelegasikan pemilihan. Jangan menyimpan semua opsi seolah-olah sudah menjadi satu rumah yang disetujui.

Confidence rendah tentang material sumber tidak menghalangi memilih material untuk rumah baru. Pilihan tersebut dicatat sebagai keputusan proyek. Jangan menyatakan bahan atau geometri sumber sudah terverifikasi.

## Satu rumah yang koheren

Isi design.architecture, layout, materials, lighting, environment dan anchors. Tuliskan bentuk serta hubungan yang menentukan pandangan kamera, bukan daftar dekorasi saja.

- Arsitektur: massa, atap, proporsi dan keluarga bukaan sesuai acuan.
- Tata ruang: fungsi yang benar-benar dipilih, bukaan penghubung dan jalur kamera yang masuk akal.
- Material dan cahaya: tampilan, warna serta keadaan yang dipertahankan.
- Lingkungan: tanaman, cuaca visual dan pemandangan melalui jendela yang koheren.
- Anchors: elemen tetap seperti pintu, jendela, dinding fitur atau furnitur utama yang relevan pada sumber.

Bedakan ciri sumber dari adaptasi baru dalam uraian desain. Potongan video tidak menyediakan denah terukur; posisi yang diperlukan untuk rumah baru ditetapkan sebagai keputusan desain, tanpa menambah jenis/jumlah area di luar pola referensi. Kiri/kanan mengikuti pandangan kamera dan tidak menjadi arah tetap rumah.

## Daftar shot sebagai unit produksi

Untuk setiap shot, isi shot_id berurutan, kind, covered_areas, duration_s, continuous, evidence_ids, framing, camera, frames dan prompt sesuai template/schema.

Catat fungsi yang sudah diungkap setelah setiap shot, lalu pilih fungsi berikutnya yang belum tercakup. Satu ruang terbuka dapat mencakup beberapa fungsi; jangan menambahkan kitchen atau bedroom tersendiri setelah fungsi tersebut sudah diungkap dalam shot gabungan. Bedroom/sleeping loft dibatasi sesuai aturan, tanpa menambah kamar dengan mengganti namanya.

Tabel untuk pengguna berisi:

| Kolom | Isi |
| --- | --- |
| Shot dan jenis | Urutan serta pola satu gerakan kontinu tanpa cut |
| Cakupan | Area/fungsi yang sudah ditampilkan |
| Durasi | Nilai dari aturan dan total penjumlahannya |
| Awal–akhir | Subjek, sudut pandang, foreground, fokus dan informasi yang terungkap |
| Gerak | Perpindahan/rotasi kamera, kecepatan dan hubungan gerak |
| Acuan | ID referensi/shot serta kutipan/pointer yang mendukung |

Gerak simultan dinyatakan sebagai berjalan bersamaan, misalnya maju sambil pan. Gerak sekuensial menyatakan urutan, misalnya maju kemudian pan. Pilih motion_relationship: single, simultaneous atau sequential secara sesuai. Jangan menyatakan sumber membuktikan urutan waktu hanya dari daftar nama gerak; jika alokasi gerak merupakan adaptasi proyek, jelaskan.

Jarak perjalanan, framing dan reveal harus masuk akal dalam durasi baku. Tidak mengubah seluruh klip menjadi 4 detik, menambah shot pengulangan atau mempercepat otomatis demi total tertentu. Jika total yang diminta tidak cocok, tunjukkan hitungannya dan keputusan cakupan yang perlu dipilih pengguna.

Audio selalu mengikuti aturan proyek: cukup ambient halus tanpa musik. Musik atau transisi dramatis dari referensi tidak otomatis dibawa ke proyek.

## Keputusan, penyimpanan dan kelanjutan

Pilihan konsep dan persetujuan desain/daftar shot adalah dua titik keputusan praproduksi. Gunakan by: user untuk keputusan yang memang diberikan dan by: delegated untuk delegasi yang dinyatakan. Isi note dengan dasar keputusan yang sebenarnya; validator tidak memberikan persetujuan atas nama pengguna.

Naikkan revision ketika keputusan yang sudah disetujui berubah. Pengisian rancangan tahap berikutnya dalam keputusan yang sama tidak harus membuat revisi baru. Jangan menganggap pengisian JSON saja sebagai persetujuan.

Pada revisi, tinjau keputusan dan sumber yang terdampak. Pertahankan yang tidak berubah berdasarkan arahan yang sudah berlaku. Catat dasar penerusan keputusan pada revision_notes; jangan mengganti nomor revisi aset/prompt untuk menyamarkan data usang. Bila proyek sudah memiliki aset, minta berkas yang diperlukan untuk menilai dampaknya.

Keluaran tahap ini memakai stage: shot_plan. assets tetap [], frames.start/end null dan prompt null. approvals.visual tetap null karena gambar belum diperiksa. approvals.shot_plan boleh null sambil menunggu keputusan pengguna; jangan menyebutnya siap dieksekusi sebelum keputusan itu diberikan atau didelegasikan.

Simpan satu catatan aktif sesuai kontrak, dengan ringkasan yang mudah dibaca. Gunakan direktori proyek pada lingkungan kerja host; saat mengembangkan di repo ini, gunakan runs/ yang diabaikan Git. Jangan menulis file proyek ke pustaka sumber atau mengubah template paket menjadi proyek pengguna.

Jalankan validator pada catatan proyek. Perbaiki kesalahan data sesuai tahap, tanpa mengarang kutipan atau bukti sumber demi meluluskan pemeriksaan. Jika pemeriksaan tidak dapat dijalankan, sampaikan batasnya.

Serahkan konsep rumah pilihan, ringkasan DNA desain dan video, daftar shot beserta total, acuan dan adaptasi, serta catatan proyek. Jika alat file tidak tersedia, berikan isi catatan secara jelas dan nyatakan file unduhan belum dibuat. Tidak mengklaim kolase atau prompt video final sebagai hasil tahap ini.
