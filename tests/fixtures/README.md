# Fixture sintetis

- [fixture-valid-r0001.zip](fixture-valid-r0001.zip): dua shot, sumber MP4, sembilan JPEG, MD lengkap dan manifest yang cocok.
- [fixture-invalid-r0001.zip](fixture-invalid-r0001.zip): format serupa dengan satu hash media sengaja salah.

Semua isi sintetis untuk menguji format dan alur; bukan audit referensi dan bukan knowledge desain. purpose=fixture ditolak importer produksi. Pengujian memakai direktori sementara terisolasi; tidak pernah menaruh ZIP ini dalam incoming/ repo aktif.

Regenerasi: `python tools/make_test_packages.py`. Factory membuat media nyata dari pola uji FFmpeg, timestamp dan hash aktual. Narasi serta label kamera merupakan simulasi yang dinyatakan eksplisit, bukan hasil pengamatan rumah.

Pemeriksaan tanpa publikasi: `python tools/library.py validate tests/fixtures/fixture-valid-r0001.zip`. Fixture invalid harus gagal dengan error hash media. Tes integrasi membangun fixture tambahan saat runtime, termasuk 300 referensi dan remote Git lokal sementara.
