# Template baku analysis.md — V2

Acuan: [contoh normal](contoh-analysis-shot-normal.md), [contoh multi area](contoh-analysis-shot-multi-area.md), dan [plan V2](improvement-v2-plan.md).

Status: fondasi renderer V2 tersedia dan menghasilkan MD dari audit.json. Renderer 2.1.1 memakai salinan template beku yang berisi struktur ini; workflow chat serta audit ulang pilot tetap Tahap 2.

**Petunjuk pengisian**

- Laporan dimulai pada judul ID di bawah. Pengantar ini dan komentar petunjuk tidak masuk laporan final; ganti semua penanda {{...}}.
- Pertahankan lima bagian utama serta kelompok A/B/C. Ulangi kartu sesuai jumlah shot, bernomor 01 dan seterusnya, dipisahkan garis horizontal.
- Satu pengambilan berkelanjutan tetap satu shot meskipun melewati banyak area. Area terlihat dan rute kamera dicatat berbeda; jangan membuat cut yang tidak ada.
- Desain berupa paragraf konkret tentang bentuk, susunan, posisi dan hubungan objek. Panjang mengikuti detail yang terlihat, tanpa kuota objek atau batas kata yang menghilangkan informasi penting. Jangan mengarang detail.
- Untuk multi area, setiap kategori desain memuat paragraf berpenanda **Nama area.** mengikuti urutan kemunculan, tetap dalam satu kartu shot.
- Nama gaya utama, pengaruh gaya dan gaya interior memakai istilah bahasa Inggris; penjelasan tetap bahasa Indonesia. identity.style_names_language wajib en pada renderer 2.1.1. Generator tidak menerjemahkan atau menebak nama gaya.
- Gaya utama wajib bernama jelas; pengaruh gaya mengikuti bukti. Luas lantai wajib rentang estimasi total lantai rumah, ditampilkan hanya sebagai **angka–angka m²** tanpa catatan kepastian atau dasar perkiraan. Rincian estimasi tetap dalam JSON.
- Bahasa sederhana menjelaskan semua arah, urutan/kebersamaan gerak, target dan perubahan penting secara singkat. Bedakan perpindahan kamera dari perubahan arah pandang.
- Notasi teknis berbahasa Inggris: + untuk bersamaan, → untuk urutan, ~× untuk perubahan skala terhadap jangkar, bukan kelipatan kecepatan. Tempo terpisah; arah, waktu dan ritme mengikuti sumber.
- Timeline gerakan wajib untuk multi area atau beberapa fase. Fase mengikuti perubahan komponen kamera; pergantian area atau tempo saja tidak memaksa fase baru. Waktu mengacu ke awal video, berurutan sesuai shot. Semua tampilan kamera harus sejalan.
- Media final hanya satu kolase per shot dan satu storyboard. Shot satu area tepat 3 panel awal/tengah/akhir dalam 3 kolom. Multi area memakai panel dinamis: awal/akhir ditambah area, penghubung/reveal dan perubahan penting; pilih jumlah paling sedikit yang tetap lengkap, tanpa wajib 5 atau panel berulang. Panel kronologis; boleh beberapa baris jika terlalu panjang.
- Storyboard overview seluruh area penting dalam satu baris. Multi area boleh beberapa panel dengan nomor shot sama. Overview adalah pilihan frame asli, biasanya awal IN/akhir OUT, bukan JPEG terpisah. Frame kerja hanya sementara.
- Judul kolase/storyboard serta nama area tetap tebal tetapi 15% lebih kecil daripada 2.1.0. Semua waktu kolase (rentang/durasi serta Start/Middle/End atau momen multi area) ditempatkan dalam blok di samping judul, font regular sekitar 75% ukuran judul; blok membungkus di sisi kanan jika panjang. Di bawah foto hanya label Start/Middle/End atau nama momen, tanpa timestamp. Caption rata kiri dan sejajar; waktu dua desimal seperti 2.37s. Header storyboard: ID — Primary style — 18.40s — 5 shot; setiap panel memakai nomor shot/nama area tebal lalu Overview · 2.37s.
- Kolase berlabel nomor shot/area/waktu/durasi; tiap panel berlabel peran atau kejadian serta timestamp. Tulisan di luar foto, rasio/detail sumber terjaga; metadata panel tetap dapat ditelusuri.
- Hapus bagian opsional yang tidak berlaku. Jangan menyisakan penanda kosong. Batas pengamatan penting dijelaskan singkat; hash, log frame dan tabel pembuktian teknis tidak tampil pada laporan manusia.

---

# {{ID}} — {{NAMA_DESAIN}}

## 1. Identitas desain

- **Nama desain rumah:** {{NAMA_DESAIN_DESKRIPTIF}}.
- **Gaya utama:** {{NAMA_GAYA_UTAMA}}.
- **Pengaruh gaya:** {{GAYA_PENDUKUNG_DAN_ALASAN_SINGKAT}}.
- **Gaya interior:** {{NAMA_DAN_KARAKTER_INTERIOR}}.
- **Ciri pengenal:** {{DUA_ATAU_TIGA_CIRI_PEMBEDA}}.
- **Palet utama:** {{WARNA_DAN_MATERIAL_TAMPAK}}.
- **Suasana dan lingkungan:** {{SUASANA_CAHAYA_DAN_LINGKUNGAN}}.

## 2. Ukuran dan proporsi bangunan

| Aspek | Estimasi visual |
| --- | --- |
| Ukuran rumah | {{TINY_SMALL_MEDIUM_ATAU_LARGE}} |
| Bentuk bangunan | {{BENTUK_DAN_SUSUNAN_MASSA}} |
| Skala vertikal | {{TINGKAT_TERLIHAT_DAN_BENTUK_BAGIAN_ATAS}} |
| Tapak bangunan | {{KESAN_BENTUK_DAN_CAKUPAN_TAPAK}} |
| Proporsi utama | {{HUBUNGAN_LEBAR_TINGGI_PANJANG}} |
| Perkiraan luas lantai | **{{LUAS_MIN}}–{{LUAS_MAX}} m²** |

## 3. Struktur dan timeline video

{{DURASI_TOTAL_JUMLAH_SHOT_DAN_CUT_ATAU_KONTINUITAS}}

| Shot | Waktu (detik) | Durasi | Area/Scene | Gerakan singkat | Ritme |
| --- | --- | --- | --- | --- | --- |
| {{NN}} | {{AWAL}}–{{AKHIR}} | {{DURASI}} detik | {{AREA_ATAU_URUTAN_AREA}} | {{GERAK_BAHASA_MANUSIA}} | {{TEMPO_DAN_PERUBAHAN}} |

<!-- Ulangi satu baris per shot, bukan per area. -->

## 4. Storyboard

![Storyboard overview seluruh area](media/storyboard.jpg)

<!-- Satu baris overview seluruh area penting; tiap panel berlabel shot, area dan waktu. Beberapa area satu shot tetap memakai nomor shot sama. -->

## 5. Detail shot

### Shot {{NN}} — {{AREA_ATAU_URUTAN_AREA}} · {{DURASI}} detik

<!-- Jenis shot berikut hanya untuk multi area. -->
**Jenis shot:** berkelanjutan, multi area, tanpa cut.

![Kolase perjalanan Shot {{NN}}](media/shot-{{NN}}.jpg)

**Urutan panel:** {{PERAN_AREA_ATAU_KEJADIAN_DAN_WAKTU_SETIAP_PANEL}}.

<!-- Normal: awal → tengah → akhir. Multi area: panel dinamis sesuai momen penting dan kronologi, bukan interval waktu seragam. Rujuk panel awal bila overview storyboard berasal dari akhir OUT; tidak menautkan JPEG frame terpisah. -->

#### A. Desain area

**Arsitektur**

{{PARAGRAF_BENTUK_SUSUNAN_DINDING_PLAFON_LANTAI_BUKAAN_KABINET_MATERIAL_DAN_POSISI_LAMPU}}

**Furnitur dan properti**

{{PARAGRAF_BENTUK_POSISI_HUBUNGAN_FURNITUR_PERALATAN_PENYIMPANAN_DEKORASI_DAN_TANAMAN}}

**Lingkungan**

{{PARAGRAF_PEMANDANGAN_BUKAAN_TAMAN_VEGETASI_BANGUNAN_SEKITAR_CUACA_DAN_HUBUNGAN_LUAR_RUMAH}}

<!-- Multi area: gunakan beberapa paragraf berpenanda nama area dalam setiap kategori, tetap satu shot. -->

#### B. Komposisi dan cahaya

| Aspek | Penjelasan |
| --- | --- |
| Area yang terlihat | {{AREA_DAN_YANG_TERLIHAT_BERSAMAAN}} |
| Rute kamera | {{LOKASI_AWAL_JALUR_DAN_AKHIR}} |
| Fokus utama | {{SUBJEK_DAN_PERALIHAN_FOKUS}} |
| Posisi kamera awal | {{LOKASI_RELATIF_ARAH_PANDANG_DAN_SUDUT}} |
| Framing awal → akhir | {{CAKUPAN_AWAL_PERUBAHAN_PENTING_DAN_AKHIR}} |
| Pencahayaan | {{SUMBER_ARAH_KARAKTER_DAN_PERUBAHAN_CAHAYA}} |

<!-- Area yang terlihat dan Rute kamera wajib untuk multi area; pada normal boleh dihapus bila mengulang judul/posisi. -->

**Hubungan antararea**

| Aspek | Penjelasan |
| --- | --- |
| Penghubung area | {{PINTU_KORIDOR_BUKAAN_ATAU_OPEN_PLAN}} |
| Peralihan yang terlihat | {{WAKTU_AREA_MULAI_TERLIHAT_DAN_KAMERA_MEMASUKINYA}} |
| Kesinambungan ruang | {{ELEMEN_PENJAGA_ORIENTASI_SEPANJANG_PERJALANAN}} |

<!-- Hubungan antararea hanya untuk multi area. Waktu area terlihat berbeda dari waktu kamera masuk; jangan mengarang waktu yang tidak didukung. -->

#### C. Gerakan kamera

**Bahasa sederhana**

{{PARAGRAF_SINGKAT_LENGKAP_LINTASAN_ARAH_PANDANG_TARGET_URUTAN_GERAK_BERSAMAAN_DAN_PERUBAHAN_PENTING}}

**Ritme:** {{TEMPO_AWAL_PERUBAHAN_PENTING_DAN_AKHIR}}.

**DNA perjalanan:** {{POLA_PERJALANAN_PERALIHAN_FOKUS_REVEAL_DAN_RITME}}.

<!-- DNA perjalanan untuk multi area; pada normal hanya bila menambah penjelasan penting. -->

**Timeline gerakan**

Semua waktu berikut dihitung dari awal video. Pergantian baris mengikuti perubahan gerakan kamera; pergantian area tidak otomatis membuat fase atau shot baru.

| Waktu (detik) | Area dan fokus | Gerakan Kamera | Ritme |
| --- | --- | --- | --- |
| {{AWAL_FASE}}–{{AKHIR_FASE}} | {{AREA_PERALIHAN_DAN_TARGET}} | {{SEMUA_KOMPONEN_SIMULTAN_DALAM_NOTASI_TEKNIS}} | {{TEMPO_DAN_PERUBAHAN}} |

<!-- Ulangi baris sesuai fase aktual. Hapus bagian Timeline gerakan untuk shot normal satu fase. -->

**Notasi teknis**

```text
{{NOTASI_TEKNIS_LENGKAP_SESUAI_URUTAN_FASE}}
```

<!-- Untuk shot berikutnya, tambahkan garis horizontal lalu ulangi kartu mulai heading Shot. -->
