# Mengambil pengetahuan HOMEKU

Sumber: https://github.com/milyarderpro/homeku. Ikuti URL sumber; tidak membaca direktori lokal repository sebagai prasyarat saat skill dipakai. Contoh path di bawah adalah path di GitHub.

## Bacaan selektif

| Kebutuhan | Path sumber |
| --- | --- |
| Prinsip dasar | knowledge/ai-knowledge.md |
| Menentukan tema | knowledge/README.md |
| Menemukan gaya, ruang dan gerak | knowledge/directories/README.md |
| Ringkasan sumber | knowledge/reference-profiles/REFERENCE_ID.md |
| Bukti shot dan struktur anotasi | references/REFERENCE_ID/analysis.yaml |
| Narasi dan gambar | references/REFERENCE_ID/analysis.md, shot-NN.jpg atau storyboard.jpg |
| Cakupan review dan batas interpretasi | knowledge/methodology.md dan knowledge/design-evidence/REFERENCE_ID.md |

Baca inti, tema yang dibutuhkan, lalu profil/shot kandidat. Tidak perlu membaca semua referensi, JSON atau frame. Tidak membekukan jumlah referensi dan daftar ID di dalam skill; pustaka dapat terus bertambah.

Pilih satu acuan utama untuk pola pengungkapan dan referensi pendukung bila dibutuhkan. Cocokkan pilihan dengan brief dan aturan produksi. Dukungan sumber diperlukan untuk jenis area, cakupan gabungan, urutan dan keluarga gerak; jangan membuat variasi generik hanya karena rumah secara umum dapat memilikinya.

## Web atau konektor

Gunakan jalur yang tersedia. Konektor GitHub adalah alternatif, bukan syarat wajib jika web sudah dapat membaca berkas.

Pilih ref atau commit yang sama untuk sumber proyek. Bila commit dapat diketahui, gunakan commit untuk URL dan knowledge.commit; bila hanya branch yang tersedia, catat branch di knowledge.ref dan biarkan commit null. Jangan mengarang SHA atau menganggap branch merupakan snapshot byte yang tidak berubah.

Bentuk URL kanonis:

- Halaman: https://github.com/milyarderpro/homeku/blob/REF/PATH
- Raw: https://raw.githubusercontent.com/milyarderpro/homeku/REF/PATH

Ganti REF dan PATH dengan versi/path yang benar. Pada konektor, gunakan alat read/fetch yang benar-benar tersedia dengan owner/repo/path/ref yang sesuai. Jangan mengasumsikan nama alat atau endpoint yang tidak disediakan lingkungan.

Jika raw gagal, coba halaman GitHub untuk file yang sama. Jika satu jalur gagal, alternatif boleh dipakai dan jalur yang benar-benar digunakan dicatat. Jangan mengisi hasil gagal dari pengetahuan lokal lalu mengklaimnya sebagai pembacaan remote.

knowledge.route menyatakan jalur pembacaan bukti aktif pada catatan proyek. Jika perlu berganti jalur, baca ulang bukti aktif melalui jalur baru atau lanjutkan tahap yang masih bisa dikerjakan tanpa mencampur riwayat akses yang tidak terwakili kontrak.

## Catatan evidence

Gunakan bentuk pada kontrak proyek:

- evidence_id unik; reference_id sesuai sumber.
- shot_ids merujuk shot/segmen yang dipakai.
- analysis_url menunjuk anotasi pada ref/commit yang dicatat.
- field_paths memakai pointer seperti /shots/1/scene untuk elemen kedua array shots.
- excerpt berisi kutipan pendek dari field yang benar-benar dikembalikan, cukup untuk mendukung cakupan/gerak yang dipakai.
- covered_areas memakai nama kanonis aturan, bukan nama kamar bebas.
- access_status adalah read hanya bila isi terkait benar-benar diperoleh. Untuk failed, isi error aktual; shot_ids, field_paths dan covered_areas kosong, excerpt kosong dan continuity unknown.

Teks parsial hanya mendukung bagian yang dikembalikan. Cari bagian relevan yang belum terbaca bila dibutuhkan; jangan memberi klaim seluruh file sudah diperiksa. Screenshot atau gambar hanya boleh disebut telah dilihat jika pikselnya benar-benar tersedia dan diperiksa.

## Kontinuitas dan penggabungan

Baca scene, framing, camera, observation_note dan transition_out bersama-sama. Shot berlabel living dan kitchen dapat merupakan satu ruang terbuka, satu gerak pengungkapan, atau dua bagian yang dipisahkan cut; jangan menyamakan kasus tersebut.

- annotated_continuous: anotasi yang dibaca menyajikan rentang sebagai satu pergerakan/shot kontinu. Simpan pointer dan kutipan pendukung. Ini penafsiran dari anotasi, bukan klaim memutar ulang seluruh video.
- reviewed_continuous: interval benar-benar ditinjau kontinu sehingga tidak adanya cut dapat diperiksa. Tiga gambar sampel atau sebuah keyframe tidak cukup untuk status ini.
- unknown: bukti kontinuitas belum memadai.
- cut_separated: bagian yang hendak digabung pada sumber dipisahkan cut.

Jangan mengubah unknown menjadi kontinu hanya untuk meluluskan validator. Pilih pola sumber lain yang mendukung, atau pertahankan bagian rancangan tersebut sebagai belum selesai.

Pada edh056, camera.continuity dan transition_out menjelaskan sambungan beberapa segmen tematik. Pergantian ID segmen tidak otomatis berarti cut. Sebaliknya, transisi cut setelah satu shot tidak berarti ada cut di dalam shot tersebut. Periksa batas interval yang dipakai; jangan memaksakan kelompok sumber yang tidak cocok menjadi jenis shot baru di luar aturan.

Bukti struktur shot harus mencakup fungsi yang sama dengan shot produksi. Sumber desain atau warna boleh menjadi pendukung tersendiri, tetapi tidak menggantikan bukti struktur pengungkapan. Ketika sumber mencatat gerak gabungan tanpa urutan yang pasti, bedakan label sumber dari alokasi gerak yang dipilih untuk proyek.

Tidak perlu menganalisis ulang seluruh video. Gunakan analisis tersimpan dan bukti yang sudah ada; periksa media tambahan secara terarah hanya bila memang diperlukan dan tersedia.
