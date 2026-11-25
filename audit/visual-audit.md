# Metode audit visual HOMEKU 3.0

Baca sebelum mengisi JSON. Periksa perjalanan utuh, lalu baseline berurutan per take kontinu. Ekstraksi bukan pengamatan. Hanya frame yang benar-benar dilihat boleh dinyatakan viewed.

## Sampling

Baseline 6 FPS ditambah frame native pertama/terakhir setiap shot. Sumber ≤6 FPS atau shot <1 detik diperiksa seluruh native. Tidak ada interpolasi. Periksa midpoint dan pilihan panel/Overview yang belum tercakup. Pendalaman 10 FPS/native hanya untuk pertanyaan visual tertentu, lalu perluas bila belum terjawab. Ringkasan 6–10 momen tidak menggantikan baseline.

Cut memakai indeks dan PTS native. Pergantian area tanpa cut tetap satu shot; rute yang dimasuki berbeda dari area yang hanya terlihat.

## Urutan keputusan per fase

1. **Depth:** bandingkan ukuran jangkar yang sama, lapisan dekat/jauh, oklusi dan ruang yang terbuka. Periksa Dolly/Zoom sebelum menyimpulkan Pan-only atau netral.
2. **Translation:** periksa gerak badan kamera lateral/vertikal melalui paralaks, perubahan sisi dan hubungan foreground/background.
3. **Rotation:** periksa putaran arah pandang terhadap jangkar. Jangan hanya mencatat komponen paling menonjol; translasi dan rotasi dapat simultan.
4. **Fase:** pisahkan ketika komponen mulai/berhenti/berubah, bukan semata area atau tempo berubah. + simultan; → antar fase, satu paragraf.
5. **Besaran dan tempo:** nilai besaran setiap komponen dari perubahan visual sepanjang fase. Nilai tempo dari perubahan per waktu setara, secara terpisah.

Simpan observations depth/translation/rotation spesifik pada fase, dengan bukti temporal bersama. Override komponen hanya jika bukti/ambiguitas berbeda. Minimal dua frame temporal berbeda pada fase/toleransi satu batas native yang dinyatakan; jangan mengarang evidence agar lolos.

## Pan, Orbit dan Truck

| Tafsir | Oklusi / paralaks | Perspektif dan jangkar |
| --- | --- | --- |
| Pan | Scene tersapu; geser layar saja bukan bukti translasi | Arah pandang berputar, perubahan sisi subjek tidak seperti lintasan mengelilinginya |
| Orbit | Lapisan dekat/jauh bergeser berbeda, foreground membuka/menutupi latar | Sisi/sudut subjek berubah sepanjang lintasan mengitari jangkar |
| Truck | Badan kamera bergeser lateral, lapisan dekat bergerak berbeda dari latar | Translasi menyamping; orientasi relatif tetap atau dikompensasi Pan |

Gunakan ketiga tes bersama. Pada scene statis, Pan Right umumnya menggeser gambar ke kiri. Jika foreground yang benar-benar dekat bergeser lebih ke kanan daripada background, badan kamera cenderung bergerak ke kiri; periksa perspektif untuk membedakan Orbit Left dan Truck Left. Tanda terbalik berlaku untuk gerak kanan. Satu tanda delta/oklusi tidak membuktikan pose 3D; distorsi lensa, zoom, objek bergerak dan deformasi generatif dapat mengacaukan petunjuk.

Kusen yang membuka/menutupi sakelar atau nakas sambil sisi objek berubah perlu diuji sebagai translasi/orbit, bukan otomatis Pan. Dolly-Out + Orbit Left + Pan Right dapat simultan: mundur, badan melingkar kiri dan pandangan berputar kanan. Ini contoh pembacaan, bukan jawaban default video.

Goyangan/drift vertikal tipis akibat berjalan atau proyeksi wide bukan Tilt. Catat Tilt hanya bila rotasi vertikal disengaja terlihat jelas dan berkelanjutan; bedakan dari pedestal. Jangan menebak pemakaian gimbal.

## Arah, notasi dan tempo

Depth_direction auditor: IN, OUT, NO IN/OUT atau null ambigu. Pan/Static/Zoom bisa tidak mempunyai translasi depth. Zoom atau pembesaran skala saja tidak membuktikan Dolly. Camera Pattern dihitung dari arah fase, bukan dari narasi atau default produksi.

Format: [Komponen Utama] ([Skala]) [+ / →] [Komponen Sekunder] ([Intensitas / Kurva]).

Evaluasi besaran setiap komponen gerak sesuai jenisnya. Cantumkan estimasi skala (~×) atau sudut (~°) jika petunjuk visual cukup untuk membuat perkiraan yang wajar. Angka tunggal dan rentang sama-sama sah. Hilangkan angka hanya pada komponen yang besarannya sulit diperkirakan secara wajar. Asumsi visual wajar diterima tanpa pengukuran piksel atau kalibrasi wajib. Lihat [contoh kamera](camera-cases.md).

- **Skala (~×).** Bandingkan dimensi yang sama dari jangkar yang sama pada awal dan akhir fase, misalnya tinggi pintu yang terlihat utuh. Untuk pembesaran, gunakan akhir/awal. Untuk pengecilan, gunakan awal/akhir. Rasio ini menyatakan perubahan skala gambar. Jika Dolly dan Zoom tidak dapat dipisahkan, hindari pemberian rasio gabungan pada masing-masing komponen.
- **Sudut (~°).** Perkirakan Pan atau Tilt dari perubahan arah pandang terhadap jangkar. Untuk Orbit, bandingkan perubahan sisi yang terlihat sepanjang lintasan mengitari subjek. Pergeseran jangkar di layar saja belum cukup untuk menaksir sudut masing-masing ketika Pan mengompensasi Orbit.

Semua shot moderate sah. Smooth bukan slow; pembesaran perspektif tidak sendirian membuktikan accelerating. Easing/intensitas berlaku pada komponennya, tidak otomatis menjadi tempo seluruh shot. Simpan tempo sekali, seragam atau segments; batasnya tidak harus sama dengan fase gerak.

## Detail desain dan framing

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

Upper dan lower merujuk zona gambar. Putuskan arah dan jenis gerak dari pengamatan visual tiga sumbu. Jika OpenCV atau NumPy tidak tersedia, lanjutkan audit visual. Helper menyimpan statistik di cache kerja dan deklarasi viewed tetap dilakukan setelah pemeriksaan frame.
