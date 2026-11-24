# Pustaka HOMEKU

HOMEKU menyimpan audit video desain, komposisi, dan gerakan kamera dalam format 3.0. `audit.json` menyimpan isi sumber, `analysis.md` menyajikan laporan manusia, dan `manifest.json` mencatat bukti serta media.

- Manusia mulai dari katalog, lalu membuka laporan referensi. [Katalog](catalogs/README.md)
- AI mulai dari indeks, lalu membaca identitas, shot, atau area yang dipilih. [Indeks](data/search-index.json) · [Kontrak reader](audit/contracts/reader.md)
- Perbandingan bentuk, susunan area, dan fakta desain tersedia bersama prinsip umum terkurasi. [Knowledge](knowledge/README.md)
- Gunakan referensi terpilih untuk mengembangkan desain, frame awal, dan gerakan yang sesuai. [Alur konsep dan produksi](audit/concept-workflow.md)

## Audit dan ingest

1. Lampirkan satu MP4 asli dan kit audit pada satu chat. Jalankan bootstrap dan ikuti prompt mulai. [Kit](audit/homeku-audit-kit.zip) · [Panduan audit](audit/README.md)
2. Koreksi dan tinjau laporan enam bagian, Overview, Storyboard, serta seluruh kolase. Setelah persetujuan keseluruhan terbaru, ekspor satu ZIP final tanpa video.
3. Simpan MP4 kanonis di `video/<id>.mp4` dan taruh ZIP di `incoming/`. Jalankan ingest untuk menerima revisi dan memperbarui turunan. Persetujuan isi terjadi di chat.

~~~sh
python tools/library.py ingest incoming/rumah-r0001.zip
python tools/library.py search --style "American Cottage" --scale tiny --area kitchen --limit 5
python tools/library.py read rumah --part shot --shot shot-01
python tools/library.py panel rumah s01-overview-01 --output /tmp/overview.png
~~~

Opsi `panel --native` memakai MP4 kanonis saat mengambil frame asli. `shot-image --from-storyboard` mengambil blok kolase dari Storyboard. [Cara membaca referensi](references/README.md)

Referensi aktif mengikuti `data/registry.json`. Katalog, Knowledge, proyeksi, dan indeks diperbarui oleh generator. Perubahan isi referensi diterima melalui ZIP revisi berurutan dan `supersedes` yang menunjuk snapshot aktif. [Kontrak paket](audit/contracts/package.md)

## Pengembangan

Gunakan Python 3.11+, FFmpeg/ffprobe, dan dependensi `requirements.txt`. Helper gerak 2D bersifat opsional dan memakai `requirements-audit-motion.txt`.

~~~sh
python -m unittest discover -s tests -t . -v
python tools/library.py build
python tools/library.py check
python tools/build_audit_kit.py --check
~~~

Untuk status hasil nyata, pilot dibedakan dari tes sintetis. [Pilot](audit/pilots/README.md)
