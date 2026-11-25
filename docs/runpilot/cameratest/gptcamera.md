# **Audit kamera — dreamshome01.mp4**

Audit menggunakan metode **HOMEKU 3.0** dari kit yang dilampirkan, dengan fokus pada gerakan kamera, perubahan fase, tempo, framing awal, serta bukti visual temporal.

## **1. Verifikasi sumber dan metode**

| Parameter                             | Hasil                                                               |
| ------------------------------------- | ------------------------------------------------------------------- |
| Ekstraksi kit                         | Berhasil                                                            |
| `python homeku_runtime.py --output .` | Berhasil — 54 resource runtime dipulihkan                           |
| `audit/visual-audit.md`               | Dibaca                                                              |
| `audit/authoring.md`                  | Dibaca                                                              |
| `audit/camera-cases.md`               | Dibaca                                                              |
| Resolusi video                        | 720 × 1280, vertikal 9:16                                           |
| Frame rate native                     | 30 FPS                                                              |
| Jumlah frame                          | 601                                                                 |
| Durasi stream video                   | 20,033 detik                                                        |
| Baseline                              | 6 FPS + batas native setiap shot                                    |
| Pendalaman                            | Frame tambahan dan native pada interval yang memerlukan pemeriksaan |
| Jumlah shot                           | 5                                                                   |

Notasi `+` menunjukkan komponen yang berlangsung simultan, sedangkan `→` menunjukkan perubahan fase secara kronologis. IN dan OUT menunjukkan arah kedalaman, bukan arah sapuan gambar.

## **2. Pemeriksaan cut dan transisi**

| Shot | Area             | Rentang frame native | Rentang PTS     | Transisi masuk       |
| ---- | ---------------- | -------------------- | --------------- | -------------------- |
| 01   | Exterior & Porch | F0–F183              | 0,000–6,100 s   | Awal video           |
| 02   | Living Room      | F184–F287            | 6,133–9,567 s   | Soft blur transition |
| 03   | Kitchen & Dining | F288–F392            | 9,600–13,067 s  | Hard cut             |
| 04   | Bedroom          | F393–F496            | 13,100–16,533 s | Hard cut             |
| 05   | Bathroom         | F497–F600            | 16,567–20,000 s | Hard cut             |

**Cut indices:** `[184, 288, 393, 497]`

Batas tiga hard cut dapat ditetapkan langsung dari frame native. Untuk transisi Shot 01 → 02, saya menggunakan F184 sebagai titik pemisah operasional karena frame tersebut merupakan bagian transisi yang paling tertutup blur. Batas ini bukan hard cut dan tidak menunjukkan awal gerakan kamera yang dapat diamati secara jernih.

## **3. Tabel hasil Camera Movement**

| Shot                      | Urutan fase dan notasi kamera                                         | Depth Direction     | Tempo    |
| ------------------------- | --------------------------------------------------------------------- | ------------------- | -------- |
| **01 — Exterior & Porch** | Orbit Right → Orbit Right + Dolly-In → Accelerating Dolly-In (\~1.7×) | NO IN/OUT → IN → IN | Moderate |
| **02 — Living Room**      | Dolly-Out (\~1.7×) + Orbit Right + Moderate Pan Left (Ease-Out)       | OUT                 | Moderate |
| **03 — Kitchen & Dining** | Straight Dolly-In (\~1.2×) → Dolly-In (\~1.4×) + Moderate Pan Right   | IN → IN             | Moderate |
| **04 — Bedroom**          | Diagonal Dolly-Out (\~1.7×) + Moderate Pan Left (Ease-Out)            | OUT                 | Moderate |
| **05 — Bathroom**         | Dolly-In (\~2.1×) + Subtle Pan Right                                  | IN                  | Moderate |

Skala pada notasi merupakan estimasi perubahan ukuran jangkar dalam gambar, bukan pengukuran jarak fisik kamera atau focal length. Untuk Shot 01 dan 03, skala yang ditulis berlaku pada fase terkait, bukan seluruh durasi shot.

## **4. Analisis fase dan bukti visual**

### **Shot 01 — Exterior & Porch**

Durasi 6,133 detik · Orbit menuju pendekatan teras

| Fase            | Interval perkiraan | Notasi                          |
| --------------- | ------------------ | ------------------------------- |
| 1               | 0,000–1,000 s      | Orbit Right                     |
| 2               | 1,000–3,000 s      | Orbit Right + Dolly-In (\~1.3×) |
| 3               | 3,000–5,833 s      | Accelerating Dolly-In (\~1.7×)  |
| Transisi keluar | 5,900–6,100 s      | Blur — bukan gerak kamera       |

**Frame pembanding:**

| Frame | PTS (s) | Pengamatan                                                           |
| ----- | ------- | -------------------------------------------------------------------- |
| F0    | 0,000   | Fasad hampir frontal, pohon besar di kiri.                           |
| F15   | 0,500   | Pohon dekat mulai bergeser ke kiri terhadap rumah.                   |
| F30   | 1,000   | Sisi kanan rumah semakin terlihat, perubahan skala masih kecil.      |
| F45   | 1,500   | Pendekatan mulai lebih jelas bersamaan dengan perubahan sudut fasad. |
| F75   | 2,500   | Dinding samping kanan terbuka lebih luas.                            |
| F90   | 3,000   | Orientasi fasad mulai relatif stabil.                                |
| F120  | 4,000   | Tangga dan tiang teras membesar.                                     |
| F150  | 5,000   | Pendekatan semakin dominan.                                          |
| F175  | 5,833   | Teras memenuhi bingkai; fasad kiri mulai terpotong.                  |

**Observations**

- **Depth:** perubahan skala relatif kecil pada awal, lalu meningkat menuju tangga dan pintu.
- **Translation:** pohon dekat bergeser lebih banyak daripada latar pepohonan. Sisi kanan bangunan terbuka, mendukung Orbit Right.
- **Rotation:** perubahan sudut pandang paling jelas pada bagian awal hingga pertengahan. Tidak cukup bukti untuk menetapkan Pan sebagai komponen terpisah.
- **Tempo:** awal tenang, kemudian pendekatan terlihat semakin cepat. Sebagian peningkatan laju gambar juga berasal dari perspektif.

**Pendalaman:** F24–F48 dan F72–F102 untuk membedakan kapan pendekatan mulai dominan dan kapan perubahan sisi fasad mereda. Batas fase bersifat perkiraan karena komponen berubah secara gradual.

Frame pembanding Shot 01

### **Shot 02 — Living Room**

Durasi 3,467 detik · Pullback dengan perubahan arah pandang

| Fase           | Interval perkiraan | Notasi                                                          |
| -------------- | ------------------ | --------------------------------------------------------------- |
| Transisi masuk | 6,133–6,367 s      | Blur                                                            |
| 1              | 6,400–9,567 s      | Dolly-Out (\~1.7×) + Orbit Right + Moderate Pan Left (Ease-Out) |

**Frame pembanding:**

| Frame | PTS (s) | Pengamatan                                               |
| ----- | ------- | -------------------------------------------------------- |
| F184  | 6,133   | Bingkai tertutup blur.                                   |
| F190  | 6,333   | Fireplace terlihat, tetapi masih ada haze.               |
| F192  | 6,400   | Framing interior sudah jernih dan layak digunakan.       |
| F210  | 7,000   | Meja dan fireplace mengecil.                             |
| F220  | 7,333   | Sisi meja dan sofa mulai terbuka.                        |
| F240  | 8,000   | Jendela kiri masuk lebih luas.                           |
| F260  | 8,667   | Sofa depan dan bidang fireplace berubah hubungan posisi. |
| F280  | 9,333   | Ruang keluarga hampir seluruhnya terungkap.              |
| F287  | 9,567   | Gerakan melambat sebelum cut.                            |

**Observations**

- **Depth:** fireplace dan meja mengecil, sementara cakupan ruang bertambah. Estimasi skala OUT sekitar 1,7×.
- **Translation:** meja dekat bergeser relatif ke kiri terhadap fireplace setelah memperhitungkan perubahan skala. Perubahan sudut meja mendukung Orbit Right.
- **Rotation:** latar menyapu ke kanan dan jendela kiri terungkap, menunjukkan Pan Left yang berjalan bersamaan.
- **Tempo:** pullback berlangsung cukup aktif di pertengahan dan mereda menjelang akhir.

**Pendalaman:** frame native F184–F194 untuk menentukan Production Start. Pembanding F200–F287 digunakan untuk menguji Orbit Right + Pan Left terhadap kemungkinan Dolly-Out + Pan saja.

Frame pembanding Shot 02

### **Shot 03 — Kitchen & Dining**

Durasi 3,500 detik · Pendekatan dapur dengan sapuan kanan pada fase lanjutan

| Fase | Interval perkiraan | Notasi                                 |
| ---- | ------------------ | -------------------------------------- |
| 1    | 9,600–10,800 s     | Straight Dolly-In (\~1.2×)             |
| 2    | 10,800–13,067 s    | Dolly-In (\~1.4×) + Moderate Pan Right |

**Frame pembanding:**

| Frame | PTS (s) | Pengamatan                                       |
| ----- | ------- | ------------------------------------------------ |
| F288  | 9,600   | Meja makan di kiri, wastafel relatif di tengah.  |
| F300  | 10,000  | Dapur membesar, arah pandang relatif stabil.     |
| F312  | 10,400  | Pendekatan berlanjut dengan meja masih terlihat. |
| F324  | 10,800  | Kandidat awal perubahan arah pandang.            |
| F336  | 11,200  | Jendela mulai bergeser ke kiri.                  |
| F348  | 11,600  | Meja makan semakin keluar dari bingkai kiri.     |
| F360  | 12,000  | Countertop kanan lebih dominan.                  |
| F384  | 12,800  | Kompor dan konfigurasi dapur kanan terungkap.    |
| F392  | 13,067  | Framing dekat pada wastafel dan countertop.      |

**Observations**

- **Depth:** wastafel, jendela dan kabinet membesar secara berkelanjutan pada kedua fase.
- **Translation:** kamera bergerak maju melalui jalur di antara meja makan dan kabinet.
- **Rotation:** arah pandang relatif stabil di awal; kemudian sapuan menuju sisi kanan menjadi jelas. Tidak cukup bukti lintasan melengkung untuk menambahkan Orbit.
- **Tempo:** pendekatan awal terkendali, kemudian framing berubah lebih cepat ketika Pan Right berlangsung.

**Pendalaman:** F312–F360 dengan interval pembanding 0,2 detik untuk menentukan onset Pan Right. Pan tidak ditulis sejak awal karena bukti sapuan kanan baru menjadi konsisten setelah fase pendekatan awal.

Frame pembanding Shot 03

### **Shot 04 — Bedroom**

Durasi 3,467 detik · Mundur diagonal untuk mengungkap kamar

| Fase | Interval        | Notasi                                                     |
| ---- | --------------- | ---------------------------------------------------------- |
| 1    | 13,100–16,533 s | Diagonal Dolly-Out (\~1.7×) + Moderate Pan Left (Ease-Out) |

**Frame pembanding:**

| Frame | PTS (s) | Pengamatan                                            |
| ----- | ------- | ----------------------------------------------------- |
| F393  | 13,100  | Kasur mendominasi foreground, jendela kanan terlihat. |
| F405  | 13,500  | Bantal dan headboard mulai lebih terbuka.             |
| F417  | 13,900  | Jendela di belakang headboard mulai terlihat.         |
| F429  | 14,300  | Sudut pandang terhadap kasur berubah.                 |
| F441  | 14,700  | Bagian ujung kasur semakin terlihat.                  |
| F453  | 15,100  | Cakupan lantai bertambah.                             |
| F465  | 15,500  | Lampu plafon masuk ke bingkai.                        |
| F477  | 15,900  | Hampir seluruh kasur terlihat.                        |
| F496  | 16,533  | Framing wide kamar dengan gerak yang mereda.          |

**Observations**

- **Depth:** bantal, bingkai lukisan dan kasur mengecil. Estimasi OUT sekitar 1,7×.
- **Translation:** kamera mundur dengan komponen lateral; hubungan kasur dengan jendela dan dinding berubah.
- **Rotation:** bidang belakang menyapu ke kanan, mendukung Pan Left.
- **Tempo:** pullback cukup aktif pada pertengahan, lalu mereda sebelum cut.

**Pendalaman:** pembanding tambahan setiap 0,4 detik untuk membedakan Diagonal Dolly-Out dari Dolly-Out + Orbit. Perubahan perspektif terlihat, tetapi kelengkungan lintasan tidak cukup tegas untuk menetapkan Orbit sebagai komponen tersendiri.

Frame pembanding Shot 04

### **Shot 05 — Bathroom**

Durasi 3,467 detik · Pendekatan dari pintu menuju jendela

| Fase | Interval        | Notasi                               |
| ---- | --------------- | ------------------------------------ |
| 1    | 16,567–20,000 s | Dolly-In (\~2.1×) + Subtle Pan Right |

**Frame pembanding:**

| Frame | PTS (s) | Pengamatan                                             |
| ----- | ------- | ------------------------------------------------------ |
| F497  | 16,567  | Shower, toilet, vanity dan jendela terlihat.           |
| F509  | 16,967  | Kamera mulai mendekati toilet.                         |
| F521  | 17,367  | Jangkar dekat membesar.                                |
| F533  | 17,767  | Jendela bergeser sedikit ke kiri.                      |
| F545  | 18,167  | Shower mulai keluar dari bingkai.                      |
| F557  | 18,567  | Jendela semakin dominan.                               |
| F569  | 18,967  | Vanity semakin terpotong.                              |
| F581  | 19,367  | Framing terkonsentrasi pada jendela dan tangki toilet. |
| F600  | 20,000  | Close framing jendela, tanaman dan keranjang.          |

**Observations**

- **Depth:** lebar jendela meningkat sekitar 2,1×; toilet dan vanity memperlihatkan perubahan skala serta oklusi yang mendukung Dolly-In.
- **Translation:** kamera maju dari pintu menuju area toilet dan jendela.
- **Rotation:** terdapat sapuan horizontal ringan ke kanan, terutama pada bagian awal hingga pertengahan.
- **Vertical movement:** framing akhir lebih terkonsentrasi pada bagian atas toilet dan jendela. Namun, bukti belum cukup untuk memisahkan Tilt Up dari perubahan perspektif dan tinggi lintasan.
- **Tempo:** moderate dengan pembesaran gambar yang semakin terasa ketika mendekati jendela.

**Pendalaman:** F545–F587 dengan interval 0,2 detik untuk menguji apakah perubahan framing vertikal merupakan Tilt Up yang disengaja. Tidak ditambahkan sebagai komponen terkonfirmasi karena tafsirnya masih ambigu.

Frame pembanding Shot 05

## **5. Camera Start & Production Start**

| Shot | Frame awal sumber | Production Start   | Framing awal produksi                                                                                         |
| ---- | ----------------- | ------------------ | ------------------------------------------------------------------------------------------------------------- |
| 01   | F0 — 0,000 s      | F0                 | Wide exterior, fasad hampir frontal, teras kanan, halaman dan pepohonan mengapit rumah.                       |
| 02   | F184 — 6,133 s    | **F192 — 6,400 s** | Medium-wide interior, fireplace sebagai fokus utama, coffee table di foreground, rak dan kursi di kedua sisi. |
| 03   | F288 — 9,600 s    | F288               | Wide interior dari akses dapur, meja makan di kiri dan wastafel di depan.                                     |
| 04   | F393 — 13,100 s   | F393               | Medium-close interior, kasur dominan di foreground, headboard di kiri dan jendela di kanan.                   |
| 05   | F497 — 16,567 s   | F497               | Wide interior dari ambang pintu, shower kiri, toilet tengah dan vanity kanan.                                 |

### **Production Start Shot 02**

Frame layak produksi

F192 · PTS 6,400 s

Native frame index: 192 · PTS native: 98304 · Time base: 1/15360

Production Start Shot 02 — F192

Posisi kamera menghadap fireplace dengan sudut sedikit menyamping. Coffee table memenuhi foreground bawah, fireplace menjadi jangkar utama di tengah, sedangkan rak built-in membingkai komposisi.

F192 dipilih sebagai frame pertama yang secara visual sudah cukup jernih untuk produksi. Pemilihan ini tidak mengubah batas awal shot sumber pada F184.

Lihat perbandingan native transisi F174–F194

## **6. Verifikasi akhir audit**

Cut dan batas native diperiksa

126 frame baseline dan batas shot diperiksa

5 frame midpoint tambahan diperiksa

Baseline ditandai viewed melalui runtime

Depth, translation dan rotation dibandingkan

Pan, Orbit, Truck dan Zoom dipertimbangkan

Production Start pada shot bertransisi ditentukan

**Baseline visual yang diperiksa:**

**Shot 01**

38 frame baseline + 1 midpoint

Lihat

**Shot 02**

22 frame baseline + 1 midpoint

Lihat

**Shot 03**

22 frame baseline + 1 midpoint

Lihat

**Shot 04**

22 frame baseline + 1 midpoint

Lihat

**Shot 05**

22 frame baseline + 1 midpoint

Lihat

### **Camera Pattern keseluruhan**

SHOT 01

**Exterior & Porch**

Orbit menuju Dolly-In

ORBIT → IN

SHOT 02

**Living Room**

Dolly-Out + Orbit + Pan

OUT

SHOT 03

**Kitchen & Dining**

Dolly-In → Dolly-In + Pan

IN

SHOT 04

**Bedroom**

Diagonal Dolly-Out + Pan

OUT

SHOT 05

**Bathroom**

Dolly-In + Subtle Pan

IN

**Pola kedalaman dominan:** IN → OUT → IN → OUT → IN.

### **Catatan keterbatasan**

- Batas fase gerakan gradual merupakan estimasi visual, berbeda dengan indeks hard cut yang terkonfirmasi.
- Skala merupakan estimasi dari jangkar gambar, bukan hasil kalibrasi kamera 3D. Sudut rotasi dalam derajat tidak ditetapkan karena belum cukup bukti untuk memberikan angka yang andal.
- Orbit pada Shot 01 dan 02 merupakan interpretasi berdasarkan perubahan perspektif dan paralaks. Bentuk lintasan fisik kamera tidak dapat dipastikan sepenuhnya dari MP4.
- Semua shot dinilai bertempo `moderate`, tetapi profil laju internalnya berbeda.
- Audit ini khusus bagian kamera sesuai permintaan, bukan audit desain lengkap atau paket ZIP tervalidasi HOMEKU.

Untuk pengembangan referensi produksi HOMEKU, pertahankan urutan fase masing-masing shot, terutama Shot 01 dan Shot 03. Menyederhanakannya menjadi satu gerakan simultan sepanjang shot akan menghilangkan karakter peralihan kamera yang terlihat pada sumber.