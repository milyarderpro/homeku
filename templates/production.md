# HOMEKU — Template Paket Produksi Video v1.2

> **TEMPLATE KOSONG**, bukan paket/video yang sudah dibuat. Gunakan dalam satu sesi produksi setelah user memilih ide. Simpan di `productions/<IDEA-ID>/production.md` **hanya setelah izin GitHub terpisah**.  
> **Aturan operasional yang berlaku:** [`rules/workflow-production.md`](../rules/workflow-production.md) v1.2. **Fakta DNA:** [`knowledge/dna-summary.md`](../knowledge/dna-summary.md).  
> **Perubahan kunci:** **SATU storyboard image kolase** (Opsi A default) / **SATU prompt pembuat kolase** (Opsi B); **dua simple prompt bahasa Indonesia** (satu per 10s clip), plus template koreksi bertahap; **ambience alami tanpa musik**.  
> **Semua tanda `<...>` adalah placeholder untuk diisi pada produksi nyata**. Tidak boleh mengklaim gate lulus atau aset tersedia hanya karena template ini memuat contoh.

## A. Identitas produksi dan persetujuan

| Kolom | Isi |
| --- | --- |
| `production_id` | `<ID_UNIK_BERDASARKAN_PENGECEKAN_REPO>` |
| `title` | `<judul konsep rumah>` |
| `concept_version` | `<v1>` |
| `status` | `idea_options / idea_selected / design_draft / design_approved / storyboard_image_pending / storyboard_image_approved / prompts_ready / qa_pending / revision_required / final_approved` |
| `source_snapshot` | `<commit SHA tempat data referensi dibaca>` |
| `primary_reference_id` | `<ID utama>` |
| `supporting_reference_ids` | `<ID pendukung A dan B opsional>` |
| `image_route` | **A_DEFAULT_ONE_BOARD** / **B_REQUESTED_ONE_BOARD_PROMPT** / **FALLBACK_SEPARATE_APPROVED** |
| `storyboard_board_id` | **BOARD-01** |
| `storyboard_board_file` | `<nama/path/link nyata atau BELUM>` |
| `storyboard_board_resolution` | `<dimensi asli dari file atau BELUM>` |
| `storyboard_board_mode` | `<referensi/ingredients/storyboard yang terverifikasi di Flow atau BELUM>` |
| `target_format` | **vertical 9:16**, target **20s**, dua generasi 10s |
| `exterior_hook_min_s` | **6s outdoor-only** |
| `audio_policy` | **NO MUSIC**, ambience alami halus saja |
| `prompt_level` | **L1_SIMPLE_DEFAULT** / `L2_CORRECTIVE` / `L3_DETAILED_RESCUE` |
| `gate_1_idea_selected` | `<status + pesan user>` |
| `gate_2_design_storyboard_approved` | `<status + pesan user>` |
| `gate_3_one_board_approved` | `<status + pesan user>` |
| `flow_clip_a_status` | `BELUM / GAGAL / LULUS` |
| `flow_clip_b_status` | `BELUM / GAGAL / LULUS` |
| `video_final_status` | `BELUM / GAGAL / LULUS` |
| `github_save_approval` | **BELUM**, atau `<pesan izin eksplisit produksi + path target>` |

**Urutan:** Gate 1 → Gate 2 → buat **satu** board/prompt board → Gate 3 → dua prompt video ringkas → Flow → QA per shot dan audio → persetujuan final. Revisi aset/desain yang mengubah hasil sebelumnya membatalkan approval bagian terdampak, tetapi tidak mewajibkan mengulang seluruh ide dari nol.

## B. Tiga kandidat ide (Gate 1)

**Wajib menampilkan tiga alternatif yang tidak hanya beda warna; hanya satu diproduksi.**

| ID ide | Nama/arsitektur dan lingkungan | S01 exterior hook ≥6s | Sumber (utama + 1–2 pendukung) dan kontribusi | Gerak kamera, interior, lighting, ritme | Orisinalitas dan risiko |
| --- | --- | --- | --- | --- | --- |
| `IDEA-A` | `<gaya, fasad, taman>` | `<frame0 → reveal pintu/rumah>` | `<ID + shot/field>` | `<dolly/tracking, room layout, hard cut>` | `<perbedaan + hambatan>` |
| `IDEA-B` | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` |
| `IDEA-C` | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` |

**Pilihan user:** `<ID dan pesan>`; **status Gate 1:** `BELUM / DISETUJUI`.

## C. Bukti sumber dan tujuh DNA — data kreatif, bukan panjang prompt

### C1. Tiga referensi dan precedence

| Peran | ID/YAML+laporan+storyboard yang dibaca | Shot/field sumber | Ciri yang dipakai | Ciri yang ditolak / konflik / batas kepastian |
| --- | --- | --- | --- | --- |
| Utama — identitas rumah | `<ID dan URL/path>` | `<shot-XX, architecture.*>` | `<massing, roofline, facade, bukaan>` | `<...>` |
| Pendukung A — lingkungan/interior | `<ID>` | `<shot-XX dan field>` | `<taman, cahaya, interior>` | `<...>` |
| Pendukung B — sinematik/edit (opsional) | `<ID atau tidak dipakai>` | `<shot-XX/framing/camera>` | `<dolly/tracking/reveal/ritme>` | `<...>` |

**Precedence:** Design Lock **yang disetujui** > karakter arsitektur sumber utama > inspirasi pendukung. `common_regions` adalah asosiasi wilayah **gaya**, bukan geolokasi. Jangan mengklaim audio atau virality dari analisis yang hanya visual.

### C2. DNA Trace (isi tujuh lapisan, tanpa terkecuali)

| DNA | [FAKTA REFERENSI]: ID / shot / field + observasi | [INTERPRETASI] | [KREASI BARU]: implikasi untuk panel, shot/kamera | Ketidakpastian |
| --- | --- | --- | --- | --- |
| **DNA-01 Hook exterior** | `<...>` | `<...>` | `<frame0 dan outdoor ≥6s; panel S01>` | `<...>` |
| **DNA-02 Arsitektur** | `<...>` | `<...>` | `<massing/atap/jendela dan semua panel>` | `<...>` |
| **DNA-03 Lingkungan** | `<...>` | `<...>` | `<foreground, path, foliage, window view>` | `<...>` |
| **DNA-04 Interior** | `<...>` | `<...>` | `<sofa/TV/island/bed/vanity dan hubungan ruang>` | `<...>` |
| **DNA-05 Sinematografi** | `<...>` | `<...>` | `<framing awal+akhir, dolly/tracking, parallax>` | `<...>` |
| **DNA-06 Lighting/Mood** | `<...>` | `<...>` | `<window light, lamp, material, weather consistency>` | `<...>` |
| **DNA-07 Editing/Narasi** | `<...>` | `<...>` | `<scene order, durations, hard cuts>` | `<...>` |

**Jejak keputusan wajib:** `<fitur → reference_id + shot_id + field_path → fakta → adaptasi → perubahan orisinal>`. Semua rincian tujuh DNA **tetap tercatat**, tetapi **tidak otomatis disalin verbatim ke prompt Flow Level 1**.

## D. Design Lock — satu rumah yang sama dalam lima panel dan dua klip

| Anchor | Kunci yang disetujui (isi lengkap setelah Gate 2) |
| --- | --- |
| Jenis/gaya/keunikan | `<orisinalitas rumah>` |
| Massa, skala, level, atap | `<ukuran tampak, slope, gable, chimney>` |
| Fasad, pintu dan jendela | `<material/warna/posisi, frame type, bukaan>` |
| Palet dan tekstur | `<stone/wood/paint/floor/metal>` |
| Lokasi visual dan lanskap | `<path, foreground trees, taman, background, cuaca tampak>` |
| Pemandangan dari jendela | `<landscape dan arah/daylight yang identik>` |
| Living | `<posisi lengkap fireplace/TV, sofa, chair, table, window, rug>` |
| Kitchen | `<island, range, sink, cabinetry, window dan hubungan ke living>` |
| Bedroom | `<bed, side tables, wardrobe, window, ceiling, textiles>` |
| Bathroom | `<vanity, shower/tub, window, fixtures, materials>` |
| Mood/cahaya/waktu | `<arah dan sifat cahaya, warm practical lighting, weather>` |
| Persyaratan gambar | **Kanvas 3:2; panel wide/readable; komposisi objek tidak terpotong; detail tinggi** |
| Persyaratan kamera | `dolly in/out`, `tracking right/left` atau kombinasi, speed natural, parallax teramati |
| Konsistensi / larangan | `<atap, jendela, posisi objek, pemandangan, furnitur, lighting tidak berubah>` |

**Gate 2:** user menyetujui Design Lock **dan** storyboard: `<pesan dan status>`.

## E. Storyboard dua klip — data detail untuk kamera dan papan referensi

### E1. Timeline default dan peta panel

| Panel | Adegan | Final (global) | Klip (waktu lokal) | Durasi | Cut |
| --- | --- | --- | --- | ---: | --- |
| **S01** | **Exterior** | **0–6s** | **A 0–6s** | **6s outdoor-only minimum** | Hard cut A:6s |
| **S02** | Living Room | 6–10s | A 6–10s | 4s | End A; join B |
| **S03** | Kitchen | 10–14s | B 0–4s | 4s | Hard cut B:4s |
| **S04** | Bedroom | 14–17s | B 4–7s | 3s | Hard cut B:7s |
| **S05** | Bathroom | 17–20s | B 7–10s | 3s | End B |

**Validasi:** A 6+4=10; B 4+3+3=10; global 20. Pada Clip B, local time **kembali ke 0**, bukan 10. Durasi outdoor dihitung sampai interior tampil, **bukan** sampai akhir shot gabungan. Jika storyboard berubah: perbarui panel, total waktu, mapping, prompt dan approval; tetap dua 10s dan exterior ≥6s.

### E2. Shot detail — satu baris setiap shot

Data di bawah harus **diisi konkret** meskipun prompt final singkat. Framing awal tiap panel **wide enough** untuk memperlihatkan susunan utama ruangan pada awal shot; gerak selesai sebelum cut.

| Shot | Source DNA: ID/shot/field | Framing awal, view-angle dan focal | Gerak kamera + speed + reveal path | Framing akhir | Objek/arsitektur/lingkungan dan cahaya terkunci | Transisi/risiko |
| --- | --- | --- | --- | --- | --- | --- |
| **S01** | `<...>` | `<rumah utuh di frame 0, foreground>` | `<dolly in + tracking right, speed natural, path/entry reveal>` | `<fasad/entry masih exterior>` | `<roof, porch, windows, trees, path, daylight>` | `hard cut A:6; jangan masuk interior sebelum 6s` |
| **S02** | `<...>` | `<wide: fireplace, sofa, armchair, table, window terbaca>` | `<tracking right + dolly in, parallax dan seating reveal>` | `<susunan living tetap utuh, tidak terpotong>` | `<jendela, sofa, chair, rug, fireplace, light>` | `end A:10; terlalu sempit = gagal` |
| **S03** | `<...>` | `<wide kitchen: island, range, sink, window>` | `<tracking+dolly, island parallax, cabinet reveal>` | `<island/kitchen tetap readable>` | `<cabinet, appliance, materials, window view>` | `hard cut B:4; jangan zoom palsu` |
| **S04** | `<...>` | `<wide bedroom: bed, sides, window>` | `<diagonal dolly out+tracking right, bed/window parallax>` | `<bed dan furniture utama utuh>` | `<bed, ceiling, textiles, light>` | `hard cut B:7; jangan terpotong` |
| **S05** | `<...>` | `<wide bathroom: vanity, tub, window, shower>` | `<tracking right+dolly, vanity→tub parallax>` | `<bath payoff lengkap dan stabil>` | `<vanity, fixture, tub, stone/tile, window>` | `end B:10; lengkap` |

**Sinematografi wajib:** tidak cukup menulis “kamera sinematik”. Tentukan **posisi awal → lintasan bergerak → objek foreground yang bergeser relatif background → komposisi akhir**. Jangan menggunakan gerak terlalu lambat hingga ruang tidak sempat terungkap dalam 3–4s. Ketentuan objek yang lengkap berpengaruh saat membuat panel, bukan hanya ketika menulis prompt.

### E3. Storyboard per generasi

| Klip | Panel yang dipilih dari BOARD-01 | Alur lokal (10s) | Gerak yang diharapkan | Audio |
| --- | --- | --- | --- | --- |
| A | **S01 + S02** | Exterior 0–6 → hard cut → Living 6–10 | `<S01 movement>` lalu `<S02 movement>` | Angin winter lembut; fireplace crackle bila tampak |
| B | **S03 + S04 + S05** | Kitchen 0–4 → hard cut → Bedroom 4–7 → hard cut → Bath 7–10 | `<gerakan tiga shot yang logis>` | Quiet natural indoor room tone |

## F. SATU storyboard image — Step 4: Opsi A atau B

### F1. Peta satu aset untuk semua shot

| Aset | Konten / panel | Susunan dan kualitas | Identitas penggunaan | Status |
| --- | --- | --- | --- | --- |
| **BOARD-01** | **S01 Exterior, S02 Living, S03 Kitchen, S04 Bedroom, S05 Bathroom** | **S01+S02 di atas; S03+S04+S05 di bawah**; kanvas landscape ~3:2; target resolusi native **3072×2048** atau lebih jika tersedia; ruangan lengkap | **SATU image** yang sama di Clip A dan Clip B sebagai *reference sheet* | `BELUM / REVISI / APPROVED_BY_USER` |

**Aturan resolusi:** ukuran 3072×2048 adalah **target bersyarat**, bukan klaim bahwa image generator pasti mendukungnya. Catat dimensi asli file. Jika hasil hanya 1536×1024, periksa apakah semua panel tetap jelas; jangan menaikkan angka lewat upscale lalu mengklaim detail meningkat. Pastikan teks label S01–S05 terbaca dan panel interior **bukan close-up sempit**.

### F2. Opsi A DEFAULT — AI langsung menghasilkan satu kolase

- Buat **satu** gambar gabungan resolusi terbaik yang tersedia, dengan **dua panel besar di atas** dan **tiga panel di bawah**. **Jangan hasilkan lima master image terpisah sebagai default**.
- Tiap panel bertindak sebagai referensi **komposisi wide** untuk adegan masing-masing. Ada foreground/midground/background; fireplace+sofa+kursi+meja+jendela (Living), island+range+sink+window (Kitchen), bed+nightstands+window (Bedroom), vanity+tub+shower+window (Bathroom).
- Label dan durasi boleh berada pada banner **di luar isi adegan panel**; border jangan menutupi fitur. Semua panel memakai **satu Design Lock**.
- Laporkan bila resolusi terbatas atau panel tidak konsisten. Lakukan revisi **panel bermasalah saja jika edit terarah mungkin**, jika tidak buat ulang board dan review seluruh panel.
- **File nyata/dimensi/keterbacaan:** `<link atau attachment nyata, WxH, catatan QA>`.

### F3. Opsi B — satu prompt gambar kolase jika diminta

**Satu prompt (Bahasa Indonesia) untuk satu image yang berisi lima panel**, bukan lima prompt. Isi di bawah dengan Design Lock dari bagian D dan isi panel dari E2.

~~~text
Buat SATU gambar storyboard fotografi arsitektur fotorealistik dengan kanvas landscape sekitar rasio 3:2, resolusi setinggi mungkin secara native. Target 3072×2048 piksel atau lebih tinggi jika generator mendukung; jangan mengurangi keterbacaan masing-masing panel.

Gambar ini adalah kolase storyboard lima panel dalam SATU image, bukan lima file terpisah:
BARIS ATAS, dua panel besar:
- S01 — Exterior (0–6s): <rumah, massa, facade, lanskap, framing wide, hero subject>
- S02 — Living Room (6–10s): <tata ruang luas: fireplace, sofa, kursi, coffee table, jendela, plafon>
BARIS BAWAH, tiga panel:
- S03 — Kitchen (10–14s): <island, range, sink, cabinetry, window dalam satu pandangan>
- S04 — Bedroom (14–17s): <bed, kedua sisi, jendela, pencahayaan dan ceiling>
- S05 — Bathroom (17–20s): <vanity, mirror, bathtub, shower, window dalam satu pandangan>

DESIGN LOCK SATU RUMAH:
<masukkan Design Lock yang sudah disetujui: bentuk, material, warna, jendela, interior, lanskap, waktu/cuaca, arah cahaya>

SEMUA PANEL:
Komposisi wide architectural view; setiap ruangan hampir seluruhnya terbaca. Jangan crop furnitur/objek hero; pertahankan foreground, midground dan background yang masuk akal untuk animasi dolly/tracking dengan parallax. Jaga bentuk jendela, material, lighting dan outdoor window views konsisten. Fotorealisme tinggi dan detail jelas di tiap panel.

Beri label S01–S05 dan nama ruangan pada banner kecil yang tidak menimpa isi foto. Pemisah panel tipis dan rapi. Hindari teks liar di dalam foto, panel duplikat, objek cacat, geometri mustahil, orang, watermark dan logo.
~~~

**Upload user:** `<BOARD-01 / belum>`. **Prompt image bukan aset gambar**; sebelum gambar diunggah, Gate 3 belum lulus.

### F4. QA board dan persetujuan Gate 3

- [ ] Ada **satu file gambar**, sudah tersedia dan dapat diperiksa; catat dimensi asli serta mode A/B.
- [ ] Lima panel sesuai urutan dua atas + tiga bawah; S01–S05 benar dan dapat dibaca; tidak ada panel tertukar/terduplikasi.
- [ ] Panel interior wide; seluruh objek hero hampir lengkap; tidak ada elemen penting terpotong oleh panel.
- [ ] Detail panel terbaca pada resolusi aktual, cukup untuk referensi; target high resolution dipenuhi **jika tersedia** atau keterbatasan dijelaskan.
- [ ] Satu Design Lock dan lingkungan/window view/lighting konsisten antara panel.
- [ ] Kedalaman ruang memungkinkan **dolly/tracking dengan parallax**, bukan terikat pada satu crop statis.
- [ ] **User menyetujui BOARD-01**: `<pesan user, status>`.

**Fallback jika Flow salah membaca board:** jangan mengklaim fitur Flow yang tidak terverifikasi. Jika mode referensi storyboard tersedia, gunakan itu. Jika Flow menampilkan kolase, beralih hanya setelah persetujuan user ke *crop panel terverifikasi* atau **lima gambar terpisah**. Catat `FALLBACK_SEPARATE_APPROVED`, mapping shot dan approval baru; tidak otomatis mengulang ide. Bila mode input hanya *first/last frame*, jangan memakai board sebagai frame awal.

## G. Google Flow — DUA PROMPT LEVEL 1 SINGKAT (Bahasa Indonesia)

> **Khusus setelah Gate 3 lulus.** Ini contoh format *final yang tinggal diisi referensi proyek*, bukan perintah membuat lima video/prompt. Gunakan satu **BOARD-01** yang sama untuk Clip A dan B bila mode Flow mendukung gambar referensi. Pada mode yang belum terbukti mendukung storyboard, jelaskan keterbatasannya; jangan menganggap satu image kolase otomatis menghasilkan lima scene bersih.

**Aturan prompt default:** cukup sebut urutan shot/panel dan durasi, gerakan kamera yang diizinkan, parallax dan kelengkapan ruang, larangan layout kolase/morphing, serta **tanpa musik**. **Jangan** menyalin bagian C–E yang panjang ke prompt utama. Instruksi spesifik hanya jika QA menunjukkan gagal.

### G1. PROMPT A — Clip A, Exterior 6s + Living 4s

~~~text
Buat video tur rumah fotorealistik vertical 9:16 dengan durasi 10 detik.

Gunakan SATU gambar kolase storyboard sebagai visual reference. Untuk clip ini, gunakan HANYA:
- S01 Exterior: 6 detik pertama, rumah tampak sejak frame pertama dan tetap di luar selama 6 detik penuh.
- S02 Living Room: 4 detik berikutnya, setelah hard cut.

Gerakan kamera hanya dolly in/out, tracking right/left, atau kombinasinya. Pilih yang paling sesuai, dengan kecepatan natural: jangan terlalu lambat dan jangan terlalu cepat. Rumah dan hampir seluruh susunan living room harus langsung terbaca, tidak terpotong saat shot berakhir.

Hasil harus seperti real moving-camera architectural home tour dengan perspective change dan parallax nyata, bukan slideshow atau digital zoom pada gambar. Gunakan hard cut bersih antarruang, jaga desain rumah konsisten. Jangan tampilkan kolase, panel split, border atau teks label storyboard dalam video.

AUDIO: JANGAN ADA MUSIK, vokal, narasi atau soundtrack. Hanya ambient natural sound yang halus.
~~~

### G2. PROMPT B — Clip B, Kitchen 4s + Bedroom 3s + Bathroom 3s

~~~text
Buat video tur rumah fotorealistik vertical 9:16 dengan durasi 10 detik, melanjutkan rumah yang SAMA dari Clip A.

Gunakan SATU gambar kolase storyboard yang sama sebagai visual reference. Untuk clip ini, gunakan HANYA:
- S03 Kitchen: 4 detik pertama.
- S04 Bedroom: 3 detik berikutnya, setelah hard cut.
- S05 Bathroom: 3 detik terakhir, setelah hard cut.

Gerakan kamera hanya dolly in/out, tracking right/left, atau kombinasinya. Sesuaikan masing-masing ruang; kecepatan natural, jangan terlalu lambat atau cepat. Tunjukkan hampir seluruh kitchen, bedroom dan bathroom dengan susunan furnitur serta fitur penting terbaca dan tidak terpotong.

Video harus terasa seperti real moving-camera architectural home tour, dengan perspective change dan parallax foreground–background yang terlihat. Bukan animasi kolase, slideshow atau digital zoom. Gunakan hard cut, satu desain rumah, jendela dan pencahayaan konsisten. Jangan tampilkan border/panel/label atau teks storyboard.

AUDIO: JANGAN ADA MUSIK, vokal, narasi atau soundtrack. Hanya ambient natural sound yang halus.
~~~

**Perhatian:** prompt ringkas ini adalah **default**, bukan jaminan model mengikuti semua cut atau bisa memakai lima panel. Jika output salah, perbaiki sesuai masalah aktual; jangan langsung membuat prompt panjang.

### G3. Level koreksi — sesuai bukti QA, bukan default

| Level | Kapan dipakai | Template tindakan |
| --- | --- | --- |
| **L1_SIMPLE_DEFAULT** | Generasi pertama | Gunakan G1/G2 apa adanya |
| **L2_CORRECTIVE** | Ada kegagalan spesifik pada klip | **Prompt G1/G2 asli + 1–3 kalimat korektif** yang mengacu shot/timestamp, misal “S02 dimulai wide dan menampilkan sofa, armchair serta fireplace utuh”, “S03 perlu lateral tracking dengan parallax nyata, bukan zoom”, “hapus musik sama sekali” |
| **L3_DETAILED_RESCUE** | L2 gagal berulang pada masalah serupa | Prompt detail **hanya** shot gagal dari E2: framing awal/akhir, lintasan dolly/tracking, focal, anchor, cahaya, negative constraints. Jangan sekaligus menambah instruksi panjang untuk seluruh shot tanpa alasan |

**Catatan retake:** `<clip A/B, level, versi, alasan, timestamp, perbedaan dari prompt awal, apakah board juga direvisi>`.

### G4. Pemeriksaan sebelum menjalankan Flow

- [ ] **Gate 3 lulus**: BOARD-01 asli sudah disetujui dan jelas.
- [ ] Mode Flow benar-benar dapat memakai storyboard image sebagai **referensi**, bukan otomatis menganggap seluruh board sebagai satu first frame.
- [ ] Prompt A hanya S01+S02, waktunya 6+4=10; Prompt B hanya S03+S04+S05, waktunya 4+3+3=10.
- [ ] Bahasa utama prompt **Indonesia**, istilah kamera teknis seperlunya.
- [ ] Kamera bergerak dengan parallax; kebutuhan ruangan utuh dan **no digital zoom** jelas.
- [ ] Ada larangan memunculkan layout kolase, garis panel, label, dan morphing.
- [ ] **NO MUSIC** dan natural ambience jelas untuk dua klip.
- [ ] Tidak ada placeholder belum diganti dalam prompt yang di-copy ke Flow.
- [ ] User mengetahui timing/cut tidak dijamin persis; baseline 2 generate tidak menjamin sukses.

## H. QA video nyata, audio, revisi, dan persetujuan

| Output/versi | Durasi & format terukur | Kualitas kamera: dolly/tracking/parallax, bukan zoom | Ruang utuh; objek tidak terpotong | Exterior/cut/continuity | AUDIO: tidak ada musik, ambience alami | Temuan & tindak lanjut | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Clip A v`<n>` | `<...>` | `<shot S01/S02, timestamp>` | `<Living lengkap?>` | `<outdoor≥6s, cut A:6?>` | `<didengar: ya/tidak, catatan>` | `<revisi>` | `BELUM/GAGAL/LULUS` |
| Clip B v`<n>` | `<...>` | `<S03/S04/S05>` | `<kitchen/bed/bath lengkap?>` | `<B:4/B:7, identitas rumah?>` | `<didengar: ya/tidak>` | `<revisi>` | `BELUM/GAGAL/LULUS` |
| Final 20s | `<...>` | `<semua shot>` | `<...>` | `<global 6/10/14/17, 9:16>` | `<tidak ada musik>` | `<join/retake>` | `BELUM/GAGAL/LULUS` |

**Gagal jika**: (a) Living hanya separuh akibat close-up/camera terlalu pelan; (b) kitchen/bed/bath hanya zoom-out tanpa parallax; (c) objek utama terpotong di akhir; (d) board, teks atau garis panel muncul; (e) eksterior <6s atau cut/ruang hilang/morphing; (f) audio ada musik; (g) rumah berubah antara klip; (h) durasi/aspek tidak memenuhi target.

**Tindakan audio:** periksa **suara aktual**, bukan sekadar ada stream audio. Jika musik muncul, revisi clip/prompt atau, atas persetujuan user, hilangkan audio bermusik lalu tambahkan ambient sound natural secara terpisah. Jangan mengklaim musik berhasil dipisahkan dari ambience tanpa pengujian. **No music** adalah aturan produksi baru, bukan “DNA audio” dari YAML visual.

**Perbaikan lokal:** revisi hanya klip/shot gagal dan bila perlu panel terkait dengan tetap menjaga panel lain; simpan catatan sebelum/sesudah. **`revision_required`** sampai semua tes nyata lulus dan user menyetujui final.

## I. Log perubahan, izin simpan dan batas P3

| Versi | Perubahan board/panel/prompt | Alasan & bukti video | Gate yang diulang | Status |
| --- | --- | --- | --- | --- |
| `<v1>` | `<...>` | `<...>` | `<...>` | `<...>` |

**Penyimpanan GitHub tidak otomatis:** `<pesan eksplisit semisal “Simpan produksi IDEA-001 ke GitHub” atau BELUM>`. Periksa apakah `productions/<IDEA-ID>/production.md` sudah ada, jangan overwrite tanpa persetujuan, commit, lalu baca ulang file remote. Hindari menyimpan MP4/JPEG besar ke repo tanpa instruksi.

**`save now` tetap milik workflow analisis** [`rules/workflow-analysis.md`](../rules/workflow-analysis.md). Jangan memakainya untuk memulai penyimpanan produksi, dan jangan menyentuh `requests/`, `video/`, `references/`, atau Actions.

**Status pilot Snowy Storybook Stone Cottage sebelumnya:** `revision_required` karena cakupan living, gerak kamera, dan musik; **tidak otomatis berubah menjadi LULUS** karena template atau prompt versi baru ditulis. Hanya hasil video aktual versi berikutnya yang dapat membuktikan peningkatan.
