# HOMEKU — Core design knowledge

Pintu masuk untuk mempelajari desain rumah dan bahasa visual home-tour. Ini adalah pustaka pengetahuan; alur kreatif proyek serta prompt generator dikelola plugin atau master prompt.

[Versi pengetahuan dan sumber](release.json) · [Direktori konsep](directories/README.md) · [Semua profil](reference-profiles/README.md) · [Bukti desain](design-evidence/README.md) · [Pola seluruh korpus](corpus-patterns.md) · [Kamus bilingual](taxonomy/README.md) · [Kontrak akses](access-contract.md)

## Bentuk rumah dan identitas

Baca bentuk massa utama, bentuk atap, tingkat bangunan, proporsi bukaan dan pintu masuk sebagai satu sistem. Sebuah label gaya saja belum menjelaskan geometri atau ukuran ruang. Pengaruh beberapa gaya dapat dipakai bersama jika bentuk, proporsi dan hirarki materialnya koheren. Kategori skala pada sumber adalah kesan visual; estimasi luasnya bukan ukuran terukur.

Penjelasan dan contoh: [arsitektur](architecture-dna.md), [kompatibilitas](design-compatibility.md). Temukan contoh melalui [keluarga gaya](directories/style_family.md), [pengaruh gaya](directories/style_influence.md), [atap](directories/roof_form.md), dan [skala](directories/scale.md).

## Interior, lanskap, cahaya dan material

Karakter interior berasal dari hubungan objek dan arsitektur: arah sofa terhadap titik perhatian, letak meja, bukaan, sirkulasi dan elemen tetap. Lanskap membentuk pendekatan ke pintu, foreground serta pemandangan melalui jendela. Palet, tampilan material, tekstur, cahaya jendela dan lampu membantu membangun karakter yang konsisten.

Baca [interior](interior-dna.md), [lanskap](landscape-dna.md), serta [cahaya dan palet](lighting-and-palette-dna.md). Gunakan direktori [ruang](directories/room_type.md), [material appearance](directories/material_appearance.md), [bukaan](directories/opening.md), [pencahayaan](directories/lighting.md) dan [mood](directories/mood.md).

## Hubungan ruang dan kontinuitas

Dua ruangan dalam potongan video yang berbeda belum membuktikan posisi atau sambungannya. Satu pandangan yang memperlihatkan living dan kitchen mendukung deskripsi ruang yang terlihat bersama, tetapi belum menghasilkan denah terukur.

Untuk rumah baru, posisi ruang, bukaan, lantai, atap, elemen tetap dan dunia di luar jendela dapat dirancang sebagai keputusan kreatif yang konsisten. Perubahan viewpoint tidak semestinya mengubah geometri rumah secara tidak disengaja. Bedakan orientasi rumah dari kiri/kanan pada gambar.

Baca [prinsip ruang](spatial-design-principles.md) dan [konfigurasi](directories/configuration.md).

## Bahasa visual dan gerak

Komposisi menjelaskan apa yang terlihat dan menjadi titik perhatian. Framing awal–akhir menunjukkan bagaimana informasi ruang diungkap. Translasi kamera, pan, tilt dan perubahan framing adalah konsep berbeda. Gerak relatif foreground terhadap background dapat membantu memahami perubahan viewpoint, tetapi label kamera tetap berupa interpretasi visual.

Urutan eksterior–interior merupakan salah satu pola dalam koleksi, dengan beragam pengecualian. Jumlah shot dan durasi sumber tidak menjadi aturan wajib produksi.

Baca [sinematografi](cinematography-dna.md) dan [gerak kamera](directories/camera.md). Profil individual menautkan scene, label kamera dan frame setiap shot; untuk menguji gerak, periksa video atau bukti temporal yang tersedia. Tautan gambar tidak berarti AI sudah melihat gambar itu.

## Menyusun desain baru dari referensi

Gunakan referensi sebagai kosakata bentuk dan hubungan visual. Orisinalitas dapat dikembangkan melalui massa, skala, bukaan, tata ruang, hirarki material, lanskap dan titik perhatian. Penggabungan referensi perlu menghasilkan satu rumah yang masuk akal. Beberapa sumber inspirasi tidak membuktikan adanya satu rumah gabungan yang sudah ada.

Baca [orisinalitas](originality-framework.md), [kompatibilitas](design-compatibility.md) dan [sintesis DNA](dna-summary.md).

## Ketidakpastian sumber dan kebebasan kreatif

Semua referensi tersimpan dapat menjadi inspirasi. Confidence mengukur kepastian klaim tentang sumber, bukan larangan memilih elemen desain baru. Tampilan seperti batu pada sumber yang komposisinya belum diketahui boleh menginspirasi keputusan menggunakan batu alam pada rumah baru. Keputusan itu tidak membuktikan bahwa sumber memakai batu alam.

Pisahkan pengamatan, agregat yang dihitung, interpretasi dan prinsip desain. Jawab “belum diketahui” untuk fakta sumber yang tidak didukung, sambil tetap membuat keputusan kreatif yang jelas saat merancang konsep baru. Tidak ada syarat verifikasi manual. Pemetaan istilah bersifat leksikal dan tidak menggantikan review visual AI.

Baca [metodologi](methodology.md), [cakupan bukti seluruh koleksi](design-evidence/README.md) dan [indeks contoh terkurasi](evidence-index.yaml). Review storyboard mencakup ciri terpilih; review temporal hanya diklaim pada sumber yang tercatat. Sampel tersedia tidak otomatis berarti sudah ditinjau.

## Menelusuri rincian

[Direktori](directories/README.md) → profil referensi → analysis.yaml/analysis.md dan frame shot. Catat ID sumber dan versi pengetahuan saat mengutip bukti. Jika akses file atau gambar gagal, nyatakan bagian yang belum terbaca.

Web dan konektor GitHub menggunakan berkas yang sama. Konsumen tidak perlu clone atau menjalankan skrip. Arsip baru dapat tumbuh sebelum masuk snapshot ini; [inventaris sumber](source-manifest.json) dan [manifest pengetahuan terbit](release.json) memiliki tanggung jawab berbeda.
