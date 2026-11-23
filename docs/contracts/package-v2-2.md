# Kontrak paket 2.2

Satu sumber isi audit: audit.json2.2. Manifest2.2 mencatat provenance dan log pemeriksaan. Laporan2.2.1 dihasilkan renderer; media tetap2.2.0, N+2 JPEG menurut kontrak2.1. Reader/index2.2. Tidak ada konversi paket diterima.

Video referensi DILARANG dalam ZIP final, termasuk source.mp4. MP4 hanya input terpisah di workspace chat dan video/<id>.mp4 di repo lokal. Tidak ada --include-source untuk format2.2.

Struktur ZIP, batas ukuran, sumber kanonis, supersedes, snapshot review/export dan ingest mengikuti package-v2-1.md dan package-v2.md. Pasangan baru: sumber2.2 → report2.2.1 + media2.2.0. Versi lama tetap menggunakan pasangan asal.

Skala: tiny/small/medium/large/unknown; unknown memerlukan state unknown pada profil skala. Rentang luas lantai tetap wajib. Nama gaya English, satu gaya per klaim; tidak ada whitelist nama gaya. Primary/interior/influence harus konsisten dengan profil. Penjelasan Indonesia, basis/uncertainty tetap JSON.

Setiap design memiliki fact_coverage untuk architecture/furnishings/environment: mapped dengan fact_ids yang ada dan mencakup area; atau not-visible/unknown dengan basis dan tanpa fact_ids. Tidak ada kuota fakta per ruangan; status bukan jalan pintas untuk menghilangkan detail yang terlihat. Kelengkapan visual diperiksa AI sebelum review.

Setiap fase memiliki motion_observations per component_index, evidence, basis, estimate_basis dan alternatives. Gerak yang dinyatakan membutuhkan ≥2 frame berbeda dalam fase; toleransi batas paling banyak satu interval frame native dan tidak keluar shot. Notasi numerik ~×/~° memerlukan estimate_basis. Bukti fase dan observasi harus tercatat viewed dalam log. Satu-frame hanya untuk Uncertain/unknown; tidak membuktikan gerakan. Pengamatan pan/orbit/truck memakai perspektif, paralaks, oklusi dan jangkar; alternatif dicatat bila ambigu. Tempo fase sesuai tempo_profile yang overlap: label tunggal jika seragam, variable jika berubah, unknown tetap dipertahankan.

Baseline 10 FPS atau seluruh native; sumber <10 FPS seluruh frame native. Record sampling rendah hanya tambahan, tidak menutup coverage wajib. Native PTS/awal/akhir wajib tepat. Log konsisten tidak membuktikan AI melihat; jangan menandai frame ekstraksi sebagai viewed.

Paragraf polos tidak boleh menyisipkan struktur Markdown/HTML. analysis.md wajib lulus struktur enam bagian dan kesamaan byte renderer. Pemeriksaan teknis berhenti sebelum review pengguna; tidak ada review isi baru setelah ingest.
