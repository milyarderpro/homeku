# HOMEKU — Workflow Produksi Video v1.1 (Production Lite)

> **Status:** aturan operasional P2; sumber DNA dari [`knowledge/dna-summary.md`](../knowledge/dna-summary.md); rencana induk [`docs/production-lite-v1.1-implementation-plan.md`](../docs/production-lite-v1.1-implementation-plan.md); [Issue #7](https://github.com/milyarderpro/homeku/issues/7).  
> **Output target:** video rumah orisinal, vertikal **9:16**, **20 detik** dari **dua klip Google Flow Omni Flash masing-masing 10 detik**.  
> **Batas tegas:** ini workflow **kreasi**, BUKAN [`rules/workflow-analysis.md`](workflow-analysis.md); **`save now` tetap eksklusif untuk menyimpan analisis video referensi.**

## 0. Cara memulai, sumber kebenaran, dan cakupan

**Pemicu produksi:** instruksi eksplisit seperti “Buat 3 ide video rumah HOMEKU”, “Mulai produksi IDEA-…”, atau “Lanjutkan storyboard produksi”. Jangan menganggap pengguna yang mengunggah MP4 untuk dianalisis ingin membuat video baru. Ketika permintaan adalah analisis video referensi, **ikuti workflow analisis v1.4** dan jangan jalankan aturan produksi ini.

Sebelum membuat ide:
1. Baca **versi terbaru `main`** dari dokumen ini, [`knowledge/dna-summary.md`](../knowledge/dna-summary.md), dan [`templates/production.md`](../templates/production.md). P1 adalah indeks, **bukan** pengganti data sumber.
2. Tinjau 58 katalog referensi sebagai basis pola. Untuk ide yang dikembangkan, pilih **satu referensi utama + satu/dua pendukung**, lalu **buka sumber lengkap** `references/<ID>/analysis.yaml`, `analysis.md` dan `storyboard.jpg` serta keyframe yang relevan. Bila ada ketidaksesuaian, **YAML/visual sumber** dan ketidakpastiannya didahulukan daripada ringkasan.
3. Gunakan **seluruh 7 DNA**: hook eksterior; arsitektur; lingkungan; interior/relasi objek; sinematografi; pencahayaan/mood; editing/urutan narasi. Hanya menyebut nama gaya, warna, atau “cinematic” **tidak memadai**.
4. **Status bukti:** pisahkan `FAKTA REFERENSI` (ID+shot/field), `INTERPRETASI` (dugaan estetis), `KREASI BARU` (rumah orisinal), dan `ATURAN PRODUKSI` (keputusan HOMEKU). Jangan menyebut durasi 6s sebagai fakta semua video referensi, dan jangan mengklaim sebab-akibat viralitas, retention atau statistik yang tidak ada.
5. Bahasa interaksi, laporan, storyboard dan penjelasan: **Bahasa Indonesia**. Prompt gambar dan prompt Omni Flash yang akan ditempel ke generator: **Bahasa Inggris**, dengan nama aset/input yang jelas.

**Bukan bagian P2:** membuat mesin RAG/vector DB, AI di GitHub Actions, otomasi akses ke Google Flow, membuat video pilot, membuat file produksi final tanpa izin, atau mengubah referensi yang sudah tersimpan.

## 1. Kontrak visual dan waktu yang tidak boleh dilanggar

| Item | Ketentuan |
| --- | --- |
| Format | Portrait 9:16; target final 20,00 detik |
| Jumlah klip | **A = 10 detik**, **B = 10 detik**; dua **prompt video utama** (satu per klip) |
| Awal video | **Exterior sebagai shot pertama**, rumah dapat dikenali sejak frame pertama |
| Durasi hook | **Exterior murni ≥6,00 detik** pada hasil final, bukan keseluruhan shot yang sudah masuk living |
| Default shot/timing global | Exterior `0–6s`; Living `6–10s`; Kitchen `10–14s`; Bedroom `14–17s`; Bathroom `17–20s` |
| Default Clip A (waktu lokal) | **0–6s Exterior** → **6–10s Living**; hard cut pada detik 6 |
| Default Clip B (waktu lokal) | **0–4s Kitchen** → **4–7s Bedroom** → **7–10s Bathroom**; hard cut detik 4 dan 7 |
| Jumlah shot/gambar | Default **5 shot + 5 master image**; jika jumlah shot berubah, **jumlah dan mapping gambar mengikuti storyboard** |
| Gerak kamera | Diturunkan dari DNA shot sumber: `framing.start/end`, `focal_subject`, `camera.movements/speed`, `observation_note`; halus dan berarah |
| Kontinuitas | Satu Design Lock untuk rumah, taman, jendela, interior, objek, lingkungan, pencahayaan dan dua klip |
| Transisi | Clean hard cut antaradegan sebagai default; **bukan morphing** atau teleportasi ruangan |
| Audio/teks | Tidak ada DNA audio/teks dalam analisis sumber; jika dibutuhkan, keputusan baru terpisah, **bukan klaim ekstraksi referensi** |

**Perubahan storyboard boleh** mengikuti pola relevan dari referensi, misalnya rumah loft, gabungan living/kitchen, laundry/closet, atau eksterior penutup, **dengan syarat**: (a) total tepat 10s+10s, (b) eksterior awal **≥6s**, (c) tidak ada celah/overlap waktu di dalam tiap klip, (d) seluruh shot memiliki tujuan visual berbeda, (e) jumlah aset dan prompt mengikuti urutan baru, (f) alasan perubahan dicatat. Jangan menyalin 5 shot dari sumber secara otomatis.

**Definisi eksterior murni:** frame masih memperlihatkan bangunan dari luar; saat kamera sudah menampilkan interior sebagai adegan utama, penghitungan exterior berakhir. **Jangan menghitung gerakan exterior→living gabungan sebagai 6s exterior** tanpa bukti frame. Pada hasil video, periksa batas transisi nyata. Karena model tidak menjamin pemotongan tepat-per-frame, bila gagal **revisi klip**, jangan menandai lulus hanya karena prompt mencantumkan “6s”.

## 2. Tahapan percakapan, keputusan dan status

**Satu sesi percakapan = satu paket ide terpilih.** Jangan buat banyak berkas dari tiga ide awal. Simpan progres dalam struktur [`templates/production.md`](../templates/production.md) di chat sampai pengguna secara eksplisit mengizinkan penyimpanan. Jika user meminta melanjutkan dari suatu status, **lanjutkan dari hasil yang sudah ada**, bukan otomatis ulang dari nol.

| Langkah | Tugas AI dan output | Keputusan/gate |
| --- | --- | --- |
| **1 — DNA Selection** | Baca P1; tentukan 2–3 referensi yang cocok, peran tiap referensi, bukti dari YAML/shot, 7 dimensi DNA | **READ-ONLY** sumber; jika evidence tidak ada, tulis `belum diketahui` |
| **2 — Idea Generation** | Tampilkan **3 Idea Cards** berbeda: nama, karakter, hook, sumber/peran, kombinasi DNA, pembeda orisinal, usulan shot 20s, potensi risiko | **Gate 1:** user memilih satu ide (contoh “Pilih IDEA-002”) |
| **3 — Design Lock & Storyboard** | Kunci rumah; tampilkan storyboard global dan per-klip; tulis framing awal/akhir, fokus, gerak+kecepatan, reveal, lighting, sumber DNA untuk **setiap shot** | **Gate 2:** user menyetujui atau merevisi konsep/desain/storyboard |
| **4 — Master Image Production** | **Opsi A DEFAULT:** AI membuat master image asli; **Opsi B atas permintaan:** AI membuat prompt gambar agar user menghasilkan sendiri. Semua gambar direview | **Gate 3:** seluruh master image sesuai Design Lock dan disetujui |
| **5 — Omni Flash Prompt Packaging** | AI menyusun **Prompt A** & **Prompt B** dalam bahasa Inggris lengkap, masing-masing satu video 10s multi-shot, mengikuti urutan dan image mapping | Tidak boleh mengaku prompt final sebelum Gate 3. Lulus validasi waktu dan DNA dulu |
| **6 — Generate, QA & Revision** | User menjalankan Flow, unggah klip; AI menilai video nyata, menyampaikan kegagalan/penyebab/prompt koreksi per klip; user menyetujui hasil | Video final hanya dinyatakan lolos jika hasil benar-benar diperiksa; save produksi terpisah |

**Contoh dialog tanpa asumsi persetujuan diam-diam:** “Buat 3 ide video baru” → AI tampilkan ide → “Pilih IDEA-002” → AI tampilkan Design Lock/storyboard → “Setuju desain, buat gambar” (Opsi A) **atau** “Buat 5 prompt gambar” (Opsi B) → user meninjau gambar → “Gambar sudah sesuai, buat prompt Flow” → user generate/unggah video → AI QA/revisi.

### 2.1 Langkah 1 — Pemilihan DNA: wajib berbasis bukti

- **Utama (1 ID):** sumber dominan arsitektur, skala, geometri, bahasa bukaan serta material.
- **Pendukung A (1 ID):** kontribusi terbatas seperti lanskap/warna interior yang kompatibel.
- **Pendukung B (opsional, 1 ID):** teknik kamera, ritme, framing atau reveal. Bisa saja pendukung A juga menyumbang kamera; tetap tulis perannya.
- Untuk tiap DNA terpakai, tulis **`referensi/shot/field → observasi → adaptasi baru → elemen yang sengaja berbeda → ketidakpastian`**.
- Konflik: **Design Lock yang disetujui > identitas arsitektur sumber utama > inspirasi pendukung**. Jangan mencampur iklim/pemandangan jendela, roofline, level, material dan spasial secara bertentangan. Jangan menganggap `common_regions` lokasi rumah sebenarnya.
- Pastikan ide **orisinal**, bukan salinan utuh rumah/shot/frame atau reproduksi adegan berurutan yang identik.

### 2.2 Langkah 2 — Tiga ide yang benar-benar berbeda

Setiap Idea Card minimal memuat: `ID sementara`; judul; deskripsi visual (fasad/lingkungan/interior); **hook exterior 6s**; ID dan peran 2–3 sumber; DNA sinematik dan edit; pembeda/novelty; susunan shot rencana; risiko kontinuitas/generasi. Ide berbeda pada setidaknya **dua aspek substantif** (arsitektur, lingkungan, cinematic reveal, organisasi ruang), bukan hanya warna atau nama.

Jangan langsung membuat gambar atau prompt video sebelum user memilih **satu** ide.

### 2.3 Langkah 3 — Design Lock sebelum gambar

Tulis identitas rumah untuk mencegah **style drift** dan **geometry drift**:
- **Bangunan:** skala tampak, jumlah lantai, arah massa dan atap, bentuk fasad, pintu/handle, posisi-bentuk-kusen jendela, porch/stairs/chimney/railing.
- **Material/warnanya:** palet utama/aksen, penampilan stucco/kayu/batu, lantai, trim, hardware.
- **Dunia luar:** jalan/path, ukuran/posisi pohon foreground, taman/bunga, pagar/lawn, cuaca/langit/season appearance, view lewat jendela.
- **Interior dan denah masuk akal:** hubungan living-kitchen-bedroom-bath, skala plafon, material/furnitur sama, penempatan focal subject; jangan mengarang denah sumber sebagai fakta.
- **Look & feel:** pencahayaan arah, temperatur dan kekuatan relatif, mood, fotorealisme, depth/perspective, portrait 9:16.
- **Sinematik+editing:** pilihan framing awal/akhir tiap shot, jalur reveal, kecepatan gerak, urutan, hard cuts, titik join antara Clip A dan B.

**Wajib tampilkan dua storyboard:** satu tabel shot global (0–20s) dan dua blok per generasi dengan **waktu lokal masing-masing 0–10s**. Konsistensi kamera **bukan** berarti semua shot memiliki satu gerakan yang sama; gerak harus mempunyai tujuan yang dapat dilihat.

### 2.4 Langkah 4 — Dua jalur gambar (pilihan pengguna)

**Opsi A — AI membuat gambar (DEFAULT):** tanpa user harus memilih mode, AI membuat **5 master image** sesuai storyboard lima shot setelah Gate 2. Tampilkan gambar satu per satu dengan identitas `image_id` dan `shot_id`; periksa kesesuaian sebelum user menerima. Bila kemampuan membuat gambar tidak tersedia saat itu, jelaskan dengan jujur dan berikan alternatif prompt; jangan berpura-pura gambar sudah dibuat.

**Opsi B — AI membuat prompt gambar (hanya bila diminta):** AI membuat **5 prompt gambar berbahasa Inggris**, setiap prompt menjelaskan rumah yang sama, komposisi frame awal, objek detail, lanskap/view, material, pencahayaan, rasio 9:16, serta elemen konsistensi/larangan distorsi. User memakai generator pilihannya lalu mengunggah hasil. **Prompt ≠ master image**; status tetap `menunggu gambar` sampai gambar benar-benar ada dan direview.

**Jika jumlah shot berubah:** hasilkan aset seperlunya untuk komposisi shot yang berbeda (jangan selalu memaksakan lima). Catat `image_id → shot_id → clip_id`. User dapat pindah Opsi A↔B **tanpa mengulang ide/Design Lock**. Revisi satu gambar jika hanya satu yang bermasalah; jika Design Lock fundamental berubah, periksa ulang semua gambar terdampak.

**Gate 3 wajib:** gambar tersedia, terbaca, sesuai rasio/komposisi yang bisa dianimasikan, memiliki identitas rumah/ruang/material/jendela/lighting yang koheren, tidak ada distorsi besar, dan **user menyetujui**. Jika belum lulus, tidak boleh mengklaim Prompt A/B final siap pakai (boleh menyusun rancangan internal yang jelas berstatus draft).

### 2.5 Langkah 5 — Dua prompt Omni Flash, bukan prompt per shot

**Output final:** tepat **dua prompt video utama berbahasa Inggris**: `PROMPT A — Clip A 10s` dan `PROMPT B — Clip B 10s`. Di setiap prompt, urutan shot multi-adegan ditulis **di dalam satu prompt**, dengan:
1. **Video identity:** rumah orisinal yang sama + format 9:16 fotorealistis, 10s.
2. **Approved image mapping:** deskripsi atau nama asset gambar spesifik yang dipakai untuk setiap shot; jangan menganggap Flow menerima semuanya sekaligus pada setiap mode.
3. **Global Design Lock:** geometri, material, bukaan, lighting, landscape dan interior continuity; Clip B adalah rumah yang **sama** dengan Clip A.
4. **Local timeline:** urutan dan batas detik lokal, durasi masing-masing; juga catat batas global di paket produksi.
5. **Per-shot cinematic direction:** `start framing → focal subject → motion/speed → reveal path → end framing`, posisi objek, pencahayaan.
6. **Transition:** `clean hard cut` di batas yang disepakati; tidak boleh morphing, teleportation, material swaps, extra rooms.
7. **Negative/quality constraints:** no unwanted people, logo, watermark, text, geometric distortion, camera shakes/whip pan, object pop-in, changing furniture/window count.
8. **Output:** exact target length 10s, portrait 9:16.

**Praflight prompt:** format seluruh slot wajib, mapping gambar valid, waktu lokal A dan B masing-masing 10s, exterior ≥6s, tidak ada slot kosong, tidak ada janji kemampuan image-input model yang belum terverifikasi. Jika mode Omni tertentu memiliki keterbatasan input gambar/scene, sampaikan keterbatasan dan sesuaikan paket sumber secara jujur; **jangan menyebut storyboard collage pasti dapat dipakai sebagai semua image input**. Prioritaskan scene clarity dan konsistensi, dengan risiko multi-cut eksplisit.

### 2.6 Langkah 6 — QA berdasarkan klip, bukan berdasarkan kata-kata prompt

- User menjalankan Google Flow. AI **tidak** menyatakan sudah mengeksekusi Flow hanya karena dua prompt dibuat.
- Setelah user mengunggah video, catat `clip_id`, durasi nyata, aspek rasio, timestamp perubahan exterior→living, cut kitchen→bedroom→bathroom, keberadaan adegan, kesesuaian dengan gambar, kelancaran gerak, distorsi, lighting dan material yang berubah.
- **LULUS:** exterior terlihat nyata ≥6s sejak frame 0; urutan dan ruang sesuai storyboard; hard cuts yang nyata; satu identitas rumah, landscape dan furnishing konsisten; klip yang digabung target 20s vertikal 9:16.
- **GAGAL:** exterior <6s, salah/ruang hilang, pergantian ruang morphing, kamera mengubah geometri/furnitur, klip tidak 10s/rasio salah, atau visual tidak selaras. Laporkan **klip, rentang waktu, bukti visual dan usulan revisi**.
- Buat prompt revisi **hanya klip terdampak** dahulu; bandingkan kembali terhadap Gate 3/Design Lock. **Dua generasi hanyalah baseline**, bukan janji percobaan pertama langsung berhasil.
- Jika kedua klip lolos, jelaskan perlunya penggabungan/trim jika durasi video final berbeda; tidak mengklaim sudah menyunting file kecuali benar-benar dilakukan.

## 3. Kontrol izin, penyimpanan dan pemisahan workflow

- **Saat ideasi/design/gambar/prompt/review:** GitHub **read-only** untuk `references/` dan aturan; berkas proyek disusun dahulu dalam chat. Jangan membuat `productions/IDEA-xxx/production.md` hanya karena user memilih ide atau mengetik `save now`.
- **`save now`** dalam [`workflow-analysis.md`](workflow-analysis.md) tetap memiliki makna khusus: satu request analisis ke `requests/pending/`. **Jangan menggunakannya untuk produksi**; jangan menulis `requests/`, `video/`, `references/`, atau workflow Actions dalam alur produksi.
- Penyimpanan produksi menggunakan **perintah eksplisit yang menyebut objek**, mis. “Simpan produksi IDEA-001 ke GitHub”; sebelum write periksa target, konflik/duplikasi, status persetujuan dan perubahan. Pada konflik, **jangan overwrite diam-diam**; minta instruksi tujuan revisi. Commit file produksi **hanya setelah** persetujuan; verifikasi ulang remote sebelum mengaku tersimpan.
- ID `IDEA-001` di template adalah **contoh**; jangan mengalokasikan nomor baru tanpa mengecek `productions/` yang sudah ada. Simpan file Markdown ringkas; jangan menjadikan repository tempat otomatis mengunggah MP4/JPEG besar.
- Jangan mengubah `rules/workflow-analysis.md`, YAML Schema 2.1, `references/`, skrip penyimpanan analisis, maupun GitHub Actions.

## 4. Pemeriksaan pra-produksi: harus lolos sebelum P3

**Gerbang DNA:**
- [ ] Ada 1 referensi utama + 1–2 pendukung dengan ID/shot asli, kelebihan dan batas masing-masing.
- [ ] **Ketujuh DNA** punya observasi, penerapan baru dan pengaruh pada hasil video, bukan hanya bentuk rumah.
- [ ] Konsep asli tidak menyalin rumah/frame/video tertentu satu banding satu.

**Gerbang desain & storyboard:**
- [ ] Design Lock memuat rumah, environment, interior, material, windows/view dan lighting.
- [ ] Shot **pertama exterior**; sejak frame pertama rumah terbaca; **durasi luar target ≥6s**.
- [ ] Dua klip video dengan durasi lokal masing-masing tepat **10 detik**, tanpa jeda/overlap.
- [ ] Semua shot memiliki kamera, framing awal–akhir, focal subject, reveal, detail, transisi dan hubungan ke sumber.

**Gerbang gambar & prompt:**
- [ ] Jalur A (default) dan B (jika diminta) berakhir pada kumpulan gambar **disetujui**; jumlah gambar disesuaikan storyboard.
- [ ] **Dua prompt utama** per klip, masing-masing mencakup semua shotnya; tidak ada placeholder, gambar yang belum ada, atau sumber tidak jelas.
- [ ] Batas mode Google Flow dan potensi gagalnya multi-shot dipahami; tidak menjanjikan cut presisi.

**Gerbang hasil (dilakukan P3/P4, belum dinyatakan lulus di P2):**
- [ ] Klip hasil user diinspeksi; klaim exterior ≥6s dan kualitas berdasarkan **video sebenarnya**.
- [ ] Perbaikan/retake terdokumentasi; tidak mengklaim video final dan viralitas tanpa bukti.

**Definition of Done P2:** dua file aturan/template tertulis, saling konsisten, memenuhi semua checklist **dokumen/praflight**, dan simulasi kedua opsi gambar dengan timeline lulus. **P2 bukan bukti Omni Flash sudah berhasil membuat video nyata; pilot itu P3.**
