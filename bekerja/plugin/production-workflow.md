# Alur penggunaan home-productions

Versi: 0.7

Diperbarui: 18 November 2026

Status: kesepakatan alur penggunaan untuk pengembangan plugin mendatang.

Dokumen ini menjadi acuan yang dapat direvisi saat membangun plugin, bukan tanda bahwa kemampuan tersebut sudah diimplementasikan. Repository tetap menjadi pustaka pengetahuan. Instruksi pelaksanaan produksi akan berada di skill dalam plugin atau master prompt. Dokumen perencanaan ini disimpan di bekerja/plugin/ agar pengembangan produksi terkumpul dan tetap terpisah dari pustaka pengetahuan.

Acuan pembangunan: [rencana implementasi](implementation-plan.md). [Peta ruang pengembangan](README.md).

## 1. Tujuan dan prinsip

Membantu pengguna menghasilkan konsep rumah baru dan paket produksi video untuk Omni Flash yang mengikuti keseluruhan DNA referensi pilihan pengguna.

Referensi dikurasi pengguna berdasarkan performa viral. DNA yang dipelajari meliputi desain, tata ruang, lighting, komposisi, area yang ditampilkan, gerakan kamera, urutan pengungkapan, ritme, durasi, transisi dan penutup. Audio produksi mengikuti aturan pengguna: tanpa musik, cukup suara ambient yang halus dan sesuai adegan. Data yang tidak tersedia tidak diisi sebagai fakta sumber.

Plugin mengembangkan rumah yang koheren dan bahasa video yang sesuai referensi. Kesesuaian DNA diperiksa sebelum publikasi; respons Facebook menjadi umpan balik setelah publikasi. Kurasi viral belum menjamin performa setiap produksi baru.

Semua referensi tersimpan boleh menginspirasi desain. Confidence menjelaskan kepastian klaim sumber, bukan larangan memilih bahan atau tata ruang baru. Tidak ada persyaratan human_verified atau review manual setiap referensi.

Arahan eksplisit terbaru pengguna menjadi pegangan proyek. Durasi 6/4 detik, larangan pengulangan area dan audio tanpa musik adalah aturan produksi pilihan pengguna; referensi menyediakan pola untuk diterapkan di dalam aturan tersebut. Jika pengguna mengubah aturan proyek, catat perubahan dan versi keputusan sebelum memperbarui aset serta prompt.

Alur ringkas:

**Brief → referensi dan pilihan konsep → desain rumah dan rancangan shot → kolase awal–akhir per shot → pemeriksaan konsistensi → pemotongan gambar → paket prompt video → generate dan revisi hasil.**

## 2. Istilah dan aturan pembagian shot

| Istilah | Makna untuk produksi |
| --- | --- |
| Area/fungsi | Bagian rumah yang ditampilkan, seperti living, kitchen, bedroom, bathroom, laundry atau wardrobe. Beberapa fungsi dapat berada dalam satu ruang terbuka. |
| Shot produksi | Satu tampilan kamera kontinu tanpa cut, termasuk ketika kamera bergerak, mengubah arah pandang atau melewati beberapa area. |
| Adegan | Satu bagian cerita atau situasi yang dapat ditampilkan dalam satu atau beberapa shot. Adegan tidak wajib berlangsung tanpa cut dan tidak dipakai sebagai unit produksi plugin. |
| Frame awal–akhir | Pandangan pada kedua ujung satu shot. Lintasan di antaranya dijelaskan dalam prompt video. |

**Shot menjadi unit produksi resmi plugin.** Satu shot berlangsung kontinu tanpa cut dan dipetakan ke satu kolase dua panel, dua file gambar individu (awal–akhir), satu prompt video dan satu klip. Jumlah kolase, pasangan gambar, prompt, klip dan anggaran durasi dihitung berdasarkan daftar shot. Tidak perlu menghitung adegan secara terpisah untuk menentukan aset produksi.

Aturan utama:

- Jumlah, jenis area, urutan dan cakupan shot merujuk contoh yang ada pada referensi terpilih. Jangan menambahkan variasi ruang atau struktur shot yang tidak mempunyai acuan hanya karena secara umum memungkinkan.
- Bedroom yang ditampilkan maksimal satu, mengikuti referensi. Jangan menambahkan bedroom lain dengan membedakan nama atau fungsi kamarnya.
- Setiap area yang sudah menjadi cakupan suatu shot ditandai selesai dan tidak mendapat shot tersendiri lagi pada shot berikutnya.
- Living-to-kitchen mencakup living dan kitchen. Setelah shot ini, lanjutkan ke bedroom atau area lain yang belum tercakup; jangan menambahkan shot living atau kitchen lagi.
- Exterior → melewati pintu → living dihitung satu shot bila gerakannya kontinu tanpa cut. Shot ini mencakup exterior dan living; lanjutkan ke kitchen atau area lain yang belum tercakup.
- Jangan menumpuk exterior-to-living dan living-to-kitchen secara otomatis karena keduanya mengulang cakupan living. Susun kombinasi yang tidak mengulang area.
- Area boleh tetap terlihat sebagai konteks atau background ketika kamera mengungkap area berikutnya. Aturan ini menghindari pengulangan shot pengungkapan area, bukan mengharuskan objek keluar dari pandangan.
- Variasi referensi seperti exterior penutup tetap menjadi informasi sumber. Untuk aturan produksi saat ini, tidak ditambahkan shot exterior penutup setelah exterior sudah tercakup.
- Bedakan gerakan bersamaan, seperti maju sambil pan, dari gerakan berurutan, seperti maju lalu pan. Daftar label gerak saja belum selalu membuktikan urutan waktunya.

Lima shot merupakan pola terbanyak dalam anotasi koleksi saat pembahasan ini. Variasinya mencakup laundry tersendiri, bathroom–laundry gabungan, walk-in closet/wardrobe, loft, ruang terbuka beberapa fungsi dan exterior penutup. Lima sampai tujuh shot adalah contoh kebutuhan produksi, bukan batas wajib. Area opsional berarti variasi yang memang tercatat dalam referensi, seperti laundry dan walk-in closet; pilih sesuai acuan, tanpa memperluas daftar ruang secara bebas.

ID shot pada anotasi perlu dibaca bersama camera.continuity, transition_out dan observation_note. Pada [edh056](../../references/edh056/analysis.yaml), segmen living dan kitchen dinyatakan terpisah secara tematik tanpa edit. Karena itu, jumlah ID anotasi tidak selalu identik dengan jumlah shot produksi tanpa cut.

Contoh sumber untuk beberapa fungsi dalam satu shot: [edh022](../../references/edh022/analysis.yaml), [edh030](../../references/edh030/analysis.yaml), [edh033](../../references/edh033/analysis.yaml), [edh034](../../references/edh034/analysis.yaml), [edh057](../../references/edh057/analysis.yaml) dan [edh060](../../references/edh060/analysis.yaml). Contoh area tambahan: [VID-003](../../references/VID-003/analysis.yaml) mencatat laundry dan walk-in closet; [edh058](../../references/edh058/analysis.yaml) mencatat walk-in closet.

### Durasi baku produksi

Durasi berikut adalah keputusan produksi pengguna. Batas generator 4–10 detik per klip mengikuti lingkungan Omni Flash yang digunakan pengguna; video lengkap dibuat dari beberapa klip.

| Jenis shot | Durasi generate dan pemakaian |
| --- | --- |
| Exterior | 6 detik |
| Exterior-to-living, kontinu tanpa cut | 6 detik |
| Living-to-kitchen, termasuk pengungkapan living–kitchen dalam satu shot gabungan | 6 detik |
| Living tersendiri | 4 detik |
| Kitchen tersendiri | 4 detik |
| Bedroom | 4 detik |
| Bathroom | 4 detik |
| Laundry dan area opsional lain sebagai shot area tersendiri | 4 detik |

Hanya tiga jenis shot pada tabel yang mendapat 6 detik: exterior, exterior-to-living dan living-to-kitchen. Shot area lainnya mengikuti 4 detik, termasuk area terpadu seperti bathroom–laundry. Dua fungsi yang terlihat bersama tidak otomatis menjadikan shot berdurasi 6 detik. Area terpadu dicatat mencakup kedua fungsi agar tidak dibuat shot pengulangannya.

Jumlahkan durasi setelah cakupan area dan daftar shot ditetapkan, sebelum membuat kolase. Total durasi mengikuti kombinasi shot; rentang durasi referensi bukan batas yang memaksa semua proyek menjadi sama panjang. Jangan otomatis memperpendek, mempercepat atau menyamaratakan semua shot menjadi 4 detik demi mengejar total tertentu.

Bila brief meminta total yang tidak cocok dengan kombinasi tersebut, tunjukkan totalnya dan sesuaikan pilihan area/shot bersama pengguna. Perubahan durasi baku memerlukan arahan pengguna.

### Aturan audio wajib

Semua klip dan video akhir menggunakan suara ambient yang halus, natural dan sesuai adegan, tanpa musik. Aturan ini tetap berlaku meskipun referensi memakai musik.

- Tanpa musik latar, soundtrack, melodi, beat atau jingle.
- Cukup ambient berintensitas rendah; tanpa narasi, dialog atau efek suara dramatis tambahan.
- Pilih suara sesuai lingkungan yang dirancang: misalnya angin/daun atau burung jauh untuk exterior, dan room tone lembut untuk interior. Contoh ini tidak mewajibkan suara tertentu muncul pada setiap shot.
- Jaga perubahan karakter dan tingkat audio tetap halus ketika klip dirangkai. Jangan menambahkan musik pada tahap editing.
- Tuliskan aturan audio secara eksplisit di setiap prompt video, bukan hanya pada ringkasan proyek.
- Dengarkan hasil ketika audio dapat diakses. Jika musik atau suara lain yang melanggar muncul, revisi hasilnya sebelum digunakan. Jika audio belum dapat didengar, tandai pemeriksaan audio belum dilakukan.

Contoh instruksi audio per shot: "Soft, natural ambient sound appropriate to the scene only. No music, soundtrack, melody, beat, narration, dialogue, or dramatic sound effects."

## 3. Alur penggunaan lengkap

### Langkah 1 — Pengguna memberikan brief

Pengguna menjelaskan gaya atau kesan rumah, kebutuhan ruang, skala, suasana, lingkungan serta target video. Brief boleh singkat.

Plugin merangkum kebutuhan, preferensi, hal yang harus dihindari dan asumsi. Pertanyaan dibatasi pada informasi yang benar-benar memengaruhi hasil. Asumsi yang mengubah bentuk rumah atau struktur video perlu diperlihatkan sebelum ditetapkan.

Keluaran: brief proyek yang jelas.

### Langkah 2 — Memilih referensi dan arah konsep

Plugin membaca repo melalui salah satu jalur: web atau konektor GitHub. Mulai dari [pengetahuan inti](../../knowledge/ai-knowledge.md), lalu tema, direktori dan profil yang relevan. Tidak perlu memuat seluruh repo. Catat versi/commit bila tersedia dan gunakan sumber versi yang sama.

Pilih referensi utama untuk bahasa video dan referensi pendukung untuk kebutuhan desain tertentu. Catat ID referensi, shot atau segmen, bagian yang diambil dan adaptasi baru. Gagal mengakses gambar atau video harus tetap dicatat sebagai belum dilihat.

Plugin menawarkan beberapa arah konsep yang berbeda secara bermakna, misalnya tiga opsi, beserta alasan kesesuaiannya dengan brief dan referensi. Pengguna memilih atau menggabungkan pilihan yang kompatibel.

Keluaran: konsep rumah pilihan dan ringkasan ciri referensi yang akan diterapkan pada desain serta videonya. Catat asal ciri tersebut dan adaptasi baru; rincian rumah serta gerak kamera dikembangkan pada langkah berikutnya.

### Langkah 3 — Menetapkan satu rumah dan rancangan shot

Plugin menyusun spesifikasi rumah sebagai acuan bersama:

- Massa, proporsi, tingkat bangunan, atap, pintu, jendela dan bukaan penghubung.
- Hubungan ruang, jalur sirkulasi, tangga dan posisi furnitur utama.
- Material pilihan, warna, tekstur dan detail yang menjadi identitas rumah.
- Lanskap, dunia di luar jendela, kondisi waktu dan karakter cahaya.
- Elemen tetap yang harus bertahan ketika sudut pandang berubah.

Hubungan baru yang belum dibuktikan referensi ditetapkan sebagai keputusan desain proyek. Pembacaan kiri/kanan gambar mengikuti arah pandang kamera; posisi elemen rumah tetap konsisten.

Bersamaan dengan itu, plugin membuat daftar shot. Untuk setiap shot, tuliskan:

| Isi rancangan | Yang harus dijelaskan |
| --- | --- |
| Cakupan | Area/fungsi yang sudah ditampilkan dan tujuan pengungkapannya |
| Acuan | Referensi dan shot/segmen pendukung serta adaptasinya |
| Awal | Posisi kamera, arah pandang, subjek, foreground dan framing |
| Gerak | Lintasan, perpaduan gerak, kecepatan dan hal yang menjadi terlihat |
| Akhir | Posisi/pandangan akhir dan komposisi tujuan |
| Kontinuitas | Elemen tetap, hubungan ruang, cahaya dan batas cut |
| Penyajian | Durasi baku 6 atau 4 detik menurut jenis shot, urutan, hubungan dengan shot berikutnya dan total durasi proyek |

Buat daftar area yang sudah tercakup setelah setiap shot. Pastikan tidak ada shot berikutnya yang mengulang pengungkapan area tersebut. Terapkan durasi baku dan tampilkan totalnya. Pilih lintasan yang masuk akal terhadap pintu, dinding, furnitur dan ruang gerak; jarak serta gerak harus sesuai durasi 6 atau 4 detik yang ditetapkan.

Keluaran: spesifikasi satu rumah dan daftar shot yang disetujui sebelum membuat gambar.

### Langkah 4 — Generate satu kolase dua panel untuk setiap shot

Mode utama yang disepakati adalah satu kolase per shot:

- Panel kiri: frame awal.
- Panel kanan: frame akhir.
- Dua panel sama besar dengan batas lurus, tanpa tulisan atau bingkai dekoratif.
- Untuk video vertikal, setiap panel ditargetkan 9:16; dua panel berdampingan membentuk kanvas gabungan 9:8.
- Resolusi kanvas dipilih agar masing-masing hasil potong layak digunakan. Ukuran dan rasio aktual harus diperiksa, tidak cukup mengandalkan permintaan dalam prompt.

Kedua panel menggambarkan dua ujung lintasan kamera dalam rumah dan lingkungan yang sama. Pada shot satu area, pandangannya berubah di area tersebut. Pada exterior-to-living atau living-to-kitchen, frame awal dan akhir boleh memperlihatkan area berbeda yang terhubung secara masuk akal melalui bukaan atau ruang terbuka yang telah dirancang. Bentuk ruang dan objek tetap bertahan; perubahan pandangan terjadi karena gerak kamera.

Gunakan spesifikasi rumah dan gambar yang sudah disetujui sebagai acuan saat membuat kolase berikutnya. Gambar acuan tambahan dibuat bila diperlukan; tidak ada kewajiban membuat paket gambar seluruh area sebelum kolase.

Keluaran: satu kolase dasar per shot, dengan kemungkinan revisi.

### Langkah 5 — Memeriksa konsistensi dan merevisi gambar

Periksa dua tingkat konsistensi:

1. Dalam satu shot: kedua panel mempertahankan geometri, letak bukaan, furnitur, material, cahaya dan lingkungan yang masuk akal.
2. Antarshot: seluruh ruang terbaca sebagai satu rumah; hubungan ruang, keluarga bukaan, material serta pandangan luar jendela tetap koheren.

Pastikan perubahan pandangan sesuai gerak kamera. Maju sambil pan tidak boleh diperlakukan sekadar sebagai dua gambar ruang berbeda yang dihubungkan transformasi bentuk.

Kolase merupakan pendekatan untuk membantu keselarasan pasangan frame, bukan jaminan konsistensi. Perbaiki bagian yang bermasalah sambil mempertahankan keputusan yang sudah disetujui. Perubahan elemen tetap harus diperiksa dampaknya pada shot lain.

Keluaran: kolase final yang sudah diperiksa.

### Langkah 6 — Memotong dan menyediakan gambar individu

Pemotongan adalah keluaran wajib. Plugin perlu memiliki kemampuan pemrosesan file untuk:

1. Memeriksa dimensi aktual dan letak batas panel.
2. Memotong setiap kolase menjadi dua gambar individu dengan mempertahankan pikselnya, tanpa generate ulang.
3. Memeriksa rasio, resolusi, ketajaman yang tersedia dan sisa garis/bingkai pada hasil potong.
4. Menyediakan tautan unduhan individual dengan nama yang jelas.

Contoh penamaan:

- shot-01-start.png
- shot-01-end.png

Jika ukuran/batas panel tidak memenuhi kebutuhan, perbaiki komposisi atau sumber gambarnya. Pemotongan tidak menambah detail yang hilang dan tidak boleh mengubah proporsi rumah melalui peregangan gambar.

Keluaran: dua file siap unduh per shot. Paket ZIP boleh ditambahkan untuk kemudahan, sementara kedua gambar tetap tersedia secara individual.

### Langkah 7 — Menyusun paket prompt Omni Flash

Prompt final disusun berdasarkan gambar hasil potong yang benar-benar sudah diperiksa. Setiap shot memiliki:

- ID shot dan nama file frame awal–akhir yang sesuai.
- Gambaran subjek/ruang, kondisi cahaya serta lingkungan yang relevan.
- Lintasan kamera, gerak bersamaan atau berurutan, kecepatan dan pengungkapan ruang.
- Kondisi awal–akhir dan elemen yang harus tetap konsisten.
- Instruksi wajib satu continuous shot tanpa cut, tanpa pergantian sudut mendadak atau transformasi bentuk ruang sebagai pengganti gerak kamera.
- Audio ambient halus sesuai adegan; tanpa musik, narasi, dialog atau efek suara dramatis tambahan.
- Durasi baku 6 atau 4 detik menurut jenis shot, serta pengaturan yang tersedia pada aplikasi Omni Flash yang digunakan.
- Hubungan edit dengan shot berikutnya, dicatat terpisah dari gerakan di dalam shot.

Pasangan gambar menentukan tujuan visual kedua ujung shot; prompt tetap menjelaskan perjalanan di antaranya. Penggunaan pasangan awal–akhir dan kontrol lain harus dicocokkan dengan versi serta antarmuka generator. Jangan menganggap semua aplikasi menyediakan kontrol yang sama.

Keluaran akhir proyek:

| Berkas/isi | Fungsi |
| --- | --- |
| Ringkasan desain final | Acuan identitas rumah dan keputusan kreatif |
| Daftar shot | Urutan, cakupan area, lintasan dan durasi |
| Gambar awal–akhir individu | Masukan visual siap unduh untuk setiap shot |
| Prompt video per shot | Instruksi lengkap yang dipasangkan dengan file yang benar |
| Petunjuk penggunaan | Penempatan aset serta pengaturan generator yang tersedia |
| Ringkasan versi proyek | Keputusan terbaru, revisi dan bagian yang masih terbuka |

### Langkah 8 — Generate, meninjau hasil dan merevisi

Dalam cakupan awal, pengguna menjalankan generate video di Omni Flash menggunakan paket tersebut, satu klip untuk setiap shot dengan durasi baku masing-masing. Setelah diperiksa, klip dirangkai sesuai daftar shot menjadi video lengkap. Gerakan di dalam setiap shot berlangsung kontinu; cut antarklip mengikuti rancangan penyajian. Menyiapkan prompt tidak otomatis berarti plugin mengirim tugas atau menghasilkan video.

Pengguna dapat membawa hasil kembali untuk diperiksa. Plugin menilai kesesuaian desain, kontinuitas, gerak, framing, ritme dan DNA referensi berdasarkan media yang benar-benar dapat dilihat, serta memeriksa ambient halus tanpa musik ketika audio dapat didengar. Revisi diarahkan ke gambar, prompt atau keputusan desain yang menjadi penyebab masalah.

Simpan catatan proyek dan berkas aset asli yang dapat dibawa ke sesi lain. Ringkasan atau project.json mencatat keputusan dan nama file, tetapi tidak menggantikan piksel gambar. Jika aset tidak tersedia saat melanjutkan sesi, minta hanya berkas yang dibutuhkan dan jangan menganggap tautan unduhan lama masih dapat diakses. Semua file dan prompt final harus merujuk versi keputusan yang sama.

Setelah publikasi, respons Facebook dapat dicatat sebagai umpan balik. Hasil tersebut tidak otomatis mengubah pengetahuan sumber atau membuktikan penyebab virality.

## 4. Titik keputusan pengguna

Pengguna terutama terlibat ketika:

1. Memilih arah konsep.
2. Menyetujui desain rumah beserta daftar shot.
3. Menyetujui paket visual final sebelum dipakai untuk video.

Plugin melanjutkan pekerjaan di antara titik tersebut sesuai arahan yang sudah diberikan. Pengguna boleh memberi keleluasaan lebih besar, misalnya meminta plugin memilih opsi terbaik dan melanjutkan sampai paket visual.

Persetujuan ini merupakan keputusan proyek kreatif, tidak menambah kewajiban verifikasi manual referensi.

## 5. Contoh proyek ringkas

Apabila referensi pilihan sudah menampilkan living–kitchen dalam satu continuous shot:

| Shot | Cakupan | Durasi | Gambar |
| --- | --- | --- | --- |
| 01 | Exterior | 6 detik | Satu kolase awal–akhir → dua file individu |
| 02 | Living-to-kitchen | 6 detik | Satu kolase awal–akhir → dua file individu |
| 03 | Bedroom | 4 detik | Satu kolase awal–akhir → dua file individu |
| 04 | Bathroom | 4 detik | Satu kolase awal–akhir → dua file individu |

Total: empat shot, 20 detik, empat kolase dasar, delapan file frame dan empat prompt video. Sesudah shot 02 langsung menuju bedroom; living dan kitchen tidak diulang.

Perbandingan kombinasi yang sah:

| Susunan shot | Total durasi |
| --- | --- |
| Exterior 6 + living 4 + kitchen 4 + bedroom 4 + bathroom 4 | 22 detik |
| Exterior 6 + living-to-kitchen 6 + bedroom 4 + bathroom 4 | 20 detik |
| Exterior-to-living 6 + kitchen 4 + bedroom 4 + bathroom 4 | 18 detik |
| Exterior 6 + living-to-kitchen 6 + bedroom 4 + laundry 4 + bathroom 4 | 24 detik |

Area opsional yang dipilih mendapat cakupan satu kali. Misalnya, menambahkan wardrobe sebagai shot tersendiri menambah 4 detik.

Contoh kebutuhan lain, bila seluruh shot memakai pasangan awal–akhir:

| Shot produksi | Kolase dasar | File frame individu |
| --- | --- | --- |
| 5 | 5 | 10 |
| 6 | 6 | 12 |
| 7 | 7 | 14 |

Hitungan ini menjelaskan aset target, bukan jaminan jumlah panggilan generate, waktu atau penghematan biaya. Revisi dan kebutuhan acuan tambahan dapat menambah proses.

## 6. Cara menggunakan dan merevisi rencana ini

Contoh permintaan pengguna yang perlu didukung plugin:

> Buat tiga arah konsep cottage tropis untuk home tour vertikal. Pelajari DNA desain dan gerak dari referensi yang relevan terlebih dahulu.

> Pilih konsep kedua, tambahkan laundry, lalu susun desain rumah dan daftar continuous shot. Area yang sudah tercakup jangan diulang. Terapkan exterior dan shot penghubung 6 detik, serta shot area tersendiri 4 detik.

> Lanjutkan ke kolase awal–akhir per shot. Periksa konsistensi rumah, potong setiap kolase dan berikan dua file individu yang siap diunduh.

> Susun prompt Omni Flash berdasarkan gambar final, kemudian berikan ringkasan proyek agar bisa dilanjutkan pada sesi berikutnya.

Dokumen ini adalah satu acuan aktif. Revisi bagian terkait secara langsung, perbarui versi/tanggal dan ringkasan perubahan. Riwayat Git menyimpan versi terdahulu; tidak perlu membuat salinan rencana atau laporan tahap baru untuk setiap revisi.

Hal yang masih perlu ditentukan saat implementasi: aplikasi/versi Omni Flash, kontrol generator yang tersedia, kemampuan generate gambar dan pemrosesan file pada lingkungan plugin, ukuran keluaran gambar yang dapat dipakai, serta mekanisme penyimpanan proyek. Alur di atas menjadi sasaran kemampuan yang harus diwujudkan dan diperiksa.

## 7. Rujukan

- [Pengetahuan inti](../../knowledge/ai-knowledge.md)
- [Akses melalui web dan konektor GitHub](../../knowledge/access-contract.md)
- [Sinematografi dan bahasa visual](../../knowledge/cinematography-dna.md)
- [Kontinuitas rumah](../../knowledge/continuity-dna.md)
- [Pola korpus dan batas hitungan](../../knowledge/corpus-patterns.md)
- [Pemeliharaan pustaka](../../docs/knowledge-maintenance.md)
- [OpenAI: image generation dan keterbatasannya](https://developers.openai.com/api/docs/guides/image-generation)
- [Google: Gemini Omni Flash](https://aistudio.google.com/docs/omni)

## 8. Ringkasan perubahan

- 0.7 — Membatasi pilihan area dan struktur shot pada contoh referensi serta menetapkan maksimal satu bedroom yang ditampilkan; menghapus perluasan beberapa bedroom.
- 0.6 — Merapikan prioritas aturan pengguna, durasi area terpadu, pengertian kedua panel untuk lintasan antararea, kewajiban continuous shot dan kelanjutan proyek beserta aset aslinya.
- 0.5 — Memindahkan acuan alur ke bekerja/plugin/, menamai home-productions dan menautkan rencana implementasi; aturan produksi tetap berlaku.
- 0.4 — Menetapkan shot sebagai unit produksi resmi dan memperjelas perbedaannya dari adegan; satu shot dipetakan ke satu kolase, dua gambar, satu prompt dan satu klip.
- 0.3 — Menetapkan seluruh klip dan video akhir tanpa musik, cukup ambient halus sesuai adegan; mewajibkan instruksi audio pada setiap prompt dan pemeriksaan hasil audio bila dapat diakses.
- 0.2 — Menetapkan exterior, exterior-to-living dan living-to-kitchen masing-masing 6 detik; shot area tersendiri 4 detik; melarang pengulangan area yang sudah tercakup; menambahkan total durasi dan contoh susunan klip.
- 0.1 — Mencatat kesepakatan alur produksi, DNA desain dan video, pembagian continuous shot tanpa duplikasi area otomatis, kolase dua panel per shot, pemotongan wajib, unduhan individu dan paket prompt Omni Flash.
