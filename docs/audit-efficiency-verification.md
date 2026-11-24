# Verifikasi implementasi audit efisien2.4

> Status setelah reset 24 November 2026: data audit edh001 telah dihapus atas permintaan pengguna. Catatan edh001 di dokumen ini bersifat historis, bukan referensi aktif atau persetujuan audit baru.

Tanggal23November2026. Mengikuti [plan](audit-efficiency-implementation-plan.md). Tahap1–7 tooling selesai; bagian teknis tahap8 (regresi/build/benchmark) selesai. Pilot2.4 ChatGPT/Gemini **belum dijalankan**, tetap tugas pengguna sesuai pembagian sebelumnya. Implementasi ini tidak mengaudit video baru atau mengesahkan/ingest hasil provider.

## Perubahan yang diterapkan

| Bagian | Hasil |
| --- | --- |
| Sumber/paket |2.4; audit.json satu sumber isi, manifest teknis, ZIP tanpa MP4/cache/log/receipt |
| Estimasi |~×/~° visual menerima asumsi wajar; piksel opsional. Gerakan jelas tetap memiliki angka, bagian ambigu memuat kendala/alternatif |
| Metadata |prepare/complete menghitung PTS, batas, midpoint, parser, summary dan log selected. Tidak membuat fakta/arah/tempo atau viewed otomatis |
| Pemeriksaan awal |check-input mengumpulkan error independen; draft wajib preflight sebelum JPEG. Validasi final tetap berlaku |
| Sampling |6FPS sekali/session, native sumber≤6FPS/shot<1s, pendalaman10/native terarah, frame tambahan dapat dipilih melalui indeks |
| Cache |Terikat sumber/stream/versi/parameter, hash diperiksa, symlink ditolak, kuota512MiB/bucket; bukan isi pustaka |
| Media |Frame kanonis sekali/frame unik; executor subset baru memakai engine/layout/font2.2.0 yang sama. JPEG diuji byte-identik |
| Laporan |Renderer/template2.2.3, struktur6bagian/A-B-C tetap, tanpa tabel pembuktian atau waktu |
| AI |Reader/index2.4, generator7; semua cabang lama/status/negasi/label/facet/pointer dipertahankan |
| Progres/log |Output pass CLI ringkas; performance.jsonl mencatat durasi alat/cache/retry. Log di workspace, bukan snapshot |
| Kit |4file input,78resource lokal berhash, helper/authoring/contoh normal+multi tersedia |

Sumber2.3 tetap pengukuran~× menurut kontraknya,2.2 tetap10FPS, seluruh format lama tidak dikonversi. Dokumen produksi bekerja/ tidak diubah. Contoh baru memakai test-pattern/fixture dan tidak masuk discovery/knowledge aktif.

## Pengujian nyata

- python -m unittest discover -s tests -t . -v: **190tes lulus,246.085detik** pada run lengkap terakhir.
- Sebelumnya31tes authoring/preflight/cache/efisiensi lulus36.612detik dan62tes kompatibilitas lulus85.717detik. Tiga regresi tambahan ikut run190tes: nilai estimasi invalid, sumber tak terbaca dan perubahan sumber saat decode.
- python tools/library.py build: lulus,1referensi/5shot. Perubahan hanya data/build.json, data/dependencies.json, data/projections/edh001.json dan data/search-index.json.
- python tools/library.py check: **ok**,1referensi/5shot.
- python tools/build_audit_kit.py --check: lulus, kit identik dengan builder.
- git diff --check: lulus.

34tes baru meliputi prepare/resume/viewed/complete normal+multi, midpoint tambahan tanpa pendalaman rutin, scope/konversi lama ditolak, estimasi visual dan pengukuran opsional, preflight banyak error/nol render input salah, sumber tak terbaca, cache korup/symlink/kuota/stream/source berubah, batch+kanonis, byte media frozen vs cache, invalidasi notasi/area/config, output tanpa cache/MP4, receipt usang, ingest/replay, seluruh pointer,300model dan pipeline CLI portable dari workspace kosong. Seluruh deklarasi viewed pada fixture adalah data sintetis, bukan pengamatan rumah.

## Benchmark lokal pada sumber edh058 yang sama

Sumber kanonis: video/edh058.mp4,19.9detik/597frame/30FPS, hash823be3ce9ee96fc07a6ab263010a09a3d60e72cfcf334ef2fbe5a38e7a550731.

Paket Gemini2.3 diekstrak dan dibaca di /tmp, tanpa mengonversi audit.json ke2.4. Kandidat benchmark purpose=fixture, dengan revisi metadata/kamera sintetis hanya untuk menguji dependensi. Mode cache opt-in memakai tooling yang sama dengan default2.4. Bukan audit visual baru, persetujuan atau ekspor/ingest produksi.

| Kasus | Waktu alat lokal | Decode frame kanonis baru | Gambar berubah dibanding baseline |
| --- | --- | --- | --- |
| Draft tanpa cache |23.361383s|Jalur asal24permintaan ekstraksi|Tidak ada |
| Draft cache awal |16.266798s|18frame unik|Tidak ada; seluruh8JPEG identik |
| Draft cache hangat |0.936628s|0|Tidak ada |
| Koreksi basis/metadata |0.934265s|0|Tidak ada |
| Koreksi notasi shot01 |1.405930s|0|Hanya shot01 dan Storyboard |
| check-input mode log invalid |0.022109s|0|Tidak membuat JPEG |

Pada run ini draft cache awal sekitar30.4% lebih cepat; pengulangan/koreksi metadata sekitar96% lebih cepat daripada jalur tanpa cache. Ini waktu helper lokal, **bukan** klaim audit AI28menit otomatis menjadi sejumlah menit tertentu. Cache/durasi diuji melalui operasi nyata; tes unit memakai jumlah operasi dan kesamaan byte, bukan ambang detik yang mudah fluktuatif.

Lokasi hasil teknis lokal:
- /tmp/homeku-efficiency-benchmark-2hlpmpj9/runs/benchmark.json
- /tmp/homeku-efficiency-benchmark-2hlpmpj9/prepare-benchmark.json

Prepare/resume diuji terpisah memakai cut dari paket2.3 terverifikasi, tanpa pengamatan baru:
-6shot,12pass (baseline+midpoint),132frame unik.
- Prepare8.094512s, satu batch FFmpeg, **0frame dinyatakan viewed**.
- Resume0.079723s, nol batch/decode tambahan, sumber pengamatan tidak ditimpa.
- Nilai waktunya pengukuran lingkungan lokal saat pengujian, bukan SLA provider.

Sampling batch tidak dipromosikan menjadi byte media final tanpa extractor kanonis; jalur media final mempertahankan byte lama sekali/frame, lalu cache. Optimasi ini mengurangi24permintaan berulang menjadi18decode unik pada cold draft dan0pada warm draft. Tidak mengganti implementasi media_v2_2.py yang terdaftar.

## Integritas dan artefak

Kit audit/homeku-audit-kit.zip: 928309byte, SHA-256:
77b9c850f2e8390759b88dc63981c631c6782a3dd1f6ea92f807fcaf1c2bc7ea

Referensi aktif tetap edh001 r0003/sumber2.1,5shot/7JPEG. Snapshot tetap:
e1572245a3cc3e88cac25409816694de5f021d2da83fbb248d5331baaee5501f

Seluruh hash referensi/video/font/layout/renderer-template lama/ZIP hasil provider/registry/ledger dibandingkan snapshot sebelum pekerjaan: **tidak ada perubahan**. Perubahan staged pengguna sebelumnya dipertahankan. Katalog/knowledge dibangun generator, bukan edit fakta manual; sumber aktif tidak dikonversi. Indeks baru versi2.4,47523byte.

Helper source2.4 dapat merender kandidat dari pengamatan baru; memasang tooling bukan menerima kandidat tersebut. Export tetap memvalidasi/mengemas byte snapshot disetujui, tanpa render ulang; cache boleh hilang saat ekspor.

## Pelaksanaan pilot berikutnya

Gunakan kit2.4 dan prompt01 pada chat baru masing-masing provider untuk edh058. Simpan run terpisah audit/result/<provider>/v2.4/run-NN/ agar hasil2.3 tetap utuh. Tinjau estimasi sudut/skala, arah/fase/tempo, detail desain/fakta, Camera Start/Overview, MD dan seluruh media. Koreksi di chat sebelum persetujuan keseluruhan dan ekspor. Semua moderate sah.

Catat waktu kandidat siap, error/retry dan durasi alat; pisahkan jeda persetujuan. Target pengurangan waktu keseluruhan sekitar30% masih perlu dibuktikan di lingkungan provider yang sebanding. Lebih cepat dengan detail hilang atau sudut dihapus kembali bukan hasil yang memenuhi tujuan. Lanjutkan lima pilot lain setelah alur memadai. Tidak ada pengujian manfaat melalui produksi konsep/gambar/video pada pekerjaan ini.

## Lanjutan kamera2.5 — 24 November 2026

Dua hasil edh058 sumber2.4 kini tersedia/diperiksa, MD serta8JPEG sesuai renderer; belum disetujui/di-ingest. Pemeriksaan visual tambahan hanya18frame, bukan audit seluruh baseline. Laporan waktu provider bukan benchmark terkontrol. Implementasi kamera2.5 melanjutkan plan audit-camera-implementation-plan.md; run2.5 pengguna belum dijalankan. Status historis di atas berlaku pada saat dicatat.
