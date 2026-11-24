# Membaca referensi HOMEKU

Manusia memilih referensi dari katalog dan membaca `analysis.md`. Laporannya memuat Profil desain, Ukuran & proporsi, Shot Timeline, Overview, Storyboard, dan Shot Details. Setiap shot mencakup desain area, framing dan pencahayaan, serta gerakan kamera. [Katalog](../catalogs/README.md)

AI mulai dari `data/search-index.json`, lalu memakai `tools/library.py read` untuk membaca identitas, shot, atau area. `audit.json` menyimpan isi sumber. Proyeksi JSON menyediakan pointer ke fakta, framing, kamera, tempo, dan bukti di manifest. [Kontrak reader](../audit/contracts/reader.md)

Satu take kontinu dapat memuat beberapa area. Kolase shot normal berisi tiga panel. Multi area memakai panel dinamis. Overview menyatukan frame wide terpilih dalam satu baris, dan Storyboard menumpuk semua kolase secara vertikal. Camera Start menunjuk awal perjalanan sumber. Overview memperlihatkan gambaran wide terpilih, yang biasanya berada di awal IN atau akhir OUT.

Gunakan `panel` untuk foto pada selection, `shot-image` untuk kolase, atau `shot-image --from-storyboard` untuk blok Storyboard. Ketiganya membaca media tersimpan. `panel --native` memerlukan MP4 kanonis untuk mengambil frame bukti asli.

Folder referensi aktif diisi importer dari ZIP final yang tercatat di registry. Koreksi diterima sebagai ZIP revisi. [Kontrak paket](../audit/contracts/package.md)
