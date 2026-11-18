# Rencana implementasi home-productions V2

Versi rencana: 2.1

Tanggal: 18 November 2026

Status: **tahap 1–6 selesai dan rilis privat 2.0.0 sudah diperbarui; tahap 7 menunggu uji manual pengguna**. Pemeriksaan teknis dan source rilis terverifikasi; kualitas/batch/gerak pada lingkungan ChatGPT dan Omni Flash tidak diklaim lulus dari tes kode.

Acuan perilaku: [alur penggunaan V2](production-workflow.md). [Peta folder dan identitas rilis](README.md). Ini satu rencana aktif pengganti rencana V1; riwayat implementasi lama tetap tersedia di Git.

## 1. Dasar dan sasaran

Temuan manual pengguna pada 18 November 2026:

| Temuan | Kedudukan bukti | Dampak pada V2 |
| --- | --- | --- |
| Kolase awal–akhir sering tidak konsisten, terutama plafon | Laporan pengujian pengguna | Ganti dengan gambar area individual dan spesifikasi plafon yang sama |
| Interpolasi first–last masih mengubah susunan meskipun diminta continuous shot | Laporan pengujian pengguna | Ganti metode utama menjadi Reference-to-Video (R2V) |
| R2V dengan satu gambar memberi hasil lebih baik dan konsisten | Percobaan pengguna; tidak digeneralisasi sebagai jaminan | Jadikan R2V dasar workflow dan uji dua referensi pada shot penghubung |

Sasaran: dari konsep rumah yang mengikuti keseluruhan DNA referensi, menghasilkan prompt/gambar individual per area, lalu prompt R2V sembilan bagian per shot beserta paket proyek yang dapat dilanjutkan.

Repository tetap pustaka pengetahuan. Semua pengembangan berada di bekerja/plugin/; knowledge/, references/ dan video/ root tidak diubah atau disalin ke paket. Analisis tersimpan digunakan secara selektif lewat URL web atau konektor GitHub, tanpa analisis ulang seluruh video.

Generate video Omni Flash, perangkaian klip dan publikasi Facebook tetap dilakukan pengguna. Tidak menambah server, API berbayar, database, UI khusus, skill kedua atau plugin duplikat.

## 2. Kontrak perilaku V2

Detail lengkap berada pada alur penggunaan; butir berikut menjadi dasar implementasi dan pemeriksaan.

| Aspek | Ketentuan |
| --- | --- |
| Mode gambar | Pengguna memilih prompt_to_image atau generate_image setelah rancangan disetujui; satu prompt untuk satu gambar area |
| Batch generate | Seluruh gambar individual dikerjakan sekaligus sesuai jumlah yang disetujui; tujuh berarti tujuh, tanpa kolase dan tanpa menunggu perintah per area. Satu per satu hanya jika diminta pengguna |
| Gambar | Pandangan luas/informatif, natural dan sesuai desain; bukan pasangan start/end wajib |
| Plafon dan struktur | Bentuk/tingkat plafon, sambungan, lampu, bukaan, furnitur tetap, material dan cahaya mengikuti keputusan rumah yang sama |
| Living-to-kitchen | Satu shot 6 detik, dua gambar individual: living dan kitchen; keduanya referensi R2V |
| Exterior-to-living | Satu shot 6 detik, dua gambar individual: exterior dan living; keduanya referensi R2V |
| Area lain | Mengikuti jenis/cakupan sumber dan rancangan; kebutuhan gambar fungsi terpadu dipetakan eksplisit, tidak otomatis menambah area fisik |
| Durasi | Exterior dan dua shot penghubung di atas 6 detik; shot area lain/fungsi terpadu 4 detik |
| Cakupan | Tidak mengulang pengungkapan area; maksimal satu bedroom/area tidur, termasuk sleeping loft |
| Kamera | Gerak gabungan harus terlihat; pan/orbit yang dipilih minimal 12 derajat, simultan/sekuensial jelas, jarak/sudut/ritme sesuai durasi |
| Video dan audio | Video 9:16, satu continuous shot tanpa cut/morphing; ambient natural halus tanpa musik, narasi, dialog atau efek dramatis |
| Persetujuan | Konsep, desain/shot dan paket gambar final; delegasi tetap berlaku, tanpa persetujuan per gambar yang dipaksakan |

Full area berarti komposisi yang menunjukkan area dan hubungan ruang secara wajar, bukan tuntutan melihat semua sisi terhalang. Rasio gambar referensi dipilih untuk cakupan dan masukan alat; tidak mewarisi kewajiban crop panel/rasio frame V1. Rasio video tetap 9:16. Dimensi, format dan kelayakan aktual tetap diperiksa.

Batch tujuh gambar dan eksekusi yang benar-benar bersamaan harus dibuktikan pada ChatGPT pengguna. Jangan menyamakan tujuh file yang terkumpul dari perintah satu per satu dengan permintaan tujuh sekaligus. Kegagalan alat pengembang tidak menjadi kesimpulan keterbatasan ChatGPT. Jangan diam-diam mengganti alur, mengurangi jumlah atau memindahkan produksi ke API.

## 3. Arsitektur dan kontrak proyek

Paket home-productions/ dan skill produce-home-tour dipertahankan. Versi paket **2.0.0**, schema proyek 2.0 dan aturan produksi 2.0.0 sudah diimplementasikan.

Gunakan satu project.json per revisi aktif. Rincian field dan tahap yang sudah tersedia dijelaskan pada [kontrak V2](home-productions/skills/produce-home-tour/references/project-contract.md).

| Bagian | Perubahan yang direncanakan |
| --- | --- |
| Identitas, brief, konsep | Pertahankan ID/revisi dan keputusan yang sudah ada |
| knowledge | Pertahankan URL/ref/commit, jalur akses, evidence dan pembedaan fakta/adaptasi |
| design | Spesifikasi rumah bersama, plafon, elemen tetap serta hubungan area; tidak mengarang denah sumber |
| image_mode | prompt_to_image atau generate_image; pilihan tersimpan agar sesi baru tidak mengulang pertanyaan |
| image_plan | Daftar gambar individual: ID, area tujuan, shot pemakai, prompt gambar, revisi dan status pemenuhan |
| assets | File referensi area, peran/cakupan, dimensi/format/hash aktual, revisi dan catatan review; role reference menggantikan start/end/collage |
| shots | Cakupan/durasi/source tetap; reference_image_ids menunjuk daftar gambar sesuai kebutuhan shot, bukan frames.start/end |
| camera | Jenis gerak, hubungan simultan/sekuensial, perkiraan jarak, sudut pan/orbit, alokasi waktu dan visible_motion_evidence |
| prompt video | Metode R2V, sembilan bagian, durasi/revisi dan ID gambar yang sama dengan shot |
| audio, approvals, revision_notes | Pertahankan aturan, asal keputusan dan revisi; tidak menciptakan persetujuan/review otomatis |

Pisahkan gambar yang direncanakan dari aset yang benar-benar tersedia. image_plan yang lengkap belum berarti file telah dibuat/dilihat. Dukungan gambar terhadap fungsi terpadu dijelaskan dalam rancangan; background tidak otomatis menjadi area/shot tambahan.

Tahap data yang diimplementasikan:

| Stage | Syarat dan batas penyerahan |
| --- | --- |
| brief / concept / shot_plan | Data perencanaan sesuai tahap; gambar belum wajib |
| image_prompt_package | Seluruh prompt gambar sesuai rancangan dan mode; sah tanpa file gambar, belum siap sebagai paket R2V final |
| image_draft | Gambar sedang dibuat/dikumpulkan atau masih perlu revisi; jumlah belum terpenuhi dicatat |
| image_final | Seluruh gambar yang diperlukan tersedia, sesuai keputusan, direview dan disetujui/didelegasikan |
| prompt_package | Gambar final serta prompt R2V sembilan bagian lengkap, terikat ke shot/durasi/revisi yang benar |

Kedua mode bertemu pada review gambar. Pada prompt_to_image, hasil dari generator pilihan pengguna harus benar-benar dapat dibuka sebelum review dan prompt video final. Jangan menambahkan persyaratan generate otomatis ke mode yang hanya meminta prompt.

Validator memeriksa struktur, jumlah/pemetaan, nilai sudut yang diminta, durasi, revisi, file dan hash. Validator tidak membuktikan gambar natural, plafon konsisten, batch berjalan serentak, sudut aktual video atau ketiadaan musik pada hasil. Hal-hal tersebut dinilai dari gambar/video/audio dan laporan pengguna.

## 4. Komponen yang diubah

Semua path pada tabel relatif terhadap bekerja/plugin/. Gunakan folder dan file yang ada; tambahkan file baru hanya jika langsung mendukung fungsi V2.

| Komponen | Pekerjaan |
| --- | --- |
| home-productions/plugin.json | Naikkan versi saat implementasi; selaraskan deskripsi R2V. Pertahankan identitas, scope/audience, publisher akun dan defaultPrompt yang masih berlaku |
| skills/produce-home-tour/SKILL.md | Rute dua mode gambar, batch, review, R2V serta kelanjutan/revisi dalam satu skill |
| references/production-rules.yaml | Aturan V2 dan versi, kebutuhan referensi, sudut gerak dan batas tahap |
| references/project-contract.md | Kontrak V2, persetujuan, aset area, pemetaan dan kompatibilitas |
| references/preproduction.md | Rumah/plafon yang sama, rancangan kamera sesuai durasi dan daftar gambar |
| references/image-workflow.md | Ganti isi kolase/crop menjadi prompt/gambar individual, batch dan review seluruh area |
| references/omni-flash.md | R2V satu/dua referensi, sembilan bagian dan revisi hasil |
| references/repo-access.md | Pertahankan jalur selektif/provenance; ubah hanya jika integrasi data membutuhkan |
| assets/project-template.json dan project.schema.json | Kontrak proyek V2 tanpa kewajiban pasangan start/end |
| assets/prompt-template.md | Ganti menjadi template R2V sembilan bagian |
| assets/image-prompt-template.md | File baru untuk prompt satu gambar area dengan spesifikasi bersama |
| scripts/validate_project.py | Validasi V2 dan pesan yang jelas untuk data V1 |
| scripts/build_production_package.py | Paket prompt gambar atau paket R2V sesuai tahap; gambar individual dan peta referensi benar |
| scripts/split_frames.py | Lepas dari alur V2; hapus dari paket setelah seluruh pemanggil/dokumen diperbarui |
| agents/openai.yaml | Selaraskan metadata lewat generator yang sesuai, pertahankan kebijakan/dependensi yang masih relevan |
| tests/ | Perbarui tes kontrak, praproduksi, penyerahan dan arsip; ganti tes crop dengan tes alur gambar V2 yang relevan |
| tooling/package_plugin.py | Pertahankan pengemas; sesuaikan bila inventaris baru menuntut perubahan nyata |

Tabel komponen skills/... mengacu ke home-productions/skills/produce-home-tour/. Dokumen pengembangan, tes, dist/ dan runs/ tetap di luar paket plugin. Tidak membuat direktori home-productions-v2/ atau salinan pustaka.

## 5. Tahap implementasi V2

### Tahap 1 — Menetapkan spesifikasi dan kasus acuan

Petakan keputusan pengguna ke aturan, mode, cakupan gambar dan data proyek. Tetapkan kasus 18/20/22/24 detik serta tujuh gambar sekaligus. Tandai laporan R2V satu gambar sebagai bukti pengguna; batch tujuh dan R2V dua gambar masih perlu diuji.

**Keluaran:** spesifikasi field/aturan dan daftar penerimaan yang siap dipakai tahap kontrak. **Selesai bila:** tidak ada kewajiban kolase/start–end yang tersisa pada spesifikasi V2, jumlah gambar dan shot tidak tercampur. Tidak perlu mengulang pengujian R2V satu gambar yang telah dilaporkan pengguna.

### Tahap 2 — Kontrak, aturan dan validator V2

Perbarui rules, schema, template dan validator. Implementasikan tahap prompt gambar tanpa aset, tahap gambar final, serta paket R2V. Periksa dua gambar pada masing-masing shot penghubung; ID/path/peran berbeda dan sesuai area, tanpa menyamarkan satu gambar identik sebagai dua area.

**Keluaran:** proyek V2 yang dapat divalidasi beserta tes bermakna. **Selesai bila:** data perencanaan valid tanpa gambar; pemetaan salah, aset kurang/usang, durasi salah, cakupan berulang, bedroom tambahan dan sudut pan/orbit di bawah 12 ditolak sesuai tahap. Video R2V final tidak ditolak hanya karena tidak memiliki start/end frame.

### Tahap 3 — Skill, desain bersama dan pilihan mode

Perbarui entrypoint/praproduksi dan metadata. Tetapkan plafon serta elemen tetap pada rancangan. Pilihan mode diambil satu kali setelah desain disetujui, atau mengikuti pilihan/delegasi yang sudah ada. Gerak berasal dari DNA sumber lalu disesuaikan dengan durasi baku; jangan menambahkan gerak/area generik tanpa acuan.

**Keluaran:** alur brief sampai daftar shot dan gambar yang jelas. **Selesai bila:** contoh empat shot/20 detik merencanakan lima gambar, bukan delapan frame; pilihan mode dan persetujuan tidak diminta ulang tanpa alasan.

### Tahap 4 — Prompt gambar dan generate seluruh gambar individual

Perbarui image-workflow dan buat template prompt gambar. Mode prompt_to_image menyerahkan seluruh prompt; generate_image mengerjakan seluruh batch individual. Gunakan spesifikasi rumah yang sama pada setiap area; periksa cakupan luas, plafon dan naturalitas. Sediakan file individual serta catatan kekurangan/revisi tanpa mengklaim jumlah selesai secara palsu.

**Keluaran:** paket prompt gambar atau gambar area sesuai mode, lalu jalur review menuju image_final. **Selesai secara teknis bila:** penghitungan/pemetaan, file aktual, status batch dan pengikatan revisi berfungsi tanpa kolase/crop. Pemenuhan tujuh gambar sekaligus dan kualitas seluruh gambar tetap dibuktikan manual setelah rilis uji.

### Tahap 5 — Prompt R2V, ekspor dan transisi data lama

Terapkan sembilan bagian prompt yang sama dengan alur penggunaan. Tentukan peran masing-masing referensi, komposisi awal–akhir, lintasan, perkiraan sudut/jarak dan bukti gerak. Samakan ID gambar/durasi/revisi antara shot, prompt dan paket.

Perbarui ekspor untuk image_prompt_package dan prompt_package. Paket pertama berisi prompt serta catatan tanpa klaim gambar tersedia. Paket final memuat gambar asli, prompt R2V, peta gambar–shot, petunjuk penggunaan dan catatan proyek.

**Keluaran:** paket yang dapat dilanjutkan pada sesi baru. **Selesai bila:** dua area penghubung tetap satu shot dengan dua referensi; tidak ada instruksi yang memaksa referensi sebagai first/last frame; salinan paket mempertahankan data/file dan tidak menimpa hasil lama.

### Tahap 6 — Pemeriksaan teknis dan update privat untuk uji

Jalankan tes yang relevan, validasi format skill/manifest, pemeriksaan seluruh tautan dan arsip. Inspeksi penghapusan komponen lama beserta pemanggilnya. Kemas hanya source plugin ke dist/; hasil gambar dan proyek percobaan tetap di runs/.

Update plugin yang sama melalui Plugin Creator setelah pemeriksaan teknis. Baca inventory/current_release_id terlebih dahulu, gunakan expected_release_id aktual dan delete_paths untuk file lama yang memang dihapus. Update bersifat overlay; tidak cukup hanya menghilangkan file dari ZIP.

**Keluaran:** rilis privat V2 untuk diuji pengguna. **Selesai bila:** versi dan komponen tersimpan dapat dibaca balik, perubahan/penghapusan terverifikasi, dan tautan rilis dicatat. Keberhasilan upload tidak otomatis berarti penerimaan atau aktivasi ChatGPT sudah lulus.

### Tahap 7 — Uji manual pengguna, perbaikan dan penerimaan

Pengguna menguji plugin rilis di ChatGPT. Prioritas: alur prompt-to-image, generate seluruh batch, review plafon/naturalitas, R2V satu gambar dan dua referensi pada kedua shot penghubung, gerak 12 derajat, serta kelanjutan sesi.

Pengguna sudah menjalankan eksperimen Omni Flash; untuk V2, kasus video baru diuji manual sesuai kesediaan/hasil yang dibawa pengguna. Jangan mengubahnya menjadi kewajiban pengujian otomatis developer atau meminta nama aplikasi/API sebagai syarat memulai. Belum diuji tetap dicatat sebagai belum diuji.

**Keluaran:** laporan pada rencana aktif ini, perbaikan terarah dan update plugin yang sama. **Selesai bila:** keluaran wajib serta kasus utama V2 diterima berdasarkan bukti; kasus yang belum teruji tidak diberi status lulus. Uji ulang difokuskan pada bagian terdampak.

## 6. Matriks penerimaan minimum

| Kasus | Hasil yang diharapkan | Cara pembuktian |
| --- | --- | --- |
| Lima area terpisah | Lima gambar, lima shot, 22 detik | Kontrak + manual gambar/prompt |
| Living-to-kitchen | Dua gambar area, satu shot 6 detik; tidak diikuti kitchen lagi | Kontrak + R2V manual |
| Exterior-to-living | Dua gambar area, satu shot 6 detik; living tidak diulang | Kontrak + R2V manual |
| Contoh empat shot | Lima gambar dan empat prompt R2V, total 20 atau 18 detik sesuai pola | Kontrak + paket |
| Laundry/wardrobe/fungsi terpadu | Sesuai sumber, durasi 4 detik; tidak mengubah pola menjadi ruang baru | Sumber + kontrak + manual |
| Prompt-to-image tujuh gambar | Tujuh prompt individual, tanpa mengklaim file gambar sudah ada | Kontrak + manual |
| Generate tujuh sekaligus | Tujuh file individual dalam satu tahap/permintaan; tidak diganti kolase/perintah per gambar | Uji manual ChatGPT; catat eksekusi aktual |
| Plafon dan hubungan ruang | Sama dengan rancangan dan konsisten antararea yang terhubung | Review gambar nyata |
| Naturalitas dan cakupan area | Area terbaca luas, perspektif/skala/cahaya wajar; tidak ada crop yang membuang informasi utama | Review gambar nyata |
| R2V dua referensi | Dua identitas area digunakan dalam satu lintasan, bukan blend dua rumah atau interpolasi wajib | Uji manual video |
| Gerak gabungan | Komponen perpindahan dan pan/orbit terlihat sesuai simultan/sekuensial | Data/prompt + review video |
| Pan/orbit di bawah 12 derajat | Rancangan ditolak untuk gerak yang memang mensyaratkannya; gerak translasi tidak dipaksa berputar | Validator + review video hasil |
| Ritme 4/6 detik | Jarak/sudut dan fase masuk akal; tidak hanya kata slow yang bertentangan dengan lintasan | Review prompt + video |
| Musik atau perubahan struktur | Temuan dicatat dan hasil direvisi; audio hanya dinilai bila dapat didengar | Review media |
| Sesi baru dan revisi desain | Mode/keputusan tetap terbaca, file asli tersedia, gambar/prompt terdampak direview ulang | Ekspor + manual |
| Data V1 dan kegagalan akses | Pesan versi/akses jelas, tidak memalsukan migrasi, gambar, review atau keberhasilan batch | Tes kontrak + manual |

## 7. Migrasi dan kebersihan repo

V2 adalah pengganti alur produksi utama, bukan tambahan pilihan kolase/interpolasi dalam menu. Dua mode hanya mengatur cara memperoleh gambar; metode video utamanya R2V.

Proyek schema 1.0 dikenali dan diberi penjelasan versi. Jangan diam-diam mengubah pasangan frame lama menjadi gambar full area atau membawa persetujuan visual ke V2. Brief, desain, sumber dan keputusan yang masih berlaku boleh dipakai kembali dengan peninjauan. Migrasi nyata dilakukan pada salinan/revisi proyek sesuai permintaan, tanpa menimpa proyek V1.

Hapus file kolase/crop yang tidak lagi dipakai setelah semua tautan, tes dan callers diperiksa. Riwayat Git serta rilis lama menyimpan versi V1; jangan mempertahankan dua entrypoint produksi yang membingungkan AI. Tool probe lama yang berada di luar paket ditinjau kegunaannya sebelum dipertahankan/dihapus.

Jangan menghapus manifest kompatibilitas yang dibuat layanan jika deklarasi yang meregenerasikannya masih berlaku. Tidak menyalin email akun ke repo. Publisher, scope/audience dan pengaturan akun dipertahankan melalui mekanisme update yang benar.

## 8. Identitas rilis dan status

Identitas terakhir yang tercatat, dibaca ulang saat implementasi/update:

- Nama: home-productions; skill: produce-home-tour.
- Versi tersedia: 2.0.0; versi sebelumnya 0.1.0 tetap tercatat dalam riwayat rilis.
- Plugin ID: plugins_6afd5aeb32208191a60a8b85426c898f.
- Release ID terakhir terverifikasi: pluginrel_6afd8f59eab0819199eed6bf3b189717; baca ulang sebelum update berikutnya.
- [Tautan plugin yang sama](https://chatgpt.com/plugins/plugins_6afd5aeb32208191a60a8b85426c898f).
- Scope terakhir USER, PRIVATE; tidak diperluas atau dipublikasikan ke direktori umum.

| Tahap V2 | Status |
| --- | --- |
| 1 — Spesifikasi dan kasus acuan | Selesai; aturan, kontrak dan kasus 18/20/22/24 detik serta tujuh gambar |
| 2 — Kontrak dan validator | Selesai; schema/rules V2, gambar area, batch, kamera dan kompatibilitas V1 |
| 3 — Skill dan desain bersama | Selesai; satu skill, plafon/connections dan keputusan mode |
| 4 — Dua mode gambar individual | Implementasi selesai; pemenuhan batch/naturalitas menunggu uji manual |
| 5 — Prompt R2V, paket dan transisi | Selesai; sembilan bagian dan dua jenis ekspor tanpa start/end wajib |
| 6 — Teknis dan update privat untuk uji | Selesai; 53 tes V2 lulus, rilis 2.0.0 dibaca balik |
| 7 — Penerimaan manual dan perbaikan | Menunggu hasil pengguna; panduan uji sudah tersedia |

Urutan tetap: implementasi → pemeriksaan teknis → update privat untuk uji → uji manual pengguna → perbaikan → penerimaan. Tidak menahan seluruh rilis hingga pengguna menguji salinan master prompt.

## 9. Acuan pemeliharaan

Perubahan perilaku memperbarui alur penggunaan, aturan mesin dan kontrak pada perubahan implementasi yang sama. Source dan rilis aktif sudah memakai V2; alur V1 tersedia pada riwayat Git/rilis sebelumnya. Setiap tahap mencatat hasil aktual pada dokumen aktif, bukan laporan/salinan plan baru.

Baseline V1: implementasi kolase/first–last tersedia pada 0.1.0; 65 tes teknis pernah lulus. Temuan manual pengguna mendorong penggantian alur, sehingga angka tersebut tidak menjadi bukti keberhasilan V2.

Revisi 2.0 — Menyusun migrasi ke gambar area individual dan R2V, dua mode gambar, batch tujuh, plafon/naturalitas, gerak terlihat minimal 12 derajat serta update privat sebelum penerimaan manual.


## 10. Hasil implementasi — 18 November 2026

| Bagian | Hasil aktual |
| --- | --- |
| Kontrak | Schema 2.0/rules 2.0.0; image_plan terpisah dari file assets, mode tersimpan, plafon/connections wajib pada rancangan |
| Gambar | Prompt-to-image sah tanpa aset; generate_image mencatat permintaan/pelaksanaan batch, gambar parsial/gagal tetap draft; PNG/JPEG/WEBP aktual diperiksa tanpa memaksa crop 9:16 |
| Pemetaan | Lima gambar untuk empat shot/20 atau 18 detik; dua referensi individual untuk living-to-kitchen dan exterior-to-living |
| Kamera | Komponen dan fase diperiksa; pan/orbit minimal 12°, translasi tidak dipaksa berputar, perkiraan jarak serta total alokasi durasi konsisten |
| Prompt | Sembilan sections menjadi satu sumber teks; peran setiap image_id, revisi/durasi/pemetaan dan aturan ambient/continuous diperiksa |
| Ekspor | image_prompt_package dan prompt_package; gambar asli, prompt, panduan dan project.json dapat dibawa ke folder/sesi baru, tanpa klaim review otomatis |
| Transisi | Data V1 mendapat pesan migrasi pada salinan; tidak otomatis mengubah frame lama atau membawa persetujuan visual |
| Pembersihan | split_frames.py dan tes crop V1 dihapus; probe_stage1.py yang tidak lagi dirujuk juga dihapus. Template gambar individual ditambahkan |
| Teknis | 53 tes V2 lulus; format skill, schema manifest resmi, Python/JSON/YAML, tautan internal dan arsip diperiksa |
| Rilis | Plugin yang sama di-update ke 2.0.0, USER/PRIVATE. Enam belas berkas upload diverifikasi lewat pembacaan balik; manifest kompatibilitas layanan menjadi berkas ke-17 |
| Preservasi | Plugin ID, publisher akun, defaultPrompt dan scope/audience tetap. Tidak menyalin email akun ke repo atau mengubah pustaka sumber |

Pengujian memakai fixture yang ditandai sintetis. Catatan parallel, review dan persetujuan pada fixture bukan bukti batch nyata atau keputusan pengguna. Dua kasus anotasi edh022/edh035 dipakai ulang untuk pemeriksaan struktur; bukan analisis ulang video. Tes ekspor membuktikan file/data tetap dapat divalidasi setelah folder kerja asal dihapus.

Rilis: [home-productions 2.0.0](https://chatgpt.com/plugins/plugins_6afd5aeb32208191a60a8b85426c898f).
Release ID: pluginrel_6afd8f59eab0819199eed6bf3b189717.
Arsip: dist/home-productions-2.0.0.zip, diabaikan Git.
SHA-256 upload: 1f0a90d3f156055f04ae4f52a2bc9fa123b3a230c636c4c36b3ff7a1f1d10677.

Update memakai expected_release_id aktual dan delete_paths untuk script crop lama. Pembacaan inventaris lengkap memverifikasi script tersebut hilang, template gambar baru tersedia, versi kompatibilitas sinkron serta publisher/defaultPrompt dipertahankan. Tidak dibuat plugin baru atau mengubah sharing.

### Tahap 7 — Serah-terima uji manual

Gunakan [panduan uji di README](README.md#uji-manual-v2). Uji terpisah:
1. Prompt-to-image: seluruh prompt area, tanpa generate otomatis atau klaim file tersedia.
2. Generate image: seluruh jumlah gambar individual sekaligus; khusus tujuh gambar, catat jumlah file dan pelaksanaan aktual.
3. Review plafon, geometri, hubungan ruang, naturalitas dan kesesuaian desain dari hasil nyata.
4. R2V satu gambar dan dua referensi pada living-to-kitchen serta exterior-to-living; satu shot, bukan dua klip.
5. Gerak gabungan, minimum rotasi yang diminta, ritme 4/6 detik, continuous shot dan ambient tanpa musik.
6. Ekspor serta kelanjutan sesi dengan file asli, lalu revisi satu keputusan dan tinjau dampaknya.

Belum ada hasil manual V2 yang diterima pada saat rilis ini. Aktivasi/pemilihan skill di ChatGPT, tujuh gambar serentak, naturalitas/plafon dan video/audio tidak dinyatakan lulus dari source atau 53 tes. Perbaikan berikutnya mengikuti temuan pengguna dan menggunakan plugin ID yang sama.

Revisi 2.1 — Mencatat implementasi tahap 1–6, pemeriksaan teknis, pembersihan alur lama, rilis privat 2.0.0 yang terverifikasi dan tahap 7 yang menunggu hasil manual.
