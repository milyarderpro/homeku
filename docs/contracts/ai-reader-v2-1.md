# Pembaca AI 2.1

Proyeksi/index 2.1 membaca sumber1.0/1.1/2.0/2.1; generator4. [Schema reader](reference-reader-v2-1.schema.json), [index](search-index-v2-1.schema.json). Sumber lama tidak dilengkapi klasifikasi/komposisi rekaan.

Cari indeks ringkas → read identity → shot/area → panel/shot-image. Identity tidak membawa seluruh shot/media. Area read tetap membawa route/fase/tempo seluruh take. Overview paragraf sama dengan sumber; Camera Start terpisah. Pola/provenance diturunkan dari depth_direction fase, null bila ambigu; satu slot per shot, campuran dikurung. Tampilan null memakai —. Tidak menjalankan sintesis AI.

Evidence inventory menyimpan metadata frame/area sekali dan locations [{path,kind,bbox,scale}]. Primary path/bbox/scale dipilih berdasarkan piksel foto tertinggi, lalu shot-collage → overview → storyboard, path/bbox stabil. Native-only menunjuk video kanonis. Provenance mempertahankan JSON Pointer sumber dan evidence_ids; turunan menunjuk fase asal.

`python tools/library.py panel ID SELECTION --output /tmp/panel.jpg` crop foto tersimpan tanpa MP4. --native eksplisit meminta MP4 terikat hash. `shot-image ID shot-NN --output /tmp/shot.jpg` menyalin kolase; --from-storyboard crop seluruh blok dari bbox tanpa MP4. Output di luar repo. Indeks membawa pola/rujukan/ID Overview, bukan paragraf/desain/media penuh. Turunan dibangun generator, bukan diedit manual.
