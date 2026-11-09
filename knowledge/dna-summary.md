# HOMEKU — Ringkasan DNA Referensi v1.1 (P1)

> **Status:** basis pengetahuan hasil observasi untuk produksi; **bukan** prompt siap pakai dan belum diuji menghasilkan video.  
> **Tracking:** [Issue #7](https://github.com/milyarderpro/homeku/issues/7) · [PR P1 #9](https://github.com/milyarderpro/homeku/pull/9).  
> **Snapshot sumber:** [`milyarderpro/homeku`, commit `80072accc56f7824d9575f144ed4e88dcf51a8bc`](https://github.com/milyarderpro/homeku/tree/80072accc56f7824d9575f144ed4e88dcf51a8bc), audit **9 November 2026**. Statistik tidak diperbarui otomatis saat `main` berubah.  
> **Sumber berurutan:** `references/<ID>/analysis.yaml` (fakta visual) → `analysis.md` (uraian) → `storyboard.jpg` dan `shot-NN.jpg` (acuan gambar). Untuk produksi, **buka ulang paket lengkap referensi terpilih**; file ini adalah indeks, bukan pengganti analisis tiap shot.

## 0. Cara menggunakan dokumen

**Tujuan:** AI mampu menghasilkan video rumah baru yang memiliki **DNA video referensi secara menyeluruh**, bukan hanya gaya arsitektur. Tujuh unsur wajib yang harus diperhatikan:

1. **Hook eksterior:** komposisi frame pertama, ciri rumah yang ditonjolkan, cara kamera mengungkap rumah.
2. **Arsitektur:** ukuran tampak, massa/atap, fasad, bukaan, material dan identitas desain.
3. **Lingkungan:** taman, foreground, pepohonan, jalur masuk, cuaca yang terlihat, pemandangan dari jendela.
4. **Interior:** hubungan ruang, posisi objek/furnitur, focal subject dan reveal dalam ruangan.
5. **Sinematografi:** framing awal–akhir, sudut pandang, pergerakan, arah, kecepatan.
6. **Pencahayaan dan mood:** cahaya alami/lampu, warna, kontras, kesatuan antarshot.
7. **Narasi visual dan editing:** urutan shot, tempo, pembagian durasi, hard cut atau gerak kontinu, komposisi penutup.

**Alur penggunaan:** baca ringkasan → pilih 1 referensi utama dan 1–2 referensi pendukung → buka YAML/laporan/storyboard referensi tersebut → catat bukti DNA per shot → buat ide orisinal → Design Lock → storyboard → gambar → dua prompt Omni Flash → QA.

Pisahkan setiap keputusan menjadi:
- **[FAKTA REFERENSI]**: observasi yang benar-benar tercatat dengan `reference_id`, `shot-XX` atau field YAML.
- **[INTERPRETASI]**: kesimpulan kreatif yang masuk akal tetapi mungkin tidak pasti.
- **[KREASI BARU]**: elemen yang sengaja diciptakan agar tidak menjiplak referensi.
- **[ATURAN PRODUKSI]**: kebijakan untuk video HOMEKU baru, **bukan** fakta yang diklaim terjadi pada semua video sumber.

**Istilah teknis:** *framing* = area gambar yang terlihat; *dolly-in/out* = pandangan mendekat/menjauh; *tracking* = bergeser; *pan* = mengarahkan pandangan ke kiri/kanan; *reveal* = objek baru mulai tampak; *hard cut* = pindah langsung antarshot tanpa perubahan bentuk/morphing; *focal subject* = objek perhatian utama. Istilah kamera adalah **interpretasi gerak pada layar**, bukan verifikasi alat kamera fisik.

## 1. Audit seluruh dataset

| Indikator | Hasil pada snapshot | Batas interpretasi |
| --- | --- | --- |
| Paket video | **58**: 10 `VID-XXX` lama + 48 `edh...` | Ke-58 memiliki `analysis.yaml`, `analysis.md` dan `storyboard.jpg` |
| Shot dan keyframe | **300** shot; **300** file `shot-NN.jpg` | File diverifikasi **ada**, bukan seluruh isinya ditinjau manual satu per satu |
| Item detail visual | **6.226**: 2.850 arsitektur, 2.504 furnitur/objek, 872 lingkungan | Total item yang dicatat, **bukan** jumlah objek unik |
| Durasi sumber | **15,300–27,233 detik**; median **20,19 detik**, rata-rata **20,57 detik** | Video baru memakai target 20 detik atas keputusan produksi |
| Jumlah shot/video | 3: **1**; 4: **6**; 5: **35**; 6: **14**; 7: **2** | Lima shot paling umum, tetapi tidak wajib |
| Label ritme | `slow` **29**, `moderate` **28**, `slow_to_moderate` **1** | Kecepatan gerak kamera dalam shot bisa berbeda dari ritme edit keseluruhan |
| Shot pembuka | **58 dari 58** dimulai dengan eksterior; **5** masuk dari eksterior→living dalam **satu shot** | Tidak semua durasi shot pembuka adalah waktu eksterior murni |
| Durasi shot pembuka | **12** kurang dari 5 dtk; **33** dari 5 hingga kurang dari 6; **13** minimal 6 | Ini durasi **shot pertama**, bukan selalu durasi outdoor-only |
| Shot pembuka berlabel eksterior ≥6 dtk | **8**: `VID-001`, `VID-002`, `VID-003`, `edh022`, `edh032`, `edh038`, `edh056`, `edh060` | Lima shot ≥6 dtk lainnya mencakup area living: `edh016`, `edh026`, `edh031`, `edh035`, `edh036` |
| Transisi | Umumnya hard/straight cut; sebagian gerak melalui pintu kontinu; beberapa blur/dissolve | Hard cut adalah **pilihan default produksi**, bukan satu-satunya pola referensi |

**Hasil review penting:** klaim bahwa setiap eksterior referensi minimal lima detik **tidak didukung data**. Contohnya [`edh019`](../references/edh019/analysis.yaml) 3,97 detik, [`edh015`](../references/edh015/analysis.yaml) 4,133 detik, [`VID-004`](../references/VID-004/analysis.yaml) 4,73 detik. **[ATURAN PRODUKSI]** keputusan HOMEKU tetap: **shot exterior minimal 6,00 detik yang benar-benar menampilkan bagian luar rumah**, di awal video 20 detik. Ini keputusan kreatif, **bukan bukti durasi 6 detik menyebabkan jutaan views**.

**Kualitas sumber:** seluruh metadata `analysis_quality.human_verified` bernilai `false`; 57 status `draft`, 1 `reviewed`. Waktu cut bersifat estimasi dan beberapa ending visual berbeda sekitar 0,1–0,15 detik dari durasi kontainer. Material, luas bangunan, wilayah geografis, musim, dan jenis pergerakan kamera dapat memiliki ketidakpastian; jangan menyebutnya telah terverifikasi.

## 2. Tujuh lapisan DNA dan penerapan praktis

### DNA-01 — Eksterior sebagai hook visual

**Pola sumber:** frame pertama biasanya langsung memperlihatkan **rumah yang dapat dikenali**, dari sudut depan/wide/tiga-perempat. Kamera bergerak perlahan mendekati pintu atau ke samping untuk membuka informasi fasad. Lanskap ikut membentuk *foreground, middle ground, background*.

- **Whole house → entry reveal:** [`edh058`](../references/edh058/analysis.yaml) shot-01, tampak lebar fasad cottage menjadi pintu lebih dekat, `dolly_in` + `slight_tracking_right`; [`VID-001`](../references/VID-001/analysis.yaml) cottage hijau sage dan porch; [`edh059`](../references/edh059/analysis.yaml) fasad batu dan pintu/balkon.
- **Foreground bergerak melewati rumah:** [`edh060`](../references/edh060/analysis.yaml) shot-01, batang pohon menghalangi sebagian lalu bergeser; [`edh047`](../references/edh047/analysis.yaml) batang pohon dengan tangga masuk; [`edh042`](../references/edh042/analysis.yaml) kanopi daun dan lawn.
- **Fitur unik sebagai akhir gerak:** [`edh038`](../references/edh038/analysis.yaml) tangga luar/teras atap; [`edh020`](../references/edh020/analysis.yaml) lengkung atap dan dinding batu; [`edh052`](../references/edh052/analysis.yaml) porch, jalan masuk, bunga dan palem.

**Saat menulis storyboard:** tetapkan *frame 0*, hero feature, tiga lapisan lanskap, framing awal, jalur kamera dan kecepatannya, kapan detail fasad terungkap, framing akhir, serta titik cut ke living. **Jangan habiskan 6 detik hanya menampilkan daun/langit atau gerak kamera tanpa perubahan visual.** Target luar rumah **≥6 detik**, diukur dari video hasil generasi.

### DNA-02 — Arsitektur, gaya dan skala

Ambil `architecture.primary_style`, `secondary_influences`, `building_scale`, `exterior_features` dan `shots[].visible_details.architectural`. Yang dijaga bukan hanya nama gaya, melainkan **massa rumah, bentuk atap, tingkat/lantai yang tampak, proporsi fasad, jendela/pintu, material tampak, railing, chimney/porch, dan hubungan dengan halaman**.

| Kelompok yang dapat dicari | Referensi representatif | Ciri yang dapat diadaptasi |
| --- | --- | --- |
| Storybook / rustic stone / alpine | [`edh020`](../references/edh020/analysis.yaml), [`edh025`](../references/edh025/analysis.yaml), [`edh057`](../references/edh057/analysis.yaml), [`edh059`](../references/edh059/analysis.yaml) | gable/arch, dinding batu tampak alami, kusen gelap, kayu, suasana hangat kontras lanskap dingin |
| Mediterranean / Spanish revival | [`edh038`](../references/edh038/analysis.yaml), [`edh058`](../references/edh058/analysis.yaml), [`edh050`](../references/edh050/analysis.yaml), [`edh053`](../references/edh053/analysis.yaml) | stucco/plester krem, genteng tampak terracotta, bukaan arch, pintu kayu, taman dan tangga teras |
| Tropical / contemporary | [`VID-005`](../references/VID-005/analysis.yaml), [`edh042`](../references/edh042/analysis.yaml), [`edh052`](../references/edh052/analysis.yaml), [`edh055`](../references/edh055/analysis.yaml) | bentuk terang, jendela luas, kayu, tanaman/palem, daylight |
| Modern farmhouse / cottage | [`edh017`](../references/edh017/analysis.yaml), [`edh041`](../references/edh041/analysis.yaml), [`edh060`](../references/edh060/analysis.yaml), [`VID-001`](../references/VID-001/analysis.yaml) | massa kompak/atap, palet tenang, kusen gelap, porch, lampu hangat |
| Compact, open plan, loft | [`edh033`](../references/edh033/analysis.yaml), [`edh060`](../references/edh060/analysis.yaml), [`edh022`](../references/edh022/analysis.yaml), [`edh057`](../references/edh057/analysis.yaml) | ruang gabungan, efisiensi ruang, loft pada contoh tertentu, skala visual kecil |

**Aturan konflik:** satu referensi **utama** menentukan identitas arsitektur; dua pendukung hanya menyumbang unsur yang disebut eksplisit. Jangan mengambil atap/level rumah alpine sekaligus tropical bungalow tanpa alasan desain. `common_regions` adalah **wilayah asosiasi gaya**, **bukan** lokasi nyata bangunan. Semua geometri final ditentukan dalam **Design Lock rumah baru**.

### DNA-03 — Environment, lanskap, pemandangan jendela

Catat jalan/tangga masuk, tanaman berbunga, lawn, pohon tinggi, kanopi foreground, pagar, hutan/pegunungan jauh, bayangan, cuaca yang **terlihat**, dan **pemandangan dari dalam jendela**.

- **Batu, musim dingin bersalju:** [`edh020`](../references/edh020/analysis.yaml), [`edh025`](../references/edh025/analysis.yaml), [`edh059`](../references/edh059/analysis.yaml).
- **Jalur taman dan bunga:** [`edh058`](../references/edh058/analysis.yaml), [`edh052`](../references/edh052/analysis.yaml), [`edh038`](../references/edh038/analysis.yaml).
- **Pohon tropis dan foreground:** [`edh042`](../references/edh042/analysis.yaml), [`edh047`](../references/edh047/analysis.yaml), [`edh055`](../references/edh055/analysis.yaml).
- **Hutan dan pohon tinggi:** [`edh056`](../references/edh056/analysis.yaml), [`edh060`](../references/edh060/analysis.yaml).

**Aturan kontinuitas:** rumah, arah jalur, jenis lanskap dan pohon besar, cuaca/season appearance, serta pemandangan dari jendela interior harus menjadi **dunia visual yang sama**. Jangan membuat halaman bersalju pada exterior dan taman tropis pada bedroom tanpa konsep yang masuk akal.

### DNA-04 — Interior, furnitur, hubungan ruang dan objek yang diungkap

Kuncinya **bukan** sekadar “living room” atau “kitchen”, melainkan posisi dan hubungan benda: sofa dengan TV/fireplace, bed dengan jendela, island dengan sink/range, bathtub dengan vanity. Tetapkan apa terlihat di frame awal dan apa menjadi terlihat setelah kamera bergerak.

| Adegan | Focal subject dan perubahan tampilan | Contoh sumber |
| --- | --- | --- |
| Living | Sofa/kursi–coffee table–TV/fireplace–jendela/tangga; detail→wide atau wide→detail | [`edh058`](../references/edh058/analysis.yaml) arch TV dan seating/window; [`edh020`](../references/edh020/analysis.yaml) fireplace batu; [`edh047`](../references/edh047/analysis.yaml) living tinggi dan tangga |
| Kitchen | Cabinetry, island/peninsula, hood/range, sink, jendela, backsplash | [`edh058`](../references/edh058/analysis.yaml) peninsula→range; [`edh052`](../references/edh052/analysis.yaml) kitchen krem; [`edh042`](../references/edh042/analysis.yaml) U-shaped kitchen |
| Bedroom | Bed/headboard sebagai jangkar, reveal jendela/ceiling/wardrobe/textile | [`edh058`](../references/edh058/analysis.yaml) dolly-out dari bed ke ruang lebih lebar; [`edh025`](../references/edh025/analysis.yaml) arch batu; [`edh047`](../references/edh047/analysis.yaml) vaulted ceiling |
| Bathroom | Vanity, sink, cermin, shower, bathtub, toilet; perubahan detail→wide atau sebaliknya | [`edh060`](../references/edh060/analysis.yaml) vanity→bathtub; [`edh058`](../references/edh058/analysis.yaml) tub→vanity; [`edh025`](../references/edh025/analysis.yaml) jendela bundar |
| Tambahan | Laundry, walk-in closet, loft, exterior closing bila masuk akal dan cukup waktu | [`edh044`](../references/edh044/analysis.yaml), [`edh055`](../references/edh055/analysis.yaml), [`edh033`](../references/edh033/analysis.yaml), [`edh051`](../references/edh051/analysis.yaml) |

**Untuk gambar master:** satu gambar per shot harus siap sebagai frame pembuka video; kunci bentuk jendela, material lantai, posisi furnitur, benda utama, arah cahaya, dan pemandangan luar. Referensi **tidak menyediakan denah terukur**; ketika membuat rumah baru, periksa sendiri hubungan ruang yang masuk akal.

### DNA-05 — Kamera: framing, sudut, arah, kecepatan, reveal

Ambil `shots[].framing.start`, `framing.end`, `framing.view_angle`, `camera.movements`, `camera.speed`, `focal_subject`, `observation_note` dan `confidence.camera`.

- **Wide→medium/close:** [`edh058`](../references/edh058/analysis.yaml) exterior shot-01 dan kitchen shot-03; [`edh047`](../references/edh047/analysis.yaml) fasad/living.
- **Detail→wide:** [`edh058`](../references/edh058/analysis.yaml) bedroom dan bathroom; [`edh044`](../references/edh044/analysis.yaml) living dimulai dari fireplace lalu menampakkan seating.
- **Lateral pan/tracking:** [`edh052`](../references/edh052/analysis.yaml) living/kitchen; [`edh038`](../references/edh038/analysis.yaml) ruangan sempit; [`edh049`](../references/edh049/analysis.yaml) opening sedikit orbit.
- **Entry kontinu (bukan cut):** [`edh016`](../references/edh016/analysis.yaml), [`edh026`](../references/edh026/analysis.yaml), [`edh031`](../references/edh031/analysis.yaml), [`edh035`](../references/edh035/analysis.yaml), [`edh036`](../references/edh036/analysis.yaml). **Bukan** contoh yang dapat digunakan menghitung outdoor 6 detik.

**Enam elemen wajib pada satu shot:** (1) framing awal, (2) focal subject awal, (3) arah dan kecepatan kamera, (4) urutan objek/area yang muncul, (5) framing akhir, (6) batasan agar bangunan/furnitur tidak berubah. “Cinematic, slow motion” saja **tidak cukup**. Tidak semua gerak yang tampak pasti hasil kamera fisik; bisa berupa zoom/gerakan sintetis.

### DNA-06 — Lighting, warna dan mood

Contoh palet sering melibatkan ivory/cream/off-white, natural/honey wood, beige/stone, black/charcoal pada kusen/fixture, foliage green dan aksen terracotta/sage/rust. Namun setiap konsep boleh memilih **palet konsisten yang berbeda**; DNA bukan berarti semua rumah berwarna sama.

- **Luar:** daylight lembut atau terang, fasad mudah dibaca, lampu dinding/teras hangat. Contoh [`edh058`](../references/edh058/analysis.yaml) daylight cerah; [`edh020`](../references/edh020/analysis.yaml) winter daylight dingin + lampu hangat; [`edh056`](../references/edh056/analysis.yaml) suasana hutan dan cahaya rumah.
- **Dalam:** jendela sebagai sumber cahaya alami, dilengkapi lampu warm dari pendant/sconce/recessed light atau fireplace; contoh [`edh058`](../references/edh058/analysis.yaml), [`edh052`](../references/edh052/analysis.yaml), [`edh047`](../references/edh047/analysis.yaml).
- **Mood:** cozy, inviting, calm, warm dan sebagainya adalah **interpretasi visual**, bukan hasil pengukuran perasaan/retensi penonton.

Kunci warna kusen, kayu, dinding, arah cahaya, cuaca, lampu, kontras dan white balance **dari Clip A ke Clip B**.

### DNA-07 — Struktur narasi dan edit

Pola dominan: **Exterior → Living → Kitchen → Bedroom → Bathroom**, dengan variasi:
- **Tur standar:** [`VID-001`](../references/VID-001/analysis.yaml), [`edh011`](../references/edh011/analysis.yaml), [`edh052`](../references/edh052/analysis.yaml), [`edh059`](../references/edh059/analysis.yaml).
- **Laundry/closet tambahan:** [`edh044`](../references/edh044/analysis.yaml), [`edh055`](../references/edh055/analysis.yaml), [`edh058`](../references/edh058/analysis.yaml).
- **Open plan/loft:** [`edh033`](../references/edh033/analysis.yaml), [`edh057`](../references/edh057/analysis.yaml), [`edh060`](../references/edh060/analysis.yaml).
- **Kembali ke eksterior di akhir:** [`edh047`](../references/edh047/analysis.yaml), [`edh051`](../references/edh051/analysis.yaml), [`edh056`](../references/edh056/analysis.yaml).
- **Transisi pengecualian:** [`VID-001`](../references/VID-001/analysis.yaml) memakai blur dan [`VID-003`](../references/VID-003/analysis.yaml) warm flash/dissolve. Untuk produksi awal Omni Flash, gunakan **hard cut**.

Secara visual, tiap adegan punya fungsi: memperkenalkan rumah → gaya hidup di living → fungsi kitchen → kenyamanan bedroom → detail bathroom. Hindari dua shot berurutan yang tidak memperlihatkan informasi baru. **Ritme edit (jumlah/durasi shot) dan ritme kamera (kecepatan dalam satu shot) harus ditetapkan terpisah.**

## 3. Aturan pemilihan 2–3 referensi dan orisinalitas

1. **Utama (1 ID):** menentukan gaya rumah, roofline/massing, level, fasad, bukaan, kesatuan material dan skala.
2. **Pendukung A (1 ID):** menambahkan elemen **tertentu** seperti taman, pencahayaan atau mood yang cocok.
3. **Pendukung B (opsional, 1 ID):** memberi pola kamera, framing, reveal, atau susunan shot. **Jangan** otomatis mengimpor fasad/atapnya.
4. **Buka sumber lengkap:** jangan membuat klaim spesifik hanya dari baris katalog. Baca `analysis.yaml`, `analysis.md`, dan storyboard untuk ID pilihan.
5. **Periksa konflik:** atap vs gaya, jumlah lantai, jendela, material, iklim, arah sunlight, pemandangan melalui jendela, hubungan ruang. Jika bentrok, pertahankan **Design Lock rumah baru yang telah disetujui**; revisi elemen pendukung.
6. **Hasil baru harus orisinal:** ubah susunan bentuk, proporsi, layout, orientasi, taman/objek dan komposisi. Pertahankan **prinsip visual dan sinematik**, bukan menyalin satu fasad atau seluruh video secara identik.
7. **Catat jejak:** `fitur DNA → ID referensi + shot/field → bukti yang terlihat → penggunaan baru → perbedaan kreatif → ketidakpastian`.

**Contoh (hipotesis kreasi, bukan bukti hasil):** utama `edh058` untuk Mediterranean cottage/eksterior; pendukung `edh052` untuk lanskap tropis; opsional `edh060` untuk penutup bathroom dengan pan dari vanity ke tub. Ketiganya memberi aspek berbeda, tetapi bentuk rumah **baru** harus masuk akal.

### Jejak DNA yang wajib dihasilkan pada setiap ide di P2

| Bagian | Informasi minimum |
| --- | --- |
| `references` | ID utama dan 1–2 ID pendukung, peran spesifik, shot sumber |
| `hook` | Frame pertama, fitur eksterior, posisi awal kamera, reveal, posisi akhir dan ≥6s |
| `architecture` | Gaya, massa, lantai, atap, fasad, bukaan, material tampak |
| `environment` | Foreground, path/taman/pohon, cuaca, view dari jendela |
| `interior` | Posisi objek, material, hubungan furnitur, focal subject tiap ruang |
| `cinematography` | Framing awal–akhir, sudut, gerak + kecepatan + objek yang diungkap |
| `lighting_mood` | Sumber cahaya dan kesatuan visual antarshot |
| `editing` | Urutan shot, durasi, local/global timestamps, transisi, akhir shot |
| `provenance` | Bukti YAML/shot untuk setiap fitur DNA yang diambil |
| `originality_unknowns` | Apa yang berbeda dari sumber dan apa yang belum dapat diverifikasi |

## 4. Contoh DNA menjadi storyboard video (simulasi)

**Konsep ilustratif:** *Tropical Mediterranean Mini Cottage*. Bukan rumah/video yang sudah dibuat.

| Lapisan DNA | Bukti referensi | Pemakaian yang diusulkan |
| --- | --- | --- |
| Hook/exterior/kamera | [`edh058`](../references/edh058/analysis.yaml) shot-01: wide→entry, `dolly_in` + `slight_tracking_right` | Wujud rumah baru sejak frame 0, lalu mendekat ke pintu selama 6 detik |
| Gaya | `edh058`: dinding krem tampak stucco, terracotta-look roof, jendela gelap | Fasad/massa baru dengan prinsip desain senada |
| Lanskap | [`edh052`](../references/edh052/analysis.yaml) shot-01: vegetasi tropis dan jalur masuk | Lanskap baru dengan orientasi konsisten ke pintu |
| Living | `edh058` shot-02: area TV/sofa dan reveal jendela/seating | Penataan living baru, pan perlahan untuk memperlihatkan ruang |
| Kitchen | `edh058` shot-03: peninsula/area kompor, dolly+tracking | Kamera bergerak ke area focal subject kitchen baru |
| Bedroom | `edh058` shot-04: bed→wide dengan dolly-out | Reveal jendela dan bed pada kamar baru |
| Bathroom | [`edh060`](../references/edh060/analysis.yaml) shot-03: pan dari vanity ke tub | Closing vanity→bathtub dengan fixture sewarna rumah |
| Cahaya/edit | `edh058`: daylight + lampu hangat; hard cuts | Cahaya/window views konsisten, clean cuts pada batas shot |

**[ATURAN PRODUKSI]** Timeline simulasi, dengan **dua generasi masing-masing 10 detik**:

| Waktu final | Waktu **lokal** dalam klip | Scene | Instruksi sinematik |
| --- | --- | --- | --- |
| **00:00–00:06** | A `0–6s` | **Exterior hook**, luar rumah ≥6 dtk | Wide→medium, dolly+tracking, rumah terbaca sejak awal |
| 00:06–00:10 | A `6–10s` | Living | Pan dan reveal objek ruang; hard cut di `6s` klip A |
| 00:10–00:14 | B `0–4s` | Kitchen | Tracking menuju focal subject; Clip B dimulai shot baru |
| 00:14–00:17 | B `4–7s` | Bedroom | Dolly-out/detail→wide; hard cut di `4s` lokal |
| 00:17–00:20 | B `7–10s` | Bathroom | Pan vanity→tub; hard cut di `7s` lokal, ending stabil |

**Bukan jaminan hasil generator:** timestamp dan hard cut adalah instruksi; video harus ditinjau. Jika model mengabaikan 6 detik eksterior atau menyatukan ruangan menjadi morphing, generasi tidak langsung dianggap lulus.

## 5. Ketentuan implementasi yang harus dibawa ke P2

| Komponen | Aturan yang disepakati |
| --- | --- |
| Output | Video rumah orisinal target **20 detik**, rasio **9:16** |
| Produksi | **Dua klip Omni Flash @10 detik**, A dan B |
| Hook | Shot exterior pertama **≥6 detik layar nyata**, bukan durasi gabungan exterior→living |
| Storyboard default | Clip A **Exterior 0–6 + Living 6–10**; Clip B **Kitchen 0–4 + Bedroom 4–7 + Bathroom 7–10** |
| Jumlah shot | Default **5**; variasi boleh jika cocok DNA, tetap dua klip dan exterior ≥6 |
| Desain | **Satu Design Lock**: bentuk, atap, lantai, bukaan, material, furnitur, lanskap, lighting dan hubungan ruang |
| Pembuatan gambar A | **Default:** AI langsung membuat **5 master image**, user melakukan review |
| Pembuatan gambar B | **Atas permintaan user:** AI membuat **5 prompt gambar berbahasa Inggris**; user menghasilkan/mengunggah, AI mereview |
| Gerbang sebelum video | **5 gambar telah disetujui**; kedua opsi harus bertemu pada titik ini |
| Prompt Flow | **Satu prompt lengkap per klip 10 detik**; mapping gambar→shot, Design Lock, local timestamps, framing, focal, kamera, lighting, hard cuts dan larangan morphing |
| QA | Cek hasil video asli: durasi, exterior, frame/ruang, konsistensi, hard cuts, artefak, total 20 detik |
| Simpan GitHub | Hanya setelah persetujuan produksi khusus; `save now` **hanya** untuk analisis referensi lama |

**Field wajib per shot untuk template P2:** `clip_id`; `local_start_s`; `local_end_s`; `global_start_s`; `global_end_s`; `scene`; `source_reference_ids` dan `source_shot_ids`; `master_image`; `framing_start`; `framing_end`; `view_angle`; `focal_subject`; `camera.movements`; `camera.speed`; `reveal_path`; `architecture_anchors`; `furniture_and_props_anchors`; `environment_anchors`; `lighting`; `transition_out`; `continuity_constraints`; `uncertainty_notes`.

**Gerbang validasi sebelum prompt:** total lokal Clip A tepat 10 detik, Clip B tepat 10 detik; tidak ada celah/overlap; exterior ≥6; setiap shot memiliki referensi DNA, gambar dan framing awal/akhir; penempatan cut jelas. Jika tidak lulus, perbaiki storyboard **sebelum** menggunakan kredit Flow.

**Batas model:** jumlah gambar yang dapat dimasukkan bergantung mode/model Google Flow, perlu dicek saat pilot. Tidak boleh berjanji semua mode mendukung 3 input image, hard cut tepat per-frame, atau dua generasi percobaan pasti cukup. Revisi klip yang gagal terlebih dahulu.

## 6. Batas yang tidak boleh ditutup dengan tebakan AI

1. **Viralitas/retensi:** video disebut telah mencapai jutaan views oleh pemilik, tetapi statistik per-platform, watch time, completion dan uji sebab-akibat **tidak** tersedia dalam analisis.
2. **Audio, musik, SFX, dialog, teks:** proses referensi hanya visual. Tidak ada DNA audio yang sah untuk disimpulkan dari YAML. Jika diperlukan, buat sebagai pilihan produksi baru dan tandai bukan dari sumber.
3. **Identitas fisik rumah:** `common_regions` adalah *wilayah asosiasi gaya*, bukan lokasi rumah; material hanya dari tampilan, luas estimasi, musim tidak pasti.
4. **Waktu exterior:** first-shot mixed exterior→living tidak mengukur outdoor-only; QA generasi harus melihat berapa detik rumah di luar benar-benar muncul.
5. **Gambar kunci:** satu `shot-NN.jpg` tidak mewakili gerakan seluruh adegan; wajib baca `framing.start/end`, `camera`, `focal_subject`, `observation_note`.
6. **Konsistensi antarshot:** gambar terpisah bisa menggambarkan rumah berbeda; Design Lock dan pemeriksaan manual harus mencegahnya.
7. **Perpindahan generatif:** hard cut di prompt belum pasti terjadi; jika morphing/ruang tidak muncul/exterior terlalu singkat, status QA gagal dan perbaiki.
8. **Freshness:** setiap penambahan referensi baru memerlukan re-audit snapshot; jangan mengubah data asli atau menyatakan tabel ini otomatis mencakup isi baru.
9. **Batas fase:** P1 hanya membangun pengetahuan. **P2 workflow/template, P3 pilot, dan P4 kesiapan produksi belum dijalankan pada PR ini**.

**P2 dinilai memiliki gap** bila mengabaikan salah satu unsur: bukti ID+shot, exterior dan environment, framing awal **dan** akhir, gerak dan kecepatan kamera, reveal, posisi furnitur dan hubungan ruang, konsistensi lighting, alur/cut/timing, Design Lock, dua opsi master image, dua prompt 10s, QA, orisinalitas dan ketidakpastian.

## 7. Katalog seluruh 58 referensi

**Kegunaan:** cari berdasarkan gaya **dan** pola edit/kamera awal. Setelah memilih maksimal tiga, buka dokumen YAML serta storyboard masing-masing untuk detail seluruh shot.

**Legenda:** `E` exterior; `L` living; `K` kitchen; `B` bedroom; `Ba` bathroom; `U` laundry; `C` closet; `X` kembali ke exterior; `LK` living+kitchen gabungan; `EL` exterior→living dalam satu shot; `Ba/U` bath+laundry; `(loft)` area loft. Tanda `*` berarti durasi shot pembuka mencakup exterior **dan** interior. Kolom *kamera pembuka* menyimpan label sumber `shots[0].camera.movements` (bukan prompt lengkap).

| File referensi | Label gaya asli | Durasi (dtk) | Shot | Shot 1 (dtk) | Urutan scene | Kamera pembuka |
| --- | --- | ---: | ---: | ---: | --- | --- |
| [VID-001](../references/VID-001/analysis.yaml) | american_storybook_cottage | 20.030 | 5 | 6.200 | E-L-K-B-Ba | `dolly_in + tracking_right` |
| [VID-002](../references/VID-002/analysis.yaml) | modern_rustic_cottage | 20.900 | 4 | 6.310 | E-L-B-Ba | `subtle_dolly_in` |
| [VID-003](../references/VID-003/analysis.yaml) | american_cottage | 26.500 | 7 | 6.700 | E-L-K-U-B-Ba-C | `dolly_in` |
| [VID-004](../references/VID-004/analysis.yaml) | organic_modern_cottage | 18.400 | 5 | 4.730 | E-L-K-B-Ba/U | `dolly_in + slight_tracking_right` |
| [VID-005](../references/VID-005/analysis.yaml) | modern_tropical_villa | 18.850 | 6 | 4.630 | E-L-K-B-Ba-X | `dolly_in + subtle_tracking_right` |
| [VID-006](../references/VID-006/analysis.yaml) | modern_cottage | 21.780 | 5 | 4.550 | E-L-K-B-Ba | `dolly_in` |
| [VID-007](../references/VID-007/analysis.yaml) | modern_traditional_cottage | 21.500 | 7 | 5.070 | E-L-K-B-C-Ba-X | `tracking_right + dolly_in` |
| [VID-008](../references/VID-008/analysis.yaml) | modern_cottage | 21.767 | 5 | 4.900 | E-L-K-B-Ba | `dolly_in + subtle_tracking_right` |
| [VID-009](../references/VID-009/analysis.yaml) | modern_tropical_villa | 17.670 | 5 | 5.100 | E-L-K-B-Ba | `dolly_in + tracking_right` |
| [VID-010](../references/VID-010/analysis.yaml) | modern_storybook_cottage | 20.530 | 6 | 5.100 | E-L-K-B-U-Ba | `dolly_in + slight_pan_right` |
| [edh011](../references/edh011/analysis.yaml) | modern_rustic_cottage | 17.530 | 5 | 5.000 | E-L-K-B-Ba | `dolly_in + slight_tracking_right` |
| [edh012](../references/edh012/analysis.yaml) | modern_contemporary_cottage | 24.400 | 5 | 4.970 | E-L-K-B-Ba | `dolly_in + subtle_tracking_right` |
| [edh013](../references/edh013/analysis.yaml) | whimsical_organic_mediterranean_tower_house | 21.477 | 5 | 4.600 | E-L-K-B-Ba | `tracking_right + subtle_dolly_in` |
| [edh015](../references/edh015/analysis.yaml) | european_rustic_stone_cottage | 20.014 | 5 | 4.133 | E-L-K-B-Ba | `slow_dolly_in` |
| [edh016](../references/edh016/analysis.yaml) | storybook_cottage | 19.830 | 5 | 9.600* | EL-K-B-Ba/U-X | `dolly_in + tracking_right` |
| [edh017](../references/edh017/analysis.yaml) | victorian_influenced_american_farmhouse | 19.770 | 6 | 4.830 | E-L-K-U-B-Ba | `dolly_in` |
| [edh018](../references/edh018/analysis.yaml) | modern_farmhouse_cottage | 17.670 | 5 | 5.070 | E-L-K-B-Ba/U | `tracking_right + subtle_dolly_in` |
| [edh019](../references/edh019/analysis.yaml) | modern_barrel_vault_cottage | 21.480 | 5 | 3.970 | E-L-K-B-Ba | `tracking_right + dolly_in` |
| [edh020](../references/edh020/analysis.yaml) | storybook_stone_cottage | 18.620 | 5 | 5.070 | E-L-K-B-Ba | `dolly_in + tracking_right` |
| [edh021](../references/edh021/analysis.yaml) | contemporary_castle_inspired_stone_cottage | 22.800 | 5 | 4.570 | E-L-K-B-Ba | `tracking_right + slow_dolly_in` |
| [edh022](../references/edh022/analysis.yaml) | contemporary_compact_minimalist_house | 21.830 | 5 | 6.570 | E-LK-B-Ba-X | `dolly_in + tracking_right` |
| [edh023](../references/edh023/analysis.yaml) | modern_tropical_contemporary | 22.400 | 5 | 4.670 | E-L-K-B-Ba | `dolly_in + subtle_tracking_right` |
| [edh024](../references/edh024/analysis.yaml) | contemporary_modern_farmhouse | 18.250 | 5 | 5.867 | E-L-K-B-Ba | `dolly_in + tracking_right + slight_tilt_up` |
| [edh025](../references/edh025/analysis.yaml) | rustic_storybook_stone_cottage | 21.082 | 6 | 5.167 | E-L-K-U-B-Ba | `slow_dolly_in + subtle_tracking_right` |
| [edh026](../references/edh026/analysis.yaml) | modern_contemporary | 21.000 | 5 | 9.667* | EL-K-B-C-Ba | `dolly_in + tracking_right + pan_right` |
| [edh027](../references/edh027/analysis.yaml) | modern_contemporary | 21.150 | 6 | 5.470 | E-L-K-B-C-Ba | `dolly_in + slight_tracking_right` |
| [edh029](../references/edh029/analysis.yaml) | contemporary_bungalow_with_modern_farmhouse_influence | 20.107 | 5 | 5.367 | E-L-K-B-Ba | `dolly_in + slight_tracking_right` |
| [edh030](../references/edh030/analysis.yaml) | mediterranean_inspired_cottage | 20.460 | 5 | 5.000 | E-LK-U-B-Ba | `slow_dolly_in + tracking_right` |
| [edh031](../references/edh031/analysis.yaml) | modern_contemporary | 27.233 | 5 | 11.333* | EL-K-B-C-Ba | `tracking_right + dolly_in + pan_right` |
| [edh032](../references/edh032/analysis.yaml) | contemporary_compact_cottage | 15.300 | 4 | 7.030 | E-L-B-X | `dolly_in + tracking_right + slight_descending` |
| [edh033](../references/edh033/analysis.yaml) | contemporary_rustic_compact_house | 18.667 | 4 | 5.033 | E-LK(loft)-Ba/U-X | `slow_tracking_right + subtle_dolly_in` |
| [edh034](../references/edh034/analysis.yaml) | modern_cottage | 20.200 | 5 | 5.033 | E-LK-B-Ba-X | `tracking_right + subtle_dolly_in` |
| [edh035](../references/edh035/analysis.yaml) | modern_cottage | 24.770 | 4 | 13.130* | EL-K-B-Ba | `dolly_in + pan_left` |
| [edh036](../references/edh036/analysis.yaml) | modern_european_cottage | 27.170 | 5 | 12.500* | EL-K-B-Ba/U-X | `dolly_in + forward_tracking_through_door + gentle_pan_right` |
| [edh037](../references/edh037/analysis.yaml) | modern_transitional_with_classical_european_accents | 19.570 | 6 | 5.100 | E-L-K-B-Ba-X | `tracking_right + dolly_in` |
| [edh038](../references/edh038/analysis.yaml) | rustic_mediterranean_cottage | 23.520 | 5 | 6.000 | E-L-K-B-Ba | `dolly_in + tracking_right` |
| [edh039](../references/edh039/analysis.yaml) | contemporary_organic_mountain_modern | 20.933 | 6 | 5.300 | E-L-K-U-B-Ba | `slow_dolly_in + subtle_tracking_right` |
| [edh040](../references/edh040/analysis.yaml) | modern_farmhouse | 20.898 | 5 | 4.597 | E-L-K-B-X | `slow_dolly_in + subtle_tracking_right` |
| [edh041](../references/edh041/analysis.yaml) | modern_farmhouse | 22.567 | 5 | 5.367 | E-L-K-B-Ba/U | `dolly_in + slight_pan_right` |
| [edh042](../references/edh042/analysis.yaml) | modern_tropical_minimalist | 22.700 | 5 | 5.433 | E-L-K-B-Ba | `slow_dolly_in + subtle_tracking_right` |
| [edh043](../references/edh043/analysis.yaml) | contemporary_european_cottage | 21.830 | 5 | 5.900 | E-L-K-B-Ba | `dolly_in + tracking_right` |
| [edh044](../references/edh044/analysis.yaml) | english_storybook_cottage | 21.360 | 6 | 5.130 | E-L-K-U-B-Ba | `dolly_in` |
| [edh045](../references/edh045/analysis.yaml) | contemporary_rustic_cottage | 23.293 | 5 | 5.900 | E-L-K-B-C | `dolly_in + subtle_tracking_right` |
| [edh046](../references/edh046/analysis.yaml) | modern_cottage_with_contemporary_farmhouse_influences | 16.881 | 5 | 5.065 | E-L-K-B-Ba | `slow_dolly_in + slight_tracking_right` |
| [edh047](../references/edh047/analysis.yaml) | modern_organic_contemporary | 18.900 | 6 | 5.067 | E-L-K-B-Ba/U-X | `slow_dolly_in + tracking_right` |
| [edh048](../references/edh048/analysis.yaml) | modern_european_cottage | 20.180 | 6 | 5.100 | E-L-K-C-B-Ba/U | `dolly_in` |
| [edh049](../references/edh049/analysis.yaml) | contemporary_organic_stone_architecture | 19.090 | 4 | 5.530 | E-K-B-Ba | `slow_lateral_tracking + subtle_orbit` |
| [edh050](../references/edh050/analysis.yaml) | spanish_revival_cottage | 18.230 | 5 | 5.470 | E-L-K-B-Ba/U | `tracking_right + subtle_dolly_in` |
| [edh051](../references/edh051/analysis.yaml) | contemporary_mediterranean | 18.370 | 6 | 5.133 | E-L-K-B-Ba-X | `dolly_in + tracking_right` |
| [edh052](../references/edh052/analysis.yaml) | contemporary_tropical_bungalow | 18.633 | 5 | 5.133 | E-L-K-B-Ba | `slow_dolly_in + subtle_tracking_right` |
| [edh053](../references/edh053/analysis.yaml) | contemporary_mediterranean_villa | 18.633 | 5 | 5.633 | E-L-K-B-Ba | `dolly_in + tracking_right` |
| [edh054](../references/edh054/analysis.yaml) | contemporary_neoclassical_townhouse | 18.300 | 5 | 5.800 | E-L-K-B-Ba | `dolly_in + slight_pan_right` |
| [edh055](../references/edh055/analysis.yaml) | tropical_contemporary_villa | 19.800 | 6 | 5.900 | E-L-K-B-C-Ba | `dolly_in + tracking_right` |
| [edh056](../references/edh056/analysis.yaml) | modern_rustic_contemporary | 23.700 | 6 | 6.600 | E-L-K-B-Ba-X | `slow_dolly_in + gradual_tracking_right` |
| [edh057](../references/edh057/analysis.yaml) | rustic_alpine_stone_cottage | 18.640 | 4 | 5.100 | E-LK-B-Ba | `dolly_in + slight_tracking_right` |
| [edh058](../references/edh058/analysis.yaml) | mediterranean_cottage | 19.900 | 6 | 5.300 | E-L-K-B-C-Ba | `dolly_in + slight_tracking_right` |
| [edh059](../references/edh059/analysis.yaml) | storybook_rustic_stone_cottage | 17.800 | 5 | 5.300 | E-L-K-B-Ba | `slow_dolly_in + tracking_right` |
| [edh060](../references/edh060/analysis.yaml) | modern_farmhouse_tiny_house | 18.470 | 3 | 8.030 | E-LK(loft)-Ba | `tracking_right + subtle_dolly_in` |

Setiap tautan mengarah ke `analysis.yaml` yang ada pada snapshot; file `analysis.md`, `storyboard.jpg` dan foto per shot berada dalam direktori referensi yang sama. Jangan melakukan migrasi ID arsip lama.

## 8. Checklist review P1

- [x] 58 direktori dengan tiga berkas wajib tersedia, total 300 keyframe.
- [x] 58 baris katalog, tidak ada ID yang hilang atau berulang, seluruh tautan YAML dicek.
- [x] Metadata durasi, urutan shot, ritme, pola kamera dan ketidakpastian diuraikan.
- [x] Tujuh DNA video menyeluruh dan jejak pengambilan sumber ditetapkan.
- [x] Gerak kamera pembuka dari tiap referensi ditambahkan ke indeks.
- [x] Aturan produksi 6 detik exterior dan Omni 2×10 dtk dipisahkan dari fakta sumber.
- [x] Opsi A (gambar langsung, default), opsi B (prompt gambar atas permintaan), dan gerbang lima gambar disetujui tercantum.
- [ ] **Belum dilakukan:** inspeksi isi semua 300 JPEG secara manual, pembuatan prompt produksi final, pengujian model/retensi, dan pilot video.

**Ringkasnya:** P1 menyediakan fondasi DNA **desain, lingkungan, interior, sinematografi, lighting, dan editing** agar AI dapat membangun konten rumah yang terasa satu keluarga dengan referensi tanpa menjiplak video. P2 harus mewajibkan penerjemahan tujuh unsur tersebut ke storyboard dan prompt, sedangkan P3 membuktikan kualitasnya pada hasil Omni Flash.
