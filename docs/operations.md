# Operasi pustaka HOMEKU

## Fondasi V2 dan batas workflow

V2 menerima audit.json sebagai sumber, MD hasil renderer dan satu kolase/shot plus storyboard. Legacy 1.0/1.1 tetap memakai MD menurut kontraknya. [Kontrak V2](contracts/package-v2.md) dan [pemetaan field](v2-field-map.md) adalah acuan teknis; workflow/prompt chat V2 tersedia pada audit/README.md. edh001 r0002/2.0 telah disetujui dan di-ingest; ZIP r0001 dipertahankan sebagai riwayat. Lihat [status Tahap 2](v2-stage-2-verification.md).

Renderer terbaru 2.1.2 memperkecil judul/nama area sekitar 15% dari 2.1.0. Header kolase cukup judul serta rentang/durasi. Di bawah foto terdapat Start/Middle/End atau momen, diikuti timestamp regular 75% ukuran label bold pada baseline yang sama. Header storyboard tetap memakai gaya utama. Nama gaya utama/pengaruh/interior memakai istilah bahasa Inggris dengan deklarasi identity.style_names_language=en; penjelasan tetap bahasa Indonesia. Renderer 2.0.0/2.1.0/2.1.1, template dan font lamanya tetap didukung. Tidak ada penerjemahan atau perubahan isi referensi aktif otomatis.

Alur helper V2 berikut telah diuji secara terisolasi dan digunakan pada edh001 r0002:

```sh
python tools/audit.py draft-v2 /path/<id>.mp4 /work/audit.json --audit-info /work/audit-info.json --output /work/candidate
python tools/audit.py review /work/candidate/<id> --source /path/<id>.mp4 --output /work/review.md
python tools/audit.py export-v2 /work/candidate/<id> --source /path/<id>.mp4 --output /work/packages --reviewed-sha256 <DIGEST_SNAPSHOT>
```

Tambahkan --include-source saat draft bila sumber kanonis belum terverifikasi. --quality/--scale/--columns mengatur media secara eksplisit. Receipt review berada di luar kandidat dan bukan persetujuan otomatis. Sesudah pengguna menyetujui keseluruhan kandidat, export mengemas byte yang sama; setiap koreksi dilakukan pada JSON/log aktual lalu draft/review ulang. Tidak ada regenerasi JPEG/created_at pada export. Aset renderer/font/template versi diterima tidak ditimpa; versi baru harus didaftarkan agar paket lama tetap dapat diperiksa.

Registry tetap version 1; entri V2 menambah contract_version/audit_sha256. Taksonomi version 3 membedakan alias dari hubungan gaya. Reader/index memakai 2.0 untuk semua format sumber. Fingerprint meliputi runtime, schema, template penulisan, template beku, font/lisensi dan prinsip/taksonomi; cache tidak menjadi sumber fakta.

Menyalin ZIP ke incoming/ lokal tidak otomatis mengolahnya. Jalankan `python tools/library.py ingest`; tidak ada review isi kedua setelah ingest. Perbaikan referensi yang sudah aktif memerlukan ZIP revisi berikutnya dengan supersedes yang benar.

## Menyiapkan audit V2 di chat

Gunakan [panduan audit V2](../audit/README.md), MP4 terpisah dan kit input berulang. ZIP input berisi empat file; AI menjalankan bootstrap untuk memulihkan 24 file runtime lengkap dengan schema/font/lisensi, lalu inspect/sample/draft-v2/review. Setelah keseluruhan kandidat disetujui, export-v2 memakai --receipt yang dibuat helper; receipt bukan persetujuan otomatis. Prompt audit/koreksi/ekspor mengatur tinjauan isi di chat; helper menyiapkan media dan memvalidasi ZIP sebelum download. Satu ZIP hasil final diunggah ke incoming/ tanpa menata file satu per satu.

`tools/audit.py` adalah helper workspace chat, bukan jalur publikasi ke references/. Input MD dan video disimpan di luar folder kandidat, sampling memakai folder baru per pass, dan regenerasi menolak file pengguna yang tidak dimilikinya. Lihat [hasil verifikasi Phase 2](phase-2-verification.md) untuk batas pengujian nyata.

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


Sumber prinsip umum berada di sources/design-principles.json, terpisah dari knowledge/ hasil generator. Perubahan sumber ini memerlukan build/check serta regenerasi kit bila panduan audit ikut berubah. Prinsip diterbitkan verbatim, tanpa sintesis AI. docs/contracts/ai-reader-v1.md menjelaskan indeks dan proyeksi. Pengujian manfaat melalui pembuatan konsep/gambar tidak termasuk pekerjaan ini.
