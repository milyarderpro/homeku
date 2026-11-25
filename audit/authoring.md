# Menyiapkan audit HOMEKU 3.0

Baca [panduan visual](visual-audit.md). Tulis pengamatan di satu `audit.json`. Helper menyiapkan frame dan metadata dari video sumber.

## Siapkan workspace

Jalankan `inspect` dan tentukan cut nyata pada video. Simpan indeks native **frame pertama setelah setiap cut** dalam `work/cuts.json`. Gunakan `[]` untuk satu take kontinu, termasuk jika kamera melewati beberapa area.

~~~sh
python tools/audit.py inspect /path/rumah.mp4
python tools/audit.py prepare /path/rumah.mp4 --cuts-file work/cuts.json --output work/audit
~~~

Workspace berisi `session.json`, kerangka `audit.json`, `audit-info.json` dan sheet. Baseline mencakup 6 FPS dan batas native. Sumber ≤6 FPS atau shot <1 detik memakai seluruh frame native. Helper menyiapkan pula frame terdekat dari midpoint. Gunakan `--resume` pada sumber dan cut yang sama untuk mempertahankan isi serta deklarasi sebelumnya.

## Tulis pengamatan

Nilai tipe rumah, susunan ruang, pencahayaan, atmosfer, dan lingkungan. Isi palet HEX dari frame yang diperiksa dan cantumkan bukti per warna. Gunakan [contoh tipe rumah](vocabulary.md#tipe-rumah) dan [panduan pengisian profil](json-guide.md#profil-desain).

Isi nama gaya dalam bahasa Inggris dan narasi dalam bahasa Indonesia. Tulis rentang luas lantai, identitas area, detail desain beserta fakta dan bukti, framing awal, Overview, serta kamera dan tempo. [Panduan JSON](json-guide.md) menjelaskan field. Contoh normal dan multi area merupakan fixture sintetis.

Tulis pengamatan depth, translation dan rotation sebelum notasi tiap fase. Nilai besaran setiap komponen dan cantumkan estimasi skala atau sudut jika dapat diperkirakan secara wajar. Jika hanya sebagian komponen dapat ditaksir, tulis angka pada bagian itu. Lihat [contoh kamera](camera-cases.md).

Periksa sheet lalu tandai frame yang sudah dilihat. Gunakan `--all-passes --all` setelah semua pass selesai diperiksa atau `--pass-id <ID> --frames <INDEKS...>` untuk bagian yang sudah dilihat.

~~~sh
python tools/audit.py mark-viewed work/audit/session.json --all-passes --all
python tools/audit.py sample --session work/audit/session.json --shot-id shot-02 --fps 10 --start 2.4 --end 2.9 --reason "Perubahan oklusi kusen untuk membedakan Orbit dan Pan"
~~~

Sesuaikan waktu pendalaman dengan PTS nyata dalam shot. Gunakan `--native` bila diperlukan, atau `sample --session work/audit/session.json --frames 24 31 --reason "Pilihan Overview tambahan"` untuk indeks tertentu. Lihat frame baru sebelum mendeklarasikan viewed.

Koreksi satu shot dapat dikirim lewat file berisi objek JSON, misalnya `{"camera":{"description":"Kamera mundur menuju lorong."}}`. Helper menggabungkan objek dan mengganti array utuh bila disertakan. Update area global langsung di sumber. Shot ID, batas waktu dan jenis transisi terkunci pada helper.

~~~sh
python tools/audit.py update-shot work/audit/session.json --shot-id shot-02 --patch work/koreksi.json
~~~

## Periksa input

Isi metode, batas pemeriksaan dan identitas model yang diketahui di `audit-info.json`. Build yang tidak diketahui diisi `null`. `complete` menata notasi, menetapkan pilihan panel native yang ditentukan kontrak, dan menyalin deklarasi viewed dari sesi.

~~~sh
python tools/audit.py complete work/audit/audit.json --session work/audit/session.json
python tools/audit.py check-input /path/rumah.mp4 work/audit/audit.json --audit-info work/audit/audit-info.json
~~~

Perbaiki field yang ditunjuk `check-input`. Untuk bukti yang belum dilihat, ambil frame yang tepat dan periksa sebelum memperbarui deklarasi. Untuk tahap peninjauan dan penyerahan, ikuti [kontrak paket](contracts/package.md).

Untuk pertanyaan visual yang masih ambigu, gunakan [bantuan statistik gerak 2D](visual-audit.md#bantuan-statistik-gerak-2d) bila lingkungan mendukungnya.

## Periksa isi sebelum memperlihatkan kandidat

- Cocokkan cut, scope area, pengamatan tiga sumbu, notasi, tempo, dan bukti pada shot yang sama.
- Periksa [kelengkapan notasi](visual-audit.md#kelengkapan-notasi-camera-movement) pada tiap fase. Pastikan jenis, arah, lintasan, intensitas, profil laju, dan estimasi yang didukung frame muncul pada komponen yang tepat. Cocokkan `notation` dengan `observations` dan deskripsi. Gunakan frame tambahan hanya jika ada pertanyaan visual spesifik yang belum terjawab.
- Periksa tipe rumah dan sumber buktinya. Cocokkan palet HEX dengan frame yang diperiksa serta pastikan pencahayaan, atmosfer, dan lingkungan masing-masing menyampaikan hal yang berbeda.
- Baca narasi desain bersama fakta yang terkait. Cocokkan gaya utama dengan ciri arsitektur dominan. Periksa bentuk bukaan, material tampak, lampu, dan fungsi furnitur. Pisahkan konfigurasi yang terlihat dari tipe layout yang masih belum pasti.
- Periksa panel awal terhadap posisi Camera Start. Pastikan Overview menjelaskan cakupan wide, sementara uraian shot memuat detail desain. Ringkas detail berulang agar tiap bagian mudah dipindai.
- Cocokkan nama area Inggris Title Case di laporan dan media. Gunakan `&` untuk fungsi dalam satu area. Periksa bahwa judul shot memakai ` / ` antararea dan caption momen multi-area sesuai gambar. Baca laporan enam bagian dan periksa gambar pada semua kolase. Untuk penyesuaian ukuran, ubah parameter render sebelum peninjauan berikutnya.

Draft memakai kualitas JPEG 91 dan skala 1 secara default. Gunakan `--scale`, `--overview-scale`, `--storyboard-scale` atau `--columns` jika tata letak melebihi batas. Satu JPEG dapat memuat sampai 60 juta piksel dengan sisi sampai 65.000 px. Batas file 95 MiB dan batas ZIP terurai 256 MiB.

## Tinjau kandidat dan serahkan ZIP

~~~sh
python tools/audit.py draft /path/rumah.mp4 work/audit/audit.json --audit-info work/audit/audit-info.json --output work/candidate
python tools/audit.py review work/candidate/rumah --output work/review.md
~~~

Setelah `review` berhasil, langsung jalankan ekspor dengan receipt kandidat tersebut. Simpan receipt di luar folder kandidat.

~~~sh
python tools/audit.py export work/candidate/rumah --receipt work/review.md.json --output work/final
~~~

Tampilkan laporan ringkasan dari table setiap shot nya, gambar Overview dan Storyboard, serta tautan unduhan ZIP tanpa MP4 dalam balasan yang sama. Jika ada koreksi, perbarui audit kerja, ulangi draft dan review, lalu ekspor dengan receipt terbaru. Berikan tautan ke ZIP hasil koreksi.

Untuk revisi referensi yang sudah aktif, gunakan nomor berikutnya pada audit dan berikan `--supersedes` dengan revision dan content_sha256 dari entri aktif.
