# Pengisian audit.json HOMEKU 3.0

Baca visual-audit.md sebelum menyimpulkan gerak. Satu audit.json ringkas adalah sumber final untuk laporan dan AI. Template belum valid sebelum placeholder/area/pilihan bukti/narasi diisi auditor. Prepare dan complete hanya membantu pekerjaan mekanis.

## Kelompok isi

| Field | Isi auditor |
| --- | --- |
| id / revision | Stem MP4 kanonis dan revisi; sumber baru r0001 |
| design.name | Nama desain deskriptif |
| design.styles | primary satu klaim; influences/interior daftar klaim diskret, nama Inggris |
| design.size | scale, levels, footprint, proportions; floor_area_m2 min/max positif wajib |
| design.features | Aspek DNA yang dinyatakan; tanpa 17 placeholder wajib |
| areas | ID ruang fisik, label, fungsi dan visible_intervals presisi |
| shots | Satu take sampai cut; bukan satu area |
| shots.design | Scope area dan architecture/furnishings/environment: text + facts |
| shots.composition | Posisi/arah/angle/tinggi/tilt awal; framing/fokus/lighting/depth/reveal |
| shots.camera | description Indonesia, phases dan tempo; journey bila menambah penjelasan |
| panels / overviews | frame_index native dan area_ids; Overview memiliki composition_summary |
| route / area_relations / relations / notes | Hanya hubungan/rute/batas yang benar-benar dinyatakan |

## Klaim dan fakta

Klaim minimal: value, state, evidence. State eksplisit observed, uncertain, not-visible, not-present, unknown. Evidence berupa daftar indeks frame native global sumber, misalnya [142,195,248]. Confidence/note opsional, tidak ada default observed/high. Unknown dapat tanpa bukti; klaim lain perlu bukti sesuai scope. Tidak terlihat bukan tidak ada.

Fakta menambahkan subject dan attribute; facet_roles eksplisit untuk struktur seperti opening, roof, massing, layout, configuration, circulation. Domain khusus dan area_ids override dipertahankan bila diperlukan. Kategori/area kontainer mengikat scope; override tidak boleh keluar dari kontainer. Bukti satu kategori tidak otomatis membuktikan seluruh fakta. Gunakan state terpisah bila objek terlihat tetapi tipe atau hubungannya belum jelas. Lihat [contoh gaya dan layout](visual-audit.md#detail-desain-dan-framing).

Tulis text manusia secara ringkas dengan ciri pembeda di awal. Gunakan `composition_summary` untuk posisi kamera, arah pandang dan cakupan wide. Uraikan detail arsitektur, furnitur dan lingkungan di `shots.design`. Facts menyimpan informasi yang diperlukan discovery. Tidak ada kuota jumlah fakta, fact_coverage paralel atau generator yang menebak fakta dari paragraf.

## Kamera

Fase memiliki start_s/end_s, notation, depth_direction, focus, evidence temporal dan observations depth/translation/rotation. Tulis pengamatan singkat spesifik interval; evidence bersama tidak disalin tiga kali. Overrides per komponen hanya bila berbeda bukti/ambiguitas.

Notation memakai + simultan; → hanya pada summary turunan antar fase. Nilai besaran tiap komponen dan tulis estimasi ~× atau ~° yang dapat dibuat secara wajar dari frame. Angka tunggal dan rentang sama-sama sah. Estimasi tetap di `notation`. Lihat [panduan visual](visual-audit.md#arah-notasi-dan-tempo).

Depth_direction IN/OUT/NO IN/OUT/null ambigu adalah keputusan auditor, bukan hasil tebak dari zoom/skala global. ~× adalah perubahan skala gambar, bukan tempo. Semua moderate sah.

Tempo hanya satu sumber: label+description jika seragam; segments bertimestamp+description bila berubah. Batas tempo boleh berbeda dari fase. Easing/intensitas komponen bukan tempo. Jangan menambahkan phase.tempo atau camera_summary/components_parsed ke audit.

## Seleksi dan metadata

Normal tiga panel Start/Middle/End pada awal, midpoint native terdekat dan akhir. Multi dinamis, awal/akhir wajib. Overview dipilih untuk gambaran area lengkap, biasanya awal IN/akhir OUT; paragrafnya menjelaskan frame itu, Camera Start tetap awal sumber.

ID selection, shot_id, PTS, duration, parsed/summary/pattern dan coverage mekanis dihitung saat diperlukan atau disimpan teknis sekali dalam manifest. Tidak disisipkan kembali ke audit ringkas. Tidak menyimpan seluruh frame video.

## Provenance proses

audit-info hanya method, limitations, provider/model yang diketahui, reviewed_ranges dan frame_reviews yang benar-benar dideklarasikan. Model build tidak diketahui null. Gunakan mark-viewed hanya setelah melihat gambar. Complete menggabungkan record session yang sebenarnya; ekstraksi bukan viewed.

Sebelum render jalankan check-input atau draft resmi. Koreksi audit kerja, lalu render/review keseluruhan snapshot terbaru. Receipt/cache/session/flow/sheet/log tidak masuk ZIP. MP4 tetap terpisah. Kontrak lengkap: contracts/package.md, contracts/report.md dan contracts/reader.md.
