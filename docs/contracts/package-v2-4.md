# Kontrak paket2.4

audit.json2.4 satu sumber isi; manifest2.4 teknis; laporan2.2.3 enam bagian; media2.2.0; reader/index2.4. Ketentuan2.3 tetap berlaku kecuali perbedaan berikut. Sumber diterima tidak dikonversi.

## Estimasi visual

~×/~° adalah perkiraan visual yang sah, memakai asumsi wajar dari video. Tidak perlu kalibrasi lensa, pose3D atau sumber eksternal. Pan/Orbit yang jelas (confidence medium/high) memiliki ~°, Dolly/Zoom memiliki ~×. Bagian low/unknown boleh tanpa angka bila estimate_basis menjelaskan kendala khusus dan alternatives terisi. Ketiadaan focal length bukan alasan tunggal menghapus angka pada gerak yang jelas.

scale_measurement tetap field nullable dan boleh null walau ada ~×. Bila diisi, evidence, dimensi, piksel positif, kronologi dan rasio diuji seperti2.3; tidak menyatakan pengukuran yang belum dijalankan. IN=akhir/awal, OUT=awal/akhir; ~× bukan kecepatan/jarak. estimate_basis satu kalimat pengamatan/asumsi cukup. Estimasi ditulis dalam tanda kurung: Dolly-In (~2×) + Pan Right (~15–20°). + simultan, → urutan; satu paragraf.

## Pengamatan dan kelengkapan

Baseline6FPS mencakup setiap shot dan batas native; sumber≤6FPS dan shot<1s native. Pendalaman10FPS/native sesuai pertanyaan; semua moderate sah. Satu take multi area tetap satu shot. camera_checks tiga sumbu, motion_observations, fact_coverage, facet_roles, status/negasi/uncertainty dan pointer tetap lengkap; basis teknis ringkas tanpa mengurangi fakta.

Helper prepare/complete mengisi hanya metadata mekanis pada sumber kerja. Tidak ada source JSON kedua. Camera Start sumber dan Overview terpilih tetap berbeda. viewed tidak diisi oleh ekstraksi/cache; deklarasi AI eksplisit diperlukan.

## Paket dan snapshot

ZIP hanya audit.json, analysis.md, manifest.json dan N+2JPEG; tanpa MP4/source.mp4, cache, log kerja atau receipt. MP4 input terpisah/sumber kanonis lokal, hash wajib cocok. analysis.md hanya renderer2.2.3, enam bagian/A-B-C yang sama; font/layout2.2.0 immutable.

check-input/preflight memeriksa data sebelum render; validasi artefak sesudah render tetap wajib. Cache terikat hash/versi/parameter dan tidak menjadi sumber fakta atau syarat ingest. Koreksi memerlukan review snapshot terbaru. Export hanya membungkus byte disetujui, tidak merender ulang. Revisi/supersedes/batas paket mengikuti2.3.

Versi2.3 tetap mewajibkan pengukuran saat ~×;2.2 tetap10FPS; semua format lama menurut kontraknya. Generator tidak mengubah fakta dari narasi.
