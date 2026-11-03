<!--
HOMEKU: ACUAN STRUKTUR LAPORAN VISUAL, bukan template yang dieksekusi langsung.
Workflow v1.2 membuat analysis.md melalui fungsi markdown() dalam
scripts/save_analysis_action.py. Jika ingin mengubah output otomatis,
ubah kode generator DAN acuan ini secara konsisten.

- Semua fakta berasal dari analysis.yaml schema 2.1 yang sama.
- ChatGPT menampilkan draft saat review; tampilan final bisa berbeda.
- Runner menambahkan marker request_id untuk deduplikasi.
- Gambar JPEG dihasilkan FFmpeg dari MP4 video/, lalu ditampilkan inline.
- storyboard.jpg dibuat oleh scripts/storyboard.py: 1–5 shot dalam satu baris (kolom sejumlah shot), lebih dari 5 shot dalam tiga kolom; judul, metadata, gambar portrait, serta label scene/waktu/kamera sesuai YAML.
- Ulangi tabel timeline dan bagian per-shot sesuai shots[].
- Jika perkiraan luas null, tampilkan "Tidak diketahui".
- `architecture.common_regions` adalah asosiasi gaya (bukan lokasi bangunan); jika kosong atau absen pada data lama, tampilkan "Tidak diketahui".
- Label manusia: Shot 01, Shot 02; ID data: shot-01, shot-02.
-->
# {{video.id}} — {{architecture.primary_style | humanize_and_title}}

<!-- homeku_request_id: {{request_id}} -->

**Sumber data:** [analysis.yaml](analysis.yaml) · **Status:** {{analysis_quality.status}} · **Diverifikasi manusia:** {{analysis_quality.human_verified | humanize}}

## 1. Informasi Video

| Informasi | Nilai |
|---|---|
| ID | {{video.id}} |
| File asli | {{video.filename}} |
| Durasi | {{video.duration_s}} |
| Resolusi | {{video.resolution}} |
| FPS | {{video.fps}} |
| Rasio | {{video.aspect_ratio}} |
| Jumlah shot | {{video.shot_count}} |

## 2. Storyboard Gabungan

![Storyboard](storyboard.jpg)

## 3. Identitas Desain

| Aspek | Hasil analisis |
|---|---|
| Gaya utama | {{architecture.primary_style | humanize}} |
| Wilayah terkait gaya desain | {{architecture.common_regions | join_humanize_or_unknown}} |
| Pengaruh gaya | {{architecture.secondary_influences | join_humanize}} |
| Ciri eksterior | {{architecture.exterior_features | join_humanize}} |
| Gaya interior | {{architecture.interior_style | join_humanize}} |
| Confidence gaya | {{architecture.style_confidence}} |

## 4. Ukuran & Proporsi Bangunan

| Aspek | Estimasi visual |
|---|---|
| Ukuran yang terlihat | {{architecture.building_scale.perceived_size | humanize}} |
| Bentuk bangunan | {{architecture.building_scale.building_form | humanize}} |
| Skala vertikal | {{architecture.building_scale.vertical_scale | humanize}} |
| Tapak bangunan | {{architecture.building_scale.footprint | humanize}} |
| Perkiraan luas lantai | {{architecture.building_scale.estimated_floor_area_m2 | range_or_unknown}} |
| Confidence | {{architecture.building_scale.confidence}} |

> Luas adalah perkiraan visual, bukan ukuran terukur.

## 5. Warna, Pencahayaan, dan Atmosfer

| Warna dominan | HEX (perkiraan) |
|---|---|
| {{visual_style.dominant_colors[].name}} | {{visual_style.dominant_colors[].hex_approx}} |
<!-- Ulangi baris warna untuk semua warna yang ada; jika kosong, tidak ada baris data. -->

| Aspek | Hasil analisis |
|---|---|
| Pencahayaan | {{visual_style.lighting | join_humanize}} |
| Lingkungan | {{visual_style.setting | join_humanize}} |
| Musim yang tampak | {{visual_style.season_appearance | humanize}} |
| Mood | {{visual_style.mood | join_humanize}} |

## 6. Struktur dan Timeline Video

**Jenis:** {{video_structure.type | humanize}} · **Tempo:** {{video_structure.overall_pace | humanize}} · **Transisi:** {{video_structure.transition_pattern | humanize}}

| Shot | Waktu (detik) | Durasi | Area/Scene | Gerakan Kamera |
|---|---|---|---|---|
| Shot {{shots[].id | number_2digit}} | {{shots[].start_s}}–{{shots[].end_s}} | {{shots[].end_s - shots[].start_s}} | {{shots[].scene | humanize}} | {{shots[].camera.movements | join_humanize}} |
<!-- Ulangi satu baris per shot. -->

## 7. Analisis per Shot

<!-- Ulangi blok ini untuk setiap shot, dengan nomor gambar/label yang sesuai. -->
### Shot {{shots[].id | number_2digit}} — {{shots[].scene | humanize}}

<img src="shot-01.jpg" alt="Shot 01" width="360">

**Waktu:** {{shots[].start_s}}–{{shots[].end_s}} detik

| Komponen | Pengamatan |
|---|---|
| Fokus utama | {{shots[].focal_subject | humanize}} |
| Framing awal → akhir | {{shots[].framing.start | humanize}} → {{shots[].framing.end | humanize}} |
| Sudut pandang | {{shots[].framing.view_angle | humanize}} |
| Gerakan kamera | {{shots[].camera.movements | join_humanize}} |
| Kecepatan kamera | {{shots[].camera.speed | humanize}} |
| Pencahayaan | {{shots[].lighting | humanize}} |
| Transisi keluar | {{shots[].transition_out | humanize}} |

**Detail yang terlihat**

- **Arsitektur:** {{shots[].visible_details.architectural | join_humanize}}
- **Furnitur dan properti:** {{shots[].visible_details.furniture_and_props | join_humanize}}
- **Lingkungan:** {{shots[].visible_details.environment | join_humanize}}

**Catatan pengamatan:** {{shots[].observation_note | humanize}}

**Confidence:** Kamera {{shots[].confidence.camera | humanize}} · Detail visual {{shots[].confidence.visual_details | humanize}}

## 8. Kualitas dan Ketidakpastian Analisis

| Parameter | Hasil |
|---|---|
| Status | {{analysis_quality.status}} |
| Verifikasi manusia | {{analysis_quality.human_verified | humanize}} |
| Ketepatan timestamp | {{analysis_quality.timestamp_precision | humanize}} |
| Ketidakpastian | {{analysis_quality.uncertainties | join_humanize}} |

**Catatan:** {{analysis_quality.notes | humanize}}

---

*Laporan ini diturunkan dari [analysis.yaml](analysis.yaml).*
