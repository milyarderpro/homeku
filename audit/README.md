# Audit HOMEKU V2 di ChatGPT/Gemini

Satu video per chat. Lampirkan **MP4 asli + homeku-audit-kit.zip**, lalu kirim [prompt audit](prompts/01-audit.md). AI menjalankan seluruh helper di workspace chat. Anda cukup meninjau laporan dan gambar, memberi koreksi, lalu mengunduh satu ZIP final. Sesudah menaruh ZIP di incoming/ lokal, jalankan `python tools/library.py ingest`.

## Alur singkat

1. AI membuka kit, membaca README, menjalankan `python homeku_runtime.py --output .`, lalu inspect video. Runtime/schema/template/font/lisensi tersedia tanpa repo penuh atau API AI.
2. AI menentukan cut nyata, memeriksa baseline 10 FPS seluruh shot + frame native awal/akhir, lalu memperdalam native bila arah/fase/tempo/detail belum jelas. Satu take melewati banyak area tetap satu shot.
3. AI mengisi `work/audit.json` dari template serta `work/audit-info.json` dari log nyata. [Panduan JSON](json-guide.md) menjelaskan bidang dan bukti. JSON adalah satu sumber isi; MD tidak ditulis terpisah.
4. AI menjalankan draft-v2 dan review. Anda melihat storyboard, kolase semua shot dan analysis.md manusia dengan desain lengkap, posisi awal, kamera sederhana/teknis dan ritme. Nama gaya memakai bahasa Inggris; prosa Indonesia.
5. Bila perlu gunakan [prompt koreksi](prompts/02-correct.md). AI memperbarui JSON/log, merender ulang dan menampilkan hasil terbaru. Persetujuan satu aspek bukan persetujuan keseluruhan audit.
6. Setelah seluruh kandidat sesuai, kirim [prompt ekspor](prompts/03-export.md). Export mengemas kandidat yang sama tanpa membuat ulang JPEG/MD/created_at. Anda mengunduh satu ZIP `<id>-r0001.zip` atau revisi yang benar.

Tidak ada review isi kedua setelah ingest. Kesalahan teknis harus diselesaikan sebelum penyerahan ZIP; helper tidak membuat atau menebak fakta agar lolos validasi.

## Perintah yang dijalankan AI

```sh
python homeku_runtime.py --output .
python tools/audit.py inspect /path/<id>.mp4
python tools/audit.py sample /path/<id>.mp4 --output work/baseline-shot-01 --start 0 --end <SHOT_END> --shot-id shot-01
python tools/audit.py sample /path/<id>.mp4 --output work/native-shot-01 --native --start <START> --end <END> --shot-id shot-01 --reason "Pan/orbit belum jelas"
python tools/audit.py draft-v2 /path/<id>.mp4 work/audit.json --audit-info work/audit-info.json --output work/candidate
python tools/audit.py review work/candidate/<id> --source /path/<id>.mp4 --output work/review.md
python tools/audit.py export-v2 work/candidate/<id> --source /path/<id>.mp4 --output work/final --receipt work/review.md.json
```

Receipt dihitung helper dan tetap di luar kandidat; pengguna tidak diminta membaca JSON/hash. Receipt bukan persetujuan otomatis: export tetap menunggu pernyataan pengguna bahwa keseluruhan hasil terbaru sesuai. `--reviewed-sha256` tetap tersedia untuk pemanggilan teknis eksplisit.

Untuk revisi yang sudah aktif, `--supersedes work/supersedes.json` berisi revision/content_sha256 aktif yang benar; jangan mengarangnya. `--include-source` pada draft menyertakan MP4 jika sumber kanonis belum terverifikasi tersedia dengan hash sama. Input JSON/video disimpan di luar folder kandidat. Draft bisa dibuat ulang setelah koreksi; export tidak melakukan draft ulang.

## Isi paket dan media

Paket final berisi audit.json, analysis.md, manifest.json, satu kolase per shot dan satu storyboard; source.mp4 opsional. Normal memakai tiga panel Start/Middle/End; multi area memakai panel dinamis yang cukup menjelaskan perjalanan. Storyboard overview seluruh area satu baris. Semua gambar berasal dari frame asli; tidak ada JPEG frame terpisah, motion/ atau seluruh rangkaian frame dalam ZIP final.

Kit input dan ZIP hasil berbeda. Kit input dikemas ringkas untuk batas lampiran provider, tetapi bootstrap memulihkan seluruh inventaris teknis yang sama dengan repo. Gunakan hanya alat yang benar-benar tersedia dan laporkan kegagalan spesifik; [panduan lingkungan](providers.md) tidak menganggap nama model sebagai bukti kemampuan eksekusi.

Format sumber/paket 2.0, renderer terbaru 2.1.2. Legacy 1.0/1.1 tetap dapat dibaca, tetapi prompt audit baru mengisi JSON V2. [Pilot](pilots/README.md) mencatat run nyata; kit siap tidak berarti tujuh pilot selesai.
