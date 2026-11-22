# HOMEKU library

- Mulai dari README.md dan kontrak yang relevan dalam docs/contracts/.
- Referensi aktif hanya ID dalam data/registry.json. archive/oldrepo/ tidak menjadi input discovery, generator atau knowledge; baca arsip hanya bila tugas memang memerlukannya.
- V2 (2.0): audit.json adalah satu sumber isi audit; analysis.md laporan manusia hasil renderer. Legacy 1.0/1.1 tetap berbasis analysis.md menurut versinya. manifest.json metadata teknis/provenance. Jangan membuat analysis.json yang diedit terpisah atau mengonversi paket diterima diam-diam.
- Perubahan referensi masuk melalui ZIP final dan revisi eksplisit. Pengguna memeriksa isi di chat sebelum download; tidak ada review isi baru setelah ingest.
- catalogs/, knowledge/, data/projections/, search-index, dependencies dan build adalah keluaran generator. Ubah sumber/tooling, lalu jalankan build; jangan merawat salinan fakta manual.
- Media V2: satu kolase media/shot-NN.jpg per take kontinu; normal 3 panel, multi area dinamis. Overview adalah pilihan frame asli (biasanya awal IN/akhir OUT), bukan JPEG tersendiri; storyboard seluruh overview satu baris. Media legacy tetap menurut kontraknya. Tidak ada motion/ atau seluruh frame tersimpan.
- Nama gaya utama, pengaruh gaya dan gaya interior memakai istilah bahasa Inggris; penjelasan tetap bahasa Indonesia. Renderer 2.1.x memerlukan identity.style_names_language=en. Jangan menerjemahkan atau mengganti nama gaya sumber yang telah diterima secara otomatis.
- Renderer/template/font versi yang sudah diterima tidak ditimpa. Review mengikat seluruh snapshot kandidat; export membungkus byte yang sama. Receipt tetap di luar ZIP.
- Dokumen bekerja/ berada di jalur produksi terpisah. omniflash-v2.md hanya acuan notasi kamera; jangan mengganti arah, tempo atau kronologi sumber dengan default produksi.
- Pertahankan uncertainty, negasi, label baru serta pointer sumber. Generator tidak menjalankan sintesis AI atau menebak fakta dari narasi.
- Fixture hanya untuk tes terisolasi, bukan referensi aktif. Jangan membuat klaim audit/review video yang belum dijalankan.
- Verifikasi tooling dengan python -m unittest discover -s tests -t . -v, python tools/library.py check, dan python tools/build_audit_kit.py --check. FFmpeg dan requirements.txt diperlukan. Tahap 1 bukan audit ulang edh001 atau penyelesaian workflow/pilot Tahap 2.
