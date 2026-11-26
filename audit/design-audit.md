# Audit desain dan kurasi media HOMEKU 3.1

Mulai fase ini setelah `check-camera` lulus. Gunakan frame dan workspace yang sama. Isi desain, area, framing, panel dan Overview di `audit.json`. Cek struktur field di [panduan JSON](json-guide.md).

## Profil dan detail per area

Nama setiap area fisik dengan label Inggris singkat dan Title Case. Gunakan `&` pada satu area yang berbagi fungsi. Biarkan renderer menggabungkan beberapa label dengan ` / `. Catat fungsi yang terlihat secara terpisah dan pakai label teknis berbahasa Inggris untuk pencarian. Tulis narasi dalam bahasa Indonesia. Pada shot multi-area, pilih panel sesuai kronologi dan beri nama momen dalam bahasa Inggris, seperti `Doorway`, bila terlihat jelas. Lihat [aturan penamaan](vocabulary.md#area-caption-dan-kontinuitas).

Nilai tipe rumah dari massa, tapak, akses dan susunan ruang. Pilih label Inggris yang paling sesuai dan gunakan `uncertain` untuk perkiraan yang wajar. [Panduan tipe rumah](vocabulary.md#tipe-rumah) memuat contoh label dan ciri visual.

Ringkas susunan ruang yang terlihat. Catat pencahayaan sebagai sumber, arah atau karakter cahaya, atmosfer sebagai kesan visual singkat, dan lingkungan sebagai kondisi fisik di sekitar rumah.

Pilih 4–6 warna yang mewakili desain bila cakupan video mencukupi. Amati bagian permukaan dengan pencahayaan merata dan hindari pantulan, bayangan pekat, serta area yang terlalu terang. Catat nama, peran, perkiraan HEX, dan frame bukti setiap warna. Detail Shot menjelaskan warna itu dipakai di mana.

Eksterior: gaya/massa, ukuran/proporsi, atap, fasad/bukaan, akses/teras, material/cahaya tampak dan lingkungan/tapak. Interior: geometri/volume/bukaan, layout/hubungan, bentuk/posisi/orientasi furnitur, penyimpanan/properti pembeda, material/cahaya dan lingkungan melalui bukaan.

Catat detail konkret seperti bentuk, fungsi, posisi, orientasi, dan hubungan antarobjek. Cocokkan text arsitektur/furnitur/lingkungan dengan fakta berkategori dan facet_roles. Tidak ada kuota fakta; validator struktural tidak membuktikan kelengkapan makna narasi.

Pilih gaya utama dari ciri arsitektur dominan yang konsisten, misalnya fasad berplester, genteng lengkung, dan bukaan lengkung berulang dapat mengarah ke `Spanish Colonial Revival`. Catat ciri dari gaya lain sebagai pengaruh bila terlihat. Jika petunjuk untuk label spesifik belum cukup, gunakan label yang lebih luas atau state `uncertain`.

Pisahkan bentuk yang terlihat dari tipe layout yang belum jelas. Contoh dapur: catat meja di sisi kiri dengan dua bangku sebagai fakta `observed`. Jika bagian yang memperlihatkan sambungan ke dinding atau kabinet berada di luar bingkai, catat tipe `island` atau `peninsula` sebagai `uncertain` bila perlu. Periksa hubungan meja dengan kabinet dari frame yang menunjukkan keduanya.

Nama gaya Inggris, penjelasan Indonesia, estimasi luas min–max wajib. Bedakan observed/uncertain/not-visible/not-present/unknown. Urutan edit bukan bukti denah atau satu rumah fisik. Jangan menegaskan material fisik dari tampilan saja.

Camera Start menjelaskan awal sumber. Untuk Overview, tulis posisi kamera, arah pandang, dan cakupan area dalam frame wide. Biasanya gambaran terlengkap muncul di awal gerakan IN atau akhir OUT. Gunakan fase kamera yang sudah diperiksa untuk menjelaskan kesesuaian framing dengan lintasan. Susun panel dan rute sesuai kronologi MP4 sumber.

## Pemeriksaan sebelum finalisasi

- Cocokkan gaya utama, tipe rumah, palet, dan detail desain dengan bukti. Pastikan pencahayaan, atmosfer, dan lingkungan menjelaskan aspek yang berbeda. Isi luas lantai sebagai satu rentang min–max.
- Cocokkan detail per area dengan fakta eksplisit dan rujukan frame. Catat peralihan, penghubung, dan area yang hanya terlihat sesuai kronologi shot.
- Pilih [tiga panel jernih](json-guide.md#seleksi-dan-metadata) pada shot biasa. Bila ada Production Start, pakai frame itu sebagai panel Start. Camera Start tetap menjelaskan awal sumber.
- Periksa panel dan Overview yang dipilih. Dalami sekitar batas shot atau midpoint bila frame usulan tertutup blur. Gunakan [aturan penamaan](vocabulary.md#area-caption-dan-kontinuitas) dan lihat frame tambahan sebelum mendeklarasikan viewed.
