# Pembaca AI 2.3

Indeks ringkas → proyeksi referensi → shot/area dan media terpilih. Semua format1.0/1.1/2.0/2.1/2.2/2.3 tetap dibaca menurut sumbernya. Tidak ada konversi sumber.

Proyeksi2.3 mempertahankan audit.json termasuk camera_checks, scale_measurement dan facet_roles, status/negasi, uncertainty dan pointer asal. Camera Pattern hanya turunan depth_direction. Camera Start sumber dan Overview akhir OUT berbeda.

design_facets indeks berisi nilai/status/confidence/area_ids/facet_roles, pointer fakta dan role_source. Format2.3 memakai facet_roles eksplisit; format lama memakai sources/fact-facets.json, versi1.0. Label asli tidak diubah. Atribut belum dipetakan tetap di knowledge/topics dan proyeksi; daftar teknis ada di data/dependencies.json.unmapped_fact_attributes. Tidak ada inferensi prosa.

Indeks tidak menyalin camera_checks, motion_observations, ukuran piksel, log frame atau narasi lengkap. read --part shot menampilkan bukti rinci dan provenance. Semua evidence tetap terhubung inventory; media tersimpan dapat dibaca tanpa membuka MP4. Mode --native eksplisit memerlukan sumber kanonis.
