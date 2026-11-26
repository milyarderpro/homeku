# Kontrak paket HOMEKU 3.1

Audit.json adalah satu sumber keputusan isi; analysis.md hasil renderer dan manifest.json metadata teknis/provenance. Kontrak ini menggantikan pemakaian beberapa format setelah cutover selesai.

## Matriks pemilik informasi

| Kemampuan | Sumber final | Turunan / tampilan |
| --- | --- | --- |
| Nama desain | design.name | Judul laporan |
| Tipe rumah | design.house_type | Profil dan facet house-type |
| Palet warna terstruktur | design.palette | Tabel Peran, Warna, HEX dan bukti per warna |
| Gaya utama | design.styles.primary | Profil dan facet primary-style |
| Pengaruh gaya | design.styles.influences[] | Daftar terpisah dan facet style-influence |
| Gaya interior | design.styles.interior[] | Profil dan facet interior-style |
| Relasi gaya | design.styles.relations[] | Filter family/blend/influence eksplisit |
| Skala rumah | design.size.scale | Profil dan facet apparent-scale |
| Tingkat terlihat | design.size.levels | Tabel ukuran dan facet levels-visible |
| Tapak / proporsi | design.size.footprint / proportions | Tabel ukuran |
| Estimasi luas | design.size.floor_area_m2 {min,max} | Rentang m² tanpa catatan wajib tambahan |
| Massa bangunan | design.features[aspect=massing] | Tabel ukuran / DNA |
| Atap | design.features[aspect=roof] | Tabel ukuran / DNA |
| Entrance / porch / bukaan | features aspek entrance / porch / openings | DNA dan discovery |
| Material utama | features aspek material-hierarchy | Profil / DNA |
| Pencahayaan / atmosfer / lingkungan | features aspek lighting / atmosphere / environment | Baris terpisah di Profil Desain |
| Konfigurasi / ciri khas / kontinuitas | features aspek spatial-configuration / distinctive-features / continuity | Profil dan DNA |
| Area fisik dan fungsi | areas[].id / label / functions | Facet area/fungsi |
| Visibilitas area | areas[].visible_intervals | Hubungan lintas area; tidak sama dengan route |
| Take kontinu | shots[].shot / start_s / end_s | Durasi dan Shot Timeline |
| Rute dan penghubung | shots[].route / area_relations | Rute kamera dan hubungan area |
| Desain manusia | shots[].design[].architecture / furnishings / environment .text | Paragraf A. Desain area |
| Fakta AI | Ketiga kategori desain .facts[] | Kategori melekat; tanpa fact_coverage paralel |
| Camera Start | shots[].composition | Posisi/arah/angle awal sumber |
| Production Start | shots[].composition.production_start | Penunjuk frame native jernih dan framing untuk awal produksi saat ada transisi |
| Framing / fokus / cahaya | shots[].composition | B. Framing & Lighting |
| Gerak Indonesia | shots[].camera.description | C. Camera Movement |
| Gerak teknis | shots[].camera.phases[].notation | Parser dan summary; tidak ditulis kembali |
| Arah translasi | phases[].depth_direction | Camera Pattern mekanis |
| Pengamatan kamera | phases[].observations / evidence | Tiga sumbu dengan bukti bersama |
| Tempo | shots[].camera.tempo | Overlap fase mekanis, terpisah dari easing |
| Alur visual | shots[].camera.journey bila diperlukan | Journey multi area |
| Panel / Overview | shots[].panels / overviews | Selection ID, PTS dan bbox dalam manifest |
| Frame wide terpilih | overviews[].composition_summary | Paragraf Overview; bukan Camera Start |
| Hubungan antarshot / batas | relations / notes | Reader dengan provenance eksplisit |
| Bukti klaim | evidence indeks native | Frame map manifest dan pointer sumber |
| Pemeriksaan viewed | Workspace session dan audit-info | Provenance pemeriksaan teknis manifest |
| Skala/sudut kamera | notation dengan estimasi visual yang dapat dibuat secara wajar | Parser memeriksa sintaks dan nilai angka yang ditulis |
| Pengukuran/flow/cache | Workspace saja | Tidak menjadi fakta kedua atau isi ZIP |

Setiap klaim memiliki satu lokasi sumber; renderer dan generator merujuk lokasi tersebut. State/negasi/evidence tetap eksplisit. Confidence yang tidak diisi berarti tidak dinilai. Narasi manusia dan fakta atomik tetap diperlukan untuk fungsi berbeda; generator tidak mengekstrak fakta dari prosa.

## Pemisahan sumber dan proses

Profile paralel, components_parsed, camera_summary, fact_coverage/fact_ids, timestamp/shot_id selection berulang, esai basis wajib dan null pengukuran kosong dihapus dari audit final. Nilai turunan dihitung sesuai kebutuhan tanpa model legacy perantara.

Frame map menyimpan indeks yang dirujuk audit dan seleksi, termasuk Production Start bila dipilih. Acuan produksi memakai shot dan deklarasi viewed yang sama dengan sumber, dengan PTS setelah awal native shot. Pada shot biasa, Production Start juga menjadi panel Start bila dipilih. Batas shot tetap memakai PTS sumber. JPEG berasal dari seleksi panel dan Overview. Sesi, status pemeriksaan kamera, cache, log performa, sheet dan receipt berada di workspace. Satu take sampai cut tetap satu shot; fungsi area yang berubah tidak menjadi cut.

## Struktur, versi dan penyerahan

Format aktif adalah 3.1. Audit ulang MP4 dengan kit 3.1 jika paket atau sesi berasal dari versi sebelumnya. Schema lokal berada di schemas/ untuk audit, audit-info, manifest, reference-reader dan search-index. Template adalah kerangka belum valid, bukan hasil pengamatan.

ZIP final bernama <id>-rNNNN.zip berisi satu folder <id>/ dengan audit.json, analysis.md, manifest.json dan media/shot-NN.jpg, media/overview.jpg, media/storyboard.jpg. Tidak ada MP4, sheet, cache, session, log atau receipt. Video sumber kanonis terpisah di video/<id>.mp4 dan SHA-256 harus cocok.

Sumber baru revision 1 dengan supersedes null. Revisi berikutnya +1 dan supersedes mengikat revision/content_sha256 aktif. `review` memvalidasi kandidat dan mencatat hash snapshot dalam receipt di luar folder kandidat. Segera setelah `review` berhasil, `export` membungkus snapshot yang sama tanpa render ulang. Tampilkan tautan ZIP bersama laporan dan media di chat agar pengguna dapat memeriksa dan memilih ZIP yang akan di-ingest.

Baseline 6 FPS ditambah batas native; sumber ≤6 FPS atau shot <1 detik seluruh native. Pendalaman 10 FPS/native sesuai pertanyaan visual. Log selected dan viewed tetap berbeda. Bukti gerak membutuhkan minimal dua frame temporal berbeda pada fase/toleransi batas satu native, dengan scope dan viewed tervalidasi.

Manifest menyimpan provenance, source metadata/hash, render fingerprint, frame map terbatas, selections, media/bbox/hash dan audit_sha256. Semua fakta tetap pada audit.json. Lihat report.md dan reader.md untuk tampilan manusia dan akses AI.

Template laporan dan layout media mengikuti aset kanonis runtime 3.1. Manifest menyimpan fingerprint kedua aset untuk verifikasi.

Validasi menggunakan allowlist dengan nama file dan casing yang tepat serta mencocokkan hash sumber, audit dan tiap JPEG. Review menghasilkan kartu dan receipt di luar kandidat. Ekspor memeriksa receipt dan snapshot, lalu memverifikasi isi ZIP terhadap hash snapshot tanpa memanggil renderer atau membaca MP4.
