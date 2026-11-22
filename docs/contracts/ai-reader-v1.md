# Kontrak pembaca AI 1.0 — provisional

Mulai dari `data/search-index.json`, cocokkan label/alias melalui `data/taxonomy.json`, lalu muat hanya `data/projections/<id>.json` yang relevan, shot/media terkait dan `knowledge/principles.json` bila dibutuhkan. Koleksi aktif hanya registry. JSON adalah keluaran otomatis; tidak diedit terpisah.

## Referensi lengkap

[Schema referensi](reference-reader-v1.schema.json) memakai schema_version 1.0 dan kind homeku.reference. `reference` mempertahankan isi model MD: identitas, summary, profile beserta status/bukti, profile_notes, palette_notes, timeline_notes, coverage, shots, relations, limitations dan links; dilengkapi source, media, audit dan content_sha256 dari manifest/sumber validasi.

Setiap shot memuat design, review_summary, composition_notes, camera_notes, composition, facts, camera_summary, phases, uncertainty dan timeline. Komponen kamera menyimpan literal, jenis yang dikenali atau other, arah, qualifiers, estimates dan target. Unknown, label baru, negasi serta alternatif dalam narasi tidak dihapus. Bukti dalam reference tetap memakai path relatif MD.

`paths` memberi jalur dari root repo ke MD, manifest dan sumber. `provenance` memetakan JSON Pointer ke bagian MD dan bukti lengkap dengan jalur root, timestamp, hash, kind serta crop. Pointer fakta/phase/DNA mengidentifikasi klaim. Seluruh media tetap tercantum dalam reference.media, termasuk storyboard dan frame awal/akhir. Membaca JSON tidak mewajibkan membuka MD.

Tidak ada fingerprint/cache dalam kontrak pembaca. Metadata cache berada dalam data/build.json dengan fingerprint sumber/tooling dan hash proyeksi. Cache boleh dibuang, dan rebuild penuh harus setara. Format sumber legacy 1.0 tetap dipertahankan sebagai format_version 1.0: profile kosong dan profile_available false, tanpa menebak data yang tidak diaudit.

## Indeks ringan

[Schema indeks](search-index-v1.schema.json) memuat schema_version, kind, taxonomy, principles, knowledge dan references. Record referensi memuat id/title/revision/json, profile_available, profile_facets dan shots. Facet mempertahankan nilai asli, canonical alias bila tersedia, state/confidence dan pointer.

Facet DNA mencakup gaya/pengaruh, skala, tingkat, massa/atap, entrance/porch/bukaan, material/palet/cahaya/lingkungan, konfigurasi/pembeda/kontinuitas. Shot memuat fungsi asli/canonical, sudut, gerakan literal/ringkasan, jenis gerak, tempo dan pointer JSON/MD/media. Design_facets hanya atribut konfigurasi/bentuk/bukaan/sirkulasi utama; fakta lengkap dan narasi tetap dalam proyeksi terpilih, tidak diduplikasi seluruhnya dalam indeks.

Facet nonpositif bukan kecocokan positif. Not-visible berarti tidak terlihat, not-present berarti ketidakhadiran yang dinyatakan pada cakupan audit, uncertain adalah tafsir, unknown belum diketahui. Pencarian tidak menyimpulkan ketidakhadiran dari field yang tidak ada. Alias menyamakan istilah eksplisit, bukan menyimpulkan gaya dari paragraf. Label baru tetap tersedia.

## Knowledge

Knowledge perbandingan menyalin variasi fakta dengan status dan pointer sumber. Jalur knowledge pada indeks menuju knowledge/topics/index.json; setiap topik menunjuk index.json dan halaman JSON maksimal 40 klaim, dengan denominator serta sumber eksplisit. Prinsip umum berasal dari sources/design-principles.json, diterbitkan verbatim ke knowledge/principles.md dan JSON. Claim_type design-principle membedakannya dari observasi video dan keputusan konsep baru. Generator tidak menjalankan AI, membuat konsep, atau menggabungkan fakta arsip saat ingest.

Schema masih provisional sampai tujuh pilot selesai. Perubahan breaking memerlukan versi kontrak baru. Versi schema pembaca terpisah dari versi format MD dan versi generator.
