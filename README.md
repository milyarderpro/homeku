# Pustaka HOMEKU

Pustaka referensi desain, komposisi dan gerakan kamera berbasis audit video. **Fondasi V2 tersedia:** audit.json sebagai sumber, laporan manusia otomatis, media kolase, ingest legacy/V2 serta pembaca AI bertahap. Tampilan 2.1.2 memakai judul/nama area tebal yang diperkecil 15%, header kolase cukup judul/rentang/durasi, dan caption Start/Middle/End dengan timestamp lebih kecil di bawah masing-masing foto. Storyboard memakai header gaya utama. Nama gaya memakai bahasa Inggris; penjelasan tetap bahasa Indonesia. Workflow/prompt dan kit chat V2 siap dipakai; audit ulang edh001 V2 sudah disetujui dan di-ingest sebagai r0002. [Status Tahap 2](docs/v2-stage-2-verification.md).

Koleksi aktif: **edh001 revisi 2, format 2.0, lima shot**. Snapshot V2 telah disetujui pengguna dan di-ingest; enam pilot pengguna belum dijalankan. Lihat [hasil verifikasi Tahap 1](docs/v2-stage-1-verification.md) dan [plan V2](docs/improvement-v2-plan.md).

## Membaca referensi

- Manusia: [katalog](catalogs/README.md) → references/<id>/analysis.md.
- AI: [indeks JSON](data/search-index.json) → identitas/shot terpilih → bukti/media yang diperlukan. [Kontrak pembaca 2.0](docs/contracts/ai-reader-v2.md) menjelaskan pencarian dan pembacaan sebagian.
- [Knowledge](knowledge/README.md) mempertahankan status, negasi dan sumber; tidak menyimpulkan fakta dari prosa atau arsip.

V2 memakai audit.json sebagai satu sumber yang ditulis auditor; analysis.md hanya laporan manusia dari renderer. Manifest menyimpan sumber/log/media teknis. Paket legacy 1.0/1.1 tetap dibaca dari MD menurut kontraknya sendiri, tanpa mengarang luas atau gaya baru.

## Menambahkan ZIP final

1. Audit dan koreksi video di chat sampai keseluruhan kandidat sesuai. Gunakan [panduan chat V2](audit/README.md), satu MP4 terpisah dan [kit audit](audit/homeku-audit-kit.zip).
2. Unduh satu ZIP final dan letakkan di incoming/ lokal.
3. Jalankan `python tools/library.py ingest` untuk memperbarui pustaka. Tidak ada watcher lokal atau proses otomatis hanya karena ZIP ditempel.
4. Lihat katalog/knowledge yang dibangun generator; tidak ada review isi kedua sesudah ingest.

Alternatif upload/push incoming/ pada branch utama memicu **Library ingest** di GitHub Actions. Paket gagal dicatat pada data/ingest.json; paket valid lain tetap diproses. Perbaikan isi referensi yang diterima selalu lewat ZIP revisi eksplisit.

Media V2: satu kolase per shot dan satu storyboard overview satu baris. Normal tiga panel awal/tengah/akhir; multi area dinamis mengikuti perjalanan. Tidak ada JPEG frame terpisah atau seluruh rangkaian frame. ZIP edh001 r0001 tetap disimpan sebagai riwayat; media aktif mengikuti r0002 yang telah disetujui. Satu MP4 kanonis per sumber berada pada video/.

## Perintah lokal

Python 3.11+, FFmpeg/ffprobe serta Pillow/jsonschema dari requirements.txt diperlukan.

```sh
python tools/library.py validate incoming/<id>-r0001.zip
python tools/library.py ingest
python tools/library.py build
python tools/library.py search --area kitchen --tempo fast --limit 5
python tools/library.py read edh001 --part shot --shot shot-03
python tools/library.py check
python -m unittest discover -s tests -t . -v
python tools/build_audit_kit.py --check
```

`build --full` melewati cache; `--root /path/repo` sebelum subperintah memilih root terisolasi. catalogs/, knowledge/, data/projections/ dan indeks adalah keluaran generator: jangan edit fakta turunan manual.

- [Kontrak paket V2](docs/contracts/package-v2.md), [laporan manusia](docs/contracts/analysis-v2.md), [pemetaan field](docs/v2-field-map.md).
- [Kontrak legacy](docs/contracts/package-v1.md), [membaca referensi](references/README.md), [operasi/revisi/retensi](docs/operations.md).
- [Alur konsep untuk AI](docs/alur-konsep-desain-v2.md), [kemampuan pustaka](docs/capability-map.md).

Referensi aktif hanya ID pada data/registry.json. archive/oldrepo/ bukan sumber discovery/generator/knowledge. Pengujian teknis tidak membuktikan kebenaran audit visual, kualitas konsep baru atau pelaksanaan pilot yang belum dijalankan.
