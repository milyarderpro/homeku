# Template satu gambar area

Gunakan satu prompt lengkap untuk satu image_id dalam image_plan. Isi dari desain yang disetujui dan [alur gambar](../references/image-workflow.md); jangan menyerahkan penanda yang belum diisi.

~~~text
Create one individual, natural architectural photograph of {{AREA_AND_ID}} in the approved house.
House design and spatial relationships: {{ARCHITECTURE_LAYOUT_CONNECTIONS}}.
Ceiling and fixed structure for this area: {{CEILING_OPENINGS_FIXED_ELEMENTS}}.
Materials and principal furniture: {{MATERIALS_FURNITURE}}.
Lighting and surroundings: {{LIGHT_ENVIRONMENT}}.
Show a wide, informative overview of the area, including the relevant floor, ceiling, openings and furniture relationships.
Composition and reference role: {{COMPOSITION_AND_REFERENCE_ROLE}}.
Keep the approved geometry, proportions and object positions. Use plausible photographic perspective, textures, light, reflections and shadows.
No collage, split panels, labels, artificial CGI/plastic appearance, extreme fisheye, transparent walls or impossible cutaway views.
~~~

Semua prompt dalam batch memakai keputusan rumah yang sama, dengan plafon/elemen tiap area yang sesuai rancangan. Jangan membuat rancangan berbeda secara independen untuk setiap gambar. Full area berarti overview yang wajar, bukan seluruh sisi terhalang terlihat sekaligus.

Pada prompt_to_image, serahkan seluruh prompt. Pada generate_image, gunakan prompt ini sebagai tugas tiap gambar dalam batch yang diminta; jangan mengubah tujuh gambar menjadi satu kolase. Referensi visual yang dipakai harus benar-benar dilampirkan melalui alat, bukan hanya disebut namanya.
