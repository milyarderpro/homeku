# Laporan manusia V2

Laporan `analysis.md` dihasilkan dari audit.json, bukan sumber ekstraksi fakta. Gunakan [template baku](../template-analysis-v2.md) dan renderer terbaru 2.1.2 dengan dukungan versi terdahulu. Salinan template sesuai versi berada pada tools/assets/templates/analysis-<versi>.md; perubahan versi selanjutnya tidak menimpa aset tersebut.

Urutan tetap:

1. Identitas desain: nama rumah, gaya utama, pengaruh, interior, ciri, palet dan suasana/lingkungan.
2. Ukuran dan proporsi: ukuran, massa, vertikal, tapak, proporsi, perkiraan luas lantai wajib.
3. Struktur dan timeline: satu baris per take kontinu; gerak bahasa manusia dan ritme.
4. Storyboard: satu baris overview seluruh area penting.
5. Detail shot: satu kolase, urutan panel dan tiga kelompok A/B/C.

A: paragraf Arsitektur, Furnitur dan properti, Lingkungan yang ditulis AI secara konkret. Multi area memakai penanda nama area dalam satu kartu. B: fokus, posisi/arah/sudut awal, framing awal → akhir dan pencahayaan; multi menambahkan rute, area terlihat serta hubungan/peralihan. C: bahasa kamera sederhana lengkap, ritme, DNA perjalanan bila berlaku, timeline fase bila multi/beberapa fase, lalu notasi teknis lengkap.

Rentang luas ditampilkan hanya `**60–90 m²**` (contoh format), tanpa dasar perkiraan atau catatan kepastian. Hash, log frame, ID fakta dan status proses tetap pada JSON/manifest/workspace. Renderer hanya menata nilai/narasi sumber; tidak menjalankan AI, menerjemahkan notasi atau menyimpulkan fakta.

Anchor eksplisit `profil-dna` dan `shot-NN` stabil. Metadata teknis dan pointer klaim berada pada proyeksi, sehingga perubahan judul manusia tidak memutus sumber. Ingest menolak laporan yang berbeda dari hasil renderer JSON sesuai versi; tidak memperbaikinya diam-diam.

[Contoh normal](../contoh-analysis-shot-normal.md) dan [contoh multi area](../contoh-analysis-shot-multi-area.md) adalah ilustrasi fiktif, bukan audit/paket aktif. Kelengkapan narasi dan kesesuaian semantiknya terhadap fakta diperiksa AI sebelum review; validator hanya memeriksa kesesuaian teknis eksplisit.

Nama gaya utama/pengaruh/interior memakai bahasa Inggris, penjelasan bahasa Indonesia. identity.style_names_language=en wajib pada renderer 2.1.x. Nilai nama berasal dari audit, bukan terjemahan renderer. Urutan panel pada laporan 2.1.x memakai Start/Middle/End atau nama momen dengan waktu ringkas, sementara timeline dan JSON mempertahankan data waktu sumber. Tampilan media mengikuti kontrak 2.1.2: judul/nama area tebal dengan ukuran 15% lebih kecil dari 2.1.0; header kolase cukup judul/rentang/durasi dan caption foto kembali memakai label serta timestamp kecil pada baris yang sama, dan header storyboard ID — Primary style — durasi — jumlah shot. Urutan panel pada MD tetap mencantumkan waktu sumber.

Versi baru: [analysis-v2-2.md](analysis-v2-2.md); dokumen ini tetap kontrak versi asal.
