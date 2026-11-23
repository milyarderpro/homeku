# Rubrik audit dan kalibrasi HOMEKU

Gunakan penilaian berbukti, bukan skor total yang dapat menutupi salah arah kamera. Ketepatan satu angka tidak dapat menggantikan kelengkapan ruang atau salah identifikasi cut.

## Desain dan konfigurasi

| Aspek | Bukti yang dicatat | Kesalahan yang harus diperbaiki di chat |
| --- | --- | --- |
| Bentuk | Dinding/volume, bidang melengkung, proporsi tampak, level lantai/plafon | Hanya menyebut nama gaya dan warna |
| Isi | Elemen yang terlihat beserta bentuk, orientasi dan posisi relatif | Mengisi ruangan dari furnitur generik yang tidak terlihat |
| Hubungan | Susunan terhadap bukaan, sudut ruang, kabinet dan jalur yang tampak | Mengarang denah atau koneksi dari urutan edit |
| Pembeda | Kombinasi fungsi, solusi penyimpanan, bukaan, platform, ceruk | Menyamakan semua bathroom sebagai tub/vanity yang sama |
| Material/cahaya | Tampilan tekstur, warna, arah dan lapisan cahaya | Memastikan spesies kayu, batu asli, negara atau lux tanpa bukti |
| Ketidakpastian | Bagian tertutup/crop, fungsi parsial, tafsir alternatif | Mengubah not-visible menjadi not-present |

## Membedakan gerakan kamera

| Tafsir | Petunjuk pendukung | Batas tafsir |
| --- | --- | --- |
| Dolly-In/Out | Perubahan skala subjek beserta perubahan kedalaman/oklusi antar lapisan | Skala saja juga dapat berasal dari zoom/crop digital |
| Pan Left/Right | Reorientasi pandangan ke kiri/kanan dan pergeseran susunan elemen | Arah benda di layar berlawanan dengan rotasi kamera; bukan label gerak kamera otomatis |
| Truck/Tracking | Pergeseran lateral dengan parallax foreground/background | Translasi lateral tidak otomatis orbit |
| Orbit Left/Right | Perubahan sisi/sudut pandang mengelilingi jangkar dan hubungan perspektif | Jangan menyebut orbit hanya karena gambar bergeser mendatar |
| Tilt/Pedestal | Rotasi vertikal versus perpindahan ketinggian dengan parallax | Perubahan crop/kemiringan generatif dapat meniru keduanya |
| Zoom | Skala relatif cenderung berubah tanpa parallax yang mendukung translasi | Tidak cukup untuk mengklaim kamera fisik atau focal length |
| Uncertain/other | Bukti tidak membedakan beberapa tafsir atau label baru | Pertahankan teks/bukti dan alternatif; jangan paksa ke gerakan yang populer |

Perubahan perspektif pada video generatif juga dapat mengandung deformasi. Pisahkan petunjuk yang diamati dari interpretasi gerak. Estimasi derajat bukan hasil rekonstruksi pose 3D; ~2× harus menyebut jangkar dan dimensi/skalanya, bukan faktor percepatan.

## Tempo dan percepatan

Bandingkan perubahan pada interval waktu sama dalam shot yang sama: perpindahan jangkar relatif lebar gambar aktif, perubahan skala, perubahan sisi yang terlihat dan laju pengungkapan area. Jika ada black bar, bedakan bidang gambar aktif dari resolusi file. Tidak ada ambang fisik universal dari video monokuler.

| Label | Pedoman operasional |
| --- | --- |
| slow | Perubahan kecil per detik; reveal berlangsung bertahap dalam rentang yang diperiksa |
| moderate | Perubahan framing/kedalaman jelas dalam beberapa detik tanpa lompatan besar setiap interval |
| fast | Perubahan framing/skala/reveal besar dalam rentang pendek dibanding fase lain yang dikalibrasi |
| variable | Laju berubah bermakna; jelaskan urutan, misalnya awal slow lalu ekor moderate/fast |
| unknown | Bukti waktu/gerak tidak cukup; wajib jelaskan batasnya |

Kelancaran adalah karakter berbeda dari tempo. Gerakan smooth dapat fast; durasi shot pendek tidak otomatis gerak fast. Pisahkan ritme edit antarshot dari kecepatan kamera di dalam shot. Jangan memaksa distribusi label agar mengikuti dugaan bahwa sebagian besar koleksi sedang/cepat.

Accelerating memerlukan perubahan yang lebih besar pada interval akhir daripada awal, dengan jangkar/observasi yang dijelaskan. Pelebaran proyeksi saat mendekati objek tidak sendirian membuktikan percepatan fisik: gunakan istilah percepatan visual pada tafsir sumber dan beri batasnya. Jika kecepatan fisik tidak teridentifikasi, simpan batas tersebut dalam uncertainty.

## Konsistensi lintas model

1. Pakai MP4 dengan hash yang sama, template, kontrak dan pembagian fase yang eksplisit.
2. Periksa arah, IN/OUT, cut, fase, tempo dan posisi overview terlebih dahulu; label gaya diperiksa setelahnya.
3. Jika Gemini/GPT berbeda, bandingkan timestamp, jangkar dan bukti. Jangan memilih jawaban karena model lebih terkenal atau tulisan lebih panjang.
4. Koreksi di chat dan tampilkan kartu dari snapshot terbaru; MD lengkap tersedia. Tidak perlu mengaudit setiap pilot dua kali; kedua lingkungan diuji di antara enam pilot yang tersisa.
5. Catat lingkungan/model yang diketahui dan perbedaan yang diselesaikan. Kontrak tetap provisional sampai pengalaman nyata selesai.

## Siap ditinjau pengguna

- Seluruh durasi tercakup; cut dibedakan dari segmen fungsi.
- Seluruh area dan pembeda yang terlihat tercatat pada audit.json dan laporan MD hasil render, dengan bukti yang tepat.
- Kamera mempunyai arah, fase, estimasi besaran yang diusahakan, tempo, dasar dan batas; tidak ada default slow/frontal atau tilt tipis dari jitter.
- Gambaran area sesuai IN/OUT atau pengecualian dijelaskan; Overview memakai frame wide setiap area penting; paragraf composition_summary menjelaskan posisi/arah/sudut/tinggi/kemiringan/cakupan/elemen/kedalaman/cahaya pada foto itu.
- Gambar awal produksi dapat ditentukan dari posisi/peran frame dan target lintasan, tanpa mengubah kronologi sumber.
- Kandidat lolos validasi teknis di chat. Pengguna kemudian menilai isi; kelulusan kode tidak menjadi pengganti penilaian visual.


## Kriteria V2

- Seluruh aspek profil DNA dicatat beserta nilai/status/confidence/bukti, bukan hanya nama gaya. Unknown eksplisit untuk yang belum diketahui.
- Baseline 10 FPS mencakup setiap shot dan frame asli pertama/terakhir; pendalaman native dilaksanakan bila arah/fase/laju meragukan. Jumlah serta rentang dilaporkan dari indeks yang benar-benar dilihat.
- Gunakan aturan arah/fase pada protokol: pan murni menyapu berlawanan arah kamera; delta paralaks mendukung translasi tetapi perlu oklusi dan perspektif. Orbit mengubah sudut mengelilingi jangkar, truck menilai arah translasi dan orientasi pandangan.
- Drift/jitter kecil bukan tilt utama. Rotasi vertikal yang jelas dan berkelanjutan dibedakan dari perubahan tinggi. Penyebab goyangan atau penggunaan gimbal tidak dipastikan.
- Ringkasan literal, tabel fase dan kartu identik pada notasi. + untuk simultan, → untuk berurutan; timeline menampilkan waktu sumber; ringkasan, fase dan label gambar mengikuti notasi sumber satu paragraf.
- Usahakan ~×/~° dengan jangkar/basis. Rasio skala bukan faktor percepatan; angka tidak diketahui dijelaskan tanpa rekaan.
- audit.json menjadi satu sumber audit; MD enam bagian mengikuti template baku, dengan kategori Arsitektur, Furnitur & dekorasi, Lingkungan serta kamera sederhana dan teknis. Snapshot review mengikat JSON, MD, manifest dan seluruh media; ekspor tidak merender ulang.
- Nama gaya teknis berbahasa Inggris; identitas dan detail tidak hanya menyebut warna. Luas lantai wajib rentang positif, tampil sebagai angka m² tanpa catatan tambahan. Basis dan ketidakpastian tetap dalam JSON.
- Satu continuous take tetap satu shot; fungsi, area terlihat, rute yang dilalui dan fase gerak dibedakan. Multi area memakai panel dinamis yang cukup menjelaskan perjalanan, tanpa menambah cut rekaan.
- Media N+2: kolase per shot, Overview satu baris, Storyboard seluruh blok vertikal; normal caption shot-NN start/middle/end dan waktu di bawah foto, multi nama momen yang sesuai. Tidak ada frame terpisah dalam paket.

## Pemeriksaan format2.1 / report2.2.0

- Camera Pattern diturunkan dari depth_direction fase; source asli tidak berubah karena workflow produksi reverse. Netral bukan ambigu. Pola campuran tetap satu shot; penulisan IN – (OUT → IN) – NO IN/OUT mempunyai tiga slot.
- Camera Start menjelaskan start sumber, paragraf Overview menjelaskan pilihan wide. End OUT tidak disebut start sumber. Overview tengah tidak otomatis dapat menjalankan seluruh lintasan dari awal.
- Shot Timeline tepat lima kolom dengan notasi teknis; Tempo tetap pada detail. Tiga kategori desain A berupa uraian regular blockquote, label di luar; multi area dikelompokkan per area dengan A/B/C bold. B poin dan C paragraf biasa.
- Periksa seluruh Overview, Storyboard, kolase dan MD. Hanya camera: bold pada gambar; ukuran caption sama dengan notasi, waktu kanan atas tetap terbaca, padding bawah mengikuti teks terakhir. Teks panjang tidak menimpa foto.
- Batas60M piksel/gambar, sisi65000px,95MiB/file,256MiB ZIP/ekstraksi. Kegagalan ukuran diperbaiki lewat konfigurasi eksplisit sebelum review terakhir; tidak menghilangkan detail diam-diam.
