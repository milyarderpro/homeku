# Template R2V per shot

Isi sembilan sections pada kontrak proyek berdasarkan gambar final dan rancangan. Baca [panduan R2V](../references/omni-flash.md). Ini kerangka penulisan, bukan prompt final.

~~~text
OUTPUT SPECIFICATION
{{SHOT_ID_AND_HOME_TOUR}}. Duration {{DURATION_S}} seconds. Vertical 9:16.

REFERENCE IMAGE ROLE
{{EACH_IMAGE_ID_AND_ITS_AREA_ROLE}}. Use these as visual identity references for connected areas of the same approved house, not mandatory endpoint frames or alternative designs.

ARCHITECTURE AND DESIGN
{{APPROVED_ARCHITECTURE_CEILING_MATERIALS_FURNITURE_OPENINGS_AND_CONNECTIONS}}

CAMERA START COMPOSITION
{{START_POSITION_VIEW_DIRECTION_SUBJECT_FOREGROUND_BACKGROUND}}

CAMERA MOVEMENT
{{PLANNED_COMPONENTS_DISTANCE_ANGLE_TIMING_AND_RELATIONSHIP}}

VISIBLE MOTION EVIDENCE
{{VISIBLE_CHANGES_CAUSED_BY_THE_PLANNED_CAMERA_MOVEMENT}}

ENDING COMPOSITION
{{GEOMETRICALLY_PLAUSIBLE_ENDING_VIEW}}

VISUAL CONSISTENCY LOCK
{{FIXED_STRUCTURE_CEILING_OBJECTS_LIGHT_AND_ENVIRONMENT_TO_PRESERVE}}

CONTINUITY AND AUDIO RULES
{{CONTINUOUS_INSTRUCTION_FROM_RULES}}
No jump cuts, sudden viewpoint changes, teleportation or morphing of the house and objects.
{{AUDIO_INSTRUCTION_FROM_RULES}}
~~~

reference_image_ids pada prompt harus sama dengan shot. Sebut setiap ID di bagian peran referensi, dengan identitas areanya. Pada penghubung, dua gambar tetap dua file area untuk satu continuous shot. Komposisi akhir berasal dari lintasan, bukan kewajiban merekonstruksi piksel gambar kedua.

Salin instruksi continuous/audio dari [aturan](../references/production-rules.yaml) ke bagian terakhir. Ganti seluruh penanda sebelum menyimpan. Jarak/sudut adalah perkiraan rancangan; pan/orbit minimal 12° hanya ketika dipilih. Isi CAMERA MOVEMENT dan VISIBLE MOTION EVIDENCE harus cocok dengan camera.components, hubungan waktu serta durasi 6/4 detik.

Jangan menambahkan kalimat cut ke shot berikutnya, musik, slow yang bertentangan dengan lintasan, atau transformasi plafon/ruang. Catatan perangkaian berada di panduan proyek.
