# Kontrak paket 2.1

`audit.json` schema_version 2.1 adalah satu sumber audit; analysis.md hasil renderer 2.2.0; manifest.json contract_version 2.1 menyimpan provenance teknis. [Schema audit](audit-v2-1.schema.json), [manifest](manifest-v2-1.schema.json), [laporan](analysis-v2-2.md), [reader](ai-reader-v2-1.md).

Isi: audit.json, analysis.md, manifest.json, N media/shot-NN.jpg, media/overview.jpg, media/storyboard.jpg; source.mp4 opsional. Receipt di luar ZIP. Tidak ada JPEG frame lepas atau motion/. N adalah jumlah take kontinu, bukan jumlah area.

shots[].overviews[].composition_summary wajib satu paragraf biasa; Camera Start tetap shots[].composition. shots[].phases[].depth_direction wajib IN, OUT, NO IN/OUT atau null ambigu. Validator menolak arah berlawanan dengan Dolly eksplisit; tidak menentukan orbit/pan/zoom hanya dari nama. Pola turunan menggabungkan arah berturut sama, mempertahankan perubahan dan slot ambigu; bukan field manual audit.

Manifest panel menunjuk selection_id/frame/PTS/area dan bbox foto [x,y,w,h]. Media memiliki blocks (kosong kecuali Storyboard); setiap blok mencatat shot_id, bbox seluruh kolase, derived_from, scale. Metadata harus tepat sama dengan layout deterministik; caption bukan bbox foto. Selection boleh muncul di beberapa media tanpa membuat identitas bukti baru.

Render/media pasangan 2.2.0; hash template/font regular/bold/layout tercatat. Quality default91 (60–98), panel_scale/overview_scale/storyboard_scale default1 (0,1], columns multi default4 (1–6). Skala Storyboard berlaku pada seluruh blok, bbox mengikuti ukuran integer aktual. Tidak memperbesar sumber/crop konteks. Batas 60 juta piksel/gambar, sisi65000px, 95MiB/file, 256MiB ZIP/ekstraksi, 2000file, teks2MiB. Preflight sebelum alokasi, ukur byte sesudah encoding. Tidak mengurangi panel/font atau membagi file diam-diam.

Aturan sumber/10FPS/native, coverage, keamanan ZIP, supersedes/revisi +1, snapshot review/export byte identik dan ingest tanpa review isi ulang mengikuti [kontrak 2.0](package-v2.md). Paket 2.0 tetap renderer lamanya. Default draft: 2.0→2.1.2; 2.1→2.2.0. Semua schema mandiri tanpa resolusi jaringan.
