# Kontrak proyek 2.1

Paket/rules 2.1.0, schema 2.1. Gunakan [template](../assets/project-template.json), [schema](../assets/project.schema.json), [aturan](production-rules.yaml) dan [validator](../scripts/validate_project.py). Data rencana tidak membuktikan kualitas gambar/video.

## Keputusan, sumber dan tahap

project_id/revision mengikat keputusan, prompt dan aset. knowledge menyimpan repo HOMEKU, ref/commit, route web/github_connector dan evidence yang benar-benar dibaca. URL anotasi harus cocok dengan versi dan ID. Bukti continuous shot harus mendukung cakupan; label tematik tanpa cut tidak otomatis menjadi shot lain.

approvals memuat concept, shot_plan dan visual: revision, by user/delegated serta note berdasarkan tindakan nyata. Mode/delegasi tidak diminta ulang tanpa alasan. Revisi material meninjau keputusan dan keluaran terdampak; jangan mengganti angka revisi aset lama untuk menutupi isi usang.

| Stage | Kebutuhan |
| --- | --- |
| brief | Template kosong sah; sumber/gambar belum wajib |
| concept | Brief, konsep pilihan, versi/jalur dan bukti sumber yang dibaca |
| shot_plan | Desain bersama, area_specs, shot, pilihan referensi, komposisi dan spatial_plan; file gambar belum wajib |
| image_prompt_package | Mode prompt_to_image, persetujuan konsep/shot, seluruh prompt lengkap; sah tanpa file, belum siap R2V final |
| image_draft | Gambar sedang diperoleh/direvisi; kegagalan/parsial dicatat sesuai fakta |
| image_final | File asli, revisi cocok, review nyata dan persetujuan/delegasi visual |
| prompt_package | Gambar final dan sembilan bagian prompt R2V per shot lengkap |

## Satu tata ruang dan komposisi

design mempertahankan architecture/layout/ceiling/materials/lighting/environment, connections dan anchors. Tambahkan area_specs: satu entri per area yang dicakup rancangan, berisi area, position, ceiling dan fixtures.

position menetapkan lokasi tetap fungsi/objek utama relatif terhadap rumah. Kitchen hanya mempunyai satu lokasi. ceiling menggambarkan plafon area tersebut; fixtures berisi jenis/posisi armatur dan kondisi cahaya yang dirancang. Setiap interior harus memiliki lampu; tidak semua lampu wajib menyala. Area yang belum terlihat pada foto tetap mempunyai spesifikasi desain jika akan diungkap video.

image_plan merupakan daftar **pandangan**, bukan kewajiban satu file per label fungsi. Setiap entri memuat image_id, primary_area, area_ids, shot_ids, revision, prompt, status, asset_id, error dan composition. area_ids hanya mencatat area yang benar-benar terlihat, termasuk kedua area living–kitchen pada foto gabungannya. primary_area adalah label pengorganisasian, bukan alasan menggandakan file.

composition memuat:
- camera_position, view_direction, height_m dan subject_view.
- view_angle_deg (boleh null di luar bedroom), subject_placement, foreground/background.
- visible_bounds, layout_note dan shot_alignment terhadap lintasan.
- full_exterior dan bed_diagonal sebagai **target komposisi**, bukan klaim hasil piksel.

Gambar yang mencakup exterior memakai full_exterior true: seluruh massa rumah terlihat beserta tepi aman. Bedroom memakai subject_view front_three_quarter, view_angle_deg 35–45 terhadap sumbu panjang bed di bidang horizontal dan bed_diagonal true. Itu preferensi pengguna/adaptasi proyek, bukan pengukuran semua sumber.

camera.spatial_plan berisi start_position, start_direction, path, end_position, end_direction dan layout_check. Gunakan tata ruang yang sama dengan komposisi gambar; jangan mendeskripsikan kitchen di posisi kedua. framing.start/end menjelaskan hasil komposisi, bukan endpoint referensi wajib.

composition dan spatial_plan boleh null sebelum rancangan lengkap atau pada salinan migrasi yang belum ditinjau; keduanya wajib pada shot_plan dan tahap setelahnya. Nilai numerik adalah perkiraan produksi. Validator tidak mengukur geometri 3D dari piksel.

## Referensi per shot

shots[].reference_image_ids menunjuk image_plan, bukan asset_id; shot_ids pada gambar adalah peta balik yang sama. reference_choice berisi count, by (default/user/delegated) dan note.

- Living-to-kitchen: default satu foto utuh living+kitchen, satu shot 6 detik. Dua referensi hanya atas pilihan pengguna/delegasi; bukan kewajiban.
- Exterior-to-living: pengguna bebas memilih **1 atau 2 referensi**. Catat by user/delegated dan jumlah yang dipilih; jangan menetapkan salah satu sebagai kewajiban atau meminta pilihan yang sudah diberikan.
- Dengan satu referensi exterior-to-living, area terlihat boleh lebih sedikit daripada cakupan video, tetapi harus berada dalam cakupan shot dan area tersembunyi mempunyai desain. Jangan memaksa seluruh interior terlihat dalam foto exterior.
- Dengan dua referensi exterior-to-living, gunakan exterior dan living individual dari rumah yang sama, bukan dua versi desain/file identik. Hubungan pintu masuk dan interior direview.
- Area lain/fungsi terpadu mengikuti cakupan sumber dan pemetaan yang disetujui. Jumlah gambar bukan penentu jumlah shot atau durasi.

Cakupan tidak berulang, maksimal satu bedroom/sleeping_loft. Exterior dan kedua penghubung 6 detik; shot lainnya 4 detik. Kamera mencatat komponen translasi/pan/orbit/tilt, simultan/sekuensial, jarak/sudut, waktu, bukti gerak dan timing_note. Pan/orbit terpilih ≥12°; translasi murni tidak dipaksa berputar.

## File, review dan batch

assets berisi asset_id, image_id, revision, role reference, path relatif, sha256, dimensi, format PNG/JPEG/WEBP, reviewed, review_origin ai_visual/user_report dan review_note. Path tetap di dalam folder proyek; file/hash/dimensi/format diperiksa bila folder tersedia, dan file wajib pada tahap final. File identik tidak boleh disamarkan sebagai dua referensi berbeda.

planned/prompt_ready/failed belum mengaku punya aset; available memerlukan file terdaftar; reviewed memerlukan review dengan asal/catatan nyata. failed memuat error. Persetujuan/review adalah catatan keputusan, bukan hasil pemeriksaan otomatis.

image_mode adalah prompt_to_image atau generate_image. image_batch mencatat request_mode all_at_once/one_by_one, execution, user_instruction dan note. Satu per satu memerlukan permintaan pengguna. Jangan mengaku parallel dari jumlah file atau permintaan batch saja. Pelaksanaan yang belum terbukti sesuai permintaan tetap draft; tes sintetis bukan bukti kemampuan host.

## Prompt dan penyerahan

prompt memuat method R2V, revision, duration_s, reference_image_ids dan sections. Sembilan bagian pada rules menjadi satu sumber teks.

REFERENCE IMAGE ROLE memuat kalimat kontrak reference_role dari aturan: gambar sebagai identitas visual/spasial, bukan first/last wajib. **Tidak ada nama file, path, image_id, asset_id atau shot_id internal di badan prompt video.** Pemetaan teknis tetap ada di JSON/panduan lampiran. CONTINUITY AND AUDIO RULES memuat instruksi continuous/ambient dari aturan; isi lainnya harus selaras.

Di chat: satu fenced code block berisi satu prompt utuh per shot. Judul, petunjuk lampiran dan penjelasan di luar. Ekspor .txt berisi teks yang sama tanpa pagar Markdown.

Paket prompt gambar boleh tanpa aset; paket R2V final memerlukan file asli. Lihat [checkpoint](../scripts/save_project.py) untuk penyimpanan tahan gagal dan [pembuat paket](../scripts/build_production_package.py) untuk ekspor. File proyek adalah catatan produksi di ruang kerja/unduhan, bukan penambahan otomatis ke GitHub.

## Kompatibilitas

Schema 2.0 dikenali dengan pesan konversi. migrate_project pada validator membuat **salinan** ke 2.1: brief, sumber, konsep, mode dan keputusan konsep/shot dipertahankan; komposisi/spatial_plan/pilihan referensi baru belum diisi. Prompt video lama dibersihkan untuk ditulis ulang, review visual baru tidak diklaim, dan keputusan visual lama dicatat sebagai historis.

Salinan kembali ke concept bila rancangan belum memenuhi kontrak baru. Ini tidak membatalkan pilihan konsep pengguna. Lengkapi data, tinjau dampak, lalu lanjutkan rancangan yang sama; jangan menghasilkan rumah baru atau menggabungkan dua foto lama secara otomatis. CLI konversi menggunakan lokasi keluaran baru, tanpa menimpa sumber.

Schema 1.0 tetap dikenali sebagai alur lama. Frame kolase/first–last tidak otomatis menjadi gambar full area atau membawa persetujuan visual.
