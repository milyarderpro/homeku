# Kontrak paket 2.3

audit.json2.3 satu sumber isi, manifest2.3 metadata, report2.2.2 laporan manusia, media2.2.0; reader/index2.3. Kontrak2.2 tetap berlaku kecuali perubahan eksplisit berikut. Sumber lama tidak dikonversi.

ZIP final hanya audit.json, analysis.md, manifest.json dan N+2 JPEG. Video termasuk source.mp4 dilarang; MP4 input terpisah dan sumber lokal kanonis video/<id>.mp4 wajib cocok hash. Receipt dan catatan/frame kerja di luar ZIP. Review mengikat seluruh byte snapshot; export tidak merender ulang. Batas ukuran/supersedes mengikuti package-v2-1.md.

Baseline6FPS seluruh shot dengan frame native pertama/terakhir. Sumber≤6FPS dan shot<1detik memakai seluruh native. Sampling di bawah6 hanya tambahan, bukan coverage. Pendalaman10FPS/native menjawab pertanyaan visual pada rentang terkait; boleh langsung native. Selected bukan viewed. Log alasan tidak kosong; semua evidence harus viewed. Toleransi evidence fase: maksimal satu interval native di batas, tetap dalam shot, dengan minimal satu frame di dalam fase.

phases[].camera_checks wajib depth/translation/rotation, masing-masing evidence dan basis, minimal dua frame fisik berbeda, juga tercantum evidence fase. Tidak ada verdict kedua: depth_direction dan components_parsed tetap keputusan kanonis. Pan/Static/Uncertain juga diperiksa; tidak dipaksa Dolly. Metode keputusan tunggal di audit/visual-audit.md.

motion_observations[].scale_measurement nullable; wajib saat notasi ~× dinyatakan. Objek berisi anchor, dimension width/height, start_evidence, end_evidence, start_px, end_px. Piksel di resolusi sumber; objek/bagian sama harus utuh kedua frame. Evidence berurutan, berbeda, dalam observasi/fase/viewed. IN=end_px/start_px; OUT=start_px/end_px. Rasio >1, notasi satu desimal atau rentang yang mencakup hasil (toleransi pembulatan0.05). Rasio ini perubahan skala, bukan faktor kecepatan/jarak. Validator memeriksa angka/pointer, tidak memastikan anchor utuh atau makna gambar.

Pan/Orbit memerlukan estimate_basis baik ada sudut maupun tidak; tanpa angka jelaskan kendala khusus. Dolly/Zoom tanpa ~× juga memerlukan alasan keterbatasan. Jika Dolly+Zoom tak terpisahkan, jangan mengatribusikan rasio total pada keduanya: null pengukuran/angka yang tidak terpisahkan dan jelaskan batas pada estimate_basis/uncertainty. Gerakan tanpa satuan itu tidak dipaksa angka.

facts[].facet_roles daftar peran eksplisit, boleh kosong untuk fakta nonstruktural. Label asli/status/negasi tetap utuh. Peran terbuka berbentuk slug, bukan whitelist tertutup. Format lama memakai sources/fact-facets.json terkurasi; aturan/pointer dicatat pada facet turunan, tidak menulis ulang fakta.

Semua shot boleh moderate/constant. tempo fase cocok tempo_profile; accelerating/decelerating tidak boleh bertentangan dengan urutan label yang diketahui. Tempo fisik tidak disimpulkan dari pembesaran perspektif saja. Pemeriksaan gambar/makna tetap tanggung jawab audit AI; validator tidak menjamin kebenaran visual.

Identitas English, estimasi luas wajib, fact_coverage, enam bagian MD dan snapshot berlaku seperti2.2. analysis.md hanya renderer2.2.2, tidak diedit manual; data checks/pengukuran tetap JSON.
