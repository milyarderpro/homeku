# HOMEKU library

- Mulai dari README.md dan kontrak yang relevan dalam docs/contracts/.
- Referensi aktif hanya ID dalam data/registry.json. archive/oldrepo/ tidak menjadi input discovery, generator atau knowledge; baca arsip hanya bila tugas memang memerlukannya.
- analysis.md adalah sumber isi audit; manifest.json menyimpan metadata teknis/provenance. Jangan membuat analysis.json yang diedit terpisah.
- Perubahan referensi masuk melalui ZIP final dan revisi eksplisit. Pengguna memeriksa isi di chat sebelum download; tidak ada review isi baru setelah ingest.
- catalogs/, knowledge/, data/projections/, search-index, dependencies dan build adalah keluaran generator. Ubah sumber/tooling, lalu jalankan build; jangan merawat salinan fakta manual.
- Setiap shot memakai satu frame asli area-overview.jpg, biasanya awal untuk IN dan akhir untuk OUT. Storyboard menggabungkan gambaran area seluruh shot. Tidak ada motion/ atau seluruh frame tersimpan.
- Dokumen bekerja/ berada di jalur produksi terpisah. omniflash-v2.md hanya acuan notasi kamera; jangan mengganti arah, tempo atau kronologi sumber dengan default produksi.
- Pertahankan uncertainty, negasi, label baru serta pointer sumber. Generator tidak menjalankan sintesis AI atau menebak fakta dari narasi.
- Fixture hanya untuk tes terisolasi, bukan referensi aktif. Jangan membuat klaim audit/review video yang belum dijalankan.
- Verifikasi perubahan tooling dengan python -m unittest discover -s tests -t . -v dan python tools/library.py check. FFmpeg dan dependensi requirements.txt diperlukan.
