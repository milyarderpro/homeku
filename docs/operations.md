# Operasi pustaka HOMEKU

## Format dan workflow aktif

Audit/paket2.4 memakai audit.json, MD enam bagian/report2.2.3, media2.2.0. Reader/index2.4 dan generator7 mendukung sumber1.0/1.1/2.0/2.1/2.2/2.3/2.4. [Paket2.4](contracts/package-v2-4.md), [laporan](contracts/analysis-v2-2-3.md), [reader](contracts/ai-reader-v2-4.md), [field map](v2-field-map.md).

Paket 2.0 tetap renderer asalnya, termasuk2.1.2 dan storyboard overview satu baris; legacy tetap kontrak MD asal. Tidak ada penerjemahan nama gaya, penambahan fakta atau konversi paket diterima otomatis. Pustaka aktif kosong setelah reset edh001 atas permintaan pengguna. Data audit dan ledger edh001 telah dihapus; MP4 kanonis dipertahankan. Audit baru dapat dimulai dari r0001 dengan supersedes null.

```sh
python tools/audit.py draft-v2 /path/<id>.mp4 /work/audit.json --audit-info /work/audit-info.json --output /work/candidate
python tools/audit.py review /work/candidate/<id> --source /path/<id>.mp4 --output /work/review.md
python tools/audit.py export-v2 /work/candidate/<id> --source /path/<id>.mp4 --output /work/packages --receipt /work/review.md.json
```

Default renderer mengikuti sumber:2.0→2.1.2,2.1→2.2.0,2.2→2.2.1,2.3→2.2.2,2.4→2.2.3. Paket2.2/2.3/2.4 melarang video dan --include-source. MP4 asli tetap terpisah, tersedia di video/<id>.mp4 dan cocok hash sebelum ingest. --quality/--scale/--columns/--overview-scale/--storyboard-scale mengatur media eksplisit; koreksi config/JSON/log diikuti draft/review seluruh kandidat. Receipt di luar kandidat bukan persetujuan otomatis. Setelah pengguna menerima keseluruhan snapshot terbaru, export membungkus byte yang sama tanpa regenerasi JPEG/MD/created_at. Aset versi diterima tidak ditimpa.

Registry tetap version1, V2 menyimpan contract_version/audit_sha256. Source2.1 wajib paragraf Overview dan klasifikasi depth_direction fase. Pola turunan mempertahankan ambigu/urutan, bukan inferensi narasi. Fingerprint mencakup runtime/schema/template/font/layout/prinsip/taksonomi. Turunan dibangun generator; cache bukan sumber fakta.

## Audit di chat dan pembacaan media

Gunakan [panduan audit](../audit/README.md) dan kit input 4 file dengan MP4 terpisah. Bootstrap memulihkan runtime/schema/template/font/lisensi versi terdaftar dari payload lokal. Inspect/sample tidak otomatis berarti frame dilihat; log viewed hanya pemeriksaan nyata. Default2.3:6FPS+awal/akhir native; sumber≤6FPS atau shot<1detik seluruh native. Pendalaman10FPS/native sesuai pertanyaan. Source2.2 tetap10FPS/native. Tampilkan Overview, Storyboard, kolase semua shot dan MD enam bagian sebelum persetujuan keseluruhan. Uji fixture portable bukan run nyata pada akun GPT/Gemini.

Input JSON/log/video dan receipt disimpan di luar folder kandidat. Kandidat diregenerasi di workspace chat, references/ berubah melalui ingest ZIP final. Setelah ZIP ditempel ke incoming/ lokal, jalankan ingest; tidak ada watcher atau review isi kedua. Untuk penyerahan tertentu gunakan `python tools/library.py ingest incoming/<id>-rNNNN.zip` agar ZIP lain tidak ikut diproses.

AI memakai indeks → identity → shot/area → gambar yang diperlukan. Panel/kolase/blok Storyboard tersimpan dapat diambil ke /tmp tanpa MP4; --native meminta sumber asli. Camera Start awal sumber terpisah dari Overview, biasanya akhir OUT. Adaptasi produksi IN lalu reverse membalik seluruh fase/rotasi/tempo dan tidak mengubah audit. [Panduan konsep/DNA/cloning](alur-konsep-desain-v2.md). Dokumen bekerja/ tetap terpisah.

## Alur dan status

`incoming ZIP → validasi → staging → proyeksi → katalog/knowledge → pemeriksaan → publikasi`.

CLI `python tools/library.py ingest` memindai semua ZIP langsung dalam incoming/. Argumen path ZIP dapat dipakai untuk batch tertentu. Paket gagal dicatat tanpa mengganti referensi aktif; paket valid lain dalam batch tetap diproses. Keluar dengan kode 1 bila ada kegagalan, meskipun paket valid sudah dipublikasikan. Keluaran JSON memuat imported, unchanged atau failed beserta error spesifik.

Registry dalam data/registry.json menyimpan revisi dan fingerprint sumber/isi/paket. data/ingest.json mengikat hasil dengan hash ZIP; tanggal eksekusi tidak dimasukkan agar replay identik tidak mengubah repo. Paket gagal dapat dicoba ulang setelah sumber/tooling diperbaiki. Revisi yang sudah berhasil tetap tercatat meskipun telah diganti oleh revisi berikutnya.

Berkas JSON dalam data/projections/ dihasilkan dari sumber sesuai versinya (audit.json V2 atau MD legacy) dan dapat dibangun ulang. Jangan edit manual. Kontrak pembaca tidak berisi metadata cache. Fingerprint dan hash proyeksi disimpan di data/build.json, mengikat seluruh byte referensi serta versi generator/schema/taksonomi/prinsip terkurasi. Alias hanya berlaku untuk label eksplisit; label baru tetap dicari dari katalog, dan konflik/negasi/unknown tetap tersimpan.

## Rebuild dan pemulihan

- `build`: memakai cache proyeksi yang masih cocok dan membangun keluaran deterministik; hanya keluaran berbeda yang dipublikasikan.
- `build --full`: melewati cache dan memvalidasi ulang seluruh referensi aktif.
- `check`: validasi sumber/media/MD aktif, inventory, dan kesetaraan hasil dengan rebuild penuh; tidak memperbaiki keluaran diam-diam.
- `recover`: memulihkan transaksi lokal yang terputus. Perintah tulis juga menjalankan pemulihan sebelum bekerja.

CLI mengunci satu root dengan flock di .homeku/. Semua kandidat dan halaman turunan disiapkan sebelum publikasi. Journal menyimpan backup dan mengembalikan state sebelumnya bila pemasangan gagal; transaksi yang selesai dibersihkan. Registry dipasang terakhir.

Pada filesystem biasa, beberapa folder tidak dapat diganti dalam satu rename. Pembaca CLI memakai lock; pembaca file eksternal dapat melihat jeda sangat singkat saat penggantian. Setelah crash, jalankan recover sebelum membaca state lokal. Di GitHub, satu commit memublikasikan keseluruhan snapshot sehingga pembaca remote mendapat versi konsisten.

Halaman kategori dibagi maksimal 40 entri per halaman. data/dependencies.json memetakan keluaran ke ID sumber; data/build.json mencatat fingerprint dan hash keluaran. Cache menghindari parsing/decode ulang pada referensi yang tidak berubah; render deterministik tetap menghitung indeks agregat agar hitungan dan penghapusan proyeksi lama konsisten.

## GitHub Actions

- Library checks: pengujian terisolasi dan check atas pustaka aktif, dengan token read-only.
- Library ingest: berjalan pada branch default untuk perubahan ZIP, sumber atau tooling terkait; tersedia Run workflow untuk retry semua paket.
- Publikasi diserialkan. Setiap run membaca snapshot branch terbaru dan seluruh incoming/, sehingga run pending yang digantikan tidak kehilangan paket.
- Jika push lain masuk saat bot menerbitkan hasil, publisher membuat worktree sementara dari branch terbaru, memproses ulang dan mencoba push kembali maksimal lima kali. Tidak memakai force push.
- Action memakai runtime Node 24. Checkout v5 mempertahankan autentikasi pada konfigurasi Git bersama yang digunakan worktree sementara; perubahan versi checkout perlu menguji kembali autentikasi tersebut. Lihat [dokumentasi checkout v5](https://github.com/actions/checkout/tree/v5).
- Bot memakai GITHUB_TOKEN dan commit hasil tidak menyalakan loop push workflow. Laporan teknis diunggah sebagai artifact homeku-ingest-report.
- Workflow memerlukan GitHub Actions aktif dan izin token contents:write untuk job ingest. Branch protection yang melarang push bot harus disesuaikan pemilik repo; tooling tidak mengubah setting akun/repo.

File workflow tersedia setelah implementasi dipush. Pengujian lokal mensimulasikan lock, rollback, skala dan konflik Git; eksekusi hosted serta izin repo harus dibuktikan lewat run GitHub pertama. Tidak ada review isi tambahan setelah ZIP diterima.

Rujukan implementasi: [concurrency GitHub](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency) dan [pemicu GITHUB_TOKEN](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow).

## Retensi dan penyimpanan

- MP4 kanonis disimpan satu kali per sumber di video/. Jika sudah tersedia, jangan sertakan lagi dalam ZIP.
- Media aktif hanya paket revisi terakhir. Revisi mengganti seluruh folder terkait dan membuang halaman/proyeksi usang dari state aktif.
- ZIP penyerahan dan ledger seluruh revisi dipertahankan. Tidak ada pembersihan otomatis atau penghapusan unggahan diam-diam.
- Riwayat Git tetap menyimpan revisi lama; menghapus file dari HEAD tidak mengurangi seluruh riwayat.
- Sebelum ingest massal, ukur ukuran sumber, ZIP dan media. Perubahan retensi/penyimpanan besar memerlukan kebijakan eksplisit, bukan pemangkasan detail audit tanpa persetujuan.
- .homeku/ adalah state lokal sementara yang diabaikan Git. Fixture dan tes berada di tests/; arsip tidak menjadi input discovery.

## Batas pembuktian

Validasi teknis tidak membuktikan kebenaran visual kamera, isi desain, sudut fisik atau hasil video generatif. Seluruh koreksi isi terjadi di chat sebelum ZIP final. Phase 2 menguji perangkat audit dan tujuh pilot nyata; data sintetis tidak menjadi knowledge produksi.


Sumber prinsip umum berada di sources/design-principles.json, terpisah dari knowledge/ hasil generator. Perubahan sumber ini memerlukan build/check serta regenerasi kit bila panduan audit ikut berubah. Prinsip diterbitkan verbatim, tanpa sintesis AI. docs/contracts/ai-reader-v2-3.md menjelaskan indeks dan proyeksi terbaru. Pengujian manfaat melalui pembuatan konsep/gambar tidak termasuk pekerjaan ini.


## Pemeriksaan kualitas sumber2.2

Baseline10FPS/native, bukti viewed dan fase, dasar angka kamera, konsistensi tempo, label gaya/skala, fact_coverage dan struktur MD wajib lolos sebelum review/export. Detail visual, kesesuaian narasi dan bukti tetap diperiksa AI di chat. Tidak ada sintesis AI pada generator atau review isi baru saat ingest. Kontrak lama, byte referensi dan aset render diterima dipertahankan.

## Metode2.3 dan discovery

Pengamatan mengikuti audit/visual-audit.md dahulu, JSON sesudah simpulan diperiksa silang. camera_checks wajib untuk semua fase, scale_measurement mendukung ~×, estimate_basis menjelaskan sudut/batas. Semua moderate sah. Template2.2.2 sama tampilan enam bagian2.2.1; checks/pengukuran tidak menambah tabel manusia.

Facet2.3 eksplisit; format lama lewat sources/fact-facets.json yang ikut fingerprint. role_source dan pointer menunjukkan aturan/fakta asal. Atribut belum dipetakan tercatat data/dependencies.json.unmapped_fact_attributes dan tetap ditemukan lewat knowledge/topics. Indeks tetap ringkas; data pemeriksaan lengkap melalui reader terpilih.

Kit memulihkan panduan lokal berhash; README hanya urutan tahap, bukan gabungan seluruh panduan. Perintah sample default6FPS; --contract-version 2.2 memilih default10. --fps 10 untuk pendalaman; --native untuk semua frame. Catatan kerja/receipt di luar ZIP. [Verifikasi](audit-method-verification.md).

## Authoring dan efisiensi2.4

Ikuti audit/authoring.md. prepare memakai cut frame-index yang telah diperiksa untuk membuat batas PTS, panel/midpoint dan baseline sekali. complete menghitung parsed metadata/summary/timestamp dan log selected dari session; isi visual/fakta tetap auditor. mark-viewed baru sesudah pemeriksaan nyata. Frame tambahan panel multi/Overview dapat diambil dengan sample --session ... --frames ...; tidak perlu membulatkan waktu manual.

check-input mengumpulkan kesalahan struktur/data sebelum JPEG. draft juga mewajibkan preflight internal; validasi artefak/snapshot sesudahnya tetap berlaku. Cache default sumber2.4 berada pada workspace audit/.cache/frames, performance.jsonl di workspace yang sama. Source lama dapat memakai --cache-dir secara eksplisit untuk pengujian teknis tanpa mengubah kontraknya.

Batch dipakai untuk sampling, sedangkan frame media final diperoleh dari extractor kanonis sekali per frame unik lalu di-cache untuk menjamin kesamaan byte. Executor subset baru memakai layout/font/media2.2.0 yang sama. Revisi basis/fakta tanpa pengaruh tampilan memakai ulang JPEG; notasi/gaya/area/panel/config yang memengaruhi gambar menginvalidasi dependensinya. Cache memiliki batas512MiB per bucket dan dapat dibangun ulang; symlink/korupsi tidak dipercaya.

performance.jsonl mencatat durasi alat, cache hit/miss, decode dan retry, bukan durasi aktif berpikir AI. Pilihan --resume tidak mengganti sumber/cut atau menimpa fakta. Tidak ada watcher, auto-viewed, auto-persetujuan atau auto-ingest.

Benchmark terisolasi: python tools/benchmark_audit.py /path/<id>.mp4 /work/audit.json --audit-info /work/audit-info.json --output /tmp/benchmark-baru. Hanya kandidat purpose=fixture dan revisi sintetis dalam root kerja kosong; bukan audit baru atau produksi. Bandingkan baseline/cold/warm/koreksi dan kesamaan byte. [Hasil nyata](audit-efficiency-verification.md).

## Default audit kamera2.5

Sumber2.5/report2.2.4/media2.2.1/reader2.5/generator8. Angka kamera opsional per komponen, termasuk medium/high; tidak perlu alasan khusus saat angka tidak ditulis. Estimate_basis cukup singkat bila berangka, boleh null bila tanpa angka. Baseline6FPS tetap; helper flow opsional/cache lokal, tanpa AI API. Kompatibilitas2.4 dan sebelumnya tetap kontrak asal, bukan default baru. Caption versi baru Start/Middle/End tebal dan waktu lebih kecil. Cache/session/flow/inventory kerja tidak masuk ZIP/knowledge; export byte sama tanpa render. Lihat docs/audit-camera-implementation-plan.md dan audit/authoring.md.
