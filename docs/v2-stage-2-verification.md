# Verifikasi Tahap 2 V2

Tanggal: 22 November 2026. **Workflow dan kit siap; keseluruhan Tahap 2 belum selesai.**

## Status sesuai urutan plan

| Langkah | Hasil aktual |
| --- | --- |
| 2.1 | Fondasi Tahap 1 diperiksa; saat pemeriksaan awal edh001 masih r0001, kontrak 2.0/renderer 2.1.2 tersedia |
| 2.2 | Template audit JSON/log serta panduan pengisian tersedia; placeholder wajib diisi hasil nyata |
| 2.3 | Protokol/rubrik/kosakata/kalibrasi diselaraskan: 10 FPS adaptif, arah/fase/tempo/jitter, area/fungsi/rute dan kelengkapan desain |
| 2.4 | Prompt audit, koreksi dan ekspor memakai sumber JSON serta persetujuan kandidat lengkap |
| 2.5 | review membuat laporan manusia + receipt eksternal; export-v2 dapat membaca --receipt, menolak salah kandidat atau snapshot berubah |
| 2.6 | Kit V2 dibangun ulang; empat file input membuka 24 file runtime lengkap tanpa repo penuh |
| 2.7 | Portabilitas teknis diuji dari workspace kosong, termasuk legacy dan V2; tes keseluruhan dicatat di bawah |
| 2.8 | Seluruh lima shot edh001 diaudit ulang dari sumber; kandidat V2 r0002 tersedia |
| 2.9 | **Selesai**: pengguna menyetujui keseluruhan kandidat V2 setelah laporan, storyboard dan kelima kolase ditampilkan |
| 2.10 | **Selesai**: r0002 diekspor tanpa perubahan, di-ingest dan lolos pemeriksaan teknis/replay |
| 2.11 | **Belum**: edh058, edh013, edh033, edh049, edh056, dreamshome01 dijalankan pengguna pada ChatGPT/Gemini |
| 2.12 | Kalibrasi masih terbuka; hasil lokal dan keterbatasan sudah dicatat, kedua provider belum terbukti lewat run pengguna |

## Perubahan utama

- Baru: audit/template-audit.json, audit/template-audit-info.json dan audit/json-guide.md. JSON diisi AI, MD dihasilkan renderer; pengguna tidak diminta mengedit JSON atau hash.
- Diperbarui: audit/README.md, protocol/rubric/vocabulary/calibration/providers dan tiga prompt. Nama gaya teknis English, luas wajib, desain konkret tiga kategori, posisi awal serta kamera sederhana/teknis tetap terpisah dari proses teknis.
- Helper tools/audit.py menambahkan --receipt, sambil mempertahankan --reviewed-sha256 dan jalur legacy. Receipt adalah pengunci byte, bukan persetujuan otomatis.
- Builder mengemas README.md, homeku_runtime.py, template-audit.json dan template-audit-info.json. Bootstrap standard-library memeriksa hash payload/inventaris, path dan isi sebelum menulis; file berbeda tidak ditimpa. Seluruh schema, implementasi versi lama, template, font regular/bold serta lisensi tetap ada.
- Panduan operasi, README utama, plan utama/plan improvement lama dan plan V2 diselaraskan dengan status sebenarnya. Tidak ada perubahan renderer/template/font beku, plugin produksi atau fakta turunan manual.

## Kit dan batas lingkungan

Kit: [homeku-audit-kit.zip](../audit/homeku-audit-kit.zip), 827,316 byte, SHA-256 `4883c7ca0403f5dea2a92a6d408048708cae82a4e5c6598e9fcdd2c4557c8330`. Empat anggota ZIP input memulihkan seluruh 24 file runtime; tidak ada video/audio dalam kit input. Python 3.11+, Pillow, jsonschema dan FFmpeg/ffprobe diperlukan untuk helper; bootstrap sendiri hanya memakai standard library. MP4 diunggah terpisah.

Panduan [ChatGPT file workflow](https://learn.chatgpt.com/docs/artifacts-viewer) dan [Gemini upload](https://support.google.com/gemini/answer/14903178?hl=en) diperiksa saat implementasi. Gemini membatasi ZIP input sampai 10 file dan tidak menaruh video/audio dalam ZIP input; kit empat file memenuhi susunan itu. Dokumentasi file tidak membuktikan setiap akun/permukaan menyediakan Python/FFmpeg. Eksekusi inspect/sample di workspace yang digunakan tetap menjadi bukti aktual. Tes lokal portabel bukan run antarmuka ChatGPT/Gemini.

## Audit ulang edh001 yang benar-benar dilakukan

Sumber video/edh001.mp4: SHA-256 `3ccf8acf75ca46922025d39b3198e3cf460f9cb3c96c4dc670be0fa2d23c0de8`, 720×1280, 30 FPS, 552 frame, durasi stream video 18.40 s. Audio tidak diperiksa. Cut tetap pada 4.733333333, 8.3, 11.566666667 dan 15 s.

| Pass | Rentang sumber (s) | Frame dipilih dan dilihat |
| --- | --- | --- |
| shot-01 · sampling | 0–4.733333333 | 48 |
| shot-02 · sampling | 4.733333333–8.3 | 37 |
| shot-03 · sampling | 8.3–11.566666667 | 34 |
| shot-04 · sampling | 11.566666667–15 | 35 |
| shot-05 · sampling | 15–18.4 | 35 |
| shot-01 · frame-by-frame | 0–4.733333333 | 142 |
| shot-02 · frame-by-frame | 4.733333333–8.3 | 107 |
| shot-04 · frame-by-frame | 11.566666667–15 | 103 |
| shot-03 · frame-by-frame | 9.8–11.566666667 | 53 |

Total **455 frame unik** melalui sembilan pass; duplikat antarpass tidak dijumlahkan sebagai frame unik. Semua contact sheet pass tersebut dibuka pada chat implementasi, dilengkapi pemeriksaan frame besar untuk detail desain. Log baru berada di manifest kandidat; log r0001 tidak dipakai sebagai klaim pemeriksaan baru. Sampling/ekstraksi sendiri tidak menandai frame sudah dilihat.

Hasil mempertahankan lima shot dan rumusan kamera r0001 setelah pemeriksaan sumber baru. Satu bathroom-laundry adalah satu area fisik/two functions, bukan contoh continuous take lintas beberapa ruang. Kelengkapan multi area masih dibuktikan fixture teknis sampai pilot nyata tersedia.

Seluruh 128 fakta lama dipertahankan dengan status/negasi/bukti native yang dipetakan. Tiga puluh klaim DNA lama dilestarikan; penamaan gaya utama diubah dari deskripsi modern kontemporer bergeometri lengkung menjadi Contemporary Modern dengan alasan dalam basis. Warm Contemporary dan pengaruh Scandinavian Contemporary ditambahkan sebagai interpretasi eksplisit, bukan fakta klasifikasi historis. Estimasi luas total rumah 60–90 m² wajib terisi; basis/uncertainty hanya JSON.

## Snapshot yang disetujui

- [Laporan review manusia lengkap](../audit/pilots/edh001-v2-review.md): lima bagian baku, desain lengkap dan semua gambar.
- [analysis.md kandidat](../audit/pilots/v2-candidates/edh001/analysis.md), [sumber audit.json](../audit/pilots/v2-candidates/edh001/audit.json), [manifest](../audit/pilots/v2-candidates/edh001/manifest.json).
- Receipt eksternal: audit/pilots/edh001-v2-review.md.json. Snapshot lengkap `71e949c51a3ca82f0a8d22c26ad98c82c6283d8c40413b8b0a24ef99e178ca45`. Setiap perubahan kandidat memerlukan review/receipt baru; receipt sendiri bukan persetujuan; pengguna kemudian menyetujui seluruh snapshot dengan “ya saya setuju”.
- Lima kolase 2260×1507 dan satu storyboard satu baris 3750×1577. Semua dibuka dan diperiksa visual: caption di bawah foto, timestamp kecil, header interval/durasi saja; tidak ada teks menimpa foto. Foto asli termasuk black bar sumber dipertahankan.
- Media: r0001 = 22 JPEG / 4,252,016 byte; kandidat V2 = 6 JPEG / 4,840,420 byte. Jumlah file berkurang, ukuran byte naik sekitar 13.8% pada native scale/quality 91. Tidak ada janji kolase otomatis lebih kecil; tidak mengubah kualitas/layout yang disetujui untuk mengejar ukuran.
- Tidak ada JPEG overview/frame kerja terpisah, motion/, clip atau source.mp4 duplikat dalam kandidat. Sumber kanonis sudah terverifikasi tersedia.

Sebelum ekspor, **28 file baseline** (referensi r0001, registry, MP4 dan kedua ZIP r0001) masih sama hash-nya. Sesudah pengguna menyetujui keseluruhan kandidat, r0002 diekspor dan di-ingest: referensi aktif/registry/turunan berubah melalui importer. MP4 dan kedua ZIP r0001 tetap sama hash-nya. Tidak dilakukan review isi kedua setelah ingest.

## Pemeriksaan teknis

Hasil akhir:

| Pemeriksaan | Hasil |
| --- | --- |
| python -m unittest discover -s tests -t . -v | **100 tes lulus**, 132.246 s |
| python tools/library.py check | Lulus; 1 referensi aktif / 5 shot |
| python tools/build_audit_kit.py --check | Lulus; kit deterministik cocok dengan sumber |
| git diff --check | Lulus |
| Kandidat draft-v2 / review dengan sumber asli | Lulus; receipt cocok snapshot lengkap |
| Hash baseline | Praekspor: 28 file sama; pasca-ingest: MP4 dan kedua ZIP r0001 tetap sama |

Suite mencakup bootstrap/inventaris lengkap serta idempotensi dan penolakan file berbeda; jalur legacy tetap dapat review/export dari kit terpulihkan. Jalur V2 terisolasi mencakup draft, review, export receipt, pembukaan ulang ZIP/ingest, penolakan kandidat yang berubah dan receipt milik kandidat lain. Tidak mengekspor edh001 r0002 untuk tes. Validasi teknis bukan penilaian isi pengguna.

Kegagalan awal yang diperbaiki: escaping string bootstrap; serta satu tes legacy yang belum menjalankan bootstrap setelah unpack. Seluruh skenario kit sekarang mengikuti langkah pemakaian baru, tanpa mengubah pemeriksaan snapshot/source/ZIP legacy.

## Langkah berikutnya

edh001 V2 telah disetujui dan aktif sebagai r0002; langkah 2.1–2.10 selesai. Berikutnya pengguna menjalankan enam pilot memakai kit V2, mulai dari edh058, dengan kedua provider terwakili. Koreksi diterapkan sebelum download; tidak ada review isi kedua setelah ingest. Kontrak tetap provisional selama pilot/kalibrasi belum selesai.

## Ekspor dan ingest r0002 setelah persetujuan

Pengguna menyetujui **seluruh** hasil yang ditampilkan dengan “ya saya setuju”. Export dijalankan memakai receipt snapshot terakhir; tidak membuat ulang JSON, MD, JPEG atau created_at. Paket final hanya memuat sembilan file kontrak: audit.json, analysis.md, manifest.json dan enam JPEG. Receipt berada di luar paket dan MP4 kanonis tidak diduplikasi.

| Identitas | Nilai |
| --- | --- |
| Snapshot disetujui = kandidat = ZIP = referensi aktif | `71e949c51a3ca82f0a8d22c26ad98c82c6283d8c40413b8b0a24ef99e178ca45` |
| ZIP final | [edh001-r0002.zip](../incoming/edh001-r0002.zip) |
| Ukuran ZIP | 4,600,760 byte |
| SHA-256 ZIP | `c290e7f81642498330cdb4b0b4b2ecaf2238c5074b83761bf31b08040e74c26f` |
| Revisi aktif / kontrak | 2 / 2.0 |
| MD aktif | `1039de150e172fa286f075644827f9bb70dcab21bc96fd8c3cd35259f10bd9ee` |
| Audit JSON aktif | `aa18332caf6fb2a32af9258720d74bb59da3f3628884ba2d0e2a765790da5168` |
| Supersedes | r0001 / 6664a56c09c428c24c30ac00bfb4c8a973647bd8269d0f661eca719197b59c96 |

Ingest pertama menghasilkan imported dan memperbarui references/edh001, registry/ledger, proyeksi/indeks, katalog dan knowledge. Semua berkas aktif dibandingkan byte per byte dengan ZIP/kandidat. Pembaca identitas/kelima shot mempertahankan 128 fakta, 32 klaim DNA dan seluruh pointer bukti; pencarian kitchen + fast menemukan r0002. Replay incoming/ terhadap r0001 dan r0002 sama-sama unchanged, changed=[] dan seluruh berkas managed tetap sama hash-nya. ZIP r0001 dan source MP4 tetap utuh.

[Laporan manusia aktif](../references/edh001/analysis.md), [sumber JSON aktif](../references/edh001/audit.json) dan [JSON pembaca AI](../data/projections/edh001.json) tersedia. Pembaruan status/calibration di kit tidak mengubah paket final yang diterima. Enam pilot pengguna serta pembuktian run ChatGPT/Gemini masih terbuka; tidak ada klaim keseluruhan Tahap 2 telah selesai.

Pemeriksaan setelah publikasi: `python tools/library.py build` menghasilkan changed=[]; `python tools/library.py check` lulus (1 referensi/5 shot), `python tools/build_audit_kit.py --check` lulus. Isi audit yang diterima tidak diedit; hanya status dokumen/pilot dan bundel panduan yang diperbarui.
