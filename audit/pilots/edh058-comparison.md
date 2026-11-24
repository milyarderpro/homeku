# Pembandingan pilot edh058

## Riwayat hasil2.0 sebelum perbaikan kualitas

Provider mengikuti keterangan pengguna. Dua ZIP hasil nyata sudah diberikan dan dibahas pada chat sebelum implementasi kualitas2.2. Pemeriksaan saat implementasi ini membaca metadata/isi paket, bukan audit ulang video. Kedua hasil belum disetujui sebagai referensi aktif dan belum di-ingest.

| Provider | File di audit/result/ | SHA-256 ZIP | Sumber / report | Shot | Fakta | Video dalam ZIP |
| --- | --- | --- | --- | --- | --- | --- |
| Gemini | edh058-r0001.zip | acde3acc02bb394055290804afcdbee428d7d36650bb15c7140b40afaadcf5c4 | 2.0 / 2.1.2 | 6 | 26 | Tidak |
| ChatGPT | edh058-r0001-HOMEKU-V2.zip | cf94cd3166e209d47f5b90af5f6bf3de7345888d4b62e3c977b90f0ff4404fd0 | 2.0 / 2.1.2 | 6 | 41 | Ada |

Temuan diskusi pilot yang mendorong perbaikan sistem:

- Gemini: label skala deskriptif tidak cocok pencarian small; detail cukup banyak namun ada klaim visual terlalu pasti.
- ChatGPT: pengaruh gaya digabung dalam satu nilai; source.mp4 ikut ZIP; nama file mengandung suffix tambahan. Suffix tidak dapat diatribusikan kepada model tanpa riwayat penamaan.
- Kedua hasil: perbedaan klasifikasi pan/orbit/truck dan tempo; kelengkapan fakta terstruktur tidak selalu mengikuti narasi. Jumlah fakta lebih banyak bukan bukti lebih benar.
- Status arah gabungan yang belum disepakati tetap terbuka. Jangan memakai salah satu output sebagai ground truth otomatis.

Format2.0/report2.1.2 adalah format saat pilot dibuat. Kedua paket dinilai menurut versinya; tidak dinyatakan melanggar aturan2.2 yang lahir kemudian. Implementasi2.2 menutup celah struktur MD, baseline, bukti fase, tempo, label, coverage dan video ZIP melalui kontrak/prompt/tooling. Tidak ada perubahan ke kedua ZIP.

Status pada pencatatan2.0: hasil tersedia; pembandingan sudah dibahas; temuan masih memerlukan audit/koreksi sumber dalam workflow baru sebelum persetujuan akhir. Tidak ada run pilot baru, persetujuan atau ingest yang disimpulkan dari tes fixture.

## Hasil2.2 terbaru dan dasar metode2.3

Dua ZIP lama2.0 di root audit/result/ kini tidak tersedia di working tree; nama/hash historis di atas dipertahankan. File pada subfolder gemini/gpt berikut adalah run berbeda, tidak menggantikan identitas byte historis.

| Provider menurut pengguna | File | SHA-256 ZIP | Byte | Sumber/report | Fakta |
| --- | --- | --- | --- | --- | --- |
| gemini | audit/result/gemini/edh058-r0001.zip | 6cb1751e50be26b5acf04ae6b163cf279e3f9d87477bf569c67e65522549f6ec | 11671353 | 2.2/2.2.1 | 35 |
| gpt | audit/result/gpt/edh058-r0001.zip | 2ddfe438798bdca759f7fbf21510199186b89c790f7aff0ec9e0f1719dc9fb9c | 11602839 | 2.2/2.2.1 | 50 |

Kedua hasil2.2 pernah lulus validasi teknis dan kesamaan renderer/media dalam pembandingan di chat. Pada audit visual sebelumnya,320frame unik diperiksa: baseline10FPS semua shot ditambah native seluruh shot02/06. Bukan seluruh597frame video. Pada implementasi metode2.3 ini hanya metadata ZIP dibaca kembali, tidak ada audit visual baru.

Temuan yang disepakati dalam diskusi:
- Gemini lebih lengkap pada gerak kedalaman: GPT shot02 hanya Pan Left dan shot06 hanya Pan Right, sehingga OUT terlewat. Ini dasar pemeriksaan depth sebelum Pan-only.
- Gemini memberi moderate semua enam shot. Pengguna menilai ini konsisten; label seragam bukan kesalahan. Perubahan skala proyeksi tidak membuktikan percepatan fisik.
- Rasio OUT lama berbeda konvensi (>1 vs<1). Sumber2.3 membakukan OUT=awal/akhir, dengan anchor utuh pada dua frame; tidak mengubah output2.2 yang tersimpan.
- Bentuk/detail konkret perlu diperiksa; hitungan35vs50fakta bukan skor akurasi. Label baru Gemini seperti opening-shape/massing-and-roof tetap utuh tetapi sebelumnya tidak masuk facet cepat; generator6 menambah mapping eksplisit.
- Pilihan orbit/truck gabungan dan nilai sudut/rasio bukan pose3D terkalibrasi. Hasil Gemini pembanding kuat sesuai preferensi pengguna, bukan ground truth seluruh paket.

Status: kedua ZIP2.2 tersedia/dibandingkan; belum disetujui keseluruhan atau di-ingest. Pilot2.3 dengan kit6FPS belum dijalankan pada ChatGPT/Gemini. Tidak ada konversi ZIP, persetujuan otomatis atau pengubahan referensi aktif.


## Pilot2.3 yang diberikan setelah evaluasi waktu

Kedua file pada result/gemini/ dan result/gpt/ kini memuat hasil2.3/report2.2.2, menggantikan berkas2.2 pada path yang sama. Hash2.2 terdahulu tetap riwayat; jangan mengklaim file lama masih tersedia dengan byte yang sama.

| Provider | SHA-256 ZIP2.3 | Fakta | Frame unik declared-viewed |
| --- | --- | --- | --- |
| gemini | 51962d120cc63600d0e5ba99403021c66c6ed85aac82221ab4e67c5e0c2e1556 | 47 | 145 |
| gpt | 20a80cbc48335ca035b693c30aabd7c3b75f341c47b913a2dd42f20a93cb1229 | 68 | 299 |

Kedua paket lulus validasi dan seluruh8JPEG identik renderer saat pemeriksaan read-only. Tambahan spotcheck12frame awal/akhir; bukan audit ulang seluruh597frame. Laporan proses masing-masing di result/<provider>/laporan.md. Gemini melaporkan8kegagalan validasi/3putaran sampling, dominasi waktu penulisan data dan perbaikan; GPT menambah10FPS seluruh6shot dan SIFT/RANSAC. Durasi provider bukan log alat mentah yang independen.

Pengguna menerima asumsi wajar pada estimasi sudut; estimasi visual tidak perlu kalibrasi. Ini menjadi kontrak2.4 untuk audit berikutnya, bukan perubahan terhadap paket2.3. Dua hasil tersedia/dibandingkan; penyerahan untuk evaluasi tidak dipakai sebagai instruksi ingest atau persetujuan kandidat lain.

Benchmark tooling2.4 memakai salinan kerja kontrak2.3 yang sama dalam /tmp dengan purpose=fixture dan revisi sintetis untuk uji cache. Bukan audit visual baru, tidak menulis ZIP asli atau sumber aktif. Angka/hasil di docs/audit-efficiency-verification.md. Run2.4 ChatGPT/Gemini belum dijalankan pada implementasi ini.
