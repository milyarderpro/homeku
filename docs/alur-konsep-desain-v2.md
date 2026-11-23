# Alur AI Membuat Konsep Desain dengan Pustaka V2

Diperbarui: 23 November 2026.

Panduan penggunaan [pustaka V2](improvement-v2-plan.md), termasuk pembacaan ringan dan pemilihan variasi referensi. Reader/index 2.1 mendukung sumber legacy dan audit 2.0/2.1; sumber 2.1 memakai laporan/media 2.2.0. Referensi aktif mengikuti registry, bukan kandidat yang belum diterima. Dokumen ini menyimpan alur penggunaan oleh AI, bukan klaim pengujian konsep atau implementasi plugin produksi.

**Permintaan pengguna → mencari referensi → membaca DNA dan gambar → membuat pilihan konsep → mengunci desain terpilih → menyiapkan gambar dan gerakan video.**

## 1. Memahami permintaan pengguna

Pengguna menjelaskan gaya, ukuran, bentuk bangunan, kebutuhan ruang dan suasana yang diinginkan. Contoh brief:

> Buat tiga konsep rumah Organic Modern Cottage berukuran kecil, dengan bentuk bangunan L dan interior hangat.

AI mencatat kebutuhan tersebut sebagai acuan pemilihan referensi dan pengembangan konsep. Contoh brief ini bukan hasil audit atau konsep yang sudah dibuat.

## 2. Mencari referensi yang relevan

AI mulai dari indeks ringkas data/search-index.json, membaca identitas beberapa kandidat, lalu mengambil detail shot dari data/projections/<id>.json sesuai kebutuhan. Bukti/media dibuka saat diperlukan. Tooling menyediakan pembacaan bagian data; hasil awal tidak membawa semua fakta, log frame atau hash teknis. Koleksi yang digunakan mengikuti registry aktif.

Pencarian mencakup gaya utama, pengaruh dan gaya interior, ukuran, bentuk bangunan, bukaan, konfigurasi ruang/furnitur, komposisi serta kamera. Pisahkan syarat wajib brief dari preferensi. Mulai dari beberapa kandidat, lalu perluas jika variasi atau bukti belum cukup. AI tidak perlu memuat ratusan laporan atau semua JSON sekaligus.

Nama gaya dicari melalui alias setara dan hubungan keluarga yang dibedakan. Gaya gabungan atau pengaruh tidak otomatis menjadi sinonim gaya utama. Kesan ukuran dan estimasi luas dibaca bersama bentuk/proporsi serta kebutuhan brief.

Referensi dapat dipilih untuk kebutuhan berbeda: satu acuan utama menjaga bentuk/identitas rumah, lainnya melengkapi konfigurasi area atau kamera yang kompatibel. Pilih variasi berdasarkan perbedaan geometri, susunan fungsi, orientasi furnitur, penyimpanan dan bukaan, bukan hanya warna atau nama gaya. Jika kecocokan hanya sebagian, AI menjelaskan bagian yang diambil dan penyesuaiannya. Sumber yang kurang dinyatakan apa adanya, tanpa mengarang referensi.

analysis.md menjadi laporan manusia untuk memahami sumber inspirasi. audit.json menyimpan isi audit; proyeksi JSON menjadi jalur pembaca AI yang menggabungkan data terkait. Prinsip dan variasi dalam knowledge digunakan sesuai kebutuhan.

## 3. Membaca DNA dan kemungkinan variasinya

AI membuka gambar yang relevan dan mempelajari hubungan desain yang membentuk karakter referensi:

- Massa bangunan, atap dan pintu masuk.
- Bentuk serta susunan jendela.
- Perpaduan material, warna dan pencahayaan.
- Konfigurasi ruang, penyimpanan serta furnitur.
- Hubungan interior dengan lingkungan luar.

Nama gaya membantu menemukan keluarga desain; ciri visual dan susunan elemen menjelaskan DNA yang dapat dikembangkan. Pengetahuan variasi dan prinsip desain membantu AI mengolah susunan baru yang koheren.

## 4. Menawarkan konsep yang berbeda

AI menawarkan jumlah konsep sesuai permintaan pengguna. Setiap konsep menjelaskan nama desain, gaya/pengaruh, bentuk dan ukuran rencana, konfigurasi utama, palet, suasana serta keunikannya.

Perbedaan konsep menyentuh bentuk atau konfigurasi: misalnya susunan massa L, penempatan halaman, bentuk bukaan atau penggabungan fungsi ruang. Variasi diteruskan ke interior; bathroom dapat berbeda melalui susunan shower, vanity, penyimpanan dan bukaan, bukan hanya pergantian warna.

AI menjelaskan secara singkat DNA referensi yang diambil dan keputusan desain baru yang dibuat. Estimasi luas referensi digunakan sebagai konteks; ukuran rencana rumah baru merupakan keputusan konsep. AI mempertahankan perbedaan antara fakta referensi dan usulan kreatif.

## 5. Memilih konsep dan mengunci identitas rumah

Pengguna memilih konsep, lalu AI menetapkan identitas rumah yang dipakai bersama oleh seluruh area:

- Bentuk bangunan dan ukuran rencana.
- Keluarga bukaan serta elemen arsitektur utama.
- Material dominan dan palet.
- Lingkungan luar dan pencahayaan.

Setiap area mengikuti identitas tersebut, dengan variasi sesuai fungsi. Unsur yang menjaga kesatuan rumah dibedakan dari furnitur/dekorasi yang dapat bervariasi. Simpan konteks ringkas keputusan proyek beserta rujukan area/kamera, lalu gunakan kembali untuk shot berikutnya. AI membuka ulang bagian referensi sesuai kebutuhan, tanpa memuat seluruh pustaka berulang. Konteks ini merupakan keputusan proyek, terpisah dari fakta pustaka referensi dan bukan referensi aktif baru.

## 6. Menyiapkan setiap shot dan gambar awal

AI merencanakan shot berdasarkan pengambilan berkelanjutan, bukan otomatis satu shot per area. Untuk setiap shot, AI menetapkan desain area yang tercakup, fokus, posisi/arah kamera awal, framing awal–akhir, pencahayaan, gerakan serta ritme. Laporan manusia mengikuti [template baku](template-analysis-v2.md): detail arsitektur, furnitur/properti dan lingkungan tetap lengkap; gerak dijelaskan dalam bahasa sederhana serta notasi teknis yang sejalan.

Untuk permintaan satu shot multi area, cari sumber yang benar-benar memperlihatkan perjalanan kontinu, lalu baca rute, penghubung, kemunculan area, fase kamera dan tempo. Jangan menganggap kumpulan shot terpisah sebagai bukti kontinuitas. Area yang terlihat tidak otomatis dilalui kamera. AI menyesuaikan susunan konsep agar jalur taman → pintu → living → kitchen, misalnya, dapat dijalankan tanpa menembus furnitur atau dinding; ini keputusan konsep baru yang dibedakan dari fakta sumber.

Satu shot multi area memakai satu posisi/gambar awal dan satu perjalanan kamera; bukan gambar awal terpisah per ruang. Frame pendukung membantu memahami area yang terungkap kemudian. Gambar awal mengikuti area pertama, sudut serong/frontal yang sesuai dan jalur reveal, bukan dipaksa memperlihatkan semua ruang sekaligus.

AI membuka media referensi untuk memeriksa kecocokan dengan geometri konsep baru. Gambar awal perlu menyediakan kedalaman, elemen dekat dan bagian yang akan terungkap sesuai gerak. Sebutan wide saja belum menjelaskan lokasi atau arah pandang kamera.

**Overview akhir Dolly-Out dibedakan dari frame awal sumber.** Baca panel awal pada kolase shot untuk memahami awal lintasan dan overview pada storyboard sesuai perannya. Untuk IN, overview biasanya berada di awal; untuk OUT biasanya di akhir. Pilihan gambar untuk alur produksi, termasuk reverse bila dipilih, dijelaskan sebagai keputusan produksi.

Kolase satu area berisi tiga panel; multi area memakai jumlah dinamis sesuai perjalanan. Gunakan label serta metadata panel untuk mengambil bagian foto area/waktu yang diperlukan, tanpa menganggap caption atau seluruh kolase sebagai satu frame awal. Storyboard tetap satu baris dan boleh menampilkan beberapa area bernomor shot sama. Frame utuh dapat diekstrak dari video jika detail belum terwakili; salinan JPEG panel tidak wajib disimpan di repo.

Gerakan kamera memakai DNA sumber yang sesuai. Pencarian ritme memakai profil tempo yang tercatat: sedang → cepat tetap ditemukan melalui kedua kecepatannya, bukan hanya variable. Baca perkembangan awal/akhir dan perubahan penting di tengah; perubahan tempo tidak otomatis menjadi pergantian komponen gerak.

Adaptasi arah, lintasan, besaran atau ritme terhadap konsep baru dijelaskan; kronologi sumber tetap tersimpan sebagai referensi. Kecocokan bentuk ruang didahulukan saat memilih lintasan, tanpa memaksakan semua pandangan frontal.

## 7. Melanjutkan ke produksi gambar dan video

Konsep serta identitas yang sudah dikunci menjadi dasar prompt gambar awal setiap shot beserta gambar pendukung bila diperlukan. Posisi kamera wide mengikuti pilihan Overview, paragraf composition_summary dan gambar terkait. Camera Start tetap awal shot sumber; keduanya dapat berbeda pada OUT. Prompt gambar menyebut posisi/arah/sudut/tinggi/kemiringan, cakupan wide, susunan elemen, kedalaman dan cahaya secara ringkas. Pilih posisi serong atau sudut ruang sesuai foto, tanpa menjadikan setiap gambar frontal.

Gerakan yang dipilih menjadi acuan prompt video. Notasi mempertahankan hubungan simultan/berurutan, besaran perkiraan dan ritme; perubahan untuk produksi dicatat sebagai adaptasi. AI atau plugin produksi menjalankan pembuatan serta pemeriksaan gambar/video sesuai alur produksinya.

Pustaka V2 menyediakan pengetahuan dan bukti. Metadata media tersimpan bersama dan ditelusuri melalui rujukan stabil; AI tidak perlu menerima salinan metadata yang sama pada setiap fakta. Pembuatan konsep, gambar dan video dilakukan oleh AI atau plugin produksi yang menggunakan pustaka; generator ingest tetap bertugas mengolah data audit secara deterministik. Implementasi pengelola proyek/plugin produksi tetap terpisah dari pekerjaan pustaka V2.

## Hasil pada setiap tahap

| Tahap | Hasil yang dibaca pengguna |
| --- | --- |
| Pencarian referensi | Referensi terpilih dan alasan pemilihannya |
| Pengembangan konsep | Pilihan desain dengan perbedaan bentuk/konfigurasi yang jelas |
| Pemilihan konsep | Satu konsep dan identitas rumah yang dikunci |
| Rencana shot | Desain area, gambar awal, framing, pencahayaan, kamera dan ritme |
| Produksi | Prompt serta hasil gambar/video sesuai konsep terpilih |

Alur ini merupakan panduan penggunaan pustaka, bukan tambahan benchmark manfaat atau tugas produksi yang wajib dijalankan selama implementasi V2. Enam audit pilot yang tersisa tetap mengikuti pembagian pada plan.

## Membaca file dan gambar secara ringan

1. data/search-index.json untuk seleksi; identitas kandidat lewat `python tools/library.py read <id>`. Jangan membuka ratusan MD atau JSON lengkap sekaligus.
2. `read <id> --part shot --shot shot-NN` atau `--part area --shot shot-NN --area <area-id>` untuk desain/komposisi/kamera terpilih. Satu area pada continuous take tetap membawa seluruh rute/fase/tempo shot. Proyeksi di data/projections/ adalah representasi untuk AI; analysis.md laporan manusia.
3. Lihat Overview untuk komposisi wide dan Storyboard untuk semua perjalanan. Sumber 2.1 menyimpan media/overview.jpg dan storyboard seluruh kolase vertikal; sumber 2.0 menyimpan overview pada storyboard satu baris menurut versi asal.
4. Ambil panel terpilih lewat `panel <id> <selection-id> --output /tmp/panel.png`; kolase lewat `shot-image <id> shot-NN --output /tmp/shot.jpg`; blok lengkap lewat `shot-image <id> shot-NN --from-storyboard --output /tmp/block.png`. Foto/blok tersimpan tidak memerlukan MP4. --native hanya jika secara khusus ingin memeriksa sumber asli.

Nama gaya membantu discovery; bentuk, konfigurasi, fungsi, penyimpanan, bukaan dan framing menentukan variasi nyata. Fakta observed/uncertain, negasi dan sumber tetap dipisahkan dari keputusan konsep baru. Knowledge/prinsip dibuka hanya yang relevan. Pustaka tidak membuat keputusan kreatif otomatis saat ingest.

## Jika pengguna meminta cloning referensi

Untuk permintaan “buat video home tour cloning seperti referensi edh001”, pakai ID aktif itu sebagai acuan desain, susunan furnitur, elemen, pencahayaan, framing, urutan shot dan kamera/tempo. Jangan menawarkan variasi kreatif kecuali diminta.

**ID aktif → Overview/Storyboard → JSON shot terpilih → gambar wide tiap shot → prompt video sesuai gerakan sumber → susunan akhir sesuai timeline.**

AI melihat foto Overview/panel/kolase untuk meniru susunan visual, membaca composition_summary bila tersedia untuk posisi wide, serta composition untuk Camera Start sumber. Gerakan disalin dari camera_summary beserta phases dan tempo_profile. Kamera gambar harus mendukung target gerak dan menjaga elemen orientasi. Single take multi area tetap satu shot: pertahankan penghubung, reveal, urutan fase dan tempo seluruh perjalanan; jangan mengarang koneksi ruang dari cut.

Untuk IN, Overview awal biasanya menjadi gambar awal produksi IN. Untuk OUT, gunakan Overview akhir yang wide sebagai gambar awal, buat perjalanan **kebalikan sumber** dengan IN, kemudian reverse seluruh hasil menjadi OUT. Balik juga arah rotasi, urutan fase, tujuan lintasan dan perkembangan tempo; mengganti Out menjadi In saja tidak cukup. Ringkasan kamera pustaka tetap gerak sumber asli, sedangkan prompt produksi dicatat terpisah.

Overview tengah, arah campuran atau area akhir dalam continuous take hanya mendukung bagian lintasan yang terlihat; sesuaikan gambar/lintasan produksi terhadap cakupan itu. Kamera tidak wajib frontal. Membaca foto yang sudah tersimpan untuk cloning/inspirasi tidak mewajibkan audit ulang MP4.
