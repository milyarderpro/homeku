# HOMEKU — Template Paket Produksi Video v1.1

> **TEMPLATE KOSONG, bukan produksi jadi.** Salin untuk satu konsep **setelah ide dipilih**, misalnya `productions/IDEA-001/production.md`; simpan ke GitHub **hanya dengan izin eksplisit**.  
> **Wajib dibaca bersama:** [`rules/workflow-production.md`](../rules/workflow-production.md) dan [`knowledge/dna-summary.md`](../knowledge/dna-summary.md).  
> **Bahasa isi:** Indonesia (catatan, review dan keputusan); **prompt image/video:** Inggris.  
> **Instruksi pengisian:** hapus atau isi semua placeholder `<...>` sebelum output dinyatakan final; label `BELUM` tidak boleh diganti `LULUS` tanpa pemeriksaan. *Catatan: referensi dan contoh ID di bawah bukan bukti konsep sudah dihasilkan.*

## A. Identitas proyek, persetujuan dan status

| Kolom | Nilai |
| --- | --- |
| `production_id` | `<IDEA-ID-UNIK-DAN-TERVERIFIKASI>` |
| `title` | `<judul rumah>` |
| `concept_version` | `<v1>` |
| `status` | `idea_options / idea_selected / design_draft / design_approved / awaiting_images / images_approved / prompts_ready / qa_pending / revision_required / final_approved` — **pilih satu** |
| `source_snapshot` | `<commit Git saat sumber analisis diperiksa>` |
| `primary_reference_id` | `<ID utama>` |
| `supporting_reference_ids` | `<ID pendukung A, ID pendukung B opsional>` |
| `image_route` | **A_DEFAULT** (AI generate) / **B_REQUESTED** (AI menulis prompt) |
| `format` | **9:16 portrait** |
| `target_final_duration_s` | **20** |
| `generations` | **2 × 10s Google Flow Omni Flash** |
| `exterior_hook_min_duration_s` | **6** |
| `idea_selected_by_user` | `<status, pesan persetujuan atau BELUM>` |
| `design_storyboard_approved_by_user` | `<status/pesan atau BELUM>` |
| `all_images_approved_by_user` | `<status/pesan atau BELUM>` |
| `final_video_approved_by_user` | `<status/pesan atau BELUM>` |
| `github_save_approval` | `BELUM / pesan eksplisit yang menyebut produksi & target file` |
| `asset_storage` | `<tautan aset jika tersedia; jangan mengarang URL>` |

**Transisi status yang diperbolehkan:** ideasi → satu ide terpilih → Design Lock/storyboard disetujui → aset gambar tersedia → gambar disetujui → dua prompt siap → QA hasil pengguna → video final disetujui. Jika ada revisi, kembali ke fase terdampak dan batalkan persetujuan yang tidak lagi valid.

## B. Tiga Idea Cards (ditampilkan sebelum user memilih)

**Aturan:** tiga kandidat **berbeda secara substantif**; masing-masing mempunyai referensi DNA, exterior hook ≥6 detik, sinematografi, urutan shot, unsur orisinal, dan risiko produksi. Hanya satu dipilih; proyek yang tidak dipilih **tidak** diteruskan ke gambar atau prompt video.

| Kandidat | Nama & ciri rumah | Hook exterior 6s / visual pertama | DNA referensi dan peran | Perbedaan orisinal | DNA kamera+edit dan rencana shot | Risiko teknis |
| --- | --- | --- | --- | --- | --- | --- |
| `<IDEA-A>` | `<gaya, bentuk, material, lanskap>` | `<wide/frame0 → hero feature → entry>` | `<utama + pendukung / ID>` | `<apa yang baru>` | `<framing, gerak, 2×10s plan>` | `<risiko>` |
| `<IDEA-B>` | `<gaya, bentuk, material, lanskap>` | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` |
| `<IDEA-C>` | `<gaya, bentuk, material, lanskap>` | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` |

**Kandidat yang dipilih:** `<ID + persetujuan user>`. **Alasan final:** `<keunikan dan kecocokan 7 DNA>`.

## C. Provenance: pemilihan referensi dan jejak tujuh DNA

### C1. Peran referensi (2–3 total)

| Peran | Referensi & sumber Git yang dibaca | Shot/field bukti | Apa yang diambil | Apa yang tidak boleh diimpor | Keyakinan/ketidakpastian |
| --- | --- | --- | --- | --- | --- |
| **Utama (arsitektur)** | `<references/ID/analysis.yaml + analysis.md + storyboard>` | `<shot-01/architecture.*>` | `<identitas, massa, detail>` | `<bagian yang sengaja berbeda>` | `<high/medium/low+alasan>` |
| **Pendukung A** | `<...>` | `<...>` | `<lanskap/lighting/interior>` | `<atap/level/style yang berbenturan>` | `<...>` |
| **Pendukung B (opsional)** | `<... atau tidak digunakan>` | `<...>` | `<sinematografi/edit>` | `<geometri sumber yang tidak kompatibel>` | `<...>` |

### C2. DNA Trace tujuh dimensi — **semuanya wajib ada**

Tulis `FAKTA REFERENSI` (dengan ID/shot/field), `INTERPRETASI`, `KREASI BARU` dan `RISIKO` untuk **setiap dimensi**, tidak hanya arsitektur. Setiap keputusan harus memengaruhi paling tidak satu shot/Desain Lock/aturan prompt.

| Layer DNA | Referensi / shot / field + observasi (FAKTA) | Interpretasi yang relevan | Implementasi pada rumah/shot BARU | Apa yang berubah dari referensi | Risiko/ketidakpastian |
| --- | --- | --- | --- | --- | --- |
| **DNA-01 Hook exterior** | `<ID/shot-01/framing+camera>` | `<mengapa reveal ini tepat>` | `<frame0, foreground, gerak, target ≥6s>` | `<...>` | `<...>` |
| **DNA-02 Architecture** | `<ID/architecture+shot detail>` | `<...>` | `<massing, roofline, bukaan>` | `<...>` | `<...>` |
| **DNA-03 Environment** | `<ID/shot/environment>` | `<...>` | `<garden, jalur, tree placement, window views>` | `<...>` | `<...>` |
| **DNA-04 Interior** | `<ID/shot/object positions>` | `<...>` | `<room relations, furniture anchors>` | `<...>` | `<...>` |
| **DNA-05 Cinematic** | `<ID/shot/framing/camera/focal>` | `<...>` | `<per-shot start/end/motion/speed/reveal>` | `<...>` | `<...>` |
| **DNA-06 Lighting/Mood** | `<ID/shot/lighting, visual_style>` | `<...>` | `<white balance, window + warm fixtures>` | `<...>` | `<...>` |
| **DNA-07 Edit/Narrative** | `<ID/video_structure+shots>` | `<...>` | `<scene order, cut positions, ending>` | `<...>` | `<...>` |

**Konflik dan resolusi:** `<contoh: sumber utama 1 lantai, pendukung 2 lantai → pilih 1 lantai; bukti yang digunakan>`. **Wilayah terkait gaya:** `<association only, bukan geolokasi>`. **Klaim viralitas:** `<tidak disimpulkan dari data visual>`.

## D. Design Lock — SATU RUMAH yang sama

Setelah **Gate 2**, salin deskripsi ini *secara konsisten* ke semua prompt gambar dan video. Jangan memasukkan objek/spasial baru yang bertentangan saat membuat klip kedua.

| Aspek | Ketentuan terkunci |
| --- | --- |
| Identitas | `<nama karakter rumah, mood, originality statement>` |
| Dimensi/level tampak | `<compact/medium/large, 1/2 level, proporsi masuk akal; bukan luas terukur>` |
| Massa dan atap | `<roof shape/slope, roof finish, elevation, chimney/terrace>` |
| Fasad dan pintu | `<warna/material tampak, porch, steps, posisi/jenis pintu, hardware>` |
| Jendela | `<sistem bukaan, warna frame, grid/arch, posisi relatif pada facade & room>` |
| Palet/material | `<primary/secondary/accent, wood/stone/metal appearance, floor>` |
| Landscape / exterior world | `<path, trees foreground/mid/background, planting, fence, neighboring context>` |
| Iklim/waktu/cahaya | `<sky/weather appearance, sun direction, daylight hardness, practical lights, consistent window views>` |
| Living | `<layout, hubungan sofa–TV/fireplace–coffee table–window–stairs, ceiling, materials>` |
| Kitchen | `<posisi sink/range/island/window, cabinetry, finishes, hubungan dengan living>` |
| Bedroom | `<bed position, headboard, window/wardrobe relation, textiles, lighting>` |
| Bathroom | `<vanity/tub/shower/toilet, fixtures, tile, windows, material and scale>` |
| Arah ruang/logika bangunan | `<rumah satu kesatuan; exterior entry → living; kitchen nearby; posisi lantai/jendela masuk akal>` |
| Look gambar/video | `<photorealistic, camera height, contrast, consistent optics/perspective, 9:16>` |
| Yang dilarang berubah | `<jumlah lantai, roofline, bentuk jendela, pintu, material, furniture anchor, weather, layout, lighting>` |

**Audit lock:** `<apa yang masih perkiraan/belum terlihat di sumber; keputusan kreatif yang mengisinya>`. **Persetujuan user atas Design Lock + storyboard:** `<pesan/status>`.

## E. Storyboard video — waktu final dan waktu lokal Omni

### E1. Pembagian default (boleh diubah dengan aturan ketat)

| Shot ID | Scene | Timeline final | Clip & waktu lokal | Durasi | Titik transisi |
| --- | --- | --- | --- | ---: | --- |
| S01 | **EXTERIOR HOOK** | **0–6s** | A 0–6s | **6s WAJIB MINIMUM** | Hard cut → Living pada A:6s |
| S02 | Living | 6–10s | A 6–10s | 4s | Akhir Clip A; join ke Clip B |
| S03 | Kitchen | 10–14s | B 0–4s | 4s | Hard cut → Bedroom pada B:4s |
| S04 | Bedroom | 14–17s | B 4–7s | 3s | Hard cut → Bathroom pada B:7s |
| S05 | Bathroom | 17–20s | B 7–10s | 3s | Video end pada B:10s |

**Timeline lokal SELALU restart pada 0** untuk setiap generasi. Clip B tidak boleh diberi instruksi lokal “10–20s”. Clip A dan B masing-masing tepat 10 detik; jumlah total 20 detik. Bila jumlah/urutan shot direvisi, gantilah tabel **dan** dua storyboard/prompt, bukan hanya menambah baris. Exterior pertama tetap outdoor-only **≥6 detik**. Perpindahan Clip A→Clip B terjadi saat penyambungan; **bukan** cut di dalam Prompt A.

### E2. Deskripsi shot **wajib lengkap**, bukan nama ruangan saja

Isi satu blok berikut untuk **setiap** shot di E1; ulang bila ada tambahan shot.

#### S01 — Exterior
- `source_DNA_ids/shot_ids/fields`: `<utama shot-01 plus pendukung jika ada>`
- `image_id`: `IMG-01`; `clip`: A; `local/global time`: `0–6s / 0–6s`
- `first_frame / framing_start / view_angle`: `<rumah utuh terbaca sejak frame 0, sudut, foreground>`
- `focal_subject`: `<entry/roof/terrace/hero feature>`
- `camera.movements + speed`: `<contoh dolly_in+subtle_tracking_right, slow; disesuaikan sumber>`
- `reveal_path / first→mid→last`: `<detail baru yang muncul di jalur kamera>`
- `framing_end`: `<tampak medium, objek tetap konsisten>`
- `architecture_anchors`: `<roofline, door, windows, facade texture, stairs>`
- `furniture_props_anchors`: `<porch props bila ada>`
- `environment_anchors`: `<path, lawn, tree locations, foreground>`
- `lighting, mood, continuity`: `<sky/daylight direction/exterior lights; views interior kompatibel>`
- `transition_out`: `hard cut at local 6s to living`
- `unknowns / risk`: `<jangan mengarang bukti>`

#### S02 — Living Room
- `source_DNA_ids/shot_ids/fields`: `<...>`; `image_id`: `IMG-02`; `clip/local/global`: A `6–10s / 6–10s`
- `first_frame / framing_start / view_angle`: `<...>`
- `focal_subject`: `<sofa / TV / fireplace / window>`
- `camera.movements + speed`: `<...>`; `reveal_path / first→mid→last`: `<...>`; `framing_end`: `<...>`
- `architecture_anchors`: `<ceiling/window/walls>`; `furniture_props_anchors`: `<sofa/table/TV position>`
- `environment_anchors`: `<consistent garden through windows>`; `lighting/mood/continuity`: `<...>`
- `transition_out`: `clip A ends at 10s; join to B kitchen`; `unknowns/risk`: `<...>`

#### S03 — Kitchen
- `source_DNA_ids/shot_ids/fields`: `<...>`; `image_id`: `IMG-03`; `clip/local/global`: B `0–4s / 10–14s`
- `first_frame / framing_start / view_angle`: `<...>`
- `focal_subject`: `<range/island/sink>`
- `camera.movements + speed`: `<...>`; `reveal_path / first→mid→last`: `<...>`; `framing_end`: `<...>`
- `architecture_anchors`: `<cabinet/window/ceiling>`; `furniture_props_anchors`: `<island/tools/appliance positions>`
- `environment_anchors`: `<consistent exterior view>`; `lighting/mood/continuity`: `<...>`
- `transition_out`: `hard cut at local B:4s to bedroom`; `unknowns/risk`: `<...>`

#### S04 — Bedroom
- `source_DNA_ids/shot_ids/fields`: `<...>`; `image_id`: `IMG-04`; `clip/local/global`: B `4–7s / 14–17s`
- `first_frame / framing_start / view_angle`: `<...>`
- `focal_subject`: `<bed/headboard/window>`
- `camera.movements + speed`: `<...>`; `reveal_path / first→mid→last`: `<...>`; `framing_end`: `<...>`
- `architecture_anchors`: `<windows/ceiling/walls>`; `furniture_props_anchors`: `<bed/nightstands/wardrobe positions>`
- `environment_anchors`: `<window view matching environment>`; `lighting/mood/continuity`: `<...>`
- `transition_out`: `hard cut at local B:7s to bathroom`; `unknowns/risk`: `<...>`

#### S05 — Bathroom
- `source_DNA_ids/shot_ids/fields`: `<...>`; `image_id`: `IMG-05`; `clip/local/global`: B `7–10s / 17–20s`
- `first_frame / framing_start / view_angle`: `<...>`
- `focal_subject`: `<vanity/tub/shower>`
- `camera.movements + speed`: `<...>`; `reveal_path / first→mid→last`: `<...>`; `framing_end`: `<...>`
- `architecture_anchors`: `<tile/window/wall>`; `furniture_props_anchors`: `<mirror/fixtures/tub relation>`
- `environment_anchors`: `<window outdoor appearance where visible>`; `lighting/mood/continuity`: `<...>`
- `transition_out`: `video_end at B:10s`; `unknowns/risk`: `<...>`

### E3. Storyboard per generasi (untuk user dan Prompt A/B)

| Klip | Per-shot storyboard ringkas | Hero detail / tujuan | Cut yang diminta |
| --- | --- | --- | --- |
| **A — 10s** | `S01 exterior 0–6s` → `S02 living 6–10s` | `<rumah hero, opening movement; living focal/reveal>` | `hard cut pada A:6s` |
| **B — 10s** | `S03 kitchen 0–4s` → `S04 bedroom 4–7s` → `S05 bathroom 7–10s` | `<kitchen function, bedroom calm, bath payoff>` | `hard cut B:4s dan B:7s` |

**Pemeriksaan storyboard otomatis/manual:** A `6+4=10`; B `4+3+3=10`; clip B waktu global = lokal+10; frame pertama exterior; semua shot memiliki sumber, image ID, kamera+reveal; tidak ada gap/overlap; hero feature visual terbaca. Jika storyboard berbeda, ubah semua bagian E–G yang terdampak.

## F. Master images — **pilih A DEFAULT atau B atas permintaan**

**Rute dipilih:** `A_DEFAULT / B_REQUESTED`. **Alasan/permintaan user untuk B:** `<pesan atau tidak ada>`.

### F1. Mapping aset nyata dan status persetujuan

| Image ID | Shot / Clip | Isi visual sesuai Design Lock | Sumber aset (hanya jika nyata) | Mode A/B | Status QA & persetujuan |
| --- | --- | --- | --- | --- | --- |
| **IMG-01** | S01/A exterior | `<framing awal, facade, landscape>` | `<file/link terverifikasi atau BELUM>` | `<A/B>` | `<BELUM / revisi / approved>` |
| **IMG-02** | S02/A living | `<...>` | `<...>` | `<A/B>` | `<...>` |
| **IMG-03** | S03/B kitchen | `<...>` | `<...>` | `<A/B>` | `<...>` |
| **IMG-04** | S04/B bedroom | `<...>` | `<...>` | `<A/B>` | `<...>` |
| **IMG-05** | S05/B bathroom | `<...>` | `<...>` | `<A/B>` | `<...>` |

**Catatan penting:** 5 image adalah default untuk 5 shot. Storyboard berbeda → ubah jumlah baris mapping dan prompt/asset yang diperlukan. **Prompt teks belum dianggap aset gambar.** Jangan mengisi tautan file yang belum dibuat/diverifikasi.

### F2. Opsi A — AI langsung membuat master image (DEFAULT)

- Setelah Design Lock dan storyboard disetujui, AI membuat **lima gambar** orisinal (atau sesuai jumlah shot yang disepakati), **dengan komposisi frame awal S01–S05**, bukan gambar ruangan generik.
- Gunakan identitas sama dan anchor dari `D`; tampilkan tiap gambar berlabel `IMG-ID/Shot`.
- Periksa atap, pintu/jendela, taman/views, lantai, furnitur, pencahayaan, perspektif; perbaiki gambar yang tidak konsisten.
- **Catatan hasil yang benar-benar dibuat:** `<untuk setiap gambar: status, catatan kualitas, tautan/attachment bila tersedia>`.

### F3. Opsi B — AI menyiapkan prompt gambar (HANYA jika diminta)

Pengguna menghasilkan gambar sendiri dan mengunggahnya untuk QA. **Tuliskan lima prompt Inggris terpisah**, menggambarkan rumah yang **sama** dan mengambil komposisi dari `E2`; jangan menganggap template di bawah sudah siap dipakai sebelum slot diganti.

**IMG-01 / Exterior — prompt image**

~~~text
Create a photorealistic vertical 9:16 architectural still image for the FIRST FRAME of a home-tour video.
HOUSE IDENTITY: <full shared Design Lock from section D>.
EXTERIOR COMPOSITION: <S01 first_frame, view_angle, foreground, middle ground, background>.
HERO FOCUS: <S01 focal_subject, facade geometry, roof, doors/windows, entrance>.
LANDSCAPE AND LIGHT: <S01 environment + weather + sun direction + practical lights>.
ANIMATION READY: Leave realistic spatial depth and room for <S01 camera movement and reveal>.
CONSISTENCY: Exactly the same home described in the Design Lock; no extra stories, changed windows, random materials, signs, people, text, watermarks, distortions.
~~~

**IMG-02 / Living — prompt image**

~~~text
Create a photorealistic vertical 9:16 architectural still for Shot S02 of THE SAME HOUSE.
HOUSE IDENTITY: <same shared Design Lock, especially roof-adjacent window system, palette, floor and natural-light direction>.
LIVING ROOM FIRST FRAME: <S02 framing_start + view_angle>.
SPATIAL ANCHORS: <sofa/TV or fireplace/window/coffee table positions; ceiling and wall geometry>.
HERO SUBJECT AND REVEAL: <S02 focal_subject; room area to reveal when animated>.
LIGHT AND OUTDOOR VIEW: <consistent garden/weather seen through the living windows>.
No design drift, no changed architecture, no added furniture, no people, captions, logos, watermarks, warped perspective.
~~~

**IMG-03 / Kitchen — prompt image**

~~~text
Create a photorealistic vertical 9:16 still for Shot S03 in THE SAME HOUSE.
HOUSE IDENTITY: <shared Design Lock for facade/interior material palette, doors/windows, lighting>.
KITCHEN FIRST FRAME: <S03 starting view angle and focal subject>.
LAYOUT ANCHORS: <island/peninsula, sink, cooking range, windows, cabinetry, appliance locations>.
CAMERA REVEAL PREPARATION: <S03 planned motion and what becomes visible>.
LIGHT/ENVIRONMENT: <same time of day, window views, natural and warm task lighting>.
Maintain exact room geometry, fixtures and palette; no people, text, logos, watermarks, distortions.
~~~

**IMG-04 / Bedroom — prompt image**

~~~text
Create a photorealistic vertical 9:16 still for Shot S04 of THE SAME HOUSE.
HOUSE IDENTITY: <same full Design Lock; consistent window shape, flooring, palette, exterior world>.
BEDROOM FIRST FRAME: <S04 framing_start and camera view angle>.
SPATIAL ANCHORS: <bed/headboard, nightstands, wardrobe/window placement, ceiling and textures>.
CAMERA REVEAL PREPARATION: <S04 camera movement, path and intended end framing>.
LIGHT: <same daylight direction and compatible warm bedroom fixtures>.
No unrelated design, no new openings, missing furniture, people, captions or visual distortion.
~~~

**IMG-05 / Bathroom — prompt image**

~~~text
Create a photorealistic vertical 9:16 still for Shot S05 in THE SAME HOUSE.
HOUSE IDENTITY: <consistent Design Lock palette, windows, materials, geometry and lighting>.
BATHROOM FIRST FRAME: <S05 framing_start, view_angle and hero fixture>.
SPATIAL ANCHORS: <vanity, sink, mirror, shower/tub, toilet, tile and hardware placement>.
CAMERA REVEAL PREPARATION: <S05 planned pan/dolly and endpoint/final visual payoff>.
LIGHT AND VIEW: <same world and time of day; window view consistent if visible>.
No morphing, distorted fixtures, wrong materials, people, logos, watermarks, text.
~~~

**Gambar yang diunggah user:** `<IMG-01..IMG-05 + status review nyata>`. Bila user mengubah mode menjadi A di tengah proses, jangan mengulang ide atau Design Lock yang sudah disetujui.

### F4. Gate gambar sebelum prompt video final

- [ ] Semua gambar yang dibutuhkan **benar-benar tersedia** dan dapat diperiksa, bukan hanya prompt.
- [ ] Aset `IMG-XX` telah dipetakan ke `SXX / Clip A atau B`.
- [ ] Material/roofline/windows/landscape/room furniture dan pencahayaan konsisten.
- [ ] Komposisi dapat bergerak dari *first frame* menuju *last frame* tanpa menghancurkan geometri.
- [ ] **User menyetujui** kumpulan gambar: `<pesan/status>`.

**Jika belum semua lulus:** status `awaiting_images`; bagian G di bawah boleh disusun sebagai **draft**, tetapi **tidak boleh** diklaim final/sudah siap dijalankan.

## G. Google Flow Omni Flash — **DUA prompt video utama**

> **Hanya isi dan finalkan bagian ini setelah Gate F4.** Ganti seluruh placeholder Inggris dengan visual nyata, timing, source assets dan Design Lock yang disetujui. **Jangan asumsikan semua mode Flow menerima 2/3+ gambar sekaligus:** sebelum membuat instruksi upload, periksa fitur model/mode aktual yang digunakan. Jika mode tidak dapat menerima mapping banyak gambar, nyatakan keterbatasan dan sepakati strategi input yang didukung, **tanpa** mengklaim storyboard collage sudah pasti setara dengan referensi per scene.

### G1. Prompt A — Omni Flash, **10s**, Exterior + Living

**Mapping sebelum ditempel:** `IMG-01 → S01 Exterior 0–6s`; `IMG-02 → S02 Living 6–10s`. **Input image mode yang benar-benar tersedia:** `<diuji/dikonfirmasi oleh user atau BELUM>`. **Persetujuan F4:** `<status>`.

~~~text
Create ONE 10-second photorealistic vertical 9:16 architectural home-tour video.
This video is CLIP A, the first half of ONE consistent, original house tour.

HOUSE IDENTITY / CONTINUITY LOCK:
<Insert the complete approved Design Lock, especially architecture, roofline, floors, facade, doors/windows, material palette, environment, daylight, interior spatial logic and lighting.>

APPROVED IMAGE REFERENCES:
<IMG-01: exterior identity and shot S01 starting composition; IMG-02: S02 living room starting composition. Describe exactly how the chosen Flow mode can use these images; do not claim unsupported simultaneous references.>

LOCAL SHOT TIMELINE — 10 seconds total:
0.0–6.0 seconds — SHOT S01: EXTERIOR HOOK. For the FULL SIX SECONDS the primary visible scene stays OUTSIDE the house. Show the complete recognizable house in the opening frame. Start from <S01 framing_start/view_angle>; focus on <S01 focal_subject>. Move camera <S01 movements/speed> and progressively reveal <S01 reveal_path and exact landmark positions>. End with <S01 framing_end> while preserving roof, doors, windows, planting and facade materials. Keep house geometry stable.
HARD CUT at local 6.0 seconds; do not morph through walls or dissolve the exterior into furniture.
6.0–10.0 seconds — SHOT S02: LIVING ROOM. Start from <S02 framing_start/view_angle>. Keep <S02 furniture+architecture anchors and light direction>. Camera <S02 movements/speed>; reveal <S02 reveal_path> and finish on <S02 framing_end>. This room must belong to the exact same house established in S01.

GLOBAL CONSTRAINTS:
Stable architecture and spatial layout, matching windows, natural materials, consistent daylight/weather, smooth deliberate camera motion, clean cut, no scene blending, no geometry warp, no object pop-in, no extra rooms, no people, captions, logos or watermarks.
Output exactly 10 seconds, portrait 9:16. End at the living-room shot, ready for a hard edit to CLIP B.
~~~

### G2. Prompt B — Omni Flash, **10s**, Kitchen + Bedroom + Bathroom

**Mapping:** `IMG-03 → S03 Kitchen 0–4s`; `IMG-04 → S04 Bedroom 4–7s`; `IMG-05 → S05 Bathroom 7–10s`. **Input image mode tersedia:** `<diuji/dikonfirmasi atau BELUM>`. **Design Lock harus identik dengan Prompt A.**

~~~text
Create ONE 10-second photorealistic vertical 9:16 architectural home-tour video.
This is CLIP B, the continuation of CLIP A. It is the EXACT SAME ORIGINAL HOUSE, not a redesigned or different property.

HOUSE IDENTITY / CONTINUITY LOCK:
<Repeat the exact approved Design Lock from CLIP A: roof and window language, facade/interior finish, floors, home scale, season/weather, garden views, furniture anchors, illumination and architectural geometry.>

APPROVED IMAGE REFERENCES:
<IMG-03 kitchen → S03, IMG-04 bedroom → S04, IMG-05 bathroom → S05. Specify only reference-input capability truly supported by the selected Flow mode.>

LOCAL SHOT TIMELINE — 10 seconds total:
0.0–4.0 seconds — SHOT S03: KITCHEN. Begin from <S03 framing_start/view_angle> showing <S03 focal_subject and exact cabinetry/island/window positions>. Camera moves <S03 movements/speed>, revealing <S03 reveal_path> and ending at <S03 framing_end>. Preserve the same house materials and lighting.
HARD CUT at local 4.0 seconds to bedroom; no morphing.
4.0–7.0 seconds — SHOT S04: BEDROOM. Begin from <S04 framing_start/view_angle>, anchored by <S04 bed, window, wall and furniture positions>. Move <S04 movements/speed> to reveal <S04 reveal_path>, end with <S04 framing_end>. Maintain the same architecture, daylight, window-view landscape and colour palette.
HARD CUT at local 7.0 seconds to bathroom; no morphing.
7.0–10.0 seconds — SHOT S05: BATHROOM. Begin from <S05 framing_start/view_angle> with <S05 focal_subject, vanity/bath/shower/window relationships>. Move <S05 movements/speed>, reveal <S05 reveal_path> and end on <S05 stable payoff framing>. Match the same fixtures, materials and mood.

GLOBAL CONSTRAINTS:
One house throughout both clips; no sudden layout changes, extra rooms, changed floors, shifting windows or furniture, object pop-in, camera shakes, scene blending, people, text, logos or watermarks.
Output exactly 10 seconds, portrait 9:16, ending on the bathroom composition.
~~~

**Catatan untuk storyboard varian:** jika urutan/jumlah shot berbeda dari E1, **tulis ulang kedua prompt** agar sesuai tabel final; jangan pakai teks 6+4/4+3+3 secara membabi buta. Tetap **satu prompt utama per klip**. Tanggal dan versi prompt: `<...>`. Persetujuan prompt oleh user: `<...>`.

### G3. Pemeriksaan pra-Flow

- [ ] Semua slot `<...>` pada dua prompt final **telah diisi**.
- [ ] Semua gambar yang dirujuk tersedia dan sudah disetujui.
- [ ] Clip A berakhir tepat detik 10; Clip B dimulai lokal 0 dan berakhir lokal 10.
- [ ] Exterior tetap tampil penuh 6 detik sesuai rencana (dan **harus diperiksa ulang pada video aktual**).
- [ ] Hard cut A:6, B:4 dan B:7 sesuai storyboard; tidak mendorong morphing ruang.
- [ ] Kamera setiap shot mempunyai framing awal–akhir, jalur reveal, speed dan tujuan fokus.
- [ ] Tidak ada konflik Design Lock, pencahayaan, lingkungan/jendela, skala/objek.
- [ ] Mode input gambar dan batas multi-shot Flow tidak dilebih-lebihkan.
- [ ] User menerima bahwa dua generasi adalah **baseline**, bukan jaminan pasti sukses.

## H. QA video nyata, revisi dan penerimaan

| Clip / versi | Durasi & rasio nyata | Exterior / batas cut teramati | Kesesuaian adegan dan DNA sinematik | Identitas/material/lighting | Temuan dan perbaikan | Status |
| --- | --- | --- | --- | --- | --- | --- |
| A / `<v1>` | `<BELUM DIUJI>` | `<waktu exterior aktual; cut 6s?>` | `<gerak/framing/reveal>` | `<...>` | `<timestamp dan perbaikan>` | `BELUM / GAGAL / LULUS` |
| B / `<v1>` | `<BELUM DIUJI>` | `<cut lokal 4s dan 7s?>` | `<kitchen, bedroom, bathroom>` | `<...>` | `<timestamp dan perbaikan>` | `BELUM / GAGAL / LULUS` |
| Final gabungan | `<durasi 20s/9:16 diverifikasi?>` | `<eksterior ≥6s?>` | `<alur E→L→K→B→Ba atau varian>` | `<dua klip satu rumah?>` | `<join/edit revision>` | `BELUM / GAGAL / LULUS` |

**QA wajib pada berkas video asli**, bukan semata prompt:
- [ ] Rumah eksterior terlihat jelas mulai frame pertama, **≥6s outdoor-only**.
- [ ] Setiap adegan muncul sesuai storyboard dan membawa detail visual baru.
- [ ] Cut aktual bukan morphing; frame/objek tidak berubah tiba-tiba.
- [ ] Gerak kamera (arah, kecepatan, tujuan reveal) cocok dengan DNA yang dipilih.
- [ ] Bahan, roofline, pintu, window views, furnishing, lighting sesuai Design Lock.
- [ ] Dua klip masing-masing 10s; video gabungan target 20s vertikal 9:16.
- [ ] Artefak/keanehan dan batas kepastian telah dilaporkan jujur.
- [ ] User memberikan keputusan final `<LULUS/GAGAL>`.

**Jika GAGAL:** isi `clip + detik masalah + bukti + penyebab dugaan + revisi prompt/aset + versi retake`. Prioritaskan regenerasi **klip yang bermasalah**, bukan selalu dua klip. Jangan menyebut berhasil sebelum QA user atau pemeriksaan video nyata. Audio/teks (jika dibuat) adalah keputusan tambahan dan tidak diklaim sebagai DNA sumber.

## I. Log perubahan dan persetujuan penyimpanan

| Versi | Apa yang berubah | Alasan/bukti | Gate mana perlu diulang | Status |
| --- | --- | --- | --- | --- |
| `<v1>` | `<...>` | `<...>` | `<idea/design/images/prompt/QA>` | `<draft/approved>` |

**Persetujuan khusus penyimpanan GitHub** (tidak sama dengan persetujuan desain atau video): `<“Simpan produksi IDEA-xxx ke GitHub”, identitas file & pesan user, atau BELUM>`. Target sesudah disetujui: `productions/<IDEA-ID>/production.md`. Sebelum commit, pastikan tidak ada ID/tabrakan file, jangan overwrite diam-diam, dan verifikasi remote setelah menyimpan.

**PERINGATAN:** kata `save now` tetap milik workflow analisis video referensi [`rules/workflow-analysis.md`](../rules/workflow-analysis.md). Jangan membuat/memperbarui `requests/pending`, `references`, `video` atau GitHub Actions hanya karena paket produksi ini disusun.
