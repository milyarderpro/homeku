# Proposal

## Why

Sebelum rilis HOMEKU 3.1, auditor perlu cara yang lebih cepat untuk meneruskan sesi, mengukur gerak kamera, mengisi struktur berulang, dan meninjau koreksi. Folder Google Drive HOMEKU sudah dipakai untuk mengambil bahan audit, sehingga alur rilis dapat memakai folder itu untuk menyimpan ZIP yang dipilih pengguna.

## What Changes

- Ukur durasi empat fase audit dan durasi, hasil, serta jumlah percobaan perintah utama di workspace.
- Periksa kesiapan runtime dan tampilkan pekerjaan yang masih perlu diselesaikan saat sesi dilanjutkan.
- Tambahkan pratinjau kandidat cut pada `inspect` dengan frame native dan PTS untuk konfirmasi auditor.
- Gunakan OpenCV untuk melacak jangkar terpilih dan mengukur perubahan panjang pada frame native untuk mendukung estimasi `~×`. Sediakan pengukuran manual dan pandu auditor mengupayakan estimasi visual per komponen untuk reproduksi kamera.
- Permudah pengisian dan koreksi satu fase kamera atau satu fakta area di `audit.json` kerja.
- Buat lembar review dengan tautan ke laporan dan media dari snapshot yang diperiksa, serta ringkasan perubahan setelah koreksi. Pertahankan ZIP sebelumnya jika koreksi menghasilkan paket lain dengan nama kanonis yang sama.
- Dokumentasikan alur ChatGPT dengan folder Google Drive HOMEKU sebagai sumber kit dan MP4 asli serta tujuan ZIP final yang dipilih pengguna. Verifikasi alur tersebut dalam pilot rilis.

## Capabilities

### New Capabilities

- `audit-session-workflow` — pemeriksaan kesiapan, status sesi, dan pratinjau cut.
- `camera-anchor-measurement` — pelacakan titik dan pengukuran rasio skala gambar dari jangkar.
- `audit-record-authoring` — pengisian dan koreksi terarah atas entri audit.
- `candidate-review-delivery` — lembar review, perbandingan hasil koreksi, dan penyerahan ZIP lewat Drive.
- `audit-performance` — pencatatan fase audit serta durasi dan hasil percobaan.

### Modified Capabilities

## Impact

Perubahan mencakup CLI dan runtime kit, panduan authoring, metode visual, prompt audit dan ekspor, pengujian, serta pilot `dreamshome01`. OpenCV dan NumPy wajib tersedia di runtime audit. Semua hasil bantu disimpan di workspace. Paket mengikuti kontrak 3.1 dan diserahkan melalui review teknis, ekspor snapshot, pemilihan pengguna, dan ingest dengan MP4 kanonis terpisah.
