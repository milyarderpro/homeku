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
5. **Besaran/tempo:** angka dapat diperkirakan visual; nilai tempo dari perubahan per waktu setara, bukan kesan smooth.

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

Format: [Komponen Utama] ([Skala]) [+ / →] [Komponen Sekunder] ([Intensitas / Kurva]). Angka opsional per komponen; angka tunggal/rentang sah. Gerak tanpa angka tidak memerlukan alasan khusus atau penurunan confidence. Asumsi visual wajar diterima tanpa kewajiban piksel/kalibrasi. Lihat camera-cases.md.

~× adalah rasio skala gambar IN=akhir/awal, OUT=awal/akhir; bukan faktor kecepatan/jarak fisik. Gunakan jangkar yang sebanding; jangan memberi rasio gabungan yang sama pada Dolly dan Zoom bila kontribusinya tidak terpisahkan. ~° dapat diperkirakan dari perubahan orientasi; jangan menyatakan estimasi sebagai pose fisik terukur.

Semua shot moderate sah. Smooth bukan slow; pembesaran perspektif tidak sendirian membuktikan accelerating. Easing/intensitas berlaku pada komponennya, tidak otomatis menjadi tempo seluruh shot. Simpan tempo sekali, seragam atau segments; batasnya tidak harus sama dengan fase gerak.

## Detail desain dan framing

Eksterior: gaya/massa, ukuran/proporsi, atap, fasad/bukaan, akses/teras, material/cahaya tampak dan lingkungan/tapak. Interior: geometri/volume/bukaan, layout/hubungan, bentuk/posisi/orientasi furnitur, penyimpanan/properti pembeda, material/cahaya dan lingkungan melalui bukaan.

Catat detail konkret, bukan daftar furnitur generik. Cocokkan text arsitektur/furnitur/lingkungan dengan fakta berkategori dan facet_roles. Tidak ada kuota fakta; validator struktural tidak membuktikan kelengkapan makna narasi.

Nama gaya Inggris, penjelasan Indonesia, estimasi luas min–max wajib. Bedakan observed/uncertain/not-visible/not-present/unknown. Urutan edit bukan bukti denah atau satu rumah fisik. Jangan menegaskan material fisik dari tampilan saja.

Camera Start menjelaskan awal sumber. Overview menjelaskan frame wide yang dipilih, biasanya awal IN atau akhir OUT; posisi/arah/angle dan cakupannya harus jelas. Default produksi reverse/durasi/lima shot tidak mengubah kronologi, tempo atau pilihan audit sumber.

## Bantuan statistik gerak 2D

~~~sh
python tools/audit.py motion-hints work/audit/session.json --shot-id shot-02
python tools/audit.py motion-hints work/audit/session.json --shot-id shot-02 --details
~~~

Helper opsional memakai 32 frame dan lebar analisis 320 px secara default. Batasnya 64 frame dan 640 px. Keluaran ringkas memuat cakupan tracking, gap, rentang valid, dan tren awal, tengah, serta akhir menurut PTS. Opsi `--details` menampilkan matriks setiap interval. `total` berlaku pada rentang PTS yang diukur dan berisi `null` saat rantai tracking terputus.

Upper dan lower merujuk zona gambar. Putuskan arah dan jenis gerak dari pengamatan visual tiga sumbu. Jika OpenCV atau NumPy tidak tersedia, lanjutkan audit visual. Helper menyimpan statistik di cache kerja dan deklarasi viewed tetap dilakukan setelah pemeriksaan frame.
