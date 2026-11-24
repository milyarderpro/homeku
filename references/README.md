# Membaca referensi

Manusia mulai dari katalog lalu analysis.md referensi terpilih. Sumber 2.1 memakai laporan enam bagian: Profil desain, Ukuran & proporsi, Shot Timeline, Overview, Storyboard dan Shot Details. Detail per shot mempunyai A. Desain area, B. Framing & Lighting, C. Camera Movement. Nama gaya teknis English; penjelasan Indonesia.

Audit.json adalah sumber audit V2; MD hasil renderer dan manifest menyimpan metadata teknis/provenance. Media2.2.0: satu kolase per take kontinu, Overview seluruh frame wide satu baris, Storyboard seluruh kolase vertikal. Normal tiga panel, multi area dinamis. Satu take tanpa cut tetap satu shot walau melalui beberapa area.

Overview dipilih dari frame asli (biasanya awal IN/akhir OUT) dengan paragraf posisi/arah/sudut/tinggi/kemiringan/cakupan/elemen/kedalaman/cahaya. Camera Start tetap posisi awal sumber. Untuk produksi OUT, Overview akhir dapat menjadi gambar awal perjalanan IN kebalikan lalu hasilnya di-reverse, termasuk fase/rotasi/tempo. Data audit tetap kronologi sumber.

AI membaca data/search-index.json lalu `tools/library.py read` untuk identitas/shot/area. Proyeksi lengkap di data/projections/. [Reader2.1](../docs/contracts/ai-reader-v2-1.md) mempertahankan pointer, status, negasi dan bukti. `panel` serta `shot-image` mengambil foto/kolase tersimpan tanpa MP4; --from-storyboard mengambil seluruh blok pada media 2.2.0, --native secara khusus memeriksa MP4.

Paket 2.0 mempertahankan laporan lima bagian dan storyboard overview satu baris. Legacy 1.0/1.1 memakai MD/media menurut kontrak masing-masing. **Pustaka aktif kosong setelah reset edh001.** Audit baru dimulai dari r0001; MP4 kanonis dipertahankan.

Folder aktif hanya diisi importer dari ZIP final. Kandidat/fixture/arsip bukan input build. Jangan edit audit/MD aktif, proyeksi, katalog atau knowledge secara manual. [Status implementasi](../docs/overview-storyboard-verification.md).
