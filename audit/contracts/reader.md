# Kontrak pembaca AI HOMEKU 3.0

AI mulai dari data/search-index.json, memilih ID/shot sesuai kebutuhan, lalu memakai read untuk identity, shot, area atau full. Tampilan manusia ada di references/<id>/analysis.md; sumber isi tetap references/<id>/audit.json.

data/projections/<id>.json adalah keluaran generator: reference sumber ringkas, source metadata, paths, provenance, derived yang diperlukan dan evidence_inventory bersama. Jangan diedit manual. Pointer provenance menyebut `document` (audit atau manifest) dan `source_pointer`. Untuk turunan, `inputs` menyebut lokasi yang dibaca. Setiap JSON Pointer sumber harus dapat diresolusikan ke audit atau manifest dalam revisi/snapshot terkait. Turunan mempunyai input pointer eksplisit, bukan seolah fakta auditor.

Facet profil berasal dari design.styles/size/features. Fakta berasal dari kategori shot.design dan facet_roles yang dinyatakan. Label asli, domain khusus, state/negasi, confidence yang dinilai serta note dipertahankan. Field tidak diisi berarti tidak dinilai; tidak otomatis unknown, observed, high atau not-present. Prinsip kurasi bukan fakta video.

Filter mencakup gaya utama/pengaruh/interior, skala, area/fungsi, konfigurasi, rute satu shot kontinu, gerak/qualifier dan tempo. Filter konfigurasi bersama filter area memeriksa scope fakta pada area yang cocok. Taksonomi hanya alias terkurasi eksplisit; label baru tetap tersedia tanpa inference prosa. Indeks tidak menyalin seluruh prosa, checks kamera, log, cache atau statistik flow.

read/panel/shot-image memakai snapshot/proyeksi/media tersimpan tanpa MP4. PTS/bukti panel berasal dari frame map dan selections manifest; crop memakai bbox terdaftar. `--native` membutuhkan MP4 kanonis. Gunakan ID selection atau `F<indeks>` untuk bukti native di luar kolase. Build/check/ingest tetap memverifikasi MP4 kanonis/hash.

Referensi aktif hanya registry. Hasil pilot, fixture, cache, incoming belum diterima dan arsip bukan sumber discovery. Registry kosong tetap sah; full/incremental/replay dan penggantian revisi harus menghasilkan keluaran konsisten tanpa data usang.
