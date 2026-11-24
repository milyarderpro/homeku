# Pustaka HOMEKU

Pustaka referensi desain, komposisi dan gerakan kamera dari audit video. Workflow baru memakai **audit/paket 2.5**, laporan **2.2.4**, media **2.2.1** dan pembaca AI **2.5**. audit.json adalah sumber audit; analysis.md laporan manusia hasil renderer. Kit ChatGPT/Gemini dan panduan audit tersedia pada [audit/README.md](audit/README.md).

**Aktif: edh001 r0003, format 2.1, lima shot dan tujuh JPEG.** Pengguna menyetujui keseluruhan snapshot; ZIP final diekspor tanpa render ulang dan di-ingest. Implementasi Overview/Storyboard selesai. Dua hasil edh058 dari Gemini/ChatGPT sudah diterima untuk dibandingkan, belum disetujui atau di-ingest; lima pilot lainnya belum tercatat. [Implementasi kualitas audit](docs/audit-quality-verification.md), [plan Overview/Storyboard](docs/implementation-plan-overview-storyboard.md), [PRD](docs/prd-overview-storyboard-cloning.md), [hasil dan status penerapan](docs/overview-storyboard-verification.md).

## Membaca referensi

- Manusia: [katalog](catalogs/README.md) → references/<id>/analysis.md. Format2.1/2.2/2.3/2.4/2.5 mempunyai enam bagian: Profil desain, Ukuran & proporsi, Shot Timeline, Overview, Storyboard dan Shot Details.
- AI: [indeks JSON](data/search-index.json) → identitas/shot/area terpilih → gambar yang diperlukan. [Kontrak reader 2.5](docs/contracts/ai-reader-v2-5.md) menjelaskan pointer dan akses tanpa MP4 untuk media tersimpan.
- [Knowledge](knowledge/README.md) mempertahankan status, negasi, label baru dan sumber; generator tidak menyimpulkan fakta dari prosa atau arsip.

Media pada sumber2.1/2.2/2.3/2.4/2.5 berisi satu kolase per take kontinu, Overview satu baris dan Storyboard seluruh kolase vertikal. Kolase normal tiga panel; multi area dinamis dalam shot yang sama. Paragraf Overview menjelaskan posisi wide pada frame terpilih; Camera Start tetap awal sumber. Camera Pattern berasal dari klasifikasi arah fase, kamera/tempo tetap mengikuti sumber asli.

Paket 2.0 mempertahankan laporan lima bagian dan storyboard overview satu baris menurut renderer asalnya. Legacy 1.0/1.1 tetap berbasis MD dan media menurut kontrak masing-masing. Paket diterima tidak dikonversi atau ditulis ulang otomatis; satu MP4 kanonis per sumber berada di video/.

## Menambahkan ZIP final

1. Lampirkan MP4 asli dan [kit audit](audit/homeku-audit-kit.zip), lalu gunakan [prompt audit](audit/prompts/01-audit.md).
2. Koreksi hasil di chat sampai Overview, Storyboard, kolase semua shot dan MD lengkap sesuai. AI mengekspor byte snapshot yang sama setelah persetujuan keseluruhan.
3. Unduh satu ZIP final tanpa video dan letakkan di incoming/ lokal. MP4 asli tetap terpisah; pastikan tersedia di video/<id>.mp4 dengan hash yang sama.
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

- [Kontrak paket2.5](docs/contracts/package-v2-5.md), [laporan2.2.4](docs/contracts/analysis-v2-2-4.md), [field map](docs/v2-field-map.md).
- [Paket 2.0](docs/contracts/package-v2.md), [legacy](docs/contracts/package-v1.md), [membaca referensi](references/README.md), [operasi](docs/operations.md).
- [Alur konsep/DNA dan cloning](docs/alur-konsep-desain-v2.md), [kemampuan pustaka](docs/capability-map.md), [pilot](audit/pilots/README.md).

Referensi aktif hanya ID pada data/registry.json. Kandidat lokal, fixture, audit/result/ dan archive/oldrepo/ bukan input discovery/generator/knowledge. Pengujian teknis tidak membuktikan kebenaran audit visual atau penyelesaian pilot yang belum dijalankan.

Default audit baru6FPS, pendalaman10FPS/native sesuai pertanyaan visual; sumber≤6FPS atau shot<1detik seluruh native. Sumber2.2 tetap10FPS menurut kontraknya. Metode [pengamatan inti](audit/visual-audit.md), [plan](docs/audit-method-6fps-implementation-plan.md) dan [verifikasi metode](docs/audit-method-verification.md). Implementasi Reader2.3/generator6 sebelumnya menambah facet/pointer. Dua hasil pilot2.3 kini tersedia; default terbaru dijelaskan berikut.

Alur2.5 memakai [authoring](audit/authoring.md): prepare → amati/isi → deklarasi viewed → complete/check-input → draft/review → persetujuan keseluruhan → export. Estimasi kamera visual ~×/~° menerima asumsi wajar; pengukuran piksel opsional. Input diperiksa sebelum render; cache/log hanya di workspace, terpisah dari ZIP. Reader2.5/generator8 mendukung semua sumber lama. [Plan efisiensi](docs/audit-efficiency-implementation-plan.md), [verifikasi](docs/audit-efficiency-verification.md). Dua hasil pilot2.4 sudah diperiksa; pilot2.5 berikutnya dijalankan pengguna memakai kit terbaru.

## Default audit kamera2.5

Sumber2.5/report2.2.4/media2.2.1/reader2.5/generator8. Angka kamera opsional per komponen, termasuk medium/high; tidak perlu alasan khusus saat angka tidak ditulis. Estimate_basis cukup singkat bila berangka, boleh null bila tanpa angka. Baseline6FPS tetap; helper flow opsional/cache lokal, tanpa AI API. Kompatibilitas2.4 dan sebelumnya tetap kontrak asal, bukan default baru. Caption versi baru Start/Middle/End tebal dan waktu lebih kecil. Cache/session/flow/inventory kerja tidak masuk ZIP/knowledge; export byte sama tanpa render. Lihat docs/audit-camera-implementation-plan.md dan audit/authoring.md.
