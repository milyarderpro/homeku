# Metode audit visual HOMEKU 3.1

Baca sebelum mengisi JSON. Periksa perjalanan utuh, lalu baseline berurutan per take kontinu. Ekstraksi bukan pengamatan. Hanya frame yang benar-benar dilihat boleh dinyatakan viewed.

## Sampling

Baseline 6 FPS ditambah frame native pertama/terakhir setiap shot. Sumber ≤6 FPS atau shot <1 detik diperiksa seluruh native. Tidak ada interpolasi. Periksa midpoint dan pilihan panel/Overview yang belum tercakup. Pendalaman 10 FPS/native hanya untuk pertanyaan visual tertentu, lalu perluas bila belum terjawab. Ringkasan 6–10 momen tidak menggantikan baseline.

Cut memakai indeks dan PTS native. Pergantian area tanpa cut tetap satu shot; rute yang dimasuki berbeda dari area yang hanya terlihat.

## Urutan keputusan per fase

Baca [camera-cases.md](camera-cases.md) sebelum menganalisis kamera. Setelah meninjau baseline, pilih sekitar 6–10 frame pembanding sesuai durasi dan kerumitan shot.

1. **Temukan kandidat batas fase.** Bandingkan beberapa frame berurutan pada awal shot sebelum menilai rentang yang lebih panjang. Cari kapan masing-masing komponen mulai, bertumpang tindih, atau berhenti. Untuk setiap dugaan batas, bandingkan frame sebelum dan sesudahnya memakai jangkar yang sama. Perubahan area serta tempo bisa berlangsung dalam satu fase gerak.
2. **Nilai kedalaman.** Bandingkan ukuran bagian yang sama pada jangkar yang sama, lapisan dekat dan jauh, serta ruang yang terbuka. Uji kemungkinan Dolly dan Zoom sebelum menyimpulkan arah kedalaman. Pembesaran saja juga dapat terjadi karena Zoom.
3. **Pisahkan lintasan badan dan arah pandang.** Bandingkan satu jangkar dekat, satu jangkar jauh, dan orientasi satu bidang pada frame yang sama. Cari komponen lateral atau vertikal serta rotasi yang berlangsung bersamaan. Gunakan panduan Pan, Orbit, dan Truck di bawah.
4. **Tegaskan fase dan notasi.** Cocokkan dugaan batas dengan frame dan komponen yang benar-benar berubah. Pakai `+` hanya pada rentang saat komponen terlihat bersamaan. Ringkasan turunan memakai `→` antar fase. Jika pendekatan mulai setelah orbit, pisahkan fase awal dan fase overlap, lalu periksa apakah orbit masih tampak di akhir. Lihat [contoh perbandingan frame](camera-cases.md#contoh-awal-overlap-dan-akhir-komponen). Baru kemudian nilai estimasi besaran, lintasan, intensitas, dan profil laju tiap komponen.

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

Sebelum menjalankan check-camera, cocokkan `notation`, `observations`, dan frame pada fase yang sama. Periksa fase yang terlewat, kemungkinan Orbit terbaca sebagai Pan, dan arah badan atau sapuan yang terbalik. Masukkan setiap komponen dan qualifier yang didukung visual ke notasi. Validator memeriksa struktur dan sintaks. Ketepatan gerak diperiksa auditor dari frame.

## Production Start

Jika awal shot tertutup transisi, periksa frame di sekitar batas. Pilih frame jernih pertama yang bisa dipakai untuk mulai produksi dan catat framing-nya. Gunakan `composition.production_start` sesuai [panduan JSON](json-guide.md#seleksi-dan-metadata). Camera Start tetap menjelaskan awal sumber. Jika belum ada frame yang layak, catat keterbatasannya di `notes`.

## Bantuan statistik gerak 2D

~~~sh
python tools/audit.py motion-hints work/audit/session.json --shot-id shot-02
python tools/audit.py motion-hints work/audit/session.json --shot-id shot-02 --details
~~~

Helper opsional memakai 32 frame dan lebar analisis 320 px secara default. Batasnya 64 frame dan 640 px. Keluaran ringkas memuat cakupan tracking, gap, rentang valid, dan tren awal, tengah, serta akhir menurut PTS. Opsi `--details` menampilkan matriks setiap interval. `total` berlaku pada rentang PTS yang diukur dan berisi `null` saat rantai tracking terputus.

Setiap segmen tren memuat `lower_minus_upper_fraction_per_s`, yaitu selisih laju geser horizontal zona bawah terhadap zona atas dalam fraksi lebar gambar per detik. Nilai positif berarti zona bawah bergeser lebih ke kanan relatif terhadap zona atas, dan nilai negatif berarti lebih ke kiri. `zone_coverage_fraction` menunjukkan bagian durasi segmen yang memiliki data kedua zona, dari 0 sampai 1. Laju `null` berarti data kedua zona tidak tersedia pada segmen itu. Laju `0` berarti selisih neto terukur nol.

Upper dan lower merujuk zona gambar. Gunakan selisih ini untuk memilih bagian yang perlu diperiksa lebih dekat, lalu nilai depth, translation, dan rotation dari frame untuk membedakan Pan, Orbit, dan Truck. Jika OpenCV atau NumPy tidak tersedia, lanjutkan audit visual. Helper menyimpan statistik di cache kerja dan deklarasi viewed tetap dilakukan setelah pemeriksaan frame.
