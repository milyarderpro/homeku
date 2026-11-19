# Template satu gambar referensi

Isi satu prompt lengkap per pandangan di image_plan, berdasarkan desain dan composition yang sama dengan [lintasan](../references/preproduction.md). Baca [alur gambar](../references/image-workflow.md). Tidak menyerahkan placeholder yang belum diisi.

~~~text
Create one individual, natural architectural photograph of {{VISIBLE_AREA_OR_CONNECTED_LIVING_KITCHEN}} in the approved house.
House architecture, materials, furnishings and fixed spatial relationships: {{APPROVED_DESIGN_AREA_SPECS_CONNECTIONS_AND_ANCHORS}}.
Ceiling and visible functional light fixtures: {{APPROVED_CEILING_FIXTURE_TYPES_POSITIONS_AND_DAYLIGHT_OR_ON_STATE}}.
Camera position and height: {{CAMERA_POSITION_AND_HEIGHT}}.
Viewing direction and subject angle: {{VIEW_DIRECTION_SUBJECT_VIEW_AND_ANGLE}}.
Subject placement, foreground and background: {{SUBJECT_PLACEMENT_FOREGROUND_BACKGROUND_AND_DEPTH}}.
Required visible boundaries and composition: {{TYPE_SPECIFIC_FULL_EXTERIOR_OR_BEDROOM_DIAGONAL_OR_CONNECTED_SPACE_COMPOSITION}}.
Spatial alignment with the planned video path: {{LAYOUT_NOTE_AND_SHOT_ALIGNMENT_WITHOUT_MOVING_FIXED_OBJECTS}}.
Lighting and surroundings: {{APPROVED_LIGHT_ENVIRONMENT}}.
Show an informative wide view with plausible photographic perspective, proportions, textures, natural light, reflections and shadows.
Preserve the approved geometry and positions. This is a visual and spatial reference, not a required first or last video frame.
One photograph only: no collage, split panels or labels; no plastic CGI appearance, excessive HDR, extreme fisheye, transparent walls or impossible cutaways.
~~~

Untuk exterior, isi batas atap, kiri/kanan dan dasar rumah seluruhnya dengan margin; sudut kamera fleksibel. Untuk bedroom, front three-quarter 35–45° horizontal terhadap sumbu panjang bed, bed memanjang diagonal; jangan memutar bed atau roll. Untuk living-to-kitchen, satu pandangan utuh living+kitchen yang terhubung dengan satu kitchen tetap.

Setiap interior mempunyai plafon dan armatur lampu yang dirancang; tidak semua lampu wajib menyala. Jika memakai satu foto exterior untuk exterior-to-living, jangan memaksa seluruh interior tampak di foto yang sama.

Kedua mode memakai spesifikasi yang sama. Satu prompt menghasilkan satu gambar individual; seluruh batch mengikuti jumlah yang disetujui, bukan satu kolase.
