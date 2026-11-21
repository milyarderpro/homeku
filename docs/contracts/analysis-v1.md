# Kontrak laporan Markdown 1.0 — provisional

Laporan memakai bahasa Indonesia, dengan istilah gerak kamera dalam bahasa Inggris. Prosa menjelaskan desain secara lengkap; tabel menjadi sumber fakta untuk katalog. Jangan menambah fakta katalog melalui narasi yang tidak masuk tabel. Tidak ada analysis.json yang diedit terpisah.

Gunakan [template awal](../../audit/template-analysis.md). Heading dan nama kolom berikut stabil serta peka kapitalisasi. Setiap tabel memakai satu baris header/separator; sel wajib diisi. Gunakan unknown untuk nilai belum diketahui, '-' untuk field yang secara eksplisit tidak berlaku, dan `\\|` untuk pipe dalam sel. Daftar dipisahkan titik koma hanya pada kolom yang disebutkan.

## Heading utama

| H2 | Isi |
| --- | --- |
| Identitas | Tabel field/value: format_version, id, revision, title |
| Ringkasan | Karakter referensi dan pembeda, dalam prosa |
| Cakupan | Tabel field/value: method dan limitations; sama dengan manifest |
| Timeline | Tabel shot, start_s, end_s, areas, transition, continuity |
| Shot shot-XX | Lima H3 per shot, sesuai daftar di bawah |
| Hubungan antarshot | Tabel from, to, relation, description, state, confidence, evidence; boleh tanpa baris data |
| Keterbatasan | Ketidakpastian keseluruhan, termasuk hal yang belum diamati |

Shot bernomor shot-01, shot-02, dan seterusnya tanpa lompatan; tambahkan anchor eksplisit `<a id="shot-01"></a>` sebelum heading shot. Timeline mencakup durasi sumber tanpa gap/overlap. `areas` memuat satu atau beberapa fungsi eksplisit dipisahkan ';'. Cut dibedakan dari segmen fungsi dalam shot kontinu; anotasi tidak membuat cut yang tidak terlihat.

MD menampilkan/menautkan media/storyboard.jpg dan gambaran area setiap shot dengan tautan relatif. Bukti hanya menautkan media yang terdaftar, anchor shot, atau sumber ../../video/<id>.mp4.

## Lima bagian per shot

### Desain dan konfigurasi

Prosa lengkap: bentuk, proporsi visual, plafon, bukaan, tampilan material, furnitur, penyimpanan, dekorasi, cahaya, lingkungan dan hubungan spasial yang terlihat. Susunan, bentuk dan fungsi lebih penting daripada sekadar nama gaya/warna. Tidak ada kuota objek wajib.

### Fakta

Kolom: `id | domain | subject | attribute | value | state | confidence | evidence`.

ID fakta f-01 dst., unik dalam shot. Domain/subject/attribute berupa label eksplisit; label baru tetap dipertahankan. Misalnya domain space, architecture, furnishing, material, lighting, environment, relation. Setiap baris menyatakan satu klaim dengan statusnya:

- observed: terlihat dan mendukung nilai yang dicatat.
- uncertain: interpretasi masih meragukan.
- not-visible: tidak terlihat pada bukti; tidak menyatakan objek tidak ada.
- not-present: audit secara eksplisit menyatakan tidak ada pada cakupan yang diperiksa.
- unknown: informasi belum diketahui.

Confidence: high, medium, low, unknown. Evidence memakai tautan Markdown lokal, misalnya `[awal](media/shot-01/start.jpg); [detail](media/shot-01/detail-01.jpg)`. Klaim membutuhkan bukti dalam shot yang sama; unknown dapat memakai '-'. Katalog tidak mengubah status nonpositif menjadi observed.

### Komposisi

Tabel field/value wajib berisi:

```text
overview_timestamp_s
overview_role
overview_reason
overview_exception
camera_position
camera_direction
view_angle
camera_height
camera_tilt
foreground
depth
reveal
start_composition
end_composition
motion_compatibility
```

overview_role: start/middle/end, mengikuti sepertiga durasi sumber. overview_exception '-' bila tidak diperlukan. camera_position/direction relatif terhadap area/subjek, bukan hanya lokasi objek di layar. view_angle dapat frontal, oblique, side atau deskripsi eksplisit lain; label baru disimpan. Besaran fisik yang tidak diketahui memakai unknown, bukan angka rekaan.

motion_compatibility menjelaskan hubungan posisi, orientasi, framing, foreground dan kedalaman dengan lintasan sumber. Catat peran gambaran area: gambar luas pada akhir Dolly-Out bukan posisi awal sumber. Data ini membantu AI membuat gambar dengan sudut yang cocok dengan gerak yang dituju, tanpa selalu memakai frontal.

### Kamera

Satu ringkasan dalam fenced block text, mempertahankan simbol →, +, ~, ° dan ×. → menyatakan fase berurutan; + menyatakan komponen simultan pada interval yang sama. Ikuti [notasi plan](../implementation-plan.md#format-ringkasan-gerakan-kamera); angka mengikuti bukti, bukan contoh wajib.

Tabel: `phase | start_s | end_s | components | anchor | tempo | speed_change | basis | evidence | confidence | uncertainty`.

Satu baris per fase berurutan, phase-01 dst. components memuat semua komponen simultan dengan '+'. Setelah whitespace dan titik penutup dinormalisasi, urutan components harus sama dengan ringkasan. Fase mencakup seluruh shot tanpa gap/overlap; jika komponen simultan mulai/berhenti di waktu berbeda, pecah fase pada batas tersebut.

Tempo: slow, moderate, fast, variable, unknown. Speed_change: accelerating, decelerating, constant, variable, unknown. Kelancaran gerak tidak menentukan tempo. Basis menjelaskan perubahan visual, dasar perkiraan dan jangkar. Uncertainty menjelaskan batas tafsir; wajib bila tempo unknown. Evidence menautkan frame terkait; bukti temporal lengkap tetap bersumber pada video.

~1.3×/~2× adalah estimasi pendekatan/perubahan skala terhadap jangkar, bukan faktor percepatan atau jarak fisik. Sudut adalah estimasi visual dengan batas yang dijelaskan. Accelerating harus konsisten dengan speed_change; strong/gentle berlaku pada komponen terkait. Label gerak baru disimpan sebagai other beserta teks literal, bukan diubah menjadi gerakan yang dikenal.

### Ketidakpastian

Jelaskan hal yang belum terlihat, klaim yang belum pasti dan batas bukti. Pemeriksaan sampling/playback/frame-by-frame dilaporkan sesuai yang benar-benar dijalankan. Media tersimpan bukan bukti bahwa seluruh frame telah diperiksa.

## Hubungan antarshot dan turunan

Hubungan memakai status/confidence yang sama dengan fakta. from/to harus ID shot yang ada; bukti dari media terdaftar. Adjacency, material pasti, dimensi, lokasi dan rumah independen tidak disimpulkan tanpa dukungan.

Generator menyalin nilai, status, confidence, notasi kamera dan pointer sumber. Knowledge mengelompokkan variasi atribut; hitungan adalah pasangan referensi/shot unik yang mencatat atribut tersebut, dengan denominator eksplisit. Tidak ada sintesis AI bebas pada ingest.
