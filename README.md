# Pustaka HOMEKU

Pustaka referensi desain, komposisi dan gerakan kamera dari audit video. Workflow baru memakai **audit/paket 2.1**, laporan/media **2.2.0** dan pembaca AI **2.1**. audit.json adalah sumber audit; analysis.md laporan manusia hasil renderer. Kit ChatGPT/Gemini dan panduan audit tersedia pada [audit/README.md](audit/README.md).

**Aktif: edh001 r0003, format 2.1, lima shot dan tujuh JPEG.** Pengguna menyetujui keseluruhan snapshot; ZIP final diekspor tanpa render ulang dan di-ingest. Implementasi Overview/Storyboard selesai. Enam pilot lain belum mempunyai run terverifikasi dalam catatan pilot. [Plan terbaru](docs/implementation-plan-overview-storyboard.md), [PRD](docs/prd-overview-storyboard-cloning.md), [hasil dan status penerapan](docs/overview-storyboard-verification.md).

## Membaca referensi

- Manusia: [katalog](catalogs/README.md) → references/<id>/analysis.md. Format2.1 mempunyai enam bagian: Profil desain, Ukuran & proporsi, Shot Timeline, Overview, Storyboard dan Shot Details.
- AI: [indeks JSON](data/search-index.json) → identitas/shot/area terpilih → gambar yang diperlukan. [Kontrak reader 2.1](docs/contracts/ai-reader-v2-1.md) menjelaskan pointer dan akses tanpa MP4 untuk media tersimpan.
- [Knowledge](knowledge/README.md) mempertahankan status, negasi, label baru dan sumber; generator tidak menyimpulkan fakta dari prosa atau arsip.

Media2.1 berisi satu kolase per take kontinu, Overview satu baris dan Storyboard seluruh kolase vertikal. Kolase normal tiga panel; multi area dinamis dalam shot yang sama. Paragraf Overview menjelaskan posisi wide pada frame terpilih; Camera Start tetap awal sumber. Camera Pattern berasal dari klasifikasi arah fase, kamera/tempo tetap mengikuti sumber asli.

Paket 2.0 mempertahankan laporan lima bagian dan storyboard overview satu baris menurut renderer asalnya. Legacy 1.0/1.1 tetap berbasis MD dan media menurut kontrak masing-masing. Paket diterima tidak dikonversi atau ditulis ulang otomatis; satu MP4 kanonis per sumber berada di video/.

## Menambahkan ZIP final

1. Lampirkan MP4 asli dan [kit audit](audit/homeku-audit-kit.zip), lalu gunakan [prompt audit](audit/prompts/01-audit.md).
2. Koreksi hasil di chat sampai Overview, Storyboard, kolase semua shot dan MD lengkap sesuai. AI mengekspor byte snapshot yang sama setelah persetujuan keseluruhan.
3. Unduh satu ZIP final dan letakkan di incoming/ lokal.
4. Jalankan `python tools/library.py ingest incoming/<id>-rNNNN.zip` untuk paket tertentu, atau `python tools/library.py ingest` untuk semua ZIP di incoming/. Tidak ada watcher lokal atau review isi kedua setelah ingest.

Perubahan referensi diterima selalu melalui ZIP revisi eksplisit dengan supersedes yang tepat. Upload/push incoming/ pada branch utama juga dapat memicu Library ingest di GitHub Actions sesuai konfigurasi repo.

## Perintah lokal

Python 3.11+, FFmpeg/ffprobe dan dependensi requirements.txt diperlukan.

```sh
python tools/library.py validate incoming/<id>-r0001.zip
python tools/library.py ingest incoming/<id>-r0001.zip
python tools/library.py build
python tools/library.py search --area kitchen --tempo fast --limit 5
python tools/library.py read edh001 --part shot --shot shot-03
python tools/library.py panel edh001 s03-overview --output /tmp/kitchen.png
python tools/library.py shot-image edh001 shot-03 --output /tmp/kitchen-shot.jpg
python tools/library.py check
python -m unittest discover -s tests -t . -v
python tools/build_audit_kit.py --check
```

`shot-image ... --from-storyboard` mengambil blok lengkap dari Storyboard pada media 2.2.0. `panel --native` meminta MP4 secara eksplisit. Build --full melewati cache; --root /path/repo sebelum subperintah memilih root terisolasi. catalogs/, knowledge/, proyeksi dan indeks adalah hasil generator.

- [Kontrak paket 2.1](docs/contracts/package-v2-1.md), [laporan2.2.0](docs/contracts/analysis-v2-2.md), [field map](docs/v2-field-map.md).
- [Paket 2.0](docs/contracts/package-v2.md), [legacy](docs/contracts/package-v1.md), [membaca referensi](references/README.md), [operasi](docs/operations.md).
- [Alur konsep/DNA dan cloning](docs/alur-konsep-desain-v2.md), [kemampuan pustaka](docs/capability-map.md), [pilot](audit/pilots/README.md).

Referensi aktif hanya ID pada data/registry.json. Kandidat lokal, fixture, audit/result/ dan archive/oldrepo/ bukan input discovery/generator/knowledge. Pengujian teknis tidak membuktikan kebenaran audit visual atau penyelesaian pilot yang belum dijalankan.
