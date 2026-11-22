# Pustaka HOMEKU

Pustaka referensi desain, komposisi dan gerakan kamera berbasis audit video. Laporan utama berada dalam Markdown; katalog dan knowledge dibangun otomatis dari data yang ditulis eksplisit dalam laporan.

**Phase 1:** fondasi dan tooling tersedia. **Phase 2:** perangkat audit chat dan helper ekspor tersedia; audit edh001 sudah disetujui dan diekspor sebagai ZIP final r0001, enam pilot berikutnya akan dijalankan pengguna di ChatGPT/Gemini. Format 1.1, profil DNA, JSON pembaca AI dan audit adaptif tersedia; paket final edh001 1.1 sudah masuk registry lokal sebagai 1 referensi/5 shot aktif. Kontrak masih provisional.

## Mencari referensi

Untuk AI: [indeks JSON](data/search-index.json) → `data/projections/<id>.json` terpilih → media dan knowledge yang relevan. JSON lengkap dihasilkan dari MD/manifest, tanpa perlu membaca ratusan MD. Lihat [kontrak pembaca AI](docs/contracts/ai-reader-v1.md). MD tetap sumber isi audit untuk manusia.

- [Katalog aktif](catalogs/README.md): ruang, desain, posisi kamera dan gerakan.
- [Knowledge dan perbandingan](knowledge/README.md): variasi beserta status dan sumbernya.
- [Cara membaca referensi](references/README.md).

Koleksi aktif hanya berasal dari registry. Video yang belum diaudit dan pustaka dalam `archive/oldrepo/` tidak dihitung.

## Menambahkan referensi

1. Ikuti [panduan audit chat](audit/README.md): lampirkan MP4 dan kit, periksa kartu shot bergambar dan MD lengkap bila diperlukan, lalu koreksi sampai sesuai.
2. Unduh satu ZIP final sesuai [kontrak paket](docs/contracts/package-v1.md).
3. Upload ZIP ke [incoming/](incoming/README.md) pada branch utama repo dan simpan perubahan.
4. Workflow **Library ingest** memvalidasi paket, memperbarui referensi/katalog/knowledge, lalu membuat satu commit hasil.

Upload adalah penyerahan audit final; tidak ada antrean review isi berikutnya. Jika paket gagal secara teknis, alasannya tercatat di `data/ingest.json` dan laporan Actions. Paket valid lain tetap diproses.

`analysis.md` menyimpan hasil audit lengkap. Setiap shot mempunyai `area-overview.jpg`, frame awal/tengah/akhir, dan tambahan detail/reveal bila perlu. Storyboard menggabungkan seluruh gambaran area. Video sumber disimpan satu kali di `video/`; tidak ada folder motion atau rangkaian seluruh frame dalam paket.

## Memelihara pustaka

Gunakan Python 3.11+ pada Linux, FFmpeg/ffprobe, serta dependensi dalam `requirements.txt`:

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python tools/library.py validate incoming/<id>-r0001.zip
.venv/bin/python tools/library.py ingest
.venv/bin/python tools/library.py build
.venv/bin/python tools/library.py check
.venv/bin/python -m unittest discover -s tests -t . -v
```

Perintah contoh memerlukan FFmpeg tersedia pada PATH. `build --full` melewati cache; `check` memvalidasi sumber aktif dan membandingkan hasil rebuild penuh. CLI `--root /path/repo` tersedia sebelum nama perintah untuk pengujian terisolasi.

- [Kontrak paket dan media](docs/contracts/package-v1.md)
- [Format laporan Markdown](docs/contracts/analysis-v1.md)
- [Pemetaan kemampuan lama dan sumber prinsip](docs/capability-map.md)
- [Operasi, revisi, retensi dan Actions](docs/operations.md)
- [Rencana implementasi](docs/implementation-plan.md)
- [Perangkat audit Gemini/ChatGPT](audit/README.md)

Workflow mulai berjalan setelah file implementasi dipush ke GitHub. Pengujian lokal tidak membuktikan izin Actions pada repo atau ketepatan audit visual; status audit nyata dicatat pada [pilot](audit/pilots/README.md).
