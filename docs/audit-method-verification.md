# Verifikasi metode audit6FPS / sumber2.3

> Status setelah reset 24 November 2026: data audit edh001 telah dihapus atas permintaan pengguna. Catatan edh001 di dokumen ini bersifat historis, bukan referensi aktif atau persetujuan audit baru.

Tanggal23November2026. Implementasi mengikuti [plan](audit-method-6fps-implementation-plan.md). Tahap1–7 tooling selesai; tahap8 run provider disiapkan dan belum dijalankan. Tidak ada audit visual baru, persetujuan kandidat, ekspor referensi nyata atau ingest pada pekerjaan ini.

## Hasil penerapan

| Bagian | Hasil |
| --- | --- |
| Metode | audit/visual-audit.md: perjalanan utuh → depth → translation → rotation → gabungan/fase → estimasi → tempo, matriks tiga tes dan kalibrasi edh058 |
| Sumber/paket |2.3; audit.json satu sumber, manifest teknis; ZIP tanpa MP4/frame kerja/receipt |
| Sampling | Default6FPS + awal/akhir native; sumber≤6FPS dan shot<1detik seluruh native; pendalaman10FPS/native sesuai pertanyaan |
| Kompatibilitas |2.2 tetap10FPS/report2.2.1;1.0/1.1/2.0/2.1 tetap aturan asal |
| Pemeriksaan | camera_checks semua fase, dua frame fisik berbeda, interval/toleransi native, evidence fase/viewed; keputusan tetap depth_direction/components |
| Estimasi | scale_measurement untuk ~×, piksel positif/finite, kronologi/dimensi, IN=akhir/awal dan OUT=awal/akhir; pembulatan/rentang dan alasan angka yang belum terpisahkan |
| Tempo | Semua moderate sah; urutan accelerating/decelerating tidak bertentangan dengan label tempo yang diketahui |
| Laporan | Renderer/template2.2.2; enam bagian dan A/B/C sama, tanpa tabel checks/pengukuran baru |
| Media | Tetap2.2.0 dengan layout/font diterima; normal3panel, multi dinamis, Overview satu baris dan Storyboard vertikal |
| AI | Reader/index2.3, generator6; facet_roles2.3 eksplisit, label lama memakai sources/fact-facets.json dan role_source |
| Label baru | Tetap proyeksi/knowledge/topics; atribut lama belum dipetakan masuk dependencies.unmapped_fact_attributes |
| Kit | Empat file input;61resource lokal berhash termasuk panduan sesuai tahap; bootstrap tanpa jaringan |

## Pengujian yang benar-benar dijalankan

- python -m unittest discover -s tests -t . -v: **156tes lulus**,207.085detik pada run terakhir. Sebelumnya34tes metode/kualitas lulus; ekspektasi tes default lama diperbarui agar short take memakai native dan2.2 tetap diuji eksplisit.
- python tools/library.py build: **lulus**,1referensi/5shot. Keluaran berubah hanya data/build.json, data/dependencies.json, data/projections/edh001.json dan data/search-index.json. Katalog/knowledge tetap dihasilkan generator; byte isinya tidak berubah.
- python tools/library.py check: **ok**,1referensi/5shot.
- python tools/build_audit_kit.py --check: **lulus**, sama persis dengan builder.
- git diff --check: **lulus**.

17tes baru mencakup sampling6/3/native/VFR, sumber rendah/shot pendek/batas/gap, kebijakan2.2, checks hilang/sama frame/salah fase/unviewed, Pan/Static/Zoom/Uncertain/gabungan, rasio IN/OUT dan pengukuran salah, atribusi Dolly+Zoom, enam shot moderate, konflik percepatan, golden MD normal/multi, snapshot ekspor/replay ingest, campuran legacy, pointer/facet/negasi/unknown, fingerprint mapping,300model serta pipeline2.3 pada workspace kit kosong.

Fixture hanya data sintetis di root terisolasi, bukan referensi aktif atau bukti pemahaman video rumah. Uji300model mempertahankan indeks di bawah4MB untuk fixture tersebut dan tanpa checks/log/pengukuran lengkap; bukan jaminan ukuran semua koleksi nyata.

## Artefak dan integritas

Kit: audit/homeku-audit-kit.zip, **887353byte**, SHA-256:
e8f118e022ee4ecdefa5560d96cf2c8a3d5e390bb07ee78117c49619bc2c6a5a

README pintu masuk kit165kata sebelum inventory; panduan tidak lagi digabung menjadi satu instruksi panjang. Bootstrap diuji memulihkan setiap resource dengan byte yang sama dan menolak overwrite file berbeda.

Indeks aktif:2.3,47523byte,39facet desain;15atribut belum dipetakan tercatat diagnostik, dengan fakta asli tetap tersedia. Proyeksi berubah sebagai keluaran generator; sumber audit aktif tetap2.1.

Referensi aktif **edh001 r0003**,5shot/7JPEG, snapshot:
e1572245a3cc3e88cac25409816694de5f021d2da83fbb248d5331baaee5501f

Registry SHA-256:
07c2aedeec2368235e6a5bc53081a7cfeba80718cade57754f0299df3bc4ceae

Ledger ingest SHA-256:
854390fc556731463d9289428245b99fd18a1c2f4cf5c1a7581587d87c363eda

Referensi/registry/ledger, renderer2.2.1/template, implementasi media2.2.0/layout/font tidak diedit; dokumen/sumber terpilih juga dibandingkan byte dengan index Git awal dan sama. Semua sumber diterima lulus check penuh. Bekerja/, video dan ZIP pilot tidak ditulis ulang. Perubahan staged sebelumnya milik pengguna tetap dipertahankan.

## Status pilot dan batas hasil

Dua hasil edh058 terbaru di result/gemini/ dan result/gpt/ adalah sumber2.2/report2.2.1; metadata/hashes dibaca kembali dan catatan dibandingkan dengan riwayat2.0, tanpa konversi ZIP atau audit visual baru. Pengguna memilih gerakan Gemini sebagai pembanding kuat dan menilai enam moderate konsisten. Kedua hasil belum disetujui keseluruhan atau di-ingest.

[Urutan pilot2.3](../audit/pilots/README.md#pilot-metode23--disiapkan-belum-dijalankan) sudah tersedia: chat baru edh058 dengan kit baru di ChatGPT/Gemini, koreksi seluruh kandidat, ekspor byte identik tanpa MP4, simpan run terpisah; kemudian lima pilot lain. Pembagian tetap pengguna menjalankan enam pilot tersisa, asisten menyiapkan/membandingkan hasil yang dikembalikan. Run2.3, persetujuan, ekspor dan ingest menunggu pelaksanaan nyata.

Validator memeriksa field/pointer/interval/angka/snapshot, tidak memastikan objek ukur utuh atau klasifikasi gerak benar dari gambar. Perbaikan akurasi visual perlu dibuktikan pada pilot; berkurangnya FPS, catatan lengkap atau156tes lulus tidak menggantikan pengamatan nyata.

## Lanjutan sesudah hasil pilot2.3 tersedia

Pada diskusi berikutnya pengguna telah memberikan dua hasil2.3 edh058 beserta laporan proses. Kedua paket lulus pemeriksaan teknis dan reproduksi JPEG; status “belum ada run2.3” pada catatan sebelumnya berlaku saat implementasi itu selesai. Hash terbaru dan status pada audit/pilots/edh058-comparison.md. Paket asli tidak dikonversi atau di-ingest oleh evaluasi ini. Perbaikan efisiensi berikutnya memakai kontrak2.4 menurut docs/audit-efficiency-implementation-plan.md; pengujian historis di dokumen ini tetap dicatat apa adanya.
