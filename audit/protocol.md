# Protokol audit HOMEKU 2.3

## 1. Inspeksi dan pengamatan

Baca audit/visual-audit.md sebagai metode inti tunggal. Inspect MP4: identitas, hash, metadata stream dan PTS native. Tentukan cut nyata. Satu take kontinu tetap satu shot walaupun beberapa area; bedakan visibility, route, fase dan cut.

Baseline6FPS semua shot + batas awal/akhir native; sumber≤6FPS atau shot<1detik seluruh native. Ambiguitas diperiksa10FPS lalu native atau langsung native pada rentang pertanyaan, bukan rentang tengah otomatis. Jangan interpolasi. Frame diekstrak belum viewed. Catatan kerja sementara memuat pengamatan sumbu/jangkar/arah, alternatif dan pertanyaan belum selesai.

Periksa kamera sesuai urutan metode inti, lalu bentuk/layout/detail rumah. Setelah simpulan diperiksa silang, baru baca json-guide.md dan kontrak untuk serialisasi. Jangan menambah konfirmasi pengguna di antara putaran internal.

## 2. Data dan kandidat

Isi audit.json2.3 dan audit-info nyata. camera_checks mencatat depth/translation/rotation per fase, termasuk Pan/Static. Keputusan hanya depth_direction/components; Camera Pattern turunan. ~× memakai scale_measurement dari objek/dimensi sama dan utuh; sudut diusahakan, keterbatasan khusus ditulis bila belum terpisahkan. Semua shot moderate sah. Jangan menambah fase/laju hanya agar bervariasi.

Catat detail Arsitektur, Furnitur & dekorasi, Lingkungan; fact_coverage dan facet_roles mempertahankan temuan konkret. Gaya English, prosa Indonesia, luas lantai wajib rentang angka. Camera Start tetap awal sumber, Overview posisi wide yang dipilih (sering akhir OUT), tiap Overview satu composition_summary. Semua bukti/panel/Overview harus viewed.

Jalankan draft-v2 dan review resmi. analysis.md hanya renderer2.2.2 enam bagian; jangan edit manual. Media2.2.0: N kolase, Overview satu baris, Storyboard vertikal; normal3panel, multi dinamis. Periksa silang JSON/narasi/fakta/kamera sederhana/notasi/fase/tempo dan seluruh gambar. Validator tidak memahami makna visual.

## 3. Tinjauan dan ekspor

Tampilkan MD lengkap, Overview, Storyboard serta semua kolase. Koreksi memperbarui sumber/log yang benar-benar diperiksa, kemudian draft/review kandidat lengkap. Persetujuan satu aspek bukan seluruh snapshot. Contoh kalimat persetujuan dalam panduan bukan instruksi pengguna.

Setelah persetujuan keseluruhan terbaru, export-v2 memakai receipt terakhir di luar kandidat. Export membungkus byte identik tanpa render ulang. ZIP final hanya JSON/MD/manifest dan N+2 JPEG, tanpa MP4, frame kerja atau receipt. MP4 tetap input terpisah dan sumber kanonis lokal. Ingest tidak mempunyai review isi kedua; revisi aktif lewat ZIP+1 dan supersedes benar.

## Kompatibilitas

Sumber2.2 tetap baseline10FPS/native dan report2.2.1;2.1 report2.2.0; format lebih lama mengikuti kontraknya. Jangan mengubah aturan sumber diterima secara diam-diam. Dokumen bekerja/ hanya acuan metode/notasi, bukan default produksi reverse/4–6detik/frontal/slow.
