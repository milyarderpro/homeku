# Hasil implementasi tahap 3–5

Implementasi lokal pada 17 November 2026. Snapshot pengetahuan: 2026-11-17-stage-3-5. Repo tetap menjadi pustaka pengetahuan; alur kreatif dan prompt generator tetap berada di plugin/master prompt mendatang.

## Tahap 3 — Percontohan dan baseline

Bank evaluasi dibekukan sebelum pengayaan: 40 kasus, terdiri dari 24 development dan 16 heldout. Dua belas kasus menguji pencarian contoh positif, 14 membandingkan nilai anotasi, delapan berisi jawaban acuan unknown dan enam membahas batas fakta sumber versus keputusan kreatif.

Baseline lokal lulus 26/26 pemeriksaan otomatis. Empat belas jawaban acuan belum dinilai terhadap respons AI konsumen; akurasi model konsumen tetap null. Hasil ini tidak mengukur ketepatan seluruh hasil pencarian atau peningkatan kualitas konsep kreatif.

Dua belas referensi pilot mencakup 59 shot. Storyboard dan contact sheet awal–tengah–akhir pilot ditinjau secara visual oleh AI. Cakupan review dicatat bersama hash anotasi, video dan media yang diperiksa. Versi build model tidak tersedia dari runtime dan dicatat null.

Temuan penting: VID-001 memiliki blur transisi pada sampel akhir shot pertama. edh033 dan edh060 memperlihatkan fungsi living/kitchen/loft bersama. Dua alias scene overview edh060 berbeda dari label shot, tetapi tidak membuktikan salah fakta. Tidak ada koreksi isi anotasi asli yang dipaksakan.

## Tahap 4 — Relasi dan bukti temporal

Tersedia 885 frame temporal dari 295 shot, dengan timestamp, hash, durasi stream dan batas sampling. Sampel ditempatkan sedikit di dalam batas shot dan dibatasi durasi video yang terdekode.

Catatan memisahkan subjek, framing tersimpan, label kamera, cahaya, transisi, gerak objek yang belum diketahui, elemen arsitektur, furnitur/dekorasi dan lingkungan. Relasi berasal dari ungkapan eksplisit pada anotasi, menyimpan teks mentah dan pointer sumber. Compound target tidak dipecah menjadi geometri dugaan. Istilah pelapis seperti stone facing, modifier front-facing dan warm under-cabinet lighting tidak disalahartikan sebagai relasi objek; deskripsi lengkapnya tetap tersimpan.

Koordinat relasi bersifat relatif terhadap pandangan kamera. Urutan edit tidak dianggap adjacency. Denah terukur, arah mata angin, ukuran fisik, focal length, material geologis, identitas objek lintas potongan dan lintasan kamera fisik tetap unknown.

## Tahap 5 — Cakupan dan sintesis

Seluruh 57 referensi mempunyai profil, pemetaan, catatan review storyboard terpilih dan paket bukti desain. Hasil awal: 3.123 observasi dengan asal bukti eksplisit dan 1.826 relasi literal. Semua 6.111 deskripsi detail tetap terlacak dalam inventaris mention per shot; jumlah tersebut bukan jumlah objek unik.

Sintesis seluruh korpus mencatat definisi hitungan, numerator, denominator, daftar pendukung dan pengecualian anotasi. Pola awal: 57/57 dimulai eksterior, 13/57 berakhir eksterior, 6/57 memenuhi aturan eksplisit open-plan beberapa fungsi, 2/57 menamai sleeping/bedroom loft, 54/57 menamai bathroom dan 55/57 menamai kitchen. Tidak adanya label bukan bukti bahwa ruangan tidak ada.

Keragaman disajikan menurut label asli serta konsep normalisasi berversi. Kategori skala visual: medium 36/57, small 16/57, large 4/57, tiny 1/57. Koleksi ini bukan sampel acak populasi rumah; kelangkaan label perlu diperiksa terhadap sinonim sebelum menjadi prioritas referensi baru.

Pemindaian kemiripan mencakup 62 video dan 900 sampel, membandingkan 1.891 pasangan. Metode hash visual menemukan nol pasangan kandidat pada ambang yang dicatat. Ini bukan bukti bahwa seluruh isi berbeda. Tes mencakup kompresi ulang JPEG; pemindaian dapat melewatkan crop berat, edit dan adegan yang tidak tersampel. Tidak ada penghapusan, penggabungan atau penyesuaian hitungan otomatis.

Tema arsitektur, interior, lanskap, cahaya, ruang, kamera, kompatibilitas, orisinalitas dan DNA ditautkan ke sintesis seluruh korpus. OBSERVATION, AGGREGATE, INFERENCE dan DESIGN_PRINCIPLE tetap dibedakan.

## Batas penyelesaian

Review storyboard mencakup ciri terpilih, bukan validasi ulang seluruh tag. Review temporal baru dilakukan pada 12 pilot; 45 sumber lain memiliki sampel dengan alasan pending yang eksplisit. Playback kontinu dan mekanika kamera belum diverifikasi ulang. Tahap 3–5 menyediakan format, bukti, cakupan dan pemeriksaan ini tanpa mengarang kejadian review.

Video, analysis.yaml, analysis.md, keyframe/storyboard asli dan request lama dipertahankan. Seluruh referensi tetap boleh menginspirasi keputusan baru; tidak ada syarat verifikasi manual atau penolakan bahan desain karena confidence rendah.

Tahap 6–7 belum selesai: publikasi commit ke GitHub dan evaluasi konsumsi AI melalui web/konektor belum dijalankan pada berkas baru ini. Hasil lokal tidak menggantikan kedua pengujian tersebut.

Lihat [cakupan bukti](../knowledge/design-evidence/README.md), [pola korpus](../knowledge/corpus-patterns.md), [review AI](../knowledge/reviews/README.md), [evaluasi](../evaluations/stage3/README.md), dan [pemeliharaan](knowledge-maintenance.md).

## Hasil validasi lokal

- Seluruh 137 tes lulus, termasuk penelusuran raw value/pointer, sumber/media usang, batas sampling, relasi ambigu, pending review, determinisme build, pemisahan adjacency dan penyimpanan paralel.
- Pemeriksaan source integrity, knowledge library, catalog, design evidence dan similarity report lulus.
- Baseline dan evaluasi lokal terkini sama-sama 26/26; 14 jawaban acuan tetap unscored dan akurasi AI konsumen null.
- Manifest sumber/anotasi tahap 3–5 identik dengan snapshot tahap 1–2-r2. Tidak ada perubahan di references/, video/ atau requests/.
- Perubahan tersedia di working tree lokal; belum dibuat commit atau dipush.
