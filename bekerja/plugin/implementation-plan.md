# Rencana implementasi home-productions

Versi rencana: 0.5

Tanggal: 18 November 2026

Status: tahap 1 selesai berdasarkan probe workspace dan hasil uji manual pengguna di ChatGPT web. Tahap 2–7 dan pemasangan plugin belum dimulai.

Acuan perilaku: [alur penggunaan](production-workflow.md). Nama teknis plugin adalah home-productions; identitas ini dipertahankan pada folder paket, manifest dan rilis.

## 1. Hasil yang akan dibangun

Plugin mendampingi pengguna dari brief, pemilihan referensi dan konsep rumah, desain serta daftar continuous shot, pembuatan kolase frame awal–akhir, pemotongan gambar, hingga paket prompt Omni Flash.

Plugin mengikuti DNA desain dan video referensi: tata ruang, bentuk, material, lighting, lingkungan, komposisi, pengungkapan ruang, gerak dan penyajian. Pilihan baru dibedakan dari klaim tentang referensi.

Keluaran proyek meliputi ringkasan desain, daftar shot dan total durasi, gambar awal–akhir individu siap unduh, prompt per shot, petunjuk penggunaan aset dan catatan versi yang dapat dibawa ke sesi berikutnya.

Cakupan awal berakhir pada paket produksi dan bantuan revisi hasil. Generate video di Omni Flash, perangkaian klip dan publikasi Facebook dijalankan pengguna. Tidak ada integrasi berbayar, publikasi otomatis atau database proyek yang ditambahkan sebagai syarat awal.

## 2. Arsitektur pilihan

### Paket berbasis skill

Mulai dengan satu plugin berbasis skill, memakai alat yang tersedia pada lingkungan ChatGPT sasaran. Ini sesuai kesepakatan bahwa workflow berada di skill/plugin dan repo menyediakan pengetahuan.

Satu skill utama, produce-home-tour, mengatur perjalanan proyek. Detail dimuat sesuai tahap dari references/, template berada di assets/, dan pemrosesan deterministik berada di scripts/ pada direktori skill. references/ di dalam skill berisi panduan produksi; references/ di root repo tetap berisi analisis video sumber. Tahap internal bukan kumpulan skill yang harus dipanggil pengguna satu per satu.

Paket menggunakan root plugin.json dalam format Agent Plugins 1.0. Tidak membuat server, UI, hooks atau konfigurasi MCP kosong pada versi awal. Skill dan sumber daya terpaket tetap berada di dalam root paket. Pilihan ini mengikuti jalur skills-only pada Plugin Creator.

### Kemampuan lingkungan yang harus tersedia

| Kemampuan | Peran | Jika belum tersedia |
| --- | --- | --- |
| Membaca web atau konektor GitHub | Membuka sumber yang relevan dan mempertahankan provenance | Tandai akses belum tersedia; jangan mengisi sumber dari dugaan |
| Generate/edit gambar dan memakai gambar acuan | Membuat kolase berdasarkan desain dan aset yang disetujui | Paket konsep dapat disiapkan, tetapi produksi visual belum selesai |
| Melihat gambar hasil | Memeriksa konsistensi dan batas panel | Tandai review visual belum dilakukan |
| Menjalankan pemrosesan gambar/file | Memotong kolase secara deterministik dan memvalidasi hasil | Kemampuan penuh belum siap; jangan menyerahkan kolase sebagai pengganti file individu |
| Menghasilkan file unduhan yang dapat dibuka pengguna | Menyerahkan kedua frame setiap shot | Jangan melaporkan berkas siap unduh sebelum tautannya bekerja |
| Membaca media hasil, termasuk audio bila tersedia | Membantu evaluasi hasil generate | Nyatakan cakupan pemeriksaan yang benar-benar dilakukan |

Skill tidak otomatis memberikan alat tersebut. Tahap pertama harus membuktikan kemampuan pada lingkungan pengguna yang sebenarnya, terutama ChatGPT web, bukan menyimpulkan dari keberhasilan di workspace pengembangan ini.

Web dan GitHub merupakan dua jalur alternatif menuju pustaka yang sama. Konektor GitHub tidak menjadi dependensi wajib bila web sudah cukup. Deklarasi dependensi hanya memakai ID alat/app atau endpoint yang sudah diverifikasi.

Jika alat bawaan tidak mendukung pemotongan/unduhan, investigasi kemampuan yang tersedia terlebih dahulu. Catat kebutuhan integrasi tambahan sebagai keputusan arsitektur. Jika akhirnya memerlukan server baru, evaluasi jalur cloud/Sites MCP sesuai Plugin Creator sebelum membangunnya; jangan menyisipkan server atau melemahkan keluaran wajib secara diam-diam.

## 3. Struktur folder target

Struktur berikut adalah target implementasi; setiap komponen dibuat ketika tahapnya dikerjakan.

~~~text
bekerja/plugin/
├── README.md
├── production-workflow.md
├── implementation-plan.md
├── .gitignore
├── home-productions/                 # hanya berkas yang akan dipasang
│   ├── plugin.json
│   ├── assets/
│   │   └── icon.png
│   └── skills/
│       └── produce-home-tour/
│           ├── SKILL.md
│           ├── agents/
│           │   └── openai.yaml        # bila metadata/dependensi dibutuhkan
│           ├── references/
│           │   ├── production-rules.yaml
│           │   ├── repo-access.md
│           │   ├── image-workflow.md
│           │   └── omni-flash.md
│           ├── assets/
│           │   ├── project-template.json
│           │   └── prompt-template.md
│           └── scripts/
│               ├── validate_project.py
│               └── split_frames.py
├── tooling/
│   ├── probe_stage1.py              # probe workspace tahap 1, sudah dibuat
│   └── package_plugin.py
├── tests/
│   ├── test_project_rules.py
│   ├── test_split_frames.py
│   └── test_package.py
├── dist/                             # generated, ignored
└── runs/                             # local project assets, ignored
~~~

Hanya home-productions/ yang masuk arsip plugin. Dokumen pengembangan, pengujian, gambar percobaan dan paket ZIP berada di luarnya. ZIP dibuat ke dist/, bukan ke dalam folder paket.

Tidak menyalin pustaka knowledge/, references/ atau video/ ke paket. Akses sumber saat plugin digunakan mengarah ke URL repository; tautan relatif di dokumen perencanaan hanya untuk pembaca repo ini.

## 4. Kontrak proyek dan sumber aturan

### Aturan produksi

Perilaku disepakati pada production-workflow.md. Saat implementasi, production-rules.yaml menjadi representasi aturan yang dipakai skill dan validator. Perubahan perilaku memperbarui keduanya dalam perubahan yang sama.

Aturan yang harus tercakup:

- Satu shot tanpa cut → satu kolase dua panel → dua file frame → satu prompt → satu klip.
- Hanya exterior, exterior-to-living dan living-to-kitchen yang berdurasi 6 detik. Shot area lainnya 4 detik, termasuk area terpadu seperti bathroom–laundry. Banyaknya fungsi dalam gambar tidak otomatis menentukan durasi 6 detik.
- Area yang sudah tercakup tidak diberi shot pengungkapan ulang. Living-to-kitchen mencakup living dan kitchen; shot berikutnya menuju area baru.
- Exterior-to-living mencakup exterior dan living. Jangan otomatis menumpuknya dengan living-to-kitchen yang mengulang living.
- Jenis, jumlah dan cakupan area harus mempunyai acuan pada referensi yang dipilih. Laundry, wardrobe/closet, loft atau fungsi gabungan digunakan sesuai contoh sumber; jangan menambah variasi ruang secara bebas.
- Bedroom yang ditampilkan maksimal satu. Jangan meloloskan pengulangan bedroom dengan memberi nama kamar berbeda.
- Semua prompt, klip dan video akhir: tanpa musik, cukup ambient halus. Tanpa narasi/dialog atau efek dramatis tambahan.
- Total durasi adalah penjumlahan durasi shot. Jangan mempercepat atau memangkas otomatis untuk memaksakan total referensi.
- Confidence membatasi klaim sumber, bukan pilihan kreatif baru. Tidak ada human_verified.
- Cut dan kesinambungan dibaca dari isi anotasi; ID segmen tematik tidak otomatis menjadi shot produksi tersendiri. Setiap shot produksi dan promptnya wajib kontinu tanpa cut.
- Arahan terbaru pengguna dan aturan produksi proyek menjadi pegangan saat menerapkan DNA referensi. Perubahan arahan dicatat pada versi keputusan; pola sumber tidak diam-diam mengganti durasi, cakupan atau audio proyek.

### Catatan proyek yang dapat dipindahkan

Gunakan satu project.json per versi proyek, disertai ringkasan yang mudah dibaca. Untuk melanjutkan sesi, sertakan berkas aset asli yang masih diperlukan; nama file atau tautan lama saja belum membuktikan gambar tersedia. Kontraknya memuat:

| Bagian | Isi utama |
| --- | --- |
| Identitas | ID proyek, versi, tahap, keputusan yang disetujui |
| Brief dan referensi | Kebutuhan, URL/ref/commit sumber, jalur akses, ID referensi dan shot, apa yang benar-benar dibaca |
| Desain rumah | Geometri, hubungan ruang, elemen tetap, material, lingkungan dan lighting |
| Shot | ID, jenis, ID area/fungsi yang dicakup, durasi, framing awal–akhir, lintasan, gerak bersamaan/berurutan |
| Aset | Kolase, ukuran aktual, batas panel, dua frame hasil potong dan status pemeriksaannya |
| Prompt | Instruksi video, audio ambient, durasi dan pasangan file yang dipakai |
| Revisi | Perubahan, dampak pada shot lain, keputusan terbuka dan status review |

Cakupan mengikuti jenis/fungsi area dan struktur shot pada referensi terpilih. Bedroom yang ditampilkan maksimal satu; perubahan nama kamar tidak menjadi alasan untuk menambahkan bedroom lain. Area terpadu mencatat semua fungsi yang sudah dicakup, sementara benda yang muncul insidental sebagai background tidak otomatis memerlukan shot tersendiri. Catat referensi pendukung untuk setiap pilihan area dan penggabungannya.

Validasi mengikuti tahap proyek:

| Tahap data | Yang wajib diperiksa |
| --- | --- |
| Brief/konsep | Kebutuhan, sumber yang benar-benar diakses dan keputusan; gambar belum diwajibkan |
| Rancangan shot | Desain rumah, cakupan tanpa pengulangan, jenis shot, durasi dan total |
| Produksi visual | Kolase serta status review aktual; percobaan yang belum selesai belum boleh diberi status final |
| Visual final/paket prompt | Dua frame per shot benar-benar tersedia, lolos pemeriksaan dimensi, cocok dengan versi keputusan dan dipasangkan ke prompt yang tepat |

Validator memeriksa struktur serta konsistensi catatan. Ia tidak mengklaim membuktikan geometri visual atau audio benar dari JSON. Temuan review visual dan audio hanya dicatat setelah media benar-benar diperiksa.

## 5. Tahapan implementasi

Status pelaksanaan: tahap 1 selesai. Bukti workspace, akses remote dan hasil uji manual pengguna di ChatGPT web dicatat di bawah; tahap 2–7 belum dimulai.

### Tahap 1 — Membuktikan kemampuan lingkungan sasaran

Pekerjaan:

- Tentukan aplikasi/versi Omni Flash yang digunakan dan kontrol pasangan awal–akhir yang tersedia.
- Periksa alat pembaca repo pada kedua jalur, tanpa menjadikan keduanya wajib digunakan bersamaan.
- Buktikan alur kecil: generate kolase dengan acuan → file hasil asli dapat diakses dan diperiksa → kolase dipotong → dua unduhan dapat dibuka. Preview gambar saja belum membuktikan file asli dapat diproses.
- Gunakan gambar sintetis untuk pemeriksaan pemotongan yang dapat diulang. Saat tahap implementasi ini dikerjakan, lakukan pilot visual kecil untuk memeriksa dukungan alat, rasio, resolusi dan aliran file. Pilot tersebut belum membuktikan konsistensi seluruh shot atau proyek.

Keluaran: catatan kemampuan aktual pada rencana ini, keputusan runtime dan jalur alat yang akan dipakai.

Kriteria selesai: jalur alat yang dipilih terbukti menyediakan kemampuan wajib. Jika masih memerlukan integrasi tambahan, catat tahap ini sebagai belum selesai beserta kebutuhan konkretnya; jangan menyatakan plugin siap penuh hanya karena kebutuhan tersebut sudah didokumentasikan.

#### Hasil pelaksanaan tahap 1 — 18 November 2026

Status: **selesai**, berdasarkan hasil probe workspace dan laporan uji manual pengguna di ChatGPT web pada 18 November 2026. Tidak ada paket plugin yang dibuat atau dipasang pada tahap ini.

| Pemeriksaan | Hasil aktual |
| --- | --- |
| Konektor GitHub | Berhasil membaca pengetahuan inti dan anotasi edh058 pada commit terpublikasi yang sama; hash teks hasilnya cocok dengan file lokal |
| Web | Halaman GitHub pengetahuan inti berhasil dibaca. URL raw pada pembaca utama mengalami cache miss; pembaca alternatif berhasil membaca inti dan bagian anotasi yang memuat shot pilot. Pembacaan seluruh byte anotasi melalui web tidak diklaim |
| Generate dengan acuan | Satu kolase exterior edh058 shot-01 berhasil dibuat memakai Imagegen bawaan dan dua gambar sumber awal–akhir |
| File asli | PNG hasil generator tersedia dan berhasil dibuka; dimensi aktual 1330 × 1182, berbeda dari ukuran 2160 × 1920 yang diminta dalam prompt |
| Pemotongan workspace | Dua PNG 657 × 1168, tepat 9:16; piksel crop dipertahankan, tanpa resize atau generate ulang |
| Pemeriksaan sintetis | Lima pemeriksaan lulus: urutan/piksel crop, penolakan lebar ganjil, penolakan rasio salah, inset 9:16 eksplisit dan perlindungan berkas lama |
| Review visual pilot | Kolase dan kedua potongan benar-benar dilihat. Ciri pintu, gable, lantern dan taman dibandingkan secara terbatas; konsistensi seluruh geometri dan gerak video belum diuji |
| Percobaan otomasi Chrome | Halaman terbuka; interaksi unggah dan tangkapan layar mengalami timeout. Percobaan otomatis ini tidak menyelesaikan uji; hasil manual pengguna dicatat terpisah di bawah |
| Uji manual ChatGPT web — laporan pengguna | Generate kolase berhasil; crop langsung tanpa unggah ulang berhasil; kedua frame berhasil diunduh, dibuka dan diverifikasi dengan Python. PNG valid, masing-masing 657 × 1168 piksel (9:16), tanpa resize atau generate ulang, tanpa kendala/error |
| Omni Flash | Dilewati atas arahan pengguna; dukungan frame awal–akhir dicatat sebagai konfirmasi pengguna, tidak diuji ulang |
| Video dan audio | Tidak dibuat atau diuji dalam pilot gambar ini |

Sumber remote yang benar-benar dibaca menggunakan commit 26c5e56cb0de66d5c1ab4f93a1285654180382a0:
[pengetahuan inti](https://github.com/milyarderpro/homeku/blob/26c5e56cb0de66d5c1ab4f93a1285654180382a0/knowledge/ai-knowledge.md) dan [anotasi edh058](https://github.com/milyarderpro/homeku/blob/26c5e56cb0de66d5c1ab4f93a1285654180382a0/references/edh058/analysis.yaml).
Commit lokal 4e53d11b220f09e6b5112cdb41b64bba2969e3ea semula dicoba, tetapi konektor mengembalikan 404 karena ref itu belum tersedia di remote. Pemeriksaan dialihkan secara eksplisit ke commit main yang terpublikasi; tidak menganggap dokumen lokal sudah diterbitkan.

Pemotongan pilot memakai inset kecil setelah batas dua panel dilihat: kiri (4, 7, 661, 1175), kanan (669, 7, 1326, 1175), dengan koordinat kanan/bawah eksklusif. Sekitar 97,63% piksel setiap panel dipertahankan. Ukuran hasil adalah resolusi pilot, belum merupakan janji resolusi produksi.

Alat pelaksanaan: [probe tahap 1](tooling/probe_stage1.py), Python 3.12.3 dan Pillow 10.2.0 di workspace ini. Probe mengasumsikan dua panel sama besar yang sudah diperiksa; ia tidak mendeteksi batas panel atau menilai desain secara otomatis dan belum menjadi script produksi tahap 4.

Aset, prompt, laporan crop dan ringkasan bukti lokal berada di runs/stage1-2026-11-18/ yang diabaikan Git. Berkas tersebut tidak tersedia sebagai isi repository remote dan tidak menambah referensi pustaka.

Keputusan: lanjutkan arsitektur plugin berbasis skill dengan kemampuan gambar dan pemrosesan file yang tersedia. Hasil uji manual pengguna melengkapi verifikasi ChatGPT web yang tertunda akibat timeout otomasi. Tidak ada kebutuhan server tambahan yang ditemukan pada tahap ini.

Asal bukti dibedakan: akses repo, generate pilot dan pemotongan workspace diamati dalam sesi pengembangan; keberhasilan alur ChatGPT web diterima dari laporan manual pengguna. Laporan manual tersebut tidak diubah menjadi klaim keberhasilan otomasi browser atau pengujian plugin yang sudah terpasang.

Tahap 1 menyelesaikan pemeriksaan kemampuan alat. Konsistensi seluruh shot, kualitas video/audio dan perilaku plugin setelah pemasangan tetap diperiksa pada tahap implementasi berikutnya sesuai cakupannya.

### Tahap 2 — Fondasi paket dan kontrak proyek

Pekerjaan:

- Buat home-productions/ dan manifest yang sesuai Plugin Creator.
- Buat satu sumber aturan produksi, template catatan proyek dan validator aturan.
- Tetapkan status tahap serta pengikatan aset/prompt pada versi keputusan yang sama.
- Pilih metadata publisher yang sebenarnya dan kategori listing yang didukung; tidak mengarang identitas publisher.

Keluaran: paket dasar, kontrak data, aturan dan validasi.

Kriteria selesai: konsep awal sah tanpa aset gambar; rancangan dengan durasi salah atau cakupan berulang ditolak; paket yang diklaim final dengan ID/versi aset tidak cocok atau pasangan frame tidak lengkap ditolak. Pesan menjelaskan masalah sesuai tahap data.

### Tahap 3 — Skill brief, referensi, konsep dan daftar shot

Pekerjaan:

- Tulis SKILL.md dengan trigger yang jelas untuk produksi home tour dan kelanjutan/revisi proyek.
- Tulis panduan akses repo secara selektif, provenance dan penanganan kegagalan baca.
- Susun brief, opsi konsep, keputusan rumah dan daftar shot menggunakan kontrak yang sama. Pastikan setiap jenis area dan pola penggabungan mempunyai acuan referensi; jangan menambah cakupan di luar pola tersebut.
- Muat detail tahap hanya ketika diperlukan. Pertanyaan pengguna dibatasi pada informasi yang memengaruhi hasil.
- Terapkan tiga titik keputusan: arah konsep; desain beserta daftar shot; paket visual final. Ikuti keleluasaan yang sudah diberikan pengguna.

Keluaran: konsep dan daftar shot yang dapat diteruskan ke produksi gambar.

Kriteria selesai: contoh exterior + living-to-kitchen + bedroom + bathroom menghasilkan empat shot, 20 detik, tanpa shot kitchen tambahan; exterior-to-living + kitchen + bedroom + bathroom menghasilkan 18 detik.

### Tahap 4 — Kolase, konsistensi dan pemotongan

Pekerjaan:

- Hubungkan instruksi generate gambar dengan spesifikasi rumah dan gambar yang sudah disetujui. Kedua panel adalah ujung lintasan dalam satu rumah; pada shot penghubung, area awal dan akhirnya dapat berbeda.
- Buat kolase dua panel: kiri awal, kanan akhir, tanpa teks/bingkai dekoratif; setiap frame vertikal ditargetkan 9:16.
- Periksa hasil aktual. Rasio kanvas dua panel idealnya 9:8; kemampuan keluaran alat perlu dicocokkan sebelum menjanjikan ukuran.
- Implementasikan split_frames.py untuk memotong batas panel yang sudah diperiksa, menjaga piksel dan memvalidasi kedua file.
- Periksa konsistensi visual terpisah dari validasi dimensi. Kembalikan ke revisi bila tata ruang, bukaan, furnitur, material atau cahaya menyimpang.
- Berikan unduhan individual; ZIP proyek opsional. Jangan mengunggah kolase utuh sebagai pengganti dua frame ke generator.

Keluaran: pasangan frame yang valid, penamaan shot-NN-start.png dan shot-NN-end.png, serta catatan review.

Kriteria selesai: pemotongan tidak menukar urutan, mencampur panel, menyisakan bingkai atau meregangkan proporsi; file hasil benar-benar dapat diunduh. Resolusi rendah ditandai, bukan diklaim bertambah detail setelah crop.

### Tahap 5 — Prompt Omni Flash dan paket proyek

Pekerjaan:

- Tulis panduan generator sesuai aplikasi yang dikonfirmasi; jangan menyalin parameter API ke UI yang tidak mendukungnya.
- Susun prompt per shot dari gambar final: gerak, framing, lintasan, durasi 6/4 detik, kontinuitas dan ambient tanpa musik.
- Periksa bahwa maju sambil pan dan maju lalu pan diterjemahkan berbeda.
- Buat ringkasan desain, shot list, total durasi, peta file–prompt, petunjuk penggunaan dan catatan versi.
- Dukung revisi hasil yang benar-benar dapat diakses. Perubahan elemen tetap memicu peninjauan shot yang terdampak.

Keluaran: paket produksi lengkap dan dapat dilanjutkan pada sesi berikutnya.

Kriteria selesai: setiap prompt memakai pasangan frame yang benar dan aturan audio eksplisit; ringkasan proyek cukup untuk melanjutkan tanpa mengandalkan ingatan sesi lama.

### Tahap 6 — Pemeriksaan perilaku dan penerimaan

Pemeriksaan kode difokuskan pada kontrak, pemotongan dan isi paket. Pemeriksaan visual memerlukan melihat gambar; pemeriksaan audio memerlukan mendengarkan hasil yang tersedia.

Skenario penerimaan minimum:

| Skenario | Hasil yang harus terjadi |
| --- | --- |
| Lima area terpisah | Exterior 6 + empat area 4 = 22 detik; lima kolase dan sepuluh frame |
| Living-to-kitchen gabungan | Kedua area selesai dalam satu shot 6 detik; kitchen tidak diulang |
| Exterior-to-living gabungan | Living tidak diulang; lanjut kitchen atau area baru |
| Bathroom–laundry terpadu | Satu shot 4 detik mencakup kedua fungsi; keduanya tidak diulang |
| Pengulangan bedroom | Ditolak; bedroom yang ditampilkan maksimal satu, termasuk ketika nama kamarnya diubah |
| Konsep tanpa gambar | Sah pada tahap konsep; pasangan gambar baru wajib untuk visual final dan paket prompt |
| Laundry atau wardrobe | Pilih sesuai contoh referensi; masing-masing 4 detik bila menjadi shot tersendiri, satu kali cakupan |
| Anotasi berupa segmen tematik kontinu | Periksa continuity/transition; jangan otomatis menambah cut |
| Akses sumber/gambar gagal | Nyatakan belum terbaca/terlihat; jangan mengarang review |
| Citra tidak konsisten atau panel keliru | Revisi sebelum menyerahkan pasangan final |
| Alat crop atau unduhan tidak tersedia | Laporkan kemampuan belum lengkap; jangan mengklaim selesai |
| Prompt atau hasil memiliki musik | Prompt diperbaiki; hasil audio ditinjau bila dapat didengar |
| Revisi jendela/material rumah | Tinjau aset dan prompt terkait; versi lama tidak tercampur |
| Sesi baru | Catatan dan aset asli digunakan untuk melanjutkan; aset yang belum tersedia diminta tanpa mengarang isinya |
| Permintaan analisis sumber saja | Hindari memulai produksi lengkap tanpa diminta |

Gunakan pilot kecil dan skenario penerimaan di atas untuk memeriksa alur. Bedakan hasil pemeriksaan kode, review visual, audio dan pengujian generator; keberhasilan salah satunya tidak menggantikan yang lain. Generate video, publikasi dan evaluasi performa Facebook tetap mengikuti cakupan yang disepakati.

Keluaran: hasil penerimaan ringkas pada rencana ini, masalah yang tersisa dan batas kemampuan.

Kriteria selesai: setiap keluaran wajib berhasil pada lingkungan sasaran; keterbatasan pemeriksaan dinyatakan sesuai bukti.

### Tahap 7 — Paket rilis dan pemasangan privat

Pekerjaan:

- Jalankan pemeriksaan paket dan buat ZIP hanya dari home-productions/, ke dist/.
- Inspeksi arsip akhir: manifest, skill, referensi, script dan aset yang benar; semua path internal valid.
- Gunakan Plugin Creator untuk menyimpan paket lengkap secara privat ketika pekerjaan dilanjutkan sampai pemasangan. Jangan membuat plugin placeholder untuk mengecek koneksi.
- Untuk pembaruan, identifikasi plugin yang sama dan gunakan update; simpan plugin ID, release ID, versi dan plugin_url setelah respons berhasil.
- Periksa komponen dan aktivasi setelah pemasangan. Pembuatan entri plugin saja belum membuktikan workflow berhasil.
- Catat informasi rilis singkat pada README ruang kerja ini. Pembuatan rencana saat ini tidak memasang, membagikan atau memublikasikan plugin.

Keluaran: paket versi awal 0.1.0, plugin privat terpasang bila termasuk cakupan implementasi, serta tautan dan identitas rilis yang terverifikasi.

Kriteria selesai: arsip dapat diperiksa, skill yang diharapkan dikenali, dan alur yang diminta berjalan pada lingkungan pengguna. Publikasi direktori publik merupakan pekerjaan terpisah.

## 6. Pemeriksaan format Plugin Creator

Acuan diperiksa pada 18 November 2026: skill create-plugin dari Plugin Creator beserta panduan plugin-packages dan zip-requirements, serta dokumentasi resmi OpenAI.

- Root plugin.json memakai schema https://agent-plugins.org/schemas/1.0.0/plugin.schema.json.
- Nama home-productions sesuai folder paket; versi paket menggunakan SemVer mulai 0.1.0.
- Skills berada langsung di `skills/<skill-name>/SKILL.md`, dengan frontmatter name dan description.
- Metadata OpenAI berada di extensions.com.openai. Listing direncanakan memakai kategori Creativity; subtitle maksimal 30 karakter.
- agents/openai.yaml hanya ditambahkan jika diperlukan dan mengikuti field yang didukung.
- mcp.json dan deklarasi app hanya dibuat untuk integrasi nyata dengan identitas/endpoint terverifikasi.
- Arsip memuat satu plugin, tanpa dokumen kerja, file proyek pengguna, cache, dependensi terinstal, symlink atau rahasia.

Aturan format diperiksa ulang saat mengemas. Tidak membuat compatibility manifest kedua kecuali lingkungan pemasangan benar-benar memerlukannya.

## 7. Pemeliharaan dan perluasan

Perbarui versi paket dan catatan rilis setelah perubahan. Pertahankan satu alur penggunaan dan satu rencana aktif; riwayat Git menyimpan versi terdahulu.

Penambahan referensi di pustaka tidak memerlukan menyalin semua analisis ke plugin. Plugin mengakses snapshot sumber yang tersedia dan mencatat versi yang digunakan per proyek.

Skill tambahan, UI, server, penyimpanan terkelola atau integrasi generator otomatis dipertimbangkan setelah kebutuhan nyata muncul. Buat keputusan arsitektur terlebih dahulu agar perubahan tidak mengubah diam-diam aturan produksi yang telah disepakati.

Berkas sementara ditempatkan di runs/ atau dist/ dan diabaikan Git. Berkas proyek untuk pengguna diserahkan melalui unduhan, tanpa otomatis dimasukkan ke pustaka pengetahuan.

## 8. Referensi teknis

- [Plugin Creator: paket plugin](https://developers.openai.com/plugins/build/plugins)
- [OpenAI: membangun skill](https://developers.openai.com/plugins/build/skills)
- [OpenAI: skill sebagai lapisan workflow](https://developers.openai.com/plugins/concepts/skills)
- [Alur penggunaan home-productions](production-workflow.md)

## 9. Status dan revisi

| Bagian | Status |
| --- | --- |
| Rencana implementasi dan struktur target | Selesai disusun |
| Tahap 1 — Kemampuan lingkungan | Selesai; probe workspace dan uji manual pengguna di ChatGPT web |
| Tahap 2 — Fondasi paket | Belum dimulai |
| Tahap 3 — Skill konsep dan shot | Belum dimulai |
| Tahap 4 — Kolase dan pemotongan | Belum dimulai |
| Tahap 5 — Prompt dan paket proyek | Belum dimulai |
| Tahap 6 — Penerimaan | Belum dimulai |
| Tahap 7 — Paket dan pemasangan | Belum dimulai |

- 0.5 — Mencatat keberhasilan generate, crop langsung dan dua unduhan PNG pada uji manual pengguna di ChatGPT web; menandai tahap 1 selesai tanpa mengubah status tahap 2–7.
- 0.4 — Menjalankan probe tahap 1, mencatat pembacaan repo dan hasil pilot gambar/crop; menandai verifikasi ChatGPT web belum lengkap dan pengujian Omni Flash dilewati sesuai arahan pengguna.
- 0.3 — Menghapus contoh perluasan beberapa bedroom dan skenario penerimaannya; membatasi cakupan pada pola referensi dengan maksimal satu bedroom yang ditampilkan.
- 0.2 — Memperjelas validasi per tahap, identitas area, durasi area terpadu, panel lintasan antararea, pembuktian kemampuan runtime dan kelanjutan proyek dengan berkas aset asli.
- 0.1 — Menyusun rencana pembangunan, struktur paket, kontrak proyek, jalur akses alternatif, pemeriksaan runtime dan kriteria penerimaan.
