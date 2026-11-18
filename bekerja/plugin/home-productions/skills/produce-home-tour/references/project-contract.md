# Kontrak proyek home-productions

Kontrak versi 1.0; aturan produksi 1.0.0. Gunakan [template proyek](../assets/project-template.json) sebagai titik awal. [Schema](../assets/project.schema.json) memeriksa struktur; [aturan produksi](production-rules.yaml) memeriksa kebijakan yang disepakati. Berkas proyek dan gambar pengguna disimpan di folder proyek, terpisah dari paket plugin dan pustaka HOMEKU.

## Tahap data

| stage | Data yang diperiksa |
| --- | --- |
| brief | Struktur awal; gambar, daftar shot dan persetujuan belum diperlukan |
| concept | Brief, konsep pilihan, jalur/versi sumber dan minimal satu bukti yang dibaca |
| shot_plan | Desain, daftar shot, cakupan, sumber struktur shot dan total durasi |
| visual_draft | Rancangan di atas sudah disetujui pengguna atau didelegasikan; gambar boleh masih dikerjakan |
| visual_final | Persetujuan visual, dua frame per shot, review tercatat dan file PNG aktual yang cocok |
| prompt_package | Seluruh kebutuhan visual final ditambah prompt yang cocok dengan frame, durasi dan revisi |

Validator bersifat baca-saja. Ia tidak memanggil web, membuat gambar, mengubah keputusan atau menyatakan review visual/audio sudah dilakukan.

## Referensi dan cakupan

knowledge mencatat repository URL, ref/commit, jalur akses dan evidence. Setiap bukti yang dibaca menyimpan ID referensi, ID shot/segmen, pointer field, kutipan singkat, cakupan fungsi dan dasar kontinuitas.

Bukti yang gagal dibaca dicatat dengan access_status: failed, error yang sebenarnya, dan tanpa mengisi klaim sumber. Bukti itu tidak dapat mendukung shot.

Setiap shot harus merujuk minimal satu bukti yang dibaca dengan cakupan fungsi yang sama dan kontinuitas yang tercatat. URL anotasi harus sesuai repository, ID referensi dan commit atau ref proyek. Keberadaan catatan ini tidak membuktikan kutipannya benar; skill tahap 3 tetap harus mengambil dan memeriksa sumber aktual.

Nama area pada catatan proyek memakai bentuk kanonis dari production-rules.yaml. Jenis shot dan kombinasi cakupannya dibatasi pola referensi yang disepakati. Tidak ada jenis shot atau nama kamar bebas untuk melewati aturan pengulangan.

Contoh living–kitchen tersedia pada edh022; sleeping loft terlihat bersama fungsi lain pada edh033/edh060. Dining dicakup bersama kitchen atau dalam ruang gabungan yang tercatat, tanpa menambahkan shot dining tersendiri. Referensi detail dipilih melalui URL pustaka saat produksi, tanpa mengemas salinan analisisnya.

Bedroom dan sleeping_loft merupakan satu kelompok area tidur dengan batas satu pengungkapan. Jika loft sudah dicakup, tidak ditambahkan bedroom terpisah. Ini mempertahankan pola referensi yang ada.

## Revisi, persetujuan dan aset

revision adalah bilangan positif. Aset aktif, prompt dan persetujuan yang dicatat harus merujuk revisi proyek yang sama. Setelah keputusan berubah, catat revisi dan tinjau ulang aset/prompt terdampak; data usang tidak boleh dinyatakan final.

Persetujuan mencatat revision, by: user atau delegated, dan note yang merujuk keputusan pengguna. Nilai tersebut merupakan catatan dari workflow, bukan bukti persetujuan yang dapat diciptakan validator.

frames.start dan frames.end menunjuk asset_id pada assets. Setiap aset mencatat shot, peran, revisi, path relatif, SHA-256, dimensi serta asal/catatan review. File kolase boleh dicatat sebagai aset pendukung; dua frame individu tetap wajib pada tahap final.

Path aset dihitung dari folder project.json. Path absolut, keluar folder, dan symlink yang mengarah keluar ditolak. Pada tahap final, validator membuka file PNG, memeriksa SHA-256 dan dimensi aktual, serta rasio 9:16 setiap frame. Validasi ini tidak mengukur ketepatan tata ruang atau kualitas visual.

## Prompt dan audio

Setiap prompt final terikat pada revisi, durasi dan dua ID frame shot yang sama. Teksnya wajib memuat instruksi continuous shot dan ambient tanpa musik dari production-rules.yaml. Pemeriksaan ini memastikan instruksi tercantum, bukan penilaian semantik seluruh prompt atau deteksi musik pada video.

Aturan yang dibundel merupakan aturan baku saat ini. Perubahan kebijakan memerlukan pembaruan aturan dan rules_version yang jelas; tidak disediakan kolom override bebas untuk menghindari validasi.

## Menjalankan pemeriksaan

Dari root paket home-productions/, jalankan pada lingkungan pemrosesan file yang tersedia:

~~~sh
python skills/produce-home-tour/scripts/validate_project.py /path/to/project.json
~~~

Dependensi dideklarasikan di scripts/requirements.txt. Hasil JSON berisi valid, errors dan batas pemeriksaan. Exit code 0 berarti valid secara struktural sesuai tahap; 1 berarti data melanggar kontrak; 2 berarti file/JSON tidak dapat dibaca.

Skill praproduksi tersedia sampai rancangan shot. Produksi gambar dan paket prompt belum diimplementasikan; paket belum dipasang. Lihat [SKILL.md](../SKILL.md) untuk alur dan batas kemampuan saat ini.
