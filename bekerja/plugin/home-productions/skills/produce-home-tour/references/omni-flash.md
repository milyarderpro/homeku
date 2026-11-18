# Prompt Omni Flash, paket proyek dan revisi

Gunakan setelah pasangan frame final benar-benar tersedia, dilihat dan disetujui atau didelegasikan. Ikuti [kontrak proyek](project-contract.md) dan [aturan produksi](production-rules.yaml). Jangan melompati produksi/review gambar dengan membuat prompt dari nama file saja.

## Batas generator yang diketahui

Dukungan Omni Flash untuk dua gambar awal–akhir dan durasi klip 4–10 detik mengikuti konfirmasi pengguna. Uji ulang generator dilewati atas arahan pengguna. Nama aplikasi, versi, label tombol dan parameter API belum ditetapkan; jangan mengarangnya atau mewajibkan pengguna menjelaskannya kembali untuk menyiapkan paket.

Petunjuk pemakaian disusun menurut fungsi: pasang gambar awal, gambar akhir, prompt shot, dan durasi shot pada kontrol yang benar-benar tersedia. Pengaturan lain hanya disebut setelah terlihat pada lingkungan pengguna. Jika antarmuka tidak dapat memenuhi pasangan/durasi tersebut, nyatakan kendalanya; jangan diam-diam mengganti pola, mempercepat atau memangkas klip.

Video lengkap dibuat dari klip per shot, bukan satu permintaan sepanjang total proyek. Exterior, exterior-to-living dan living-to-kitchen tetap 6 detik; shot area lain 4 detik. Luas cakupan, jumlah bedroom dan urutan tidak berubah pada tahap prompt.

## Menulis prompt dari gambar final

Lihat frame awal dan akhir yang dipilih setiap shot. Cocokkan dengan framing, lintasan, hubungan gerak, durasi dan elemen tetap pada catatan aktif. Jika gambar bertentangan dengan keputusan, kembali ke [alur visual](image-workflow.md); jangan menutupi perbedaan geometri dengan prompt transformasi.

Gunakan [template prompt](../assets/prompt-template.md) untuk menguraikan subjek, material/cahaya yang tampak, lingkungan, framing awal, perjalanan kamera, reveal, framing akhir dan hal yang harus bertahan. Pilihan baru tetap dibedakan dari klaim sumber. Instruksi gerak harus menyatakan simultan atau berurutan sesuai camera.motion_relationship; daftar nama gerak saja belum cukup.

Tulis satu prompt untuk satu continuous shot tanpa cut. Penugasan gambar awal–akhir terjadi lewat kontrol gambar generator; menyebut nama file dalam teks tidak menggantikan pemasangan kedua file. Cocokkan file dalam teks dengan peta aset dan jangan membuat prompt mengarah ke shot/versi lain.

Salin dua instruksi wajib dari prompt_constraints pada aturan produksi ke setiap prompt: continuous shot dan ambient halus tanpa musik, narasi, dialog atau efek dramatis. Sesuaikan ambient dengan lingkungan secara halus. Musik referensi tidak dibawa ke produksi. Jangan menyisipkan instruksi musik atau cut yang bertentangan di bagian lain prompt.

Isi shots[].prompt dengan revision aktif, duration_s shot, start_asset_id, end_asset_id dan text lengkap tanpa penanda template. Pertahankan visual_final bila prompt masih dikerjakan. Naikkan stage: prompt_package ketika seluruh prompt lengkap dan cocok dengan pasangan final, lalu jalankan validator. Validasi memeriksa pengikatan serta instruksi wajib; ia tidak menilai makna seluruh prompt atau mendengar audio.

## Mengekspor paket yang dapat dilanjutkan

Gunakan [build_production_package.py](../scripts/build_production_package.py) untuk mengemas keputusan dan aset yang sudah selesai, bukan membuat keputusan/prompt baru:

~~~sh
python skills/produce-home-tour/scripts/build_production_package.py /path/to/project/project.json --output /path/to/delivery/project-r1
~~~

Script menerima prompt_package yang valid dan file asli yang tersedia. Ia mempertahankan keputusan, ID/revisi, teks prompt dan piksel aset; tidak memberi review atau persetujuan. Folder tujuan harus baru. Keluaran:

| Isi | Fungsi |
| --- | --- |
| project.json | Catatan aktif: brief, konsep, desain, sumber, shot, keputusan, aset dan prompt |
| production-guide.md | Ringkasan rumah, shot/total, peta frame–prompt, gerak/framing, urutan perangkaian, sumber dan catatan versi |
| prompts/shot-NN.txt | Teks prompt persis dari shot yang sama |
| File aset pada path proyek | Dua PNG final per shot dan kolase bila dicatat sebagai aset; tidak mengandalkan tautan unduhan sesi lama |

Nama project.json, production-guide.md dan folder prompts/ disediakan untuk keluaran paket; aset disimpan di folder gambar seperti frames/. Paket mempertahankan path relatif aset dan memvalidasi ulang salinan. Tidak menyalin pustaka HOMEKU, file lain dari folder proyek atau riwayat percobaan yang tidak tercatat sebagai aset aktif.

Serahkan panduan, catatan proyek, prompt dan tautan individu kedua frame setiap shot melalui mekanisme file host. ZIP proyek opsional boleh ditambahkan setelah isinya diperiksa; dua frame tetap punya tautan individu. Ini paket proyek produksi, bukan ZIP plugin tahap pemasangan. Jika file/pemrosesan tidak tersedia, nyatakan bagian yang belum dibuat; jangan mengklaim paket mandiri hanya dari teks dan nama file.

Peta untuk pengguna memisahkan durasi, file awal, file akhir dan prompt. Pengguna memasang dua gambar sesuai peran, menyalin prompt yang sama, lalu menghasilkan satu klip dengan durasi tabel. Sesudah klip ditinjau, rangkai mengikuti urutan shot; cut antarklip berada di luar continuous shot. Tidak menambah pengungkapan area yang sudah tercakup atau musik pada perangkaian.

## Revisi hasil dan sesi berikutnya

Saat pengguna membawa hasil, periksa hanya media yang benar-benar dapat dibuka. Untuk gambar/video yang terlihat, bedakan temuan desain, geometri, kontinuitas, lintasan, framing dan ritme. Dengarkan audio bila dapat diakses; bila belum, catat pemeriksaan audio belum dilakukan. Jangan mengklaim video/audio sudah ditinjau dari thumbnail, metadata atau nama file.

Arahkan revisi pada penyebabnya. Gerak/timing yang salah ditangani pada rancangan/prompt; perubahan bentuk, bukaan atau material dapat memerlukan perbaikan gambar. Perubahan elemen tetap menuntut peninjauan shot lain yang terdampak. Jangan mengubah durasi baku, menambah area/bedroom atau membubuhkan musik untuk memperbaiki hasil.

Ketika keputusan yang disetujui berubah, naikkan revision dan catat alasan serta dampaknya pada revision_notes. Tinjau ulang persetujuan/aset/prompt sesuai kontrak. Pertahankan file lama di luar catatan aktif; jangan mengganti nomor revisinya untuk menyamarkan data usang. Aset yang tetap dipakai dicatat pada revisi baru hanya setelah ditinjau ulang terhadap keputusan baru, dengan review_note yang menjelaskan dasar penggunaannya. Perbarui prompt dari pasangan yang dipilih, kemudian ekspor ke folder revisi baru.

Untuk melanjutkan sesi, baca project.json dan production-guide.md serta pastikan file gambar asli dapat diakses. Gunakan keputusan/persetujuan yang masih berlaku; minta hanya aset atau konteks yang hilang. Catat temuan hasil dan keputusan revisi dalam revision_notes tanpa menambah field bebas. Berkas proyek tidak otomatis menjadi pengetahuan sumber.

Penyerahan paket tidak berarti video sudah dibuat, dirangkai atau dipublikasikan. Generate Omni Flash dan publikasi Facebook tetap dijalankan pengguna. Uji perilaku plugin terpasang, kualitas video/audio serta evaluasi seluruh alur dilaksanakan sesuai tahap penerimaan.
