# Protokol audit HOMEKU V2

Workflow sumber/paket2.1 dan renderer/media2.2.0. Kontrak tetap provisional sampai pilot nyata selesai. Prinsip berlaku untuk ratusan sumber, bukan hanya tujuh pilot.

## Urutan audit

1. Buka kit dan jalankan bootstrap, baca template/panduan. Inspect MP4: ID, SHA-256, durasi stream video, dimensi, FPS rasional dan PTS native. Operasi alat dijalankan nyata; tidak diisi dari dugaan model.
2. Tentukan cut/take dari seluruh video dan perubahan di batasnya. Satu take exterior → living → kitchen tanpa cut tetap satu shot. Area fisik, fungsi, area terlihat, rute dilalui serta fase kamera dicatat terpisah.
3. Periksa baseline **10 FPS sepanjang setiap shot**, termasuk frame asli pertama/terakhir. Sumber di bawah 10 FPS memakai seluruh frame tersedia. Lihat setiap gambar terpilih; frame yang diekstrak belum otomatis viewed.
4. Perdalam **semua frame native** pada rentang arah/fase/laju, oklusi, blur atau detail yang meragukan. Awali 0.5–1s bila cocok, perluas sampai seluruh shot bila perlu. Native dapat 24/30/60 FPS atau lainnya tanpa interpolasi. Pendalaman yang diperlukan harus selesai sebelum review final.
5. Audit desain/komposisi: nama gaya English, ukuran/proporsi dan luas wajib, tiga kategori narasi area, konfigurasi/orientasi/penyimpanan/bukaan, cahaya/lingkungan, posisi dan framing awal. Status/basis/bukti disimpan eksplisit dalam JSON.
6. Audit kamera dengan tiga tes di bawah. Catat semua komponen simultan, urutan fase, depth_direction, estimasi skala/sudut, jangkar, tempo dan perubahan penting. Sumber diikuti apa adanya; tidak ada reverse, durasi 4/6s, default slow atau frontal produksi.
7. Pilih panel setelah memahami perjalanan. Normal Start/Middle/End; multi dinamis paling sedikit yang cukup menjelaskan area/penghubung/reveal/perubahan penting. Overview seluruh area biasanya awal IN/akhir OUT; alasan dan satu composition_summary per frame dicatat. Posisi awal sumber tetap tersimpan terpisah. Satu frame dapat mencakup beberapa area tanpa duplikasi.
8. Isi audit.json dan metadata/log nyata, kemudian draft-v2. Periksa silang narasi/fakta, kamera sederhana/teknis, timeline/fase/tempo dan semua pilihan media. Jalankan review dan tampilkan MD manusia enam bagian, Overview, Storyboard serta kolase seluruh shot.
9. Koreksi di chat memperbarui JSON dan pemeriksaan yang benar-benar diulang; draft/review ulang kandidat lengkap. Persetujuan satu shot/aspek bukan seluruh kandidat.
10. Setelah pengguna menyatakan keseluruhan kandidat terbaru sesuai, export-v2 memakai receipt/digest terakhir. Tidak merender ulang. Validasi folder dan ZIP dibuka ulang; pengguna mengunduh satu ZIP lalu ingest lokal tanpa review isi kedua.

## Aturan Penentuan Arah & Fase

| Aspek | Keputusan berdasarkan bukti |
| --- | --- |
| Pan murni | Rotasi pandangan; pada scene statis gambar menyapu kiri mendukung Pan Right dan sebaliknya. Foreground/background relatif serempak. Jangan menentukan arah hanya dari gerak satu objek |
| Oklusi foreground | Pergeseran kusen/meja/tiang yang menutupi atau membuka elemen belakang mendukung translasi. Periksa bersama perspektif dan jangkar |
| Paralaks | Foreground lebih ke kanan relatif background mendukung translasi kamera ke kiri; kebalikannya mendukung kanan. Delta bukan tes tunggal, terutama bila dolly/pan/generatif bercampur |
| Orbit / truck | Orbit mengubah sudut/sisi mengelilingi jangkar yang tetap terbingkai. Truck menilai geser lateral serta orientasi pandangan; perpindahan layar saja tidak membuktikan orbit |
| Dolly / zoom | Skala bersama perubahan kedalaman/oklusi mendukung dolly. Skala saja tidak membuktikan gerak fisik atau focal length |
| IN / OUT | depth_direction setiap fase: IN/OUT/NO IN/OUT/null ambigu. Pan/orbit/zoom/static tidak otomatis maju/mundur; jangan menyamakan belum diketahui dengan netral |
| Fase | + hanya komponen simultan pada interval yang sama. → saat komponen mulai/berhenti/berubah. Area atau tempo berubah saja tidak memaksa fase baru |
| Tilt | Drift/jitter vertikal kecil tidak disebut subtle tilt. Tilt nyata memerlukan rotasi vertikal jelas dan berkelanjutan, berbeda dari pedestal/perubahan tinggi; penggunaan gimbal tidak disimpulkan dari gambar |

Pola per shot/video dihitung helper dari klasifikasi fase; bukan ringkasan manual kedua. Fase netral awal + IN tetap IN, perubahan IN/OUT nyata tetap berurutan. Jika arah berubah, pisahkan fase pada bukti perubahan tersebut. Notasi summary/fase satu paragraf tanpa Enter setelah → atau +.

Usahakan ~× dan ~° dari jangkar yang dilihat. ~× adalah rasio skala, bukan kelipatan kecepatan. Bila sudut tertentu tidak dapat dipisahkan dari gerak gabungan, simpan keterbatasan pada basis/uncertainty; jangan mengarang presisi. Bahasa sederhana harus membedakan badan kamera melingkar ke kiri dari pandangan memutar ke kanan.

## Tempo, cakupan dan pemulihan

Smooth tidak berarti slow. Bandingkan perubahan per interval waktu sama: skala jangkar, bukaan sisi, lintasan dan reveal. Simpan tempo_profile moderate/fast/dll beserta perubahan yang benar-benar diamati; variable tidak menggantikan label kecepatannya. Bedakan tempo kamera dari ritme cut.

Frame review mencatat selected indices dan viewed indices nyata; record sampling/native harus sesuai PTS. Jika dibagi beberapa rentang, baseline tetap mencakup shot tanpa gap. Native overlap baseline sah; jangan menjumlahkan duplikat sebagai frame unik. Audio hanya diklaim bila benar-benar diperiksa. Durasi video dapat berbeda dari container/audio.

Semua frame audit/contact sheet sementara berada di workspace kerja. Paket final hanya kolase per shot, Overview satu baris dan Storyboard vertikal seluruh blok, tanpa motion/, klip shot atau frame terpisah. Jika workspace/sumber hilang, pulihkan dari sumber dan JSON terbaru; jangan membuat bukti/hash palsu. Masalah teknis diselesaikan di chat sebelum ZIP final.

Sebelum ingest, koreksi chat tetap dapat memakai revisi yang sama. Setelah revisi aktif, gunakan +1 dan supersedes benar. Dokumen bekerja/masterprompt hanya acuan tes pembeda/notasi; ketentuan produksi tidak menjadi aturan audit pustaka.
