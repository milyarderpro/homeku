# Operasi pustaka HOMEKU

## Alur dan status

`incoming ZIP → validasi → staging → proyeksi → katalog/knowledge → pemeriksaan → publikasi`.

CLI `python tools/library.py ingest` memindai semua ZIP langsung dalam incoming/. Argumen path ZIP dapat dipakai untuk batch tertentu. Paket gagal dicatat tanpa mengganti referensi aktif; paket valid lain dalam batch tetap diproses. Keluar dengan kode 1 bila ada kegagalan, meskipun paket valid sudah dipublikasikan. Keluaran JSON memuat imported, unchanged atau failed beserta error spesifik.

Registry dalam data/registry.json menyimpan revisi dan fingerprint sumber/isi/paket. data/ingest.json mengikat hasil dengan hash ZIP; tanggal eksekusi tidak dimasukkan agar replay identik tidak mengubah repo. Paket gagal dapat dicoba ulang setelah sumber/tooling diperbaiki. Revisi yang sudah berhasil tetap tercatat meskipun telah diganti oleh revisi berikutnya.

Berkas JSON dalam data/projections/ dihasilkan dari MD dan dapat dibangun ulang. Jangan edit manual. Fingerprint mengikat seluruh byte referensi serta versi generator/schema/taksonomi. Alias hanya berlaku untuk label eksplisit; label baru tetap dicari dari katalog, dan konflik/negasi/unknown tetap tersimpan.

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
