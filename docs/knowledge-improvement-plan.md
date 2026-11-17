# Rencana Peningkatan Pengetahuan HOMEKU

Disusun dan diperjelas 17 November 2026. Tahap 1–6 memiliki implementasi dan kandidat publik pada branch codex/knowledge-stage-6-7. Tahap 7 mencakup audit, pemeliharaan dan uji akses terpandu dua jalur pada commit yang sama; benchmark AI independen belum dilakukan. Pengguna memilih cukup uji akses untuk tahap 7 saat ini. Dasar snapshot: 57 referensi, 295 shot, 6.111 detail visual. Review temporal 45 sumber tetap pending; uji akses tidak mengubah cakupan review isi.

**Kemajuan tahap 1–2**

- Inventaris sumber dan snapshot pengetahuan dipisahkan. Tes mengikuti manifest, bukan jumlah tetap referensi.
- Profil individual dan tautan kompatibilitas grup lama tersedia, dengan prototipe bacaan inti dan direktori untuk akses web/konektor.
- Kontrak JSON Schema mencakup sumber, snapshot, normalisasi, observasi, review AI dan agregat. Kontrak observasi/review/agregat menyiapkan tahap berikutnya; tidak ada review baru yang diklaim.
- Kamus versi 1.0.1 memuat 107 konsep dalam 11 dimensi dengan alias Indonesia/Inggris. Seluruh 57 referensi memiliki pemetaan yang menyimpan label sumber.
- Label parsial, ambigu dan belum terpetakan tetap terlihat dalam laporan cakupan; normalisasi leksikal tidak diklaim sebagai verifikasi visual.
- Penyimpanan paralel memperbarui inventaris setelah rebase tanpa menerbitkan pengetahuan baru.
- Pengujian lokal meliputi pertumbuhan arsip, koreksi anotasi, sumber hilang, snapshot/kamus immutable, pemetaan dan penyimpanan paralel. Smoke test web dan konektor untuk konten baru belum dijalankan karena perubahan belum dipush.
- Rincian pemakaian dan hasil tersedia di [pemeliharaan](knowledge-maintenance.md) dan [laporan tahap 1–2](stage-1-2-report.md).

**Kemajuan tahap 3–5**

- Bank 40 kasus dibekukan sebelum pengayaan: 24 development, 16 heldout. Baseline dan hasil terkini lulus 26/26 cek lokal; 14 jawaban acuan tidak diberi skor model konsumen.
- Dua belas pilot mencakup 59 shot. Review AI terikat hash sumber dan media, dengan cakupan yang tercatat serta versi build model null karena tidak tersedia.
- Seluruh 57 storyboard mendapat review ciri terpilih. Tersedia 885 sampel temporal untuk 295 shot; 12 sumber ditinjau pada sampel temporal, 45 lainnya diberi alasan pending.
- Paket bukti berisi 3.123 observasi dan 1.826 relasi literal yang menelusuri pointer anotasi. Koordinat dunia, denah dan adjacency lintas cut tidak ditebak.
- Agregat dan laporan keragaman menyertakan definisi, denominator, pendukung dan pengecualian. Tema desain terhubung ke sintesis seluruh korpus.
- Pemeriksaan kemiripan 62 video pada 900 sampel menghasilkan nol kandidat menurut ambang terlapor; tidak dianggap bukti bebas overlap dan tidak menghapus sumber.
- Tidak ada koreksi anotasi/video asli yang dipaksakan. Perbedaan alias scene disimpan sebagai discrepancy, bukan salah fakta yang sudah terbukti.
- Rincian cakupan, batas review dan langkah berikutnya: [laporan tahap 3–5](stage-3-5-report.md).

**Kemajuan tahap 6–7**

- Pintu masuk 228 kata, peta bacaan 326 kata dan inti 788 kata; tema serta contoh dibuka sesuai kebutuhan.
- Modul kontinuitas tersedia; profil 493–722 kata dan metadata pendukung dipisahkan secara penyajian. Bukti tetap pada path asli.
- Kandidat dipublikasikan pada branch uji; web dan konektor diuji pada commit 217c63a473f5b6d9d967b1cb3372dae355ffed8b.
- Kedua jalur membaca 32 path unik dan menghasilkan 40 respons berbukti. Masing-masing lulus 26 cek mekanis; 14 jawaban semantik tidak diberi skor independen.
- Probe pencarian belum menemukan hasil target; navigasi path langsung berhasil. Gambar benar-benar ditampilkan melalui konektor; visual melalui web belum diklaim berhasil.
- Satu respons manifest web bersifat parsial. Identitas rilis diperiksa dari field yang dikembalikan, tanpa menganggap seluruh binding telah dibaca.
- Asisten memiliki konteks repo sebelumnya dan mengetahui jawaban acuan. Benchmark buta AI konsumen tetap pekerjaan terbuka, bukan hasil yang disimpulkan dari tes kode atau akses.
- Hasil, batas pengukuran dan pemeliharaan: [laporan tahap 6–7](stage-6-7-report.md).

**Tujuan**

Membuat pengetahuan yang makin akurat dan mudah digunakan AI ketika koleksi berkembang menjadi ratusan referensi. AI perlu dapat menemukan contoh yang sesuai, menelusuri alasan ke sumber, membedakan fakta dari interpretasi, serta menyatakan ketidakpastian. Repo tetap menyimpan pengetahuan desain; penyusunan konsep proyek, keputusan produksi, dan prompt Omni Flash tetap dikelola master prompt atau skill plugin.

Menambah jumlah referensi memperluas cakupan. Akurasi membutuhkan bukti yang diperiksa, pengelompokan yang konsisten, dan evaluasi yang terpisah.

**Kontrak akses dan pemisahan tanggung jawab**

Pengguna memberikan URL repo GitHub kepada AI. URL tersebut mengidentifikasi sumber pengetahuan, sedangkan alat yang tersedia menentukan jalur pembacaannya. Dua jalur akses didukung:

| Jalur | Cara mengakses | Kontrak pengetahuan |
| --- | --- | --- |
| Web/URL | Membaca README, Markdown dan tautan sumber melalui alat akses web yang tersedia; jalur tanpa autentikasi berlaku untuk konten publik yang dapat diakses | Paket inti dan navigasi tetap dapat digunakan tanpa konektor GitHub |
| Konektor GitHub | Membaca file dan, bila didukung alatnya, mencari referensi pada repository yang dapat diakses akun terhubung | Menggunakan file, ID bukti dan versi pengetahuan yang sama dengan jalur web |

Repo tetap menyediakan pustaka statis. AI pembaca tidak diwajibkan melakukan clone, menjalankan skrip, memakai CLI, database atau layanan pencarian buatan khusus. Konektor GitHub merupakan jalur tambahan yang didukung, bukan syarat menggunakan repo publik melalui web. Repo privat memerlukan jalur akses terautentikasi yang tersedia pada konsumen.

Kedua jalur tidak otomatis berarti seluruh file sudah dibaca atau semua gambar sudah dilihat. Kemampuan membaca file, mengikuti tautan, mencari dan mengakses bukti visual diuji secara terpisah pada konsumen yang nanti digunakan. Pemilihan jalur dan penanganan kegagalan akses diatur plugin/master prompt mendatang; kegagalan membaca tidak boleh disamarkan sebagai keberhasilan mempelajari sumber.

README root menjadi pintu masuk pengetahuan dengan tautan langsung menuju ringkasan inti, tema desain, direktori referensi dan bukti. Instruksi pemeliharaan/penyimpanan dipisahkan secara navigasi dari bacaan utama untuk konsumen. Sediakan satu paket inti Markdown yang cukup mandiri untuk pemahaman umum, lalu detail tematik dan profil sumber yang dapat dibuka bertahap. Ini tetap satu repo GitHub, tanpa layanan runtime tambahan.

| Di repo ini | Di plugin atau master prompt mendatang |
| --- | --- |
| Pengetahuan arsitektur, interior, lanskap, pencahayaan, ruang, kamera dan narasi visual | Alur tanya jawab dan pengumpulan brief proyek |
| Prinsip sintesis desain, kompatibilitas, orisinalitas dan kontinuitas | Menetapkan konsep rumah baru, tata ruang baru dan keputusan kreatif proyek |
| Deskripsi visual dan gerak yang dapat diterjemahkan menjadi prompt | Menulis prompt final dan memilih fitur/parameter Omni Flash sesuai versi yang dipakai |
| Katalog, contoh sumber, bukti dan ketidakpastian | Mengarahkan AI membaca bagian repo yang dibutuhkan dan menjalankan proses produksi |

Pengetahuan harus cukup kaya untuk mendukung seluruh rentang dari konsep rumah sampai deskripsi adegan video. Pengetahuan gerak, komposisi dan konsistensi visual tetap berada di repo; template prompt generator, durasi produksi wajib, jadwal frame dan alur persetujuan berada pada konsumen.

Indeks JSON/YAML/JSONL membantu pemeliharaan dan konsumen yang mendukungnya, tetapi pengetahuan penting tetap tersedia sebagai Markdown. Mesin pencarian semantik, embedding, database vektor dan API tidak menjadi prasyarat rencana ini.


**Kondisi awal sebelum implementasi tahap 1–5**

| Bagian | Kondisi |
| --- | --- |
| Integritas sumber | Selesai: sumber tersedia, fingerprint SHA-256, duplikat edh026 dihapus dan edh027 dipertahankan |
| Validasi struktur | Pemeriksaan paket dan regresi tersedia; hasil setelah penghapusan metadata verifikasi manual: 100 tes lulus |
| Review isi | Review dilakukan oleh AI sebelum penyimpanan; pengayaan berikutnya memakai catatan review dan ketidakpastian tanpa syarat verifikasi manual |
| Indeks bukti | 23 record yang menjangkau 7 referensi dan 14 shot |
| Istilah | Banyak label gaya dan scene bebas; belum ada kamus normalisasi terstruktur |
| Pertumbuhan koleksi | Tes masih memiliki angka tetap 57/295 serta delapan grup profil |
| Pengetahuan ruang | Prinsip umum tersedia; relasi yang diamati belum menjadi data terstruktur yang merata |
| Akses AI melalui web/konektor | Katalog dan profil tersedia; paket inti, navigasi dan evaluasi kedua jalur belum diimplementasikan |

**Kebijakan penggunaan kreatif**

Semua referensi tersimpan dapat menjadi inspirasi. Confidence dan status review menjelaskan kepastian klaim tentang sumber, bukan kelayakan atau izin menggunakan elemen desain. AI boleh memilih batu alam pada konsep baru meskipun komposisi permukaan sumber belum pasti. Keputusan desain baru harus dibedakan dari pengamatan sumber. Tidak ada syarat verifikasi manual; review tambahan dilakukan oleh AI untuk memperbaiki bukti atau pengayaan.

**Arsitektur pengetahuan yang dituju**

Sumber video/gambar → anotasi asli → pengayaan terstruktur dan catatan review → sintesis pengetahuan → paket inti Markdown, tema dan direktori referensi di GitHub → akses melalui web atau konektor GitHub → AI pembaca → plugin/master prompt menyusun konsep dan prompt video.

Arsip sumber dapat terus bertambah. Versi pengetahuan hanya berubah setelah perubahan yang terkait diperiksa. Semua lapisan turunan menyimpan kaitan ke sumber dan versi anotasi; lapisan turunan dapat dibangun ulang. Tidak ada lapisan yang boleh mengubah tebakan menjadi observasi.

**Tahap 1 — Siapkan pertumbuhan koleksi dan kontrak data**

Tujuan: penambahan referensi tidak mematahkan tes karena angka tetap atau langsung mengubah pengetahuan yang telah diterbitkan.

Pekerjaan:
- Tetapkan kontrak dua jalur akses dari URL repo: web dan konektor GitHub. Rancang pintu masuk README, paket inti Markdown, tautan bertahap serta pemetaan ID/path yang sama untuk keduanya. Uji contoh bacaan kecil pada masing-masing jalur sebelum memperluas pengayaan.
- Bedakan inventaris seluruh arsip dengan daftar referensi pada versi pengetahuan yang diterbitkan. Referensi baru boleh tersimpan sambil menunggu pengayaan/review.
- Ganti pemeriksaan jumlah tetap dengan pemeriksaan kelengkapan, kesesuaian ID, dan jumlah yang dihitung dari inventaris/versi terkait. Angka 57/295 tetap dicatat sebagai baseline historis.
- Ganti pembagian delapan grup profil yang kaku dengan profil per ID dan daftar isi yang dihasilkan otomatis. Tautan lama mendapat pemetaan agar tidak putus.
- Tetapkan kontrak data untuk sumber, observasi, review, normalisasi, klaim dan agregat.
- Pertahankan kompatibilitas analysis.yaml schema 2.1. Pengayaan awal disimpan sebagai berkas pendamping; migrasi skema asli hanya dilakukan jika benar-benar diperlukan.
- Hubungkan pembaruan manifest sumber dengan penambahan arsip secara deterministik, tanpa otomatis menerbitkan interpretasi baru.
- Uji satu penambahan, beberapa penambahan bersamaan, koreksi satu anotasi, penghapusan sumber, dan kemunculan kembali ID yang dipensiunkan.

Hasil: kontrak dua jalur akses dan navigasi, spesifikasi skema, indeks inventaris, manifest versi pengetahuan, dan tes yang dapat mengikuti pertumbuhan data.

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

Status: format review dan baseline sudah diterapkan. Review baru mencakup storyboard terpilih dan sampel temporal pilot; tidak mengklaim validasi ulang semua gerak sepanjang shot.

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

Status: relasi literal, inventaris mention, koordinat pandangan, pemisahan framing/kamera/objek/transisi dan sampel temporal sudah tersedia untuk semua shot; geometri yang tidak terbukti tetap unknown.

Tujuan: pengetahuan menjelaskan susunan dan perubahan visual, bukan hanya daftar objek.

Pekerjaan:
- Tambahkan relasi terstruktur: sofa menghadap fireplace; meja berada di antara sofa dan kabinet; jendela berada pada sisi ruang yang terlihat.
- Tandai sistem koordinat: kiri/kanan gambar, arah pandang kamera, atau orientasi rumah. Jangan mencampurkannya.
- Catat sambungan ruang dan pemandangan melalui bukaan hanya ketika didukung sumber. Potongan living lalu kitchen tidak otomatis membuktikan adjacency.
- Pisahkan elemen tetap, furnitur dan dekorasi; simpan bentuk, ukuran relatif, orientasi, oklusi, dan focal point yang terlihat.
- Untuk shot yang memerlukan penjelasan gerak, simpan frame awal–tengah–akhir atau timestamp bukti yang relevan. Jumlah frame mengikuti kebutuhan bukti.
- Bedakan gerak kamera, gerak objek, perubahan framing, dan transisi antarscene.
- Lengkapi pengetahuan visual yang dibutuhkan untuk menyusun prompt: subjek, bentuk/proporsi relatif, material appearance, tekstur, posisi, orientasi, komposisi, arah cahaya, mood, keadaan awal–akhir shot, gerakan dan hal yang tetap konsisten.
- Sintesis prinsip kontinuitas satu rumah: identitas massa/atap, bukaan, elemen tetap, palet dan dunia luar jendela. Tandai ini sebagai prinsip atau keputusan desain baru jika bukan hubungan yang terbukti pada sumber.
- Jelaskan hubungan sebab visual secara beralasan, misalnya pergeseran foreground saat viewpoint berubah. Gunakan contoh observasi dan pengecualian, tanpa menyimpan instruksi parameter generator.
- Jangan mengisi panjang fokus, koordinat fisik, arah mata angin, dimensi atau denah dengan presisi yang tidak didukung.
- Catat konflik/kemungkinan artefak visual sebagai keterbatasan; sumber home-tour tidak otomatis membuktikan bangunan fisik yang koheren.

Hasil: data relasi dan bukti temporal yang dapat dirujuk per shot. Ini adalah deskripsi sumber, bukan denah baru atau instruksi video produksi.

Selesai ketika: pertanyaan relasi dapat dijawab dengan bukti atau unknown, dan perubahan sudut pandang tidak menghasilkan klaim posisi yang saling bertentangan.

**Tahap 5 — Perluas cakupan dan perbarui sintesis**

Status: seluruh referensi memiliki paket bukti dan laporan cakupan. Review temporal 45 sumber ditunda dengan alasan eksplisit. Agregat, keragaman, kemiripan dan sintesis korpus sudah tersedia.

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

**Tahap 6 — Terbitkan pengetahuan untuk akses web dan konektor GitHub**

Status implementasi: pintu masuk ringkas, peta tema, modul kontinuitas, profil deskriptif dan navigasi direktori tersedia. Publikasi kandidat dan pengujian dua jalur dicatat dalam laporan tahap 6–7.

Tujuan: dari URL repo, AI dapat memahami pengetahuan inti dan mengambil rincian yang relevan melalui web maupun konektor GitHub, menggunakan satu sumber pengetahuan yang sama.

Pekerjaan:
- Susun README root sebagai pintu masuk; prioritaskan bacaan pengetahuan dan pisahkan tautan pemeliharaan/analisis sumber.
- Hasilkan satu paket inti Markdown yang mandiri untuk konteks umum. Hindari menjadikannya salinan penuh ratusan analisis.
- Sediakan modul tematik untuk arsitektur, interior, lanskap, cahaya, ruang, kompatibilitas, orisinalitas, kamera, komposisi dan kontinuitas.
- Hasilkan direktori Markdown berdasarkan keluarga gaya, skala, jenis/konfigurasi ruang dan kebutuhan visual. Setiap entri menaut ke profil ringkas, shot dan bukti terkait.
- Simpan profil per referensi agar jumlah sumber dapat tumbuh tanpa membuat satu halaman sangat panjang. Sediakan navigasi balik dan identitas sumber pada setiap halaman.
- Buat deskripsi teks cukup bermakna untuk konsumen yang hanya membaca teks. Tautan gambar/video merupakan bukti tambahan; jangan berasumsi konsumen sudah dapat melihatnya.
- Pastikan tautan file dapat dibuka melalui akses web yang tersedia pada konsumen; sediakan tautan konten mentah bila dibutuhkan dan diuji.
- Sertakan path repository dan ID stabil pada indeks/profil agar konsumen berkonektor dapat mengambil file yang sama tanpa bergantung pada tampilan halaman GitHub. Fitur pencarian konektor digunakan bila tersedia dan diuji.
- Kedua jalur merujuk satu versi pengetahuan dan sumber kanonis yang sama. Jangan membuat dua salinan pengetahuan yang dipelihara terpisah. Saat pengujian, gunakan branch/commit atau rilis yang sama agar perbedaan hasil tidak disebabkan pembaruan sumber.
- Plugin/master prompt kelak memilih alat yang tersedia dan sesuai. Konektor yang mampu membaca langsung dapat digunakan; web menjadi jalur alternatif untuk konten publik yang dapat dibuka. Tidak ada kewajiban mengaktifkan kedua jalur sekaligus.
- Kecualikan requests, fixture tes, salinan anotasi, rencana implementasi dan instruksi operasional dari jalur bacaan pengetahuan.
- Indeks JSON/YAML/JSONL dapat dihasilkan sebagai pendamping. Tidak ada kewajiban membangun pencarian khusus, embedding, database atau API sendiri; AI pembaca juga tidak perlu menjalankan skrip. Alat konektor yang tersedia dapat digunakan oleh konsumen.
- Semua halaman turunan mencatat sumber dan versi pengetahuan serta dapat dibangun ulang saat data berubah.

Hasil: pintu masuk README, paket inti Markdown, modul tematik, direktori yang dikelompokkan dan profil dengan tautan bukti.

Selesai ketika: pengujian web dan konektor masing-masing menunjukkan konsumen dapat menemukan, memahami dan merujuk pengetahuan dari URL repo tanpa clone atau menjalankan kode. Keberhasilan satu jalur tidak dianggap membuktikan keberhasilan jalur lain; keterbatasan akses gambar dicatat tersendiri.

**Tahap 7 — Evaluasi rilis dan pemeliharaan berkelanjutan**

Cakupan yang dipilih pengguna untuk implementasi saat ini: uji akses dan pemeliharaan; benchmark AI independen menjadi pengujian lanjutan.

Status implementasi: audit bacaan dan validator rekaman remote tersedia. Uji akses terpandu dibedakan dari benchmark model independen; asisten ini memiliki konteks repo sebelumnya sehingga tidak memenuhi isolasi konteks benchmark buta.

Tujuan: peningkatan jumlah data menghasilkan manfaat yang terukur dan tidak menurunkan mutu yang sudah ada.

Evaluasi mencakup:
- Ketepatan menemukan contoh dan sinonim melalui direktori/tautan web serta pembacaan/pencarian file konektor, termasuk beberapa jawaban yang sama-sama valid.
- Apakah kutipan benar-benar mendukung jawaban, bukan sekadar menunjuk file yang ada.
- Kemampuan membedakan observasi, inferensi dan prinsip.
- Ketepatan menjawab unknown untuk denah, material, ukuran atau gerak yang tidak terbukti.
- Ketahanan terhadap referensi konflik, label ambigu, sumber duplikat dan data yang belum ditinjau.
- Keragaman referensi yang dipilih untuk pertanyaan luas, serta jumlah halaman yang perlu dibuka dan bagian pengetahuan yang terlewat.
- Dampak koreksi sumber: hanya indeks, review dan sintesis yang bergantung padanya yang ditandai untuk pembaruan.

Evaluasi utama meniru penggunaan sebenarnya dengan dua pengujian terpisah pada pertanyaan dan snapshot pengetahuan yang sama:

1. Jalur web: AI mendapat URL repo dan alat baca web, tanpa konektor GitHub, file lokal atau indeks yang dimuat sebelumnya.
2. Jalur konektor: AI mendapat URL repo dan konektor GitHub yang memiliki akses baca yang sesuai, tanpa clone atau file lokal.

Pada masing-masing jalur, uji apakah AI menemukan tema dan sumber yang tepat, menjelaskan alasan desain yang didukung, serta membedakan ketidakpastian sumber dari kebebasan keputusan desain baru. Ukur panjang bacaan, jumlah halaman/file yang diambil, sumber yang dipilih dan akses bukti visual yang benar-benar berhasil. Periksa apakah perbedaan jawaban berasal dari perbedaan akses atau interpretasi. Jalur kreatif tidak harus menghasilkan konsep yang identik; dukungan fakta sumber dan versi pengetahuannya harus konsisten.

Pengujian repo privat hanya dijalankan pada jalur yang memiliki akses sah. Pengujian akses publik yang gagal dicatat sebagai keterbatasan konsumen, bukan alasan mengarang isi repo. Tidak ada mesin pencarian tambahan atau indeks eksternal yang diwajibkan oleh evaluasi ini.

Target awal yang diusulkan: 100% tautan/ID bukti valid dan nol dugaan yang disajikan sebagai fakta sumber tanpa dukungan bukti. Target ketepatan penemuan referensi dan anggaran bacaan ditetapkan setelah baseline pada konsumen yang dipilih. Pertanyaan tentang sumber yang tidak memiliki jawaban dinilai terpisah dari tugas kreatif; ketidakpastian sumber tidak membatalkan usulan desain baru. Ini kriteria rencana, bukan hasil pengujian saat ini.

Setiap rilis pengetahuan mencatat versi skema/kamus, daftar sumber dan revisinya, jumlah record, perubahan penting, hasil evaluasi dan keterbatasan. Review yang menyangkut anotasi berubah ditandai usang sampai ditinjau ulang. Koreksi faktual dapat diprioritaskan tanpa menunggu kelompok penambahan berikutnya.

Selesai ketika: build dapat diulang, perubahan dapat dibandingkan dengan versi sebelumnya, dan penurunan mutu terdeteksi sebelum indeks baru dipakai konsumen.

**Struktur implementasi dan kelanjutan**

Struktur tahap 1–5 yang sudah tersedia:
- schemas/: kontrak observasi, review, relasi dan versi pengetahuan.
- knowledge/taxonomy/: kamus dan alias.
- knowledge/reference-profiles/<reference_id>.md: profil per sumber.
- knowledge/enrichment/<reference_id>.json: normalisasi yang ditautkan ke sumber.
- knowledge/design-evidence/<reference_id>.json dan .md: observasi, relasi, mention dan bukti shot.
- knowledge/temporal/<reference_id>/: indeks timestamp, frame sampel dan contact sheet.
- knowledge/reviews/<reference_id>.json: catatan review dengan cakupan dan revisi.
- knowledge/aggregates.json, diversity.json dan corpus-patterns.md: hitungan dan sintesis.
- knowledge/similarity/: kandidat kemiripan dan sampel arsip.
- knowledge/ai-knowledge.md: paket inti Markdown yang sama untuk akses web dan konektor GitHub.
- knowledge/directories/: direktori Markdown menurut tema/gaya/ruang.
- Indeks pendamping tahap 6 hanya ditambah bila diperlukan; bukan prasyarat akses.
- knowledge/releases/: manifest versi pengetahuan.
- evaluations/: pertanyaan acuan dan laporan evaluasi; dikecualikan dari korpus pengetahuan.

**Pembagian pekerjaan**

| Pelaksana | Tanggung jawab |
| --- | --- |
| Kode deterministik pada pemeliharaan repo | Validasi skema/ID, hash, katalog, hitungan, deteksi perubahan dan pembangunan halaman/indeks statis |
| AI dengan akses visual | Usulan normalisasi, review visual yang dilabeli AI, relasi yang didukung dan usulan sintesis |
| AI peninjau pada evaluasi | Periksa dukungan bukti, klaim ambigu dan jawaban acuan; simpan alasan, cakupan dan ketidakpastian |
| Master prompt / skill plugin | Memilih jalur web/konektor, mengarahkan pembacaan pengetahuan dari URL repo, merancang rumah baru, dan menerjemahkannya menjadi prompt generator |

**Urutan implementasi yang direkomendasikan**

Mulai tahap 1 dan 2, termasuk prototipe navigasi/paket inti yang diuji melalui web dan konektor GitHub. Lanjutkan percontohan tahap 3–4 sebelum mengubah seluruh koleksi. Perluas pada tahap 5, kemudian lengkapkan publikasi Markdown dan evaluasi konsumsi AI pada tahap 6–7. Kerangka evaluasi disiapkan lebih awal pada tahap 3 agar menjadi pembanding sepanjang implementasi. Plugin dan master prompt produksi belum dibangun pada pekerjaan ini.

Pekerjaan dapat dibagi menjadi perubahan yang mudah diperiksa: (1) skema dan pertumbuhan koleksi; (2) kamus dan pemetaan; (3) percontohan review serta relasi; (4) perluasan bukti dan sintesis; (5) publikasi pengetahuan Markdown, evaluasi dua jalur akses, indeks pendamping dan pemeliharaan. Setiap perubahan memiliki migrasi yang dapat ditelusuri dan tidak menambahkan aturan produksi video ke repo.

Tidak perlu menunggu ratusan referensi untuk memulai. Terapkan fondasi pada 57 referensi sekarang, lalu gunakan mekanisme yang sama setiap kali koleksi bertambah. Keberhasilan dinilai dari kualitas jawaban berbukti dan kemudahan pemeliharaan, bukan jumlah file atau panjang anotasi.
