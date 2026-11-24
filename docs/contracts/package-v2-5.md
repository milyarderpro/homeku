# Kontrak paket 2.5

Sumber audit.json2.5, manifest2.5, report2.2.4, media2.2.1, reader/index2.5 dan generator8. audit.json satu sumber isi; analysis.md hasil renderer. Kontrak2.4 tetap untuk paket lama.

## Kamera

Format [Komponen Utama] ([Skala]) [+ / →] [Komponen Sekunder] ([Intensitas / Kurva]). Kurung, angka dan komponen tambahan opsional. Medium/high tanpa angka sah, tanpa alasan atau alternatives khusus. Estimate_basis boleh null bila angka tidak ditulis. Bila angka ada, basis visual/asumsi singkat cukup; scale_measurement opsional, bila diisi diuji.

Angka tunggal default; rentang sah, termasuk ~1.75× dan ~25°–30°. Positif berhingga, rentang berurutan; rasio IN/OUT≥1. Sumber kerja dinormalisasi x→× dan koma desimal→titik tanpa mengubah nilai. Nilai diterima tidak diubah. ~× skala gambar, bukan tempo.

Parser mempertahankan raw, gerak dasar, direction, qualifiers, estimates dan toward. Straight/Diagonal/Pure/Mild/Subtle/Moderate/Strong/gentle serta Constant/Accelerating/Decelerating/Ease-In/Ease-Out tidak hilang. Intensitas bukan tempo. Easing melekat pada komponennya; speed_change fase bisa variable bila gabungan berbeda.

Contoh sah: Dolly-Out (~1.6×) + Orbit Left + Subtle Pan Right (Ease-Out).
+ simultan, → fase; satu paragraf. Notasi tiap fase tidak mengandung →; summary dihitung dari urutan fase. Camera Pattern tetap dari depth_direction, bukan tebakan prosa.

## Pengamatan dan fakta

Baseline6FPS+native boundaries; sumber≤6FPS/shot<1s seluruh native. Pendalaman10/native sesuai pertanyaan. Kamera depth→translation→rotation, jangkar dekat/jauh nyata dan per interval. Bukan selalu30FPS. Helper motion-hints opsional tanpa verdict atau panggilan AI; statistik, cache, session, inventory kerja dan performa tidak masuk paket/knowledge.

Facts/facet_roles/fact_coverage, state/negasi/uncertainty dan evidence tetap lengkap. Tak ada kuota enam fakta. Duplikasi fakta identik ditolak. Validator tidak menjamin kelengkapan makna narasi; AI mencocokkan temuan sebelum ekspor. Nama gaya English, prosa Indonesia, luas lantai wajib rentang angka.

## Media dan snapshot

Normal3panel Start/Middle/End dengan label tebal dan waktu lebih kecil di bawah gambar. Multi area dinamis; satu take tetap satu shot. Overview wide satu baris, Storyboard seluruh kolase vertikal; Camera Start tetap awal sumber. Layout/font lama utuh.

ZIP hanya audit.json, analysis.md, manifest.json dan N+2JPEG. Tanpa video, frame kerja, log, cache, inventory kerja atau receipt. MP4 kanonis terpisah/hash sesuai. Review mengikat seluruh snapshot; ekspor membungkus byte sama tanpa render ulang. Ingest hanya final/revisi eksplisit; tidak ada review isi kedua.

Sumber2.4 tetap angka wajib pada gerak jelas;2.3 tetap pengukuran ~×;2.2 tetap10FPS. Tidak ada konversi diam-diam.
