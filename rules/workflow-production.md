# HOMEKU — Workflow Produksi Video v1.2 (Production Lite)

> **Status:** aturan operasional untuk ide dan video rumah baru, bukan workflow analisis referensi.  
> **Sumber observasi:** [Ringkasan DNA P1](../knowledge/dna-summary.md), dilanjutkan dengan paket asli di `references/<ID>/`. **Template eksekusi:** [`templates/production.md`](../templates/production.md). **Roadmap:** [rencana implementasi](../docs/production-lite-v1.1-implementation-plan.md), [Issue #7](https://github.com/milyarderpro/homeku/issues/7).  
> **Perubahan v1.2:** default **satu storyboard image kolase lima panel beresolusi tinggi**; **dua prompt Google Flow singkat berbahasa Indonesia**; kamera dolly/tracking yang benar-benar mengungkap ruang; **tanpa musik, hanya ambience alami**.  
> **Prioritas aturan:** untuk **prosedur produksi**, dokumen v1.2 ini dan template v1.2 menggantikan ketentuan lama tentang 5 gambar terpisah, prompt panjang berbahasa Inggris, dan audio bebas pada P0/P1. **Fakta dan observasi DNA P1 tidak diubah**.

## 0. Pemicu, sumber kebenaran, dan batas aman

Workflow produksi dijalankan saat user meminta **ide video rumah baru, desain/storyboard, gambar kolase, prompt Flow, atau QA pilot**. Jika user mengunggah video untuk **analisis referensi**, jalankan [`workflow-analysis.md`](workflow-analysis.md) v1.4 **bukan** dokumen ini.

Sebelum produksi:
1. Baca ringkasan DNA beserta katalog 58 referensi sebagai **indeks**. Pilih **1 referensi utama + 1–2 pendukung** yang berbeda perannya. Baca ulang `analysis.yaml`, `analysis.md` dan storyboard/keyframe relevan untuk referensi terpilih.
2. Rekam sumber dengan `reference_id`, `shot_id`, `field_path`, fakta visual, apa yang diadaptasi, perbedaan orisinal, dan ketidakpastian.
3. Gunakan **semua tujuh DNA**: **DNA-01** hook exterior; **DNA-02** arsitektur; **DNA-03** lingkungan; **DNA-04** interior/posisi objek; **DNA-05** framing dan gerak kamera; **DNA-06** lighting/mood; **DNA-07** ritme, alur, transisi. Video harus terasa seperti **tur rumah**, bukan hanya lima foto dekorasi.
4. Pisahkan **[FAKTA REFERENSI]**, **[INTERPRETASI]**, **[KREASI BARU]** dan **[ATURAN PRODUKSI]**. Analisis referensi visual **tidak** membuktikan metrik retensi/virality maupun audio asli. `common_regions` berarti wilayah terkait gaya, bukan lokasi rumah.
5. Interaksi, Design Lock, storyboard, **prompt image dan video default memakai bahasa Indonesia**; istilah teknis seperti `dolly in`, `tracking right`, `parallax`, `hard cut` boleh tetap dalam bahasa Inggris. Bila user minta prompt bahasa lain, sesuaikan.

**Tidak diubah:** `references/`, `video/`, `requests/`, `rules/workflow-analysis.md`, YAML analisis, dan GitHub Actions. `save now` **khusus workflow analisis**; tidak pernah berarti izin menulis produksi.

## 1. Kontrak produksi yang tetap berlaku

| Parameter | Aturan |
| --- | --- |
| Bentuk akhir | Rumah baru orisinal; target **20 detik**, **vertical 9:16** |
| Generasi | **2 klip × 10 detik** Google Flow Omni Flash; **1 prompt utama per klip** |
| Hook | Exterior terlihat sejak frame pertama dan berlangsung **≥6,00 detik outdoor-only**; bukan durasi shot gabungan yang sudah menampilkan interior |
| Clip A (lokal) | **S01 Exterior 0–6s**, **S02 Living 6–10s**, `hard cut` pada detik lokal 6 |
| Clip B (lokal) | **S03 Kitchen 0–4s**, **S04 Bedroom 4–7s**, **S05 Bathroom 7–10s**, `hard cut` pada detik lokal 4 dan 7 |
| Waktu global | 0–6 exterior; 6–10 living; 10–14 kitchen; 14–17 bedroom; 17–20 bathroom |
| Gambar default | **SATU** storyboard image rasio landscape sekitar **3:2**, berisi **lima panel** berlabel S01–S05 untuk kelima shot |
| Prompt default | **Simple First**: prompt singkat **bahasa Indonesia**, 2 prompt total, satu per klip; jangan mengulang Design Lock panjang bila sudah tercermin pada storyboard |
| Kamera | `dolly in`, `dolly out`, `tracking right`, `tracking left`, atau kombinasi; gerak disesuaikan ruangan dan durasi, **perspective change + parallax nyata**, bukan zoom digital |
| Cakupan ruang | Sejak awal shot interior, **susunan ruangan utama hampir seluruhnya terbaca**; gerak mengungkap tambahan detail tanpa memotong furniture/fitur penting sebelum akhir |
| Suara | **Tidak ada musik, vokal, dialog/narasi, atau SFX sinematik**; hanya ambience alami halus dan relevan; bila Flow tak patuh, **QA audio gagal** |
| Sumber | Tujuh DNA direkam di Design Lock, shot detail, dan panel. Detail panjang **tidak wajib diulang** dalam prompt video |
| Perubahan | Jumlah shot atau panel boleh berubah jika disetujui dan punya alasan DNA, tetapi harus memetakan **semua shot dengan jelas**, mempertahankan **dua 10s** dan exterior ≥6s |

**Batas kemampuan model:** satu gambar kolase adalah **reference sheet**, bukan bukti mode Flow dapat membaca 5 panel sebagai 5 image inputs independen. Jika mode hanya mendukung *first frame / last frame*, **jangan** memasang seluruh kolase sebagai frame awal karena label/garis panel bisa dianimasikan. Pilih input referensi/ingredients/storyboard **jika tersedia dan teruji**; jika tak tersedia atau Flow hanya menggerakkan kolase seperti slide, gunakan fallback yang disetujui user (mis. panel hasil crop/5 gambar terpisah) dan **catat perubahan jalur**. Tidak ada jaminan `hard cut` atau timing tepat per-frame dari satu generasi; QA hasil video wajib.

## 2. Enam langkah dengan gerbang persetujuan

| Step | Tugas AI | Syarat lanjut |
| --- | --- | --- |
| **1. DNA Selection** | Pelajari P1, baca 2–3 paket referensi dan ketujuh DNA; cantumkan ID serta bukti kamera/komposisi | Data sumber read-only, tidak mengada-ada |
| **2. Idea Generation** | Beri **3 ide berbeda** dengan hook, sumber/roles, pembeda orisinal, sinematografi dan risiko | **Gate 1:** user memilih **satu** konsep |
| **3. Design Lock & Storyboard** | Tetapkan rumah satu identitas, lanskap/window views, furnitur, lighting, shot framing awal-akhir, kamera/reveal, dua timeline 10s | **Gate 2:** user setujui desain dan storyboard |
| **4. Storyboard Image** | **Opsi A DEFAULT:** AI buat **1 image kolase**; **Opsi B jika diminta:** AI buat **1 prompt untuk menghasilkan kolase**; cek kelima panel | **Gate 3:** kolase **nyata** tersedia dan **disetujui** user |
| **5. Simple Omni Prompts** | Buat **2 prompt singkat bahasa Indonesia**, panel A=S01–S02 dan B=S03–S05; camera, cuts, ambience, larangan kolase ditayangkan | Preflight waktu, mapping, audio, gambar; keluarkan prompt saat Gate 3 lulus |
| **6. Generate & QA** | User jalankan Flow, upload dua klip atau gabungannya; AI audit **visual + audio**, revisi tepat pada masalahnya | Hasil P3/P4 belum lulus sebelum **video aktual** dan suara diperiksa |

**Pengendalian status:** `idea_options → idea_selected → design_draft → design_approved → storyboard_image_pending → storyboard_image_approved → prompts_ready → qa_pending → revision_required / final_approved`. Perubahan besar pada Design Lock **membatalkan approval gambar/prompt yang terdampak**. User boleh meminta revisi pada titik mana pun; jangan memaksa mengulang tahap sebelumnya yang tidak terdampak.

### Step 1–2: memilih dan mengolah DNA

Untuk setiap ide wajib ada satu arsitektur utama, satu pendukung lingkungan/interior/lighting, dan pendukung opsional sinematografi/edit. Uraikan kontribusi tiap referensi **tanpa** mengimpor seluruh facade/atap pendukung. Pastikan ketujuh DNA tercermin dalam keputusan final, misalnya:
- **DNA-01:** rumah utuh sejak frame 0 dan perubahan fokus eksterior selama 6s.
- **DNA-02:** gaya dan geometri rumah yang konsisten.
- **DNA-03:** path, pohon, landscape, kondisi luar dan view melalui jendela.
- **DNA-04:** ruangan utuh dan relasi sofa–kursi–meja–jendela, island–range–sink, bed–nightstand–window, vanity–shower–tub.
- **DNA-05:** framing dan **gerak yang mengubah posisi/perspektif kamera**, tidak hanya lensa zoom.
- **DNA-06:** arah cahaya/warm practical lamps/warna yang sama lintas panel.
- **DNA-07:** urutan shot, ritme, hard cut dan komposisi akhir yang memuaskan.

Setiap Idea Card memuat nama, tampak rumah, lingkungan, hook, 2–3 sumber dan perannya, gerak kamera/ritme yang dipinjam, elemen baru, urutan target 20s, risiko. Ketiga ide **berbeda secara substantif**, bukan sekadar warna. Jangan membuat gambar sampai user memilih satu.

### Step 3: Design Lock + storyboard — detail tetap diperlukan di sini

Kunci: massa/skala/level/roofline; facade, pintu & kusen; material/warna; path, pohon dan window view; hubungan living–kitchen–bedroom–bathroom; posisi objek dan pencahayaan; lensa/perspektif wajar; gaya tur dan waktu tiap shot.

Untuk **setiap shot S01–S05** isi:
`shot_id`, `source_reference_ids/shot_ids/field_paths`, `clip_id`, `global_start/end_s`, `local_start/end_s`, `framing_start/end`, `view_angle`, `focal_subject`, `camera_movement` + `speed`, `reveal_path`, `architecture_anchors`, `furniture_anchors`, `environment_anchors`, `lighting`, `transition_out`, `uncertainty`.

Syarat framing: interior bukan close-up yang menutupi mayoritas ruangan; **paling lambat paruh awal shot** pengguna dapat membaca tata ruang penting, dan pada akhir shot subjek utama **tidak terpotong**. Gerak **bertujuan**: pilih salah satu/kombo `dolly` dan `tracking` yang menghasilkan pergeseran relatif foreground–midground–background. Cek waktu lokal Clip A/B terpisah; tidak boleh ada gap/overlap. Sampaikan desain+storyboard dalam Bahasa Indonesia dan tunggu Gate 2.

### Step 4: satu storyboard image 5 panel — SOP versi 1.2

**Opsi A DEFAULT:** setelah Gate 2, **generate satu gambar gabungan** yang memuat **semua panel sekaligus**, bukan lima gambar terpisah dan bukan kolase yang menggabungkan lima gambar generasi berbeda secara otomatis. User memberi persetujuan untuk seluruh panel. Opsi B **hanya atas permintaan:** buat **satu prompt** (bahasa Indonesia kecuali istilah teknis yang berguna), kemudian user menghasilkan/mengunggah **satu** gambar kolase; **prompt belum dianggap gambar**.

**Spesifikasi default board:**
1. **Kanvas landscape sekitar 3:2**. Target **≥3072×2048 px hanya jika generator mendukung resolusi native yang memadai**; jika tidak, hasil terbaik yang tersedia harus dilaporkan, tidak mengklaim native tinggi hanya karena upscaling. Prioritaskan **keterbacaan setiap panel** pada ukuran sebenarnya, bukan angka piksel semata.
2. **Dua panel lebar pada baris atas**: **S01 Exterior (0–6s)** kiri, **S02 Living (6–10s)** kanan. **Tiga panel pada baris bawah**: **S03 Kitchen (10–14s)**, **S04 Bedroom (14–17s)**, **S05 Bathroom (17–20s)**.
3. Label panel ditempatkan sebagai **metadata di pinggir/banner**, tidak menutupi ruangan. Pemisah panel bersih dan tipis. Di output Flow **label, border, dan layout kolase tidak boleh tampil**.
4. **S01:** keseluruhan bangunan **sudah terbaca** plus landscape dan jalur kamera yang punya foreground/midground/background.
5. **S02–S05:** gunakan **wide architectural view** yang memperlihatkan **hampir seluruh karakter ruangan beserta hubungan objek**; ruang tidak boleh sekadar close-up fireplace/island/bed/vanity. Hindari tepi panel memotong sofa, armchair, island, bed, bathtub, atau window utama.
6. Semua panel **satu identitas rumah**: window family, stone/wood, suhu warna, arah cahaya, cuaca, pemandangan eksterior, posisi objek dan perspektif logis. Ingat **panel landscape sebagai acuan komposisi** untuk video portrait 9:16; potongan vertikal 9:16 harus tetap dapat menggambarkan ruang atau Flow perlu membuat sudut pandang baru yang tetap konsisten. Jangan menjanjikan crop otomatis bisa memperlihatkan semua isi panel landscape.
7. **Satu gambar final saja** untuk kedua klip. Setiap panel perlu detail cukup untuk masing-masing shot meskipun area panel lebih kecil daripada gambar terpisah.

**QA Gate 3:** jumlah/urutan/label panel benar, desain cocok, tidak ada clipping objek penting, tiap ruang hampir lengkap, resolusi cukup dibaca ketika di-zoom, panel tidak rusak/tertukar, kedalaman untuk parallax jelas, dan user menyetujui satu board. Jika satu panel buruk, lakukan edit terarah pada panel itu **dengan menjaga empat panel lain**, atau regenerate board dan review ulang. Jangan menganggap panel baru otomatis disetujui.

**Fallback tertib:** jika board tidak bisa menghasilkan panel yang jelas, resolusi terlalu rendah, Flow salah memilih panel, atau kolase justru muncul dalam video, tawarkan **panel crop yang terverifikasi** atau **lima master image terpisah** sebagai alternatif **setelah persetujuan user**. Kembali ke QA aset dan ubah mapping/prompt seperlunya; tidak perlu ulang ide dan Design Lock yang masih valid.

### Step 5: dua prompt video singkat dalam Bahasa Indonesia (Simple First)

**Default Level 1 — Simple Base:** **tidak** memasukkan seluruh DNA Trace, furnitur satu per satu, atau Design Lock berulang. Detail itu sudah ada dalam storyboard dan board. Dua prompt **siap copy** berisi hanya:
- format portrait 9:16, 10s;
- **satu board kolase** sebagai referensi; **panel mana dan urutan+durasi lokal** tiap klip;
- gerak kamera dibatasi `dolly in/out` dan `tracking right/left` atau kombinasi, **kecepatan natural (tidak terlalu lambat/cepat)**;
- hampir semua ruangan terbaca, `perspective change` dan `parallax` nyata, **bukan fake zoom/slideshow**;
- `hard cut` di batas shot, larangan menayangkan label/panel/border, dan kontinuitas;
- **NO MUSIC, NO VOCALS/NARRATION, natural subtle ambience only**.

**Level 2 — Simple + Corrective:** bila hasil aktual gagal, **ulang Level 1 + paling banyak 1–3 instruksi spesifik** yang menyasar masalah teramati, misalnya “living dimulai terlalu dekat; mulai wide agar kursi/sofa utuh”, “kamera cuma zoom; lakukan tracking kanan dengan parallax nyata”, atau “musik muncul; tanpa musik”. **Revisi hanya klip bermasalah dahulu**. Catat timestamp, bukti, versi dan efek revisi.

**Level 3 — Detailed Rescue:** hanya jika Level 2 masih gagal; detail per-shot dari Design Lock, framing awal/akhir, objek, jalur kamera, cahaya, dan pembatasan khusus. **Jangan menjadikan prompt panjang wajib di awal**. Level 3 bukan jaminan model patuh.

**Mode input Flow:** user menggunakan board sebagai *visual reference* **jika mode relevan tersedia**. Jangan mengasumsikan *first/last frame* atau *ingredients* tertentu menerima storyboard panel secara semantik. Jika output memperlihatkan kolase, hentikan pendekatan board sebagai sumber video dan beralih ke fallback aset yang benar setelah persetujuan. Label “S02” dalam prompt adalah **petunjuk pemilihan panel**, bukan teks yang boleh digambar di video.

### Step 6: QA dua klip dan audio alami

Lihat video **aktual**, bukan hanya prompt. Terima video A, B, atau gabungan 20s; bila hanya gabungan tersedia, evaluasi cut global di 6, 10, 14, 17 detik.

**Periksa per shot**: seluruh identitas bangunan/porsi penting ruangan terbaca; objektif camera translation (pergeseran perspektif relatif foreground/midground/background), kamera bergerak natural tidak terlalu pasif/tergesa, tidak hanya crop/zoom; adegan tidak memotong furniture saat berakhir; cut eksplisit; material/jendela/landscape konsisten; tidak ada panel atau label.

**Periksa waktu**: eksterior **≥6s nyata**, dua klip target masing-masing 10s, final 20s/9:16. Durasi dan cut presisi **tidak dijamin** oleh prompt; jika salah, catat dan retake/edit seperlunya dengan persetujuan.

**Periksa audio dengan mendengar/analisis:** harus **tanpa musik, vocal/narasi, SFX sinematik**, hanya ambience alami sesuai adegan (angin ringan di exterior, fireplace crackle di living bila memang tampak menyala, quiet room tone di interior). Jangan menganggap stream audio ada/tiada sebagai bukti bahwa musik ada/tiada—**dengarkan**. Jika Flow tetap membuat musik, **status audio GAGAL**. Opsi pemulihan: regenerasi prompt atau *mute* audio yang bermusik lalu pasang natural ambience baru dalam edit; jangan klaim bisa memisahkan musik bersih dari ambience tanpa bukti.

**Keputusan:** `BELUM DIUJI` / `GAGAL` / `LULUS` **per clip, visual dan audio**. Baru `final_approved` setelah video digabung dan lulus QA serta persetujuan user. Pelajaran pilot lama: gambar bisa indah tetapi **ruang dan gerak kamera gagal**; jangan samakan estetika still image dengan keberhasilan tur video.

## 3. Izin menulis GitHub: selalu terpisah

Selama ideasi, storyboard, gambar, prompt, QA: `references/` dan aturan **read-only**. File `productions/<ID>/production.md` dibuat **hanya** setelah perintah jelas semisal **“Simpan produksi IDEA-001 ke GitHub”**. Periksa ketersediaan ID/path dan konflik, gunakan izin spesifik, commit, lalu **verifikasi remote**. Jangan menambah MP4/JPEG biner besar ke repo secara otomatis.

`save now` **tetap eksklusif** untuk analisis referensi melalui `requests/pending/`. Tidak boleh digunakan pada produksi; jangan membuat/memodifikasi `requests/`, `references/`, `video/`, atau GitHub Actions.

## 4. Definition of Done v1.2 dan skenario gagal

**Pemeriksaan pra-generasi**
- [ ] Tiga ide dibuktikan dari DNA referensi; user pilih satu; Design Lock/storyboard disetujui.
- [ ] Tujuh DNA, source trace, framing dan camera reveal tiap shot ada dalam data produksi **walau prompt video sengaja singkat**.
- [ ] Board memuat **lima panel benar S01–S05**, 2 atas + 3 bawah, layout/rasio/resolusi memadai, semua ruangan hampir utuh dan readable; user setujui **satu board**.
- [ ] Clip A 6+4=10; Clip B 4+3+3=10; dua prompt ringkas bahasa Indonesia; cakupan shot benar, tanpa label kolase dan tanpa musik.
- [ ] Jika Flow tidak mendukung storyboard referensi atau 3D parallax dari board, pembatasan dijelaskan dan fallback disetujui.

**Pemeriksaan hasil aktual (P3/P4)**
- [ ] Kamera menampilkan **perubahan perspektif dan parallax**, bukan hanya zoom.
- [ ] Living/kitchen/bed/bath room **nyaris utuh**, tidak terpotong sebelum cut.
- [ ] Exterior outdoor-only ≥6s; cut/ruang dan timing sesuai.
- [ ] Audio **tanpa musik**, hanya ambience alami yang terdengar masuk akal.
- [ ] User menerima hasil; kegagalan/retake terdokumentasi.

**Penting:** dokumen aturan yang lulus tidak berarti Flow telah lulus QA. Pilot P3 sebelumnya **`revision_required`** sampai video baru diuji; v1.2 merupakan perubahan workflow berdasar temuan tersebut, **bukan bukti jaminan hasil yang lebih baik**.
