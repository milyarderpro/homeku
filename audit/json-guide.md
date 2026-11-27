# Pengisian audit.json HOMEKU 3.1

Gunakan [panduan kamera](visual-audit.md) pada fase 2 dan [panduan desain](design-audit.md) pada fase 3. Satu audit.json ringkas adalah sumber final untuk laporan dan AI. Template belum valid sebelum placeholder/area/pilihan bukti/narasi diisi auditor. Prepare dan complete hanya membantu pekerjaan mekanis.

## Kelompok isi

| Field | Isi auditor |
| --- | --- |
| id / revision | Stem MP4 kanonis dan revisi; sumber baru r0001 |
| design.name | Nama desain deskriptif |
| design.house_type | Satu tipe dalam bahasa Inggris dengan value, state dan evidence |
| design.palette | Warna utama dengan value (nama warna), role, hex, state dan evidence per warna |
| design.styles | primary satu klaim; influences/interior daftar klaim diskret, nama Inggris |
| design.size | scale, levels, footprint, proportions; floor_area_m2 min/max positif wajib |
| design.features | Aspek DNA yang dinyatakan; tanpa 17 placeholder wajib |
| areas | ID ruang fisik, label Inggris Title Case, fungsi Inggris eksplisit dan visible_intervals presisi |
| shots | Satu take sampai cut; bukan satu area |
| shots.design | Scope area dan architecture/furnishings/environment: text + facts |
| shots.composition | Posisi/arah/angle/tinggi/tilt awal; framing/fokus/lighting/depth/reveal |
| shots.camera | description Indonesia, phases dan tempo; journey bila menambah penjelasan |
| panels / overviews | frame_index native dan area_ids; Overview memiliki composition_summary |
| route / area_relations / relations / notes | Hanya hubungan/rute/batas yang benar-benar dinyatakan |

## Klaim dan fakta

Klaim minimal: value, state, evidence. State eksplisit observed, uncertain, not-visible, not-present, unknown. Evidence berupa daftar indeks frame native global sumber, misalnya [142,195,248]. Confidence/note opsional, tidak ada default observed/high. Unknown dapat tanpa bukti; klaim lain perlu bukti sesuai scope. Tidak terlihat bukan tidak ada.

Fakta menambahkan subject dan attribute; facet_roles eksplisit untuk struktur seperti opening, roof, massing, layout, configuration, circulation. Domain khusus dan area_ids override dipertahankan bila diperlukan. Kategori/area kontainer mengikat scope; override tidak boleh keluar dari kontainer. Bukti satu kategori tidak otomatis membuktikan seluruh fakta. Gunakan state terpisah bila objek terlihat tetapi tipe atau hubungannya belum jelas. Lihat [contoh gaya dan layout](design-audit.md#profil-dan-detail-per-area).

Tulis text manusia secara ringkas dengan ciri pembeda di awal. Gunakan `composition_summary` untuk posisi kamera, arah pandang dan cakupan wide. Uraikan detail arsitektur, furnitur dan lingkungan di `shots.design`. Facts menyimpan informasi yang diperlukan discovery. Tidak ada kuota jumlah fakta, fact_coverage paralel atau generator yang menebak fakta dari paragraf.

## Mengisi satu fase atau fakta

Gunakan `edit-record` pada audit kerja untuk menambah satu entri atau mengoreksi field yang dipilih. Tanpa `--record-index`, file patch harus berisi satu entri yang lengkap. Untuk koreksi, pilih indeks mulai dari nol dan sertakan field yang ingin diubah. Saat membaca audit kerja untuk memilih indeks entri atau blok desain, catat SHA-256 dari byte JSON yang sama sebagai `AUDIT_SHA256`. Jika hash sudah berubah, baca ulang audit dan pastikan indeks masih menunjuk ke entri yang benar. Field lain pada entri yang sama tetap dipakai dari audit kerja.

Contoh koreksi notasi fase pertama yang bukti dan observasinya sudah terisi. Simpan objek seperti `{"notation":"Dolly-In (~1.5×)"}` di `work/fase.json` dan sesuaikan dengan pengamatan.

~~~sh
python tools/audit.py edit-record work/audit/session.json --shot-id shot-02 --kind phase --record-index 0 --expect-audit-sha256 "$AUDIT_SHA256" --patch work/fase.json
python tools/audit.py check-camera work/audit/session.json --shot-id shot-02
~~~

Untuk menambah fakta, beri scope area pada blok desain lalu simpan satu objek fakta yang memuat `subject`, `attribute`, `value`, `state`, dan `evidence`. Contoh ini menambahkan entri ke kategori arsitektur pada blok desain pertama.

~~~sh
python tools/audit.py edit-record work/audit/session.json --shot-id shot-02 --kind fact --block-index 0 --category architecture --expect-audit-sha256 "$AUDIT_SHA256" --patch work/fakta.json
~~~

Keluaran mencantumkan `source_pointer` entri serta `camera_recheck_required` bila perubahan membuat pemeriksaan kamera sebelumnya usang. Periksa frame terkait dan ulangi `check-camera --shot-id` untuk shot itu. `update-shot` tersedia untuk perubahan beberapa field shot sekaligus.

## Profil Desain

Pilih tipe rumah yang paling sesuai dari frame. Gunakan `uncertain` untuk perkiraan yang wajar, atau `value: null` dan `state: unknown` jika tipe tidak dapat diperkirakan. Tipe di luar daftar contoh tetap sah.

Untuk palet, isi `hex` dengan enam digit seperti `#F0E8DA`. Gunakan `role` seperti Dominan, Pendamping atau Aksen. Targetkan 4–6 warna yang mewakili rumah dan cantumkan bukti frame per warna. Simpan daftar di `design.palette`.

Gunakan `spatial-configuration` untuk susunan ruang utama, `material-hierarchy` untuk material, `lighting` untuk kondisi cahaya, `atmosphere` untuk kesan visual dalam satu kalimat, serta `environment` untuk lingkungan fisik.

## Kamera

Fase memiliki start_s/end_s, notation, depth_direction, focus, evidence temporal dan observations depth/translation/rotation. Tulis pengamatan singkat spesifik interval; evidence bersama tidak disalin tiga kali. Isi override per komponen jika bukti atau ambiguitasnya berbeda. Saat urutan komponen yang memakai override berubah, sertakan array `overrides` dengan indeks baru yang sesuai dengan gerak dan bukti masing-masing.

Notation memakai + simultan; → hanya pada summary turunan antar fase. Nilai besaran tiap komponen dan tulis estimasi ~× atau ~° yang dapat dibuat secara wajar dari frame. Angka tunggal dan rentang sama-sama sah. Estimasi tetap di `notation`. Lihat [panduan visual](visual-audit.md#arah-notasi-dan-tempo).

Depth_direction IN/OUT/NO IN/OUT/null ambigu adalah keputusan auditor, bukan hasil tebak dari zoom/skala global. ~× adalah perubahan skala gambar, bukan tempo. Semua moderate sah.

Tempo hanya satu sumber: label+description jika seragam; segments bertimestamp+description bila berubah. Batas tempo boleh berbeda dari fase. Easing/intensitas komponen bukan tempo. Jangan menambahkan phase.tempo atau camera_summary/components_parsed ke audit.

## Seleksi dan metadata

Satu `areas[].label` menamai satu area fisik. Gunakan `Bathroom & Laundry` untuk dua fungsi dalam satu ruang dan catat kedua fungsi di `areas[].functions`. Tulis `Open-Plan Living` dan `Sleeping Loft` sebagai dua label pada ID berbeda. Renderer menggabungkan kedua label dengan ` / ` pada judul shot. Gunakan padanan Inggris untuk nilai teknis yang dipakai filter dan bahasa Indonesia untuk narasi.

Untuk shot biasa, pilih frame jernih pertama sebagai `Start` dan frame jernih terakhir sebagai `End`. Hitung midpoint dari batas shot sumber dengan `(start_s + end_s) / 2`. Untuk panel `Middle`, pilih frame native jernih dengan PTS paling dekat ke midpoint tersebut. Batasi pilihan frame `Middle` pada rentang panel `Start` sampai `End`. Hindari transition blur, motion blur berlebihan, dan artefak transisi. Isi `panels[].frame_index` dengan indeks native yang sudah dilihat. Jika Production Start dipilih, gunakan indeks yang sama sebagai panel Start. Batas native, durasi, fase, dan notasi kamera mengikuti sumber.

Multi-area memakai jumlah panel yang sesuai dengan momen visual, dengan awal dan akhir wajib. Isi `panels[].label` pada momen antara yang bisa dinamai, misalnya `Living & Kitchen` atau `Doorway`. Overview dipilih untuk gambaran area lengkap, biasanya awal IN/akhir OUT; paragrafnya menjelaskan frame itu, Camera Start tetap awal sumber.

Jika transisi mengaburkan awal shot, simpan frame jernih pertama yang layak di `shots[].composition.production_start`. Isi `frame_index` native dan `composition_summary` satu paragraf tentang posisi, arah, dan framing. Frame harus berada setelah Start native dalam shot yang sama dan tercatat viewed. Untuk awal yang jernih, biarkan field ini absen dan gunakan Start biasa. Jika belum ada acuan jernih, catat keterbatasan di `notes`. Panel, Overview, dan Camera Start mengikuti sumber.

ID selection, shot_id, PTS, duration, parsed/summary/pattern dan coverage mekanis dihitung saat diperlukan atau disimpan teknis sekali dalam manifest. Tidak disisipkan kembali ke audit ringkas. Tidak menyimpan seluruh frame video.

## Provenance proses

audit-info hanya method, limitations, provider/model yang diketahui, reviewed_ranges dan frame_reviews yang benar-benar dideklarasikan. Model build tidak diketahui null. Gunakan mark-viewed hanya setelah melihat gambar. Complete menggabungkan record session yang sebenarnya; ekstraksi bukan viewed.

Jalankan check-camera sebelum mengisi desain. Sebelum render jalankan complete dan check-input dengan sesi yang sama. Koreksi audit kerja, lalu render/review keseluruhan snapshot terbaru. Receipt/cache/session/flow/sheet/log tidak masuk ZIP. MP4 tetap terpisah. Kontrak lengkap: contracts/package.md, contracts/report.md dan contracts/reader.md.
