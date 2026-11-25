# Metode audit visual HOMEKU 3.0

Baca sebelum mengisi JSON. Periksa perjalanan utuh, lalu baseline berurutan per take kontinu. Ekstraksi bukan pengamatan. Hanya frame yang benar-benar dilihat boleh dinyatakan viewed.

## Sampling

Baseline 6 FPS ditambah frame native pertama/terakhir setiap shot. Sumber ≤6 FPS atau shot <1 detik diperiksa seluruh native. Tidak ada interpolasi. Periksa midpoint dan pilihan panel/Overview yang belum tercakup. Pendalaman 10 FPS/native hanya untuk pertanyaan visual tertentu, lalu perluas bila belum terjawab. Ringkasan 6–10 momen tidak menggantikan baseline.

Cut memakai indeks dan PTS native. Pergantian area tanpa cut tetap satu shot; rute yang dimasuki berbeda dari area yang hanya terlihat.

## Urutan keputusan per fase

Baca [camera-cases.md](camera-cases.md) sebelum menganalisis kamera. Setelah meninjau baseline, pilih sekitar 6–10 frame pembanding sesuai durasi dan kerumitan shot.

1. **Temukan kandidat batas fase.** Bandingkan awal, tengah, dan akhir. Cari kapan komponen mulai, berhenti, atau berubah. Lihat frame sebelum dan sesudah dugaan batas. Perubahan area serta tempo bisa berlangsung dalam satu fase gerak.
2. **Nilai kedalaman.** Bandingkan ukuran bagian yang sama pada jangkar yang sama, lapisan dekat dan jauh, serta ruang yang terbuka. Uji kemungkinan Dolly dan Zoom sebelum menyimpulkan arah kedalaman. Pembesaran saja juga dapat terjadi karena Zoom.
3. **Pisahkan lintasan badan dan arah pandang.** Bandingkan satu jangkar dekat, satu jangkar jauh, dan orientasi satu bidang pada frame yang sama. Cari komponen lateral atau vertikal serta rotasi yang berlangsung bersamaan. Gunakan panduan Pan, Orbit, dan Truck di bawah.
4. **Tegaskan fase dan notasi.** Cocokkan dugaan batas dengan frame dan komponen yang benar-benar berubah. Pakai `+` untuk komponen simultan dalam satu fase. Ringkasan turunan memakai `→` antar fase. Baru kemudian nilai estimasi besaran, lintasan, intensitas, dan profil laju tiap komponen.

Catat depth, translation, dan rotation secara spesifik di `observations`. Pakai bukti temporal bersama dan override bila bukti suatu komponen berbeda. Gunakan minimal dua frame temporal pada fase atau dalam toleransi satu batas native. Jika masih ada tafsir yang bersaing, catat perbedaan yang terlihat atau batasnya di pengamatan fase dan dalami interval itu saja.

## Pan, Orbit dan Truck

| Tafsir | Yang diperiksa |
| --- | --- |
| Pan | Sapuan latar dan perubahan arah pandang terhadap jangkar. Pada scene statis, Pan Right umumnya menggeser latar ke kiri. |
| Orbit | Pergeseran relatif lapisan dekat dan jauh disertai perubahan sisi atau sudut bidang subjek yang dikitari. |
| Truck | Pergeseran relatif akibat badan bergerak menyamping, dengan lintasan lebih lurus. Arah pandang bisa tetap atau berputar untuk mengimbangi translasi. |

Bandingkan pergeseran relatif setelah mempertimbangkan perubahan skala akibat Dolly. Foreground yang bergerak lebih ke kiri daripada latar dapat mendukung badan kamera ke kanan, dan sebaliknya. Konfirmasi dengan bidang subjek dan oklusi. Misalnya, bila meja dekat berubah orientasi terhadap dinding sambil latar menyapu ke kanan, uji Orbit Right bersama Pan Left. Distorsi lensa, objek bergerak, dan deformasi generatif dapat membuat satu tanda menyesatkan.

Untuk arah vertikal, periksa rotasi yang disengaja dan berkelanjutan sebelum menulis Tilt. Bandingkan dengan perpindahan tinggi kamera dan drift tipis akibat jalan atau proyeksi wide.

## Arah, notasi dan tempo

Tentukan `depth_direction` per fase sebagai IN, OUT, NO IN/OUT, atau null jika ambigu. Camera Pattern mengikuti arah fase. Gunakan pola `[Komponen Utama] ([Skala]) [+ / →] [Komponen Sekunder] ([Intensitas / Kurva])`.

- **Lintasan dan intensitas.** Gunakan `Straight` atau `Diagonal` bila lintasannya terlihat. Gunakan `Pure` setelah memeriksa bahwa fase hanya memperlihatkan satu komponen. Pilih intensitas yang sesuai dari `Mild`, `Subtle`, `Gentle`, `Moderate`, atau `Strong`.
- **Skala (~×).** Bandingkan dimensi yang sama dari jangkar utuh pada awal dan akhir fase. Untuk pembesaran gunakan akhir/awal. Untuk pengecilan gunakan awal/akhir. Rasio ini menyatakan perubahan skala gambar. Jika Dolly dan Zoom sulit dipisahkan, pertahankan batas perkiraan gabungannya.
- **Sudut (~°).** Taksir Pan atau Tilt dari perubahan arah pandang, serta Orbit dari perubahan sisi yang terlihat sepanjang lintasan. Saat Pan mengimbangi Orbit, pisahkan tafsir putaran tiap komponen sebelum menaksir sudutnya.
- **Profil laju.** Bandingkan beberapa interval PTS setara. Gunakan `Constant`, `Accelerating`, `Decelerating`, `Ease-In`, atau `Ease-Out` saat didukung perubahan laju setelah mempertimbangkan perspektif. Nilai tempo shot tersendiri. Semua shot boleh `moderate` jika pengamatan mendukungnya.

Cantumkan estimasi per komponen jika bisa ditaksir secara wajar. Angka tunggal dan rentang sama-sama sah. Gunakan angka tunggal jika perkiraannya berdekatan. Perkiraan visual wajar diterima tanpa pengukuran piksel atau kalibrasi wajib.

## Kelengkapan notasi Camera Movement

Sebelum review, cocokkan `notation`, `observations`, dan frame pada fase yang sama. Periksa fase yang terlewat, kemungkinan Orbit terbaca sebagai Pan, dan arah badan atau sapuan yang terbalik. Masukkan setiap komponen dan qualifier yang didukung visual ke notasi. Validator memeriksa struktur dan sintaks. Ketepatan gerak diperiksa auditor dari frame.

## Detail desain dan framing

Nama setiap area fisik dengan label Inggris singkat dan Title Case. Gunakan `&` pada satu area yang berbagi fungsi. Biarkan renderer menggabungkan beberapa label dengan ` / `. Catat fungsi yang terlihat secara terpisah dan pakai label teknis berbahasa Inggris untuk pencarian. Tulis narasi dalam bahasa Indonesia. Pada shot multi-area, pilih panel sesuai kronologi dan beri nama momen dalam bahasa Inggris, seperti `Doorway`, bila terlihat jelas. Lihat [aturan penamaan](vocabulary.md#area-caption-dan-kontinuitas).

Nilai tipe rumah dari massa, tapak, akses dan susunan ruang. Pilih label Inggris yang paling sesuai dan gunakan `uncertain` untuk perkiraan yang wajar. [Panduan tipe rumah](vocabulary.md#tipe-rumah) memuat contoh label dan ciri visual.

Ringkas susunan ruang yang terlihat. Catat pencahayaan sebagai sumber, arah atau karakter cahaya, atmosfer sebagai kesan visual singkat, dan lingkungan sebagai kondisi fisik di sekitar rumah.

Pilih 4–6 warna yang mewakili desain bila cakupan video mencukupi. Amati bagian permukaan dengan pencahayaan merata dan hindari pantulan, bayangan pekat, serta area yang terlalu terang. Catat nama, peran, perkiraan HEX, dan frame bukti setiap warna. Detail Shot menjelaskan warna itu dipakai di mana.

Eksterior: gaya/massa, ukuran/proporsi, atap, fasad/bukaan, akses/teras, material/cahaya tampak dan lingkungan/tapak. Interior: geometri/volume/bukaan, layout/hubungan, bentuk/posisi/orientasi furnitur, penyimpanan/properti pembeda, material/cahaya dan lingkungan melalui bukaan.

Catat detail konkret, bukan daftar furnitur generik. Cocokkan text arsitektur/furnitur/lingkungan dengan fakta berkategori dan facet_roles. Tidak ada kuota fakta; validator struktural tidak membuktikan kelengkapan makna narasi.

Pilih gaya utama dari ciri arsitektur dominan yang konsisten, misalnya fasad berplester, genteng lengkung, dan bukaan lengkung berulang dapat mengarah ke `Spanish Colonial Revival`. Catat ciri dari gaya lain sebagai pengaruh bila terlihat. Jika petunjuk untuk label spesifik belum cukup, gunakan label yang lebih luas atau state `uncertain`.

Pisahkan bentuk yang terlihat dari tipe layout yang belum jelas. Contoh dapur: catat meja di sisi kiri dengan dua bangku sebagai fakta `observed`. Jika bagian yang memperlihatkan sambungan ke dinding atau kabinet berada di luar bingkai, catat tipe `island` atau `peninsula` sebagai `uncertain` bila perlu. Periksa hubungan meja dengan kabinet dari frame yang menunjukkan keduanya.

Nama gaya Inggris, penjelasan Indonesia, estimasi luas min–max wajib. Bedakan observed/uncertain/not-visible/not-present/unknown. Urutan edit bukan bukti denah atau satu rumah fisik. Jangan menegaskan material fisik dari tampilan saja.

Camera Start menjelaskan awal sumber. Untuk Overview, tulis paragraf singkat tentang posisi, arah pandang, dan bagian area yang terlihat pada frame wide, biasanya awal IN atau akhir OUT. Simpan perincian arsitektur, furnitur, dan lingkungan di uraian shot. Utamakan ciri yang membedakan area. Default produksi reverse/durasi/lima shot tidak mengubah kronologi, tempo atau pilihan audit sumber.

## Bantuan statistik gerak 2D

~~~sh
python tools/audit.py motion-hints work/audit/session.json --shot-id shot-02
python tools/audit.py motion-hints work/audit/session.json --shot-id shot-02 --details
~~~

Helper opsional memakai 32 frame dan lebar analisis 320 px secara default. Batasnya 64 frame dan 640 px. Keluaran ringkas memuat cakupan tracking, gap, rentang valid, dan tren awal, tengah, serta akhir menurut PTS. Opsi `--details` menampilkan matriks setiap interval. `total` berlaku pada rentang PTS yang diukur dan berisi `null` saat rantai tracking terputus.

Setiap segmen tren memuat `lower_minus_upper_fraction_per_s`, yaitu selisih laju geser horizontal zona bawah terhadap zona atas dalam fraksi lebar gambar per detik. Nilai positif berarti zona bawah bergeser lebih ke kanan relatif terhadap zona atas, dan nilai negatif berarti lebih ke kiri. `zone_coverage_fraction` menunjukkan bagian durasi segmen yang memiliki data kedua zona, dari 0 sampai 1. Laju `null` berarti data kedua zona tidak tersedia pada segmen itu. Laju `0` berarti selisih neto terukur nol.

Upper dan lower merujuk zona gambar. Gunakan selisih ini untuk memilih bagian yang perlu diperiksa lebih dekat, lalu nilai depth, translation, dan rotation dari frame untuk membedakan Pan, Orbit, dan Truck. Jika OpenCV atau NumPy tidak tersedia, lanjutkan audit visual. Helper menyimpan statistik di cache kerja dan deklarasi viewed tetap dilakukan setelah pemeriksaan frame.
