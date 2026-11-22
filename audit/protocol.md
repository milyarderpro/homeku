# Protokol audit HOMEKU

Versi workflow: 1.1. Kontrak paket/MD tetap provisional sampai seluruh pilot nyata selesai. Protokol berlaku untuk video baru maupun audit ulang; jumlah referensi tidak dibatasi daftar pilot.

## Alur dalam satu chat

1. Pengguna melampirkan MP4 dan homeku-audit-kit.zip, lalu mengirim prompt audit. MP4 diunggah terpisah dari kit.
2. AI membaca README kit, template dan kontrak. Ambil ID dari stem file; hitung SHA-256 dan metadata aktual dengan helper. Periksa seluruh durasi dan susunan shot dari video, bukan anotasi arsip.
3. Audit desain, hubungan spasial, komposisi dan gerak dalam lintasan terpisah. Mulai 10 FPS sepanjang setiap shot serta frame asli pertama/terakhir. Perdalam seluruh frame asli pada rentang meragukan, lalu seluruh shot bila belum cukup. Lihat frame yang dipilih; frame sampling bukan klaim seluruh frame video sudah dilihat.
4. Tulis analysis.md 1.1 lengkap sesuai template, termasuk profil DNA, narasi palet dan ikhtisar shot. Data teknis dilipat, narasi/gambar tetap terlihat. Pilih frame gambaran area dan perannya. Buat kandidat melalui helper draft, baca kembali gambar/storyboard, lalu selesaikan kesalahan teknis di chat.
5. Jalankan helper review atas kandidat terbaru. Tampilkan storyboard dan kartu setiap shot: gambar area, ikhtisar/pembeda, posisi/arah, awal/akhir, notasi kamera lengkap, fase/ritme, dasar dan ketidakpastian. Sediakan MD lengkap yang nyaman dibaca; pengguna tidak diwajibkan membaca seluruh tabel teknis. Kartu memuat hash snapshot MD yang sama.
6. Terapkan koreksi pengguna pada laporan lengkap. Jika perubahan menyentuh shot, waktu, media atau kamera, bangun ulang kandidat dan tampilkan bagian yang berubah beserta konteksnya. Satu snapshot terkini menjadi sumber ekspor.
7. Setelah pengguna menyatakan isi sesuai, hitung SHA-256 analysis.md yang disepakati. Jalankan export dengan digest tersebut. Helper membangun ulang media, manifest dan ZIP dari snapshot yang sama serta memvalidasi ZIP setelah dibuka ulang.
8. Berikan satu ZIP final untuk diunduh. Pengguna menaruh ZIP di incoming/ repo; alur repo memperbarui seluruh keluaran tanpa pemeriksaan isi kedua.

Pengujian perangkat ini tidak menandakan semua pilot telah diaudit atau pengguna telah menyetujui isi. Audit di chat implementasi dan audit di lingkungan ChatGPT/Gemini sehari-hari dicatat sebagai lingkungan berbeda.

## Kedalaman pengamatan

Catat yang benar-benar terlihat: geometri ruang/massa, plafon, bukaan, tampilan finishing, furnitur/perangkat, penyimpanan, dekorasi, lapisan cahaya, lingkungan, konfigurasi dan hubungan antar elemen. Beri posisi relatif, orientasi dan pembeda. Contoh bathroom dapat dibedakan oleh konfigurasi shower, posisi toilet/vanity, laundry, bentuk bukaan, ceruk dan sirkulasi, bukan hanya warna ubin.

Jangan memaksakan daftar furnitur yang sama pada semua ruang. Tidak ada kuota benda. Objek yang hanya sebagian terlihat tetap dapat dicatat dengan batas identifikasinya. Objek yang tak terlihat tidak otomatis tidak ada. Material fisik, ukuran, lensa, lokasi dan adjacency tidak dipastikan dari penampilan saja.

Prosa membuat laporan nyaman dibaca; tabel mencatat seluruh fakta yang perlu dicari/dibandingkan. Tidak boleh menyembunyikan variasi penting hanya di prosa sehingga generator tidak menemukannya. Fakta memakai satu klaim per baris beserta state/confidence/bukti. Label baru boleh dipakai secara konsisten; parser tidak menyimpulkan istilah dari narasi.

## Kamera dan gambar awal

Pisahkan posisi kamera, arah pandang dan jenis gerak. Frontal/serong/samping harus mengikuti video. Jelaskan foreground, lapisan kedalaman, target gerak, oklusi dan area yang terungkap. Data ini menjadi acuan saat AI merancang gambar baru dengan sudut yang sesuai lintasan.

area-overview.jpg adalah satu frame asli dengan cakupan area terbaik, mempertahankan rasio dan dimensi sumber. Untuk IN biasanya awal; untuk OUT biasanya akhir. Untuk orbit/pan/gabungan, pilih cakupan nyata dan jelaskan alasannya. Peran frame di dalam shot dicatat; pandangan akhir Dolly-Out tidak disamakan dengan posisi awal sumber.

Ringkasan kamera Inggris memakai → untuk fase berurutan dan + untuk komponen simultan. Setiap fase mempunyai interval, jangkar, tempo, perubahan kecepatan, dasar visual, confidence dan uncertainty. Wajib menilai besaran dan mengusahakan estimasi ~sudut/~rasio dari jangkar visual; bila belum dapat diperkirakan, jelaskan batasnya. Jangan mengarang angka atau menyalin contoh masterprompt. Jangan membalik arah atau memaksakan durasi 4/6 detik dari alur produksi.

## Bukti tersimpan dan bukti sementara

Paket final berisi storyboard, satu area-overview dan start/middle/end per shot, serta reveal/detail yang dibutuhkan. Storyboard merupakan gabungan area-overview seluruh shot dengan nomor, area dan timestamp. Tidak ada motion/, klip shot atau seluruh frame video dalam paket.

Pemeriksaan selama audit boleh memakai lebih banyak frame, contact sheet dan playback dalam workspace sementara. Gunakan folder sampling kosong yang berbeda untuk tiap lintasan pemeriksaan agar bukti lama tidak tercampur. Daftar waktu dibuat dari PTS integer dan time_base asli, bukan string waktu yang dibulatkan. Catat metode/rentang yang benar-benar dilihat, bukan hanya yang diekstrak. Jangan mengaku mendengar audio jika audio tidak diperiksa. Durasi stream video dapat berbeda dari audio/container.

## Koreksi, revisi dan pemulihan

Sebelum sebuah paket masuk repo, koreksi di chat dapat tetap memakai revisi paket yang sama: paket lama diganti seluruhnya sebelum diunggah. Sesudah revisi itu aktif, gunakan revisi berikutnya dan supersedes dari registry/hasil validate; jangan mengarang hash versi sebelumnya.

Simpan sumber dan analysis.md utama di luar folder kandidat yang dihasilkan helper. Draft selalu dibuat ulang ke folder bersih. Extras dan audit-info hanya instruksi kerja di chat; keduanya tidak ikut ZIP referensi dan tidak menjadi analysis.json kedua.

Jika sumber atau workspace chat hilang, minta lampiran yang diperlukan kembali dan bangun ulang dari snapshot teks terakhir yang ditinjau. Jika suatu operasi alat gagal, sebut kegagalan spesifik dan jangan membuat file palsu, hash perkiraan atau klaim validasi yang belum dijalankan. Pengguna tidak diminta memperbaiki struktur file di repo setelah download.


## Pemeriksaan adaptif dan log aktual

Jalankan sample per shot dengan default 10 FPS dan batas shot yang tepat. Sumber di bawah 10 FPS diperiksa seluruh frame tersedia. Helper selalu menambahkan frame asli pertama/terakhir dalam interval, terpisah dari grid 10 FPS. Gunakan --native untuk pendalaman: semua frame asli 24/30/60 FPS atau sesuai sumber, tanpa interpolasi. Rentang 0,5–1 detik bisa menjadi awal pendalaman; perluas sesuai perubahan, bukan batas wajib.

Pendalaman diperlukan ketika pan/orbit/truck belum terpisah, fase/arah/laju belum jelas, blur/oklusi/gerak cepat mengaburkan perubahan, atau koreksi pengguna berbeda dari tafsir audit. Jika belum dilakukan, bagian tersebut belum selesai. Catat alasan dan batas yang masih ada.

sampling.json mencatat indeks/PTS yang dipilih dan template review_record dengan viewed_frame_indices kosong. Setelah benar-benar melihat gambar, isi indeks yang telah dilihat dalam audit-info.frame_reviews. Setiap shot wajib memiliki baseline seluruh durasi; boleh dibagi beberapa rentang tanpa gap agar setiap ekstraksi tidak melebihi 1000 frame. Pendalaman disimpan sebagai record tambahan. Ekstraksi bukan pemeriksaan dan helper tidak mengisi persetujuan. Jangan menyatakan frame-by-frame penuh kecuali seluruh frame asli dalam rentang tersebut dilihat.

## Aturan Penentuan Arah & Fase

Terapkan tiga tes dari bagian audit kamera masterprompt audit-video.md: oklusi foreground, selisih paralaks, serta perubahan perspektif/pembingkaian. Ketentuan produksi dan durasi masterprompt tidak dipakai di pustaka; omniflash-v2.md hanya acuan notasi.

| Aspek | Cara memutuskan |
| --- | --- |
| Pan murni | Pada adegan statis, gambar menyapu kiri mendukung Pan Right; gambar menyapu kanan mendukung Pan Left. Pastikan rotasi pandangan, bukan gerak objek |
| Arah lateral | Foreground bergerak lebih kanan relatif background mendukung kamera ke kiri; kebalikannya mendukung ke kanan. Periksa bersama oklusi, posisi jangkar dan perspektif |
| Orbit / truck | Perubahan sisi/sudut mengelilingi jangkar yang tetap terbingkai mendukung orbit. Nilai perpindahan lateral dan orientasi pandangan untuk truck; gabungan boleh dicatat |
| IN / OUT | Catat bila didukung perubahan skala/kedalaman/oklusi; pan/orbit/static tidak dipaksa memiliki komponen maju/mundur |
| Fase | + hanya pada interval simultan. Jika komponen mulai/berhenti berbeda waktu, pecah fase dengan →. Catat waktu sumber dan waktu relatif shot pada kartu |
| Tilt tipis | Drift/jitter/goyangan vertikal kecil dan koreksi framing sesaat tidak disebut subtle tilt-up/down atau komponen tilt utama |
| Tilt nyata | Tilt-Up/Down memerlukan rotasi pandangan vertikal yang jelas/berkelanjutan dan pengungkapan bagian atas/bawah. Bedakan dari perpindahan ketinggian kamera |

Delta fg_dx − bg_dx hanya petunjuk pendukung. Dolly, pan gabungan, jangkar, perspektif dan deformasi dapat mengubahnya; jangan menetapkan arah dari satu angka. Tidak ada kesimpulan ketiadaan gimbal hanya dari gambar. Pertahankan tilt yang jelas pada sumber.

## Profil DNA dan pemeriksaan silang

Lengkapi seluruh aspek profil dengan pengamatan atau interpretasi berbukti; unknown eksplisit jika belum diketahui. Periksa gaya/pengaruh, skala tampak, tingkat/massa/atap, entrance/porch/bukaan, hierarki material/palet/cahaya/lingkungan, konfigurasi/pembeda dan kontinuitas. Material tampak bukan material fisik; urutan edit bukan denah. Mood/gaya diberi dasar interpretasi.

Periksa kesesuaian narasi, profil, fakta, komposisi, ringkasan/fase kamera dan media sebelum menampilkan kartu. Generator tidak memeriksa makna prosa atau menyintesis fakta. Tidak ada uji membuat konsep/gambar atau benchmark manfaat pustaka dalam workflow audit.
