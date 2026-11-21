# Omni Flash R2V, kamera dan penyerahan

Gunakan setelah gambar asli tersedia, dilihat dan disetujui/didelegasikan. Baca [kontrak](project-contract.md), [aturan](production-rules.yaml) dan [template R2V](../assets/prompt-template.md). Jika gambar menyimpang dari rancangan, kembali ke [alur gambar](image-workflow.md).

## Identitas visual/spasial, bukan endpoint

Satu shot memakai satu prompt R2V dan satu klip. Gambar terlampir menjadi referensi identitas visual/spasial, **bukan kontrol frame awal atau akhir wajib**, bukan interpolasi first–last. Kamera tetap mempunyai komposisi awal/akhir yang direncanakan dan sesuai geometri.

- Living-to-kitchen default satu foto utuh living+kitchen yang terhubung. Kitchen tetap satu pada lokasi rancangan. Referensi tambahan hanya jika diminta pengguna/delegasi.
- Exterior-to-living mengikuti **pilihan pengguna 1 atau 2 referensi**; tidak mewajibkan dua atau mengunci satu. Jika dua, exterior/living individual menggambarkan satu rumah dan sambungan yang sama.
- Jika satu untuk exterior-to-living, interior tidak harus sudah terlihat penuh pada foto exterior. Desain ruang yang akan terungkap dijelaskan dari rancangan, tanpa mengklaim piksel telah membuktikannya atau membuat cutaway/transparansi.
- Fungsi terpadu lain mengikuti pemetaan yang disetujui. Jumlah referensi tidak menambah shot/cut atau mengubah durasi.

reference_image_ids tetap di data/panduan lampiran. **Jangan menuliskan nama file, path, image_id, asset_id atau shot_id internal dalam badan prompt video**, termasuk REFERENCE IMAGE ROLE. Gunakan “the attached reference image” atau deskripsi visual bila perlu. Alat mengenali gambar yang benar-benar dilampirkan; teks nama file bukan lampiran.

Kalimat reference_role dari prompt_constraints wajib hadir pada REFERENCE IMAGE ROLE. Jelaskan peran visual, bukan endpoint. Jangan meminta dissolve, blend dua rumah, teleportasi atau menciptakan pintu baru demi menyambung referensi.

Tidak menebak nama tombol, versi aplikasi, format/jumlah input di luar yang sudah dibuktikan pengguna atau parameter API. Percobaan R2V satu gambar yang sudah dilaporkan tidak diulang sebagai syarat developer. Hasil baru diuji pengguna pada host sesungguhnya.

## Sembilan bagian

Gunakan sembilan nama sections pada aturan, isi lengkap dan saling sesuai:

| Bagian | Isi |
| --- | --- |
| OUTPUT SPECIFICATION | Jenis home tour/area atau transisi, durasi shot 4/6 detik, video vertikal 9:16 |
| REFERENCE IMAGE ROLE | Identitas visual/spasial gambar terlampir; tegas bukan first/last wajib, tanpa nama file/ID |
| ARCHITECTURE AND DESIGN | Struktur, posisi ruang, material/furnitur, plafon/lampu, bukaan dan sambungan tetap |
| CAMERA START COMPOSITION | Posisi/arah awal, subjek, foreground/background berdasarkan tata ruang |
| CAMERA MOVEMENT | Gerak yang dipilih dari DNA per area, lintasan, jarak/sudut, ritme, hubungan simultan/sekuensial |
| VISIBLE MOTION EVIDENCE | Perubahan pada elemen nyata untuk membuktikan setiap gerak terpilih |
| ENDING COMPOSITION | Framing akhir yang sesuai lintasan dan geometri, tanpa endpoint gambar wajib |
| VISUAL CONSISTENCY LOCK | Struktur/posisi objek/ruang yang tetap; kitchen tunggal, plafon/lampu/bukaan tidak berubah |
| CONTINUITY AND AUDIO RULES | Satu shot tanpa cut/morphing; ambient natural halus tanpa musik/narasi/dialog/efek dramatis |

Salin continuous/audio dari aturan ke bagian terakhir. Baca prompt utuh agar tidak ada bagian lain meminta musik, cut atau perubahan struktur. Penanda template belum diisi tidak boleh diserahkan.

prompt.method R2V, revision, duration_s dan reference_image_ids cocok dengan shot. sections adalah satu sumber teks; jangan membuat text kedua yang bisa berbeda dari sections.

## Cocokkan gerak dengan gambar

Gunakan design.area_specs/connections/anchors, composition dan camera.spatial_plan yang sama. Posisi/arah kamera → lintasan → akhir harus sesuai ruang yang terlihat atau dirancang. Referensi tidak harus disalin sebagai komposisi awal, tetapi lintasan tidak boleh bertentangan dengan gambar.

Kitchen di depan pada gambar tidak otomatis membuat pan kanan salah. Periksa pose kamera, bidang pandang, rute dan akhir yang dituju. Jika tidak sesuai, revisi gambar/posisi kamera atau lintasan yang masih mengikuti sumber/desain; jangan menambah kitchen di kanan atau memindahkan kitchen yang sudah ada. Kalimat larangan duplikasi hanya pengunci setelah rancangan geometris sesuai.

Pilih gerak dari DNA sumber per area; tidak selalu dolly + pan. Dolly maju/mundur, tracking lateral, pan, orbit atau tilt dipakai jika cocok. Gerak tunggal sah. Gerak gabungan yang dipilih harus terlihat seluruh komponennya, bukan otomatis dihapus agar prompt mudah dijalankan.

Pan/orbit terpilih ≥12°. Pan adalah rotasi arah pandang, orbit perpindahan mengitari fokus. Jangan menggantinya dengan roll, rumah/bed yang berputar atau zoom digital yang tidak diminta.

single/simultaneous mencakup seluruh waktu shot; sequential mempunyai fase tersambung dengan total tepat. “Move forward while panning” berbeda dari “first move forward, then pan”. Pilihan waktu yang tidak dibuktikan sumber ditandai sebagai adaptasi proyek.

Exterior dan kedua penghubung 6 detik; area/fungsi terpadu lain 4 detik. Sesuaikan jarak, sudut, kecepatan dan jumlah fase. Jangan memakai slow sebagai kata wajib untuk rute panjang/banyak fase dalam 4 detik. Perubahan material pada rancangan yang disetujui kembali ke keputusan desain.

visible_motion_evidence memakai elemen yang sudah ada: foreground/perspektif saat dolly, pengungkapan sisi saat pan, parallax saat orbit. Angka 12° dalam prompt bukan bukti rotasi aktual video; periksa dari hasil nyata.

## Format chat siap salin

Tampilkan satu prompt lengkap sembilan bagian dalam **satu fenced code block per shot**. Di dalam block hanya teks final; tanpa judul pengantar, nama berkas, ID internal, JSON, placeholder, komentar atau instruksi membersihkan teks.

Judul shot, durasi ringkas, petunjuk lampiran dan catatan berada di luar block. Peta ID–file–shot boleh tampil di panduan luar prompt. Pengguna cukup menyalin isi block.

File video-prompts/*.txt berisi teks yang sama tanpa pagar Markdown. Renderer pada [pembuat paket](../scripts/build_production_package.py) menjaga urutan sembilan bagian dan dapat merender format chat dari sumber yang sama.

## Paket dan kelanjutan

| Stage | Penyerahan |
| --- | --- |
| image_prompt_package | project.json, production-guide.md dan seluruh image-prompts/*.txt; tidak mengklaim gambar telah dibuat/direview atau siap R2V final |
| prompt_package | Catatan/panduan, prompt gambar, gambar referensi asli dan video-prompts/*.txt per shot |

Jalankan pembuat paket dengan file checkpoint aktif dan folder tujuan baru. project.json, production-guide.md, image-prompts/ dan video-prompts/ adalah nama keluaran; simpan aset pada folder lain, misalnya images/. Jangan menimpa paket lama. Salinan divalidasi ulang.

Panduan memuat desain, komposisi/lintasan, peta lampiran sesuai pilihan, jumlah, durasi, sumber, keputusan, batch dan revisi. Tidak menyalin pustaka atau percobaan yang tidak terdaftar ke paket.

Serahkan unduhan tiap gambar, prompt dan panduan/catatan lewat mekanisme host. ZIP opsional tidak menggantikan gambar individual. Pengguna memasang 1/2 referensi sesuai peta pada R2V, memilih durasi shot dan generate satu klip; bukan memasukkan total durasi proyek sebagai satu klip.

Simpan keputusan melalui [checkpoint](../scripts/save_project.py). Bila gagal, lanjutkan dari data sesi dan jelaskan status, tanpa tautan palsu atau mengulang penulisan ke lokasi yang sama. Untuk schema 2.0, konversi pada salinan sebelum melengkapi komposisi dan review baru; brief/konsep/delegasi yang berlaku tidak diulang.

## Revisi hasil

Tinjau hanya video/gambar/audio yang dapat diakses. Thumbnail atau metadata tidak membuktikan geometri, naturalitas, plafon, lampu, gerak atau ambient.

Revisi penyebab: orientasi/geometri pada rancangan/gambar; jenis/jarak/sudut/ritme pada rencana kamera/prompt. Pertahankan bagian yang sudah benar. Perubahan elemen tetap meninjau semua bagian terdampak, tanpa menambah bedroom, mengulang area atau mengubah durasi/audio sebagai jalan pintas.

Cut antarklip hanya pada panduan perangkaian, tanpa musik pada editing. Sesi baru membawa catatan dan file asli; minta hanya yang hilang. Penyiapan paket tidak berarti video sudah dibuat, diterima, dirangkai atau dipublikasikan.
