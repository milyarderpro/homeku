# Pembaca AI 2.0

Indeks `data/search-index.json` dan `data/projections/<id>.json` memakai schema_version 2.0, termasuk ketika sumbernya legacy. Format sumber dicatat sebagai reference.format_version 1.0/1.1/2.0. Proyeksi dihasilkan deterministik, tidak diedit terpisah.

AI membaca indeks ringkas → identitas terpilih → shot/area → bukti yang dibutuhkan. [Alur konsep](../alur-konsep-desain-v2.md) menjelaskan penggunaan; konteks proyek/DNA lock tetap keputusan produksi di luar fakta pustaka.

## CLI lokal

```sh
python tools/library.py search --style 'american cottage' --scale small --limit 5
python tools/library.py search --tempo fast --area kitchen --limit 5
python tools/library.py search --configuration 'curved island' --limit 5
python tools/library.py search --route living kitchen --limit 5
python tools/library.py search --style cottage --style-relation family
python tools/library.py read <id>
python tools/library.py read <id> --part shot --shot shot-01
python tools/library.py read <id> --part area --shot shot-01 --area kitchen-1
python tools/library.py read <id> --part full
python tools/library.py panel <id> p-start --output /tmp/start.png
python tools/library.py panel <id> frame:shot-01:42 --native --output /tmp/frame.jpg
```

Contoh label/ID bukan klaim data aktif tersedia. --limit 1–50, default 10; --offset melanjutkan hasil dan next_offset menunjukkan halaman selanjutnya. Filter gaya default primary-style; --style-role style-influence/interior-style tersedia. Alias hanya ejaan setara. --style-relation family/blend/influence memperluas berdasarkan hubungan yang benar-benar dicatat auditor. Tanpa opsi tersebut family tidak otomatis menyamakan gaya. Uncertain tetap dapat ditemukan dengan status asli; --observed-only membatasi observed. Unknown/not-visible/not-present tidak menjadi kecocokan positif.

Filter area berulang dipenuhi dalam shot yang sama; fungsi laundry dalam satu bathroom tidak membuat dua area fisik. Filter route mencari urutan lintasan eksplisit dalam satu shot multi area. Beberapa cut yang kebetulan memiliki living dan kitchen tidak digabung menjadi rute. Sumber legacy tanpa model area fisik tidak dikarang menjadi multi area. Tempo memakai gabungan label fase dan setiap interval tempo_profile, sehingga moderate → fast tetap ditemukan melalui keduanya.

## Isi dan provenance

Envelope berisi schema_version/kind, reference lengkap, paths, provenance, evidence_inventory. `reference` mempertahankan semua bidang sumber berikut metadata source/media/audit teknis. `paths.audit` menunjuk audit.json untuk V2 dan null untuk legacy. Proyeksi tidak menyimpan fingerprint cache; data/build.json menyimpan hash proyeksi dan fingerprint generator/schema/template/font/taksonomi/prinsip.

`provenance` memakai JSON Pointer proyeksi, pointer sumber JSON untuk V2 dan anchor MD. Klaim merujuk evidence_ids; metadata bukti tersimpan sekali dalam evidence_inventory, bukan disalin penuh setiap klaim. Bukti panel mempunyai bbox foto dan PTS; bukti frame native tanpa panel menunjuk sumber MP4. Path sementara tidak diterbitkan. Path media pada inventaris relatif terhadap folder referensi yang ditunjuk paths.analysis; path video relatif terhadap root repo.

Read identity tidak mengirim seluruh log/media/shot. Read shot mengembalikan satu shot dan bukti terkait. Read area memfilter desain/fakta area tersebut **tetapi mempertahankan seluruh rute/fase kamera shot**, sehingga kontinuitas tidak dipotong menjadi shot baru. Panel diekstrak ke lokasi sementara di luar repo; crop tidak menyertakan caption, --native mengambil frame asli dari sumber dengan hash yang sesuai.

Indeks tidak membawa narasi desain, seluruh fakta, frame_reviews atau inventaris gambar. Facet konfigurasi memuat domain/subjek/atribut/nilai/status/pointer; profil tetap mempertahankan state/confidence. Tidak ada ekstraksi semantik dari MD V2, sintesis AI saat ingest, database atau embedding wajib.

Legacy dibaca eksplisit tanpa membuat estimasi luas/gaya/area baru. Generator membangun ulang koleksi campuran, sementara semua dokumen dan media paket yang diterima tetap byte-asli. Katalog/knowledge mempertahankan negasi, uncertainty dan label baru; denominator memakai pasangan referensi/shot unik yang mencatat atribut, bukan jumlah area/fase atau rumah independen.
