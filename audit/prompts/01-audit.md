# Mulai audit HOMEKU 3.1

Audit MP4 terlampir untuk pustaka HOMEKU. Ekstrak kit, jalankan `python homeku_runtime.py --output .`, lalu baca `audit/authoring.md`. Jalankan empat fase di bawah secara berurutan dalam chat ini.

1. **Pemetaan shot.** Konfirmasi cut dan siapkan sesi dengan `prepare`. Satu take kontinu bisa memuat beberapa area.
2. **Audit kamera.** Baca `audit/visual-audit.md` dan `audit/camera-cases.md`. Periksa baseline, dalami bagian yang perlu, lalu simpan fase, notasi, bukti, tempo dan Production Start jika dipilih. Deklarasikan viewed setelah melihat frame. Jalankan `check-camera` dan ringkas hasil per shot sebelum beralih ke desain.
3. **Audit desain dan kurasi media.** Baca `audit/design-audit.md` dan `audit/json-guide.md`. Lengkapi profil, desain per area, komposisi, panel dan Overview di JSON yang sama. Jika kamera dikoreksi, periksa ulang shot terkait.
4. **Validasi dan ekspor.** Ikuti `complete → check-input → draft → review → export` dari panduan authoring. Setelah kandidat lulus, langsung berikan laporan, media dan satu ZIP final tanpa MP4 dalam balasan yang sama.
