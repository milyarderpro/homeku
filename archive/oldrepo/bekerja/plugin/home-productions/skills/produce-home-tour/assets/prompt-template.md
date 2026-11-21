# Template R2V per shot

Isi sembilan sections dari gambar final dan rancangan aktif. Baca [panduan Omni Flash](../references/omni-flash.md). Kerangka ini bukan prompt siap pakai sampai semua penanda terisi.

~~~text
OUTPUT SPECIFICATION
{{HOME_TOUR_AREA_OR_TRANSITION}}. Duration {{DURATION_S}} seconds. Vertical 9:16.

REFERENCE IMAGE ROLE
Attached images provide visual and spatial references, not mandatory first or last frames.
{{VISUAL_ROLE_OF_ATTACHED_REFERENCE_WITHOUT_FILE_NAMES_OR_INTERNAL_IDS}}.

ARCHITECTURE AND DESIGN
{{APPROVED_STRUCTURE_SINGLE_SPATIAL_LAYOUT_CEILING_FIXTURES_MATERIALS_FURNITURE_AND_OPENINGS}}

CAMERA START COMPOSITION
{{START_POSITION_DIRECTION_SUBJECT_FOREGROUND_BACKGROUND_FROM_SPATIAL_PLAN}}

CAMERA MOVEMENT
{{SOURCE_COMPATIBLE_MOVEMENT_PATH_DISTANCE_ANGLE_SPEED_TIMING_AND_RELATIONSHIP}}

VISIBLE MOTION EVIDENCE
{{OBSERVABLE_CHANGES_FOR_EVERY_SELECTED_CAMERA_COMPONENT}}

ENDING COMPOSITION
{{ENDING_VIEW_GEOMETRICALLY_CONSISTENT_WITH_THE_PATH}}

VISUAL CONSISTENCY LOCK
{{FIXED_ROOM_AND_OBJECT_POSITIONS_SINGLE_KITCHEN_CEILING_FIXTURES_LIGHT_AND_ENVIRONMENT}}

CONTINUITY AND AUDIO RULES
One continuous shot with no cuts.
No jump cuts, sudden viewpoint changes, teleportation or morphing of the house and objects.
Soft natural ambient sound only. No music, narration, dialogue, or dramatic sound effects.
~~~

reference_image_ids pada metadata harus sama dengan shot. Jangan memasukkan nama file, path atau ID internal ke bagian prompt mana pun. Identitas lampiran dijelaskan secara visual; peta teknis berada di luar prompt.

Living-to-kitchen default satu foto gabungan. Exterior-to-living menerima pilihan pengguna 1 atau 2 referensi. Kedua pola tetap satu shot 6 detik, tanpa kewajiban menyalin gambar sebagai frame pembuka/penutup.

Pilih gerak dari DNA per area; tidak selalu dolly + pan. Pan/orbit terpilih ≥12°; jarak/sudut/fase/kecepatan masuk akal dalam durasi baku. Komposisi, lintasan dan akhir memakai tata ruang yang sama, bukan kitchen/ruang baru.

Di chat, satu prompt lengkap per fenced code block. Judul shot, catatan dan peta lampiran di luar block. File .txt menyimpan isi yang sama tanpa pagar Markdown. Jangan menyisipkan cut antarklip, musik, placeholder atau JSON.
