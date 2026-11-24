# Verifikasi implementasi audit kamera 2.5

Tanggal: 24 November 2026. Mengikuti [plan implementasi](audit-camera-implementation-plan.md). **Tahap 1–8 selesai; tahap 9 siap dijalankan pengguna di ChatGPT/Gemini, belum dijalankan.**

Implementasi ini tidak melakukan audit visual ulang edh058, tidak mengesahkan sepuluh studi kasus, dan tidak menerima/mengekspor/meng-ingest referensi produksi baru. Pengujian paket lengkap memakai fixture terisolasi.

## 1. Hasil implementasi

| Bagian | Hasil |
| --- | --- |
| Versi | Sumber/paket2.5, report/template2.2.4, media2.2.1, reader/index2.5, generator8 |
| Angka kamera | Opsional per komponen, termasuk medium/high; estimate_basis boleh null tanpa angka; angka tunggal default, rentang boleh |
| Notasi | Seluruh sepuluh contoh eksperimen dan variasi tanpa angka lulus; Straight/Diagonal/Pure/Mild/Subtle/Moderate/Strong serta easing dipertahankan |
| Tempo | Intensitas Pan tidak menambah tempo; easing tetap pada komponen terkait, fase gabungan boleh variable |
| Authoring | Normalisasi sumber kerja x/koma desimal tanpa mengubah nilai; parser sama untuk complete/preflight/model; source/session harus versi sama |
| Batch | Maksimal32frame per ekspresi; bounded split pada masalah ekspresi relevan, cache parsial/resume; bukan retry semua error |
| Helper | motion-hints opsional, ≤64frame dan width≤640; default32frame/320px, tanpa verdict, tanpa AI API, tidak menulis audit/viewed |
| Cache helper | Hash sumber/PTS/parameter/kode/backend, receipt hash, symlink ditolak, kuota32MiB; cache frame tetap512MiB/bucket |
| Fakta | Pemeriksaan duplikasi identik, coverage/area/evidence/facet; ringkasan kerja review terpisah. Tidak ada kuota fakta atau inferensi fakta dari narasi |
| Media | Caption label tebal dan waktu lebih kecil di bawah panel; Start/Middle/End, multi dinamis, Overview satu baris/Storyboard vertikal |
| Pembaca AI | Filter --movement/--camera-qualifier; qualifier eksplisit dan pointer/status/literal terjaga; indeks tidak memuat statistik kerja |
| Kit | Empat input,90resource berhash; dependensi inti tetap Pillow/jsonschema/FFmpeg |
| Snapshot | Review mengikat seluruh kandidat; ekspor byte sama tanpa render ulang; ZIP tanpa MP4/cache/log/receipt/inventory kerja |

Sumber2.4 tetap aturan angka asal,2.3 tetap pengukuran ~× dan2.2 tetap baseline10FPS. Baseline baru tetap6FPS/native; tidak turun menjadi6–10frame per shot. Font dan implementasi media/report/template/layout lama tidak diubah.

## 2. Pengujian nyata

Run akhir lengkap pada Python3.12, lingkungan /tmp/homeku-motion-env:

~~~sh
python -m unittest discover -s tests -t . -v
~~~

**214 tes lulus dalam240.629detik, tanpa skip.** Log: /tmp/homeku-camera-final-tests.log. OpenCV4.14.0 dan NumPy2.5.5 diuji nyata di lingkungan terpisah; FFmpeg6.1.1-3ubuntu5.

- Sembilan tes notasi mencakup sepuluh studi kasus dan variasi tambahan, confidence high tanpa angka, dua desimal, angka invalid, easing per komponen, parsed tampering dan kompatibilitas2.4.
- Sembilan tes workflow2.5 mencakup source→prepare/viewed/complete/preflight→draft/review→export/ingest/replay fixture, filter qualifier, no-video, no-render invalid, golden MD, normal/multi, cache/subset/full byte-parity dan kit portable.
- Enam tes helper/fallback mencakup transformasi sintetis diketahui, Δt native, tekstur kosong, cache statistik, batas kerja, missing dependency dan tidak mengubah audit/viewed. Empat di antaranya memakai OpenCV nyata.
- Tes lama tetap menguji source kontrak asal; assertion reader/default kit mengikuti2.5. Core tanpa OpenCV juga menjalankan pipeline portable; empat tes OpenCV dilewati pada run core tersebut, lalu semuanya berjalan pada run akhir di atas.
- Temuan integrasi awal pada enum sumber indeks dan target mock preflight sudah diperbaiki; run akhir lengkap lulus.
- Dua sumber provider2.4 tetap utuh; validasi/provenance lama tetap didukung.

Checks akhir: build, library check, kit --check, dan git diff --check lulus. Tidak perlu menjalankan suite kembali hanya untuk perubahan catatan verifikasi ini.

## 3. Performa dan biaya pemrosesan

Benchmark teknis memakai MP4 kanonis edh058 yang sama,19.9detik/597frame/30FPS. JSON provider disalin **secara eksplisit menjadi fixture teknis sementara2.5**, dengan purpose=fixture serta penanda bukan audit visual baru. ZIP provider tidak diubah dan fixture tidak masuk registry.

Hasil lokal di /tmp/homeku-camera-bench-ktlla1x9:

| Operasi | Waktu nyata | Operasi ulang / hasil |
| --- | --- | --- |
| Draft tanpa cache |26.375905s|Baseline delapan JPEG media2.2.1 |
| Draft cache awal |17.891823s|18decode kanonis; seluruh JPEG identik dengan baseline |
| Draft cache hangat |0.860125s|0decode baru; JPEG identik |
| Koreksi metadata |0.868975s|0decode baru; tidak ada JPEG berubah |
| Koreksi notasi shot01 |1.348147s|0decode baru; hanya shot01 dan Storyboard berubah |
| Prepare132frame |11.487833s|5batch FFmpeg;0retry pada lingkungan ini |
| Resume |0.082025s|0batch/decode tambahan |
| Helper shot02 pertama |0.670337s|Statistik lokal tanpa pengambilan keputusan |
| Helper ulang |0.080402s|Cache statistik digunakan |

Prepare memilih132frame; **nol frame dinyatakan viewed** pada benchmark. Helper off tidak dipanggil. Hasil render di renders/benchmark.json; sampling/helper di sampling/sampling-benchmark.json. Waktu ini pengukuran lokal, bukan SLA atau klaim durasi audit provider. Guard retry dan kuota helper juga diperiksa pada run tes akhir.

Tidak ada pemanggilan API AI dari tooling. Helper tidak wajib; OpenCV/NumPy tidak masuk requirements.txt inti atau payload biner kit. Dependensi opsional dipasang sekali di lingkungan pengujian; CI memakai cache kedua file requirements dan menguji core sebelum memasang paket opsional.

Batch32 memakai beberapa decode scan pada prepare pertama agar ekspresi aman; ini biaya lokal sekali yang ditukar dengan pemulihan otomatis lintas lingkungan. FFmpeg5.1 **belum diuji langsung** pada host ini. Kegagalan parser disimulasikan sampai batch≤8 dengan132frame; retry bounded berhasil, cache digunakan ulang, permission error fail-fast. Tidak mengklaim simulasi sebagai run Gemini/FFmpeg5.1 nyata.

## 4. Kapasitas dan tampilan

Uji terpisah300model/300shot campuran2.4+2.5: **2,080,412byte indeks**, seluruh schema/proyeksi dibangun; statistik/cache/log/pengukuran lengkap tidak masuk indeks. Artefak: /tmp/homeku-camera-capacity-s94vbu06/capacity.json. Ini fixture kapasitas, bukan300referensi aktif.

Preview diperiksa visual:
- Normal: /tmp/homeku-camera-bench-ktlla1x9/renders/baseline/edh058/media/shot-03.jpg.
- Multi area sintetis: /tmp/homeku-camera-multi-preview-e0o34plk/media-preview/media/shot-01.jpg.

Label/timestamp berada di bawah, label bold/waktu lebih kecil. Label reveal panjang membungkus tanpa menabrak panel/teks kamera; multi tidak dipaksa lima panel. Header/identitas/font dan bar hitam bawaan sumber dipertahankan. Fixture test-pattern bukan audit rumah.

## 5. Integritas dan artefak penyerahan

Kit audit/homeku-audit-kit.zip: **950817byte**, empat file input,90resource.
SHA-256: **dceb06648111c84610e4197e0bffb4efe074e350f35f6168fa977c31ba95bee4**.

Dibanding kit2.4 terakhir928309byte, kenaikan sekitar2.4%; dependensi OpenCV/NumPy tidak dibundel. Kit dibangun melalui builder resmi, bukan edit ZIP manual.

Snapshot sebelum pekerjaan menyimpan143hash artefak lama: referensi/video, schema lama, engine/report/template/layout/font lama, hasil provider, registry dan panduan eksperimen. **Tidak ada hash berubah.** Ledger data/ingest.json juga tidak berubah menurut diff Git. edh001 tetap r0003/sumber2.1,5shot/7JPEG, snapshot:
e1572245a3cc3e88cac25409816694de5f021d2da83fbb248d5331baaee5501f.

Build hanya memperbarui data/build.json, data/dependencies.json, data/projections/edh001.json dan data/search-index.json; bukan mengonversi isi referensi.

File pada plan yang tidak memerlukan edit: tools/homeku/video.py, engine.py, camera_pattern.py dan report_validation.py sudah memakai dispatch/data yang sesuai; audit/template-audit-info.json tidak memiliki default versi yang perlu diubah. data/taxonomy.json dan sources/fact-facets.json tidak membutuhkan alias/inferensi baru. Inventory kerja diletakkan dalam fungsi audit_quality.py dan output review terpisah; tidak menambah sumber audit kedua.

## 6. Tahap 9 — pilot pengguna

Gunakan MP4 edh058 + kit baru di chat baru ChatGPT/Gemini, lalu prompt01. Simpan run di audit/result/<provider>/v2.5/run-NN/; hasil2.4 jangan ditimpa. Koreksi semua kamera/desain/MD/media di chat sebelum persetujuan keseluruhan dan ekspor.

Periksa apakah gerakan gabungan/fase lebih tepat, angka dapat dihilangkan per komponen tanpa penalti, detail desain masuk fakta, ekstraksi tidak memerlukan patch, caption rapi dan alur tetap ringan. Catat waktu sampai kandidat siap terpisah dari persetujuan/ekspor. Setelah memadai lanjutkan edh013, edh033, edh049, edh056 dan dreamshome01.

**Run provider2.5, persetujuan, ekspor dan ingest baru belum terjadi.** Pengujian teknis dan preview bukan bukti audit kamera hampir sempurna; ketepatan visual tetap dinilai melalui hasil pilot nyata.
