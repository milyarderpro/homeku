# Rencana Peningkatan Pengetahuan HOMEKU

Disusun 17 November 2026. Status: rencana implementasi; tahap-tahap berikut belum dikerjakan. Dasar: 57 referensi aktif, 295 shot, dan 6.111 butir detail visual setelah perapian integritas sumber.

**Tujuan**

Membuat pengetahuan yang makin akurat dan mudah digunakan AI ketika koleksi berkembang menjadi ratusan referensi. AI perlu dapat menemukan contoh yang sesuai, menelusuri alasan ke sumber, membedakan fakta dari interpretasi, serta menyatakan ketidakpastian. Repo tetap menyimpan pengetahuan desain; penyusunan konsep proyek, keputusan produksi, dan prompt Omni Flash tetap dikelola master prompt atau skill plugin.

Menambah jumlah referensi memperluas cakupan. Akurasi membutuhkan bukti yang diperiksa, pengelompokan yang konsisten, dan evaluasi yang terpisah.

**Kondisi awal**

| Bagian | Kondisi |
| --- | --- |
| Integritas sumber | Selesai: sumber tersedia, fingerprint SHA-256, duplikat edh026 dihapus dan edh027 dipertahankan |
| Validasi struktur | Pemeriksaan paket dan regresi tersedia; hasil sebelumnya 95 tes lulus |
| Review isi | Review dilakukan oleh AI sebelum penyimpanan; pengayaan berikutnya memakai catatan review dan ketidakpastian tanpa syarat verifikasi manual |
| Indeks bukti | 23 record yang menjangkau 7 referensi dan 14 shot |
| Istilah | Banyak label gaya dan scene bebas; belum ada kamus normalisasi terstruktur |
| Pertumbuhan koleksi | Tes masih memiliki angka tetap 57/295 serta delapan grup profil |
| Pengetahuan ruang | Prinsip umum tersedia; relasi yang diamati belum menjadi data terstruktur yang merata |
| Pencarian AI | Katalog dan profil tersedia; belum ada evaluasi pencarian dan paket ekspor yang terukur |

**Kebijakan penggunaan kreatif**

Semua referensi tersimpan dapat menjadi inspirasi. Confidence dan status review menjelaskan kepastian klaim tentang sumber, bukan kelayakan atau izin menggunakan elemen desain. AI boleh memilih batu alam pada konsep baru meskipun komposisi permukaan sumber belum pasti. Keputusan desain baru harus dibedakan dari pengamatan sumber. Tidak ada syarat verifikasi manual; review tambahan dilakukan oleh AI untuk memperbaiki bukti atau pengayaan.

**Arsitektur pengetahuan yang dituju**

Sumber video/gambar → anotasi asli → pengayaan terstruktur dan catatan review → versi pengetahuan yang diterbitkan → indeks untuk konsumen AI.

Arsip sumber dapat terus bertambah. Versi pengetahuan hanya berubah setelah perubahan yang terkait diperiksa. Semua lapisan turunan menyimpan kaitan ke sumber dan versi anotasi; lapisan turunan dapat dibangun ulang. Tidak ada lapisan yang boleh mengubah tebakan menjadi observasi.

**Tahap 1 — Siapkan pertumbuhan koleksi dan kontrak data**

Tujuan: penambahan referensi tidak mematahkan tes karena angka tetap atau langsung mengubah pengetahuan yang telah diterbitkan.

Pekerjaan:
- Bedakan inventaris seluruh arsip dengan daftar referensi pada versi pengetahuan yang diterbitkan. Referensi baru boleh tersimpan sambil menunggu pengayaan/review.
- Ganti pemeriksaan jumlah tetap dengan pemeriksaan kelengkapan, kesesuaian ID, dan jumlah yang dihitung dari inventaris/versi terkait. Angka 57/295 tetap dicatat sebagai baseline historis.
- Ganti pembagian delapan grup profil yang kaku dengan profil per ID dan daftar isi yang dihasilkan otomatis. Tautan lama mendapat pemetaan agar tidak putus.
- Tetapkan kontrak data untuk sumber, observasi, review, normalisasi, klaim dan agregat.
- Pertahankan kompatibilitas analysis.yaml schema 2.1. Pengayaan awal disimpan sebagai berkas pendamping; migrasi skema asli hanya dilakukan jika benar-benar diperlukan.
- Hubungkan pembaruan manifest sumber dengan penambahan arsip secara deterministik, tanpa otomatis menerbitkan interpretasi baru.
- Uji satu penambahan, beberapa penambahan bersamaan, koreksi satu anotasi, penghapusan sumber, dan kemunculan kembali ID yang dipensiunkan.

Hasil: spesifikasi skema, indeks inventaris, manifest versi pengetahuan, dan tes yang dapat mengikuti pertumbuhan data.

Selesai ketika: sumber baru dapat masuk sebagai data yang menunggu review, pengetahuan terbit tetap konsisten, dan penghitungan tidak bergantung pada angka 57.

**Tahap 2 — Bangun kamus istilah dan pemetaan**

Tujuan: AI dapat menemukan pengetahuan yang setara meskipun istilah anotasinya berbeda.

Pekerjaan:
- Buat keluarga gaya, pengaruh gaya, jenis ruang, konfigurasi ruang, bentuk atap, bukaan, material appearance, pencahayaan dan gerakan kamera.
- Simpan label asli bersama label normalisasi; jangan mengganti label asli secara massal.
- Pisahkan dimensi yang bercampur. Contoh: jenis ruang living/kitchen, konfigurasi open_plan, dan fitur loft adalah tiga atribut berbeda.
- Simpan alias Indonesia/Inggris untuk pencarian.
- Beri status sementara pada istilah baru yang belum dapat dipetakan. Pemetaan ambigu perlu ditinjau; hindari pencocokan otomatis yang memaksakan kategori.
- Bedakan unknown, not_visible, not_applicable, dan data yang belum diisi.

Hasil: kamus istilah berversi dan hasil pemetaan untuk seluruh 57 referensi.

Selesai ketika: setiap label terpetakan atau masuk daftar ambigu yang terlihat jelas; pencarian sinonim mengembalikan contoh yang semestinya tanpa menghilangkan perbedaan desain.

**Tahap 3 — Tetapkan evaluasi awal dan tinjau kelompok percontohan**

Tujuan: membuktikan format baru meningkatkan mutu sebelum diterapkan ke seluruh koleksi.

Mulai dengan sekitar 10–15 referensi yang mewakili keluarga gaya, skala, konfigurasi, lingkungan, dan tingkat kesulitan berbeda. Jumlah ini usulan awal; pilihan final mengikuti hasil inventaris dan kamus. Jangan hanya memilih sumber yang paling kaya anotasinya.

Pekerjaan:
- Susun sekitar 30–50 pertanyaan evaluasi sebelum penyetelan pencarian. Pisahkan contoh untuk pengembangan dan contoh uji yang ditahan.
- Periksa anotasi terhadap gambar dan video asli. Klaim tentang gerak memerlukan pemeriksaan sepanjang shot.
- Catat observasi yang didukung, salah, ambigu, dan tidak dapat dipastikan.
- Simpan metode review, peninjau/model dan versinya, tanggal, bukti yang diperiksa, serta alasan koreksi.
- Pisahkan confidence dari status review. Catat review AI dan cakupannya tanpa flag verifikasi global; confidence tidak menjadi larangan memilih elemen untuk desain baru.
- AI memeriksa bukti sumber untuk koreksi dan jawaban acuan; catat ketidakpastian atau konflik yang belum dapat diselesaikan. Review tambahan bukan syarat memakai referensi tersimpan untuk inspirasi.
- Koreksi anotasi sumber melalui perubahan yang terlacak. Simpan hash/revisi anotasi yang diperiksa agar review dapat ditandai usang setelah perubahan.

Hasil: kelompok percontohan yang ditinjau, catatan perbedaan, contoh bukti terstruktur, serta evaluasi awal.

Selesai ketika: format menangani kasus benar, salah, ambigu dan unknown; review AI tercatat tanpa menciptakan kepastian baru yang tidak didukung sumber.

**Tahap 4 — Perkaya hubungan desain dan bukti temporal**

Tujuan: pengetahuan menjelaskan susunan dan perubahan visual, bukan hanya daftar objek.

Pekerjaan:
- Tambahkan relasi terstruktur: sofa menghadap fireplace; meja berada di antara sofa dan kabinet; jendela berada pada sisi ruang yang terlihat.
- Tandai sistem koordinat: kiri/kanan gambar, arah pandang kamera, atau orientasi rumah. Jangan mencampurkannya.
- Catat sambungan ruang dan pemandangan melalui bukaan hanya ketika didukung sumber. Potongan living lalu kitchen tidak otomatis membuktikan adjacency.
- Pisahkan elemen tetap, furnitur dan dekorasi; simpan bentuk, ukuran relatif, orientasi, oklusi, dan focal point yang terlihat.
- Untuk shot yang memerlukan penjelasan gerak, simpan frame awal–tengah–akhir atau timestamp bukti yang relevan. Jumlah frame mengikuti kebutuhan bukti.
- Bedakan gerak kamera, gerak objek, perubahan framing, dan transisi antarscene.
- Jangan mengisi panjang fokus, koordinat fisik, arah mata angin, dimensi atau denah dengan presisi yang tidak didukung.
- Catat konflik/kemungkinan artefak visual sebagai keterbatasan; sumber home-tour tidak otomatis membuktikan bangunan fisik yang koheren.

Hasil: data relasi dan bukti temporal yang dapat dirujuk per shot. Ini adalah deskripsi sumber, bukan denah baru atau instruksi video produksi.

Selesai ketika: pertanyaan relasi dapat dijawab dengan bukti atau unknown, dan perubahan sudut pandang tidak menghasilkan klaim posisi yang saling bertentangan.

**Tahap 5 — Perluas cakupan dan perbarui sintesis**

Tujuan: pengetahuan mewakili seluruh koleksi dan tidak terus bergantung pada sedikit contoh.

Pekerjaan:
- Terapkan format yang telah lulus percontohan ke 57 referensi secara bertahap, misalnya per kelompok 10–15 referensi.
- Pastikan setiap referensi memiliki profil, pemetaan istilah, status review dan bukti penting. Tidak perlu mengubah semua tag menjadi klaim terpisah jika tidak menambah nilai.
- Setiap klaim memperoleh ID stabil, sumber/shot, lokasi bukti, revisi sumber/anotasi, jenis klaim, confidence dan keterbatasan.
- Pertahankan OBSERVATION, AGGREGATE, INFERENCE dan DESIGN_PRINCIPLE sebagai kategori berbeda.
- Perbarui DNA tematik dengan pola pendukung, contoh pengecualian, syarat kompatibilitas dan batas penerapan.
- Agregat mencatat definisi yang dihitung, numerator, denominator dan versi dataset. Hitung berdasarkan sumber independen yang diketahui, bukan banyaknya tag atau pengulangan anotasi.
- Tambahkan deteksi kemiripan untuk video yang di-encode ulang, dipotong, atau memakai adegan yang sama. Hasil kemiripan menjadi kandidat review; jangan menghapus otomatis.
- Pantau keragaman gaya, skala, ruangan dan lingkungan agar penambahan referensi berikutnya mengisi kekurangan koleksi.

Hasil: cakupan seluruh koleksi yang terlihat dalam laporan, indeks bukti yang lebih merata, dan sintesis yang dapat ditelusuri.

Selesai ketika: semua referensi tercakup atau memiliki alasan penundaan yang eksplisit, dan ringkasan tidak menyamarkan sumber lemah sebagai pola yang kuat.

**Tahap 6 — Sediakan paket pengetahuan untuk pencarian AI**

Tujuan: master prompt atau plugin dapat mengambil pengetahuan yang relevan tanpa membaca seluruh repo.

Pekerjaan:
- Hasilkan indeks terstruktur per referensi, per shot, dan per klaim dari data yang telah diterbitkan.
- Sertakan style family, skala, ruang, konfigurasi, material appearance, mood, kamera, confidence, status review, ID bukti dan tautan gambar.
- Mulai dari filter metadata dan pencarian teks. Ukur hasilnya sebelum menambahkan pencarian semantik/embedding.
- Pisahkan unit pencarian yang cukup kecil untuk relevansi, tetapi tetap membawa konteks rumah dan sumbernya.
- Bedakan mode pencarian contoh desain dengan pencarian bukti faktual. Status review harus terlihat di keduanya.
- Ekspor hanya data yang diizinkan versi pengetahuan. Kecualikan requests, fixture tes, salinan YAML, rencana implementasi, dan instruksi operasional dari korpus pengetahuan AI.
- Paket dapat berupa JSONL/JSON dan Markdown yang dihasilkan otomatis. Mesin pencarian atau adapter layanan ditempatkan pada konsumen/plugin bila diperlukan.
- Uji konsumen yang hanya membaca teks dan konsumen yang dapat membuka gambar. Tautan gambar saja tidak berarti AI sudah melihat gambar itu.

Hasil: kontrak konsumsi pengetahuan, indeks yang dapat dibangun ulang, dan contoh pengambilan bukti.

Selesai ketika: pencarian menghasilkan sumber relevan beserta konteks dan ketidakpastiannya, tanpa mencampurkan dokumen operasional.

**Tahap 7 — Evaluasi rilis dan pemeliharaan berkelanjutan**

Tujuan: peningkatan jumlah data menghasilkan manfaat yang terukur dan tidak menurunkan mutu yang sudah ada.

Evaluasi mencakup:
- Ketepatan pencarian contoh dan sinonim, termasuk beberapa jawaban yang sama-sama valid.
- Apakah kutipan benar-benar mendukung jawaban, bukan sekadar menunjuk file yang ada.
- Kemampuan membedakan observasi, inferensi dan prinsip.
- Ketepatan menjawab unknown untuk denah, material, ukuran atau gerak yang tidak terbukti.
- Ketahanan terhadap referensi konflik, label ambigu, sumber duplikat dan data yang belum ditinjau.
- Keragaman hasil pencarian untuk pertanyaan yang luas.
- Dampak koreksi sumber: hanya indeks, review dan sintesis yang bergantung padanya yang ditandai untuk pembaruan.

Target awal yang diusulkan: 100% tautan/ID bukti valid; nol dugaan yang disajikan sebagai fakta sumber tanpa dukungan bukti; dan sedikitnya 90% pertanyaan pencarian berjawaban memiliki contoh relevan dalam lima hasil pertama. Ukuran dan target ini harus dikalibrasi setelah baseline; bukan hasil pengujian saat ini. Pertanyaan yang tidak memiliki jawaban dinilai terpisah.

Setiap rilis pengetahuan mencatat versi skema/kamus, daftar sumber dan revisinya, jumlah record, perubahan penting, hasil evaluasi dan keterbatasan. Review yang menyangkut anotasi berubah ditandai usang sampai ditinjau ulang. Koreksi faktual dapat diprioritaskan tanpa menunggu kelompok penambahan berikutnya.

Selesai ketika: build dapat diulang, perubahan dapat dibandingkan dengan versi sebelumnya, dan penurunan mutu terdeteksi sebelum indeks baru dipakai konsumen.

**Struktur tambahan yang diusulkan**

Nama berikut adalah usulan, belum merupakan file yang tersedia:
- schemas/: kontrak observasi, review, relasi dan versi pengetahuan.
- knowledge/taxonomy/: kamus dan alias.
- knowledge/reference-profiles/<reference_id>.md: profil per sumber.
- knowledge/enrichment/<reference_id>.yaml: normalisasi dan hubungan yang ditautkan ke sumber.
- knowledge/reviews/<reference_id>.yaml: catatan review dengan cakupan dan revisi.
- knowledge/evidence/: record bukti dengan ID stabil.
- knowledge/indexes/: ekspor pencarian yang dihasilkan otomatis.
- knowledge/releases/: manifest versi pengetahuan.
- evaluations/: pertanyaan acuan dan laporan evaluasi; dikecualikan dari korpus pengetahuan.

**Pembagian pekerjaan**

| Pelaksana | Tanggung jawab |
| --- | --- |
| Kode deterministik | Validasi skema/ID, hash, katalog, hitungan, deteksi perubahan dan pembangunan indeks |
| AI dengan akses visual | Usulan normalisasi, review visual yang dilabeli AI, relasi yang didukung dan usulan sintesis |
| AI peninjau pada evaluasi | Periksa dukungan bukti, klaim ambigu dan jawaban acuan; simpan alasan, cakupan dan ketidakpastian |
| Master prompt / skill plugin | Mengambil pengetahuan, merancang rumah baru, dan menerjemahkannya menjadi prompt generator |

**Urutan implementasi yang direkomendasikan**

Mulai tahap 1 dan 2. Lanjutkan percontohan tahap 3–4 sebelum mengubah seluruh koleksi. Perluas pada tahap 5, kemudian bangun dan evaluasi konsumsi AI pada tahap 6–7. Kerangka evaluasi disiapkan lebih awal pada tahap 3 agar menjadi pembanding sepanjang implementasi.

Pekerjaan dapat dibagi menjadi perubahan yang mudah diperiksa: (1) skema dan pertumbuhan koleksi; (2) kamus dan pemetaan; (3) percontohan review serta relasi; (4) perluasan bukti dan sintesis; (5) indeks, evaluasi rilis dan pemeliharaan. Setiap perubahan memiliki migrasi yang dapat ditelusuri dan tidak menambahkan aturan produksi video ke repo.

Tidak perlu menunggu ratusan referensi untuk memulai. Terapkan fondasi pada 57 referensi sekarang, lalu gunakan mekanisme yang sama setiap kali koleksi bertambah. Keberhasilan dinilai dari kualitas jawaban berbukti dan kemudahan pemeliharaan, bukan jumlah file atau panjang anotasi.
