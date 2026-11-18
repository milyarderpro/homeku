# Kontrak proyek home-productions V2

Schema proyek 2.0; rules 2.0.0. Gunakan [template](../assets/project-template.json), [schema](../assets/project.schema.json) dan [aturan](production-rules.yaml). File proyek/hasil berada di folder proyek host, terpisah dari paket plugin dan pustaka.

## Tahap dan mode

| Stage | Syarat |
| --- | --- |
| brief | Struktur awal; gambar/shot belum wajib |
| concept | Brief, konsep pilihan, jalur/versi dan sumber yang benar-benar dibaca |
| shot_plan | Desain termasuk ceiling/connections, cakupan sumber, kamera teralokasi, daftar gambar dan total |
| image_prompt_package | Mode prompt_to_image, keputusan konsep/shot, seluruh prompt gambar; aset belum wajib |
| image_draft | Mode dipilih, keputusan dan prompt gambar siap; gambar sedang dikerjakan atau perlu revisi |
| image_final | Seluruh file asli dan review, persetujuan visual, revisi dan pelaksanaan gambar sesuai mode |
| prompt_package | Gambar final serta prompt R2V sembilan bagian yang cocok |

Validator baca-saja dan tidak memakai jaringan. Proyek schema 1.0 ditolak dengan pesan peninjauan/migrasi V2; tidak diam-diam mengubah frame atau persetujuan lama. Migrasi pada salinan hanya ketika diminta.

## Sumber, rumah dan cakupan

knowledge mempertahankan repo, ref/commit, route web/github_connector serta evidence berisi referensi/shot, pointer, kutipan, cakupan dan kontinuitas. read hanya untuk isi yang benar-benar diperoleh; failed memuat error aktual tanpa klaim isi. Setiap shot merujuk bukti kontinu dengan cakupan sama. Metadata tidak membuktikan kutipannya benar; ikuti [akses repo](repo-access.md).

Jenis/cakupan mengikuti aturan sumber, tanpa pengulangan area dan maksimal satu fungsi tidur bedroom/sleeping_loft. Confidence tidak melarang desain baru. design menjelaskan architecture, layout, ceiling, materials, lighting, environment, connections dan anchors. Bedakan adaptasi rumah baru dari denah sumber.

## Gambar dan aset

image_mode null selama belum dipilih, lalu prompt_to_image/generate_image. image_batch mencatat request_mode all_at_once atau one_by_one, execution, user_instruction dan note. Satu per satu memerlukan instruksi eksplisit; parallel/external/sequential/unknown memerlukan dasar pada note.

image_plan berisi image_id, primary_area, area_ids, shot_ids, revision, prompt, status, asset_id dan error. Satu gambar aktif untuk satu area tujuan. Fungsi terpadu boleh tercakup pada area_ids; background insidental bukan tujuan tambahan.

shots[].reference_image_ids menunjuk image_plan, bukan asset_id. shot_ids pada gambar merupakan peta balik yang harus sama. Living-to-kitchen memerlukan living dan kitchen; exterior-to-living memerlukan exterior dan living. Fungsi terpadu lain dapat memakai kebutuhan tambahan yang masih berada dalam cakupan dan rancangan.

assets memuat file role reference yang terikat image_id dan revisi. asset_id pada image_plan menunjuk file tersebut. Path relatif dari project.json, tetap di dalam folder proyek; symlink keluar ditolak. Hash, format dan dimensi aktual diperiksa jika folder proyek tersedia; pada tahap final file wajib tersedia. Tidak ada kewajiban gambar 9:16 atau start/end/collage; video tetap 9:16.

PNG/JPEG/WEBP statis diperiksa sesuai format aktual; kesesuaian input pada aplikasi pengguna diperiksa pada workflow. Dua file identik atau satu path yang dipakai ulang tidak boleh menyamar sebagai area lain. reviewed membutuhkan review_origin dan review_note nyata. Validator tidak membuktikan plafon, naturalitas atau geometri.

Pada generate_image, final all_at_once membutuhkan catatan pelaksanaan parallel; one_by_one membutuhkan sequential dan instruksi pengguna. Jumlah file tidak membuktikan pelaksanaan serentak. Pada prompt_to_image, gambar eksternal dicatat dengan execution external atau unknown beserta dasar perolehannya; paket prompt gambar saja sah tanpa pelaksanaan/file.

## Kamera dan prompt video

camera mencatat description, motion_relationship, components, visible_motion_evidence dan timing_note. Komponen berjenis translation/pan/orbit/tilt, mempunyai start_s/duration_s serta perkiraan distance_m/angle_deg. single satu komponen sepanjang shot; simultaneous dua atau lebih sepanjang durasi sama; sequential fase berurutan yang tepat mencakup durasi shot. Translasi memerlukan jarak positif; pan/orbit minimal 12 derajat. Ini pemeriksaan rencana, bukan sudut hasil video.

shots[].prompt null sebelum ditulis; setelah lengkap memuat method R2V, revision, duration_s, reference_image_ids dan sections. Sembilan nama bagian mengikuti prompt_sections pada aturan. REFERENCE IMAGE ROLE menyebut setiap image_id dengan perannya. CONTINUITY AND AUDIO RULES memuat instruksi wajib aturan secara utuh. Penanda template yang belum diisi ditolak.

sections menjadi satu sumber teks. [Pembuat paket](../scripts/build_production_package.py) merender judul/bagian ke file prompt secara deterministik; tidak ada text kedua yang boleh berbeda dari sections. Isi semantik, naturalitas, bukti gerak dan keselarasan audio tetap ditinjau AI/pengguna dari hasil aktual.

## Revisi, persetujuan dan ekspor

revision bilangan positif. Prompt gambar, aset, prompt video dan approval aktif harus sesuai revisi tersebut. Perubahan keputusan memerlukan peninjauan ulang, bukan hanya mengganti nomor aset lama. approval memuat revision, by user/delegated dan note dari keputusan sebenarnya; script tidak memberi persetujuan.

[Pembuat paket](../scripts/build_production_package.py) menerima image_prompt_package atau prompt_package yang valid. Paket pertama tidak disebut siap video; paket final menyertakan semua gambar dan peta referensi. Salinan divalidasi ulang, tujuan lama tidak ditimpa, file sumber tidak diubah.

Dari root paket:

~~~sh
python skills/produce-home-tour/scripts/validate_project.py /path/to/project.json
~~~

[Dependensi](../scripts/requirements.txt) menggunakan Python, PyYAML, jsonschema dan Pillow. Exit 0 valid secara struktural, 1 melanggar kontrak, 2 file/JSON tidak terbaca. Hasil juga menyebut jumlah gambar tersedia/direview dan batas pemeriksaan; bukan sertifikat kelulusan manual.
