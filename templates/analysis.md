<!--
HOMEKU: TEMPLATE LAPORAN VISUAL
- Isi setiap nilai dari analysis.yaml (sumber data utama).
- Jangan menambah fakta, audio, ide konten, atau prompt yang tidak ada di YAML.
- Ulangi bagian "Analisis per Shot" sebanyak video.shot_count.
- Gambar tampil langsung (inline), bukan hanya tautan.
- Label shot yang ditampilkan: Shot 01, Shot 02, ... (ID YAML: shot-01, shot-02, ...).
- File ini berada di references/VID-XXX/analysis.md bersama storyboard.jpg dan shot-01.jpg dst.
- Tampilkan ukuran rumah berdasarkan architecture.building_scale; rentang m² adalah estimasi, bukan ukuran terukur.
-->
# {{video.id}} — {{architecture.primary_style | humanize}}

> {{ringkasan_visual_berdasarkan_YAML}}

**Sumber data:** [analysis.yaml](analysis.yaml) · **Status:** `{{analysis_quality.status}}` · **Diverifikasi manusia:** {{analysis_quality.human_verified}}

## 1. Informasi Video

| Informasi | Nilai |
|---|---|
| ID | `{{video.id}}` |
| File asli | `{{video.filename}}` |
| Durasi | {{video.duration_s}} detik |
| Resolusi | {{video.resolution}} |
| FPS | {{video.fps}} |
| Rasio | {{video.aspect_ratio}} |
| Jumlah shot | {{video.shot_count}} |

## 2. Storyboard Gabungan

![Storyboard {{video.id}}](storyboard.jpg)

> Storyboard merangkum semua shot. Setiap gambar shot juga ditampilkan langsung pada bagian rincian di bawah.

## 3. Identitas Desain

| Aspek | Hasil analisis |
|---|---|
| Gaya utama | {{architecture.primary_style | humanize}} |
| Pengaruh gaya | {{architecture.secondary_influences | join}} |
| Ciri eksterior | {{architecture.exterior_features | join}} |
| Gaya interior | {{architecture.interior_style | join}} |
| Confidence gaya | {{architecture.style_confidence}} |

## 4. Ukuran & Proporsi Bangunan

| Aspek | Estimasi visual |
|---|---|
| Ukuran yang terlihat | {{architecture.building_scale.perceived_size | humanize}} |
| Bentuk bangunan | {{architecture.building_scale.building_form | humanize}} |
| Skala vertikal | {{architecture.building_scale.vertical_scale | humanize}} |
| Tapak bangunan | {{architecture.building_scale.footprint | humanize}} |
| Perkiraan luas lantai | {{architecture.building_scale.estimated_floor_area_m2.min}}–{{architecture.building_scale.estimated_floor_area_m2.max}} m² |
| Confidence | {{architecture.building_scale.confidence}} |

> Luas adalah **estimasi visual**, bukan ukuran pasti. Jika tidak bisa diperkirakan, tampilkan "Tidak diketahui" (bukan `null–null` m²). Tidak perlu memeriksa konsistensi dimensi eksterior–interior.

## 5. Warna, Pencahayaan, dan Atmosfer

| Warna dominan | HEX (perkiraan) |
|---|---|
| {{visual_style.dominant_colors[].name}} | `{{visual_style.dominant_colors[].hex_approx}}` |
<!-- Ulangi baris ini untuk setiap warna. -->

| Aspek | Hasil analisis |
|---|---|
| Pencahayaan | {{visual_style.lighting | join}} |
| Lingkungan | {{visual_style.setting | join}} |
| Musim yang tampak | {{visual_style.season_appearance}} |
| Mood | {{visual_style.mood | join}} |

## 6. Struktur dan Timeline Video

**Jenis:** {{video_structure.type | humanize}} · **Tempo:** {{video_structure.overall_pace}} · **Pola transisi:** {{video_structure.transition_pattern | humanize}}

| Shot | Waktu (detik) | Durasi | Area/Scene | Gerakan Kamera |
|---|---|---|---|---|
| {{shots[].id | humanize}} | {{shots[].start_s}}–{{shots[].end_s}} | {{end_s - start_s}} dtk | {{shots[].scene | humanize}} | {{shots[].camera.movements | join}} |
<!-- Ulangi baris ini untuk setiap shot. -->

## 7. Analisis per Shot

<!-- Ulangi SELURUH blok untuk Shot 02, Shot 03, dst. Label tampilan 'Shot 01' berasal dari ID YAML 'shot-01'. -->
### {{shots[].id | humanize}} — {{shots[].scene | humanize}}

<img src="shot-01.jpg" alt="Keyframe {{shots[].id | humanize}} — {{shots[].scene | humanize}}" width="360">

**Waktu:** {{shots[].start_s}}–{{shots[].end_s}} detik · **Durasi:** {{end_s - start_s}} detik

| Komponen | Pengamatan |
|---|---|
| Fokus utama | {{shots[].focal_subject | humanize}} |
| Framing awal → akhir | {{shots[].framing.start}} → {{shots[].framing.end}} |
| Sudut pandang | {{shots[].framing.view_angle | humanize}} |
| Gerakan kamera | {{shots[].camera.movements | join}} |
| Kecepatan kamera | {{shots[].camera.speed}} |
| Pencahayaan | {{shots[].lighting | humanize}} |
| Transisi keluar | {{shots[].transition_out | humanize}} |

**Detail yang terlihat**

- **Arsitektur:** {{shots[].visible_details.architectural | join}}
- **Furnitur dan properti:** {{shots[].visible_details.furniture_and_props | join}}
- **Lingkungan:** {{shots[].visible_details.environment | join}}

**Catatan pengamatan:** {{shots[].observation_note}}

**Confidence:** Kamera {{shots[].confidence.camera}} · Detail visual {{shots[].confidence.visual_details}}

<!-- Untuk shot berikutnya: gunakan <img src="shot-02.jpg" ...>, <img src="shot-03.jpg" ...> dst. Nomor gambar tetap dua digit dan harus sesuai dengan shots[].keyframe di YAML. -->

## 8. Kualitas dan Ketidakpastian Analisis

| Parameter | Hasil |
|---|---|
| Status | {{analysis_quality.status}} |
| Verifikasi manusia | {{analysis_quality.human_verified}} |
| Ketepatan timestamp | {{analysis_quality.timestamp_precision}} |
| Ketidakpastian | {{analysis_quality.uncertainties | join}} |

**Catatan:** {{analysis_quality.notes}}

---

*Laporan ini merupakan representasi visual dari [analysis.yaml](analysis.yaml), bukan sumber fakta atau analisis yang terpisah.*
