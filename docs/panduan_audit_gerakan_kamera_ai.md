# Panduan Teknis Audit Gerakan Kamera Video Referensi (untuk AI & Kreator)

Dokumen ini adalah panduan baku berbasis eksperimen nyata untuk melatih dan memandu AI dalam mengaudit gerakan kamera pada video vertikal *home tour* (9:16) secara akurat dan konsisten—mampu membedakan **`Dolly-In`**, **`Dolly-Out`**, **`Pan`**, **`Orbit`**, dan **`Truck`**, serta memisahkan pola **`Multi-Phase`** dari **`Simultaneous`**.

---

## 1. Prinsip Dasar & Batasan Metodologi

1. **Wajib Verifikasi Ganda (*Dual-Verification*):** Jangan menyimpulkan gerakan kamera hanya dari angka *optical flow* global atau 1–2 frame tampilan 1 FPS. Selalu gabungkan **pengukuran kuantitatif per interval** (*optical flow*) dengan **pemeriksaan visual *contact sheet*** (6–10 frame per shot).
2. **Transparansi Resolusi Sampling:**
   - **Deteksi batas *cut* antar shot:** dilakukan pada **30 FPS penuh** (seluruh frame) agar titik potong tiap shot presisi.
   - **Audit gerakan kamera makro:** dilakukan pada sampling **6–10 frame berjarak rata per shot** (setara ~2–3 FPS, tiap ~0,35–0,50 detik). Akurat untuk arah makro (*dolly*, *pan*, *orbit*, perubahan fase), tetapi tidak menangkap getaran mikro di bawah 0,3 detik.
3. **Kejujuran Estimasi Derajat:** File video tidak memiliki data sensor giroskop. Angka sudut seperti `~15°` atau `~25°–30°` adalah **estimasi geometris kasar** dari rasio geser horizontal terhadap perkiraan *horizontal FOV* lensa *wide* vertikal (~50°–65°), bukan hasil pengukuran alat ukur.
4. **Anti-Halusinasi Audit:** Jika AI tidak memiliki *code execution*, gunakan Protokol Audit Visual (Bagian 6) dan nyatakan hasilnya sebagai estimasi visual tanpa mengarang angka piksel atau *timestamp*.

---

## 2. Taksonomi Istilah Teknis Baku

Seluruh label hasil audit wajib mengikuti **satu format teknis seragam** (dilarang mencampur bahasa sehari-hari seperti "maju lurus" dengan "Dolly-In"):

**Format Baku:**
`[Mode]: [Komponen Utama] ([Skala]) [+ / →] [Komponen Sekunder] ([Intensitas / Kurva])`

| Elemen | Istilah Teknis Baku | Aturan Pemakaian |
| :--- | :--- | :--- |
| **Mode** | `Multi-Phase:` / `Simultaneous:` | Gunakan `→` untuk perpindahan fase pada `Multi-Phase`, dan `+` untuk gerak serentak pada `Simultaneous`. |
| **Sumbu Z (Kedalaman)** | `Dolly-In`, `Dolly-Out`, `Diagonal Dolly-Out`, `Static Distance` | Gantikan seluruh kata "maju", "mundur", atau "jarak tetap". |
| **Sumbu Rotasi & Geser** | `Orbit Left/Right`, `Pan Left/Right`, `Truck Left/Right` | Gunakan `Orbit` secara konsisten (jangan dicampur dengan `Arc` di label akhir). |
| **Intensitas Pan** | `Subtle (~15°)`, `Moderate (~20°–25°)`, `Strong (~25°–35°)` | Ditentukan dari persentase geser horizontal `|total_dx| / lebar_frame`. |
| **Kurva Kecepatan** | `Constant`, `Accelerating (Ease-In)`, `Decelerating (Ease-Out)` | Dituliskan konsisten pada komponen yang berubah kecepatan atau di akhir label. |

---

## 3. Alur Audit 4 Langkah

### Langkah 1 — Deteksi Batas *Cut* (30 FPS Penuh)
- Baca seluruh frame video secara berurutan, ubah ke *grayscale* kecil (`160×284`), lalu hitung rata-rata selisih piksel absolut antar frame (`mean(|frame_t − frame_{t-1}|)`).
- Lonjakan di atas ambang `> 28–35` (atau turunkan ke `> 20` untuk transisi warna hangat yang mirip) menandai titik *cut* antar shot.

### Langkah 2 — Ekstraksi *Contact Sheet* & Pengukuran *Optical Flow*
- Untuk tiap shot, ekstrak **10 frame berjarak rata** (dari `frame_awal + 1` hingga `frame_akhir - 2`) dan susun menjadi 1 gambar *contact sheet* (2 baris × 5 kolom) berlabel waktu.
- Pada setiap pasangan frame sampel berurutan:
  1. Deteksi hingga 400 titik sudut/tekstur (`cv2.goodFeaturesToTrack`).
  2. Lacak perpindahannya ke frame berikutnya (`cv2.calcOpticalFlowPyrLK`).
  3. Estimasi transformasi 2D (`cv2.estimateAffinePartial2D`) untuk memperoleh **`scale`**, **`dx`** (geser horizontal pusat frame), dan **`dy`** (geser vertikal pusat frame).
  4. Hitung median aliran horizontal di **zona bawah 30% (`fg_dx`, latar depan)** dan **zona atas 30% (`bg_dx`, latar belakang)**, lalu hitung **selisih paralaks relatif**:
     `Δparallax = fg_dx − bg_dx`

### Langkah 3 — Klasifikasi Gerakan (3 Tes & Rumus Baku)

#### A. Sumbu Kedalaman (`scale`) & Kurva Kecepatan
- `total_scale` = perkalian seluruh `scale` interval.
- **`total_scale > 1,10` → `Dolly-In`:** Skala dibaca langsung (misal `2,18` → `~2.2x`).
- **`total_scale < 0,90` → `Dolly-Out`:** Skala pelebaran dihitung dengan **`1 / total_scale`** (misal `0,63` → `1 / 0,63 ≈ 1,59` → `~1.6x`; `0,57` → `~1.75x`).
- **`scale` per interval `0,98 – 1,02` → `Static Distance`** (jarak konstan, misal `Pure Orbit`).
- **Kurva kecepatan:** `scale` terus naik (`1,05 → 1,16`) = `Accelerating (Ease-In)`; `scale` melambat mendekati `1,00` di 1–2 interval akhir (`0,90 → 0,95`) = `Decelerating (Ease-Out)`.

#### B. Matriks 3 Tes Pembeda: `Pan` vs `Orbit` vs `Truck`

| Jenis Gerakan | Tes 1: Tutup-Buka Benda Depan (*Occlusion*) | Tes 2: Nilai `Δparallax = fg_dx − bg_dx` | Tes 3: Sudut Perspektif & Posisi Subjek |
| :--- | :--- | :--- | :--- |
| **`Pan`** (menoleh di tempat) | **Tidak ada** — benda depan & belakang bergeser serempak tanpa saling menutupi. | `Δparallax ≈ 0` (`fg_dx ≈ bg_dx`) | Sudut kemiringan dinding/meja **tetap sama**; bidang pandang menyapu ke objek sebelah. |
| **`Orbit`** (melingkar mengitari subjek) | **Ada & jelas** — benda depan (kusen pintu, meja, semak) bergeser menutupi/membuka benda belakang. | `|Δparallax|` **besar** (umumnya `> 20–30px`/interval) | Subjek utama **tetap terbingkai**, sementara **sudut pandang 3D berubah** (dinding samping terbuka, kemiringan meja berputar). |
| **`Truck`** (geser menyamping lurus) | **Ada & jelas** — benda depan bergeser cepat relatif terhadap latar belakang. | `|Δparallax|` **besar** | Lensa menghadap lurus tanpa mengunci subjek; subjek meluncur lurus melintasi layar dari tepi ke tepi. |

#### C. Rumus Arah Fisik & Intensitas `Pan`
- **Pada `Pan` Murni (`Δparallax ≈ 0`):** `dx < 0` (gambar geser kiri) = **`Pan Right`**; `dx > 0` (gambar geser kanan) = **`Pan Left`**.
- **Pada `Orbit` atau `Truck` (`|Δparallax|` besar):**
  - `fg_dx − bg_dx > 0` (benda depan geser lebih ke **kanan** relatif ke belakang) = badan kamera bergerak ke **KIRI (`Orbit Left` / `Truck Left`)**.
  - `fg_dx − bg_dx < 0` (benda depan geser lebih ke **kiri** relatif ke belakang) = badan kamera bergerak ke **KANAN (`Orbit Right` / `Truck Right`)**.
- **Estimasi Intensitas `Pan` (rasio `|total_dx| / lebar_frame` pada 9:16):**
  - `15%–20%` → **`Subtle (~15°)`**
  - `21%–30%` → **`Moderate (~20°–25°)`**
  - `> 35%` → **`Strong (~25°–35°)`**

#### D. Deteksi `Multi-Phase` vs `Simultaneous` & Aturan `dy` (*Tilt*)
- **`Multi-Phase`:** Ada perubahan vektor tajam di tengah klip (misal `0–2s` `scale ≈ 1,01` lalu `2–5s` `scale > 1,12`; atau `0–2s` `dx ≈ 0` lalu `2–3,5s` `dx` melonjak `> 30px`).
- **`Simultaneous`:** Seluruh komponen gerak aktif bersamaan sejak `0,0s` hingga akhir.
- **Aturan `dy` (*Tilt* Tipis):** Pergeseran vertikal kecil sering muncul alami dari perspektif lensa lebar saat `Dolly-In`/`Dolly-Out`. **Abaikan dan jangan labeli sebagai *tilt*** kecuali terlihat gerakan *crane* / dongak-tunduk vertikal yang ekstrem di *contact sheet*.

### Langkah 4 — Verifikasi Silang Visual (Anti-3 Jebakan Klasik)
1. **Jebakan `Pan` Kuat Menutupi Sinyal `Orbit`:** Pada `Orbit Left + Strong Pan Right`, `fg_dx` dan `bg_dx` bisa **sama-sama negatif** (misal `-28px` vs `-75px`). Jangan hanya melihat tandanya—hitung **`Δparallax = -28 − (-75) = +47px`** lalu cek *occlusion* benda depan di *contact sheet*.
2. **Jebakan Angka Global pada Eksterior:** `total_scale` bisa menyembunyikan fase `Pure Orbit` di 2 detik awal. Selalu cek deret per interval + *contact sheet* untuk melihat apakah dinding samping bangunan berputar terbuka sebelum kamera masuk `Dolly-In`.
3. **Jebakan Menyamakan `Diagonal Dolly-Out` dengan `Orbit`:** Jika sudut dinding belakang dan tepi kasur tetap paralel dari awal hingga akhir tanpa rotasi sudut tajam, labeli sebagai `Diagonal Dolly-Out + Pan`, bukan `Orbit`.

---

## 4. 10 Studi Kasus Nyata Lengkap (Hasil 3 Video Eksperimen)

### A. Pola `Dolly-In` (`Multi-Phase` & `Simultaneous`)

| # | Label Teknis Baku | Pola Angka Terukur | Konfirmasi Visual & Pelajaran Kunci |
| :--- | :--- | :--- | :--- |
| **1** | `Multi-Phase: Pure Orbit Left → Accelerating Dolly-In (~2.0x)` | `0–2s`: `scale ≈ 1,01`, `fg_dx = +17px`, `bg_dx = -22px` (`Δparallax = +39px`). `2–5,5s`: `scale` naik `1,04 → 1,12`. | Semak depan bergeser ke kanan & pohon belakang ke kiri pada 2s awal (orbit murni), lalu tangga spiral keluar kiri saat kamera meluncur cepat ke pintu (*J-Curve* kiri). |
| **2** | `Multi-Phase: Pure Orbit Right → Accelerating Dolly-In (~2.1x)` | `0–2s`: `scale ≈ 1,01`, `fg_dx = -35px`, `bg_dx = +24px` (`Δparallax = -51px`). `2–4,7s`: `scale` naik `1,09 → 1,19`. | Jalan setapak depan bergeser ke kiri & pohon belakang ke kanan, dinding samping kanan teras terbuka, lalu akselerasi lurus ke pintu (*J-Curve* kanan). |
| **3** | `Multi-Phase: Straight Dolly-In → Dolly-In + Strong Pan Right (~25°–30°)` | `0–2s`: `scale ~1,06`, `dx ≈ -2 s/d -5px` (nol). `2–3,5s`: `scale ~1,05`, `dx` melonjak `-23 → -45 → -60px`. | Selama 2s awal jendela/wastafel diam di sumbu tengah vertikal; setelah detik ke-2 seluruh sisi kiri tersapu keluar frame secara tajam. |
| **4** | `Simultaneous: Accelerating Dolly-In (~2.2x) + Accelerating Pan Left (~25°–30°)` | `total_scale = 2,18` (`1,05 → 1,16`); `dx` positif naik terus (`+3 → +57px`, total `+35,7%`); `fg_dx` & `bg_dx` searah kanan. | Sudut dinding ubin & kabinet tetap paralel (bukan orbit); rak kanan & kompor keluar ke kanan, mengunci ketat ke sisi kiri dapur. |
| **5** | `Simultaneous: Dolly-In (~2.0x) + Subtle Pan Right (~15°)` | `total_scale = 1,94`; `dx` konsisten `-8 s/d -16px` (`-14,6%`); `Δparallax ≈ 0` (`-0,5 s/d +6px`); `dy` positif ringan. | Sudut kabin *shower* tetap datar (pan murni halus); `dy` diabaikan karena murni efek ekspansi perspektif lensa lebar saat mendekat. |

### B. Pola `Dolly-Out` (`Orbit`, `Diagonal` & Kasus Jebakan)

| # | Label Teknis Baku | Pola Angka Terukur | Konfirmasi Visual & Pelajaran Kunci |
| :--- | :--- | :--- | :--- |
| **6** | `Simultaneous: Dolly-Out (~1.6x) + Orbit Left + Subtle Pan Right (Ease-Out)` | `total_scale = 0,63` (`1/0,63 ≈ 1,6×`); `dx` negatif (`-10 s/d -25px`); `Δparallax = +39 s/d +50px`; melambat di akhir (`scale = 0,97`). | Sofa depan geser kanan, jendela belakang geser kiri; dinding TV berputar makin miring ke sisi kiri sementara 4 jendela lengkung terbuka di kanan. |
| **7** | `Simultaneous: Dolly-Out (~1.75x) + Orbit Right + Strong Pan Left (Ease-Out)` | `total_scale = 0,58` (`1/0,58 ≈ 1,75×`); `dx` positif besar (`+26 → +56 → +28px`, total `+37,1%`); `fg_dx` negatif `-7px` vs `bg_dx` `+34px` (`Δparallax = -41px`). | Sudut pandang berputar drastis dari frontal (0°) menjadi diagonal 45°; kemiringan meja kopi berputar tajam sementara 2 jendela kiri terbuka. |
| **8** | `Simultaneous: Mild Dolly-Out (~1.3x) + Orbit Left + Strong Pan Right (~35°, Ease-Out)` | `total_scale = 0,76` (`~1,3×`); `dx = -326px` (`-45,3%`); `fg_dx = -28px` vs `bg_dx = -75px` → **`Δparallax = +47px`**. | **Kasus Jebakan:** `fg_dx` & `bg_dx` sama-sama negatif, tetapi di *contact sheet* kusen pintu kayu di depan menutupi saklar lampu & nakas di belakangnya — bukti pasti `Orbit Left`. |
| **9** | `Simultaneous: Diagonal Dolly-Out (~2.5x) + Moderate Pan Right (Ease-Out)` | `total_scale = 0,40` (`1/0,40 = 2,5×`); `dx = -198px` (`-27,6%`); `scale` melambat `0,90 → 0,94` di akhir. | Kamera mundur jauh menyusuri lorong kiri melintasi atas meja marmer *peninsula* hingga seluruh dapur, plafon lengkung, dan 2 jendela kanan terbuka. |
| **10** | `Simultaneous: Diagonal Dolly-Out (~1.75x) + Subtle Pan Left (Ease-Out)` | `total_scale = 0,57` (`~1,75×`); `dx` positif sedang (`+10 → +25 → +15px`, total `+21,3%`). | Pembeda `Diagonal Dolly-Out` vs `Orbit`: sudut dinding belakang dan jendela kanan tetap paralel tanpa rotasi tajam; sisi kiri ruangan terbuka lebar. |

---

## 5. Skrip Python OpenCV Siap Pakai (AI dengan *Code Execution*)

```python
import cv2
import numpy as np

VIDEO_PATH = "path/to/reference_video.mp4"
CUT_THRESHOLD = 28.0  # Turunkan ke 20.0 jika ada transisi warna hangat yang halus

cap = cv2.VideoCapture(VIDEO_PATH)
fps = cap.get(cv2.CAP_PROP_FPS)
total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(f"FPS: {fps:.2f}, Frames: {total}, Res: {w}x{h}, Dur: {total/fps:.2f}s")

# 1. Deteksi batas cut pada FPS penuh
prev = None
cuts = [0]
for i in range(total):
    ret, frame = cap.read()
    if not ret:
        break
    small = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), (160, 284))
    if prev is not None:
        diff = np.mean(np.abs(small.astype(float) - prev.astype(float)))
        if diff > CUT_THRESHOLD and (i - cuts[-1] > 20):
            cuts.append(i)
    prev = small
cuts.append(total)
print("Detected cuts (frame, sec):", [(c, round(c / fps, 2)) for c in cuts])

# 2. Audit per shot: Contact Sheet 10 frame + Optical Flow + Delta Parallax
for idx in range(len(cuts) - 1):
    s, e = cuts[idx], cuts[idx + 1]
    dur = (e - s) / fps
    print(f"\n=== SHOT {idx+1} [{s/fps:.2f}s - {e/fps:.2f}s, dur={dur:.2f}s] ===")
    frs = np.linspace(s + 1, e - 2, 10, dtype=int)

    # Buat Contact Sheet 2x5
    thumbs = []
    for fr in frs:
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(fr))
        ret, img = cap.read()
        if ret:
            t = (fr - s) / fps
            sm = cv2.resize(img, (240, 426))
            cv2.putText(sm, f"+{t:.2f}s", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
            thumbs.append(sm)
    if len(thumbs) == 10:
        grid = np.vstack([np.hstack(thumbs[:5]), np.hstack(thumbs[5:])])
        cv2.imwrite(f"shot{idx+1}_grid.jpg", grid)

    # Hitung Optical Flow & Delta Parallax per interval
    tot_scale, tot_dx, tot_dy = 1.0, 0.0, 0.0
    print("Interval | scale | dx | dy | fg_dx | bg_dx | d_parallax(fg-bg)")
    for j in range(len(frs) - 1):
        f0, f1 = int(frs[j]), int(frs[j + 1])
        cap.set(cv2.CAP_PROP_POS_FRAMES, f0)
        _, im0 = cap.read()
        cap.set(cv2.CAP_PROP_POS_FRAMES, f1)
        _, im1 = cap.read()
        g0 = cv2.cvtColor(im0, cv2.COLOR_BGR2GRAY)
        g1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
        pts0 = cv2.goodFeaturesToTrack(g0, maxCorners=400, qualityLevel=0.01, minDistance=12)
        if pts0 is None or len(pts0) < 10:
            continue
        pts1, st, _ = cv2.calcOpticalFlowPyrLK(g0, g1, pts0, None)
        gp0, gp1 = pts0[st == 1], pts1[st == 1]
        if len(gp0) < 10:
            continue
        M, _ = cv2.estimateAffinePartial2D(gp0, gp1)
        if M is None:
            continue
        sc = np.sqrt(M[0, 0] ** 2 + M[1, 0] ** 2)
        cx, cy = w / 2, h / 2
        dx = (M[0, 0] * cx + M[0, 1] * cy + M[0, 2]) - cx
        dy = (M[1, 0] * cx + M[1, 1] * cy + M[1, 2]) - cy
        tot_scale *= sc
        tot_dx += dx
        tot_dy += dy

        flow = gp1 - gp0
        fg_dx = np.median(flow[gp0[:, 1] > h * 0.7, 0]) if np.any(gp0[:, 1] > h * 0.7) else 0.0
        bg_dx = np.median(flow[gp0[:, 1] < h * 0.3, 0]) if np.any(gp0[:, 1] < h * 0.3) else 0.0
        dp = fg_dx - bg_dx
        t0, t1 = (f0 - s) / fps, (f1 - s) / fps
        print(f"+{t0:.2f}-{t1:.2f}s | {sc:.3f} | {dx:+6.1f} | {dy:+5.1f} | {fg_dx:+6.1f} | {bg_dx:+6.1f} | {dp:+7.1f}")

    inv = f" (~{1/tot_scale:.2f}x wider)" if tot_scale < 0.95 else f" (~{tot_scale:.2f}x closer)"
    print(f"TOTAL: scale={tot_scale:.3f}{inv}, dx={tot_dx:+.1f}px ({tot_dx/w*100:+.1f}%), dy={tot_dy:+.1f}px")
```

---

## 6. Protokol Audit Visual (*Fallback* untuk AI Tanpa Python)

Jika AI hanya dapat melihat frame video tanpa eksekusi kode, jalankan 4 pemeriksaan visual berurutan pada frame awal, tengah, dan akhir tiap shot:

1. **Cek Sumbu Kedalaman (`Dolly-In` vs `Dolly-Out`):** Objek tengah membesar ke tepi frame → `Dolly-In`; objek tengah menyusut dan area baru terbuka di sekelilingnya → `Dolly-Out`.
2. **Tes Tutup-Buka (*Occlusion Test* — `Pan` vs `Orbit`):** Pilih 1 benda paling dekat kamera (kusen pintu, ujung sofa, tiang, semak) dan 1 benda di belakangnya. Jika benda depan menutupi atau membuka benda belakang → `Orbit` / `Truck` (benda depan geser kanan relatif ke belakang = `Orbit Left`; geser kiri = `Orbit Right`). Jika tidak saling menutupi dan sudut dinding tetap paralel → `Pan` (objek geser kiri = `Pan Right`; geser kanan = `Pan Left`).
3. **Cek `Multi-Phase` vs `Simultaneous`:** Bandingkan separuh awal dengan separuh akhir: apakah ada fase `Pure Orbit` atau `Straight Dolly-In` sebelum berubah arah? Jika ya → `Multi-Phase`; jika mengalir serentak sejak awal → `Simultaneous`.
4. **Pelaporan Jujur:** Tuliskan label memakai **Taksonomi Istilah Teknis Baku (Bagian 2)** dengan catatan bahwa skala dan sudut adalah estimasi visual, tanpa mengarang angka piksel atau *timestamp* yang tidak dapat diverifikasi.