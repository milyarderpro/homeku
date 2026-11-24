# HOMEKU library

- Mulai dari README.md dan kontrak yang relevan dalam docs/contracts/.
- Referensi aktif hanya ID dalam data/registry.json. archive/oldrepo/ tidak menjadi input discovery, generator atau knowledge; baca arsip hanya bila tugas memang memerlukannya.
- V2 (2.0/2.1/2.2/2.3/2.4): audit.json adalah satu sumber isi audit; analysis.md laporan manusia hasil renderer. Legacy 1.0/1.1 tetap berbasis analysis.md menurut versinya. manifest.json metadata teknis/provenance. Jangan membuat analysis.json yang diedit terpisah atau mengonversi paket diterima diam-diam.
- Perubahan referensi masuk melalui ZIP final dan revisi eksplisit. Pengguna memeriksa isi di chat sebelum download; tidak ada review isi baru setelah ingest.
- catalogs/, knowledge/, data/projections/, search-index, dependencies dan build adalah keluaran generator. Ubah sumber/tooling, lalu jalankan build; jangan merawat salinan fakta manual.
- Media sumber 2.1/report 2.2.0: satu kolase media/shot-NN.jpg per take kontinu, media/overview.jpg seluruh pilihan wide satu baris, media/storyboard.jpg seluruh kolase vertikal. Normal 3 panel; multi area dinamis. Sumber 2.0 mempertahankan storyboard overview satu baris tanpa overview.jpg. Legacy tetap menurut kontraknya; tidak ada motion/ atau seluruh frame tersimpan.
- Nama gaya utama, pengaruh gaya dan gaya interior memakai istilah bahasa Inggris; penjelasan tetap bahasa Indonesia. Renderer 2.1.x/2.2.0 memerlukan identity.style_names_language=en. Jangan menerjemahkan atau mengganti nama gaya sumber yang telah diterima secara otomatis.
- Sumber 2.1 wajib composition_summary satu paragraf per Overview dan depth_direction per fase (IN/OUT/NO IN/OUT/null ambigu). Camera Pattern turunan, bukan fakta manual kedua. Camera Start tetap awal sumber, berbeda dari Overview akhir OUT. Notasi satu paragraf tanpa Enter setelah → atau +.
- Renderer/template/font versi yang sudah diterima tidak ditimpa. Review mengikat seluruh snapshot kandidat; export membungkus byte yang sama. Receipt tetap di luar ZIP.
- Dokumen bekerja/ berada di jalur produksi terpisah. omniflash-v2.md hanya acuan notasi kamera; jangan mengganti arah, tempo atau kronologi sumber dengan default produksi.
- Pertahankan uncertainty, negasi, label baru serta pointer sumber. Generator tidak menjalankan sintesis AI atau menebak fakta dari narasi.
- Fixture hanya untuk tes terisolasi, bukan referensi aktif. Jangan membuat klaim audit/review video yang belum dijalankan.
- Verifikasi tooling dengan python -m unittest discover -s tests -t . -v, python tools/library.py check, dan python tools/build_audit_kit.py --check. FFmpeg dan requirements.txt diperlukan. Status tooling, kandidat, persetujuan, ekspor/ingest dan pilot harus dibedakan. Mengimplementasikan workflow tidak berarti persetujuan kandidat baru. Lihat docs/implementation-plan-overview-storyboard.md dan docs/overview-storyboard-verification.md.

- Workflow2.3 (kompatibilitas): report2.2.2/media2.2.0/reader2.3/generator6. ZIP final tanpa video; MP4 input terpisah/sumber kanonis lokal. Baseline6FPS/native; sumber≤6FPS dan shot<1detik seluruh native; pendalaman10FPS/native sesuai pertanyaan visual. Sumber2.2 tetap10FPS/report2.2.1.
- Baca audit/visual-audit.md sebelum serialisasi JSON; depth→translation→rotation sebelum simpulan, termasuk Pan/Static. camera_checks, motion_observations/scale_measurement, fact_coverage dan enam bagian MD wajib tervalidasi. ~× rasio skala IN=akhir/awal, OUT=awal/akhir, bukan tempo; semua moderate sah.
- facts[].facet_roles eksplisit pada2.3/2.4; format lama memakai sources/fact-facets.json. Label asli dan provenance dipertahankan; mapping terkurasi bukan inferensi prosa. Lihat docs/audit-method-verification.md dan kontrakpackage2.3.

- Default baru2.4: report2.2.3/media2.2.0/reader2.4/generator7; format lama tetap aturan asal, khusus2.3 pengukuran~× tetap wajib. Estimasi2.4 visual ~×/~° memakai asumsi wajar; piksel opsional dan bukan syarat kalibrasi. Bagian jelas tetap memiliki angka, kendala khusus dipertahankan pada bagian ambigu.
- Authoring2.4 melalui audit/authoring.md: prepare/complete mengisi hanya turunan mekanis, mark-viewed deklarasi eksplisit AI setelah melihat, check-input sebelum render. audit.json tetap satu sumber final. Kerangka/contoh bukan audit valid atau referensi aktif.
- Cache/session/performance hanya workspace, tidak masuk snapshot/ZIP/proyeksi/knowledge. Jangan menimpa media/renderer/template/font terdaftar. Executor subset baru wajib byte-identik; cache tidak melewati validasi/snapshot review. Ekspor tidak merender ulang.
