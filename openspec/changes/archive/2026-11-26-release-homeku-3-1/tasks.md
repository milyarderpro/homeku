# Tasks

## 1. Kontrak dan aset 3.1

- [x] 1.1 Naikkan `FORMAT_VERSION`, skema `audit`, `manifest`, `reference-reader`, dan `search-index`, kontrak serta contoh dalam `audit/`. Wajibkan `house_type` dan `palette` pada profil. Verifikasi fixture 3.1 lulus, profil yang kehilangan data wajib gagal, dan masukan 3.0 mendapat petunjuk audit ulang.
- [x] 1.2 Konsolidasikan layout di `tools/assets/layouts/media.json` dan template di `tools/assets/templates/analysis.md`. Hapus cabang lama dari `render_assets.py`, `media.py`, dan `reporting.py`. Perbarui fixture laporan dan uji tampilan profil, shot satu area dan multi-area, Overview, Storyboard, dan Production Start.
- [x] 1.3 Selaraskan model, pembaca, paket, dan fingerprint generator dalam `tools/homeku/` serta fixture pustaka. Perbarui dokumen repo yang menyatakan versi aktif dan inventaris aset. Verifikasi build dan discovery dengan registry 3.1 terisolasi dan uji penolakan artefak lama.

## 2. Pemeriksaan kamera pada workspace audit

- [x] 2.1 Ekstrak pemeriksaan kamera dan timeline yang dapat dipakai sebelum desain dari `audit_quality.py`, `models.py`, dan `preflight.py`. Verifikasi pemeriksaan menerima data kamera yang lengkap ketika kolom desain masih kosong serta menolak rujukan frame, fase, atau Production Start yang tidak sah.
- [x] 2.2 Tambahkan `check-camera` di `tools/audit.py` dan penyimpanan status per shot di `audit_session.py` serta `authoring.py`. Verifikasi status terikat ke sumber, versi dan batas shot, dua kali pemeriksaan terhadap input yang sama memberi hasil yang sama, dan sesi dengan versi lama atau sumber berbeda ditolak.
- [x] 2.3 Gunakan status pemeriksaan pada `complete`, `check-input`, dan `draft`. Uji bahwa perubahan notasi, observasi, fase, tempo, atau Production Start menunjukkan shot dan bagian terdampak, sedangkan penyuntingan desain dan kurasi media yang valid bisa diteruskan.
- [x] 2.4 Hubungkan alur koreksi shot dengan `check-camera --shot-id`. Uji bahwa koreksi satu shot dapat lolos setelah diperiksa kembali, perubahan di shot lain tetap terdeteksi, dan perubahan source atau cut perlu pemetaan ulang.

## 3. Panduan dan kit satu chat

- [x] 3.1 Tata `audit/authoring.md`, `audit/visual-audit.md`, `audit/camera-cases.md`, `audit/json-guide.md`, dan panduan baru `audit/design-audit.md` sesuai empat fase. Selaraskan README dan prompt `01-audit.md`, `02-correct.md`, dan `03-export.md`. Uji urutan perintah yang ditulis, termasuk penajaman visual menggunakan frame tambahan hanya pada bagian yang perlu diperiksa.
- [x] 3.2 Perbarui `tools/build_audit_kit.py` dan hasilkan kit 3.1 untuk pengujian. Verifikasi inventaris dan eksekusi dari folder ekstraksi yang hanya berisi kit dan MP4. Uji paket final tanpa MP4, status sesi, atau artefak kerja.

## 4. Persiapan penggantian pustaka

- [x] 4.1 Siapkan prosedur cutover sekali pakai dalam workspace penerbitan. Gunakan validator, transaksi penyimpanan dan generator pustaka untuk mengikat pengganti ke predecessor serta MP4 kanonis, lalu bangun ulang ledger dan keluaran. Verifikasi penolakan paket hilang, versi lama, hash sumber berbeda, dan predecessor stale tanpa mengubah pustaka aktif.
- [x] 4.2 Simulasikan cutover dari registry pendahulu ke snapshot pengganti 3.1 memakai fixture. Verifikasi jalur ingest normal untuk ZIP baru, perilaku saat staging gagal, rollback snapshot, dan dry run dari `tools/publish_actions.py` serta workflow CI/Actions. Pastikan incoming dan discovery menggunakan snapshot 3.1 dan pertahankan jalur aktif pada satu kontrak sesudah transisi.

## 5. Verifikasi integrasi dan perbaikan pilot

- [x] 5.1 Jalankan alur lengkap dari empat fase sampai ingest terhadap pustaka terisolasi. Cocokkan kamera dari pemeriksaan fase 2 dengan `audit.json` dan `analysis.md` dalam ZIP. Verifikasi receipt terhadap snapshot, hasil media, serta perubahan katalog, reader dan Knowledge.
- [x] 5.2 Jalankan `python -m unittest discover -s tests -t . -v`, `python tools/library.py check`, dan `python tools/build_audit_kit.py --check` terhadap snapshot staging lengkap. Periksa inventaris kit untuk satu pasangan template dan layout, panduan per fase, serta satu kontrak aktif.

- [x] 5.3 Selaraskan `audit/json-guide.md`, panduan media terkait, dan validasi agar `complete` mempertahankan pilihan panel jernih di `panels[].frame_index` serta memakai Production Start sebagai panel Start pada shot biasa. Uji awal dan akhir blur, midpoint yang dilewati, urutan panel, frame di luar shot atau belum viewed, dan Production Start terhadap batas native.
- [x] 5.4 Perbarui `audit/visual-audit.md` dan `audit/camera-cases.md` dengan contoh awal, overlap, dan akhir komponen. Uji secara visual pada frame awal `dreamshome01` Shot 01 dan hubungan notasi tiap fase dengan frame pembanding.
- [x] 5.5 Inventarisasi kosakata area dan fungsi dari seluruh pilot yang tersedia. Selaraskan normalisasi indeks dan kueri di `generation.py`, `reader.py`, dan `data/taxonomy.json`. Uji alias setara, variasi istilah baru, pencarian gabungan area dan rute, serta preservasi label asli. Pastikan Shot 03 dari JSON Gemini dan GPT ditemukan lewat `dining`.
- [x] 5.6 Bangun ulang kit serta keluaran generator di staging terisolasi setelah perbaikan. Jalankan suite unittest, `python tools/library.py check` pada snapshot staging, dan `python tools/build_audit_kit.py --check`. Verifikasi kolase dan Storyboard mengacu pada pilihan panel yang sama seperti manifest.

## 6. Gerbang rilis dan penggantian referensi aktif

- [x] 6.1 Verifikasi ulang kedua ZIP `dreamshome01` dari ChatGPT dan Gemini terhadap MP4 kanonis. Cocokkan pemeriksaan kamera lokal, JSON, laporan, kolase, Storyboard, dan batas native. Ekspor ulang dengan panel jernih dan midpoint shot sumber. Pilih Gemini sebagai dasar kandidat yang menangkap dua fase Shot 03. Kedua keluaran menemukan Shot 03 melalui filter `kitchen` dan `dining`.
- [x] 6.2 Audit ulang `video/edh001.mp4`, ekspor dan validasi `edh001-r0003.zip` berformat 3.1, serta siapkan laporan dan media untuk tinjauan pengguna. Kandidat mengikat revisi 2 dan `content_sha256` predecessor.
- [x] 6.3 Setelah pengguna memilih ZIP pengganti, verifikasi paket terhadap MP4 dan predecessor di registry aktif. Jalankan cutover dengan prosedur yang sudah diuji. Periksa kembali registry, incoming, referensi, dan semua keluaran pustaka. Penerbitan ke GitHub mengikuti otorisasi pengguna.
