# Fixture sintetis

- [fixture-valid-r0001.zip](fixture-valid-r0001.zip): dua shot, sumber MP4, sembilan JPEG, MD lengkap dan manifest yang cocok.
- [fixture-invalid-r0001.zip](fixture-invalid-r0001.zip): format serupa dengan satu hash media sengaja salah.

Semua isi sintetis untuk menguji format dan alur; bukan audit referensi dan bukan knowledge desain. purpose=fixture ditolak importer produksi. Pengujian memakai direktori sementara terisolasi; tidak pernah menaruh ZIP ini dalam incoming/ repo aktif.

Regenerasi: `python tools/make_test_packages.py`. Factory membuat media nyata dari pola uji FFmpeg, timestamp dan hash aktual. Narasi serta label kamera merupakan simulasi yang dinyatakan eksplisit, bukan hasil pengamatan rumah.

Pemeriksaan tanpa publikasi: `python tools/library.py validate tests/fixtures/fixture-valid-r0001.zip`. Fixture invalid harus gagal dengan error hash media. Tes integrasi membangun fixture tambahan saat runtime, termasuk 300 referensi dan remote Git lokal sementara.

## Fixture V2

make_v2_inputs menghasilkan MP4 test-pattern nyata dan audit JSON sintetis di root sementara. Normal: satu area bathroom dengan fungsi laundry, tiga panel. Multi: living/kitchen dengan visibilitas bertumpang tindih, rute terpisah dari visibilitas, satu fase lintas area dan tempo moderate → fast. Tes memperluas kasus reentry, kamera tidak berpindah antararea, fase/ruang berulang, input tidak valid, revisi serta kapasitas 300 model. Log viewed pada fixture adalah deklarasi sintetis untuk validator; bukan bukti audit video rumah nyata. Tidak boleh masuk registry produksi.

Sumber fixture baru memakai `make_v2_inputs(..., version="2.1")`; default 2.0 dipertahankan untuk regresi renderer lama. Arah dan paragraf Overview sintetis bukan hasil audit video rumah. Tes 2.1 menjalankan media N+2, lokasi berulang, block crop tanpa MP4 dan pipeline draft/review/export/ingest pada root bertanda fixture.


Fixture kualitas2.2 memakai version=2.2 dengan motion_observations dan fact_coverage sintetis. Snapshot MD lengkap normal/multi berada di reports/*-2.2.1.md. ZIP2.2 tanpa video; MP4 test-pattern ditempatkan terpisah di root fixture. Ini pengujian tooling, bukan audit/penerimaan pilot nyata.

Fixture metode2.3 memakai version="2.3", camera_checks tiga sumbu, scale_measurement dan facet_roles sintetis. Golden normal/multi reports/method-*-2.2.2.md dibuat renderer. Native log test-pattern10FPS untuk semua bukti; tes sampling6FPS/VFR/low-FPS/shot pendek terpisah. 300model diuji pada root terisolasi, tanpa mengubah registry produksi.

Fixture efisiensi2.4 memakai estimasi visual tanpa pengukuran piksel, camera_checks/coverage/facets lengkap dan phase notation bertanda kurung. Contoh normal/multi lengkap di audit/examples/ dibuat dari factory yang sama; golden reports/efficiency-*-2.2.3.md. Prepare/log viewed adalah deklarasi sintetis pada test-pattern, bukan audit rumah. Cache/helper/benchmark hanya direktori sementara dan purpose=fixture; tidak ada ingest produksi.
