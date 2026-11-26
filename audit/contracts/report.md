# Kontrak laporan manusia HOMEKU 3.1

analysis.md hanya dihasilkan renderer dari audit.json dan metadata manifest; tidak menjadi input authoring atau sumber fakta generator. Template resmi tools/assets/templates/analysis.md memiliki enam bagian berurutan:

1. Profil desain memuat nama, tipe rumah, gaya utama, pengaruh gaya, gaya interior, susunan ruang utama, ciri khas, material utama, pencahayaan, atmosfer, lingkungan, dan tabel Palet warna.
2. Ukuran & proporsi: skala, massa, tingkat/atap, tapak, proporsi dan perkiraan luas lantai min–max.
3. Shot Timeline: durasi, jumlah shot, Camera Pattern dan tabel shot/waktu/durasi/area/kamera.
4. Overview: gambar wide satu baris beserta paragraf komposisi masing-masing pilihan.
5. Storyboard: kolase seluruh shot tersusun vertikal.
6. Shot Details: satu blok per take kontinu, gambar kolase dan A. Desain area, B. Framing & Lighting, C. Camera Movement.

Palet warna memakai tabel Peran, Warna, HEX di bagian bawah Profil Desain. Detail Shot mencatat penggunaan warna dan cahaya setempat.

Nama gaya teknis memakai bahasa Inggris; penjelasan bahasa Indonesia. Luas cukup **60–90 m²**, tanpa dasar perkiraan atau label kepastian tambahan wajib. Narasi sumber dipertahankan utuh dan di-escape untuk keamanan tampilan; renderer tidak mengarang, menerjemahkan ulang atau menyimpulkan isi.

Nama area berasal dari `areas[].label` untuk laporan, kolase, Storyboard, dan Overview. Audit baru memakai nama Inggris Title Case. ` / ` menyambung label area fisik yang berbeda pada judul. Overview memakai area yang masuk di frame wide terpilih.

Paragraf Overview menjelaskan posisi kamera, arah pandang dan bagian area yang masuk dalam frame wide. Rincian bahan tampak, susunan furnitur dan ciri desain dijelaskan di bagian A. Gunakan paragraf singkat dengan ciri pembeda di awal.

A memuat arsitektur, furnitur/dekorasi dan lingkungan per area. B memuat fokus, posisi/arah/sudut/ketinggian/kemiringan Camera Start, framing awal→akhir, pencahayaan, foreground, kedalaman, reveal dan kesesuaian gerak. Multi area juga menampilkan rute, penghubung, visibilitas/peralihan dan orientasi ruang yang dinyatakan. C memuat gerakan Indonesia singkat-lengkap, tempo, alur visual bila diperlukan, timeline fase dan notasi teknis satu paragraf.

Camera Start menjelaskan awal sumber. Jika `composition.production_start` tersedia, tampilkan satu baris `Production Start` tepat setelah Camera Start, dengan indeks native, waktu dari frame map, dan framing singkat. Overview memiliki framing tersendiri dan dapat berada di akhir OUT. Kamera teknis berasal dari urutan notation fase, bukan field summary manual. Jika tempo berubah, tampilkan interval, label dan deskripsi tiap segmen. Tempo fase diturunkan dari segmen yang bertumpang tindih. Tidak ada tabel parser, log atau esai teknis pemeriksaan dalam laporan manusia.

Media: satu kolase per shot normal tiga panel jernih Start/Middle/End dengan waktu frame terpilih. Jika ada Production Start, frame tersebut tampil sebagai Start. Multi-area memakai awal, akhir, dan momen penting sesuai kebutuhan. Caption di bawah foto: label tebal, waktu lebih kecil. Header shot memuat ID/area dan rentang/durasi tanpa baris caption berulang. Overview satu baris; Storyboard vertikal. Identitas memuat ID referensi – gaya utama – durasi x.xxs – jumlah shot.

Validasi menolak MD yang tidak cocok dengan hasil renderer, bagian hilang atau media tidak terdaftar. Gambar/teks/manifest menjadi satu snapshot yang ditinjau sebelum ekspor.
